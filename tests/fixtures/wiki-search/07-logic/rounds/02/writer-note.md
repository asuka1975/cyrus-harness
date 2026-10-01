# Writer の作業の報告（2周目）

差分の設計書（model-plan-delta.md）の1節〜12節のとおりに、Argument.lean と Model.lean を直した。model-plan.md と食い違うところは、差分に従った。

## 書いたもの

- `07-logic/Argument.lean`
  - §1: `Method` に `tuned` を足した（`current`・`tuned`・`fullText`）。`Prob` は変えていない。
  - §2: 宣言21個。足したもの: `extraOtherMinutes`・`estimateYen`・`gainYen`（`Approvable` より前）・`CurrentIncremental`・`IndexComplete`。
    名前を変えたもの: `missExtraMinutes` → `extraNotYetMinutes`。消したもの: `CheaperFix`。docstring を差分の3.1節に合わせた。
  - §3: 計算の def 8個。足したもの: `missAfterIndex`・`savedOverTunedMinutes`・`savedOverTunedWageYen`。
    名前を変えたもの: `lostYen` → `lostWageYen`、`benefitYen` → `savedWageYen`。計算を変えたもの: `lostMinutes`。
  - §4: 関係公理47個（【実験】3・【経験則】2・【自明】5・【仮定】37）。差分の12節の数と一致する。
    - 消した7個: `cost_eq`・`no_cheaper_fix`・`searches_same`・`foundMinutes_same`・`missExtra_same`・`noHit_same`・`overlook_same`。
    - 足した28個: 差分の4.4節の表のとおり。
    - 型か種類を変えた5個: `search_decomp`（型）、`miss_compose`（【仮定】→【自明】）、`notYet_le_of_fast`（前提に `IndexComplete M` を足した）、
      `missExtra_current_ge` → `extraNotYet_current_ge`（名前と型）、`approvable_of_net`（型）。
    - docstring だけを変えた8個: 差分の4.3節のとおり。
    - 4.5節で「共通」「同上」とまとめてあった論拠・弱い点・要ファクト・`@support なし` の理由は、公理ごとに全文を書いた。「Writer への注」は写していない。
  - §5: 式の補題を含む途中の定理、主張の定理6個（C0・C1 は1個ずつ、C2・C3 は2個ずつ）、`@baseline` 1個、[不利] 3個。
    - 消した2個: `miss_current_ge`・`saved_only_from_notYet`。
    - 足したもの: `notYet_tuned_ge`・`saved_ge_gap`・`savedOverTuned_ge_gap`・`savedOverTuned_ge`・`unfav_saved_le_gap`（[不利]）と、式の補題3個（下の「設計書と違うところ」）。
- `07-logic/Model.lean`（証人）: Argument.lean の axiom 68個（宣言21・関係公理47）を、同じ名前・同じ型の `def` / `theorem` に差し替えた。
  axiom 以外の行は、Argument.lean から機械的に写した（手で写し直していないので、行の食い違いはない）。末尾に、関係公理の前提が成り立つことを示す `example` を8個足した。
- 冒頭の「主張と定理の対応」の表と「設計書（model-plan.md）との違い」を書き直した。

## 定理が依存する関係公理の確かめ

`#print axioms` で、すべての定理が依存する関係公理を出し、差分の6.1節の「使う判断」の列と突き合わせた。すべて一致した。とくに次を確かめた。

- `saved_ge_gap` は `extraNotYet_current_ge`（符号だけ）を使い、`extraNotYet_nonneg` を使わない。
- `unfav_saved_le_gap` は `extraNotYet_nonneg` を使い、`extraNotYet_current_ge` を使わない。主張の側の `_full_le` も使わない。
- `unfav_saved_le_lost` は `_full_ge` のうち時間と回数の4つだけを使い、`noHit_full_ge`・`overlook_full_ge` を使わない。
- `baseline_lost_le_survey` は `searchesPerDay_nonneg` を使い、`searches_current_ge` を使わない。
- `claim_C0_approvable` は `claim_C3_saved` を使わず、層1の tuned の値は `notYet_tuned_ge` だけから来る。
  その結果、C0 は `delay_current_ge_workday` に依存しなくなった（手戻りの一覧で、この公理の行き先は C2・C3 だけになる）。

## 設計書と違うところ

Argument.lean の冒頭の「設計書（model-plan.md）との違い」にも同じことを書いた。

1. 数の補題 `rat_mul_le_mul` は1周目のまま残した（`grind` が積の単調性を解けないため）。
2. 式の補題を3つ足した。差分の6.1節の「Writer への注」の式の変形を、定理として切り出しただけで、新しい判断は含まない。
   - `missAfterIndex_nonneg`: `Prob` の範囲だけから出る。関係公理を使わない（確信度 1）。
   - `miss_sub_notYet`: 見つからない確率 − 層1の確率 =（1 − 層1の確率）× `missAfterIndex`。【自明】の `miss_compose` だけを使う（確信度 1）。
   - `search_layers`: `search_decomp` を、上の式で書き直したもの。【自明】の2つだけを使う（確信度 1）。
   - 理由: `saved_ge_gap`・`savedOverTuned_ge_gap`・`unfav_saved_le_gap`・`unfav_saved_le_lost`・`lost_ge` で同じ変形を繰り返さないため。
3. `savedOverTuned_ge_gap` は、`saved_ge_gap` を途中の定理として使って示した。差分の「saved_ge_gap と同じ判断に、tuned の6つを足したもの」のとおりで、依存する関係公理も一致する。
4. `search_current_eq` の1行目（命題の文）を「検索で探し物をするのに使う時間は20分」に直した。差分は論拠と弱い点だけを変えるとしているが、
   3.1節で `searchMinutes` を「検索で使う時間」に限ったので、1行目も合わせた。`@confidence 0.75` と `@reviewer` の行は、1字も変えていない。
5. 差分の5節で向きを数え直した公理のうち、docstring に「向き:」の行がなかった `prodDelay_le_test`（新方式に有利）と `beneficiaries_ge`（新方式に不利）に、「向き:」の行を足した。
6. `delay_current_ge_workday` の要ファクトにある「（登録すれば @support に足せる）」は、「（登録すれば、支える事実に足せる）」と書いた。
   CLI は docstring の中の `@support` を、行の途中でも印として読むため（下の「検査について」）。
7. 同じ理由で、`current_not_incremental` の弱い点の「@against にも @support にも置けない」は、「反対の証拠にも支える事実にも置けない」と書いた。
8. 重なる文を1つにまとめたところがある。`prodDelay_le_test` の要ファクト（「本番と同じ記事数の環境で測る」と「本番の記事数（約3万件）の環境で測る」）、
   `beneficiaries_ge` の論拠（「回答者だけを数えるのは不利な向き」が2度出る）。意味は変えていない。
9. `workDays_ge` の向きの行から、「1周目は控えめな値としていたが」と「（R8）」を外した。docstring には、いまの判断だけを書いた。

### 名前を変えずに型を変えた公理について

呼び出し元の指示に「公理の命題を変えたり分けたりするときは、名前を変えて新しい公理として書きます」とある。
一方、差分の設計書は、`search_decomp`・`notYet_le_of_fast`・`approvable_of_net` の型を、名前を変えずに変えている（`miss_compose` は種類だけを変え、型は変えていない）。

差分の設計書に従い、名前はそのままにした。理由は次の2つ。

- この3つには `@reviewer` の行がない。名前を変える決まりは、Reviewer が下げた値を、命題を変えたあとに持ち越さないためのもので、守るべき判断がない。
- 名前を変えると、`cyrus logic-round diff` が差分の設計書の行（`search_decomp` など）を宣言に当てられず、消した公理と足した公理に分かれて出る。

`cost_eq` を `estimate_eq` と `cost_le_estimate` に分け、`missExtra_current_ge` を `extraNotYet_current_ge` にしたのは、差分の設計書が名前を変えているとおり。
`cost_eq` を消したので、その `@reviewer` の行（0.3 ← 0.6）もなくなった。`estimate_eq` は F4 の値（0.6）になり、費用の経路の値は `cost_le_estimate` の 0.05 に下がる（差分の4.5節の注のとおり）。

## 証人の世界

差分の6.3節の値をもとにした。境目ちょうどの値ばかりにしないため、ほかの値に響かない量だけを、不等式が真に成り立つ値に変えた。

| 量 | 6.3節 | 証人 | 真に成り立つようになった公理 |
|---|---|---|---|
| `indexDelaySec .tuned` | 86400 | 43200 | `tuned_slow_of_rebuild`（28800 < 43200） |
| `indexDelaySec .fullText` | 4.2 | 4 | `prodDelay_le_test`（4 < 4.2） |
| `firstYearCost` | 3,000,000 | 2,800,000 | `cost_le_estimate` |
| `gainYen` | 5,220,864 | 6,000,000 | `gain_ge_wage` |
| `manyMinutes` | 20 | 15 | `many_threshold_le` |

- 主張の下限を決める量の案（回数4、余分な時間5、層1の 1/10 と 1/1000、層2・層3の 1/5、412人、200日、3,000円）は、6.3節のまま境目の値にした。
  変えると `foundMinutes` などが連れて変わり、6.2節・6.3節と照らしにくくなるため。境目の値でも、主張の不等式は余裕をもって成り立つ（5,220,864円 > 3,000,000円）。
- `Approvable` は「`firstYearCost` < `gainYen`」と定義した（差分の11節）。前提が崩れれば結論も崩れる世界で、`approvable_of_net` が試される。
- 含意の形の関係公理は、どれも前提が成り立つ例を持つ。`notYet_ge_of_slow` は `current`（86400秒）と `tuned`（43200秒）、
  `notYet_le_of_fast` は `fullText`（4秒、`IndexComplete` が真）、`tuned_slow_of_rebuild` は `CurrentIncremental` が偽、`approvable_of_net` は 2,800,000 < 6,000,000。
  Model.lean の末尾の `example` に残した。主張の定理は、どれも前提を持たない。

## 門の結果

`python3 .claude/skills/cyrus/scripts/cyrus.py --doc wiki-search lean`: エラー 0 件・警告 0 件・参考 0 件。

- 証人: 68個の型がすべて一致、元の行はすべて同じ順で残っている（missing_lines 0）、Lean 標準の3公理以外に依存しない。
- 主張ごとの確信度: C0 0.05、C1 0.05、C2 0.05、C3 0.05（どれも hypothesis）。1周目から上がった主張はない。
- 原子命題47（【自明】5・【実験】3・【経験則】2・【仮定】37。主張の定理が使う39、`@baseline` だけが使う0、使われない8）。
- 公理の値: `search_current_eq` 0.75（Reviewer の値のまま）、`delay_current_ge_workday` 0.3（同）、`estimate_eq` 0.6（F4）、`testDelay_le_five` 0.95、`beneficiaries_ge` 0.9、【自明】5つは 1、【仮定】37はすべて 0.05。

## 検査について・Reviewer に伝えたい点

- **CLI は、docstring の中の `@support`・`@against`・`@confidence`・`@reviewer` を、行の途中でも印として読む。**
  `_ids_on_lines` は `@support\b([^\n]*)` を docstring のどこからでも拾う。差分の設計書の文（「登録すれば @support に足せる」「@against にも @support にも置けない」）を
  そのまま写すと、印の行として読まれる（この2つは事実 ID を含まないので値は変わらない。ただ、文中の `@support` の後に事実 ID が来れば支えに数えられ、
  `@confidence` の後に数が来れば `@confidence` が2つあることになり LG008 で止まる）。ガイドには「印は docstring の中に1行ずつ書く」とあるだけで、
  文中に書いてはいけないことは書かれていない。検査の誤りとまでは言えないが、Planner が設計書に印の語をそのまま書くと、Writer が言い換えることになる。
- **「使われない」8つの原子は、設計どおり。** 7つ（`_full_ge` の6つと `extraNotYet_nonneg`）は [不利] の定理だけが使う。`searchMinutes_nonneg` は [不利] の `unfav_saved_le_survey` だけが使う。
  [不利] の定理に印を付けないので、CLI は公理の使用に数えない。手戻りの一覧で「主張 なし」と出るのも、この7つである。
- **公理系の全体は、置き換えで6つの量が変わらないことを仮定している。** `_full_le` と `_full_ge` を両方置いたので、合わせると `searchesPerDay`・`foundMinutes`・`extraNotYetMinutes`・
  `extraOtherMinutes`・`pNoHit`・`pOverlook` の `fullText` と `current` は等しくなる（どの証人でも同じ。Model.lean の冒頭にも書いた）。
  片側に分けた効果は、定理ごとの依存に表れる（主張の定理は `_full_le` だけ、不利な結論の定理は `_full_ge` だけ）。どちらかの片側が崩れると、もう一方の側の定理は残る。
- `search_current_eq` の `@reviewer` の行は、いまはない `missExtraMinutes` に触れている。Reviewer だけが付ける印なので、変えずに残した。
  差分の設計書は、範囲が合ったかを Reviewer が設問5の文面で確かめる、としている。
- C0 の最も弱い公理の一覧に29個、C3 に19個が並ぶ。どれも 0.05 で、特定の公理が特に弱いという意味ではない。
