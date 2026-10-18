# ステージ13: 言葉を読者に合わせる（Wording Check）

フェーズ: 仕上げ 2/2　成果物: `final.md`　承認: 必要

## ねらい

原稿の言葉遣いを、読者に合わせて直します。
最後にユーザーに完成版を確認してもらいます。次の2つの層で見ます。

| 層 | 見るもの | 方法 |
| --- | --- | --- |
| 推敲 | 不自然な比喩、あいまいな主述関係、硬い表現、冗長な言い方、立場に合わない文末や敬語 | yomiyasu スキル（推敲は非決定論、検査と記録は決定論） |
| 読者の辞書と表記 | 読者が知らない語の説明、避けるべき語、ひらく漢字、表記ゆれ | `cyrus wording`（決定論） |

yomiyasu（nanaism/yomiyasu）は、cyrus の依存として APM で一緒に入ります。場所は `.claude/skills/yomiyasu/` です。

## 進め方

### 1. yomiyasu で推敲する

雛形として `draft.md` の写しが `final.md` にできています。`draft.md` を原文にして yomiyasu で推敲し、結果を `final.md` に書きます。

Skill ツールで `yomiyasu` を呼びます。依頼には次のことを書きます。yomiyasu は、言われなかった種類や読者を推定で決めたときは、直す箇所を控えめにします。わかっていることはすべて渡します。

- **原文**: `documents/<slug>/draft.md`（書き換えない）
- **最終稿の保存先**: `documents/<slug>/final.md`（上書きしてよい）
- **文書の種類**（`--doc-type`）: `08-structure.json` の `doc_type` から、次の表で決める。当てはまらなければ付けない。

  | doc_type | yomiyasu の値 |
  | --- | --- |
  | 提案書 | proposal |
  | 手順書・マニュアル | manual |
  | 解説・技術記事・社内ブログ | article |
  | 障害報告 | incident |
  | 議事録 | minutes |
  | スライド | slides |
  | 仕様書・規程・契約書 | formal |
  | 論文・研究レポート | paper |
  | メール・チャット | mail |

- **読者**（`--reader`）: `03-reader.json` の `knowledge_level` から決める。novice は general、intermediate は informed、expert は expert。
- **書き手と読み手の関係**: `01-intent.md` と `03-reader.json` の persona からわかる範囲で書く（例: 書き手は情報システム部の担当者、読み手は決裁者の部長）。関係を渡すと、yomiyasu は読み手に合わせて敬語を直す。
- **文書の立場**（`--stance`）: 提案や推奨なら「勧め」、守ってもらう決まりや手順なら「決まり」、解説や報告なら「説明」。決めきれなければ付けない。
- **資料**: 渡さない。事実はステージ6で確かめてあり、ここでは事実を足さない。
- **返答の形**: 本文は `final.md` に保存し、返答に本文を載せない。返答には「変えたところ」「書き手に確かめたい点」「事実の確かめ」「確認の記録」だけを書く。

yomiyasu は推敲のあと、`yomiyasu_check.py run --source draft.md --final final.md` で lint と diff をかけ、`verify` で記録と照らします。途中でフックが lint や wording のエラーを知らせてきても、yomiyasu の手順を最後まで終えてから、手順2・3で直します。

### 2. 読者の辞書と表記を検査する

`cyrus wording final.md` を実行します。検出されるものは次のとおりです。

- **WD001（エラー）** 読者に対して避けるべき語 → 指定の言い換えにする。
- **WD002 / WD003（エラー）** 読者が知らない語が説明なしに使われている／説明が初出より後 → 初出で説明するか、知っている語に言い換える。
- **WD004（参考）** 読者辞書にない語 → 読者が知っている語か判断する。知らない語なら説明か言い換えをする。判断に迷う語が多ければ、まとめてユーザーに聞き、答えを `03-reader.json` の `known_terms` / `unknown_terms` に追加する（辞書が育つほど検査が正確になる）。
- **WD005（警告）** ひらく漢字（「及び」「既に」「予め」など） → ひらく。
- **WD007 / WD008（警告）** 表記ゆれ・全角英数字 → 統一する。

yomiyasu は、補助動詞と形式名詞の「事」「為」のほかは表記を変えません。WD005・WD007・WD008 は、ここで直します。

yomiyasu が「書き手に確かめたい点」に「ここに説明が必要です」と挙げた語は、WD002 と同じように扱います。

### 3. 認知負荷を確かめる

`cyrus lint final.md` で、言い換えによって認知負荷が上がっていないか確かめます。

### 4. 直したら、yomiyasu の検査をやり直す

手順2・3で `final.md` を直したら、yomiyasu の検査をもう一度実行します。完了条件では、`final.md` が最後に yomiyasu で検査した本文のままかを確かめるからです。プロジェクトのルートで、手順1で決めた値を付けて実行します（`--doc-type` と `--reader` の値は、yomiyasu の出力の `yomiyasu-check:` で始まる行にもあります）。

```bash
python3 .claude/skills/yomiyasu/scripts/yomiyasu_check.py run --source documents/<slug>/draft.md --final documents/<slug>/final.md --doc-type <値> --reader <値> --stance=<値> --fact-gaps
python3 .claude/skills/yomiyasu/scripts/yomiyasu_check.py verify --final documents/<slug>/final.md --source documents/<slug>/draft.md
```

- run の出力の「意味が変わる恐れ」と「直した箇所」を読み、手順2・3の直しで意味が変わっていないか確かめる。変わっていたら直して、run からやり直す。
- run の1行目に「修正は1回までの決まりを超えています」と出ることがあります。これは yomiyasu の推敲の決まりで、辞書の検査やユーザーの指示による直しは止めません。
- verify の1行目に「ハッシュが記録と合いました」と出れば終わりです。

## ユーザーへの確認

- 完成版の冒頭（要約の節）と、主な変更点を3行程度で見せる。
- yomiyasu の「書き手に確かめたい点」があれば、あわせて聞く（最大2点）。
- 「読者の〇〇さんが読む想定で、この内容でよいですか。気になる言い回しがあれば教えてください」と聞く。
- ユーザーの修正を反映したら、手順2〜4をやり直し、再度 `cyrus check` を通す。
- 承認をもらったら `cyrus advance --confirmed "…"` を実行する。これでワークフローは完了です。完成版の場所（`documents/<slug>/final.md`）をユーザーに伝えます。

## 完了条件

- `final.md` に lint と wording のエラーがない。
- `final.md` が、yomiyasu で `draft.md` から推敲して検査した本文のままである（yomiyasu の verify が通る）。
- ユーザーの承認をもらって `cyrus advance --confirmed "…"`。
