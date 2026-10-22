---
id: surplus-deficit-filled-line
name: 損益面グラフ
aliases: [surplus-deficit-filled-line-chart, surplus-deficit-line-chart, difference-area-chart]
layer: primitive
family: chart

primary_intent: deviation
secondary_intents: []

information_structure:
  shape: items
  attributes:
    - temporal
    - quantitative

scale:
  periods: 10〜300
  series: "1"

precision: overview

complexity: low

visual_encoding:
  time: position
  value: position
  deviation: area
  sign: color

text_dependency: low

abstraction: abstract

best_for:
  - 基準線からの隔たりの推移（損益・収支・目標との差）を見せる
  - 正負が入れ替わる時期を目立たせる
  - 期間が多く棒では細かすぎる

avoid_when:
  - 基準線が定まらない
  - 値が基準の片側にしか振れない
  - 個々の時点の値を正確に読ませる必要がある
  - 単色の媒体で上下の面の色が区別できない

alternatives:
  - diverging-bar-chart
  - line-chart
---

# 損益面グラフ

## 定義

時間に沿った値を折れ線で描き、基準線（ゼロ・目標・平均）との間を塗りつぶす図である。基準線より上の面と下の面を異なる色にし、黒字と赤字のような正負の期間を面で表す。面の広さが、隔たりの大きさと期間の長さの積として見える。

## 目的

基準からの隔たりが時間とともにどう推移したか、どの期間がどちら向きでどれだけだったかを、面の色と広がりで答えられるようにする。

## どういうときに利用するか

- 基準線からの隔たりの推移（損益・収支・目標との差）を見せる
- 正負が入れ替わる時期を目立たせる
- 期間が多く、期間ごとの棒では細かすぎる

## どういうときに利用してはいけないか

- 基準線が定まらない
- 値が基準の片側にしか振れない
- 個々の時点の値を正確に読ませる、または単色の媒体で上下の色が区別できない

## 入力の構造

`items: temporal + quantitative`。各時点の値と基準値を持つ。基準値は定数でも時点ごとの値でもよい。

| 月 | 収支（万円） |
| --- | --- |
| 2026-01 | +120 |
| 2026-02 | -45 |

## デザインの文法

- 横軸は時間、縦軸は値とし、基準線を太めに描いて基準の値を明記する
- 基準線より上の面と下の面を対照的な二色で塗る
- 折れ線は面より濃い色で細く描く
- 期間の目盛は等間隔にし、縦軸の範囲は上下で同じにする

## 作成時のルール

- 基準値が何かをキャプションに書く
- 正負が入れ替わる時点に注釈を置く
- 読み取ってほしい期間（最大の赤字期など）を一文で添える

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 縦軸の範囲を片側だけ広げ、面の大きさを歪める
- 複数の系列の面を重ねて塗る
- 正負の面に似た色相を使う

## 利用例

- 月次の損益を 36 か月分示し、赤字の期間を見せる
- 日次の在庫数と目標在庫との差を示す

## NGパターン

- 基準線をグラフの下端に置く: 下側の面が描けず、負の期間が消える
- 三系列の面を重ねる: 面が重なり合い、どの系列の正負か読めない
