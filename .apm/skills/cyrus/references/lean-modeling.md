# Lean でモデルを書くときの落とし穴と回避策

ステージ7で `Argument.lean` と証人 `Model.lean` を書くときの注意です。Lean 4 の標準ライブラリだけを使います（Mathlib は使いません）。

## Lean の落とし穴

| 落とし穴 | 回避策 |
|---|---|
| コンストラクタのない `inductive` は空の型になり、公理系が矛盾しやすい | 中身を決めない型は `axiom T : Type` で宣言する。CLI が門で止める |
| 名前空間付きの `def Foo.bar` の中で、同名の `bar` を書くと自分自身を指す | `_root_.bar` と書く |
| 宣言した関数に依存する `def` は、コードを生成できずにエラーになる | ファイル全体を `noncomputable section` で囲む |
| 自然数で「どこまでも狭義に増える」と「上限がある」を同時に要求すると、両立しない | 確率は `Rat` か `Prob` で表す |
| 確率の合成で、値が 0〜1 の範囲を外れる | 層ごとの「起こらない確率」の積を取り、その余事象にする |
| 範囲だけの公理（`_mem`）が増える | `Prob` の型に入れる（下の例）。入れてよいのは [0,1] の範囲だけ |
| `Nat` の引き算は 0 で打ち切られる | 大小関係を先に示すか、`Rat` を使う |
| `grind` は、`Rat` の定数計算・線形の不等式・環の等式は解けるが、積の単調性は解けない | 積の単調性は `Rat.mul_le_mul_of_nonneg_left` などの補題で示し、残りを `grind` に任せる |
| `decide` は `Rat` を含む式で止まる（`0 ≤ 1/10` のような定数の比較でも） | `Rat` には `decide` を使わず、`unfold` してから `grind` を使う |
| `simp` が、帰納法の仮定の中の関数まで書き換える | 先に「定数の和は件数×定数」のような補題を立て、それを使う |
| `native_decide` は、隠れた公理を増やす | 使わない（CLI が門で止める） |
| `Set` などは Mathlib にしかない | `List` や述語で表す |

範囲を型に入れる例:

```lean
structure Prob where
  val : Rat
  nonneg : 0 ≤ val
  le_one : val ≤ 1
```

型に置いた判断（例:「率は段階によらない」）を、docstring で「計算の性質」と書かないでください。範囲以外の判断は関係公理にします。

## CLI（`cyrus lean`）に読ませるための書き方

- `axiom`・`theorem`・`namespace`・`section`・`end` は行頭から書く。字下げした `axiom`・`theorem` は読めないので、門で止まる。
- docstring（`/-- … -/`）は、宣言の直前に置く。印（`@support` など）は docstring の中に1行ずつ書く。
- `@support` の行に書いた事実 ID は、支えとして読まれる。支えがないときは `@support なし（理由）` と書く。「なし」で始まる行の ID は読まれないので、理由に事実 ID を書いてよい。
- 関係公理の型の最上位と `∀` の直下に `∧` を置かない。`∃` の中、`→` の右、`¬` の中の `∧` はよい。
  - だめ: `axiom p_mem : ∀ M : Method, 0 ≤ p M ∧ p M ≤ 1`（原子命題2つを1つにまとめている）
  - よい: `axiom p_nonneg : ∀ M : Method, 0 ≤ p M` と `axiom p_le_one : ∀ M : Method, p M ≤ 1`（または `Prob` の型に入れる）
- 事実 ID は 06-facts.json のとおりに書く。分けた事実は枝番（`F26a`）で書き、親の番号（`F26`）を残さない。
- 証人 `Model.lean` は、`Argument.lean` の `axiom` を同じ名前・同じ型の `def` / `theorem` に差し替えるだけにする。axiom 以外のコードの行は同じ順で残す。コメントと docstring は変えてよい。
- 証人の定義は、Lean 標準の公理（`propext`・`Classical.choice`・`Quot.sound`）以外に依存してはいけない（`sorry` を使うと止まる）。
- 証人の証明に `DecidableEq` などが要るなら、`deriving` は `Argument.lean` の帰納型の側に書く（証人は axiom 以外の行を変えられず、`instance` も足せないため）。
- 証人で、宣言した型を数の型（`Nat` など）にして数値リテラル（`(0 : Person)` など）を使うなら、`def` ではなく `abbrev` にする（`def` だとインスタンスが見つからない）。
- 証人には `example` を足してよい。主張の定理の前提が証人の世界で成り立つことは、`example` で示して残す。
- 2周目から `Argument.lean` の axiom 以外の行を直したら、`Model.lean` にも同じ変更を写す（写し忘れると LG022 で止まる）。
