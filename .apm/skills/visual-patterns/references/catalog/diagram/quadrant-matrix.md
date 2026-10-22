---
id: quadrant-matrix
name: 2軸マトリクス
aliases: [two-by-two-matrix, quadrant-chart, four-quadrant-matrix]
layer: primitive
family: diagram

primary_intent: positioning
secondary_intents: []

information_structure:
  shape: items
  attributes:
    - categorical
    - ordinal

scale:
  items: 3〜20
  cells: 4（象限）

precision: overview

complexity: low

visual_encoding:
  horizontal-criterion: position
  vertical-criterion: position
  quadrant: containment

text_dependency: medium

abstraction: abstract

best_for:
  - 対象を二つの評価軸で位置づけ、どの象限に入るかを見せる
  - 象限ごとの方針（投資・撤退など）を対象と結び付けて示す

avoid_when:
  - 軸が測定値で、二つの量の連動が主題である
  - 評価の観点が三つ以上ある
  - 評価の根拠が示せず、位置が恣意的に見える

alternatives:
  - continuum
  - scatter-plot
  - comparison-table
---

# 2軸マトリクス

## 定義

二つの評価軸を縦横に取り、各軸を高低で二分して四つの象限を作り、対象を象限の中に置いた図である。位置は測定値ではなく評価で決める。象限ごとに名前や方針を付けることが多い。

## 目的

読み手が「この対象は二つの観点でどこに位置し、どの象限に入るか」に答えられるようにする。

## どういうときに利用するか

- 製品・施策・関係者を、重要度と緊急度のような二つの観点で分類したい
- 象限ごとに取るべき方針が決まっており、対象をその方針に対応づけたい
- 対象が 5 以上あり、文章では二つの観点の組み合わせを保持できない（手順2 の「項目 × 属性」の行）

## どういうときに利用してはいけないか

- 軸が測定値で、二つの量の連動を読ませたい
- 観点が三つ以上あり、二軸に圧縮すると情報が落ちる
- 位置を決めた評価の根拠がなく、読み手が位置を測定値と誤読する恐れがある

## 入力の構造

items: categorical + ordinal。各対象が二つの軸それぞれに高低などの段階を持つ。

```yaml
axes: {x: 市場の成長率, y: 相対シェア}
items:
  - {name: 製品A, x: 高, y: 高}
  - {name: 製品B, x: 低, y: 高}
```

## デザインの文法

- 横軸と縦軸の名前と、各軸の高低の向きを端に書く
- 軸の中央で区切って四つの象限を作り、象限の名前を隅に書く
- 対象は名前付きの点か枠で置き、象限の中での位置は評価の段階に合わせる
- 対象の大きさを変える場合は、大きさが何を表すかを凡例に書く

## 作成時のルール

- 位置が評価で決まることと、評価の基準をキャプションか本文に書く
- 象限の境界近くの対象は、どちらの象限に入れたかを明示する
- 読み取ってほしい結論（どの対象がどの方針に当たるか）を本文に一文で書く

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 軸に目盛りを付け、評価の位置を測定値のように見せる
- 一つの対象を複数の象限にまたがって置く
- 軸の高低の向きを図ごとに変える

## 利用例

- BCG matrix と Portfolio diagram（Periodic Table of Visualization Methods）。市場成長率と相対シェアで事業を四象限に分ける
- Magic quadrant。実行能力とビジョンの完全性でベンダーを位置づける
- Stakeholder rating map。影響力と関心の高低で関係者を分け、関わり方を決める

## NGパターン

- 象限の名前を書かず、点だけを置く。象限に入ることの意味が読めず、位置づけが伝わらない
- 測定値を評価の段階に丸めて置く。測れるのに正確さを捨て、読み手が値を推測する
