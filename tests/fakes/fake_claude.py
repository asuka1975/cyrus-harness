#!/usr/bin/env python3
"""テスト用の偽の Claude Code（-p --output-format json）。

プロンプトを標準入力で受け取り、Claude Code と同じ形の JSON を返す。--json-schema があれば回答を
structured_output に入れ、なければ result の文章の中に ```json で書く。
呼び出し方が安全か（plan モード・作業ディレクトリに画像だけ・プロンプトに原稿の場所がない）と、
設定ファイルで渡した環境変数を記録する。
"""
import json
import os
import sys

args = sys.argv[1:]
prompt = sys.stdin.read()
problems = []
if "--permission-mode" not in args or args[args.index("--permission-mode") + 1] != "plan":
    problems.append("plan モード（読み取り専用）で起動していない")
files = sorted(os.listdir(os.getcwd()))
if not files or any(not f.endswith(".png") for f in files):
    problems.append(f"作業ディレクトリに画像以外がある: {files}")
if not prompt:
    problems.append("プロンプトが標準入力で渡されていない")
if "documents" in prompt or "draft.md" in prompt:
    problems.append("プロンプトに原稿の場所が含まれている")
log = os.environ.get("FAKE_READER_LOG")
if log:
    with open(log, "w", encoding="utf-8") as f:
        json.dump({"args": args, "files": files, "problems": problems, "prompt": prompt,
                   "env": {k: os.environ.get(k) for k in ("FAKE_READER_TOKEN", "FAKE_READER_DROP")}},
                  f, ensure_ascii=False)
if problems:
    print(json.dumps({"type": "result", "subtype": "error", "is_error": True, "result": "; ".join(problems)},
                     ensure_ascii=False))
    sys.exit(1)
result = {
    "reader_summary": "検索の置き換えのために300万円の承認を求める提案。",
    "main_point": "検索を置き換えるため300万円を承認してほしい。",
    "requested_action": "予算の承認",
    "sections": [{"heading": "お願いしたいこと", "understood": "300万円の承認を求めている", "confidence": "high"}],
    "confusing_points": [],
    "visual_notes": {"stood_out": ["見出し"], "missed_or_hidden": ["表1の金額"], "layout_issues": []},
}
out = {"type": "result", "subtype": "success", "is_error": False, "usage": {"output_tokens": 1}}
if "--json-schema" in args:
    out["result"] = json.dumps(result, ensure_ascii=False)
    out["structured_output"] = result
else:
    out["result"] = "画像を読みました。\n\n```json\n" + json.dumps(result, ensure_ascii=False, indent=2) + "\n```\n"
print(json.dumps(out, ensure_ascii=False))
