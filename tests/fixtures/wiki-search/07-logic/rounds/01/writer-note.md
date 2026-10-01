# Writer の作業の報告（1周目）

## 書いたもの

- `07-logic/Argument.lean`: 設計書（model-plan.md）の2節・3節・5節のとおりに書いた。
  - §1: `Method`（`current`・`fullText`）、`Prob`（値・0以上・1以下）。
  - §2: 宣言17個（`indexDelaySec` など。中身を決めない `axiom`）。
  - §3: 計算の def 5個（`lostMinutes`・`savedMinutes`・`yenPerDailyMinute`・`lostYen`・`benefitYen`）。
  - §4: 関係公理26個（【実験】3・【経験則】2・【自明】3・【仮定】18）。どれも原子命題1つ。
  - §5: 数の補題1個、途中の定理7個、主張の定理6個（C0・C1 は1個ずつ、C2・C3 は2個ずつ）、`@baseline` 1個、[不利] 2個。
- `07-logic/Model.lean`: 証人。`Argument.lean` の axiom 43個（とその docstring）だけを、同じ名前・同じ型の `def` / `theorem` に差し替えた。
  値は設計書5節の「証人の値の例」のとおり。

## 設計書と違うところ

`Argument.lean` の冒頭の「設計書（model-plan.md）との違い」にも同じことを書いた。

1. 数の補題 `rat_mul_le_mul` を足した（0 以上の数どうしの不等式を掛け合わせる）。
   - 理由: 標準ライブラリの `grind` は積の単調性を解けない（試して確かめた）。ガイドの落とし穴の表のとおり、
     `Rat.mul_le_mul_of_nonneg_left/right` で補題を立て、残りを `grind` に任せた。
   - 関係公理を使わないので、確信度には効かない。現実についての判断は含まない。
2. 設計書4節に載っている「同じとみなす」置き方の公理7つに、「向き:」の行を足した（4節の向きを写しただけ）。
3. `*_same` の5つの弱い点は、設計書の3.1節が「4節」に預けているので、4節と6節の説明から書いた。
   `missExtra_same` だけは材料がなかったので、中立の向きに合わせて「探し直しの時間は検索の仕組みで変わりうる（どちらの向きにも）」と書いた。
   Reviewer に確かめてほしい。

定理が依存する関係公理は、`#print axioms` で確かめ、設計書5節の「使う判断」の列とすべて一致した。

## 書き方で気をつけたこと

- `@support なし（…）` の括弧の中に事実 ID を書かなかった。CLI は `@support` の行にある事実 ID をすべて支えとして読むので、
  理由に F3 などを書くと、支えのない公理が F3 に支えられたことになる。事実 ID は「論拠:」「弱い点:」に書いた。
- そのため、`prodDelay_le_test` の弱い点の F3 と、`notYet_ge_of_slow` の論拠・弱い点の F2 は、`@support` にない事実として手がかりに出るはず。
  設計書が「支える事実: なし」としているとおりで、隠していない。
- `@confidence` は設計書の案のまま（【経験則】の `delay_current_ge_workday` 0.6、`beneficiaries_ge` 0.9、【仮定】はすべて 0.05）。
- `cost_eq` は【実験】だが、設計書に要ファクトがあるので「要ファクト:」も書いた。

## 門の結果

`python3 .claude/skills/cyrus/scripts/cyrus.py --doc wiki-search lean`: エラー 0 件・警告 0 件。

- 証人: 43個の型がすべて一致、元の行はすべて同じ順で残っている、Lean 標準の3公理以外に依存しない。
- 主張ごとの確信度: C0 0.05、C1 0.05、C2 0.05、C3 0.05（どれも hypothesis）。
  - C1 は `many_threshold_le`、C2 は `prodDelay_le_test`、C3 と C0 は【仮定】の連なり（層の確率・回数・時間・金額）で決まる。
- 原子命題26（主張の定理が使う24、`@baseline` だけが使う1、使われない1）。

## 証人の世界について

- 多くの量を、関係公理の境目の値に置いた（回数 4、余分な時間 5、層1の確率 1/10 と 1/1000、層2・層3の確率 1/5、人数 412、日数 200、人件費 3000、「多い」の境目 20）。
  設計書5節の値の例のとおりで、境目の値でも主張の不等式（費用 < 1年分の人件費）は余裕をもって成り立つ（5,220,864円と8,240,000円 > 3,000,000円）。
- 含意の形の関係公理は、前提が実際に成り立つ例を持つ。`notYet_ge_of_slow` は `current`（86400秒）、`notYet_le_of_fast` は `fullText`（4.2秒）、
  `approvable_of_net` は前提が2つとも成り立つ。
- 真に成り立つ不等式もある（`testDelay_le_five` は 4.2 < 5、`delay_current_ge_workday` は 28800 < 86400、`searchMinutes_nonneg`・`foundMinutes_nonneg` は 0 より大きい）。

## 検査が誤っていると思う点・Reviewer に伝えたい点

- 「使われない」公理1つは `searchMinutes_nonneg`、「`@baseline` だけが使う」1つは `foundMinutes_nonneg`。
  `searchMinutes_nonneg` は [不利] の定理 `unfav_saved_le_survey` が使っている。設計書の指示どおり [不利] の定理に印を付けていないので、
  CLI は公理の使用に数えない。ガイドの決まりどおりの数え方で、検査の誤りではないが、手がかりの「使われない公理」は、この事情で出ている。
- C3 の「最も弱い公理」が `foundMinutes_same` と出るのは、0.05 の公理が18個並んでいて、そのうち最初のものが選ばれているだけ。
  この公理が特に弱いという意味ではない。
- 誤りだと思う検査はなかった。
