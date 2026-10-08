"""ぼかした画像を、エージェント型の LLM ツール（読み手）に読ませ、何が伝わったかを再構成させる。

読み手のコマンドは、プロジェクトのルートの cyrus.config.json（vision.reader）で決める。
設定ファイルがなければ、agy 経由で Gemini に読ませる。原稿を書いた Claude とは別のモデルに読ませることで、
書き手と同じモデルが読み手を演じる偏りを避けるためである。

どのコマンドでも、読み手には画像だけを渡す。画像は、プロジェクトと無関係な一時ディレクトリにコピーし、
そこを作業ディレクトリにして起動する。原稿やその他の成果物のパスは知らせない
（agy の --sandbox はファイルの読み取りを制限しないため、置き場所で隔離する）。

読み取り専用で起動すること（権限確認を省略しない、plan モードにする、使えるツールを絞る）は、
コマンドの書き方で決まる。既定の agy は、権限確認を省略せず、読み取り専用の plan モードで起動する。
ヘッドレス実行では確認が必要な操作（シェルコマンドなど）は自動で拒否され、
ワークスペース内のファイル閲覧だけが使える。
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

from .workspace import project_root

CONFIG_NAME = "cyrus.config.json"
RESULT_NAME = "reader-result.json"  # skim/visual/ に保存する、読み手の回答
DEFAULT_MODEL = "gemini-3.8-flash-medium"
DEFAULT_TIMEOUT = 900
MAX_PAGES = 12

# コマンドの引数に書ける置き換え。{prompt} がどの引数にもなければ、プロンプトは標準入力で渡す。
PLACEHOLDERS = ("prompt", "workdir", "schema", "schema_file", "model", "timeout")
PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_]+)\}")
READER_KEYS = ("name", "command", "model", "env", "timeout")
# 読み手の出力（JSON）のうち、回答が入っている項目。前から順に探す。
RESULT_FIELDS = ("structured_output", "response", "result")

LEVEL_JA = {"novice": "この分野の初心者", "intermediate": "基本は知っている中級者", "expert": "この分野の専門家"}

SCHEMA = {
    "type": "object",
    "properties": {
        "reader_summary": {"type": "string", "description": "文書が全体として言っていること（2〜3文）"},
        "main_point": {"type": "string", "description": "書き手がいちばん伝えたいこと（1文）"},
        "requested_action": {"type": "string", "description": "読者に求めている行動。わからなければ「不明」"},
        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "heading": {"type": "string"},
                    "understood": {"type": "string", "description": "この節で言っていると思うこと（1文）"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                },
                "required": ["heading", "understood", "confidence"],
            },
        },
        "confusing_points": {"type": "array", "items": {"type": "string"}},
        "visual_notes": {
            "type": "object",
            "properties": {
                "stood_out": {"type": "array", "items": {"type": "string"}, "description": "目に飛び込んできたもの"},
                "missed_or_hidden": {"type": "array", "items": {"type": "string"}, "description": "重要そうなのに目立たなかったもの"},
                "layout_issues": {"type": "array", "items": {"type": "string"}, "description": "見た目の構造でわかりにくかった点"},
            },
            "required": ["stood_out", "missed_or_hidden", "layout_issues"],
        },
    },
    "required": ["reader_summary", "main_point", "requested_action", "sections", "confusing_points", "visual_notes"],
}


class ReaderUnavailable(RuntimeError):
    """読み手を起動できない、または読み手の回答を読めない。"""


class ReaderConfigError(ReaderUnavailable):
    """設定ファイルの書き方に誤りがある。"""


@dataclass
class ReaderConfig:
    name: str
    command: list[str]
    model: str | None = None
    env: dict[str, str | None] = field(default_factory=dict)  # None は「その変数を消して起動する」
    timeout: int = DEFAULT_TIMEOUT
    source: Path | None = None  # 設定ファイルの場所。None なら既定の agy

    @property
    def prompt_via_stdin(self) -> bool:
        return not any("{prompt}" in a for a in self.command)

    @property
    def schema_given(self) -> bool:
        """スキーマをコマンドで渡しているか（渡していなければ、プロンプトに書く）。"""
        return any("{schema}" in a or "{schema_file}" in a for a in self.command)


# ---------------------------------------------------------------- 設定


def config_path() -> Path:
    env = os.environ.get("CYRUS_CONFIG")
    return Path(env) if env else project_root() / CONFIG_NAME


def _default_reader() -> ReaderConfig:
    agy = os.environ.get("CYRUS_AGY")
    if not (agy and Path(agy).exists()):
        agy = "agy"
    command = [agy, "-p", "{prompt}", "--add-dir", "{workdir}", "--mode", "plan",
               "--output-format", "json", "--json-schema", "{schema}",
               "--model", "{model}", "--print-timeout", "{timeout}s"]
    return ReaderConfig("Gemini（agy）", command, os.environ.get("CYRUS_AGY_MODEL") or DEFAULT_MODEL)


def _expand(s: str) -> str:
    return os.path.expandvars(os.path.expanduser(s))


def load_config(path: Path | None = None) -> ReaderConfig:
    """読み手の設定を読む。

    command を書かなければ既定の agy を使い、name・model・env・timeout だけを上書きできる。
    command を書いたら、model は書いたときだけ使い、name は省略するとコマンドの名前になる。
    """
    path = path or config_path()
    if not path.exists():
        if os.environ.get("CYRUS_CONFIG"):
            raise ReaderConfigError(f"環境変数 CYRUS_CONFIG が指す設定ファイル {path} がありません。")
        return _default_reader()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ReaderConfigError(f"{path} を JSON として読めません: {e}") from e
    if not isinstance(data, dict):
        raise ReaderConfigError(f"{path} の中身は JSON のオブジェクトにしてください。")
    vision = data.get("vision", {})
    sec = vision.get("reader", {}) if isinstance(vision, dict) else None
    if not isinstance(sec, dict):
        raise ReaderConfigError(f"{path} の vision と vision.reader は、オブジェクトにしてください。")
    unknown = [k for k in sec if k not in READER_KEYS]
    if unknown:
        raise ReaderConfigError(f"{path} の vision.reader に知らない項目があります: {', '.join(unknown)}"
                                f"（書けるのは {', '.join(READER_KEYS)}）")

    if "command" in sec:
        command = sec["command"]
        if not (isinstance(command, list) and command and all(isinstance(a, str) and a for a in command)):
            raise ReaderConfigError(f"{path} の vision.reader.command は、空でない文字列のリストにしてください"
                                    "（例: [\"claude\", \"-p\", \"{prompt}\"]）。")
        cfg = ReaderConfig(Path(command[0]).name, [_expand(a) for a in command])
    else:
        cfg = _default_reader()
    cfg.source = path

    if "name" in sec:
        if not (isinstance(sec["name"], str) and sec["name"].strip()):
            raise ReaderConfigError(f"{path} の vision.reader.name は、空でない文字列にしてください。")
        cfg.name = sec["name"].strip()
    if "model" in sec:
        if sec["model"] is not None and not isinstance(sec["model"], str):
            raise ReaderConfigError(f"{path} の vision.reader.model は、文字列か null にしてください。")
        cfg.model = sec["model"] or None
    if "timeout" in sec:
        t = sec["timeout"]
        if isinstance(t, bool) or not isinstance(t, int) or t <= 0:
            raise ReaderConfigError(f"{path} の vision.reader.timeout は、正の整数（秒）にしてください。")
        cfg.timeout = t
    if "env" in sec:
        env = sec["env"]
        if not isinstance(env, dict) or any(v is not None and not isinstance(v, str) for v in env.values()):
            raise ReaderConfigError(f"{path} の vision.reader.env は、変数名から文字列（消すときは null）への"
                                    "オブジェクトにしてください。")
        cfg.env = {k: (None if v is None else _expand(v)) for k, v in env.items()}

    for a in cfg.command:
        for name in PLACEHOLDER_RE.findall(a):
            if name not in PLACEHOLDERS:
                raise ReaderConfigError(f"{path} の vision.reader.command に知らない置き換え {{{name}}} があります"
                                        f"（使えるのは {', '.join('{' + p + '}' for p in PLACEHOLDERS)}）。")
    return cfg


def child_env(cfg: ReaderConfig) -> dict[str, str]:
    env = dict(os.environ)
    for k, v in cfg.env.items():
        if v is None:
            env.pop(k, None)
        else:
            env[k] = v
    return env


def find_command(cfg: ReaderConfig) -> str | None:
    return shutil.which(cfg.command[0], path=child_env(cfg).get("PATH"))


def available() -> bool:
    """読み手のコマンドがこの環境で使えるか。設定ファイルに誤りがあれば ReaderConfigError。"""
    return find_command(load_config()) is not None


def build_command(cfg: ReaderConfig, values: dict[str, str]) -> list[str]:
    """コマンドの置き換えを埋める。値に { } が含まれていても二重には置き換えない。"""
    if any("{model}" in a for a in cfg.command) and not values.get("model"):
        raise ReaderConfigError("コマンドに {model} がありますが、モデルが決まっていません。"
                                "設定ファイルの vision.reader.model か、`cyrus vision --model` で指定してください。")
    return [PLACEHOLDER_RE.sub(lambda m: values[m.group(1)], a) for a in cfg.command]


def describe(cfg: ReaderConfig, model: str | None = None) -> list[str]:
    """設定の中身を、読み手を起動せずに確かめるための説明。環境変数は値を出さない（鍵が入りうるため）。"""
    model = model or cfg.model
    shown = {"prompt": "<プロンプト>", "workdir": "<画像だけを置いた一時ディレクトリ>",
             "schema": "<回答の JSON スキーマ>", "schema_file": "<回答の JSON スキーマのファイル>",
             "model": model or "<モデル未指定>", "timeout": str(cfg.timeout)}
    lines = [
        f"設定ファイル: {cfg.source or f'なし（{CONFIG_NAME} がないので、既定の agy を使う）'}",
        f"読み手: {cfg.name}",
        f"モデル: {model or '（指定なし）'}",
        "コマンド: " + shlex.join(PLACEHOLDER_RE.sub(lambda m: shown[m.group(1)], a) for a in cfg.command),
        f"実行ファイル: {find_command(cfg) or '見つかりません'}",
        "プロンプト: " + ("標準入力で渡す" if cfg.prompt_via_stdin else "引数で渡す")
        + ("（回答の形もプロンプトに書く）" if not cfg.schema_given else ""),
        f"時間の上限: {cfg.timeout}秒",
    ]
    set_keys = [k for k, v in cfg.env.items() if v is not None]
    unset_keys = [k for k, v in cfg.env.items() if v is None]
    if set_keys:
        lines.append(f"設定する環境変数: {', '.join(set_keys)}")
    if unset_keys:
        lines.append(f"消す環境変数: {', '.join(unset_keys)}")
    return lines


# ---------------------------------------------------------------- プロンプト


def build_prompt(reader: dict | None, page_names: list[str], has_overview: bool, truncated: bool,
                 schema_in_prompt: bool = False) -> str:
    reader = reader or {}
    p = reader.get("persona") or {}
    ctx = reader.get("reading_context") or {}
    who = p.get("role") or "この文書の想定読者"
    lines = [
        f"あなたは「{who}」です。" + (f"{p['background']}。" if p.get("background") else ""),
        f"知識の程度: {LEVEL_JA.get(reader.get('knowledge_level'), '基本は知っている中級者')}。",
        f"この文書を読む理由: {reader['motivation']}" if reader.get("motivation") else "",
        f"使える時間はおよそ{ctx['time_budget_min']}分です。" if ctx.get("time_budget_min") else "",
        "",
        "この作業ディレクトリにある画像は、ある文書を画面で読んだときの見え方です。",
        f"- {page_names[0]} 〜 {page_names[-1]}: 文書を上から順にスクロールした各画面です。"
        "読み手の目が留まった箇所（見出し、段落の最初の文、太字、箇条書きの頭、図表のキャプション）だけがくっきり見え、"
        "その周りは少しぼやけ、それ以外は読めないほどぼやけています。拾い読みしたときの見え方を模したものです。",
    ]
    if has_overview:
        lines.append("- overview.png: 文書全体を縮小したもので、一瞥したときの見え方です。")
    if truncated:
        lines.append(f"- 文書は長いため、最初の{len(page_names)}画面だけを渡しています。")
    lines += [
        "",
        "画像は、ファイルを開くツール（view_file、Read など）で1枚ずつ開いて見てください。シェルコマンドは使わないでください。",
        "",
        "次のことを守ってください。",
        "- この作業ディレクトリの画像以外のファイルは読まないでください。検索もしないでください。",
        "- ぼやけて読めない部分を、推測で補いすぎないでください。確信が持てないことは「不明」と書いてください。",
        "- 読み手として、画像から実際に読み取れたことだけを答えてください。",
        "",
        "画像をすべて見たうえで、次のことを答えてください。",
        "1. この文書が全体として何を言っているか（reader_summary）",
        "2. 書き手がいちばん伝えたいこと（main_point）と、読者に求めている行動（requested_action）",
        "3. 見出しごとに、その節が言っていると思うこと（sections）",
        "4. 拾い読みでは意味がつかめなかった箇所（confusing_points）",
        "5. 見た目について: 目に飛び込んできたもの、重要そうなのに目立たなかったもの、見た目の構造でわかりにくかった点（visual_notes）",
        "",
        "回答はすべて日本語で書いてください。",
    ]
    if schema_in_prompt:
        lines += [
            "回答は、次の JSON スキーマに合う JSON オブジェクトだけを出力してください。",
            json.dumps(SCHEMA, ensure_ascii=False),
        ]
    return "\n".join(l for l in lines if l is not None)


# ---------------------------------------------------------------- 回答の取り出し


def _looks_like_result(obj) -> bool:
    return isinstance(obj, dict) and ("reader_summary" in obj or "visual_notes" in obj)


def _json_object(text: str) -> dict | None:
    """出力全体か、最後の { で始まる行を JSON のオブジェクトとして読む。"""
    try:
        whole = json.loads(text)
        if isinstance(whole, dict):
            return whole
    except json.JSONDecodeError:
        pass
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                return obj
    return None


def _result_in_text(text: str) -> dict | None:
    """文章の中から回答の JSON を探す（```json の囲み、全体、最初の { から最後の } まで、の順）。"""
    candidates = re.findall(r"```(?:json)?\s*\n(.*?)\n```", text, re.S)
    candidates.append(text.strip())
    if "{" in text and "}" in text:
        candidates.append(text[text.index("{"): text.rindex("}") + 1])
    for c in candidates:
        try:
            obj = json.loads(c)
        except json.JSONDecodeError:
            continue
        if _looks_like_result(obj):
            return obj
    return None


def parse_output(stdout: str) -> tuple[dict, dict]:
    """読み手の標準出力から、回答と、回答を包んでいた情報（使用量など）を取り出す。

    agy や Claude Code の JSON 出力（structured_output・response・result）にも、
    回答の JSON だけを出す読み手にも、文章の中に ```json で回答を書く読み手にも対応する。
    """
    envelope = _json_object(stdout)
    if envelope is not None:
        if _looks_like_result(envelope):
            return envelope, {}
        meta = {k: v for k, v in envelope.items() if k not in RESULT_FIELDS}
        for k in RESULT_FIELDS:
            v = envelope.get(k)
            if _looks_like_result(v):
                return v, meta
            if isinstance(v, str):
                found = _result_in_text(v)
                if found is not None:
                    return found, meta
        texts = [str(envelope.get(k)) for k in RESULT_FIELDS if envelope.get(k) is not None]
        raise ReaderUnavailable("読み手が、決まった形の回答を返しませんでした: "
                                + (texts[0] if texts else json.dumps(envelope, ensure_ascii=False))[:400])
    found = _result_in_text(stdout)
    if found is not None:
        return found, {}
    raise ReaderUnavailable(f"読み手の出力から回答の JSON を見つけられませんでした: {stdout.strip()[:400]}")


def _validate(result: dict) -> None:
    missing = [k for k in SCHEMA["required"] if k not in result]
    if missing:
        raise ReaderUnavailable(f"読み手の回答に {', '.join(missing)} がありません。"
                                "回答の形を守らせるには、コマンドに {schema} か {schema_file} を渡す引数を足してください。")
    if not isinstance(result.get("sections"), list) or not isinstance(result.get("visual_notes"), dict):
        raise ReaderUnavailable("読み手の回答の sections はリスト、visual_notes はオブジェクトにしてください。")


# ---------------------------------------------------------------- 実行


def run(pages: list[Path], overview: Path | None, reader: dict | None, model: str | None = None,
        cfg: ReaderConfig | None = None) -> dict:
    cfg = cfg or load_config()
    model = model or cfg.model
    exe = find_command(cfg)
    if not exe:
        where = f"{cfg.source} の vision.reader.command" if cfg.source else f"{CONFIG_NAME} か環境変数 CYRUS_AGY"
        raise ReaderUnavailable(f"読み手のコマンド {cfg.command[0]} が見つかりません（{where} で指定できます）。")
    truncated = len(pages) > MAX_PAGES
    use = pages[:MAX_PAGES]
    # 作業ディレクトリには画像だけを置く。スキーマのファイルは別の一時ディレクトリに置く。
    with tempfile.TemporaryDirectory(prefix="cyrus-reader-") as td, \
            tempfile.TemporaryDirectory(prefix="cyrus-schema-") as sd:
        work = Path(td)
        for p in use:
            shutil.copyfile(p, work / p.name)
        if overview and overview.exists():
            shutil.copyfile(overview, work / "overview.png")
        schema = json.dumps(SCHEMA, ensure_ascii=False)
        schema_file = Path(sd) / "schema.json"
        schema_file.write_text(schema, encoding="utf-8")
        prompt = build_prompt(reader, [p.name for p in use], bool(overview and overview.exists()), truncated,
                              schema_in_prompt=not cfg.schema_given)
        argv = build_command(cfg, {"prompt": prompt, "workdir": str(work), "schema": schema,
                                   "schema_file": str(schema_file), "model": model or "",
                                   "timeout": str(cfg.timeout)})
        argv[0] = exe
        stdin = {"input": prompt} if cfg.prompt_via_stdin else {"stdin": subprocess.DEVNULL}
        started = time.time()
        try:
            proc = subprocess.run(argv, cwd=str(work), capture_output=True, text=True, timeout=cfg.timeout + 60,
                                  env=child_env(cfg), **stdin)
        except subprocess.TimeoutExpired as e:
            raise ReaderUnavailable(f"{cfg.name} が {cfg.timeout} 秒以内に終わりませんでした。") from e
        except OSError as e:
            raise ReaderUnavailable(f"{cfg.name} を起動できませんでした: {e}") from e
    try:
        result, meta = parse_output(proc.stdout or "")
    except ReaderUnavailable as e:
        detail = (proc.stderr or "").strip()[:400]
        raise ReaderUnavailable(f"{e}（終了コード {proc.returncode}）" + (f"\n標準エラー: {detail}" if detail else "")) from e
    for k in ("toolAction", "toolSummary"):  # agy が回答に混ぜてくる項目
        result.pop(k, None)
    _validate(result)
    return {
        "reader": cfg.name,
        "model": model,
        "exit_code": proc.returncode,
        "duration_seconds": round(time.time() - started, 1),
        "pages_given": [p.name for p in use],
        "truncated": truncated,
        "meta": meta,
        "result": result,
    }
