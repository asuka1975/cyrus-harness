---
id: bubble-chart
name: バブルチャート
aliases: [bubble, bubble-plot, bubble-scatter-plot]
layer: primitive
family: chart

primary_intent: correlation
secondary_intents: []

information_structure:
  shape: items
  attributes:
    - quantitative
    - quantitative
    - quantitative

scale:
  points: 5〜100（円が重なって読めなくなる前まで）
  series: 1〜3

precision: overview

complexity: low

visual_encoding:
  x-variable: position
  y-variable: position
  third-variable: area
  group: color

text_dependency: low

abstraction: abstract

best_for:
  - 二変数の関係に、規模（人口・売上など）を円の大きさで加える
  - 規模の大きい項目が関係のどの位置にあるかを目立たせる

avoid_when:
  - 第三の変数を正確に比べさせる（面積の差は読み取りにくい）
  - 点が多く、円が重なって位置が読めない
  - 第三の変数が規模ではなく、大きさで表す意味がない

alternatives:
  - scatter-plot
  - xy-heatmap
---

# バブルチャート

## 定義

横軸と縦軸に数値変数を取り、各項目をその交点に円として描く図である。円の面積が第三の数値変数を表す。集団は円の色で分ける。

## 目的

二つの変数の関係を読ませつつ、規模の大きい項目がその関係のどこにあるかを答えられるようにする。

## どういうときに利用するか

- 二変数の関係に、項目の規模を重ねて見せたい
- 規模の大きい少数の項目が傾向を支えているかを見せたい
- 項目が百以下で、円が互いに見分けられる

## どういうときに利用してはいけないか

- 第三の変数の差を正確に読ませる（面積の差は過小に見える）
- 項目が多く、円が重なって位置が読めない
- 第三の変数に負の値や 0 が含まれる

## 入力の構造

`items: quantitative + quantitative + quantitative`。各項目が三つの数値を持つ。集団を分ける場合は + categorical。

| 国 | 一人あたり GDP | 平均寿命 | 人口 |
| --- | --- | --- | --- |
| A | 42000 | 83 | 1.2億 |
| B | 9000 | 71 | 2.1億 |

## デザインの文法

- 第三の変数は円の半径ではなく面積に比例させる
- 円の大きさの凡例を、代表的な値（大・中・小）で示す
- 円は半透明にし、重なった円が見えるようにする
- 大きい円を奥、小さい円を手前に描く

## 作成時のルール

- 第三の変数は規模（数えられる量）に限る
- 最大の円が図の面積を占めすぎないよう、大きさの範囲を調整する
- 注目する項目には名前を円の近くに書く
- 関係の性質（相関であり因果ではない）を本文で述べる

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 半径を値に比例させる（面積が値の二乗になる）
- 円の大きさで比率や割合を表す
- 円の色にさらに別の数値変数を割り当てる

## 利用例

- 国ごとの一人あたり所得と平均寿命の関係を、人口を円の大きさで重ねて示す
- 機能ごとの開発工数と不具合件数の関係を、利用者数を円の大きさで重ねて示す

## NGパターン

- 半径を値に比例させる。値が二倍の項目が四倍の面積に見える
- 千件の取引を円で描く。円が重なって塊になり、位置も大きさも読めない
