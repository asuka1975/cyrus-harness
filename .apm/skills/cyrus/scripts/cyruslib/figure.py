"""図表を visual-patterns スキルにつなぐ。

- ステージ10: 10-detail.json の figure / table ブロックの spec（問い・答え・根拠の形・趣旨・パターン）を、
  カタログの規則（taxonomy.md の手順2・5・6）で検査する。検査そのものはスキルの vp_figure.py が受け持つ。
- ステージ11: draft.md の図表（Mermaid・PNG・表）とキャプションが設計どおりかを照合する。Vega-Lite の仕様を PNG にする。
- ステージ12: 図表だけを一枚ずつ画像にして、原稿を知らない読み手に読ませる（逆読み。手順9）。
  答えとの照合は cyrus-alignment-judge が行い、結果は 12-cogload.json の figure_test に記録する。
"""

from __future__ import annotations

import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from . import jatext, mdparse, skim
from .issues import Issue, excerpt
from .workspace import SKILL_DIR, Workspace, project_root

SKILL_NAME = "visual-patterns"
SCRIPT_REL = Path("scripts") / "vp_figure.py"
FIGURES_DIR = "figures"            # documents/<slug>/figures/: Vega-Lite の仕様（*.vl.json）と描いた PNG
READ_DIR = Path("skim") / "figures"  # 逆読み用に切り出した画像と、読み手の回答
RESULT_NAME = "reader-result.json"
KIND_LABEL = {"figure": "図", "table": "表"}
# spec.render ごとに、キャプションの前後にあるべきブロック
SOURCE_FOR_RENDER = {"mermaid": "mermaid", "vega-lite": "image", "image": "image", "markdown-table": "table"}
SOURCE_JA = {"mermaid": "Mermaid のコードブロック", "image": "画像", "table": "表"}
# キャプションは「図N: …」「表N: …」（区切りはコロンかピリオド）。「図 1 のとおり」のような参照の文を拾わないよう、空白だけの区切りは認めない
CAPTION_RE = re.compile(r"^\s*(図|表)\s*([0-9０-９]+)\s*[：:．.]\s*(.*?)\s*$")
ZEN2HAN = str.maketrans("０１２３４５６７８９", "0123456789")
MERMAID_LINES_WARN = 40
VERDICTS = ("match", "partial", "mismatch", "misread")
PREFERS = ("yes", "no", "either")


# ---------------------------------------------------------------- スキルの場所


def find_skill() -> Path | None:
    env = os.environ.get("CYRUS_VISUAL_PATTERNS")
    if env:
        return Path(env) if (Path(env) / SCRIPT_REL).exists() else None
    # APM は同じパッケージのスキルを cyrus と同じ skills/ に置く
    for cand in (SKILL_DIR.parent / SKILL_NAME, project_root() / ".claude" / "skills" / SKILL_NAME):
        if (cand / SCRIPT_REL).exists():
            return cand
    return None


_modules: dict[str, object] = {}


def vp():
    """スキルの vp_figure モジュール。見つからなければ None。"""
    skill = find_skill()
    if skill is None:
        return None
    key = str(skill)
    if key not in _modules:
        name = f"cyrus_vp_figure_{len(_modules)}"
        spec = importlib.util.spec_from_file_location(name, skill / SCRIPT_REL)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod  # dataclass が型注釈を解決するときに、モジュールが登録されている必要がある
        spec.loader.exec_module(mod)
        _modules[key] = mod
    return _modules[key]


def missing_skill_issue(rule: str = "GT101") -> Issue:
    return Issue(rule, "error", "visual-patterns スキルが見つかりません。`apm install` で入れてください"
                                "（場所は環境変数 CYRUS_VISUAL_PATTERNS で指定できます）。")


# ---------------------------------------------------------------- 設計（10-detail.json）


@dataclass
class Planned:
    label: str     # 図1 / 表1（kind ごとに、設計に現れた順）
    kind: str      # figure / table
    section: str
    block: dict

    @property
    def spec(self) -> dict:
        s = self.block.get("spec")
        return s if isinstance(s, dict) else {}

    @property
    def answer(self) -> str:
        a = self.spec.get("answer")
        return a if isinstance(a, str) else ""


def _blocks(detail: dict | None):
    """10-detail.json の (節, ブロック) の組。どちらもオブジェクトのものだけ（LLM の書き損じで落ちないように）。"""
    if not isinstance(detail, dict):
        return
    for s in detail.get("sections") or []:
        if not isinstance(s, dict):
            continue
        for b in s.get("blocks") or []:
            if isinstance(b, dict):
                yield s, b


def planned(detail: dict | None) -> list[Planned]:
    out: list[Planned] = []
    n = {"figure": 0, "table": 0}
    for s, b in _blocks(detail):
        k = b.get("kind")
        if k in KIND_LABEL:
            n[k] += 1
            out.append(Planned(f"{KIND_LABEL[k]}{n[k]}", k, str(s.get("id", "")), b))
    return out


def check_detail(detail: dict | None, reader_level: str | None = None, chrome: bool | None = None) -> list[Issue]:
    """figure / table ブロックの spec を、カタログの規則で検査する。"""
    items = planned(detail)
    mod = vp()
    if mod is None:
        return [missing_skill_issue()] if items else []
    index, routes = mod.load_index(), mod.load_routes()
    if chrome is None:
        chrome = mod.find_chrome() is not None
    issues: list[Issue] = []
    for it in items:
        for i in mod.check_spec(it.spec, it.kind, index, routes, reader_level, chrome):
            issues.append(Issue(i.rule, i.severity, f"節 {it.section} の{it.label}: {i.message}"))
    # 文章にしたブロックに spec を書いてあり、手順2 の目安では図表になるなら知らせる（迷ったときの判断材料）
    for s, b in _blocks(detail):
        if b.get("kind") not in KIND_LABEL and isinstance(b.get("spec"), dict):
            ok, why = mod.figure_warranted(b["spec"].get("evidence"))
            if ok:
                issues.append(Issue("VP021", "info", f"節 {s.get('id')} の {b.get('kind')} ブロック: 手順2 の目安では図表にします（{why}）。"
                                                     "文章を選んだ理由を plan に書いてください。"))
    return issues


# ---------------------------------------------------------------- 原稿（draft.md）


@dataclass
class Found:
    label: str
    kind: str
    n: int
    caption: str
    line: int
    source: str = ""     # mermaid / image / table / ""
    src: str = ""        # 画像のパス、Mermaid のテキスト、表の Markdown
    block_line: int = 0


def _claim(f: Found, b: mdparse.Block) -> bool:
    if b.kind == "code" and b.lang == "mermaid":
        f.source, f.src, f.block_line = "mermaid", b.text, b.line
    elif b.kind == "image":
        f.source, f.src, f.block_line = "image", b.src, b.line
    elif b.kind == "table":
        f.source, f.src, f.block_line = "table", b.text, b.line
    else:
        return False
    return True


def draft_figures(text: str) -> list[Found]:
    """原稿の図表（キャプション「図N: …」「表N: …」と、その前後の Mermaid・画像・表）を集める。"""
    blocks = mdparse.parse(text)
    out: list[Found] = []
    seen: set[str] = set()
    claimed: set[int] = set()  # すでに別のキャプションが取ったブロック（キャプションを図の上に置く書き方でも取り違えない）
    for i, b in enumerate(blocks):
        if b.kind != "paragraph":
            continue
        m = CAPTION_RE.match(jatext.strip_inline(b.text))
        if not m:
            continue
        n = int(m.group(2).translate(ZEN2HAN))
        f = Found(f"{m.group(1)}{n}", "figure" if m.group(1) == "図" else "table", n, m.group(3), b.line)
        if f.label in seen:  # 同じ番号のキャプションが二つ: 最初のものを採り、二つ目は数えない
            continue
        for j in (i - 1, i + 1):
            if 0 <= j < len(blocks) and j not in claimed and _claim(f, blocks[j]):
                claimed.add(j)
                break
        out.append(f)
        seen.add(f.label)
    # 画像の代替テキストがキャプションを兼ねている場合
    for b in blocks:
        if b.kind != "image":
            continue
        m = CAPTION_RE.match(jatext.strip_inline(b.text))
        if m:
            n = int(m.group(2).translate(ZEN2HAN))
            label = f"{m.group(1)}{n}"
            if label not in seen:
                out.append(Found(label, "figure", n, m.group(3), b.line, "image", b.src, b.line))
                seen.add(label)
    return sorted(out, key=lambda f: f.line)


def _norm(s: str) -> str:
    """照合用に、空白と句読点・括弧を落とす。数字の間の小数点とカンマ（1.5、1,200）は意味があるので残す。"""
    s = re.sub(r"[\s。、：:「」『』（）()]", "", jatext.strip_inline(s))
    return re.sub(r"(?<!\d)[．.，,]|[．.，,](?!\d)", "", s)


def image_paths(ws: Workspace, text: str) -> list[Path]:
    """原稿が参照する、文書のディレクトリの中の画像。"""
    out = []
    for b in mdparse.parse(text):
        if b.kind == "image":
            p = _local(ws, b.src)
            if p is not None and p not in out:
                out.append(p)
    return out


def assets_hash(ws: Workspace, text: str) -> str:
    """原稿が参照する画像ファイルの指紋。本文を変えずに PNG を差し替えても変わる。"""
    h = hashlib.sha256()
    for p in sorted(image_paths(ws, text)):
        h.update(str(p.relative_to(ws.dir)).encode("utf-8"))
        h.update(p.read_bytes() if p.exists() else b"<missing>")
    return h.hexdigest()[:16]


def figures_hash(ws: Workspace, text: str, detail: dict | None) -> str:
    """図表の逆読みが、何に対して行われたかの指紋: 本文（Mermaid・表・キャプションを含む）、画像の中身、設計の答え。"""
    specs = [{"label": it.label, "answer": it.answer, "question": it.spec.get("question"), "reading": it.spec.get("reading"),
              "render": it.spec.get("render")} for it in planned(detail)]
    h = hashlib.sha256(skim.text_hash(text).encode("utf-8"))
    h.update(assets_hash(ws, text).encode("utf-8"))
    h.update(json.dumps(specs, ensure_ascii=False, sort_keys=True).encode("utf-8"))
    return h.hexdigest()[:16]


def caption_labels(text: str) -> list[str]:
    """原稿のキャプションのラベル（図1・表1…）を、現れた順にすべて返す（重複を含む）。"""
    out = []
    for b in mdparse.parse(text):
        if b.kind == "paragraph":
            m = CAPTION_RE.match(jatext.strip_inline(b.text))
            if m:
                out.append(f"{m.group(1)}{int(m.group(2).translate(ZEN2HAN))}")
    return out


def _local(ws: Workspace, src: str) -> Path | None:
    """原稿からの相対パスの画像。URL や、文書のディレクトリの外に出るパスは扱わない。"""
    if not src or re.match(r"^[a-z]+:", src) or Path(src).is_absolute():
        return None
    p = ws.path(src)
    try:
        p.resolve().relative_to(ws.dir.resolve())
    except ValueError:
        return None
    return p


def check_draft(ws: Workspace, text: str, detail: dict | None, name: str = "draft.md") -> list[Issue]:
    """原稿（draft.md か final.md）の図表が設計（10-detail.json）どおりかを照合する。"""
    plan = planned(detail)
    found = draft_figures(text)
    if not plan and not found:
        return []
    issues: list[Issue] = []
    by_label = {f.label: f for f in found}
    for it in plan:
        f = by_label.get(it.label)
        if f is None:
            issues.append(Issue("GT113", "error", f"{it.label}（節 {it.section}）が {name} にありません。設計どおりに図表を置き、"
                                                  f"直後に「{it.label}: <答えの一文>」のキャプションを付けてください。"))
            continue
        if it.answer and _norm(f.caption) != _norm(it.answer):
            issues.append(Issue("GT114", "error", f"{it.label}のキャプションが、設計の答え「{excerpt(it.answer)}」と違います。"
                                                  "図表から読み取ってほしい答えの一文を、そのままキャプションに書きます（1.4）。"
                                                  "答えを変えるなら `cyrus back detail` で spec.answer を直してください。", f.line))
        render = it.spec.get("render")
        want = SOURCE_FOR_RENDER.get(render) if isinstance(render, str) else None
        if want and f.source != want:
            issues.append(Issue("GT115", "error", f"{it.label}は {render} で描く設計ですが、キャプションの前後に{SOURCE_JA[want]}がありません。", f.line))
        elif f.source == "image":
            p = _local(ws, f.src)
            if p is None or not p.exists():
                hint = ("スクリーンショット・写真は実物の素材が要ります（ハーネスは作れません）。素材を figures/ に置き、本文のパスを合わせてください。"
                        if render == "image" else "Vega-Lite の仕様を figures/ に置き、`cyrus figure render` で PNG を作ってください。")
                issues.append(Issue("GT116", "error", f"{it.label}の画像 {f.src or '（パスなし）'} がありません（文書のディレクトリの中の相対パスにします）。"
                                                      + hint, f.block_line))
            elif render == "vega-lite" and not p.with_suffix(".vl.json").exists():
                issues.append(Issue("GT116", "warn", f"{it.label}の元の仕様（{p.with_suffix('.vl.json').name}）が figures/ にありません。"
                                                     "描き直せるよう、PNG と同じ名前で残してください。", f.block_line))
        if f.source == "mermaid":
            n_lines = len([l for l in f.src.splitlines() if l.strip()])
            if n_lines > MERMAID_LINES_WARN:
                issues.append(Issue("VP080", "warn", f"{it.label}の Mermaid が {n_lines} 行あります。規模の制約を超えるなら、"
                                                     "組み合わせ（手順7）か分割を検討してください。", f.block_line))
    labels = {it.label for it in plan}
    for f in found:
        if f.label not in labels:
            issues.append(Issue("GT117", "error", f"{f.label}は設計（10-detail.json）にありません。`cyrus back detail` で spec を足すか、"
                                                  "図表を外してください。図表には必ず、答えと根拠の形を先に決めます。", f.line))
    # 同じ番号のキャプションが二つ以上
    caps = caption_labels(text)
    for dup in sorted({c for c in caps if caps.count(c) > 1}):
        issues.append(Issue("GT117", "error", f"{dup}のキャプションが {caps.count(dup)} つあります。番号は図表ごとに一つにしてください。"))
    # キャプションのない図表（検査と逆読みから漏れる）
    claimed = {f.block_line for f in found if f.block_line}
    for b in mdparse.parse(text):
        if b.line in claimed:
            continue
        if b.kind == "code" and b.lang == "mermaid":
            issues.append(Issue("GT117", "error", "キャプションのない Mermaid の図があります。設計の図なら直後に「図N: <答えの一文>」を付け、"
                                                  "設計にないなら外してください。", b.line))
        elif b.kind == "image":
            issues.append(Issue("GT117", "error", "キャプションのない画像があります。設計の図なら直後に「図N: <答えの一文>」を付け、"
                                                  "設計にないなら外してください。", b.line))
        elif b.kind == "table":
            issues.append(Issue("GT117", "warn", "キャプションのない表があります。設計の表なら直後に「表N: <答えの一文>」を付けてください"
                                                 "（本文の一部として使う小さな表なら、このままでも構いません）。", b.line))
    return issues


# ---------------------------------------------------------------- 描画


def render_all(ws: Workspace, only: set[str] | None = None) -> list[tuple[Path, dict]]:
    """figures/*.vl.json を PNG にする。"""
    mod = vp()
    if mod is None:
        raise RuntimeError(missing_skill_issue().message)
    out: list[tuple[Path, dict]] = []
    for spec in sorted((ws.dir / FIGURES_DIR).glob("*.vl.json")):
        png = spec.with_name(spec.name[: -len(".vl.json")] + ".png")
        if only and spec.name not in only and png.name not in only:
            continue
        size = mod.render(json.loads(spec.read_text(encoding="utf-8")), png)
        out.append((png, size))
    return out


# ---------------------------------------------------------------- 逆読み（手順9）


FIGURE_SCHEMA = {
    "type": "object",
    "properties": {
        "figures": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "画像のファイル名"},
                    "claim": {"type": "string", "description": "この図表だけから読み取れる、書き手の主張（一文）。読み取れなければ「不明」"},
                    "answer": {"type": "string", "description": "問いが添えられた図表では、その問いへの答え。なければ空"},
                    "prefers_text": {"type": "string", "enum": ["yes", "no", "either"],
                                     "description": "この図表は、箇条書きや文章のほうが読みやすかったか。yes = 文章のほうがよい、no = 図表でよい、either = どちらとも"},
                    "reason": {"type": "string", "description": "prefers_text の理由"},
                    "unclear": {"type": "string", "description": "どこに注目すればよいかわからなかった点。なければ空"},
                },
                "required": ["file", "claim", "prefers_text", "reason"],
            },
        },
    },
    "required": ["figures"],
}


def _table_html(markdown: str) -> str:
    blocks = mdparse.parse(markdown)
    rows = blocks[0].rows if blocks and blocks[0].kind == "table" else []
    if not rows:
        return "<pre>" + html.escape(markdown) + "</pre>"
    head = "<tr>" + "".join(f"<th>{html.escape(jatext.strip_inline(c))}</th>" for c in rows[0]) + "</tr>"
    body = "".join("<tr>" + "".join(f"<td>{html.escape(jatext.strip_inline(c))}</td>" for c in r) + "</tr>" for r in rows[1:])
    return f"<table><thead>{head}</thead><tbody>{body}</tbody></table>"


def figure_images(ws: Workspace, found: list[Found], out_dir: Path) -> list[tuple[Found, Path]]:
    """図表を、本文やキャプションから切り離して一枚ずつ PNG にする。"""
    mod = vp()
    if mod is None:
        raise RuntimeError(missing_skill_issue().message)
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("fig-*.png"):
        old.unlink()
    pairs: list[tuple[Found, Path]] = []
    for i, f in enumerate(found, 1):
        png = out_dir / f"fig-{i:02d}.png"
        if f.source == "mermaid":
            mod.render(f.src, png)
        elif f.source == "image":
            p = _local(ws, f.src)
            if p is None or not p.exists():
                continue
            shutil.copyfile(p, png)
        elif f.source == "table":
            mod.render({"html": _table_html(f.src)}, png)
        else:
            continue
        pairs.append((f, png))
    return pairs


def build_prompt(reader: dict | None, pairs: list[tuple[Found, Path]], questions: dict[str, str]) -> str:
    """読み手への指示。キャプションも本文も答えも渡さない（図のみ）。読み方が参照の図表にだけ、問いを添える。

    カタログ（development.md 2）は案内に出典とパターン名だけを書くが、ここでは読み手が LLM なので、
    パターン名が主張の形を先に知らせることになる。それより厳しく、出典もパターン名も渡さない。
    読者ペルソナ（役割・背景・知識の程度）は、想定読者として読ませるために渡す（cyrus vision と同じ）。
    """
    reader = reader or {}
    p = reader.get("persona") or {}
    from .visionreader import LEVEL_JA
    lines = [
        f"あなたは「{p.get('role') or 'ある文書の想定読者'}」です。" + (f"{p['background']}。" if p.get("background") else ""),
        f"知識の程度: {LEVEL_JA.get(reader.get('knowledge_level'), '基本は知っている中級者')}。",
        "",
        "この作業ディレクトリにある画像は、ある文書に置かれた図表を、本文やキャプションから切り離して一枚ずつにしたものです。",
        "互いに別の図表で、順序に意味はありません。",
        "- " + "、".join(png.name for _, png in pairs),
    ]
    qs = [f"- {png.name} は、読み手が次の問いの答えを探す図表です: {questions[f.label]}" for f, png in pairs if f.label in questions]
    if qs:
        lines += ["", "次の画像には、先に問いを示します。"] + qs
    lines += [
        "",
        "画像は、ファイルを開くツール（view_file、Read など）で1枚ずつ開いて見てください。シェルコマンドは使わないでください。",
        "この作業ディレクトリの画像以外のファイルは読まないでください。検索もしないでください。",
        "図表にないことを推測で補わないでください。読み取れないことは「不明」と書いてください。",
        "",
        "画像ごとに、次のことを答えてください。",
        "1. この図表だけから読み取れる、書き手の主張を一文で（claim）",
        "2. 問いが示された図表では、その問いへの答え（answer）",
        "3. この図表は、箇条書きや文章のほうが読みやすかったか（prefers_text: yes = 文章のほうが読みやすい、no = 図表でよい、either = どちらとも）と、その理由（reason）",
        "4. どこに注目すればよいかわからなかった点（unclear）",
        "",
        "回答はすべて日本語で書いてください。",
    ]
    return "\n".join(lines)


def read_figures(ws: Workspace, text: str, found: list[Found], reader: dict | None, cfg=None, model: str | None = None) -> dict:
    """図表だけを読み手に読ませ、回答を skim/figures/reader-result.json に保存して返す。"""
    from . import visionreader
    plan = {it.label: it for it in planned(ws.read_json("10-detail.json"))}
    out_dir = ws.path(str(READ_DIR))
    pairs = figure_images(ws, found, out_dir)
    if not pairs:
        raise RuntimeError("画像にできる図表がありません（Mermaid・画像・表のどれかをキャプションの前後に置いてください）。")
    questions = {f.label: str(plan[f.label].spec.get("question") or "") for f, _ in pairs
                 if f.label in plan and plan[f.label].spec.get("reading") == "lookup" and plan[f.label].spec.get("question")}
    cfg = cfg or visionreader.load_config()
    # 読み手に一度に渡せる画像の数には上限があるので、図表が多いときは分けて読ませる（黙って切り捨てない）
    by_file: dict[str, dict] = {}
    runs: list[dict] = []
    for start in range(0, len(pairs), visionreader.MAX_PAGES):
        batch = pairs[start:start + visionreader.MAX_PAGES]
        prompt = build_prompt(reader, batch, questions)
        res = visionreader.run([png for _, png in batch], None, reader, model=model, cfg=cfg, prompt=prompt, schema=FIGURE_SCHEMA)
        runs.append(res)
        for x in res["result"].get("figures") or []:
            if isinstance(x, dict):
                by_file[str(x.get("file", "")).strip()] = x
    figures = []
    for f, png in pairs:
        r = by_file.get(png.name) or by_file.get(png.stem) or {}
        figures.append({"label": f.label, "file": png.name, "source": f.source, "question": questions.get(f.label, ""),
                        "claim": str(r.get("claim") or ""), "answer": str(r.get("answer") or ""),
                        "prefers_text": str(r.get("prefers_text") or ""), "reason": str(r.get("reason") or ""),
                        "unclear": str(r.get("unclear") or "")})
    first = runs[0]
    out = {"source": "draft.md", "draft_hash": skim.text_hash(text),
           "figures_hash": figures_hash(ws, text, ws.read_json("10-detail.json")), "figures": figures,
           "reader": first.get("reader"), "model": first.get("model"),
           "exit_code": max(r.get("exit_code", 0) for r in runs),
           "duration_seconds": round(sum(r.get("duration_seconds", 0) for r in runs), 1),
           "pages_given": [p for r in runs for p in r.get("pages_given", [])], "batches": len(runs),
           "meta": first.get("meta", {}), "raw": [r["result"] for r in runs]}
    (out_dir / RESULT_NAME).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def tools_available() -> bool:
    """逆読みに要るもの（スキル・Chrome・読み手のコマンド）がそろっているか。読み手の設定に誤りがあれば ReaderConfigError。"""
    from . import visionreader
    mod = vp()
    return mod is not None and mod.find_chrome() is not None and visionreader.available()


def check_figure_test(ws: Workspace, ft: dict | None, plan: list[Planned], current_hash: str,
                      text: str | None = None, detail: dict | None = None) -> list[Issue]:
    """12-cogload.json の figure_test（図表の逆読みを cyrus-alignment-judge が判定したもの）を検査する。

    text と detail を渡すと、画像の中身と設計の答えまで含めた指紋（figures_hash）も照合する。
    """
    from . import visionreader
    if not plan:
        return []
    if not ft or not isinstance(ft, dict):
        return [Issue("GT150", "error", "figure_test（図表の逆読み）がありません（オブジェクトにしてください）。`cyrus figure read` で読み手に読ませ、"
                                        "cyrus-alignment-judge の判定を記録してください。")]
    if ft.get("skipped_reason"):
        try:
            usable = tools_available()
        except visionreader.ReaderConfigError as e:
            return [Issue("GT158", "error", f"読み手の設定に誤りがあります: {e}")]
        if usable:
            return [Issue("GT151", "error", "この環境では visual-patterns・Chrome・読み手のコマンドが使えるので、図表の逆読みは省略できません。")]
        return []
    rec = ws.path(str(READ_DIR)) / RESULT_NAME
    try:
        run = json.loads(rec.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [Issue("GT152", "error", f"{READ_DIR}/{RESULT_NAME} がないか、読めません。`cyrus figure read` で読み手に読ませてください。")]
    issues: list[Issue] = []
    if run.get("draft_hash") != current_hash or ft.get("draft_hash") != current_hash:
        issues.append(Issue("GT153", "error", "図表の逆読みが、いまの draft.md で行われていません。原稿を直したら `cyrus figure read` からやり直し、"
                                              "figure_test.draft_hash を更新してください。"))
    elif text is not None and run.get("figures_hash") != figures_hash(ws, text, detail):
        issues.append(Issue("GT153", "error", "図表の逆読みのあとで、画像ファイルか設計の答え（spec.answer など）が変わっています。"
                                              "`cyrus figure read` からやり直してください。"))
    # 読み手の回答（実行記録）に、設計の図表ごとの回答があるか
    replies = {x.get("label"): x for x in run.get("figures") or [] if isinstance(x, dict)}
    for it in plan:
        r = replies.get(it.label)
        if r is None or not str(r.get("claim") or "").strip():
            issues.append(Issue("GT152", "error", f"読み手の回答（{READ_DIR}/{RESULT_NAME}）に{it.label}の読み取りがありません。"
                                                  "読み手に渡っていないか、回答が空です。`cyrus figure read` をやり直してください。"))
    got = {x.get("label"): x for x in ft.get("figures") or [] if isinstance(x, dict)}
    for it in plan:
        x = got.get(it.label)
        if x is None:
            issues.append(Issue("GT154", "error", f"figure_test.figures に{it.label}の判定がありません。"))
            continue
        r = replies.get(it.label) or {}
        if r.get("prefers_text") in PREFERS and x.get("prefers_text") != r.get("prefers_text"):
            issues.append(Issue("GT154", "error", f"figure_test の{it.label}の prefers_text（{x.get('prefers_text')}）が、"
                                                  f"読み手の回答（{r.get('prefers_text')}）と違います。読み手の答えをそのまま写してください。"))
        v = x.get("verdict")
        if v not in VERDICTS:
            issues.append(Issue("GT154", "error", f"figure_test の{it.label}の verdict は {' / '.join(VERDICTS)} にしてください。"))
        elif v in ("mismatch", "misread"):
            issues.append(Issue("GT155", "error", f"{it.label}の逆読みが答えと合いません（{v}: {x.get('note', '')}）。"
                                                  "欠落なら添え書きを足すか文章に寄せ、誤推論なら配置・矢印・色・強調を直して描き直し、"
                                                  "`cyrus figure read` からやり直してください（手順9）。"))
        elif v == "partial":
            issues.append(Issue("GT156", "warn", f"{it.label}の逆読みは部分一致です（{x.get('note', '')}）。欠けた点を添え書きで補うか、直してください。"))
        # 削除の問い: note は判定者の理由（読み手の理由の写しを含む）なので、書き手の判断は別の欄 keep_reason に書く
        if x.get("prefers_text") == "yes" and not (isinstance(x.get("keep_reason"), str) and x["keep_reason"].strip()):
            issues.append(Issue("GT157", "warn", f"{it.label}について、読み手は文章のほうが読みやすいと答えました。図表を消して添え書きだけでも答えが伝わるなら"
                                                 "削ります（手順9・削除の問い）。残すなら、その理由を keep_reason に書いてください。"))
    return issues
