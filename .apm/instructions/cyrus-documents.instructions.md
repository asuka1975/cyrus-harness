---
applyTo: "documents/**"
description: cyrus で書く文書の成果物を編集するときの約束
---

# cyrus の成果物を編集するとき

- `documents/<slug>/` は cyrus ワークフローの成果物です。編集する前に、`python3 .claude/skills/cyrus/scripts/cyrus.py next` で現在のステージを確かめ、そのステージのガイドに従ってください。
- `state.json` と `.current` は CLI が管理します。手で書き換えないでください。ステージの移動は `cyrus advance` / `cyrus back` で行います。
- 本文（`draft.md`・`final.md`）は `.claude/skills/cyrus/references/japanese-style.md` の指針に従って書きます。1文に1つのこと、結論を先に、読者が知らない語は初出で説明、文体を混ぜない。
- 主張の強さは `07-logic/report.json` の hedge に合わせます。
- 成果物を保存するとフックが検査結果を返します。エラーが出たらその場で直してください。
