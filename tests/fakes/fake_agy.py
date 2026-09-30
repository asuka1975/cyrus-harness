#!/usr/bin/env python3
"""テスト用の偽の agy。呼び出し方が安全か（読み取り専用・権限確認を省略しない・画像だけを渡す）を確かめ、決まった回答を返す。"""
import json
import os
import sys

args = sys.argv[1:]
problems = []
if "--dangerously-skip-permissions" in args:
    problems.append("権限確認を省略している")
if "--mode" not in args or args[args.index("--mode") + 1] != "plan":
    problems.append("plan モード（読み取り専用）で起動していない")
files = sorted(os.listdir(os.getcwd()))
if not files or any(not f.endswith(".png") for f in files):
    problems.append(f"作業ディレクトリに画像以外がある: {files}")
prompt = args[args.index("-p") + 1]
if "documents" in prompt or "draft.md" in prompt:
    problems.append("プロンプトに原稿の場所が含まれている")
log = os.environ.get("FAKE_AGY_LOG")
if log:
    with open(log, "w", encoding="utf-8") as f:
        json.dump({"args": args, "files": files, "problems": problems}, f, ensure_ascii=False)
if problems:
    print(json.dumps({"status": "ERROR", "response": "; ".join(problems)}, ensure_ascii=False))
    sys.exit(3)
result = {
    "reader_summary": "検索の置き換えのために300万円の承認を求める提案。",
    "main_point": "検索を置き換えるため300万円を承認してほしい。",
    "requested_action": "予算の承認",
    "sections": [{"heading": "お願いしたいこと", "understood": "300万円の承認を求めている", "confidence": "high"}],
    "confusing_points": [],
    "visual_notes": {"stood_out": ["見出し"], "missed_or_hidden": ["表1の金額"], "layout_issues": []},
}
print(json.dumps({"status": "SUCCESS", "duration_seconds": 0.1, "structured_output": result,
                  "usage": {"total_tokens": 1}}, ensure_ascii=False))
