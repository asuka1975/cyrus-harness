---
id: force-field-diagram
name: フォースフィールド図
aliases: [force-field-analysis, lewin-force-field-diagram]
layer: primitive
family: diagram

primary_intent: opposing-forces
secondary_intents: []

information_structure:
  shape: items
  attributes:
    - categorical
    - ordinal

scale:
  items: 4〜16
  groups: 2（推進・抑制）

precision: overview

complexity: low

visual_encoding:
  side: position
  direction: shape
  strength: length

text_dependency: medium

abstraction: abstract

best_for:
  - 変化を推進する要因と妨げる要因を対置し、どちらが優勢かを見せる
  - 施策の実行前に、強めるべき要因と弱めるべき要因を共有する

avoid_when:
  - 要因の強さを測定値として正確に比べさせたい
  - 要因同士の因果の連鎖が主題である
  - 要因が一方にしかなく、対立の構図がない

alternatives:
  - cause-effect-chain
  - diverging-bar-chart
  - comparison-table
---

# フォースフィールド図

## 定義

中央に現状や目標の線を引き、変化を推進する要因を一方から、妨げる要因を反対側から、線に向かう矢印として並べた図である。矢印の長さや太さで要因の強さを示す。レヴィンの力の場の分析に由来する。

## 目的

読み手が「この変化を何が推し進め、何が妨げているか、どちらが優勢か」に答えられるようにする。

## どういうときに利用するか

- 施策や変更の実行可能性を、賛成と障害の要因を対置して検討させたい
- 要因が両側に複数あり、箇条書きでは対立の構図と強さの偏りが見えない
- 施策の計画で、強める要因と取り除く要因を決める材料を示したい

## どういうときに利用してはいけないか

- 要因の強さが測定値で、正確に比べさせたい。矢印の長さは評価の目安にすぎない
- 要因が互いに引き起こし合い、連鎖が主題である
- 要因が片側にしかない。対置する相手がなく、箇条書きで足りる

## 入力の構造

items: categorical + ordinal。各要因が推進か抑制かの区分と、強さの段階を持つ。

```yaml
change: テスト自動化の導入
forces:
  - {name: 手動テストの工数増, side: driving, strength: 3}
  - {name: 既存コードの結合度, side: restraining, strength: 2}
```

## デザインの文法

- 中央に変化の対象を縦の線か枠で示し、左に推進、右に抑制の要因を置く
- 矢印は両側から中央の線に向け、向きで推進と抑制を区別する
- 強さは矢印の長さに対応づけ、段階を 3〜5 にそろえる
- 推進と抑制を色でも区別し、凡例を付ける

## 作成時のルール

- 要因は短い名詞句にし、推進か抑制かが一つに決まる形で書く
- 強さの段階の基準（何を 3 とするか）を本文かキャプションに書く
- 図から読み取ってほしい結論（どちらが優勢か、何を変えるか）を本文に一文で書く

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- 強さに根拠がないのに矢印の長さを変える
- 同じ要因を推進と抑制の両側に書く
- 要因の数の多さを強さの優勢と読ませる

## 利用例

- テスト自動化の導入判断。工数削減や品質の要因と、学習コストや既存コードの要因を対置する
- 組織変更の計画。推進する関係者の支持と、現場の抵抗の要因を示す

## NGパターン

- 矢印の長さを全部同じにする。推進と抑制の列挙にとどまり、どちらが優勢かが読めない
- 要因を 20 以上並べる。対立の構図が埋もれ、重要な要因が分からない
