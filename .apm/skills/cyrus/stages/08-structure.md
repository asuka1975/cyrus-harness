# ステージ8: 文書の骨組みを決める（Document Structure Design）

フェーズ: 組み立て 2/5　成果物: `08-structure.md`（constructivism の出力）と `08-structure.json`　承認: 不要（ステージ9でまとめて承認をもらう）

## ねらい

文書の章立て（節の並びと役割）を決めます。
章立ての選択は、constructivism スキル（asuka1975/constructivism。cyrus の依存として APM で一緒に入る）に任せます。読者の目的・読む姿勢・メッセージの種別から、技術文書・学術・ビジネス文書のカタログ（チュートリアル、ハウツー、解説記事、技術記事、設計書、ADR、論文、報告書、企画書、稟議書、議事録、ポストモーテム、通知、メールなど）に照らして構成を選び、日本語の見出しの骨子を出します。
cyrus は、その骨子を節にし、各節がどの主張を運び、読者のどの疑問に答えるかを決めます。

## 進め方

### 1. constructivism に構成を選んでもらう

Skill ツールで `constructivism` を呼びます。渡す入力は次の5項目です。すべて、これまでの成果物にあります。わかっていることはすべて渡します（欠けた項目はスキルが既定値で補い、「仮定」に書きます）。

| constructivism の入力 | 出どころ |
| --- | --- |
| 目的（読者が読後に何をするか） | `03-reader.json` の `purpose`: decide → 決める（承認）、report → 報告を受ける、act → 作業する、learn → 学ぶ、lookup → 調べる、understand → 理解する、persuade → 動かされる、verify → 検証する、summary → 要点だけ知る |
| 読者（役割・専門性・読む姿勢） | `03-reader.json` の `persona.role`、`knowledge_level`（novice → 初学者、intermediate → 中級、expert → 専門家）、`reading_context.reading_mode`（careful → 通読、skim → 拾い読み、reference → 検索、headline → 冒頭だけ） |
| メッセージ（中心の主張と種別） | `05-claims.json` の C0 の `text`（1〜2文）と `message_kind`（proposal → 提言、decision → 決定の記録、report → 事実報告、instruction → 手順指示、explanation → 概念説明、comparison → 比較評価、education → 教育） |
| 内容（種別と主要な要素） | `04-analysis.md` の「読者に必要な情報」と、主張の木（C1〜、F1〜）から、手順的／概念的／参照的／時系列／データ中心のどれかを判断し、主要な要素を箇条書きで渡す |
| 制約（指定書式・媒体・分量・社内外） | `01-intent.md` の「種類と形式」「制約」（社内の様式や投稿規定があれば必ず渡す。それが骨格になる）、`03-reader.json` の `reading_context.medium`（screen・mobile → Web／Wiki、print → PDF、slide → スライド、mail → メール）、`audience_scope`（internal → 社内、external → 社外。なければ社内）、分量の上限（01-intent.md に字数や枚数があればそれ。なければ `reading_context.time_budget_min` × 読む速さ（初心者 400・中級 500・専門家 600 字／分）を「約 N 字」として渡す） |

返答は「構成選択結果」「骨子」「構成チェック」の3節の Markdown です。**そのまま `documents/<slug>/08-structure.md` に保存します**（手を加えない。コードフェンス（```）で囲まない。cyrus check が骨子の見出しと節の対応を照合します）。

### 2. 骨子を `08-structure.json` に落とす

- `genre` ← 採用構成、`form` ← 型（PREP／SDS／SCQA／IMRaD／Diátaxis の種別など）、`style` ← 文体（敬体か常体）、`second_choice` ← 第2候補、`deviations` ← 仮定・逸脱。`title` は、ユーザーが決めた題があればそれを、なければ標題案を使う。`doc_type` には cyrus の大まかな種類（提案書・手順書・解説・報告など）を書く。
- `sections`: 骨子の番号付きの項目を、順に H2 の節にする。`heading` は骨子の見出しのまま、`purpose` は「役割」、`length_hint` は「目安」、`elements` は「入れる要素」（ステージ10で、節に何を置くかの出発点になる）。必要なら H3 の小節を足してよい（骨子の見出しはすべて残す）。
- 骨子の見出しを変えたくなったら、`08-structure.md` の骨子も直し、「仮定・逸脱」に理由を書く。
- 読者の `questions`（03-reader.json）を、それぞれどの節が答えるか割り当てる（`reader_question`）。答える節のない疑問が残らないようにする。
- 主張（C0〜）をすべて、どこかの節に割り当てる（`claims`）。C0 は原則として冒頭の節に置く（結論を先に）。構成の「核メッセージの位置」が末尾や両方なら、それに従う。

### 3. 読者の負荷の決まり（CLI が検査する）

- 最上位の節は7個まで。多ければまとめる（定型の必須セクションは削らず、第2階層を統合する）。
- 見出しの階層は3段（H2〜H4）まで。レベルを飛ばさない。
- 見出しは短く（30字以内）、見出しだけを拾い読みしても流れがわかるようにする。
- 同じ階層の見出しは形を揃える（すべて名詞止め、など）。
- スマホで読まれるなら、表を減らし、節を短くする。

## 成果物 `08-structure.json`

```json
{
  "title": "文書のタイトル",
  "doc_type": "提案書",
  "genre": "企画書・提案書",
  "form": "SCQA",
  "style": "敬体",
  "second_choice": "エグゼクティブサマリー＋稟議書",
  "deviations": "読む姿勢は未指定のため「通読」を仮定した。分量の制約で「実施計画」と「費用」を1節に統合した",
  "format": "markdown",
  "conclusion_first": true,
  "sections": [
    {"id": "S1", "heading": "提案の要旨", "level": 2, "purpose": "何を・いくらで・何が得られるかを先に示す", "length_hint": "10%",
     "elements": ["置き換えの依頼", "300 万円", "理由の要約"], "reader_question": "結局、何をしてほしいのか", "claims": ["C0"]},
    {"id": "S2", "heading": "現状と課題", "level": 2, "purpose": "SCQA の S と C", "length_hint": "20%", "reader_question": "…", "claims": ["C1"]},
    {"id": "S2.1", "heading": "…", "level": 3, "purpose": "…", "length_hint": "", "reader_question": "…", "claims": ["C2"]}
  ]
}
```

- `conclusion_first` を false にすると、C0 を冒頭に置かない構成も許される（チュートリアルや教材のような積み上げ型）。

## 完了条件

- `08-structure.md` に constructivism の出力があり、骨子の見出しがすべて `sections` にある。
- `genre`・`form`・`style` がある。
- `cyrus check` でエラーが0になったら `cyrus advance`。
