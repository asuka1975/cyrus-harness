/-!
# 小さな論証（テスト用）

門をすべて通る最小の論証。テストは、この写しを1か所ずつ壊して、門が止まることを確かめる。
-/

namespace Mini

noncomputable section

/-- 開発の方式。 -/
inductive Method where
  | document
  | lean
  deriving DecidableEq

/-- 仕様。 -/
axiom Spec : Type

/-- 仕様が関門を通る。 -/
axiom passes : Spec → Prop

/-- 仕様が矛盾を含む。 -/
axiom contradictory : Spec → Prop

/-- 方式ごとの、伝え間違えた要件の数。 -/
axiom missCount : Method → Nat

/-- 【実験】関門を通った仕様は矛盾を含まない。
@support F1 -/
axiom passes_consistent : ∀ s : Spec, passes s → ¬ contradictory s

/-- 【経験則】ドキュメント方式では、伝え間違いが起こる。
@support F2
@confidence 0.8
論拠: 承認の場で見落としが報告されている。
弱い点: 件数は1つのチームの記録だけ（F3 も参照）。 -/
axiom doc_miss_pos : 0 < missCount .document

/-- 【仮定】Lean 方式の伝え間違いは、ドキュメント方式より多くない。
@support なし
@confidence 0.5
論拠: 関門が矛盾を止める。
弱い点: 関門の外の伝え間違いは数えていない。
要ファクト: 両方式で、伝え間違えた要件の数を数える。 -/
axiom lean_le_doc : missCount .lean ≤ missCount .document

/-- 【経験則】Lean 方式でも、伝え間違いは起こる。
@support F3
@confidence 0.9
論拠: 試用で報告がある。
弱い点: 報告は未確認。 -/
axiom lean_miss_pos : 0 < missCount .lean

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
