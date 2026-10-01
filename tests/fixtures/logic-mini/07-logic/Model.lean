/-!
# 小さな論証の証人（テスト用）

Argument.lean の axiom を、同じ名前・同じ型の定義に差し替えた写し。
-/

namespace Mini

noncomputable section

/-- 開発の方式。 -/
inductive Method where
  | document
  | lean
  deriving DecidableEq

/-- 仕様。 -/
def Spec : Type := Bool

/-- 仕様が関門を通る。 -/
def passes : Spec → Prop := fun s => s = true

/-- 仕様が矛盾を含む。 -/
def contradictory : Spec → Prop := fun _ => False

/-- 方式ごとの、伝え間違えた要件の数。 -/
def missCount : Method → Nat := fun M => match M with
  | .document => 2
  | .lean => 1

/-- 【実験】関門を通った仕様は矛盾を含まない。
@support F1 -/
theorem passes_consistent : ∀ s : Spec, passes s → ¬ contradictory s :=
  fun _ _ h => h

/-- 【経験則】ドキュメント方式では、伝え間違いが起こる。
@support F2
@confidence 0.8
論拠: 承認の場で見落としが報告されている。
弱い点: 件数は1つのチームの記録だけ（F3 も参照）。 -/
theorem doc_miss_pos : 0 < missCount .document := by decide

/-- 【仮定】Lean 方式の伝え間違いは、ドキュメント方式より多くない。
@support なし
@confidence 0.5
論拠: 関門が矛盾を止める。
弱い点: 関門の外の伝え間違いは数えていない。
要ファクト: 両方式で、伝え間違えた要件の数を数える。 -/
theorem lean_le_doc : missCount .lean ≤ missCount .document := by decide

/-- 【経験則】Lean 方式でも、伝え間違いは起こる。
@support F3
@confidence 0.9
論拠: 試用で報告がある。
弱い点: 報告は未確認。 -/
theorem lean_miss_pos : 0 < missCount .lean := by decide

/-- @claim C1 [決定論] 関門を通った仕様は、矛盾を含まない。 -/
theorem claim_C1_no_contradiction : ∀ s : Spec, passes s → ¬ contradictory s :=
  fun s h => passes_consistent s h

/-- @claim C0 [件数] Lean 方式の伝え間違いは、ドキュメント方式より多くない。 -/
theorem claim_C0_not_worse : missCount .lean ≤ missCount .document :=
  lean_le_doc

/-- @claim C2 [件数] ドキュメント方式では伝え間違いが起こる。 -/
theorem claim_C2_doc_miss : 0 < missCount .document :=
  doc_miss_pos

/-- @beyond C0 どちらの方式でも伝え間違いは起こり、Lean 方式のほうが多くない。 -/
theorem beyond_C0_both : 0 < missCount .lean ∧ missCount .lean ≤ missCount .document :=
  ⟨lean_miss_pos, lean_le_doc⟩

end

end Mini
