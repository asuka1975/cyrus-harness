---
id: proportional-symbol
name: プロポーショナル・シンボル
aliases: [ordered-proportional-symbol, proportional-symbol-chart, proportional-circle-chart]
layer: primitive
family: chart

primary_intent: magnitude-comparison
secondary_intents: [ranking]

information_structure:
  shape: items
  attributes:
    - categorical
    - quantitative

scale:
  items: 2〜12
  series: "1"

precision: overview

complexity: low

visual_encoding:
  category: position
  value: area

text_dependency: low

abstraction: abstract

best_for:
  - 値の差が極端に大きく最大値に合わせた軸では小さい値が見えない
  - おおまかな規模の違いを伝える
  - 記号を値の順に並べて規模の順位を見せる

avoid_when:
  - 値の差が小さく面積の違いが読めない
  - 個々の値を正確に読ませる必要がある
  - 項目が十を超えて記号が重なる

alternatives:
  - bar-chart
  - lollipop-chart
---

# プロポーショナル・シンボル

## 定義

項目ごとに円などの記号を置き、値を記号の面積で表す図である。記号は一列に並べることも、値の順に並べることもできる。面積は長さより差を読み取りにくいため、桁が違うほどの差を見せるのに向く。

## 目的

どれが桁違いに大きいか、規模の順はどうかを、記号の面積の違いで答えられるようにする。

## どういうときに利用するか

- 値の差が極端に大きく、最大値に合わせた軸では小さい値が見えない
- おおまかな規模の違いを伝えればよい
- 記号を値の順に並べ、規模の順位を見せる

## どういうときに利用してはいけないか

- 値の差が小さく、面積の違いが読めない
- 個々の値を正確に読ませる必要がある
- 項目が十を超え、記号が重なる

## 入力の構造

`items: categorical + quantitative`。項目名と数値の組を一行ずつ持つ。

| サービス | 月間リクエスト数 |
| --- | --- |
| 検索 | 1200000000 |
| 管理画面 | 35000 |

## デザインの文法

- 値は半径ではなく面積に比例させる
- 記号の形は一種類にそろえ、同じ基準線上に並べる
- 記号の中か直下に項目名と値を書く
- 凡例に代表的な値の記号を二、三個置き、面積と値の対応を示す

## 作成時のルール

- 最大の記号が図の幅に収まるよう、面積の基準値を決める
- 読み手に比べさせたい二つの記号を隣に置く
- 記号同士は重ねず、間隔をそろえる
- 読み取ってほしい規模の差を一文で添える

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 半径や直径を値に比例させる
- 立体の球や錐体で描く
- 記号を地図や座標の上に置き、位置に意味があるように見せる

## 利用例

- 主要国の国内総生産を円の面積で比べ、上位国との差を見せる
- サービスごとの月間リクエスト数（数万〜十億）を比べる
- 製品ごとの累計出荷台数を値の順に並べる

## NGパターン

- 直径を値に比例させる: 面積は値の二乗になり、差を誇張する
- 値が 100 と 120 の二項目を円で比べる: 面積の差が読み取れず、同じに見える
