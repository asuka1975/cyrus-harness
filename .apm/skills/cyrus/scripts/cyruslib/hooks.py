"""Claude Code のフック。

- post-edit: 成果物が書き換えられたら、そのステージの完了条件を検査し、エラーがあれば Claude に返す。
  （決定論的な検査結果を、非決定論的な執筆ループに即座に戻すための仕組み）
- session-start: 進行中のドキュメントがあれば、その進捗をコンテキストに入れる。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from . import gates, lint, wording
from .issues import count, format_issues
from .reader import build_profile
from .workspace import STAGES, Workspace, artifact_owner, stage

WATCHED_TEXT = {"draft.md", "final.md"}


def _read_stdin() -> dict:
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}


def post_edit(payload: dict) -> int:
    tool_input = payload.get("tool_input") or {}
    fp = tool_input.get("file_path") or tool_input.get("path")
    if not fp:
        return 0
    owner = artifact_owner(Path(fp))
    if not owner:
        return 0
    ws, st, rel = owner
    messages: list[str] = []
    if rel in WATCHED_TEXT:
        text = Path(fp).read_text(encoding="utf-8")
        prof = build_profile(ws.read_json("03-reader.json"))
        issues, metrics = lint.lint_text(text, prof)
        if rel == "final.md":
            w, _ = wording.check_wording(text, prof, wording.glossary_from_detail(ws.read_json("10-detail.json")))
            issues += w
        errs = [i for i in issues if i.severity == "error"]
        c = count(issues)
        if errs:
            messages.append(f"cyrus: {rel} に認知負荷・言葉遣いのエラーが {c['error']} 件あります（警告 {c['warn']} 件）。")
            messages.append(format_issues(errs, rel, limit=10, min_severity="error"))
    elif st is not None and rel.endswith(".json"):
        try:
            json.loads(Path(fp).read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            messages.append(f"cyrus: {rel} が JSON として読めません: {e}")
        else:
            current = ws.load().get("stage")
            if current == st.key:
                issues = [i for i in gates.run_gate(ws, st.key) if i.severity == "error" and i.rule != "GT002"]
                if issues:
                    messages.append(f"cyrus: {rel} の完了条件でエラーが {len(issues)} 件あります（TODO の残りは除く）。")
                    messages.append(format_issues(issues, rel, limit=10))
    if messages:
        print("\n".join(messages), file=sys.stderr)
        return 2
    return 0


def session_start() -> int:
    ws = Workspace.current()
    if ws is None:
        return 0
    st = ws.load()
    if st.get("stage") == "done":
        return 0
    s = stage(st["stage"])
    print(f"[cyrus] 執筆中のドキュメントがあります: 「{st.get('title') or ws.slug}」（{ws.slug}）"
          f" 現在のステージ: {s.name}／{s.title_ja}。/cyrus で再開できます。")
    return 0


def run(event: str) -> int:
    try:
        if event == "post-edit":
            return post_edit(_read_stdin())
        if event == "session-start":
            return session_start()
    except Exception as e:  # フックの失敗で作業を止めない
        print(f"cyrus hook ({event}) で内部エラー: {e}", file=sys.stderr)
        return 0
    return 0
