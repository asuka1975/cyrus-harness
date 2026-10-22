---
id: fault-tree
name: 故障の木
aliases: [failure-tree, fault-tree-diagram, fault-tree-analysis]
layer: primitive
family: diagram

primary_intent: causation
secondary_intents: []

information_structure:
  shape: hierarchy
  attributes:
    - categorical

scale:
  levels: 2〜6
  nodes: 5〜40

precision: exact

complexity: high

visual_encoding:
  gate-type: shape
  cause-effect: connection
  level: position

text_dependency: medium

abstraction: abstract

best_for:
  - 頂上の事象がどの原因の組み合わせ（AND・OR）で起きるかを論理的に示す
  - 単一の原因で致命的な結果に至る経路を見つけさせる

avoid_when:
  - 読み手が論理ゲートの記号を知らない
  - 原因の組み合わせ条件が定まらず、因果の向きだけを示したい
  - 因果がループする

alternatives:
  - cause-effect-chain
  - ishikawa-diagram
---

# 故障の木

## 定義

望ましくない事象を頂上に置き、その原因となる事象を論理ゲート（AND・OR）で結んで下へ展開した木である。ゲートは、下位の事象がすべて起きたときに上位が起きるか、いずれか一つで起きるかを区別する。末端には基本事象を置く。

## 目的

読み手が「頂上の事象は、どの原因がどう組み合わさると起きるか」に答えられるようにする。

## どういうときに利用するか

- 障害や事故の原因を、組み合わせ条件を含めて論理的に示したい
- 単一の基本事象で頂上事象に至る経路（単一障害点）を見つけさせたい
- 安全性やリスクの評価で、原因の構造を関係者と正確に共有したい

## どういうときに利用してはいけないか

- 読み手が AND・OR のゲート記号を知らず、凡例でも補えない（手順2 の末尾の制約）
- 原因の組み合わせ条件が未確定で、連鎖の向きだけを見せたい
- 原因が結果に戻るループを含み、木にならない

## 入力の構造

hierarchy: categorical。根が頂上事象、中間ノードがゲートの種類を持ち、葉が基本事象。

```yaml
top: データ消失
gate: AND
children:
  - {event: 主系ディスク故障}
  - {event: バックアップ失敗, gate: OR, children: [ジョブ未実行, 保存先の容量不足]}
```

## デザインの文法

- 頂上事象を最上部に置き、下へ展開する。深さを位置で読ませる
- AND と OR は標準のゲート記号で区別し、記号の違いが一目で分かる大きさにする
- 事象は長方形、基本事象は円など、事象の種類を形で区別する
- 同じ深さの事象を横にそろえる

## 作成時のルール

- ゲート記号の凡例を図の中に置く
- 事象は「何が」「どうなる」の形で一つの状態として書く
- 単一障害点となる経路を色で強調し、本文に結論として書く

## 意図の型と手段

| 意図の型 | 手段 |
| --- | --- |

## やってはいけないこと

- ゲートを省略して線だけで結び、AND と OR を区別しない
- 一つの事象を木の複数箇所に書き、同じ原因を別の原因に見せる
- 対策や推奨を事象として木に混ぜる

## 利用例

- 機器の安全性評価。致命的な故障に至る基本事象の組み合わせを示す
- システム障害の分析。冗長化が効かなかった条件を AND ゲートで示す

## NGパターン

- すべてのゲートを OR にした木。分類して並べただけになり、組み合わせ条件を示す意味がない
- ゲートの記号を独自の形にする。読み手の慣習にない記号は学習を要し、誤読を招く
