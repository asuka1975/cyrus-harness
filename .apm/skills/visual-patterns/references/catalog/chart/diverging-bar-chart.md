---
id: diverging-bar-chart
name: 分岐横棒グラフ
aliases: [diverging-bar, diverging-column-chart, positive-negative-bar-chart]
layer: primitive
family: chart

primary_intent: deviation
secondary_intents: []

information_structure:
  shape: items
  attributes:
    - categorical
    - quantitative

scale:
  items: 2〜30
  series: "1"

precision: overview

complexity: low

visual_encoding:
  category: position
  deviation: length
  direction: color

text_dependency: low

abstraction: abstract

best_for:
  - 正負の値が混在する増減・損益・差を項目ごとに示す
  - 基準値（ゼロ・目標・平均）からの隔たりを強調する
  - 項目を隔たりの順に並べて最大のプラスとマイナスを見せる

avoid_when:
  - 値がすべて同符号で分岐の意味がない
  - 基準からの隔たりではなく量そのものを比べる
  - 個々の値を正確に読ませる必要がある

alternatives:
  - diverging-stacked-bar-chart
  - spine-chart
  - bar-chart
---

# 分岐横棒グラフ

## 定義

基準線を中央に置き、項目ごとの値を基準線から左右へ伸びる横棒の長さで表す図である。正負の向きは棒の伸びる側と色で区別する。縦棒にして上下に伸ばすこともできる。

## 目的

各項目が基準からどれだけ、どちら向きに離れているかを、棒の向きと長さで答えられるようにする。

## どういうときに利用するか

- 正負の値が混在する（増減・損益・差）
- 基準値（ゼロ・目標・平均）からの隔たりを強調する
- 項目を隔たりの順に並べ、最大のプラスとマイナスを見せる

## どういうときに利用してはいけないか

- 値がすべて同符号で、分岐の意味がない
- 基準からの隔たりではなく、量そのものを比べる
- 個々の値を正確に読ませる必要がある

## 入力の構造

`items: categorical + quantitative`。項目ごとに基準値からの差を持つ。差でない値は、基準値を引いて差にしてから使う。

| 部門 | 対前年増減（%） |
| --- | --- |
| 営業 | +12 |
| 開発 | -8 |

## デザインの文法

- 基準線は太めに描き、基準の値（ゼロ・目標）を明記する
- 正を右、負を左に伸ばし、正負を二色で区別して色の意味を凡例か軸に書く
- 項目は値の順に並べ、項目名は左端にそろえる
- 軸の目盛は左右で同じ間隔・同じ範囲にする

## 作成時のルール

- 基準値が何かをキャプションに書く
- 左右の目盛範囲を同じにし、片側だけ広げない
- 読み取ってほしい最大の隔たりを一文で添える

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 基準線をゼロ以外にしながら明記しない
- 正負で異なる尺度を使う
- 立体表示や影で棒の長さを歪める

## 利用例

- 部門ごとの予算の対前年増減を示す
- 各地域の売上の対計画差を示す
- 設問ごとの平均点と全体平均との差を示す

## NGパターン

- 項目名を棒の先端に置く: 棒の向きで項目名の位置が揺れ、探しにくい
- 全項目が正の値で描く: 分岐が起きず、基準線が無意味になる
