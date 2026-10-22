---
id: marimekko
name: マリメッコ
aliases: [marimekko-chart, mekko-chart, mosaic-plot]
layer: primitive
family: chart

primary_intent: part-to-whole
secondary_intents: [magnitude-comparison]

information_structure:
  shape: items
  attributes:
    - categorical
    - quantitative

scale:
  categories: 3〜10
  groups: 2〜6

precision: overview

complexity: medium

visual_encoding:
  category: position
  total: length
  share: length
  sub-category: color

text_dependency: medium

abstraction: abstract

best_for:
  - 項目の大きさと内訳の割合を同時に見せる
  - 市場の規模と占有率のように二段階の構成を一つに示す
  - 項目の幅の合計が全体を表す

avoid_when:
  - 項目または内訳が多く細い区画にラベルが入らない
  - 内訳の割合だけ（または大きさだけ）が主題である
  - 個々の値を正確に読ませる必要がある

alternatives:
  - stacked-column-chart
  - treemap
  - bar-chart
---

# マリメッコ

## 定義

項目ごとに縦棒を置き、棒の幅を項目の総量に比例させ、棒の高さを 100% として内訳の割合を積み上げる図である。各区画の面積が、その内訳の絶対量を表す。幅の合計が全体になる。

## 目的

全体は何からなり、各項目がどれだけ大きく、その内訳の割合はどうかを、幅と高さの両方で答えられるようにする。

## どういうときに利用するか

- 項目の大きさと内訳の割合を同時に見せる
- 市場の規模と占有率のように、二段階の構成を一つに示す
- 項目の幅の合計が全体を表す

## どういうときに利用してはいけないか

- 項目または内訳が多く、細い区画にラベルが入らない
- 内訳の割合だけ、または大きさだけが主題である
- 個々の値を正確に読ませる必要がある

## 入力の構造

`items: categorical + quantitative`。項目ごとの総量と、内訳ごとの量を持つ。内訳の合計が総量になる。

| 地域 | 総量 | 製品A | 製品B |
| --- | --- | --- | --- |
| 関東 | 500 | 300 | 200 |
| 関西 | 200 | 50 | 150 |

## デザインの文法

- 幅は総量に比例させ、棒の間隔はゼロか最小にする
- 高さは 100% で固定し、内訳を積み上げる。積み上げの順序は全項目でそろえる
- 内訳は色で区別し、凡例の順を積み上げの順に合わせる
- 項目名を棒の上か下に幅に沿って書き、区画内の数値は幅が足りる区画だけに書く

## 作成時のルール

- 項目は総量の順、または意味のある順に並べる
- 内訳の色は多くても六色にする
- 読み取ってほしい区画を一つ決め、一文で添える

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 高さも量にし、100% の固定を崩す
- 区画の面積を正確に比べさせる
- 内訳の積み上げ順を項目ごとに変える

## 利用例

- 地域ごとの市場規模（幅）と製品ごとの占有率（高さ）を示す
- 部門ごとの人員数（幅）と雇用形態の割合（高さ）を示す

## NGパターン

- 十二地域に八製品: 区画が細かく、ラベルも色も読めない
- 幅をすべて同じにする: 大きさの情報が消え、割合しか残らない
