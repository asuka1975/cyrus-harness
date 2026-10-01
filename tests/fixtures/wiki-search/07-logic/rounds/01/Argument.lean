/-!
# 論証のモデル: 社内Wiki検索の刷新提案

設計書: `07-logic/model-plan.md`。主張: `05-claims.json`。事実: `06-facts.json`。

## 書き方の約束（ガイド `stages/07-logic.md` の「Writer の約束」の要約）

- `def` は計算の手順だけに使う。現実についての判断は、宣言（中身を決めない `axiom`）と関係公理（型が命題の `axiom`）に分ける。
- 判断を、定理の引数、宣言の型、比較相手の定義、計算の def の docstring に置かない。
- 両方式の式に現れる量は、方式を引数に取る。「同じとみなす」なら【仮定】の関係公理にし、理由と向きを書く。
- 論証に必要な関係は、確信度が低くても省かない。要ファクトを付ける。
- 関係公理の型の最上位と ∀ の直下に ∧ を置かない（原子命題ごとに公理を分ける）。
- 関係公理の docstring の先頭に種類を書く: 【自明】（論拠）、【実験】（@support）、【経験則】（@support・@confidence・論拠・弱い点）、【仮定】（同上と「要ファクト:」）。
- 主張を示す定理に `@claim C…` を付ける。主張より強い定理は `@beyond C…`、比べる相手を確かめる定理は `@baseline`。
- 不利な結論も定理として導く。有利な向きの仮定を経由しない経路を選ぶ。
- 検査の警告を消すために、ラベルを変えたり、公理を省いたりしない。
- `@reviewer`・`@against`・`@restates` は Reviewer だけが付ける。

## 主張と定理の対応

種類: [決定論] Prop の世界、[確率] 確率・期待値の比較、[件数] 件数の比較、[不利] 書き手の結論に不利な定理。

| 主張 | 主張の文 | 定理 | 種類 |
|---|---|---|---|
| C0 | 社内Wikiの検索を全文検索エンジンに置き換えるため、来期予算で300万円を承認してほしい | `claim_C0_approvable` | [確率] |
| C1 | いまの検索では、社員が探し物に多くの時間を使っている | `claim_C1_many` | [決定論] |
| C2 | 置き換えれば、書いた記事がすぐ検索に出るようになる | `claim_C2_soon`（項1: 5秒以内）、`claim_C2_faster`（項2: いまより早い） | [決定論] |
| C3 | 費用は、失われている時間に比べて小さい | `claim_C3_lost`（読み a: 失われている時間）、`claim_C3_saved`（読み b: 取り戻せる時間） | [確率] |

印のない定理:

| 定理 | 示すこと | 種類 |
|---|---|---|
| `baseline_lost_le_survey` | いまの検索の「失われている時間」を、アンケートの1日20分より大きく置いていない（比べる相手の確認） | [決定論] |
| `unfav_saved_le_survey` | 取り戻せる時間は、1日20分を超えない | [不利] |
| `unfav_saved_le_lost` | 取り戻せる時間は、失われている時間を超えない | [不利] |
| `saved_only_from_notYet` | 取り戻せる時間は、層1（まだ検索に出ない）の確率の差からだけ生まれる | [確率]（[不利] の読みもある） |

`baseline_lost_le_survey` には `@baseline` の印を付けている。

## 設計書（model-plan.md）との違い

- 数の補題 `rat_mul_le_mul`（0 以上の数どうしの不等式を掛け合わせる）を §5 の先頭に足した。関係公理を使わない数学の補題で、
  標準ライブラリの `grind` が積の単調性を解けないために置いた。現実についての判断は含まない。
- 設計書の4節に載っている「同じとみなす」置き方の公理（`noHit_same`・`overlook_same`・`searches_same`・`foundMinutes_same`・
  `missExtra_same`・`notYet_ge_of_slow`・`notYet_le_of_fast`）の docstring に「向き:」の行を足し、4節の向きを写した。
- 設計書の3.1節は、`*_same` の5つの論拠と弱い点を「4節」に預けている。そこで、この5つの弱い点は、4節の向きの説明と
  6節の不利な結論の説明から書いた。`missExtra_same` だけは設計書に弱い点の材料がないので、
  「探し直しの時間は検索の仕組みで変わりうる（どちらの向きにも）」と、中立の向きに合わせて書いた。
- ほかは、宣言・計算の def・関係公理・定理の名前と型、定理が使う関係公理は、設計書の2節・3節・5節のとおり。
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

/-- 記事を保存してから、検索に出るまでにかかる時間（秒）。 -/
axiom indexDelaySec : Method → Rat

/-- 試験環境の全文検索エンジンで測った、保存から検索に出るまでの時間（秒）。
本番の `indexDelaySec .fullText` とは別の量。試験環境の全文検索エンジンだけの量なので、方式を取らない。 -/
axiom testDelaySec : Rat

/-- 層1。探し物1回で、探す記事が、検索の時点でまだ検索に出ていない確率。 -/
axiom pNotYet : Method → Prob

/-- 層2。検索に出る状態の記事が、入れた語で引けない確率。 -/
axiom pNoHit : Method → Prob

/-- 層3。引けた記事を、結果の中で見落とす確率。 -/
axiom pOverlook : Method → Prob

/-- 探し物1回が、検索で見つからない確率（3つの層のどれかで失敗する）。
層の確率との関係は、関係公理 `miss_compose` に置く。 -/
axiom missProb : Method → Prob

/-- 社員1人が1日に、検索で探し物をする回数。 -/
axiom searchesPerDay : Method → Rat

/-- 見つかった探し物1回にかかる時間（分）。 -/
axiom foundMinutes : Method → Rat

/-- 見つからなかった探し物1回で、見つかった場合より余分に探し物に使う時間（分）。
探し直しや、ほかの場所を探す時間を含む。 -/
axiom missExtraMinutes : Method → Rat

/-- 社員1人が1日に探し物に使う時間（分）。F1 の「1日平均20分」は、この量の `current` の値。
回数と時間への分け方は、関係公理 `search_decomp` に置く。 -/
axiom searchMinutes : Method → Rat

/-- 置き換えの効果を受ける社員の数。
会社の量で、検索の仕組みを変えても変わらないので、方式を取らない（金額に直すとき、2つの方式の差に1回だけ掛ける）。 -/
axiom beneficiaries : Rat

/-- 1年の勤務日数。会社の量なので、方式を取らない。 -/
axiom workDays : Rat

/-- 社員1人の1時間あたりの人件費（円。会社の負担分を含む）。会社の量なので、方式を取らない。 -/
axiom wagePerHour : Rat

/-- 置き換えの初年度に、追加で必要な費用（円）。置き換える側にだけ現れる量なので、方式を取らない。 -/
axiom firstYearCost : Rat

/-- 読者（部長）が「多い」と受け取る、1人1日あたりの探し物の時間の境目（分）。読者の判断の量なので、方式を取らない。 -/
axiom manyMinutes : Rat

/-- いまの検索の仕組みのまま、300万円より安い費用で、保存から検索に出るまでを5秒以内にできる。 -/
axiom CheaperFix : Prop

/-- 部長が、来期予算で300万円を承認する理由がそろっている。 -/
axiom Approvable : Prop

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

/-- 【実験】いまの検索では、社員1人が1日に探し物に使う時間は20分。
@support F1
@confidence 0.75
@reviewer 0.75 ← 0.95 理由: F1 が述べるのは「検索で探し物をするのに」使う時間。モデルの searchMinutes は、search_decomp と missExtraMinutes の宣言を通して、検索が失敗したあとに「ほかの場所を探す時間」も含む。F1 の20分がその時間を含むかは、設問5の文面（02-context/survey-2026.md。02-context に無い）で確かめられず、04-analysis.md は「探し物に1日平均20分」と書いて範囲が揺れている。数は確かめられ、範囲の一致は確かめられないので、partially_verified 相当にする
論拠: 社内アンケート2026の設問5の集計で、1日平均20分。
弱い点: 回答者412名の自己申告の平均。F1 の「探し物に使う時間」に入らない時間（人に聞いて返事を待つ時間など）は、モデルでも数えない（新方式に不利な向き）。 -/
axiom search_current_eq : searchMinutes .current = 20

/-- 【実験】試験環境の全文検索エンジンでは、保存から検索に出るまでが5秒以内。
@support F3
論拠: 試験環境で記事を20件保存し、検索に出るまでの時間を計測した。最大4.2秒。
弱い点: 試験環境の20件で測った値。本番への持ち込みは `prodDelay_le_test` で別に置く。 -/
axiom testDelay_le_five : testDelaySec ≤ 5

/-- 【実験】置き換えの初年度の費用は300万円。
@support F4
@confidence 0.3
@reviewer 0.3 ← 0.6 理由: F4 が述べるのは「見積もりの金額が300万円」まで（ユーザーの証言）。宣言 firstYearCost は「初年度に追加で必要な費用」で、見積もりが社内作業・運用費を含むこと、実際の費用が見積もりを超えないことを述べた事実はない。等号のうち、見積もりの額は F4 で支えられ、見積もりが追加の費用のすべてであることは支えられない。見積書も 02-context/estimate.md に無く確かめられない
論拠: 移行の初年度費用の見積もりが300万円。
弱い点: 金額はユーザーの証言（F4 は user_asserted）。見積もりに、移行の社内作業の時間や、2年目以降の保守の費用が入っているかは分からない。
要ファクト: 見積書で、金額と、費用に含まれる範囲を確かめる。 -/
axiom cost_eq : firstYearCost = 3000000

/-! ### 【経験則】 -/

/-- 【経験則】いまの検索では、保存から検索に出るまで8時間（1日の勤務時間。28800秒）以上かかる。
@support F2
@confidence 0.3
@reviewer 0.3 ← 0.6 理由: F2 は不満の理由の割合で、遅れを測っていない。F2 が支えるのは「当日の記事が出ないことが多い」までで、8時間という下限は述べておらず、原因が遅れか並び（層3）かも分けていない。直接の根拠になりうる「夜間に1回だけ索引を作り直している」（02-context/sources.md の聞き取りメモ）は 06-facts.json に登録されていない
論拠: F2 で、不満の理由の1位が「当日の記事が出てこない」（回答者の48%）。遅れが数分なら、この言い方にはならない。その日のうちに出ない、つまり勤務時間の1日分ほど遅れていると読める。
弱い点: F2 は不満の理由で、遅れを測ったものではない。当日の記事が出ない原因が、並び（層3。新しい記事が結果の下のほうに出る）である可能性もある。
要ファクト: いまの検索の、検索の対象を更新する間隔を、設定で確かめる。 -/
axiom delay_current_ge_workday : 28800 ≤ indexDelaySec .current

/-- 【経験則】置き換えの効果を受ける社員は412人以上。
@support F1
@confidence 0.9
論拠: F1 の平均は回答者412名のもの（F1 の notes）。回答者は社員で、置き換え後も同じ検索を使う。社員全体ではなく回答者だけを数えるので、新方式に不利な向きの置き方になる。
弱い点: 回答者のなかに、異動や退職で検索を使わなくなる人がいる。 -/
axiom beneficiaries_ge : 412 ≤ beneficiaries

/-! ### 【自明】 -/

/-- 【自明】どの方式でも、1日の探し物の時間 = 回数 ×（見つかった場合の時間 ＋ 見つからない確率 × 余分な時間）。
論拠: `foundMinutes` を「見つかった探し物1回の平均の時間」、`missExtraMinutes` を「見つからなかった探し物1回の平均の余分な時間」と決めれば、全確率の公式でそのまま成り立つ。 -/
axiom search_decomp : ∀ M : Method,
  searchMinutes M = searchesPerDay M * (foundMinutes M + (missProb M).val * missExtraMinutes M)

/-- 【自明】どの方式でも、1日の探し物の時間は0以上。
論拠: 時間は負にならない。 -/
axiom searchMinutes_nonneg : ∀ M : Method, 0 ≤ searchMinutes M

/-- 【自明】どの方式でも、見つかった探し物1回の時間は0以上。
論拠: 時間は負にならない。 -/
axiom foundMinutes_nonneg : ∀ M : Method, 0 ≤ foundMinutes M

/-! ### 【仮定】層1: まだ検索に出ない -/

/-- 【仮定】本番の記事数でも、全文検索エンジンで保存から検索に出るまでの時間は、試験環境で測った時間を超えない。
@support なし（本番と同じ記事数の環境で測った記録はない）
@confidence 0.05
論拠: 保存から検索に出るまでの時間は、主に検索の対象を更新する間隔で決まり、記事の数には大きく依らない、という一般の考え。
弱い点: 本番の記事数での計測ではない（F3 の notes）。記事が多いと更新に時間がかかることがある。
要ファクト: 本番と同じ記事数の環境で、保存から検索に出るまでの時間を測る。 -/
axiom prodDelay_le_test : indexDelaySec .fullText ≤ testDelaySec

/-- 【仮定】どの方式でも、保存から検索に出るまで8時間（28800秒）以上かかるなら、探し物のうち、まだ検索に出ていない記事を探すものは10%以上。
@support なし（探し物1回あたりの、その日の記事を探す割合を数えた記録はない）
@confidence 0.05
論拠: 遅れが8時間以上あれば、その日に保存された記事は、その日のうちには検索に出ない。F2 で48%が「当日の記事が出てこない」を挙げていて、当日の記事を探すことは珍しくない。
向き: 中立。どの方式にも同じ形で当てはめる。社員がどれだけ新しい記事を探すかは、社員の仕事で決まり、検索の仕組みに依らない（設計書の4節）。
弱い点: F2 は回答者に占める割合で、探し物1回あたりの割合は、どの事実にもない。10%は案の値で、`claim_C3_saved` が崩れる境目は約5.8%（設計書の5節）。
要ファクト: いまの検索の記録（検索と閲覧の記録）で、探し物のうち、その日に保存された記事を探していたものの割合を数える。 -/
axiom notYet_ge_of_slow : ∀ M : Method, 28800 ≤ indexDelaySec M → 1 / 10 ≤ (pNotYet M).val

/-- 【仮定】どの方式でも、保存から検索に出るまで5秒以内なら、まだ検索に出ていない記事を探すものは0.1%以下。
@support なし（保存の直後に、その記事を探す検索を数えた記録はない）
@confidence 0.05
論拠: 記事を保存してから5秒以内に、その記事を探す人はほとんどいない。
向き: 中立。どの方式にも同じ形で当てはめる。社員がどれだけ新しい記事を探すかは、社員の仕事で決まり、検索の仕組みに依らない（設計書の4節）。
弱い点: 書いた本人が、保存した直後に検索で確かめることはある。
要ファクト: 記事の保存から5秒以内に、その記事を探す検索がどれだけあるかを、記録で数える。 -/
axiom notYet_le_of_fast : ∀ M : Method, indexDelaySec M ≤ 5 → (pNotYet M).val ≤ 1 / 1000

/-! ### 【仮定】層2・層3: いまの検索の値 -/

/-- 【仮定】いまの検索で、検索に出る状態の記事が、入れた語で引けない確率は20%以下。
@support なし（結果が0件だった検索の割合を数えた記録はない）
@confidence 0.05
論拠: いまの検索でも、探し物の多くは見つかっている（見つからなければ、1日20分では収まらない）。
弱い点: 20%は案の値。
要ファクト: 検索の記録で、結果が0件だった検索の割合を数える。アンケートで、見つからなかった理由を聞く。 -/
axiom noHit_current_le : (pNoHit .current).val ≤ 1 / 5

/-- 【仮定】いまの検索で、引けた記事を結果の中で見落とす確率は20%以下。
@support なし（結果は出たが記事を開かずに終わった検索を数えた記録はない）
@confidence 0.05
論拠: いまの検索でも、探し物の多くは見つかっている（見つからなければ、1日20分では収まらない）。
弱い点: 20%は案の値。
要ファクト: 検索の記録で、結果は出たが、どの記事も開かずに終わった検索の割合を数える。 -/
axiom overlook_current_le : (pOverlook .current).val ≤ 1 / 5

/-! ### 【仮定】層2・層3: 同じとみなす -/

/-- 【仮定】語で引けない確率は、方式によらず同じ。
@support なし（同じ検索語で2つの方式を比べた記録はない）
@confidence 0.05
論拠: 事実がないので、方式による違いを見込まない。
向き: 新方式に不利。全文検索エンジンは本文の語でも引けるので下がる見込みがあるが、それを見込まない。
弱い点: 全文検索エンジンのほうが語で引けるなら、層2からも効果が生まれ、取り戻せる時間は増える。
要ファクト: 同じ検索語の組を、試験環境で2つの方式に入れ、引けた割合を比べる。 -/
axiom noHit_same : pNoHit .fullText = pNoHit .current

/-- 【仮定】見落とす確率は、方式によらず同じ。
@support なし（同じ探し物で見落としを2つの方式で比べた記録はない）
@confidence 0.05
論拠: 事実がないので、方式による違いを見込まない。
向き: 新方式に有利。本文の語でも引けると結果が増え、見落としが増える可能性を見込まない。
弱い点: 全文検索エンジンで結果が増えて見落としが増えるなら、取り戻せる時間は小さくなる。
要ファクト: 試験環境で社員に同じ探し物をしてもらい、結果の中から見つけられた割合を2つの方式で比べる。 -/
axiom overlook_same : pOverlook .fullText = pOverlook .current

/-! ### 【仮定】層の合成 -/

/-- 【仮定】どの方式でも、探し物1回が見つからない確率 = 1 −（層1で失敗しない確率 × 層2で失敗しない確率 × 層3で失敗しない確率）。3つの層の失敗は独立。
@support なし（見つからなかった探し物の理由の重なりを数えた記録はない）
@confidence 0.05
論拠: 記事がまだ出ていないこと、語で引けないこと、見落とすことは、別々の原因で起こる。3つの層の失敗が互いに重ならない（排反）とみなす置き方に比べると、独立とみなすほうが、取り戻せる時間を小さく見積もる（新方式に不利な向き）。
弱い点: 新しい記事ほど語で引けにくい、などの重なりがありうる。
要ファクト: 見つからなかった探し物の理由を1件ずつ記録し、理由が重なる割合を確かめる。 -/
axiom miss_compose : ∀ M : Method,
  (missProb M).val = 1 - (1 - (pNotYet M).val) * (1 - (pNoHit M).val) * (1 - (pOverlook M).val)

/-! ### 【仮定】時間: いまの検索の値 -/

/-- 【仮定】いまの検索で、社員1人が1日に検索で探し物をする回数は4回以上。
@support なし（1人1日あたりの検索の回数を数えた記録はない）
@confidence 0.05
論拠: 1日20分を数回の探し物で使っていると考えるのが自然。
弱い点: 4回は案の値。
要ファクト: 検索の記録から、1人1日あたりの検索の回数を数える。 -/
axiom searches_current_ge : 4 ≤ searchesPerDay .current

/-- 【仮定】いまの検索で、見つからなかった探し物1回は、見つかった場合より5分以上余分にかかる。
@support なし（見つからなかったときの余分な時間を聞いた記録はない）
@confidence 0.05
論拠: 見つからないときは、語を変えて探し直したり、ほかの場所を探したりする。
弱い点: 5分は案の値。
要ファクト: アンケートで、探し物が見つからなかったときに余分にかかる時間を聞く。 -/
axiom missExtra_current_ge : 5 ≤ missExtraMinutes .current

/-! ### 【仮定】時間: 同じとみなす -/

/-- 【仮定】探し物の回数は、方式によらず同じ。
@support なし（試験導入の前後で検索の回数を比べた記録はない）
@confidence 0.05
論拠: 探し物の回数は仕事の中身で決まり、検索の仕組みでは大きく変わらない。
向き: 新方式に有利。見つかりやすくなって検索の回数が増え、時間が増える分を見込まない。
弱い点: 置き換えで検索が使いやすくなると、回数が増えることがある。そのときは、取り戻せる時間はさらに小さくなる（設計書の6節）。
要ファクト: 試験導入の前後で、1人1日あたりの検索の回数を比べる。 -/
axiom searches_same : searchesPerDay .fullText = searchesPerDay .current

/-- 【仮定】見つかった探し物1回の時間は、方式によらず同じ。
@support なし（同じ探し物にかかる時間を2つの方式で測った記録はない）
@confidence 0.05
論拠: 見つかった後に記事を開いて読む時間は、記事で決まる。
向き: 決まらない。結果が増えて選ぶ時間が延びれば新方式に有利な置き方、並びがよくなって縮めば新方式に不利な置き方。
弱い点: 見つかる探し物まで速くなるなら、取り戻せる時間は増え、`unfav_saved_le_lost` は崩れることがある。
要ファクト: 試験環境で、同じ探し物にかかる時間を2つの方式で測る。 -/
axiom foundMinutes_same : foundMinutes .fullText = foundMinutes .current

/-- 【仮定】見つからなかった探し物の余分な時間は、方式によらず同じ。
@support なし（見つからなかった後の行動を聞いた記録はない）
@confidence 0.05
論拠: 見つからなかった後の行動（探し直す、ほかの場所を探す）は、検索の仕組みに依らない。
向き: 中立。
弱い点: 探し直しの時間は、検索の仕組みで変わりうる（探し直しが速くなれば短くなり、結果が増えて選ぶのに手間取れば長くなる）。
要ファクト: 見つからなかった後に何をしているか（探し直す・ほかの場所を探す）を、アンケートで聞く。 -/
axiom missExtra_same : missExtraMinutes .fullText = missExtraMinutes .current

/-! ### 【仮定】金額に直す -/

/-- 【仮定】1年の勤務日数は200日以上。
@support なし（会社の年間の所定労働日数を確かめた記録はない）
@confidence 0.05
論拠: 多くの会社の年間の勤務日数は200日より多いので、控えめな値にした。
弱い点: 初年度は移行の期間があれば、新しい検索を使える日数は減る。
要ファクト: 会社の年間の所定労働日数を、人事に確かめる。 -/
axiom workDays_ge : 200 ≤ workDays

/-- 【仮定】社員1人の1時間あたりの人件費は3,000円以上。
@support なし（会社の負担分を含む人件費を確かめた記録はない）
@confidence 0.05
論拠: 会社の負担分を含む人件費として、控えめな値にした。
弱い点: 会社の実際の値ではない。
要ファクト: 会社の負担分を含む、1時間あたりの人件費を、経理に確かめる。 -/
axiom wage_ge : 3000 ≤ wagePerHour

/-! ### 【仮定】読者の判断 -/

/-- 【仮定】部長が「多い」と受け取る境目は、1人1日20分以下。
@support なし（部長が1日20分をどう受け取るかを確かめた記録はない）
@confidence 0.05
論拠: 1日20分は、年200日で1人あたり約67時間になる。
弱い点: 境目は読者の判断で、証拠がない。
要ファクト: 部長が1日20分を「多い」と受け取るかを、ユーザーに確かめる。または、比べる基準の値（他社や一般の調査）を集める。 -/
axiom many_threshold_le : manyMinutes ≤ 20

/-- 【仮定】いまの検索の仕組みのまま、300万円より安く、保存から検索に出るまでを5秒以内にする方法はない。
@support なし（いまの仕組みで更新の間隔を短くできるかを確かめた記録はない）
@confidence 0.05
論拠: 06-facts.json に、いまの仕組みで遅れを短くできるという事実はない。
弱い点: いまの仕組みの設定を変えるだけで、更新の間隔を短くできる可能性がある。そうなら、置き換えの効果（層1の差）の多くは、安い方法でも得られる（`saved_only_from_notYet`）。
要ファクト: いまの仕組みで更新の間隔を短くできるか、できるならその費用を、情報システム部の担当者に確かめる。 -/
axiom no_cheaper_fix : ¬ CheaperFix

/-- 【仮定】1年分の取り戻せる時間の人件費が初年度の費用を上回り、しかも、もっと安い方法がないなら、部長が承認する理由はそろう。
@support なし（部会での予算の判断の基準を確かめた記録はない）
@confidence 0.05
論拠: 読者は費用対効果に厳しく、「承認するかどうかを判断できる」ことを求めている（03-reader.json）。
弱い点: 03-reader.json は読者像で、06-facts.json の事実ではない。予算の枠や、ほかの案件との優先度で判断が変わりうる。
要ファクト: 部会での予算の判断の基準を、ユーザーに確かめる（費用対効果のほかに、予算の枠や、ほかの案件との優先度があるか）。 -/
axiom approvable_of_net : firstYearCost < benefitYen → ¬ CheaperFix → Approvable

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
