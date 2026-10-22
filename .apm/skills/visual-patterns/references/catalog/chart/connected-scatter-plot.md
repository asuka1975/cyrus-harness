---
id: connected-scatter-plot
name: つなげた散布図
aliases: [connected-scatterplot, connected-scatter-chart]
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
  periods: 5〜30
  series: 1〜2

precision: overview

complexity: medium

visual_encoding:
  x-variable: position
  y-variable: position
  time-order: connection
  series: color

text_dependency: medium

abstraction: abstract

best_for:
  - 二つの変数が時間とともにどう連動して変化したかを一本の軌跡で見せる
  - 変化の方向が途中で反転した時期を見せる

avoid_when:
  - 読み手がこの読み方に慣れておらず、説明を添えられない
  - 時点が多く、軌跡が交差して順序を追えない
  - 一方の変数の推移だけが答えである

alternatives:
  - line-chart
  - scatter-plot
---

# つなげた散布図

## 定義

横軸と縦軸に数値変数を取り、各時点の値を点として描き、時間順に線でつなぐ図である。線は時間の経路を表し、点の位置が二変数の値を表す。時間は軸に持たず、点のラベルと線の向きで示す。

## 目的

二つの変数が時間とともにどの方向へ動き、連動の仕方がいつ変わったかを答えられるようにする。

## どういうときに利用するか

- 二変数の変化を一本の軌跡として同時に辿らせたい
- 二変数の関係が、ある時期を境に変わったことを見せたい
- 時点が三十以下で、線を順に追える

## どういうときに利用してはいけないか

- 読み手が軌跡の読み方を知らず、添え書きで補えない
- 時点が多く、線が交差して順序を追えない
- 一方の変数の推移だけが答えで、もう一方は不要である

## 入力の構造

`items: temporal + quantitative + quantitative`。各時点が二つの数値を持ち、時点の順序が決まっている。

| 年 | 失業率 (%) | インフレ率 (%) |
| --- | --- | --- |
| 2021 | 2.8 | 0.2 |
| 2022 | 2.6 | 2.5 |

## デザインの文法

- 始点と終点を目立たせ、矢印または色の濃淡で時間の向きを示す
- 主な時点（年など）のラベルを点の近くに直接書く
- 線は細くし、点の位置が読めるようにする
- 系列は二つまでにし、色で分ける

## 作成時のルール

- 軌跡の読み方（線は時間順）をキャプションに一文で書く
- 時点の間隔が不均一な場合は、ラベルで明示する
- 向きが反転した時点があれば、そこに注釈を置く
- 二軸の範囲は軌跡全体が収まるように取り、途中で切らない

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 時間の向きを示す手がかり（矢印・濃淡・ラベル）を省く
- 系列を三つ以上重ねて軌跡を絡ませる
- 点を省いて線だけにする

## 利用例

- 失業率とインフレ率の年ごとの組み合わせを軌跡で描き、関係が変わった時期を示す
- 広告費と新規顧客数の月ごとの推移を軌跡で描き、費用対効果が落ちた時期を示す

## NGパターン

- 日次データ三百点をつなぐ。線が絡み合い、順序も傾向も読めない
- 矢印もラベルもなく線だけを描く。読み手はどちらが始点か分からず、単なる相関の図と誤読する
