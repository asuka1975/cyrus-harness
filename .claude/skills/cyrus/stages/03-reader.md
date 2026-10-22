# ステージ3: 読者を描く（Target Reader）

フェーズ: インタビュー 3/6　成果物: `03-reader.json`　承認: 必要

## ねらい

読者を1人の具体的な人物として描き、その人の**知識の範囲（語彙）**と**読む状況**を定義します。
ここで作る語彙の辞書は、ステージ13の言葉遣い検査でそのまま使われます。読む状況は、文や段落の長さの基準（lint の閾値）を決めます。

## 聞くこと

1. **読者はどんな人か。** 立場・職種・経験年数、この話題との距離。「具体的に1人思い浮かべるなら、誰ですか」と聞くと描きやすい。
2. **どのくらい知っているか。** AskUserQuestion で3択にする。
   - 初心者（novice）: この分野の用語をほとんど知らない
   - 中級者（intermediate）: 基本用語は知っているが、細部は知らない
   - 専門家（expert）: 分野の用語や慣習を知っている
3. **どんな状況で読むか。** 画面／スマホ／印刷／スライド／メール（mail）、じっくり読むか（careful）／拾い読みか（skim）／必要なときに引くか（reference）／冒頭だけ読むか（headline。多忙な決裁者）、何分使えるか。社外の読者なら `audience_scope` を external にする。
4. **読み終えた読者は何をするか（purpose）。** AskUserQuestion で選んでもらう。文書の構成（ステージ8）を決める軸になるので、必ず一つに決める。
   - decide: 決める（承認・決定する）／ report: 報告を受ける／ act: 作業する／ learn: 学ぶ／ lookup: 調べる／ understand: 理解する／ persuade: 動かされる（依頼・説得）／ verify: 検証する（学術）／ summary: 要点だけ知る
5. **なぜ読むのか、読む前にどんな疑問を持っているか。**
6. **語彙の確認。** ステージ2の素材から、読者が知っていそうか微妙な語を5〜15個拾い、「この語は読者に説明なしで通じますか」とまとめて聞く（AskUserQuestion の multiSelect が便利）。図表の記法（フローチャート、シーケンス図、ガントチャートなど）を読者が知っているかも、ここで聞いておくと、ステージ10で図表を選びやすい。
   - 通じる語 → `known_terms`
   - 通じない語 → `unknown_terms`（本文では初出で説明が必要になる）
   - 使ってほしくない語（社内の隠語、誤解を招く語） → `avoid_terms`（言い換えも一緒に）

ユーザーが「おまかせ」と言った項目は、ステージ1・2の情報から推定し、推定であることを承認時に伝えます。

## 成果物 `03-reader.json`

```json
{
  "persona": {"name": "呼び名", "role": "立場・職種", "background": "経験・前提知識・関心ごと"},
  "knowledge_level": "novice | intermediate | expert",
  "purpose": "decide | report | act | learn | lookup | understand | persuade | verify | summary",
  "audience_scope": "internal | external（省略すると internal）",
  "known_terms": ["読者が説明なしで理解できる語"],
  "unknown_terms": ["読者が知らない語（使うなら初出で説明する）"],
  "avoid_terms": [{"term": "使わない語", "replace": "代わりの言い方"}],
  "reading_context": {"medium": "screen | mobile | print | slide | mail", "reading_mode": "careful | skim | reference | headline", "time_budget_min": 10},
  "motivation": "読者がこの文書を読む理由",
  "questions": ["読者が読む前に持っている疑問"],
  "success_criteria": ["読後に読者が〜できる"]
}
```

`questions` はステージ8で節の割り当てに、`success_criteria` はステージ12のペルソナレビューで使います。具体的に書いてください。
`purpose` と `reading_mode` は、ステージ8で constructivism（構成を選ぶスキル）に渡す「読者の目的」「読む姿勢」になります。

## 完了条件

- `cyrus check` でエラーが0。
- 読者像を2〜3行で見せ（例: 「情シス3年目の田中さん。検索の仕組みは知らない。会議の前に5分で読む」）、承認をもらって `cyrus advance --confirmed "…"`。
