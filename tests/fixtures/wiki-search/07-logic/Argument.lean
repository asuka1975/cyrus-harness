/-!
# 論証構造: 社内Wiki検索の刷新提案
-/

-- ========== 命題 ==========
/-- F1: 社員は検索で探し物をするのに1日平均20分使っている -/
axiom P_F1 : Prop
/-- F2: 不満の理由の1位は当日の記事が出てこないこと（48%） -/
axiom P_F2 : Prop
/-- F3: 試験環境では保存から5秒以内に検索に出た -/
axiom P_F3 : Prop
/-- F4: 初年度費用の見積もりは300万円 -/
axiom P_F4 : Prop
/-- 本番でも試験環境と同じ速さで検索に出る -/
axiom P_ProdLikeTrial : Prop
/-- C0: 置き換えのため来期予算で300万円を承認してほしい -/
axiom P_C0 : Prop
/-- C1: 社員が探し物に多くの時間を使っている -/
axiom P_C1 : Prop
/-- C2: 置き換えれば記事がすぐ検索に出る -/
axiom P_C2 : Prop
/-- C3: 費用は失われている時間に比べて小さい -/
axiom P_C3 : Prop

-- ========== 事実 ==========
/-- @fact F1 -/
axiom fact_F1 : P_F1
/-- @fact F2 -/
axiom fact_F2 : P_F2
/-- @fact F3 -/
axiom fact_F3 : P_F3
/-- @fact F4 -/
axiom fact_F4 : P_F4

-- ========== 仮定 ==========
/-- @confidence 0.7 本番は記事数が多いが、試験環境と同じ構成なら速さは大きく変わらないと見込む -/
axiom assume_ProdLikeTrial : P_ProdLikeTrial

-- ========== 推論規則と主張 ==========
/-- @confidence 0.9 1日20分は勤務時間の4%にあたり、多いと言える -/
axiom rule_C1 : P_F1 ∧ P_F2 → P_C1
theorem claim_C1 : P_C1 := rule_C1 ⟨fact_F1, fact_F2⟩

/-- @confidence 0.85 試験環境で速く、本番も同等なら、記事はすぐ検索に出る -/
axiom rule_C2 : P_F3 ∧ P_ProdLikeTrial → P_C2
theorem claim_C2 : P_C2 := rule_C2 ⟨fact_F3, assume_ProdLikeTrial⟩

/-- @confidence 0.8 社員400名の1日20分を金額にすると、300万円を大きく上回る -/
axiom rule_C3 : P_F4 ∧ P_F1 → P_C3
theorem claim_C3 : P_C3 := rule_C3 ⟨fact_F4, fact_F1⟩

/-- @confidence 0.85 問題があり、解決でき、費用が見合うなら、承認を求めるのは妥当である -/
axiom rule_C0 : P_C1 ∧ P_C2 ∧ P_C3 → P_C0
theorem claim_C0 : P_C0 := rule_C0 ⟨claim_C1, claim_C2, claim_C3⟩
