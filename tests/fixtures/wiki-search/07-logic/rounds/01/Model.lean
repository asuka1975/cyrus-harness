/-!
# 証人: 社内Wiki検索の刷新提案

`Argument.lean` のすべての `axiom` を、同じ名前・同じ型の具体的な `def` / `theorem` に差し替えた写し。公理系が無矛盾であることの証拠。
axiom 以外の行は、`Argument.lean` と同じ順で残している。`instance`・`attribute`・`open`・`set_option` は足していない。

## 証人の世界（設計書 model-plan.md の5節の値の例のとおり）

| 量 | current | fullText |
|---|---|---|
| `indexDelaySec`（秒） | 86400 | 4.2 |
| `pNotYet` | 1/10 | 1/1000 |
| `pNoHit`・`pOverlook` | 1/5 | 1/5 |
| `missProb` | 53/125（0.424） | 1127/3125（0.36064） |
| `searchesPerDay`（回） | 4 | 4 |
| `foundMinutes`（分） | 72/25（2.88） | 72/25（2.88） |
| `missExtraMinutes`（分） | 5 | 5 |
| `searchMinutes`（分。`search_decomp` の式で計算） | 20 | 18.7328 |

方式によらない量: `testDelaySec` 4.2、`beneficiaries` 412、`workDays` 200、`wagePerHour` 3000、`firstYearCost` 3,000,000、
`manyMinutes` 20。`CheaperFix` は偽、`Approvable` は真。

この世界で、関係公理の前提は空回りしない。

- `notYet_ge_of_slow` の前提（遅れ 28800 秒以上）は `current` で成り立ち（86400 秒）、結論 1/10 ≤ 1/10 が成り立つ。
- `notYet_le_of_fast` の前提（遅れ 5 秒以内）は `fullText` で成り立ち（4.2 秒）、結論 1/1000 ≤ 1/1000 が成り立つ。
- `approvable_of_net` の前提は2つとも成り立つ（`benefitYen` = 4,120,000 × 1.2672 = 5,220,864 円 > 3,000,000 円、`CheaperFix` は偽）。
- `savedMinutes` = 1.2672 分、`lostMinutes` = 8.48 分。

多くの量は、関係公理の境目の値に置いている（回数 4、余分な時間 5、層1の確率 1/10 と 1/1000、層2・層3の確率 1/5、
人数 412、日数 200、人件費 3000、境目 20）。境目の値でも、主張の定理の真の不等式（費用 < 1年分の人件費など）は余裕をもって成り立つ。
真に成り立つ不等式もある（`testDelay_le_five` は 4.2 < 5、`delay_current_ge_workday` は 28800 < 86400、
`searchMinutes_nonneg`・`foundMinutes_nonneg` は 0 より大きい）。
-/

namespace WikiSearch

-- 公理で宣言した関数に依存する定義は実行できないので、すべて計算不能として扱う
noncomputable section

/-! ## §1 帰納型（定義） -/

/-- 比べる2つの方式。`current` はいまの検索の仕組み、`fullText` は置き換えた後の全文検索エンジン。 -/
inductive Method where
  | current
  | fullText

/-- 確率。型に入れるのは、0 以上 1 以下という範囲だけ。 -/
structure Prob where
  val : Rat
  nonneg : 0 ≤ val
  le_one : val ≤ 1

/-! ## §2 宣言（中身を決めない型・関数・定数） -/

/-- 証人: 記事の保存から検索に出るまでの秒数。いまの検索は 86400 秒（1日）、置き換えた後は 4.2 秒。 -/
def indexDelaySec : Method → Rat := fun M => match M with
  | .current => 86400
  | .fullText => 21 / 5

/-- 証人: 試験環境の計測値。F3 の最大 4.2 秒。 -/
def testDelaySec : Rat := 21 / 5

/-- 証人: 層1の確率。いまの検索は 1/10、置き換えた後は 1/1000。 -/
def pNotYet : Method → Prob := fun M => match M with
  | .current => ⟨1 / 10, by grind, by grind⟩
  | .fullText => ⟨1 / 1000, by grind, by grind⟩

/-- 証人: 層2の確率。どちらの方式も 1/5。 -/
def pNoHit : Method → Prob := fun _ => ⟨1 / 5, by grind, by grind⟩

/-- 証人: 層3の確率。どちらの方式も 1/5。 -/
def pOverlook : Method → Prob := fun _ => ⟨1 / 5, by grind, by grind⟩

/-- 証人: 見つからない確率。層の確率から `miss_compose` の式で計算した値。 -/
def missProb : Method → Prob := fun M => match M with
  | .current => ⟨53 / 125, by grind, by grind⟩
  | .fullText => ⟨1127 / 3125, by grind, by grind⟩

/-- 証人: 1人1日の探し物の回数。どちらの方式も 4 回。 -/
def searchesPerDay : Method → Rat := fun _ => 4

/-- 証人: 見つかった探し物1回の時間。どちらの方式も 2.88 分（いまの検索の1日の時間が 20 分になるように決めた）。 -/
def foundMinutes : Method → Rat := fun _ => 72 / 25

/-- 証人: 見つからなかった探し物1回の余分な時間。どちらの方式も 5 分。 -/
def missExtraMinutes : Method → Rat := fun _ => 5

/-- 証人: 1人1日の探し物の時間。`search_decomp` の式で計算する（いまの検索は 20 分、置き換えた後は 18.7328 分）。 -/
def searchMinutes : Method → Rat := fun M =>
  searchesPerDay M * (foundMinutes M + (missProb M).val * missExtraMinutes M)

/-- 証人: 効果を受ける社員の数。412 人。 -/
def beneficiaries : Rat := 412

/-- 証人: 1年の勤務日数。200 日。 -/
def workDays : Rat := 200

/-- 証人: 1時間あたりの人件費。3,000 円。 -/
def wagePerHour : Rat := 3000

/-- 証人: 初年度の費用。3,000,000 円。 -/
def firstYearCost : Rat := 3000000

/-- 証人: 「多い」の境目。20 分。 -/
def manyMinutes : Rat := 20

/-- 証人: もっと安い方法は、この世界にはない。 -/
def CheaperFix : Prop := False

/-- 証人: 承認する理由は、この世界ではそろっている。 -/
def Approvable : Prop := True

/-! ## §3 計算の def（手順だけ。判断を入れない） -/

/-- 読み (a) の「失われている時間」（分）: いまの検索の、1日の探し物の回数 × 見つからない確率 × 見つからなかった1回の余分な時間。 -/
def lostMinutes : Rat :=
  searchesPerDay .current * (missProb .current).val * missExtraMinutes .current

/-- 読み (b) の「取り戻せる時間」（分）: 1人1日の探し物の時間の、いまの検索と置き換えた後の差。 -/
def savedMinutes : Rat :=
  searchMinutes .current - searchMinutes .fullText

/-- 1人1日1分の時間が、1年で何円の人件費になるか: 人数 × 勤務日数 × 1時間あたりの人件費 ÷ 60。 -/
def yenPerDailyMinute : Rat :=
  beneficiaries * workDays * wagePerHour / 60

/-- 読み (a) の時間の、1年分の人件費（円）。 -/
def lostYen : Rat :=
  yenPerDailyMinute * lostMinutes

/-- 読み (b) の時間の、1年分の人件費（円）。 -/
def benefitYen : Rat :=
  yenPerDailyMinute * savedMinutes

/-! ## §4 関係公理 -/

/-! ### 【実験】 -/

/-- 証人: 4 ×（2.88 ＋ 0.424 × 5）= 20。 -/
theorem search_current_eq : searchMinutes .current = 20 := by
  show (4 : Rat) * (72 / 25 + 53 / 125 * 5) = 20
  grind

/-- 証人: 4.2 ≤ 5。 -/
theorem testDelay_le_five : testDelaySec ≤ 5 := by
  show (21 / 5 : Rat) ≤ 5
  grind

/-- 証人: 定義どおり。 -/
theorem cost_eq : firstYearCost = 3000000 := rfl

/-! ### 【経験則】 -/

/-- 証人: 28800 ≤ 86400。 -/
theorem delay_current_ge_workday : 28800 ≤ indexDelaySec .current := by
  show (28800 : Rat) ≤ 86400
  grind

/-- 証人: 412 ≤ 412。 -/
theorem beneficiaries_ge : 412 ≤ beneficiaries := by
  show (412 : Rat) ≤ 412
  grind

/-! ### 【自明】 -/

/-- 証人: `searchMinutes` をこの式で定義したので、定義どおり。 -/
theorem search_decomp : ∀ M : Method,
  searchMinutes M = searchesPerDay M * (foundMinutes M + (missProb M).val * missExtraMinutes M) :=
  fun _ => rfl

/-- 証人: 20 と 18.7328 は 0 以上。 -/
theorem searchMinutes_nonneg : ∀ M : Method, 0 ≤ searchMinutes M := by
  intro M
  cases M
  · show (0 : Rat) ≤ 4 * (72 / 25 + 53 / 125 * 5)
    grind
  · show (0 : Rat) ≤ 4 * (72 / 25 + 1127 / 3125 * 5)
    grind

/-- 証人: 2.88 は 0 以上。 -/
theorem foundMinutes_nonneg : ∀ M : Method, 0 ≤ foundMinutes M := by
  intro _
  show (0 : Rat) ≤ 72 / 25
  grind

/-! ### 【仮定】層1: まだ検索に出ない -/

/-- 証人: 4.2 ≤ 4.2。 -/
theorem prodDelay_le_test : indexDelaySec .fullText ≤ testDelaySec := by
  show (21 / 5 : Rat) ≤ 21 / 5
  grind

/-- 証人: `current` で前提が成り立ち（86400 秒）、結論 1/10 ≤ 1/10 が成り立つ。`fullText` では前提が成り立たない（4.2 秒）。 -/
theorem notYet_ge_of_slow : ∀ M : Method, 28800 ≤ indexDelaySec M → 1 / 10 ≤ (pNotYet M).val := by
  intro M h
  cases M
  · show (1 / 10 : Rat) ≤ 1 / 10
    grind
  · have h' : (28800 : Rat) ≤ 21 / 5 := h
    grind

/-- 証人: `fullText` で前提が成り立ち（4.2 秒）、結論 1/1000 ≤ 1/1000 が成り立つ。`current` では前提が成り立たない（86400 秒）。 -/
theorem notYet_le_of_fast : ∀ M : Method, indexDelaySec M ≤ 5 → (pNotYet M).val ≤ 1 / 1000 := by
  intro M h
  cases M
  · have h' : (86400 : Rat) ≤ 5 := h
    grind
  · show (1 / 1000 : Rat) ≤ 1 / 1000
    grind

/-! ### 【仮定】層2・層3: いまの検索の値 -/

/-- 証人: 1/5 ≤ 1/5。 -/
theorem noHit_current_le : (pNoHit .current).val ≤ 1 / 5 := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-- 証人: 1/5 ≤ 1/5。 -/
theorem overlook_current_le : (pOverlook .current).val ≤ 1 / 5 := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-! ### 【仮定】層2・層3: 同じとみなす -/

/-- 証人: どちらの方式も同じ値。 -/
theorem noHit_same : pNoHit .fullText = pNoHit .current := rfl

/-- 証人: どちらの方式も同じ値。 -/
theorem overlook_same : pOverlook .fullText = pOverlook .current := rfl

/-! ### 【仮定】層の合成 -/

/-- 証人: 1 − 9/10 × 4/5 × 4/5 = 53/125、1 − 999/1000 × 4/5 × 4/5 = 1127/3125。 -/
theorem miss_compose : ∀ M : Method,
  (missProb M).val = 1 - (1 - (pNotYet M).val) * (1 - (pNoHit M).val) * (1 - (pOverlook M).val) := by
  intro M
  cases M
  · show (53 / 125 : Rat) = 1 - (1 - 1 / 10) * (1 - 1 / 5) * (1 - 1 / 5)
    grind
  · show (1127 / 3125 : Rat) = 1 - (1 - 1 / 1000) * (1 - 1 / 5) * (1 - 1 / 5)
    grind

/-! ### 【仮定】時間: いまの検索の値 -/

/-- 証人: 4 ≤ 4。 -/
theorem searches_current_ge : 4 ≤ searchesPerDay .current := by
  show (4 : Rat) ≤ 4
  grind

/-- 証人: 5 ≤ 5。 -/
theorem missExtra_current_ge : 5 ≤ missExtraMinutes .current := by
  show (5 : Rat) ≤ 5
  grind

/-! ### 【仮定】時間: 同じとみなす -/

/-- 証人: どちらの方式も同じ値。 -/
theorem searches_same : searchesPerDay .fullText = searchesPerDay .current := rfl

/-- 証人: どちらの方式も同じ値。 -/
theorem foundMinutes_same : foundMinutes .fullText = foundMinutes .current := rfl

/-- 証人: どちらの方式も同じ値。 -/
theorem missExtra_same : missExtraMinutes .fullText = missExtraMinutes .current := rfl

/-! ### 【仮定】金額に直す -/

/-- 証人: 200 ≤ 200。 -/
theorem workDays_ge : 200 ≤ workDays := by
  show (200 : Rat) ≤ 200
  grind

/-- 証人: 3000 ≤ 3000。 -/
theorem wage_ge : 3000 ≤ wagePerHour := by
  show (3000 : Rat) ≤ 3000
  grind

/-! ### 【仮定】読者の判断 -/

/-- 証人: 20 ≤ 20。 -/
theorem many_threshold_le : manyMinutes ≤ 20 := by
  show (20 : Rat) ≤ 20
  grind

/-- 証人: `CheaperFix` は偽。 -/
theorem no_cheaper_fix : ¬ CheaperFix := fun h => h

/-- 証人: `Approvable` は真。前提も2つとも成り立つ（5,220,864 円 > 3,000,000 円、`CheaperFix` は偽）。 -/
theorem approvable_of_net : firstYearCost < benefitYen → ¬ CheaperFix → Approvable :=
  fun _ _ => trivial

/-! ## §5 主張の定理 -/

/-! ### 数の補題（関係公理を使わない） -/

/-- 0 以上の数どうしの不等式は、掛け合わせても成り立つ（a ≤ b、c ≤ d ならば a × c ≤ b × d）。 -/
theorem rat_mul_le_mul {a b c d : Rat} (ha : 0 ≤ a) (hab : a ≤ b) (hc : 0 ≤ c) (hcd : c ≤ d) :
    a * c ≤ b * d := by
  have h1 : a * c ≤ b * c := Rat.mul_le_mul_of_nonneg_right hab hc
  have h2 : b * c ≤ b * d := Rat.mul_le_mul_of_nonneg_left hcd (by grind)
  grind

/-! ### 途中の定理 -/

/-- いまの検索で、まだ検索に出ていない記事を探す確率は 1/10 以上。 -/
theorem notYet_current_ge : 1 / 10 ≤ (pNotYet .current).val :=
  notYet_ge_of_slow .current delay_current_ge_workday

/-- 置き換えた後、まだ検索に出ていない記事を探す確率は 1/1000 以下。 -/
theorem notYet_fullText_le : (pNotYet .fullText).val ≤ 1 / 1000 := by
  have h1 := prodDelay_le_test
  have h2 := testDelay_le_five
  exact notYet_le_of_fast .fullText (by grind)

/-- いまの検索で、探し物1回が見つからない確率は 1/10 以上（層2・層3の値によらず、層1の確率以上になる）。 -/
theorem miss_current_ge : 1 / 10 ≤ (missProb .current).val := by
  have hm := miss_compose .current
  have ha := notYet_current_ge
  have ha1 := (pNotYet .current).le_one
  have hb0 := (pNoHit .current).nonneg
  have hb1 := (pNoHit .current).le_one
  have hc0 := (pOverlook .current).nonneg
  have hc1 := (pOverlook .current).le_one
  have hx : (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) ≤ 1 * 1 :=
    rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
  have hy : (1 - (pNotYet .current).val) * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val))
      ≤ (1 - (pNotYet .current).val) * (1 * 1) :=
    Rat.mul_le_mul_of_nonneg_left hx (by grind)
  grind

/-- いまの検索の「失われている時間」（読み a）は、1人1日2分以上（4回 × 1/10 × 5分）。 -/
theorem lost_ge : 2 ≤ lostMinutes := by
  unfold lostMinutes
  have hs := searches_current_ge
  have hm := miss_current_ge
  have he := missExtra_current_ge
  have h1 : 4 * (1 / 10) ≤ searchesPerDay .current * (missProb .current).val :=
    rat_mul_le_mul (by grind) hs (by grind) hm
  have h2 : 4 * (1 / 10) * 5 ≤ searchesPerDay .current * (missProb .current).val * missExtraMinutes .current :=
    rat_mul_le_mul (by grind) h1 (by grind) he
  grind

/-- 取り戻せる時間（読み b）= 回数 × 余分な時間 ×（層2で失敗しない確率 × 層3で失敗しない確率）×（層1の確率の差）。
取り戻せる時間は、層1の差からだけ生まれる。 -/
theorem saved_only_from_notYet :
    savedMinutes = searchesPerDay .current * missExtraMinutes .current
      * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val))
      * ((pNotYet .current).val - (pNotYet .fullText).val) := by
  unfold savedMinutes
  rw [search_decomp .current, search_decomp .fullText, miss_compose .current, miss_compose .fullText,
    searches_same, foundMinutes_same, missExtra_same, noHit_same, overlook_same]
  grind

/-- 取り戻せる時間（読み b）は、1人1日 792/625 分（1.2672分）以上（4回 × 5分 ×（4/5 × 4/5）×（1/10 − 1/1000））。 -/
theorem saved_ge : 792 / 625 ≤ savedMinutes := by
  rw [saved_only_from_notYet]
  have hs := searches_current_ge
  have he := missExtra_current_ge
  have hb := noHit_current_le
  have hc := overlook_current_le
  have ha := notYet_current_ge
  have hf := notYet_fullText_le
  have hx : (4 / 5) * (4 / 5) ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
    rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
  have h1 : 4 * 5 ≤ searchesPerDay .current * missExtraMinutes .current :=
    rat_mul_le_mul (by grind) hs (by grind) he
  have h2 : 4 * 5 * ((4 / 5) * (4 / 5))
      ≤ searchesPerDay .current * missExtraMinutes .current
        * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val)) :=
    rat_mul_le_mul (by grind) h1 (by grind) hx
  have h3 : 4 * 5 * ((4 / 5) * (4 / 5)) * (1 / 10 - 1 / 1000)
      ≤ searchesPerDay .current * missExtraMinutes .current
        * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val))
        * ((pNotYet .current).val - (pNotYet .fullText).val) :=
    rat_mul_le_mul (by grind) h2 (by grind) (by grind)
  grind

/-- 1人1日1分の時間は、1年で 4,120,000円以上の人件費になる（412人 × 200日 × 3,000円 ÷ 60）。 -/
theorem yenPerDailyMinute_ge : 4120000 ≤ yenPerDailyMinute := by
  unfold yenPerDailyMinute
  have hb := beneficiaries_ge
  have hw := workDays_ge
  have hp := wage_ge
  have h1 : 412 * 200 ≤ beneficiaries * workDays := rat_mul_le_mul (by grind) hb (by grind) hw
  have h2 : 412 * 200 * 3000 ≤ beneficiaries * workDays * wagePerHour :=
    rat_mul_le_mul (by grind) h1 (by grind) hp
  grind

/-! ### 主張の定理 -/

/-- @claim C3 [確率] 読み (b): 初年度の費用は、置き換えで取り戻せる時間の1年分の人件費より小さい。 -/
theorem claim_C3_saved : firstYearCost < benefitYen := by
  unfold benefitYen
  have hy := yenPerDailyMinute_ge
  have hs := saved_ge
  have hc := cost_eq
  have h : 4120000 * (792 / 625) ≤ yenPerDailyMinute * savedMinutes :=
    rat_mul_le_mul (by grind) hy (by grind) hs
  grind

/-- @claim C3 [確率] 読み (a): 初年度の費用は、いまの検索で失われている時間の1年分の人件費より小さい。 -/
theorem claim_C3_lost : firstYearCost < lostYen := by
  unfold lostYen
  have hy := yenPerDailyMinute_ge
  have hl := lost_ge
  have hc := cost_eq
  have h : 4120000 * 2 ≤ yenPerDailyMinute * lostMinutes :=
    rat_mul_le_mul (by grind) hy (by grind) hl
  grind

/-- @claim C0 [確率] 来期予算で300万円を承認する理由がそろう。 -/
theorem claim_C0_approvable : Approvable :=
  approvable_of_net claim_C3_saved no_cheaper_fix

/-- @claim C1 [決定論] いまの検索で1人1日に探し物に使う時間は、「多い」の境目以上。 -/
theorem claim_C1_many : manyMinutes ≤ searchMinutes .current := by
  rw [search_current_eq]
  exact many_threshold_le

/-- @claim C2 [決定論] 項1: 置き換えれば、記事は保存から5秒以内に検索に出る。 -/
theorem claim_C2_soon : indexDelaySec .fullText ≤ 5 := by
  have h1 := prodDelay_le_test
  have h2 := testDelay_le_five
  grind

/-- @claim C2 [決定論] 項2: 置き換えれば、記事はいまより早く検索に出る。 -/
theorem claim_C2_faster : indexDelaySec .fullText < indexDelaySec .current := by
  have h1 := claim_C2_soon
  have h2 := delay_current_ge_workday
  grind

/-! ### 比べる相手の確認と、不利な結論 -/

/-- @baseline いまの検索の「失われている時間」（読み a）を、アンケートの1日20分より大きく置いていない。 -/
theorem baseline_lost_le_survey : lostMinutes ≤ 20 := by
  unfold lostMinutes
  have hd := search_decomp .current
  have he := search_current_eq
  have hs := searches_current_ge
  have hf := foundMinutes_nonneg .current
  have h0 : 0 ≤ searchesPerDay .current * foundMinutes .current := Rat.mul_nonneg (by grind) hf
  grind

/-- [不利] 置き換えで取り戻せる時間は、1人1日20分を超えない。 -/
theorem unfav_saved_le_survey : savedMinutes ≤ 20 := by
  unfold savedMinutes
  have he := search_current_eq
  have hn := searchMinutes_nonneg .fullText
  grind

/-- [不利] 置き換えで取り戻せる時間（読み b）は、いまの検索で失われている時間（読み a）を超えない。 -/
theorem unfav_saved_le_lost : savedMinutes ≤ lostMinutes := by
  unfold savedMinutes lostMinutes
  rw [search_decomp .current, search_decomp .fullText, searches_same, foundMinutes_same, missExtra_same]
  have hs := searches_current_ge
  have he := missExtra_current_ge
  have hm := (missProb .fullText).nonneg
  have h0 : 0 ≤ searchesPerDay .current * (missProb .fullText).val * missExtraMinutes .current :=
    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hm) (by grind)
  grind

end

end WikiSearch
