---
id: diverging-stacked-bar-chart
name: 分岐対称積み上げ横棒グラフ
aliases: [diverging-stacked-bar, diverging-stacked-column-chart, likert-chart]
layer: primitive
family: chart

primary_intent: deviation
secondary_intents: []

information_structure:
  shape: items
  attributes:
    - categorical
    - ordinal
    - quantitative

scale:
  items: 2〜15
  categories: 3〜7

precision: overview

complexity: medium

visual_encoding:
  category: position
  response: color
  share: length
  balance: position

text_dependency: low

abstraction: abstract

best_for:
  - 賛成・中立・反対のような態度を含む調査結果を示す
  - 複数の設問の傾きを一覧で比べる
  - 回答区分が三〜七段階の順序尺度である

avoid_when:
  - 回答区分に順序がない
  - 中立の区分がなく中央を決められない
  - 個々の割合を正確に読ませる必要がある
  - 単色の媒体で区分の濃淡が区別できない

alternatives:
  - diverging-bar-chart
  - spine-chart
---

# 分岐対称積み上げ横棒グラフ

## 定義

賛成・中立・反対のような順序のある回答区分を、中立の区分を中央線の左右に半分ずつ置き、肯定側と否定側へ積み上げた横棒の図である。設問ごとに一本の棒を置き、区分の割合を区画の長さで表す。

## 目的

各設問について肯定と否定のどちらにどれだけ傾いているかを、中央線からの左右の広がりで答えられるようにする。

## どういうときに利用するか

- 賛成・中立・反対のような態度を含む調査結果を示す
- 複数の設問の傾きを一覧で比べる
- 回答区分が三〜七段階の順序尺度である

## どういうときに利用してはいけないか

- 回答区分に順序がない
- 中立の区分がなく、中央をどこにするか決められない
- 個々の割合を正確に読ませる、または単色の媒体で濃淡が区別できない

## 入力の構造

`items: categorical + ordinal + quantitative`。設問ごとに各区分の割合を持つ。区分は順序付きである。

| 設問 | 反対 | 中立 | 賛成 |
| --- | --- | --- | --- |
| 評価制度は公平だ | 30 | 20 | 50 |
| 残業は適切だ | 55 | 25 | 20 |

## デザインの文法

- 中立の区分を中央線の左右に半分ずつ置き、肯定側を右、否定側を左に積み上げる
- 色は肯定と否定で色相を分け、強さを濃淡で表す。中立は無彩色にする
- 設問は肯定側の割合の順に並べる
- 軸は中央をゼロとし、左右に割合の目盛を置く

## 作成時のルール

- 区分の順序と色の対応を凡例に書き、凡例の並びを棒の並びに合わせる
- 回答数（n）を設問ごとかキャプションに書く
- 傾きが最も大きい設問を一文で添える

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 区分ごとに色相をばらばらにする
- 中立を片側の端に置く
- 設問の並びを順不同にする

## 利用例

- 従業員満足度調査の十設問を五段階で示し、否定に傾く設問を見せる
- 機能ごとの利用者の賛否を三段階で示す

## NGパターン

- 中立を右端に置く: 中央線が肯定と否定の境にならず、傾きが読めない
- 七区分に七色相: 色の順序が読めず、強さが伝わらない
