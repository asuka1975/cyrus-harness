---
id: parallel-coordinates
name: 平行座標プロット
aliases: [parallel-coordinates-plot, parallel-coordinate-chart, pcp]
layer: primitive
family: chart

primary_intent: magnitude-comparison
secondary_intents: []

information_structure:
  shape: items
  attributes:
    - categorical
    - quantitative

scale:
  categories: 4〜12
  items: 5〜100

precision: overview

complexity: medium

visual_encoding:
  attribute: position
  value: position
  item: connection
  group: color

text_dependency: medium

abstraction: abstract

best_for:
  - 項目が多く（四〜十二）一覧で比べる
  - 対象が多く（数十〜百）傾向のある群を見つける
  - 特定の対象を目立たせて全体の中での位置を示す

avoid_when:
  - 項目が三つ以下
  - 対象が数百を超えて線が塗りつぶされる
  - 個々の値を正確に読ませる必要がある
  - 読み手がこの記法に慣れておらず凡例を置けない

alternatives:
  - radar-chart
  - comparison-table
  - bar-chart
---

# 平行座標プロット

## 定義

複数の項目を平行に並べた縦軸に割り当て、対象ごとに各軸上の値を折れ線で結ぶ図である。線の形が対象の特徴を表し、隣り合う軸の間で線が交差するかどうかが、項目間の関係を示す。

## 目的

多くの項目にわたって対象がどのような値の組を持つか、どの対象が似ているか、どの対象が外れているかを、線の形で答えられるようにする。

## どういうときに利用するか

- 項目が多く（四〜十二）、一覧で比べる
- 対象が多く（数十〜百）、傾向のある群を見つける
- 特定の対象を目立たせ、全体の中での位置を示す

## どういうときに利用してはいけないか

- 項目が三つ以下である
- 対象が数百を超え、線が塗りつぶされる
- 個々の値を正確に読ませる、または読み手がこの記法に慣れていない

## 入力の構造

`items: categorical + quantitative`。対象ごとに全項目の値を持つ。項目ごとの尺度は違ってよい。

| サーバー | CPU（%） | メモリ（%） | 応答時間（ms） |
| --- | --- | --- | --- |
| web-01 | 45 | 70 | 120 |
| web-02 | 92 | 88 | 850 |

## デザインの文法

- 軸は等間隔に平行に並べ、軸ごとに独立した尺度と最小値・最大値を書く
- 軸の順序は、関係を見たい項目を隣に置く
- 線は細く半透明にし、目立たせる対象だけ濃い色にする
- 群は色で区別し、三色までにする

## 作成時のルール

- 軸の順序を変えて見え方を比べ、伝えたい関係が読める順に決める
- 各軸の向き（上が大きい）をそろえる
- 目立たせる線は一〜三本にとどめ、読み取ってほしい特徴を一文で添える

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 線に太さや塗りを加え、面として読ませる
- 軸の尺度を書かず、線の高さだけ見せる
- すべての線を同じ濃さで描く

## 利用例

- 三十台のサーバーを八項目で比べ、異常な一台を目立たせる
- 製品候補を十項目で比べ、似た製品の群を見る

## NGパターン

- 千対象を不透明な線で描く: 線が重なり、どの対象も読めない
- 軸の順序を無作為に並べる: 隣接軸の交差に意味がなく、関係が読めない
