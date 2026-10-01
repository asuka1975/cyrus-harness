/-!
# 証人: 社内Wiki検索の刷新提案

`Argument.lean` のすべての `axiom` を、同じ名前・同じ型の具体的な `def` / `theorem` に差し替えた写し。公理系が無矛盾であることの証拠。
axiom 以外の行は、`Argument.lean` と同じ順で残している。`instance`・`attribute`・`open`・`set_option` は足していない。
末尾に、関係公理の前提が成り立つことを示す `example` を足した。

## 証人の世界（差分の設計書 model-plan-delta.md の6.3節の値をもとにした）

| 量 | current | tuned | fullText |
|---|---|---|---|
| `indexDelaySec`（秒） | 86400 | 43200 | 4 |
| `pNotYet` | 1/10 | 1/10 | 1/1000 |
| `pNoHit`・`pOverlook` | 1/5 | 1/5 | 1/5 |
| `missProb` | 53/125（0.424） | 53/125 | 1127/3125（0.36064） |
| `missAfterIndex`（計算） | 9/25 | 9/25 | 9/25 |
| `searchesPerDay`（回） | 4 | 4 | 4 |
| `foundMinutes`（分） | 72/25（2.88） | 72/25 | 72/25 |
| `extraNotYetMinutes`・`extraOtherMinutes`（分） | 5 | 5 | 5 |
| `searchMinutes`（分。`search_decomp` の式で計算） | 20 | 20 | 18.7328 |
| `IndexComplete` | 真 | 真 | 真 |

方式によらない量: `testDelaySec` 4.2、`beneficiaries` 412、`workDays` 200、`wagePerHour` 3000、`estimateYen` 3,000,000、
`firstYearCost` 2,800,000、`manyMinutes` 15、`gainYen` 6,000,000。`CurrentIncremental` は偽。
`Approvable` は「`firstYearCost` < `gainYen`」と定義した（前提が崩れれば結論も崩れる世界で、`approvable_of_net` を試す）。

計算の値: `savedMinutes` と `savedOverTunedMinutes` は 1.2672 分、`lostMinutes` は 8.48 分、`yenPerDailyMinute` は 4,120,000 円、
`savedWageYen` と `savedOverTunedWageYen` は 5,220,864 円、`lostWageYen` は 34,937,600 円。

### 設計書の6.3節の値から変えたところ

境目ちょうどの値ばかりにしないため、ほかの値に響かない量を、関係公理の不等式が真に成り立つ値にした。

- `indexDelaySec .tuned` を 86400 から 43200 にした（`tuned_slow_of_rebuild` の結論 28800 < 43200 が真に成り立つ。`pNotYet .tuned` は 1/10 のまま）。
  安い設定の変更は、いまのままより速いが、8時間より短くはならない世界になる。
- `indexDelaySec .fullText` を 4.2 から 4 にした（`prodDelay_le_test` が 4 < 4.2 で真に成り立つ）。
- `firstYearCost` を 3,000,000 から 2,800,000 にした（`cost_le_estimate` が真に成り立つ）。
- `gainYen` を 5,220,864 から 6,000,000 にした（`gain_ge_wage` が真に成り立つ）。
- `manyMinutes` を 20 から 15 にした（`many_threshold_le` が真に成り立つ）。

### 不等式が、真に成り立つか、境目ちょうどか

- 真に成り立つ（<）: `testDelay_le_five`（4.2 < 5）、`delay_current_ge_workday`（28800 < 86400）、`prodDelay_le_test`（4 < 4.2）、
  `tuned_slow_of_rebuild`（28800 < 43200）、`cost_le_estimate`、`gain_ge_wage`、`many_threshold_le`、`extraNotYet_nonneg`・`extraOther_nonneg`（0 < 5）、
  `searchMinutes_nonneg`・`foundMinutes_nonneg`・`searchesPerDay_nonneg`、`missAfterIndex_nonneg`。
- 境目ちょうど（=）: `notYet_ge_of_slow`（1/10）、`notYet_le_of_fast`（1/1000）、`noHit_current_le`・`overlook_current_le`（1/5）、
  `searches_current_ge`（4）、`extraNotYet_current_ge`（5）、`extraOther_le_notYet`（5 = 5）、`beneficiaries_ge`（412）、`workDays_ge`（200）、`wage_ge`（3000）。
  どれも主張の下限を決める量の案の値で、6.3節の値のまま残した。境目の値でも、主張の定理の真の不等式（費用 < 人件費）は余裕をもって成り立つ。
- `_tuned_ge` の6つも等号で満たしている（`tuned` の層1のほかの量は、いまの検索と同じにした）。

### 公理系そのものが決める等号（証人の選び方ではない）

置き換えの片側の公理は、主張の側（`_full_le`）と不利な結論の側（`_full_ge`）の両方を置いている。
2つを合わせると、`searchesPerDay`・`foundMinutes`・`extraNotYetMinutes`・`extraOtherMinutes`・`pNoHit`・`pOverlook` の6つの量で、
`fullText` の値は `current` の値に等しくなる。これはどの証人でも同じで、公理系の全体としては1周目の等式と同じ世界しか許さない。
片側に分けた効果は、定理ごとの依存（主張の定理は `_full_le` だけ、不利な結論の定理は `_full_ge` だけに頼る）に表れる。

### 前提が空回りしないこと

含意の形の関係公理は、どれも前提が成り立つ例を持つ（末尾の `example`）。

- `notYet_ge_of_slow` の前提（遅れ 28800 秒以上）は、`current`（86400 秒）と `tuned`（43200 秒）で成り立つ。
- `notYet_le_of_fast` の前提（遅れ 5 秒以内、欠けた記事がない）は、`fullText`（4 秒、`IndexComplete` が真）で成り立つ。
- `tuned_slow_of_rebuild` の前提（`CurrentIncremental` でない）は成り立つ。
- `approvable_of_net` の前提（2,800,000 < 6,000,000）は成り立ち、`Approvable` はこの前提そのものなので、前提が崩れれば結論も崩れる。
- 主張の定理（`claim_C0_approvable`・`claim_C1_many`・`claim_C2_soon`・`claim_C2_faster`・`claim_C3_saved`・`claim_C3_lost`）は、どれも前提を持たない。
-/

namespace WikiSearch

-- 公理で宣言した関数に依存する定義は実行できないので、すべて計算不能として扱う
noncomputable section

/-! ## §1 帰納型（定義） -/

/-- 比べる3つの方式。
`current` は、いまの検索の仕組み（中身が Elasticsearch などの全文検索エンジンかは、06-facts.json にない）。
`tuned` は、いまの検索の仕組みのまま、300万円より安い費用でできる設定の変更（索引を作り直す間隔を短くする、保存のたびに索引へ足す、など）を、
保存から検索に出るまでがいちばん短くなるように施したもの。そうした変更ができないなら、いまのままと同じもの。
`fullText` は、置き換えた後の全文検索エンジン。 -/
inductive Method where
  | current
  | tuned
  | fullText

/-- 確率。型に入れるのは、0 以上 1 以下という範囲だけ。 -/
structure Prob where
  val : Rat
  nonneg : 0 ≤ val
  le_one : val ≤ 1

/-! ## §2 宣言（中身を決めない型・関数・定数） -/

/-- 証人: 記事の保存から検索に出るまでの秒数。いまの検索は 86400 秒（1日）、安い設定の変更は 43200 秒（半日）、
置き換えた後は 4 秒（試験環境の最大 4.2 秒より短い）。 -/
def indexDelaySec : Method → Rat := fun M => match M with
  | .current => 86400
  | .tuned => 43200
  | .fullText => 4

/-- 証人: 試験環境の計測値。F3 の最大 4.2 秒。 -/
def testDelaySec : Rat := 21 / 5

/-- 証人: いまの仕組みは、保存のたびに索引へ足せない（偽）。 -/
def CurrentIncremental : Prop := False

/-- 証人: どの方式も、すべての記事を索引に持っている（真）。 -/
def IndexComplete : Method → Prop := fun _ => True

/-- 証人: 層1の確率。いまの検索と安い設定の変更は 1/10、置き換えた後は 1/1000。 -/
def pNotYet : Method → Prob := fun M => match M with
  | .current => ⟨1 / 10, by grind, by grind⟩
  | .tuned => ⟨1 / 10, by grind, by grind⟩
  | .fullText => ⟨1 / 1000, by grind, by grind⟩

/-- 証人: 層2の確率。どの方式も 1/5。 -/
def pNoHit : Method → Prob := fun _ => ⟨1 / 5, by grind, by grind⟩

/-- 証人: 層3の確率。どの方式も 1/5。 -/
def pOverlook : Method → Prob := fun _ => ⟨1 / 5, by grind, by grind⟩

/-- 証人: 見つからない確率。層の確率から `miss_compose` の式で計算した値。 -/
def missProb : Method → Prob := fun M => match M with
  | .current => ⟨53 / 125, by grind, by grind⟩
  | .tuned => ⟨53 / 125, by grind, by grind⟩
  | .fullText => ⟨1127 / 3125, by grind, by grind⟩

/-- 証人: 1人1日の探し物の回数。どの方式も 4 回。 -/
def searchesPerDay : Method → Rat := fun _ => 4

/-- 証人: 見つかった探し物1回の時間。どの方式も 2.88 分（いまの検索の1日の時間が 20 分になるように決めた）。 -/
def foundMinutes : Method → Rat := fun _ => 72 / 25

/-- 証人: 層1で見つからなかった探し物1回の余分な時間。どの方式も 5 分。 -/
def extraNotYetMinutes : Method → Rat := fun _ => 5

/-- 証人: 層2・層3で見つからなかった探し物1回の余分な時間。どの方式も 5 分。 -/
def extraOtherMinutes : Method → Rat := fun _ => 5

/-- 証人: 1人1日の探し物の時間。`search_decomp` の式で計算する（いまの検索と安い設定の変更は 20 分、置き換えた後は 18.7328 分）。 -/
def searchMinutes : Method → Rat := fun M =>
  searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M
    + ((missProb M).val - (pNotYet M).val) * extraOtherMinutes M)

/-- 証人: 効果を受ける社員の数。412 人。 -/
def beneficiaries : Rat := 412

/-- 証人: 初年度に置き換えた検索を使える勤務日数。200 日。 -/
def workDays : Rat := 200

/-- 証人: 1時間あたりの人件費。3,000 円。 -/
def wagePerHour : Rat := 3000

/-- 証人: 見積もりの額。3,000,000 円。 -/
def estimateYen : Rat := 3000000

/-- 証人: 実際に追加で要る初年度の費用。2,800,000 円（見積もりより少ない）。 -/
def firstYearCost : Rat := 2800000

/-- 証人: 「多い」の境目。15 分。 -/
def manyMinutes : Rat := 15

/-- 証人: 会社が得る値打ち。6,000,000 円（安い設定の変更に比べて取り戻せる時間の人件費 5,220,864 円より多い）。 -/
def gainYen : Rat := 6000000

/-- 証人: 承認する理由がそろうのは、初年度の費用が会社の得る値打ちより小さいとき（前提が崩れれば、結論も崩れる世界）。 -/
def Approvable : Prop := firstYearCost < gainYen

/-! ## §3 計算の def（手順だけ。判断を入れない） -/

/-- 方式 M で、索引に入っている記事を探して、層2か層3で失敗する確率: 1 −（1 − 層2の確率）×（1 − 層3の確率）。 -/
def missAfterIndex (M : Method) : Rat :=
  1 - (1 - (pNoHit M).val) * (1 - (pOverlook M).val)

/-- 読み (a) の「失われている時間」（分）: いまの検索の、1日の探し物の回数 ×（層1で見つからない確率 × 層1の余分な時間 ＋
（見つからない確率 − 層1で見つからない確率）× 層2・層3の余分な時間）。
いまの検索で、見つからなかった探し物のために1人1日に余分に検索で使っている時間。 -/
def lostMinutes : Rat :=
  searchesPerDay .current * ((pNotYet .current).val * extraNotYetMinutes .current
    + ((missProb .current).val - (pNotYet .current).val) * extraOtherMinutes .current)

/-- 読み (b) の「取り戻せる時間」（分）: 1人1日の探し物の時間の、いまの検索と置き換えた後の差。 -/
def savedMinutes : Rat :=
  searchMinutes .current - searchMinutes .fullText

/-- 置き換えで、安い設定の変更をした場合に比べて、1人1日に取り戻せる時間（分）: 1人1日の探し物の時間の、安い設定の変更と置き換えた後の差。 -/
def savedOverTunedMinutes : Rat :=
  searchMinutes .tuned - searchMinutes .fullText

/-- 1人1日1分の時間が、初年度（`workDays` の日数）でいくらの人件費になるか: 人数 × 勤務日数 × 1時間あたりの人件費 ÷ 60。 -/
def yenPerDailyMinute : Rat :=
  beneficiaries * workDays * wagePerHour / 60

/-- 読み (a) の時間の、初年度の人件費（円）。 -/
def lostWageYen : Rat :=
  yenPerDailyMinute * lostMinutes

/-- 読み (b) の時間の、初年度の人件費（円）。会社の得ではなく、人件費に直した量。 -/
def savedWageYen : Rat :=
  yenPerDailyMinute * savedMinutes

/-- 安い設定の変更に比べて取り戻せる時間の、初年度の人件費（円）。 -/
def savedOverTunedWageYen : Rat :=
  yenPerDailyMinute * savedOverTunedMinutes

/-! ## §4 関係公理 -/

/-! ### 【実験】 -/

/-- 証人: 4 ×（2.88 ＋ 0.1 × 5 ＋（0.424 − 0.1）× 5）= 20。 -/
theorem search_current_eq : searchMinutes .current = 20 := by
  show (4 : Rat) * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5) = 20
  grind

/-- 証人: 4.2 < 5。 -/
theorem testDelay_le_five : testDelaySec ≤ 5 := by
  show (21 / 5 : Rat) ≤ 5
  grind

/-- 証人: 定義どおり。 -/
theorem estimate_eq : estimateYen = 3000000 := rfl

/-! ### 【経験則】 -/

/-- 証人: 28800 < 86400。 -/
theorem delay_current_ge_workday : 28800 ≤ indexDelaySec .current := by
  show (28800 : Rat) ≤ 86400
  grind

/-- 証人: 412 ≤ 412（境目の値）。 -/
theorem beneficiaries_ge : 412 ≤ beneficiaries := by
  show (412 : Rat) ≤ 412
  grind

/-! ### 【自明】 -/

/-- 証人: `searchMinutes` をこの式で定義したので、定義どおり。 -/
theorem search_decomp : ∀ M : Method,
  searchMinutes M = searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M
    + ((missProb M).val - (pNotYet M).val) * extraOtherMinutes M) :=
  fun _ => rfl

/-- 証人: 20・20・18.7328 は 0 以上。 -/
theorem searchMinutes_nonneg : ∀ M : Method, 0 ≤ searchMinutes M := by
  intro M
  cases M
  · show (0 : Rat) ≤ 4 * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5)
    grind
  · show (0 : Rat) ≤ 4 * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5)
    grind
  · show (0 : Rat) ≤ 4 * (72 / 25 + 1 / 1000 * 5 + (1127 / 3125 - 1 / 1000) * 5)
    grind

/-- 証人: 2.88 は 0 以上。 -/
theorem foundMinutes_nonneg : ∀ M : Method, 0 ≤ foundMinutes M := by
  intro _
  show (0 : Rat) ≤ 72 / 25
  grind

/-- 証人: 4 は 0 以上。 -/
theorem searchesPerDay_nonneg : ∀ M : Method, 0 ≤ searchesPerDay M := by
  intro _
  show (0 : Rat) ≤ 4
  grind

/-- 証人: 1 − 9/10 × 4/5 × 4/5 = 53/125、1 − 999/1000 × 4/5 × 4/5 = 1127/3125。 -/
theorem miss_compose : ∀ M : Method,
  (missProb M).val = 1 - (1 - (pNotYet M).val) * (1 - (pNoHit M).val) * (1 - (pOverlook M).val) := by
  intro M
  cases M
  · show (53 / 125 : Rat) = 1 - (1 - 1 / 10) * (1 - 1 / 5) * (1 - 1 / 5)
    grind
  · show (53 / 125 : Rat) = 1 - (1 - 1 / 10) * (1 - 1 / 5) * (1 - 1 / 5)
    grind
  · show (1127 / 3125 : Rat) = 1 - (1 - 1 / 1000) * (1 - 1 / 5) * (1 - 1 / 5)
    grind

/-! ### 【仮定】層1: まだ検索に出ない -/

/-- 証人: 4 < 4.2。 -/
theorem prodDelay_le_test : indexDelaySec .fullText ≤ testDelaySec := by
  show (4 : Rat) ≤ 21 / 5
  grind

/-- 証人: いまの検索（86400 秒）と安い設定の変更（43200 秒）で前提が成り立ち、結論 1/10 ≤ 1/10 が成り立つ。
置き換えた後は前提が成り立たない（4 秒）。 -/
theorem notYet_ge_of_slow : ∀ M : Method, 28800 ≤ indexDelaySec M → 1 / 10 ≤ (pNotYet M).val := by
  intro M h
  cases M
  · show (1 / 10 : Rat) ≤ 1 / 10
    grind
  · show (1 / 10 : Rat) ≤ 1 / 10
    grind
  · have h' : (28800 : Rat) ≤ 4 := h
    grind

/-- 証人: 置き換えた後で前提が2つとも成り立ち（4 秒、欠けた記事なし）、結論 1/1000 ≤ 1/1000 が成り立つ。
いまの検索と安い設定の変更では、遅れの前提が成り立たない（86400 秒、43200 秒）。 -/
theorem notYet_le_of_fast : ∀ M : Method, indexDelaySec M ≤ 5 → IndexComplete M → (pNotYet M).val ≤ 1 / 1000 := by
  intro M h _
  cases M
  · have h' : (86400 : Rat) ≤ 5 := h
    grind
  · have h' : (43200 : Rat) ≤ 5 := h
    grind
  · show (1 / 1000 : Rat) ≤ 1 / 1000
    grind

/-- 証人: `IndexComplete` はどの方式でも真。 -/
theorem fullText_complete : IndexComplete .fullText := trivial

/-! ### 【仮定】安い設定の変更の速さ -/

/-- 証人: `CurrentIncremental` は偽。 -/
theorem current_not_incremental : ¬ CurrentIncremental := fun h => h

/-- 証人: 前提（`CurrentIncremental` は偽）が成り立ち、結論 28800 < 43200 が成り立つ。 -/
theorem tuned_slow_of_rebuild : ¬ CurrentIncremental → 28800 ≤ indexDelaySec .tuned := by
  intro _
  show (28800 : Rat) ≤ 43200
  grind

/-! ### 【仮定】層2・層3: いまの検索の値 -/

/-- 証人: 1/5 ≤ 1/5（境目の値）。 -/
theorem noHit_current_le : (pNoHit .current).val ≤ 1 / 5 := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-- 証人: 1/5 ≤ 1/5（境目の値）。 -/
theorem overlook_current_le : (pOverlook .current).val ≤ 1 / 5 := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-! ### 【仮定】層2・層3: 置き換えで悪くならない（主張の側が使う片側） -/

/-- 証人: どの方式も同じ値（`noHit_full_ge` と合わせると、どの証人でも等しくなる）。 -/
theorem noHit_full_le : (pNoHit .fullText).val ≤ (pNoHit .current).val := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-- 証人: どの方式も同じ値（`overlook_full_ge` と合わせると、どの証人でも等しくなる）。 -/
theorem overlook_full_le : (pOverlook .fullText).val ≤ (pOverlook .current).val := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-! ### 【仮定】層2・層3: 置き換えでよくならない（不利な結論の側だけが使う片側） -/

/-- 証人: どの方式も同じ値。 -/
theorem noHit_full_ge : (pNoHit .current).val ≤ (pNoHit .fullText).val := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-- 証人: どの方式も同じ値。 -/
theorem overlook_full_ge : (pOverlook .current).val ≤ (pOverlook .fullText).val := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-! ### 【仮定】時間: いまの検索の値 -/

/-- 証人: 4 ≤ 4（境目の値）。 -/
theorem searches_current_ge : 4 ≤ searchesPerDay .current := by
  show (4 : Rat) ≤ 4
  grind

/-- 証人: 5 ≤ 5（境目の値）。 -/
theorem extraNotYet_current_ge : 5 ≤ extraNotYetMinutes .current := by
  show (5 : Rat) ≤ 5
  grind

/-- 証人: 0 < 5。 -/
theorem extraNotYet_nonneg : 0 ≤ extraNotYetMinutes .current := by
  show (0 : Rat) ≤ 5
  grind

/-- 証人: 0 < 5。 -/
theorem extraOther_nonneg : 0 ≤ extraOtherMinutes .current := by
  show (0 : Rat) ≤ 5
  grind

/-- 証人: 5 ≤ 5（境目の値）。 -/
theorem extraOther_le_notYet : extraOtherMinutes .current ≤ extraNotYetMinutes .current := by
  show (5 : Rat) ≤ 5
  grind

/-! ### 【仮定】時間: 置き換えで悪くならない（主張の側が使う片側） -/

/-- 証人: どの方式も同じ値。 -/
theorem searches_full_le : searchesPerDay .fullText ≤ searchesPerDay .current := by
  show (4 : Rat) ≤ 4
  grind

/-- 証人: どの方式も同じ値。 -/
theorem found_full_le : foundMinutes .fullText ≤ foundMinutes .current := by
  show (72 / 25 : Rat) ≤ 72 / 25
  grind

/-- 証人: どの方式も同じ値。 -/
theorem extraNotYet_full_le : extraNotYetMinutes .fullText ≤ extraNotYetMinutes .current := by
  show (5 : Rat) ≤ 5
  grind

/-- 証人: どの方式も同じ値。 -/
theorem extraOther_full_le : extraOtherMinutes .fullText ≤ extraOtherMinutes .current := by
  show (5 : Rat) ≤ 5
  grind

/-! ### 【仮定】時間: 置き換えでよくならない（不利な結論の側だけが使う片側） -/

/-- 証人: どの方式も同じ値。 -/
theorem searches_full_ge : searchesPerDay .current ≤ searchesPerDay .fullText := by
  show (4 : Rat) ≤ 4
  grind

/-- 証人: どの方式も同じ値。 -/
theorem found_full_ge : foundMinutes .current ≤ foundMinutes .fullText := by
  show (72 / 25 : Rat) ≤ 72 / 25
  grind

/-- 証人: どの方式も同じ値。 -/
theorem extraNotYet_full_ge : extraNotYetMinutes .current ≤ extraNotYetMinutes .fullText := by
  show (5 : Rat) ≤ 5
  grind

/-- 証人: どの方式も同じ値。 -/
theorem extraOther_full_ge : extraOtherMinutes .current ≤ extraOtherMinutes .fullText := by
  show (5 : Rat) ≤ 5
  grind

/-! ### 【仮定】安い設定の変更は、層1のほかの点でよくならない（C0 の側だけが使う片側） -/

/-- 証人: どの方式も同じ値。 -/
theorem searches_tuned_ge : searchesPerDay .current ≤ searchesPerDay .tuned := by
  show (4 : Rat) ≤ 4
  grind

/-- 証人: どの方式も同じ値。 -/
theorem found_tuned_ge : foundMinutes .current ≤ foundMinutes .tuned := by
  show (72 / 25 : Rat) ≤ 72 / 25
  grind

/-- 証人: どの方式も同じ値。 -/
theorem extraNotYet_tuned_ge : extraNotYetMinutes .current ≤ extraNotYetMinutes .tuned := by
  show (5 : Rat) ≤ 5
  grind

/-- 証人: どの方式も同じ値。 -/
theorem extraOther_tuned_ge : extraOtherMinutes .current ≤ extraOtherMinutes .tuned := by
  show (5 : Rat) ≤ 5
  grind

/-- 証人: どの方式も同じ値。 -/
theorem noHit_tuned_ge : (pNoHit .current).val ≤ (pNoHit .tuned).val := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-- 証人: どの方式も同じ値。 -/
theorem overlook_tuned_ge : (pOverlook .current).val ≤ (pOverlook .tuned).val := by
  show (1 / 5 : Rat) ≤ 1 / 5
  grind

/-! ### 【仮定】金額に直す -/

/-- 証人: 2,800,000 < 3,000,000。 -/
theorem cost_le_estimate : firstYearCost ≤ estimateYen := by
  show (2800000 : Rat) ≤ 3000000
  grind

/-- 証人: 200 ≤ 200（境目の値）。 -/
theorem workDays_ge : 200 ≤ workDays := by
  show (200 : Rat) ≤ 200
  grind

/-- 証人: 3000 ≤ 3000（境目の値）。 -/
theorem wage_ge : 3000 ≤ wagePerHour := by
  show (3000 : Rat) ≤ 3000
  grind

/-- 証人: 安い設定の変更に比べて取り戻せる時間の人件費は 4,120,000 × 1.2672 = 5,220,864 円で、6,000,000 円より少ない。 -/
theorem gain_ge_wage : savedOverTunedWageYen ≤ gainYen := by
  show (412 * 200 * 3000 / 60 : Rat)
      * (4 * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5)
        - 4 * (72 / 25 + 1 / 1000 * 5 + (1127 / 3125 - 1 / 1000) * 5)) ≤ 6000000
  grind

/-! ### 【仮定】読者の判断 -/

/-- 証人: 15 < 20。 -/
theorem many_threshold_le : manyMinutes ≤ 20 := by
  show (15 : Rat) ≤ 20
  grind

/-- 証人: `Approvable` を「初年度の費用 < 会社が得る値打ち」と定義したので、前提がそのまま結論になる。前提は成り立つ（2,800,000 円 < 6,000,000 円）。 -/
theorem approvable_of_net : firstYearCost < gainYen → Approvable :=
  fun h => h

/-! ## §5 主張の定理 -/

/-! ### 数と式の補題 -/

/-- 0 以上の数どうしの不等式は、掛け合わせても成り立つ（a ≤ b、c ≤ d ならば a × c ≤ b × d）。 -/
theorem rat_mul_le_mul {a b c d : Rat} (ha : 0 ≤ a) (hab : a ≤ b) (hc : 0 ≤ c) (hcd : c ≤ d) :
    a * c ≤ b * d := by
  have h1 : a * c ≤ b * c := Rat.mul_le_mul_of_nonneg_right hab hc
  have h2 : b * c ≤ b * d := Rat.mul_le_mul_of_nonneg_left hcd (by grind)
  grind

/-- どの方式でも、層2か層3で失敗する確率は 0 以上（層2・層3の確率の範囲だけから出る）。 -/
theorem missAfterIndex_nonneg : ∀ M : Method, 0 ≤ missAfterIndex M := by
  intro M
  unfold missAfterIndex
  have hb0 := (pNoHit M).nonneg
  have hb1 := (pNoHit M).le_one
  have hc0 := (pOverlook M).nonneg
  have hc1 := (pOverlook M).le_one
  have hx : (1 - (pNoHit M).val) * (1 - (pOverlook M).val) ≤ 1 * 1 :=
    rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
  grind

/-- どの方式でも、見つからない確率 − 層1の確率 =（1 − 層1の確率）× 層2か層3で失敗する確率（`miss_compose` の式の変形）。 -/
theorem miss_sub_notYet : ∀ M : Method,
    (missProb M).val - (pNotYet M).val = (1 - (pNotYet M).val) * missAfterIndex M := by
  intro M
  unfold missAfterIndex
  rw [miss_compose M]
  grind

/-- どの方式でも、1日の探し物の時間 = 回数 ×（見つかった場合の時間 ＋ 層1の確率 × 層1の余分な時間 ＋
（1 − 層1の確率）× 層2か層3で失敗する確率 × 層2・層3の余分な時間）（`search_decomp` と `miss_compose` の式の変形）。 -/
theorem search_layers : ∀ M : Method,
    searchMinutes M = searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M
      + (1 - (pNotYet M).val) * missAfterIndex M * extraOtherMinutes M) := by
  intro M
  rw [search_decomp M, miss_sub_notYet M]

/-! ### 途中の定理 -/

/-- いまの検索で、まだ検索に出ていない記事を探す確率は 1/10 以上。 -/
theorem notYet_current_ge : 1 / 10 ≤ (pNotYet .current).val :=
  notYet_ge_of_slow .current delay_current_ge_workday

/-- 安い設定の変更をしても、まだ検索に出ていない記事を探す確率は 1/10 以上。 -/
theorem notYet_tuned_ge : 1 / 10 ≤ (pNotYet .tuned).val :=
  notYet_ge_of_slow .tuned (tuned_slow_of_rebuild current_not_incremental)

/-- 置き換えた後、まだ検索に出ていない記事を探す確率は 1/1000 以下。 -/
theorem notYet_fullText_le : (pNotYet .fullText).val ≤ 1 / 1000 := by
  have h1 := prodDelay_le_test
  have h2 := testDelay_le_five
  exact notYet_le_of_fast .fullText (by grind) fullText_complete

/-- いまの検索の「失われている時間」（読み a）は、1人1日2分以上（4回 × 1/10 × 5分。層2・層3の分は0以上なので落とす）。 -/
theorem lost_ge : 2 ≤ lostMinutes := by
  unfold lostMinutes
  have hs := searches_current_ge
  have ha := notYet_current_ge
  have he := extraNotYet_current_ge
  have ho := extraOther_nonneg
  have hL := miss_sub_notYet .current
  have hA := missAfterIndex_nonneg .current
  have ha1 := (pNotYet .current).le_one
  have hm : 0 ≤ (missProb .current).val - (pNotYet .current).val := by
    rw [hL]
    exact Rat.mul_nonneg (by grind) hA
  have h1 : (1 / 10) * 5 ≤ (pNotYet .current).val * extraNotYetMinutes .current :=
    rat_mul_le_mul (by grind) ha (by grind) he
  have h2 : 0 ≤ ((missProb .current).val - (pNotYet .current).val) * extraOtherMinutes .current :=
    Rat.mul_nonneg hm ho
  have h3 : 4 * ((1 / 10) * 5) ≤ searchesPerDay .current * ((pNotYet .current).val * extraNotYetMinutes .current
      + ((missProb .current).val - (pNotYet .current).val) * extraOtherMinutes .current) :=
    rat_mul_le_mul (by grind) hs (by grind) (by grind)
  grind

/-- 取り戻せる時間（読み b）は、回数(いま) ×（層1の確率の差）×（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）以上。
置き換えた後の量を、主張の側の片側の公理で、いまの検索の値に置き換えた上界から出す。 -/
theorem saved_ge_gap :
    searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val)
      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current)
      ≤ savedMinutes := by
  unfold savedMinutes
  rw [search_layers .current, search_layers .fullText]
  have hsf := searchesPerDay_nonneg .fullText
  have hfc := foundMinutes_nonneg .current
  have he1 := extraNotYet_current_ge
  have he2 := extraOther_nonneg
  have hs := searches_full_le
  have hf := found_full_le
  have hx1 := extraNotYet_full_le
  have hx2 := extraOther_full_le
  have hb := noHit_full_le
  have hc := overlook_full_le
  have hAf := missAfterIndex_nonneg .fullText
  have hAc := missAfterIndex_nonneg .current
  have hp0 := (pNotYet .fullText).nonneg
  have hp1 := (pNotYet .fullText).le_one
  have hA : missAfterIndex .fullText ≤ missAfterIndex .current := by
    unfold missAfterIndex
    have hb1 := (pNoHit .current).le_one
    have hc1 := (pOverlook .current).le_one
    have hx : (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val)
        ≤ (1 - (pNoHit .fullText).val) * (1 - (pOverlook .fullText).val) :=
      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
    grind
  have h1 : (pNotYet .fullText).val * extraNotYetMinutes .fullText
      ≤ (pNotYet .fullText).val * extraNotYetMinutes .current :=
    Rat.mul_le_mul_of_nonneg_left hx1 hp0
  have h2a : missAfterIndex .fullText * extraOtherMinutes .fullText
      ≤ missAfterIndex .fullText * extraOtherMinutes .current :=
    Rat.mul_le_mul_of_nonneg_left hx2 hAf
  have h2b : missAfterIndex .fullText * extraOtherMinutes .current
      ≤ missAfterIndex .current * extraOtherMinutes .current :=
    Rat.mul_le_mul_of_nonneg_right hA he2
  have h3 : (1 - (pNotYet .fullText).val) * (missAfterIndex .fullText * extraOtherMinutes .fullText)
      ≤ (1 - (pNotYet .fullText).val) * (missAfterIndex .current * extraOtherMinutes .current) :=
    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
  have hG : foundMinutes .fullText + (pNotYet .fullText).val * extraNotYetMinutes .fullText
        + (1 - (pNotYet .fullText).val) * missAfterIndex .fullText * extraOtherMinutes .fullText
      ≤ foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current := by
    grind
  have hG0a : 0 ≤ (pNotYet .fullText).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 (by grind)
  have hG0b : 0 ≤ (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current :=
    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current := by
    grind
  have h4 := Rat.mul_le_mul_of_nonneg_left hG hsf
  have h5 := Rat.mul_le_mul_of_nonneg_right hs hG0
  grind

/-- 取り戻せる時間（読み b）は、1人1日 792/625 分（1.2672分）以上（4回 ×（1/10 − 1/1000）×（16/25 × 5分））。 -/
theorem saved_ge : 792 / 625 ≤ savedMinutes := by
  have hg := saved_ge_gap
  have hs := searches_current_ge
  have he1 := extraNotYet_current_ge
  have hle := extraOther_le_notYet
  have he2 := extraOther_nonneg
  have hb := noHit_current_le
  have hc := overlook_current_le
  have ha := notYet_current_ge
  have hf := notYet_fullText_le
  have hAc := missAfterIndex_nonneg .current
  have h1A : 16 / 25 ≤ 1 - missAfterIndex .current := by
    unfold missAfterIndex
    have hx : (4 / 5) * (4 / 5) ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
    grind
  have hAe : missAfterIndex .current * extraOtherMinutes .current
      ≤ missAfterIndex .current * extraNotYetMinutes .current :=
    Rat.mul_le_mul_of_nonneg_left hle hAc
  have hq : (16 / 25) * 5 ≤ (1 - missAfterIndex .current) * extraNotYetMinutes .current :=
    rat_mul_le_mul (by grind) h1A (by grind) he1
  have hK : (16 / 25) * 5 ≤ extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current := by
    grind
  have hP : 1 / 10 - 1 / 1000 ≤ (pNotYet .current).val - (pNotYet .fullText).val := by grind
  have h1 : 4 * (1 / 10 - 1 / 1000) ≤ searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val) :=
    rat_mul_le_mul (by grind) hs (by grind) hP
  have h2 : 4 * (1 / 10 - 1 / 1000) * ((16 / 25) * 5)
      ≤ searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val)
        * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) :=
    rat_mul_le_mul (by grind) h1 (by grind) hK
  grind

/-- 安い設定の変更に比べて取り戻せる時間は、回数(いま) ×（層1の確率の差。安い設定の変更と置き換えた後）×
（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）以上。
安い設定の変更の量を、C0 の側の片側の公理で、いまの検索の値に置き換えた下界を、`saved_ge_gap` に足して出す。 -/
theorem savedOverTuned_ge_gap :
    searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val)
      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current)
      ≤ savedOverTunedMinutes := by
  have hg := saved_ge_gap
  unfold savedMinutes at hg
  unfold savedOverTunedMinutes
  have hSc := search_layers .current
  have hSt := search_layers .tuned
  have hsc := searchesPerDay_nonneg .current
  have hfc := foundMinutes_nonneg .current
  have he1 := extraNotYet_current_ge
  have he2 := extraOther_nonneg
  have hs := searches_tuned_ge
  have hf := found_tuned_ge
  have hx1 := extraNotYet_tuned_ge
  have hx2 := extraOther_tuned_ge
  have hb := noHit_tuned_ge
  have hc := overlook_tuned_ge
  have hAt := missAfterIndex_nonneg .tuned
  have hAc := missAfterIndex_nonneg .current
  have hp0 := (pNotYet .tuned).nonneg
  have hp1 := (pNotYet .tuned).le_one
  have hA : missAfterIndex .current ≤ missAfterIndex .tuned := by
    unfold missAfterIndex
    have hb1 := (pNoHit .tuned).le_one
    have hc1 := (pOverlook .tuned).le_one
    have hx : (1 - (pNoHit .tuned).val) * (1 - (pOverlook .tuned).val)
        ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
    grind
  have h1 : (pNotYet .tuned).val * extraNotYetMinutes .current
      ≤ (pNotYet .tuned).val * extraNotYetMinutes .tuned :=
    Rat.mul_le_mul_of_nonneg_left hx1 hp0
  have h2a : missAfterIndex .current * extraOtherMinutes .current
      ≤ missAfterIndex .tuned * extraOtherMinutes .current :=
    Rat.mul_le_mul_of_nonneg_right hA he2
  have h2b : missAfterIndex .tuned * extraOtherMinutes .current
      ≤ missAfterIndex .tuned * extraOtherMinutes .tuned :=
    Rat.mul_le_mul_of_nonneg_left hx2 hAt
  have h3 : (1 - (pNotYet .tuned).val) * (missAfterIndex .current * extraOtherMinutes .current)
      ≤ (1 - (pNotYet .tuned).val) * (missAfterIndex .tuned * extraOtherMinutes .tuned) :=
    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
  have hG : foundMinutes .current + (pNotYet .tuned).val * extraNotYetMinutes .current
        + (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current
      ≤ foundMinutes .tuned + (pNotYet .tuned).val * extraNotYetMinutes .tuned
        + (1 - (pNotYet .tuned).val) * missAfterIndex .tuned * extraOtherMinutes .tuned := by
    grind
  have hG0a : 0 ≤ (pNotYet .tuned).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 (by grind)
  have hG0b : 0 ≤ (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current :=
    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .tuned).val * extraNotYetMinutes .current
        + (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current := by
    grind
  have h4 := Rat.mul_le_mul_of_nonneg_right hs hG0
  have h5 := Rat.mul_le_mul_of_nonneg_left hG (by grind : 0 ≤ searchesPerDay .tuned)
  grind

/-- 安い設定の変更に比べて取り戻せる時間は、1人1日 792/625 分（1.2672分）以上（4回 ×（1/10 − 1/1000）×（16/25 × 5分））。 -/
theorem savedOverTuned_ge : 792 / 625 ≤ savedOverTunedMinutes := by
  have hg := savedOverTuned_ge_gap
  have hs := searches_current_ge
  have he1 := extraNotYet_current_ge
  have hle := extraOther_le_notYet
  have he2 := extraOther_nonneg
  have hb := noHit_current_le
  have hc := overlook_current_le
  have ha := notYet_tuned_ge
  have hf := notYet_fullText_le
  have hAc := missAfterIndex_nonneg .current
  have h1A : 16 / 25 ≤ 1 - missAfterIndex .current := by
    unfold missAfterIndex
    have hx : (4 / 5) * (4 / 5) ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
    grind
  have hAe : missAfterIndex .current * extraOtherMinutes .current
      ≤ missAfterIndex .current * extraNotYetMinutes .current :=
    Rat.mul_le_mul_of_nonneg_left hle hAc
  have hq : (16 / 25) * 5 ≤ (1 - missAfterIndex .current) * extraNotYetMinutes .current :=
    rat_mul_le_mul (by grind) h1A (by grind) he1
  have hK : (16 / 25) * 5 ≤ extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current := by
    grind
  have hP : 1 / 10 - 1 / 1000 ≤ (pNotYet .tuned).val - (pNotYet .fullText).val := by grind
  have h1 : 4 * (1 / 10 - 1 / 1000) ≤ searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val) :=
    rat_mul_le_mul (by grind) hs (by grind) hP
  have h2 : 4 * (1 / 10 - 1 / 1000) * ((16 / 25) * 5)
      ≤ searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val)
        * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) :=
    rat_mul_le_mul (by grind) h1 (by grind) hK
  grind

/-- 1人1日1分の時間は、初年度に 4,120,000円以上の人件費になる（412人 × 200日 × 3,000円 ÷ 60）。 -/
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

/-- @claim C3 [確率] 読み (b): 初年度の費用は、置き換えで（いまのままと比べて）取り戻せる時間の初年度の人件費より小さい。 -/
theorem claim_C3_saved : firstYearCost < savedWageYen := by
  unfold savedWageYen
  have hy := yenPerDailyMinute_ge
  have hs := saved_ge
  have hc := cost_le_estimate
  have he := estimate_eq
  have h : 4120000 * (792 / 625) ≤ yenPerDailyMinute * savedMinutes :=
    rat_mul_le_mul (by grind) hy (by grind) hs
  grind

/-- @claim C3 [確率] 読み (a): 初年度の費用は、いまの検索で失われている時間の初年度の人件費より小さい。 -/
theorem claim_C3_lost : firstYearCost < lostWageYen := by
  unfold lostWageYen
  have hy := yenPerDailyMinute_ge
  have hl := lost_ge
  have hc := cost_le_estimate
  have he := estimate_eq
  have h : 4120000 * 2 ≤ yenPerDailyMinute * lostMinutes :=
    rat_mul_le_mul (by grind) hy (by grind) hl
  grind

/-- @claim C0 [確率] 来期予算で300万円を承認する理由がそろう。
初年度の費用 ≤ 300万円 < 5,220,864円 ≤ 安い設定の変更に比べて取り戻せる時間の人件費 ≤ 会社が得る値打ち、から示す。 -/
theorem claim_C0_approvable : Approvable := by
  apply approvable_of_net
  have hy := yenPerDailyMinute_ge
  have hs := savedOverTuned_ge
  have hg := gain_ge_wage
  have hc := cost_le_estimate
  have he := estimate_eq
  unfold savedOverTunedWageYen at hg
  have h : 4120000 * (792 / 625) ≤ yenPerDailyMinute * savedOverTunedMinutes :=
    rat_mul_le_mul (by grind) hy (by grind) hs
  grind

/-- @claim C1 [決定論] いまの検索で1人1日に探し物に使う時間は、「多い」の境目以上。
@restates many_threshold_le 理由: 「1日20分は多い」は読者の判断で、事実から導けない。その判断だけを【仮定】に切り出し、確信度 0.05 のまま主張の値に出しているので、隠してはいない。ステージ5で C1 を数字の文（1日平均20分）に言い換えるまで、このままにする -/
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

/-- @baseline いまの検索の「失われている時間」（読み a）を、アンケートの1日20分より大きく置いていない。
失われている時間 = 20 − 回数 × 見つかった場合の時間。 -/
theorem baseline_lost_le_survey : lostMinutes ≤ 20 := by
  unfold lostMinutes
  have hd := search_decomp .current
  have he := search_current_eq
  have hs := searchesPerDay_nonneg .current
  have hf := foundMinutes_nonneg .current
  have h0 : 0 ≤ searchesPerDay .current * foundMinutes .current := Rat.mul_nonneg hs hf
  grind

/-- [不利] 置き換えで取り戻せる時間は、1人1日20分を超えない。 -/
theorem unfav_saved_le_survey : savedMinutes ≤ 20 := by
  unfold savedMinutes
  have he := search_current_eq
  have hn := searchMinutes_nonneg .fullText
  grind

/-- [不利] 置き換えで取り戻せる時間（読み b）は、回数(いま) ×（層1の確率の差）×（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）を超えない。
層1の差が縮めば、効果もそれだけ縮む。置き換えた後の量を、不利な結論の側の片側の公理で、いまの検索の値に置き換えた下界から出す。
主張の側の片側の公理（`_full_le`）も、量の仮定（4回、5分、10%）も通らない。 -/
theorem unfav_saved_le_gap :
    savedMinutes ≤ searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val)
      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) := by
  unfold savedMinutes
  rw [search_layers .current, search_layers .fullText]
  have hsf := searchesPerDay_nonneg .fullText
  have hfc := foundMinutes_nonneg .current
  have he1 := extraNotYet_nonneg
  have he2 := extraOther_nonneg
  have hs := searches_full_ge
  have hf := found_full_ge
  have hx1 := extraNotYet_full_ge
  have hx2 := extraOther_full_ge
  have hb := noHit_full_ge
  have hc := overlook_full_ge
  have hAf := missAfterIndex_nonneg .fullText
  have hAc := missAfterIndex_nonneg .current
  have hp0 := (pNotYet .fullText).nonneg
  have hp1 := (pNotYet .fullText).le_one
  have hA : missAfterIndex .current ≤ missAfterIndex .fullText := by
    unfold missAfterIndex
    have hb1 := (pNoHit .fullText).le_one
    have hc1 := (pOverlook .fullText).le_one
    have hx : (1 - (pNoHit .fullText).val) * (1 - (pOverlook .fullText).val)
        ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
    grind
  have h1 : (pNotYet .fullText).val * extraNotYetMinutes .current
      ≤ (pNotYet .fullText).val * extraNotYetMinutes .fullText :=
    Rat.mul_le_mul_of_nonneg_left hx1 hp0
  have h2a : missAfterIndex .current * extraOtherMinutes .current
      ≤ missAfterIndex .fullText * extraOtherMinutes .current :=
    Rat.mul_le_mul_of_nonneg_right hA he2
  have h2b : missAfterIndex .fullText * extraOtherMinutes .current
      ≤ missAfterIndex .fullText * extraOtherMinutes .fullText :=
    Rat.mul_le_mul_of_nonneg_left hx2 hAf
  have h3 : (1 - (pNotYet .fullText).val) * (missAfterIndex .current * extraOtherMinutes .current)
      ≤ (1 - (pNotYet .fullText).val) * (missAfterIndex .fullText * extraOtherMinutes .fullText) :=
    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
  have hG : foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current
      ≤ foundMinutes .fullText + (pNotYet .fullText).val * extraNotYetMinutes .fullText
        + (1 - (pNotYet .fullText).val) * missAfterIndex .fullText * extraOtherMinutes .fullText := by
    grind
  have hG0a : 0 ≤ (pNotYet .fullText).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 he1
  have hG0b : 0 ≤ (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current :=
    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current := by
    grind
  have h4 := Rat.mul_le_mul_of_nonneg_right hs hG0
  have h5 := Rat.mul_le_mul_of_nonneg_left hG hsf
  grind

/-- [不利] 置き換えで取り戻せる時間（読み b）は、いまの検索で失われている時間（読み a）を超えない。 -/
theorem unfav_saved_le_lost : savedMinutes ≤ lostMinutes := by
  unfold savedMinutes lostMinutes
  rw [search_decomp .current, search_decomp .fullText]
  have hsf := searchesPerDay_nonneg .fullText
  have hfc := foundMinutes_nonneg .current
  have he1 := extraNotYet_nonneg
  have he2 := extraOther_nonneg
  have hs := searches_full_ge
  have hf := found_full_ge
  have hx1 := extraNotYet_full_ge
  have hx2 := extraOther_full_ge
  have hL := miss_sub_notYet .fullText
  have hAf := missAfterIndex_nonneg .fullText
  have hp0 := (pNotYet .fullText).nonneg
  have hp1 := (pNotYet .fullText).le_one
  have hm : 0 ≤ (missProb .fullText).val - (pNotYet .fullText).val := by
    rw [hL]
    exact Rat.mul_nonneg (by grind) hAf
  have hq1 : 0 ≤ (pNotYet .fullText).val * extraNotYetMinutes .fullText := Rat.mul_nonneg hp0 (by grind)
  have hq2 : 0 ≤ ((missProb .fullText).val - (pNotYet .fullText).val) * extraOtherMinutes .fullText :=
    Rat.mul_nonneg hm (by grind)
  have hI : foundMinutes .current ≤ foundMinutes .fullText + (pNotYet .fullText).val * extraNotYetMinutes .fullText
      + ((missProb .fullText).val - (pNotYet .fullText).val) * extraOtherMinutes .fullText := by
    grind
  have h4 := Rat.mul_le_mul_of_nonneg_right hs hfc
  have h5 := Rat.mul_le_mul_of_nonneg_left hI hsf
  grind


/-! ### 関係公理の前提が、証人の世界で成り立つこと -/

-- `notYet_ge_of_slow` の前提は、いまの検索で成り立つ（86400 秒）。
example : 28800 ≤ indexDelaySec .current := by
  show (28800 : Rat) ≤ 86400
  grind

-- `notYet_ge_of_slow` の前提は、安い設定の変更でも成り立つ（43200 秒）。
example : 28800 ≤ indexDelaySec .tuned := by
  show (28800 : Rat) ≤ 43200
  grind

-- `notYet_le_of_fast` の1つ目の前提は、置き換えた後で成り立つ（4 秒）。
example : indexDelaySec .fullText ≤ 5 := by
  show (4 : Rat) ≤ 5
  grind

-- `notYet_le_of_fast` の2つ目の前提は、置き換えた後で成り立つ（欠けた記事がない）。
example : IndexComplete .fullText := trivial

-- `tuned_slow_of_rebuild` の前提は成り立つ（いまの仕組みは保存のたびに索引へ足せない）。
example : ¬ CurrentIncremental := fun h => h

-- `approvable_of_net` の前提は成り立つ（2,800,000 円 < 6,000,000 円）。
example : firstYearCost < gainYen := by
  show (2800000 : Rat) < 6000000
  grind

-- 取り戻せる時間は、主張の定理の下限（1.2672 分）ちょうどで、失われている時間（8.48 分）より短い。
example : savedMinutes = 792 / 625 := by
  show (4 : Rat) * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5)
      - 4 * (72 / 25 + 1 / 1000 * 5 + (1127 / 3125 - 1 / 1000) * 5) = 792 / 625
  grind

example : lostMinutes = 212 / 25 := by
  show (4 : Rat) * (1 / 10 * 5 + (53 / 125 - 1 / 10) * 5) = 212 / 25
  grind

end

end WikiSearch
