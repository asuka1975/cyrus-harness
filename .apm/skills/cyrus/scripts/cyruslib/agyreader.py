"""ぼかした画像を Gemini（agy コマンド）に読ませ、何が伝わったかを再構成させる。

原稿を書いた Claude とは別のモデルに読ませることで、書き手と同じモデルが読み手を演じる偏りを避ける。
Gemini には画像だけを渡す。画像は、プロジェクトと無関係な一時ディレクトリにコピーしてから渡し、
原稿やその他の成果物のパスは知らせない（agy の --sandbox はファイルの読み取りを制限しないため、置き場所で隔離する）。

安全のため、agy は権限確認を省略せず、読み取り専用の plan モードで起動する。
ヘッドレス実行では確認が必要な操作（シェルコマンドなど）は自動で拒否され、
ワークスペース内のファイル閲覧だけが使える。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

DEFAULT_MODEL = os.environ.get("CYRUS_AGY_MODEL", "gemini-3.8-flash-medium")
MAX_PAGES = 12

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


class AgyUnavailable(RuntimeError):
    pass


def find_agy() -> str | None:
    env = os.environ.get("CYRUS_AGY")
    if env and Path(env).exists():
        return env
    return shutil.which("agy")


def build_prompt(reader: dict | None, page_names: list[str], has_overview: bool, truncated: bool) -> str:
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
        "画像は、ファイル閲覧ツール（view_file など）で1枚ずつ開いて見てください。シェルコマンドは使わないでください。",
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
    return "\n".join(l for l in lines if l is not None)


def run(pages: list[Path], overview: Path | None, reader: dict | None, model: str | None = None,
        timeout: int = 900) -> dict:
    agy = find_agy()
    if not agy:
        raise AgyUnavailable("agy コマンドが見つかりません（環境変数 CYRUS_AGY で場所を指定できます）。")
    truncated = len(pages) > MAX_PAGES
    use = pages[:MAX_PAGES]
    with tempfile.TemporaryDirectory(prefix="cyrus-gemini-") as td:
        work = Path(td)
        for p in use:
            shutil.copyfile(p, work / p.name)
        if overview and overview.exists():
            shutil.copyfile(overview, work / "overview.png")
        prompt = build_prompt(reader, [p.name for p in use], bool(overview and overview.exists()), truncated)
        cmd = [agy, "-p", prompt, "--add-dir", str(work), "--mode", "plan",
               "--output-format", "json", "--json-schema", json.dumps(SCHEMA, ensure_ascii=False),
               "--model", model or DEFAULT_MODEL, "--print-timeout", f"{timeout}s"]
        started = time.time()
        try:
            proc = subprocess.run(cmd, cwd=str(work), capture_output=True, text=True, timeout=timeout + 60,
                                  stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired as e:
            raise AgyUnavailable(f"agy が {timeout} 秒以内に終わりませんでした。") from e
    payload = None
    for line in reversed((proc.stdout or "").splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                payload = json.loads(line)
                break
            except json.JSONDecodeError:
                continue
    if payload is None:
        raise AgyUnavailable(f"agy の出力を読めませんでした（終了コード {proc.returncode}）: {(proc.stderr or proc.stdout).strip()[:400]}")
    result = payload.get("structured_output")
    if result is None:
        try:
            result = json.loads(payload.get("response", ""))
        except (TypeError, json.JSONDecodeError):
            raise AgyUnavailable(f"agy が構造化された回答を返しませんでした: {str(payload.get('response'))[:400]}")
    for k in ("toolAction", "toolSummary"):
        result.pop(k, None)
    return {
        "model": model or DEFAULT_MODEL,
        "status": payload.get("status"),
        "duration_seconds": round(payload.get("duration_seconds") or (time.time() - started), 1),
        "pages_given": [p.name for p in use],
        "truncated": truncated,
        "usage": payload.get("usage"),
        "denied_actions": payload.get("denied_actions") or [],
        "result": result,
    }
