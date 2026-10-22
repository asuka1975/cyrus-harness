---
id: line-column-chart
name: 棒と折れ線グラフの複合グラフ
aliases: [line-column, line-and-column-chart, combo-chart, bar-line-chart]
layer: primitive
family: chart

primary_intent: time-series-change
secondary_intents:
  - correlation

information_structure:
  shape: items
  attributes:
    - temporal
    - quantitative
    - quantitative

scale:
  periods: 3〜30
  series: 2（棒と線で一つずつ）

precision: overview

complexity: medium

visual_encoding:
  period: position
  amount: length
  rate: position
  series: color

text_dependency: medium

abstraction: abstract

best_for:
  - 量（売上など）と比率（成長率など）の推移を同じ期間で並べて見せる
  - 量と割合の関係が時期によってどう変わるかを見せる

avoid_when:
  - 二つの系列が同じ単位で、一つの軸で描ける
  - 二つの軸の目盛を操作しないと関係が見えない
  - 期間が三十を超え、棒が細くなって読めない

alternatives:
  - line-chart
  - bar-chart
---

# 棒と折れ線グラフの複合グラフ

## 定義

横軸に時点を取り、量を棒の長さで、比率を折れ線の位置で描く図である。棒と線は単位が違うため、左右に別の縦軸を持つ。棒が量を、線が比率を担う役割分担を固定する。

## 目的

量と比率が時間とともにそれぞれどう推移し、両者がどの時期に連動し、どの時期に離れたかを答えられるようにする。

## どういうときに利用するか

- 単位の違う量と比率を、同じ期間で並べて見せたい
- 量が増えても比率が下がった時期など、二系列のずれを見せたい
- 期間が三十以下で、棒を一本ずつ見分けられる

## どういうときに利用してはいけないか

- 二系列が同じ単位で、一つの軸で描ける
- 読み手が二軸の読み方に慣れておらず、添え書きで補えない
- 軸の範囲を操作しないと二系列が重ならない

## 入力の構造

`items: temporal + quantitative + quantitative`。各時点が量と比率の二つの数値を持つ。

| 月 | 売上 (百万円) | 利益率 (%) |
| --- | --- | --- |
| 1月 | 120 | 8.5 |
| 2月 | 135 | 7.9 |

## デザインの文法

- 量は棒、比率は線に固定し、逆にしない
- 左軸を棒、右軸を線に対応させ、軸の見出しに単位を書く
- 棒と線の色を軸の見出しの色と揃え、どちらの軸かを示す
- 棒の軸は 0 から始める

## 作成時のルール

- 右軸の範囲は、線が棒と無意味に交差しないように取る
- 二系列の関係（連動か独立か）をキャプションに一文で書く
- 線の系列は一本に絞る
- 比率の軸は 0 または基準値（100% など）を含める

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 二つの軸の範囲を調整して、交差や一致を演出する
- 同じ単位の二系列に二軸を使う
- 棒を二系列以上積み上げて、線と重ねる

## 利用例

- 月ごとの売上（棒）と利益率（線）を並べ、売上が伸びても利益率が落ちた時期を示す
- 週ごとのリクエスト数（棒）とエラー率（線）を並べ、負荷と障害の関係を示す

## NGパターン

- 右軸の範囲を狭め、線が棒の頂点をなぞるように見せる。読み手は強い連動と誤読する
- 売上と費用（どちらも円）を棒と線に分ける。同じ軸で比べられるのに二軸が差を隠す
