/-!
# 論証のモデル: 社内Wiki検索の刷新提案

設計書: `07-logic/model-plan.md`、2周目の差分の設計書（`07-logic/rounds/02/model-plan-delta.md`）、3周目の差分の設計書 `07-logic/model-plan-delta.md`。
主張: `05-claims.json`。事実: `06-facts.json`。失敗の台帳: `07-logic/ledger.json`。

## 書き方の約束（ガイド `stages/07-logic.md` の「Writer の約束」の要約）

- `def` は計算の手順だけに使う。現実についての判断は、宣言（中身を決めない `axiom`）と関係公理（型が命題の `axiom`）に分ける。
- 判断を、定理の引数、宣言の型、比較相手の定義、計算の def の docstring に置かない。
- 両方式の式に現れる量は、方式を引数に取る。「同じとみなす」なら【仮定】の関係公理にし、理由と向きを書く。
- 論証に必要な関係は、確信度が低くても省かない。要ファクトを付ける。
- 関係公理の型の最上位と ∀ の直下に ∧ を置かない（原子命題ごとに公理を分ける）。
- 関係公理の docstring の先頭に種類を書く: 【自明】（論拠）、【実験】（支える事実）、【経験則】（支える事実・確信度の案・論拠・弱い点）、【仮定】（同上と「要ファクト:」）。
- 印は docstring の行の先頭に書く。CLI は行頭の印だけを読む。
- 主張を示す定理に `@claim C…` を付ける。主張より強い定理は `@beyond C…`、比べる相手を確かめる定理は `@baseline`。
- 不利な結論も定理として導く。有利な向きの仮定を経由しない経路を選ぶ。主張にしない不利な結論の定理は、印を付けず、docstring の先頭に [不利] と書く。
- 検査の警告を消すために、ラベルを変えたり、公理を省いたりしない。
- `@reviewer`・`@against`・`@restates` は Reviewer だけが付ける。

## 主張と定理の対応

種類: [決定論] Prop の世界、[確率] 確率・期待値の比較、[件数] 件数の比較、[不利] 書き手の結論に不利な定理。

| 主張 | 主張の文 | 定理 | 種類 |
|---|---|---|---|
| C0 | 社内Wikiの検索を全文検索エンジンに置き換えるため、来期予算で300万円を承認してほしい | `claim_C0_approvable`（比べる相手は、いまの仕組みのままでできる安い設定の変更 `tuned`） | [確率] |
| C1 | いまの検索では、社員が探し物に多くの時間を使っている | `claim_C1_many` | [決定論] |
| C2 | 置き換えれば、書いた記事がすぐ検索に出るようになる | `claim_C2_soon`（項1: 勤務時間中に保存した記事は、いちばん長くても5秒以内に検索に出る）、`claim_C2_faster`（項2: そのいちばん長い遅れが、いまより短い） | [決定論] |
| C3 | 費用は、失われている時間に比べて小さい | `claim_C3_lost`（読み a: 失われている時間）、`claim_C3_saved`（読み b: いまのままと比べて取り戻せる時間） | [確率] |

主張の定理のほかの定理（`@claim` の印がないもの。`baseline_lost_le_survey` だけに `@baseline` の印を付けている）:

| 定理 | 示すこと | 種類 |
|---|---|---|
| `rat_mul_le_mul` | 0 以上の数どうしの不等式を掛け合わせる（数の補題） | — |
| `missAfterIndex_nonneg` | 層2か層3で失敗する確率は 0 以上（確率の範囲から出る式の補題） | — |
| `miss_sub_notYet` | 見つからない確率 − 層1の確率 =（1 − 層1の確率）× 層2か層3で失敗する確率（`miss_compose` の式の変形） | — |
| `search_layers` | 1日の探し物の時間を、層1の確率と「層2か層3で失敗する確率」で書き直した式（`search_decomp` と `miss_compose` の式の変形） | — |
| `notYet_current_ge` | いまの検索で、まだ検索に出ていない記事を探す確率は 1/10 以上 | [確率] |
| `notYet_tuned_ge` | 安い設定の変更をしても、まだ検索に出ていない記事を探す確率は 1/10 以上 | [確率] |
| `notYet_fullText_le` | 置き換えた後、まだ検索に出ていない記事を探す確率は 1/1000 以下 | [確率] |
| `lost_ge` | 失われている時間（読み a）は1人1日2分以上 | [確率] |
| `saved_ge_gap` | 取り戻せる時間（読み b）は、層1の差に比例する式以上 | [確率] |
| `saved_ge` | 取り戻せる時間（読み b）は1人1日1.2672分以上 | [確率] |
| `savedOverTuned_ge_gap` | 安い設定の変更に比べて取り戻せる時間は、層1の差に比例する式以上 | [確率] |
| `savedOverTuned_ge` | 安い設定の変更に比べて取り戻せる時間は1人1日1.2672分以上 | [確率] |
| `yenPerDailyMinute_ge` | 1人1日1分の時間は、初年度に4,120,000円以上の人件費になる | [決定論] |
| `baseline_lost_le_survey` | いまの検索の「失われている時間」を、アンケートの1日20分より大きく置いていない（比べる相手の確認。`@baseline`） | [決定論] |
| `unfav_saved_le_survey` | 取り戻せる時間は、1日20分を超えない | [不利] |
| `unfav_saved_le_gap` | 取り戻せる時間は、層1の差（いまのままと置き換えた後）に比例する式を超えない | [不利] |
| `unfav_savedOverTuned_le_gap` | 安い設定の変更に比べて取り戻せる時間は、層1の差（安い設定の変更と置き換えた後）に比例する式を超えない | [不利] |
| `unfav_saved_le_lost` | 取り戻せる時間は、失われている時間を超えない | [不利] |

## 設計書（model-plan.md）との違い

model-plan.md、2周目の差分、3周目の差分が食い違うところは、新しい差分の設計書に従った。そのうえでの違い:

- 数の補題 `rat_mul_le_mul`（0 以上の数どうしの不等式を掛け合わせる）を §5 の先頭に置いている（1周目から）。
  関係公理を使わない数学の補題で、標準ライブラリの `grind` が積の単調性を解けないために置いた。現実についての判断は含まない。
- 式の補題を3つ置いている（2周目から）。どれも2周目の差分の6.1節の「Writer への注」に書かれた式の変形を、定理として切り出したもので、新しい判断は含まない。
  - `missAfterIndex_nonneg`: `pNoHit`・`pOverlook` の確率の範囲（`Prob` の型）だけから出る。関係公理を使わない。
  - `miss_sub_notYet`: 【自明】の `miss_compose` だけを使う。
  - `search_layers`: 【自明】の `search_decomp` と `miss_compose` だけを使う。
  - `saved_ge_gap`・`savedOverTuned_ge_gap`・`unfav_saved_le_gap`・`unfav_savedOverTuned_le_gap`・`unfav_saved_le_lost`・`lost_ge` の証明で、同じ変形を繰り返さないために置いた。
- `savedOverTuned_ge_gap` は、`saved_ge_gap` を途中の定理として使って示した（2周目から。依存する関係公理は、2周目の差分の6.1節の「使う判断」と同じ）。
- `current_no_daytime` の「向き:」は、3周目の差分の設計書の「C3 と C0 の層1の下限を決める」ではなく、「C3 の層1の下限と、C2 の項2を決める」と書いた。
  C0 の筋道は、安い設定の変更の層1の下限を `tuned_no_daytime_of_rebuild` から出すので、`current_no_daytime` を通らない（`claim_C0_approvable` が依存する公理に出ない）。
  代わりに、`claim_C2_faster` が `maxDelay_of_noDaytime` と合わせて使う。
- `sameDay_tuned_ge` の「向き:」からは、差分の設計書の文にある、消した公理との比べ（「2周目までの notYet_ge_of_slow は「中立」としていたが」）と、
  指摘の番号（R16）を外し、いまの判断だけを書いた。2周目に `workDays_ge` の向きの行から1周目との比べを外したのと同じ扱いで、意味は変えていない。
- 2周目にこの節へ書いた「CLI は docstring の中の印の語を、文の途中でも印として読む」は誤りだった。CLI が読むのは、docstring の行の先頭の印だけである
  （ガイドの「関係公理と定理の印」）。差分の設計書の文のうち印の語を含むものを言い換えて写したのは、差分の設計書の「Writer への注」の指示に従ったためである
  （例: `current_not_incremental` の弱い点の「反対の証拠にも支える事実にも置けない」）。
- 2周目に、docstring に「向き:」の行がなかった `beneficiaries_ge`（新方式に不利）に「向き:」の行を足した（2周目の差分の5節の数え直しに合わせた）。
- 2周目に、重なる文を1つにまとめた（`prodMaxDelay_le_test` の要ファクトの「本番の記事数の環境で測る」、`beneficiaries_ge` の論拠の「回答者だけを数えるのは不利な向き」）。意味は変えていない。
- 2周目の差分の設計書は、型を変えた `search_decomp`・`approvable_of_net` の名前を変えていない。この2つには `@reviewer` の行がなかったので、名前はそのままにした。
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

/-- 勤務時間中に保存した記事が、保存から検索に出るまでにかかる時間の、いちばん長い場合（秒）。
勤務時間中のどの時刻に保存しても、この時間のうちには検索に出る。移行で欠けて検索に出ない記事は入れない（`IndexComplete` に分けた）。 -/
axiom maxDelaySec : Method → Rat

/-- 試験環境の全文検索エンジンに記事を20件保存して測った、保存から検索に出るまでの時間の最大（秒）。F3 の最大4.2秒に当たる。
本番の `maxDelaySec .fullText` とは別の量なので、方式を取らない。 -/
axiom testDelaySec : Rat

/-- いまの検索の仕組みは、記事を保存するたびに、その記事だけを索引に足せる（索引を丸ごと作り直さずに更新できる）。 -/
axiom CurrentIncremental : Prop

/-- その方式の検索が、Wiki のすべての記事を、閲覧できる人の検索に出る状態で索引に持っている（移行で記事や閲覧の権限が欠けていない）。 -/
axiom IndexComplete : Method → Prop

/-- その方式では、勤務時間中（1日8時間、28800秒）に索引が更新され、その日の勤務時間中に保存された記事が、同じ日の勤務時間中に検索に出ることがある。 -/
axiom DaytimeUpdate : Method → Prop

/-- 層1。探し物1回で、探す記事が、検索の時点でまだ検索に出ていない確率。 -/
axiom pNotYet : Method → Prob

/-- 層1の内訳。探し物1回が、勤務時間中の探し物で、しかも同じ日の勤務時間中に（検索より前に）保存された記事を探すものである確率。 -/
axiom pSameDay : Method → Prob

/-- 勤務時間中に、同じ日の勤務時間中に保存された記事を探したとき、検索の時点でその記事がまだ検索に出ていない確率
（そうした探し物であることを条件とした、条件付きの確率）。 -/
axiom pStale : Method → Prob

/-- 層2。索引に入っている記事を探したとき、入れた語でその記事を引けない確率。索引に入っていることを条件とした、条件付きの確率。 -/
axiom pNoHit : Method → Prob

/-- 層3。引けた記事を、結果の中で見落とす確率。引けたことを条件とした、条件付きの確率。 -/
axiom pOverlook : Method → Prob

/-- 探し物1回が、検索で見つからない確率（3つの層のどれかで失敗する）。
層の確率との関係は、関係公理 `miss_compose` に置く。 -/
axiom missProb : Method → Prob

/-- 社員1人が1日に、検索で探し物をする回数。 -/
axiom searchesPerDay : Method → Rat

/-- 見つかった探し物1回に、検索で使う時間（分）。 -/
axiom foundMinutes : Method → Rat

/-- 層1で見つからなかった（探す記事が、まだ検索に出ていなかった）探し物1回で、見つかった場合より余分に検索で使う時間（分）。
検索の外の時間は入らない。 -/
axiom extraNotYetMinutes : Method → Rat

/-- 層2か層3で見つからなかった（語で引けなかった、見落とした）探し物1回で、見つかった場合より余分に検索で使う時間（分）。
検索の外の時間は入らない。 -/
axiom extraOtherMinutes : Method → Rat

/-- 社員1人が1日に、検索で探し物をするのに使う時間（分）。検索の外でほかの場所を探す時間や、人に聞いて返事を待つ時間は入らない。
F1 の「1日平均20分」は、この量の `current` の値。回数と時間への分け方は、関係公理 `search_decomp` に置く。 -/
axiom searchMinutes : Method → Rat

/-- 置き換えの効果を受ける社員の数。
会社の量で、検索の仕組みを変えても変わらないので、方式を取らない（金額に直すとき、2つの方式の差に1回だけ掛ける）。 -/
axiom beneficiaries : Rat

/-- 初年度のうち、置き換えた検索を使える勤務日数（移行の期間を除く）。会社の量なので、方式を取らない。 -/
axiom workDays : Rat

/-- 社員1人の1時間あたりの人件費（円。会社の負担分を含む）。会社の量なので、方式を取らない。 -/
axiom wagePerHour : Rat

/-- 移行の初年度費用の見積もりの額（円）。置き換える側にだけ現れる量なので、方式を取らない。 -/
axiom estimateYen : Rat

/-- 置き換えの初年度に、実際に追加で必要になる費用（円）。置き換える側にだけ現れる量なので、方式を取らない。
見積もりの額とは別の量で、2つの関係は関係公理 `cost_le_estimate` に置く。 -/
axiom firstYearCost : Rat

/-- 読者（部長）が「多い」と受け取る、1人1日あたりの探し物の時間の境目（分）。読者の判断の量なので、方式を取らない。 -/
axiom manyMinutes : Rat

/-- 置き換えたとき、安い設定の変更（`tuned`）をした場合に比べて、会社が初年度に得る値打ち（円）。2つの方式の差の量なので、方式を取らない。 -/
axiom gainYen : Rat

/-- 部長が、来期予算で300万円を承認する理由がそろっている。 -/
axiom Approvable : Prop

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

/-- 【実験】いまの検索では、社員1人が1日に、検索で探し物をするのに使う時間は20分。
@support F1
論拠: 社内アンケート2026の設問5「検索で探し物をするのに、1日に何分くらい使っていますか」の、回答者412名の平均が20分（survey-2026.md）。設問の範囲は「検索で探し物をする時間」で、`searchMinutes` の範囲（検索で使う時間に限った）と同じ。
弱い点: 自己申告の平均。中央値は15分で、長く答えた人が平均を引き上げている。検索の外でほかの場所を探す時間や、人に聞いて待つ時間は、設問にもモデルにも入らない（新方式に不利な向き）。 -/
axiom searchTime_current_eq : searchMinutes .current = 20

/-- 【実験】試験環境の全文検索エンジンでは、保存から検索に出るまでが5秒以内。
@support F3
論拠: 試験環境で記事を20件保存し、検索に出るまでの時間を計測した。最大4.2秒。
弱い点: 試験環境の20件で測った値。本番への持ち込みは `prodMaxDelay_le_test` で別に置く。 -/
axiom testDelay_le_five : testDelaySec ≤ 5

/-- 【実験】移行の初年度費用の見積もりの額は300万円。
@support F4
論拠: 移行の初年度費用の見積もりは300万円（F4）。estimate.md は、この見積もりが構築と移行作業を含むと書く。
弱い点: 金額はユーザーの証言で、見積書はユーザーの手元にある（F4 の notes）。 -/
axiom estimate_eq : estimateYen = 3000000

/-! ### 【経験則】 -/

/-- 【経験則】いまの検索は、勤務時間中に索引を更新しない。
@support F2
@confidence 0.3
論拠: F2 で、不満の理由の1位が「当日の記事が出てこない」（回答者の48%）。勤務時間中に索引を更新していれば、この不満がいちばん多くはならない。
弱い点: F2 は不満の理由で、索引の更新の仕方を述べていない。原因が並び（層3。新しい記事が結果の下のほうに出る）かもしれない。聞き取りメモ（sources.md）の「昨日書いた手順が検索で見つからない」は、夜間に作り直しているなら昨日の記事は今日には出るはずで、食い違う。原因は、作り直しの失敗か、層2・層3かもしれない。
要ファクト: 聞き取りメモの「いまの検索は、夜間に1回だけ索引を作り直している」を事実として登録し、設定で確かめる。登録すれば、この公理を直接支える。「昨日書いた手順が見つからない」の原因を、問い合わせの記録で確かめる。
向き: 新方式に有利（C3 の層1の下限と、C2 の項2（いまより早く検索に出る）を決める）。 -/
axiom current_no_daytime : ¬ DaytimeUpdate .current

/-- 【経験則】置き換えの効果を受ける社員は412人以上。
@support F1
@confidence 0.9
論拠: F1 の平均は回答者412名のもの（F1 の notes）。回答者は社員で、置き換え後も同じ検索を使う。アンケートの対象は全社員480名で（survey-2026.md）、回答者の412名だけを数えるのは、新方式に不利な向きの置き方である。
弱い点: 回答者のなかに、異動や退職で検索を使わなくなる人がいる。
向き: 新方式に不利（効果を受ける人を少なめに数える）。 -/
axiom beneficiaries_ge : 412 ≤ beneficiaries

/-! ### 【自明】 -/

/-- 【自明】どの方式でも、1日の探し物の時間 = 回数 ×（見つかった場合の時間 ＋ 層1で見つからない確率 × 層1の余分な時間 ＋（見つからない確率 − 層1で見つからない確率）× 層2・層3の余分な時間）。
論拠: `foundMinutes` を「見つかった探し物1回の平均の時間」、それに `extraNotYetMinutes` を足したものを「層1で見つからなかった探し物1回の平均の時間」、`extraOtherMinutes` を足したものを「層2・層3で見つからなかった探し物1回の平均の時間」と決めれば、全確率の公式でそのまま成り立つ。層1で見つからない確率は `pNotYet`、層2・層3で見つからない確率は `missProb` − `pNotYet` で、2つは重ならない。 -/
axiom search_decomp : ∀ M : Method,
  searchMinutes M = searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M
    + ((missProb M).val - (pNotYet M).val) * extraOtherMinutes M)

/-- 【自明】どの方式でも、1日の探し物の時間は0以上。
論拠: 時間は負にならない。 -/
axiom searchMinutes_nonneg : ∀ M : Method, 0 ≤ searchMinutes M

/-- 【自明】どの方式でも、見つかった探し物1回の時間は0以上。
論拠: 時間は負にならない。 -/
axiom foundMinutes_nonneg : ∀ M : Method, 0 ≤ foundMinutes M

/-- 【自明】どの方式でも、1日の探し物の回数は0以上。
論拠: 回数は負にならない。 -/
axiom searchesPerDay_nonneg : ∀ M : Method, 0 ≤ searchesPerDay M

/-- 【自明】どの方式でも、探し物1回が見つからない確率 = 1 −（1 − 層1の確率）×（1 − 層2の確率）×（1 − 層3の確率）。
論拠: `pNoHit` を「索引に入っている記事のうち、語で引けない割合」、`pOverlook` を「引けた記事のうち、見落とす割合」という条件付きの確率として宣言した。見つかるのは、索引に入っていて、語で引けて、見落とさないときだけなので、見つかる確率 =（1 − 層1）×（1 − 層2）×（1 − 層3）は、確率の連鎖律そのものである。3つの層が独立だという判断は要らない。 -/
axiom miss_compose : ∀ M : Method,
  (missProb M).val = 1 - (1 - (pNotYet M).val) * (1 - (pNoHit M).val) * (1 - (pOverlook M).val)

/-- 【自明】どの方式でも、勤務時間中に索引を更新しないなら、勤務時間中に保存した記事のいちばん長い遅れは8時間（28800秒）以上。
論拠: 勤務時間中に索引を更新しない方式では、勤務の始まりに保存した記事は、勤務が終わるまで検索に出ない。`maxDelaySec` はどの時刻に保存した場合も含む「いちばん長い場合」で、勤務時間は `DaytimeUpdate` の宣言で8時間と決めたので、28800秒以上になる。C2 が使うのは、いまの遅れが5秒より長いことだけである。 -/
axiom maxDelay_of_noDaytime : ∀ M : Method, ¬ DaytimeUpdate M → 28800 ≤ maxDelaySec M

/-- 【自明】どの方式でも、勤務時間中に索引を更新しないなら、その日の記事をその日の勤務時間中に探すと、必ずまだ検索に出ていない。
論拠: 勤務時間中に索引を更新しない方式では、その日の勤務時間中に保存された記事は、その日の勤務時間中には検索に出ない。`pStale` は勤務時間中にその日の記事を探す探し物についての確率なので、1になる。型は下側（1 以上）だけを置く。上側は `Prob` の範囲で決まる。 -/
axiom stale_of_noDaytime : ∀ M : Method, ¬ DaytimeUpdate M → 1 ≤ (pStale M).val

/-- 【自明】どの方式でも、その日の記事を勤務時間中に探し、しかもその記事がまだ検索に出ていない確率は、層1の確率を超えない。
論拠: `pSameDay` × `pStale` は、連鎖律で「勤務時間中にその日の記事を探し、しかもその記事がまだ検索に出ていない」確率になる。これは「探す記事が、検索の時点でまだ検索に出ていない」（`pNotYet`）の一部なので、全体の確率を超えない。 -/
axiom notYet_ge_sameDay_stale : ∀ M : Method, (pSameDay M).val * (pStale M).val ≤ (pNotYet M).val

/-! ### 【仮定】層1: まだ検索に出ない -/

/-- 【仮定】本番の記事数でも、置き換えた後の、勤務時間中に保存した記事のいちばん長い遅れは、試験環境で測った20件の最大を超えない。
@support なし（本番と同じ記事数の環境で測った記録はない）
@confidence 0.05
論拠: 保存から検索に出るまでの時間は、主に検索の対象を更新する間隔で決まり、記事の数には大きく依らない、という一般の考え。試験環境は「本番と同じ構成」（trial.md）で、違うのは記事の数だけである。
弱い点: 本番の記事数での計測ではない（F3 の notes）。記事が多いと更新に時間がかかることがある。試験環境の20件を、勤務時間のいろいろな時刻に散らして保存したかは分からない。20件の最大は、「どの時刻に保存しても」のいちばん長い場合より短いことがある。
要ファクト: 本番の記事数（約3万件、trial.md）の環境で、保存から検索に出るまでの時間を測る。trial.md の「本番と同じ構成」を事実として登録する。
向き: 新方式に有利。 -/
axiom prodMaxDelay_le_test : maxDelaySec .fullText ≤ testDelaySec

/-- 【仮定】いまの検索で、探し物のうち、勤務時間中に、同じ日の勤務時間中に保存された記事を探すものは10%以上。
@support なし（探し物1回あたりの、その日の記事を探す割合を数えた記録はない）
@confidence 0.05
論拠: F2 で48%が「当日の記事が出てこない」を挙げていて、その日の記事を探すことは珍しくない。
弱い点: F2 は回答者に占める割合で、探し物1回あたりの割合は、どの事実にもない。10%は案の値。結論が崩れる境目は、ほかの値をいまの案のままにすると約5.8%（C3 でも C0 でも同じ）。「昨日書いた手順が見つからない」の原因が層2・層3なら、10%を下回りうる。
要ファクト: いまの検索の記録（検索と閲覧の記録）で、勤務時間中の探し物のうち、同じ日に保存された記事を探していたものの割合を数える。
向き: 量の仮定。大きいほど新方式に有利。 -/
axiom sameDay_current_ge : 1 / 10 ≤ (pSameDay .current).val

/-- 【仮定】安い設定の変更をしても、探し物のうち、その日の記事を勤務時間中に探すものの割合は減らない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 社員がどれだけ新しい記事を探すかは、仕事の中身で決まる。安い設定の変更は、索引を更新する時機だけを変える。
弱い点: 設定の変更と一緒に、「当日の記事は翌日に探す」などの使い方を案内すれば、この割合は下がる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に有利。「社員がどれだけ新しい記事を探すかは方式に依らない」という判断のうち、安い設定の変更に当てはめる部分は C0 に有利な向きなので、その片側だけを置いた。 -/
axiom sameDay_tuned_ge : (pSameDay .current).val ≤ (pSameDay .tuned).val

/-- 【仮定】どの方式でも、勤務時間中に保存した記事が、いちばん長くても5秒で検索に出て、しかも移行で欠けた記事がないなら、まだ検索に出ていない記事を探すものは0.1%以下。
@support なし（保存の直後に、その記事を探す検索を数えた記録はない）
@confidence 0.05
論拠: 記事を保存してから5秒以内に、その記事を探す人はほとんどいない。
向き: 中立。どの方式にも同じ形で当てはめる。社員がどれだけ新しい記事を探すかは、社員の仕事で決まり、検索の仕組みに依らない（設計書の4節）。
弱い点: 書いた本人が、保存した直後に検索で確かめることはある。移行で欠けた記事は、遅れによらず検索に出ない。その分は前提の `IndexComplete` に分け、`fullText_complete` に置いた。
要ファクト: 記事の保存から5秒以内に、その記事を探す検索がどれだけあるかを、記録で数える。 -/
axiom notYet_le_of_maxFast : ∀ M : Method, maxDelaySec M ≤ 5 → IndexComplete M → (pNotYet M).val ≤ 1 / 1000

/-- 【仮定】置き換えた後の検索は、Wiki のすべての記事を、閲覧できる人の検索に出る状態で索引に持つ（移行で欠けない）。
@support なし（移行の前後で、記事数と閲覧の権限を突き合わせた記録はない）
@confidence 0.05
論拠: 移行の作業には、記事を移すことが含まれる（estimate.md の「移行作業」）。
弱い点: 本番の記事は約3万件ある（trial.md）。移行で記事や添付、閲覧の権限が欠けると、その記事は遅れによらず検索に出ない。estimate.md は、閲覧の権限を移すことにはふれていない。
要ファクト: 移行の試験で、移行の前後の記事数と閲覧の権限を突き合わせる。
向き: 新方式に有利。新方式だけに起こる失敗を見込まない。 -/
axiom fullText_complete : IndexComplete .fullText

/-! ### 【仮定】安い設定の変更で、勤務時間中に索引を更新できるか -/

/-- 【仮定】いまの検索の仕組みは、記事を保存するたびに、その記事だけを索引に足すことができない。
@support なし（いまの検索の仕組みの種類と、索引の更新の仕方を確かめた記録はない）
@confidence 0.05
論拠: 02-context/sources.md の聞き取りメモは「いまの検索は、夜間に1回だけ索引を作り直している」と書く。保存のたびに索引へ足せるなら、作り直しを待つ必要はない。
弱い点: 03-reader.json の avoid_terms は、Elasticsearch を「いまの検索の仕組み」に言い換えるよう指定している。いまの仕組みが Elasticsearch なら、記事ごとに索引へ足せるのが普通で、この公理は誤りになる（棄却の候補）。夜間の作り直しは、仕組みの制約ではなく、設定かもしれない。03-reader.json と聞き取りメモは 06-facts.json の事実ではないので、反対の証拠にも支える事実にも置けない。
要ファクト: いまの検索の仕組みが何か（Elasticsearch か）、記事を保存のたびに索引へ足す設定があるか、夜間に作り直している理由を、情報システム部に確かめる。聞き取りメモの「夜間に1回だけ索引を作り直している」を事実として登録する。
向き: C0 に有利。 -/
axiom current_not_incremental : ¬ CurrentIncremental

/-- 【仮定】いまの仕組みが保存のたびに索引へ足せないなら、300万円より安い設定の変更では、勤務時間中に索引を1回も更新できない。
@support なし（作り直しにかかる時間と負荷、勤務時間中に回す費用を確かめた記録はない）
@confidence 0.05
論拠: 保存のたびに索引へ足せないなら、新しい記事を検索に出すには、索引を丸ごと作り直すしかない。いまの仕組みは、作り直しを夜間に1回だけ回している（sources.md の聞き取りメモ）。夜間に回すのは、作り直しが重く、勤務時間中に回すと検索が止まるか遅くなるからだと考えられる。300万円より安い設定の変更では、この重さは変わらない。`tuned` は安い変更のうち記事がいちばん早く検索に出るものなので、勤務時間中に1回でも更新できる安い変更があれば、`tuned` もそうする。だからこの公理は、「300万円より安い変更のどれでも、勤務時間中に索引を1回も更新できない」という意味になる。
弱い点: 本番の記事は約3万件（trial.md）で、作り直しが数分で済み負荷も小さいなら、昼に1回回すのは設定だけでできる。そのとき、この公理は誤りになる。1回だけなら、その日の記事がまだ出ていない確率は約0.63〜0.65（保存と検索の時刻が勤務時間に一様に散らばるとした計算）で、層1は約6.3〜6.5%。C0 が崩れる境目（約5.8%）をわずかに上回る。2回なら約0.5で、境目（約0.58）を下回り、C0 は示せない。夜間に回しているのは、負荷ではなく、ただの設定かもしれない。
要ファクト: 安い設定の変更で、勤務時間中に1回でも索引を作り直せるか。できるなら、1日に何回まで回せて、費用はいくらか。作り直し1回にかかる時間と負荷を、情報システム部に確かめる。
向き: C0 に有利。 -/
axiom tuned_no_daytime_of_rebuild : ¬ CurrentIncremental → ¬ DaytimeUpdate .tuned

/-! ### 【仮定】層2・層3: いまの検索の値 -/

/-- 【仮定】いまの検索で、索引に入っている記事のうちで、入れた語で引けない割合（索引に入っていることを条件とした確率）は20%以下。
@support なし（結果が0件だった検索の割合を数えた記録はない）
@confidence 0.05
論拠: いまの検索でも、探し物の多くは見つかっている（見つからなければ、1日20分では収まらない）。
弱い点: 20%は案の値。survey-2026.md の設問6で、回答者の35%が「言葉が少し違うと見つからない」を挙げた。回答者に占める割合で、探し物1回あたりの割合ではない。
要ファクト: 検索の記録で、結果が0件だった検索の割合を数える。アンケートで、見つからなかった理由を聞く。
向き: 量の仮定。小さいほど新方式に有利（層1の失敗が減った分のうち、層2・層3の失敗に移る分が小さくなる）。設問6の35%は、この値がもっと大きい可能性を示す（回答者に占める割合なので、反対の証拠ではない）。 -/
axiom noHit_current_le : (pNoHit .current).val ≤ 1 / 5

/-- 【仮定】いまの検索で、引けた記事のうちで、結果の中で見落とす割合（引けたことを条件とした確率）は20%以下。
@support なし（結果は出たが記事を開かずに終わった検索を数えた記録はない）
@confidence 0.05
論拠: いまの検索でも、探し物の多くは見つかっている（見つからなければ、1日20分では収まらない）。
弱い点: 20%は案の値。survey-2026.md の設問6で、回答者の22%が「検索結果の並び順が役に立たない」を挙げた。回答者に占める割合で、探し物1回あたりの割合ではない。
要ファクト: 検索の記録で、結果は出たが、どの記事も開かずに終わった検索の割合を数える。
向き: 量の仮定。小さいほど新方式に有利（層1の失敗が減った分のうち、層2・層3の失敗に移る分が小さくなる）。設問6の22%は、この値がもっと大きい可能性を示す（回答者に占める割合なので、反対の証拠ではない）。 -/
axiom overlook_current_le : (pOverlook .current).val ≤ 1 / 5

/-! ### 【仮定】層2・層3: 置き換えで悪くならない（主張の側が使う片側） -/

/-- 【仮定】置き換えても、索引に入っている記事を語で引けない確率は上がらない。
@support なし（同じ検索語で2つの方式を比べた記録はない）
@confidence 0.05
論拠: 全文検索エンジンは、本文の語でも引ける。いまの検索が本文の語で引けないなら、置き換えで下がる。いまの検索も本文の語で引ける（03-reader.json は「いまの検索の仕組み」を Elasticsearch の言い換えとしている）なら、同じ程度になる。どちらでも上がりはしない、とみなす。
弱い点: 置き換えた後は、その日に書かれた新しい記事も索引に入る。新しい記事ほど語で引けにくい（題名や使う語が固まっていない）なら、索引に入っている記事のうちで引けない割合は上がる。1周目は miss_compose の弱い点に書いていたこの重なりを、ここに移した。語の切り方しだいで、「言葉が少し違うと見つからない」（survey-2026.md の設問6で回答者の35%）が増えることもある。
要ファクト: 同じ検索語の組を試験環境で2つの方式に入れ、引けた割合を、新しい記事と古い記事に分けて比べる。
向き: 新方式に有利（主張の側が使う）。 -/
axiom noHit_full_le : (pNoHit .fullText).val ≤ (pNoHit .current).val

/-- 【仮定】置き換えても、引けた記事を見落とす確率は上がらない。
@support なし（同じ探し物で見落としを2つの方式で比べた記録はない）
@confidence 0.05
論拠: 結果の並びの見やすさは、画面で決まる。
弱い点: 本文の語でも引けると結果が増え、見落としが増える。「検索結果の並び順が役に立たない」は、設問6で回答者の22%。
要ファクト: 試験環境で社員に同じ探し物をしてもらい、結果の中から見つけられた割合を2つの方式で比べる。
向き: 新方式に有利（主張の側が使う）。 -/
axiom overlook_full_le : (pOverlook .fullText).val ≤ (pOverlook .current).val

/-! ### 【仮定】層2・層3: 置き換えでよくならない（不利な結論の側だけが使う片側） -/

/-- 【仮定】置き換えても、索引に入っている記事を語で引けない確率は下がらない。
@support なし（同じ検索語で2つの方式を比べた記録はない）
@confidence 0.05
論拠: 事実がないので、置き換えで語で引けるようになる分を見込まない。
弱い点: いまの検索が本文の語で引けないなら、置き換えで層2はよくなり、この公理は崩れる。そのときは効果が層1の外からも生まれ、不利な結論 unfav_saved_le_gap は示せなくなる（新方式に有利な向きに外れる）。
要ファクト: いまの検索の仕組みが本文の語で引けるかを、情報システム部に確かめる。同じ検索語の組を試験環境で2つの方式に入れ、引けた割合を、新しい記事と古い記事に分けて比べる。
向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
axiom noHit_full_ge : (pNoHit .current).val ≤ (pNoHit .fullText).val

/-- 【仮定】置き換えても、引けた記事を見落とす確率は下がらない。
@support なし（同じ探し物で見落としを2つの方式で比べた記録はない）
@confidence 0.05
論拠: 事実がないので、並びがよくなる分を見込まない。
弱い点: 全文検索エンジンの並び（語の合い方の強い順）で見落としが減るなら崩れる。
要ファクト: 試験環境で社員に同じ探し物をしてもらい、結果の中から見つけられた割合を2つの方式で比べる。
向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
axiom overlook_full_ge : (pOverlook .current).val ≤ (pOverlook .fullText).val

/-! ### 【仮定】時間: いまの検索の値 -/

/-- 【仮定】いまの検索で、社員1人が1日に検索で探し物をする回数は4回以上。
@support なし（1人1日あたりの検索の回数を数えた記録はない）
@confidence 0.05
論拠: 1日20分を数回の探し物で使っていると考えるのが自然。
弱い点: 4回は案の値。境目は、ほかの値をいまの案のままにすると約2.3回。
要ファクト: 検索の記録から、1人1日あたりの検索の回数を数える。
向き: 量の仮定。大きいほど新方式に有利（取り戻せる時間は回数に比例する）。 -/
axiom searches_current_ge : 4 ≤ searchesPerDay .current

/-- 【仮定】いまの検索で、層1で見つからなかった（探す記事がまだ検索に出ていなかった）探し物1回は、見つかった場合より5分以上余分に検索で使う。
@support なし（層1で見つからなかったときの余分な時間を聞いた記録はない）
@confidence 0.05
論拠: その日の記事は、どう語を変えても出てこないので、出ていないと気づくまで探し直しが続く。語を変えて検索し、結果を見直すのに1回1分ほどかかり、5回ほど繰り返すと5分になる。
弱い点: 5分は案の値。早くあきらめて書いた人に聞けば、検索で使う時間は短い（そのあと人に聞く時間は、モデルの時間に入らない）。時間を検索で使う時間に限ったので、あきらめて人に聞くまでの時間だけが入る。数回であきらめる人は2〜3分で済む。境目は、ほかの値をいまの案のままにすると約2.9分。
要ファクト: アンケートか聞き取りで、「当日の記事が検索に出なかったとき、検索に余分に何分使ったか」を聞く。見つからなかったとき全般ではなく、層1の失敗に向けて聞く。
向き: 量の仮定。大きいほど新方式に有利。 -/
axiom extraNotYet_current_ge : 5 ≤ extraNotYetMinutes .current

/-- 【仮定】いまの検索で、層1で見つからなかった探し物の余分な時間は0以上。
@support なし（層1で見つからなかったときの余分な時間を聞いた記録はない）
@confidence 0.05
論拠: 探す記事が出てこないときは、見つかったときより検索に長くかかる。
弱い点: 検索で使う時間だけを数えるので、すぐにあきらめれば、見つかったとき（記事を開いて読む時間を含む）より短いことがある。
要ファクト: extraNotYet_current_ge と同じ聞き取り（当日の記事が検索に出なかったとき、検索に余分に何分使ったか）で確かめる。
向き: 符号だけの仮定。extraNotYet_current_ge から導けるが、不利な結論の定理が「5分以上」という量の仮定を通らずに済むように、別に置く。 -/
axiom extraNotYet_nonneg : 0 ≤ extraNotYetMinutes .current

/-- 【仮定】いまの検索で、層2・層3で見つからなかった（語で引けなかった、見落とした）探し物の余分な時間は0以上。
@support なし（層2・層3で見つからなかったときの余分な時間を聞いた記録はない）
@confidence 0.05
論拠: 語が合わないときや見落としたときも、見つかるまでより長く探す。
弱い点: すぐにあきらめれば、見つかったときより短いことがある。
要ファクト: 見つからなかったときの余分な時間を、理由（当日の記事か、語が合わないか、見落としか）ごとに聞く。
向き: 符号だけの仮定。主張の側と不利な結論の側の両方で、積の大小をそろえるために使う。 -/
axiom extraOther_nonneg : 0 ≤ extraOtherMinutes .current

/-- 【仮定】いまの検索で、層2・層3で見つからなかったときの余分な時間は、層1で見つからなかったときの余分な時間を超えない。
@support なし（層2・層3で見つからなかったときの余分な時間を聞いた記録はない）
@confidence 0.05
論拠: 語が合わないときや見落としたときは、語を変えれば見つかることが多い。当日の記事は、どう探しても出てこないので、探し直しが長くなる。
弱い点: 語を変えても見つからず、長く探し続けることもある。
要ファクト: 見つからなかったときの余分な時間を、理由（当日の記事か、語が合わないか、見落としか）ごとに聞き（extraOther_nonneg と同じ聞き取り）、2つの時間を比べる。
向き: 新方式に有利。置き換えで層1の失敗が減ると、その一部は層2・層3の失敗に移る（記事は出るが、語で引けない、見落とす）。その分の余分な時間を小さく見る。 -/
axiom extraOther_le_notYet : extraOtherMinutes .current ≤ extraNotYetMinutes .current

/-! ### 【仮定】時間: 置き換えで悪くならない（主張の側が使う片側） -/

/-- 【仮定】置き換えても、1人1日の探し物の回数は増えない。
@support なし（試験導入の前後で検索の回数を比べた記録はない）
@confidence 0.05
論拠: 探し物の回数は仕事の中身で決まり、検索の仕組みでは大きく変わらない。
弱い点: 検索が役に立つようになると、人に聞く代わりに検索を使う回数が増える。
要ファクト: 試験導入の前後で、1人1日あたりの検索の回数を比べる。
向き: 新方式に有利（主張の側が使う）。 -/
axiom searches_full_le : searchesPerDay .fullText ≤ searchesPerDay .current

/-- 【仮定】置き換えても、見つかった探し物1回の時間は延びない。
@support なし（同じ探し物にかかる時間を2つの方式で測った記録はない）
@confidence 0.05
論拠: 見つかった後に記事を開いて読む時間は、記事で決まる。
弱い点: 本文の語でも引けると結果が増え、選ぶ時間が延びる。
要ファクト: 試験環境で、同じ探し物にかかる時間を2つの方式で測る。
向き: 新方式に有利（主張の側が使う）。 -/
axiom found_full_le : foundMinutes .fullText ≤ foundMinutes .current

/-- 【仮定】置き換えても、層1で見つからなかったときの余分な時間は延びない。
@support なし（層1で見つからなかったときの時間を2つの方式で比べた記録はない）
@confidence 0.05
論拠: 当日の記事が出ないときの探し直し方は、検索の仕組みに依らない。
弱い点: 置き換えた後は層1の失敗がまれ（0.1%以下）なので、この時間が効くのはその分だけである。
要ファクト: アンケートか聞き取りで、「当日の記事が検索に出なかったとき、検索に余分に何分使ったか」を聞く（extraNotYet_current_ge と同じ聞き取り）。
向き: 新方式に有利（主張の側が使う）。 -/
axiom extraNotYet_full_le : extraNotYetMinutes .fullText ≤ extraNotYetMinutes .current

/-- 【仮定】置き換えても、層2・層3で見つからなかったときの余分な時間は延びない。
@support なし（見つからなかったときの探し直しの時間を2つの方式で比べた記録はない）
@confidence 0.05
論拠: 語が合わないときや見落としたときの探し直し方は、検索の仕組みで大きく変わらない。
弱い点: 結果が増えると、探し直しで結果を見直す時間が延びる。
要ファクト: 試験環境で、見つからなかったときの探し直しの時間を2つの方式で比べる。
向き: 新方式に有利（主張の側が使う）。 -/
axiom extraOther_full_le : extraOtherMinutes .fullText ≤ extraOtherMinutes .current

/-! ### 【仮定】時間: 置き換えでよくならない（不利な結論の側だけが使う片側） -/

/-- 【仮定】置き換えても、1人1日の探し物の回数は減らない。
@support なし（試験導入の前後で検索の回数を比べた記録はない）
@confidence 0.05
論拠: 探し物の回数は仕事の中身で決まり、検索の仕組みでは大きく変わらない。
弱い点: 探し直しが減れば、回数は減る。
要ファクト: 試験導入の前後で、1人1日あたりの検索の回数を比べる。
向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
axiom searches_full_ge : searchesPerDay .current ≤ searchesPerDay .fullText

/-- 【仮定】置き換えても、見つかった探し物1回の時間は縮まない。
@support なし（同じ探し物にかかる時間を2つの方式で測った記録はない）
@confidence 0.05
論拠: 見つかった後に記事を開いて読む時間は、記事で決まる。
弱い点: 並びがよくなれば、見つかるまでが短くなる。
要ファクト: 試験環境で、同じ探し物にかかる時間を2つの方式で測る。
向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
axiom found_full_ge : foundMinutes .current ≤ foundMinutes .fullText

/-- 【仮定】置き換えても、層1で見つからなかったときの余分な時間は縮まない。
@support なし（層1で見つからなかったときの時間を2つの方式で比べた記録はない）
@confidence 0.05
論拠: 当日の記事が出ないときの探し直し方は、検索の仕組みに依らない。
弱い点: 置き換えた後は層1の失敗がまれ（0.1%以下）なので、この時間が効くのはその分だけである。
要ファクト: アンケートか聞き取りで、「当日の記事が検索に出なかったとき、検索に余分に何分使ったか」を聞く（extraNotYet_current_ge と同じ聞き取り）。
向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
axiom extraNotYet_full_ge : extraNotYetMinutes .current ≤ extraNotYetMinutes .fullText

/-- 【仮定】置き換えても、層2・層3で見つからなかったときの余分な時間は縮まない。
@support なし（見つからなかったときの探し直しの時間を2つの方式で比べた記録はない）
@confidence 0.05
論拠: 語が合わないときや見落としたときの探し直し方は、検索の仕組みで大きく変わらない。
弱い点: 本文の語でも引けると、探し直しが早く済む。
要ファクト: 試験環境で、見つからなかったときの探し直しの時間を2つの方式で比べる。
向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
axiom extraOther_full_ge : extraOtherMinutes .current ≤ extraOtherMinutes .fullText

/-! ### 【仮定】安い設定の変更は、層1のほかの点でよくならない（C0 の側だけが使う片側） -/

/-- 【仮定】安い設定の変更をしても、1人1日の探し物の回数は減らない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 当日の記事が見つかるようになって探し直しが減れば、回数が減る。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
axiom searches_tuned_ge : searchesPerDay .current ≤ searchesPerDay .tuned

/-- 【仮定】安い設定の変更をしても、見つかった探し物1回の時間は縮まない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 設定の変更と同時に並びの設定も直せば、短くなる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
axiom found_tuned_ge : foundMinutes .current ≤ foundMinutes .tuned

/-- 【仮定】安い設定の変更をしても、層1で見つからなかったときの余分な時間は縮まない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 遅れが短くなって「もう少し待てば出る」と分かれば、探し直しが短くなる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
axiom extraNotYet_tuned_ge : extraNotYetMinutes .current ≤ extraNotYetMinutes .tuned

/-- 【仮定】安い設定の変更をしても、層2・層3で見つからなかったときの余分な時間は縮まない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 設定の変更と同時に語の引き方や並びの設定も直せば、短くなる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
axiom extraOther_tuned_ge : extraOtherMinutes .current ≤ extraOtherMinutes .tuned

/-- 【仮定】安い設定の変更をしても、索引に入っている記事を語で引けない確率は下がらない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 設定の変更と同時に語の切り方（辞書）も直せば、下がる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
axiom noHit_tuned_ge : (pNoHit .current).val ≤ (pNoHit .tuned).val

/-- 【仮定】安い設定の変更をしても、引けた記事を見落とす確率は下がらない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 設定の変更と同時に並びの設定も直せば、下がる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
axiom overlook_tuned_ge : (pOverlook .current).val ≤ (pOverlook .tuned).val

/-! ### 【仮定】安い設定の変更は、層1のほかの点で悪くならない（不利な結論の側だけが使う片側） -/

/-- 【仮定】安い設定の変更をしても、1人1日の探し物の回数は増えない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 設定の変更を社内に知らせると、検索を試す回数が増えることがある。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に不利。安い設定の変更が、層1のほかの点で悪くなる分を見込まない。不利な結論の定理 unfav_savedOverTuned_le_gap だけが使う。 -/
axiom searches_tuned_le : searchesPerDay .tuned ≤ searchesPerDay .current

/-- 【仮定】安い設定の変更をしても、見つかった探し物1回の時間は延びない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 作り直しの間隔を短くすると、作り直しの最中に検索が遅くなり、見つかるまでの時間が延びる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に不利。安い設定の変更が、層1のほかの点で悪くなる分を見込まない。不利な結論の定理 unfav_savedOverTuned_le_gap だけが使う。 -/
axiom found_tuned_le : foundMinutes .tuned ≤ foundMinutes .current

/-- 【仮定】安い設定の変更をしても、層1で見つからなかったときの余分な時間は延びない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 作り直しの最中に検索が遅くなると、探し直しに時間がかかる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に不利。安い設定の変更が、層1のほかの点で悪くなる分を見込まない。不利な結論の定理 unfav_savedOverTuned_le_gap だけが使う。 -/
axiom extraNotYet_tuned_le : extraNotYetMinutes .tuned ≤ extraNotYetMinutes .current

/-- 【仮定】安い設定の変更をしても、層2・層3で見つからなかったときの余分な時間は延びない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 作り直しの最中に検索が遅くなると、探し直しに時間がかかる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に不利。安い設定の変更が、層1のほかの点で悪くなる分を見込まない。不利な結論の定理 unfav_savedOverTuned_le_gap だけが使う。 -/
axiom extraOther_tuned_le : extraOtherMinutes .tuned ≤ extraOtherMinutes .current

/-- 【仮定】安い設定の変更をしても、索引に入っている記事を語で引けない確率は上がらない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 作り直しの設定を変えるときに、語の切り方（辞書）の設定も変わり、引けない語が増えることがある。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に不利。安い設定の変更が、層1のほかの点で悪くなる分を見込まない。不利な結論の定理 unfav_savedOverTuned_le_gap だけが使う。 -/
axiom noHit_tuned_le : (pNoHit .tuned).val ≤ (pNoHit .current).val

/-- 【仮定】安い設定の変更をしても、引けた記事を見落とす確率は上がらない。
@support なし（設定の変更で何が変わるかを確かめた記録はない）
@confidence 0.05
論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
弱い点: 作り直しの間隔を変えると、並びに使う値の更新も変わり、並びが悪くなることがある。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に不利。安い設定の変更が、層1のほかの点で悪くなる分を見込まない。不利な結論の定理 unfav_savedOverTuned_le_gap だけが使う。 -/
axiom overlook_tuned_le : (pOverlook .tuned).val ≤ (pOverlook .current).val

/-! ### 【仮定】金額に直す -/

/-- 【仮定】置き換えの初年度に実際に追加で要る費用は、見積もりの額を超えない。
@support なし（見積もりが、初年度に追加で要る費用のすべてを含むことを述べた事実はない。F4 は額だけを述べる）
@confidence 0.05
論拠: estimate.md は、見積もりが構築と移行作業を含むと書く。主な費用は見積もりに入っている。
弱い点: 社内の担当者の作業時間や、運用の費用（サーバー、保守、使用料）が入っているかは分からない。実際の費用が見積もりを超えることもある。
要ファクト: 見積書で、費用に含まれる範囲（社内の作業時間、運用の費用、使用料）を確かめる。estimate.md の「構築と移行作業を含む」を事実として登録する。
向き: 新方式に有利。見積もりを超える分を見込まない。 -/
axiom cost_le_estimate : firstYearCost ≤ estimateYen

/-- 【仮定】初年度のうち、置き換えた検索を使える勤務日数は200日以上。
@support なし（会社の年間の所定労働日数と、移行にかかる期間を確かめた記録はない）
@confidence 0.05
論拠: 年間の勤務日数は200日より多い。移行の期間を差し引いても、200日を下回らない見込み。
弱い点: 移行に2か月ほどかかれば、200日を下回りうる。
要ファクト: 会社の年間の所定労働日数と、移行にかかる期間を確かめる。
向き: 新方式に有利。比べているのは初年度の費用と初年度の効果で、移行の期間の分だけ日数は減る。 -/
axiom workDays_ge : 200 ≤ workDays

/-- 【仮定】社員1人の1時間あたりの人件費は3,000円以上。
@support なし（会社の負担分を含む人件費を確かめた記録はない）
@confidence 0.05
論拠: 会社の負担分を含む人件費として、控えめな値にした。
弱い点: 会社の実際の値ではない。境目は、ほかの値をいまの案のままにすると約1,724円。
要ファクト: 会社の負担分を含む、1時間あたりの人件費を、経理に確かめる。
向き: 量の仮定。大きいほど新方式に有利。 -/
axiom wage_ge : 3000 ≤ wagePerHour

/-- 【仮定】置き換えで会社が得る値打ちは、安い設定の変更に比べて取り戻せる時間の人件費を下回らない。
@support なし（取り戻した時間を会社の値打ちとして数える基準を確かめた記録はない）
@confidence 0.05
論拠: 会社は社員の時間に人件費を払っている。取り戻した時間がほかの仕事に使われれば、少なくとも人件費の分の値打ちを生む。
弱い点: 取り戻せる時間は1人1日約1.3分で、細切れの時間はほかの仕事に回らないことがある。費用対効果に厳しい読者（03-reader.json）が、最初に尋ねうる点である。
要ファクト: 社内のほかの投資の判断で、節約した時間を人件費で金額に直しているか、部会がその換算を認めるかを、ユーザーに確かめる。
向き: 新方式に有利。 -/
axiom gain_ge_wage : savedOverTunedWageYen ≤ gainYen

/-! ### 【仮定】読者の判断 -/

/-- 【仮定】部長が「多い」と受け取る境目は、1人1日20分以下。
@support なし（部長が1日20分をどう受け取るかを確かめた記録はない）
@confidence 0.05
論拠: 1日20分は、年200日で1人あたり約67時間になる。
弱い点: 境目は読者の判断で、証拠がない。
要ファクト: 部長が1日20分を「多い」と受け取るかを、ユーザーに確かめる。または、比べる基準の値（他社や一般の調査）を集める。 -/
axiom many_threshold_le : manyMinutes ≤ 20

/-- 【仮定】置き換えで会社が得る値打ち（安い設定の変更に比べた分）が初年度の費用を上回るなら、部長が承認する理由はそろう。
@support なし（部会での予算の判断の基準を確かめた記録はない）
@confidence 0.05
論拠: 読者は費用対効果に厳しく、承認するかどうかを判断できることを求めている（03-reader.json）。`gainYen` は安い設定の変更に比べた値打ちなので、「いまの仕組みの設定を変えるだけで足りるのでは」という問いに答える。安い設定の変更の費用（0円以上）を差し引かずに比べるので、差額で比べるより厳しい比べ方になる。
弱い点: 03-reader.json は読者像で、06-facts.json の事実ではない。予算の枠や、ほかの案件との優先度で判断が変わりうる。ほかの製品や、ほかの業者の見積もり（相見積もり）のような、300万円より安い置き換えの案とは比べていない。
要ファクト: 部会での予算の判断の基準（費用対効果のほかに、予算の枠や優先度があるか）を、ユーザーに確かめる。より安い置き換えの案があるか（相見積もり）を、ユーザーに確かめる。
向き: 新方式に有利（判断の基準）。 -/
axiom approvable_of_net : firstYearCost < gainYen → Approvable

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

/-- いまの検索で、まだ検索に出ていない記事を探す確率は 1/10 以上（その日の記事を探す 1/10 以上 × まだ出ていない 1）。 -/
theorem notYet_current_ge : 1 / 10 ≤ (pNotYet .current).val := by
  have h1 := notYet_ge_sameDay_stale .current
  have h2 := stale_of_noDaytime .current current_no_daytime
  have h3 := sameDay_current_ge
  have h4 : (1 / 10) * 1 ≤ (pSameDay .current).val * (pStale .current).val :=
    rat_mul_le_mul (by grind) h3 (by grind) h2
  grind

/-- 安い設定の変更をしても、まだ検索に出ていない記事を探す確率は 1/10 以上（その日の記事を探す 1/10 以上 × まだ出ていない 1）。 -/
theorem notYet_tuned_ge : 1 / 10 ≤ (pNotYet .tuned).val := by
  have h1 := notYet_ge_sameDay_stale .tuned
  have h2 := stale_of_noDaytime .tuned (tuned_no_daytime_of_rebuild current_not_incremental)
  have h3 := sameDay_current_ge
  have h4 := sameDay_tuned_ge
  have h5 : (1 / 10) * 1 ≤ (pSameDay .tuned).val * (pStale .tuned).val :=
    rat_mul_le_mul (by grind) (by grind) (by grind) h2
  grind

/-- 置き換えた後、まだ検索に出ていない記事を探す確率は 1/1000 以下。 -/
theorem notYet_fullText_le : (pNotYet .fullText).val ≤ 1 / 1000 := by
  have h1 := prodMaxDelay_le_test
  have h2 := testDelay_le_five
  exact notYet_le_of_maxFast .fullText (by grind) fullText_complete

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
  rw [searchTime_current_eq]
  exact many_threshold_le

/-- @claim C2 [決定論] 項1: 置き換えれば、勤務時間中に保存した記事は、いちばん長くても保存から5秒以内に検索に出る。 -/
theorem claim_C2_soon : maxDelaySec .fullText ≤ 5 := by
  have h1 := prodMaxDelay_le_test
  have h2 := testDelay_le_five
  grind

/-- @claim C2 [決定論] 項2: 置き換えれば、勤務時間中に保存した記事の、いちばん長い遅れが、いまより短くなる。 -/
theorem claim_C2_faster : maxDelaySec .fullText < maxDelaySec .current := by
  have h1 := claim_C2_soon
  have h2 := maxDelay_of_noDaytime .current current_no_daytime
  grind

/-! ### 比べる相手の確認と、不利な結論 -/

/-- @baseline いまの検索の「失われている時間」（読み a）を、アンケートの1日20分より大きく置いていない。
失われている時間 = 20 − 回数 × 見つかった場合の時間。 -/
theorem baseline_lost_le_survey : lostMinutes ≤ 20 := by
  unfold lostMinutes
  have hd := search_decomp .current
  have he := searchTime_current_eq
  have hs := searchesPerDay_nonneg .current
  have hf := foundMinutes_nonneg .current
  have h0 : 0 ≤ searchesPerDay .current * foundMinutes .current := Rat.mul_nonneg hs hf
  grind

/-- [不利] 置き換えで取り戻せる時間は、1人1日20分を超えない。 -/
theorem unfav_saved_le_survey : savedMinutes ≤ 20 := by
  unfold savedMinutes
  have he := searchTime_current_eq
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

/-- [不利] 安い設定の変更に比べて取り戻せる時間は、回数(いま) ×（安い設定の変更と置き換えた後の層1の差）×
（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）を超えない。
安い設定の変更で層1が下がれば、C0 の効果もそれに比例して縮む。
主張の側の片側の公理（`_full_le`、`_tuned_ge`）も、量の仮定（4回、5分、10%）も通らない。 -/
theorem unfav_savedOverTuned_le_gap :
    savedOverTunedMinutes ≤ searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val)
      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) := by
  have hg := unfav_saved_le_gap
  unfold savedMinutes at hg
  unfold savedOverTunedMinutes
  have hSc := search_layers .current
  have hSt := search_layers .tuned
  have hst := searchesPerDay_nonneg .tuned
  have hfc := foundMinutes_nonneg .current
  have he1 := extraNotYet_nonneg
  have he2 := extraOther_nonneg
  have hs := searches_tuned_le
  have hf := found_tuned_le
  have hx1 := extraNotYet_tuned_le
  have hx2 := extraOther_tuned_le
  have hb := noHit_tuned_le
  have hc := overlook_tuned_le
  have hAt := missAfterIndex_nonneg .tuned
  have hAc := missAfterIndex_nonneg .current
  have hp0 := (pNotYet .tuned).nonneg
  have hp1 := (pNotYet .tuned).le_one
  have hA : missAfterIndex .tuned ≤ missAfterIndex .current := by
    unfold missAfterIndex
    have hb1 := (pNoHit .current).le_one
    have hc1 := (pOverlook .current).le_one
    have hx : (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val)
        ≤ (1 - (pNoHit .tuned).val) * (1 - (pOverlook .tuned).val) :=
      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
    grind
  have h1 : (pNotYet .tuned).val * extraNotYetMinutes .tuned
      ≤ (pNotYet .tuned).val * extraNotYetMinutes .current :=
    Rat.mul_le_mul_of_nonneg_left hx1 hp0
  have h2a : missAfterIndex .tuned * extraOtherMinutes .tuned
      ≤ missAfterIndex .tuned * extraOtherMinutes .current :=
    Rat.mul_le_mul_of_nonneg_left hx2 hAt
  have h2b : missAfterIndex .tuned * extraOtherMinutes .current
      ≤ missAfterIndex .current * extraOtherMinutes .current :=
    Rat.mul_le_mul_of_nonneg_right hA he2
  have h3 : (1 - (pNotYet .tuned).val) * (missAfterIndex .tuned * extraOtherMinutes .tuned)
      ≤ (1 - (pNotYet .tuned).val) * (missAfterIndex .current * extraOtherMinutes .current) :=
    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
  have hG : foundMinutes .tuned + (pNotYet .tuned).val * extraNotYetMinutes .tuned
        + (1 - (pNotYet .tuned).val) * missAfterIndex .tuned * extraOtherMinutes .tuned
      ≤ foundMinutes .current + (pNotYet .tuned).val * extraNotYetMinutes .current
        + (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current := by
    grind
  have hG0a : 0 ≤ (pNotYet .tuned).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 he1
  have hG0b : 0 ≤ (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current :=
    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .tuned).val * extraNotYetMinutes .current
        + (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current := by
    grind
  have h4 := Rat.mul_le_mul_of_nonneg_left hG hst
  have h5 := Rat.mul_le_mul_of_nonneg_right hs hG0
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

end

end WikiSearch
