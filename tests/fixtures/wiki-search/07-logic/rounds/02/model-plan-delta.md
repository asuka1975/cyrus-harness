# 差分の設計書（2周目）: 社内Wiki検索の刷新提案

Logical Model Planner が書く。1周目の監査（review.md。判定: 差し戻し（高 2・中 7・低 6））の指摘に答える、局所修正の設計書である。
Lean Writer は、model-plan.md とこの差分に従って Argument.lean と Model.lean を直す。2つが食い違うところは、この差分に従う。

この文書の読み方:

- 変更は、表の1行に1つずつ書いた。変える宣言・公理・定理の名前は、行の先頭の列にだけ、バッククォートで囲んで挙げた。ほかの列の名前は、囲まずに書いた（差分との対応表を読みやすくするため）。
- この差分に名前の出ていない宣言・公理・定理は、変えない。docstring も変えない（savedMinutes、Approvable なども含む）。
- 論拠・弱い点・要ファクト・向きは、表の下の段落に、公理ごとに書いた。Writer は docstring にそのまま写す。「Writer への注」とある文は写さない。
- 4.5節で、いくつかの公理に「共通」「同上」とまとめて書いた論拠・弱い点・要ファクト・@support なし の理由は、Writer が公理ごとに展開し、それぞれの docstring に全文を書く。docstring に「共通」「同上」とは書かない。
- 9節は「採らない指摘」と「ほかのステージに送る指摘」で、モデルを変えない。

## 0. この周で新しく使った素材

02-context/ に、1周目にはなかった素材が3つ入った。06-facts.json は変わっていないので、@support に挙げる事実は増えない。素材は、公理の論拠・弱い点・要ファクトに引く。

- survey-2026.md: 設問5の文面は「検索で探し物をするのに、1日に何分くらい使っていますか」。回答者412名の平均は20分、中央値は15分。対象は全社員480名。設問6（複数回答）は、「当日の記事が出てこない」48%、「言葉が少し違うと見つからない」35%、「検索結果の並び順が役に立たない」22%。
- trial.md: 試験環境に「本番と同じ構成で」記事を20件保存し、検索に出るまで最小1.1秒・最大4.2秒。本番の記事数（約3万件）では測っていない。
- estimate.md: 初年度費用300万円は「構築と移行作業を含む」。見積書はユーザーの手元にあり、金額だけを写した。

## 1. 指摘ごとの扱い

| 指摘 | 重大度 | 扱い | 直す節 |
|---|---|---|---|
| R1 | 高 | 採る。「いまの仕組みのままでできる、300万円より安い設定の変更」を3つ目の方式としてモデルに入れ、C0 はそれと比べる。安い案の境目を、5秒から8時間（層1の公理の境目）に合わせる | 3・4・5・6・7節 |
| R2 | 高 | 採る。「いまの仕組みは、保存のたびに索引へ足せない」を【仮定】にし、C0 の筋道の上に置く。本文の語で引けるかどうかは、別の公理にせず、層2の片側の公理の弱い点と要ファクトに書く（理由は9節） | 3・4・10節 |
| R3 | 中 | 弱い点と要ファクトを書き直す。確信度は変えない（上げるには事実が要る） | 4節 |
| R4 | 中 | 採る。見積もりの額（【実験】）と、実際の費用が見積もりを超えないこと（【仮定】）に分ける | 3・4節 |
| R5 | 中 | 採る。設問5の文面に合わせ、時間の量を「検索で使う時間」に限る。確信度は変えない | 3・4節 |
| R6 | 中 | 採る。会社が得る値打ちを宣言にし、「人件費の分を下回らない」を【仮定】にする。人件費に直した量の名前も変える | 3・4・6節 |
| R7 | 中 | 採る。余分な時間を「層1で見つからないとき」と「層2・層3で見つからないとき」に分ける | 3・4・6節 |
| R8 | 中 | 採る。「同じとみなす」等式を、主張が使う片側と不利な結論が使う片側に分け、向きを数え直す | 4・5節 |
| R9 | 中 | 一部を採る。取り戻せる時間の無条件の上界を [不利] の定理にする。「層1の差が0以下なら」と境目の定理は、前提が公理から否定されて空回りするので置かない（9節） | 6・7・9節 |
| R10 | 低 | ステージ5で決める | 9節 |
| R11 | 低 | ステージ5で決める。試験環境の量の意味（20件の最大）だけ宣言に書く | 3・9節 |
| R12 | 低 | 採る。失敗でない量の行を外し、新方式だけに起こる失敗の行を足す。移行で記事が欠けることを公理にする | 4・8節 |
| R13 | 低 | 採る。証人の Approvable を、前提から決まる命題にする | 11節 |
| R14 | 低 | ステージ5で決める | 9節 |
| R15 | 低 | 素材が入ったので、引用を確かめられるようになった。事実の登録の見直しはステージ6 | 0・10節 |

## 2. 1節（主張の形と論証の深さ）の変更

- 主張の形は変えない。C0 と C3 は比較の文、C1 と C2 は能力の文のままとする。
- C0 の比べる相手を変える。1周目は「いまのまま」と比べ、「もっと安い方法はない」を1つの【仮定】で足していた。2周目は、置き換えを「いまの仕組みのままでできる、300万円より安い設定の変更」（方式 tuned）と比べる。理由は7節に書いた。
- C3 は、置き換えと「いまのまま」を比べる文なので、比べる相手を変えない。
- C0 の定理は、claim_C3_saved を使わなくなる。C3 は独立した主張として残し、C0 は tuned と比べる同じ形の筋道（savedOverTuned_ge）で示す。1周目の設計書の「C0 は C3 の結論を使う」は、この差分で置き換える。本文では、C3 の数字（いまのままと比べた値）と、C0 の理由（安い設定の変更と比べた値）は、同じ下限の値になる（6.2節）。

## 3. 2節（コンポーネント）の変更

### 3.1 宣言

| 名前 | 変化 | 型 | 何を表すか（docstring に写す） |
|---|---|---|---|
| `Method` | コンストラクタを1つ足す | 型（コンストラクタ current・tuned・fullText） | 比べる3つの方式。current は、いまの検索の仕組み（中身が Elasticsearch などの全文検索エンジンかは、06-facts.json にない）。tuned は、いまの検索の仕組みのまま、300万円より安い費用でできる設定の変更（索引を作り直す間隔を短くする、保存のたびに索引へ足す、など）を、保存から検索に出るまでがいちばん短くなるように施したもの。そうした変更ができないなら、いまのままと同じもの。fullText は、置き換えた後の全文検索エンジン |
| `pNoHit` | docstring を変える | 変えない | 層2。索引に入っている記事を探したとき、入れた語でその記事を引けない確率。索引に入っていることを条件とした、条件付きの確率 |
| `pOverlook` | docstring を変える | 変えない | 層3。引けた記事を、結果の中で見落とす確率。引けたことを条件とした、条件付きの確率 |
| `searchMinutes` | docstring を変える | 変えない | 社員1人が1日に、検索で探し物をするのに使う時間（分）。検索の外でほかの場所を探す時間や、人に聞いて返事を待つ時間は入らない。F1 の「1日平均20分」は、この量の current の値 |
| `foundMinutes` | docstring を変える | 変えない | 見つかった探し物1回に、検索で使う時間（分） |
| `missExtraMinutes` → `extraNotYetMinutes` | 名前と意味を変える | Method → Rat（変えない） | 層1で見つからなかった（探す記事が、まだ検索に出ていなかった）探し物1回で、見つかった場合より余分に検索で使う時間（分）。検索の外の時間は入らない |
| `extraOtherMinutes` | 新設 | Method → Rat | 層2か層3で見つからなかった（語で引けなかった、見落とした）探し物1回で、見つかった場合より余分に検索で使う時間（分）。検索の外の時間は入らない |
| `testDelaySec` | docstring を変える | 変えない | 試験環境の全文検索エンジンに記事を20件保存して測った、保存から検索に出るまでの時間の最大（秒）。F3 の最大4.2秒に当たる。本番の indexDelaySec .fullText とは別の量なので、方式を取らない |
| `workDays` | docstring を変える | 変えない | 初年度のうち、置き換えた検索を使える勤務日数（移行の期間を除く）。会社の量なので、方式を取らない |
| `estimateYen` | 新設 | Rat | 移行の初年度費用の見積もりの額（円）。置き換える側にだけ現れる量なので、方式を取らない |
| `firstYearCost` | docstring を変える | 変えない | 置き換えの初年度に、実際に追加で必要になる費用（円）。見積もりの額とは別の量で、2つの関係は関係公理 cost_le_estimate に置く |
| `gainYen` | 新設。Approvable より前に宣言する | Rat | 置き換えたとき、安い設定の変更（tuned）をした場合に比べて、会社が初年度に得る値打ち（円）。2つの方式の差の量なので、方式を取らない |
| `CurrentIncremental` | 新設 | Prop | いまの検索の仕組みは、記事を保存するたびに、その記事だけを索引に足せる（索引を丸ごと作り直さずに更新できる） |
| `IndexComplete` | 新設 | Method → Prop | その方式の検索が、Wiki のすべての記事を、閲覧できる人の検索に出る状態で索引に持っている（移行で記事や閲覧の権限が欠けていない） |
| `CheaperFix` | 削除 | — | 比べる相手を tuned にしたので要らない（R1） |

宣言の順は、gainYen を Approvable より前にする（11節で、証人の Approvable を gainYen で定義するため）。CurrentIncremental と IndexComplete の位置は Writer が決めてよい。

### 3.2 計算の def

| 名前 | 変化 | 計算 | 何を表すか |
|---|---|---|---|
| `missAfterIndex` | 新設 | 1 −（1 − pNoHit M の値）×（1 − pOverlook M の値） | 方式 M で、索引に入っている記事を探して、層2か層3で失敗する確率 |
| `lostMinutes` | 計算を変える | current の searchesPerDay ×（pNotYet の値 × extraNotYetMinutes ＋（missProb の値 − pNotYet の値）× extraOtherMinutes） | 読み (a)。いまの検索で、見つからなかった探し物のために1人1日に余分に検索で使っている時間 |
| `savedOverTunedMinutes` | 新設 | searchMinutes .tuned − searchMinutes .fullText | 置き換えで、安い設定の変更をした場合に比べて、1人1日に取り戻せる時間 |
| `yenPerDailyMinute` | docstring を変える（計算は同じ） | 変えない | 1人1日1分の時間が、初年度（workDays の日数）でいくらの人件費になるか |
| `lostYen` → `lostWageYen` | 名前を変える（計算は同じ） | yenPerDailyMinute × lostMinutes | 読み (a) の時間の、初年度の人件費 |
| `benefitYen` → `savedWageYen` | 名前を変える（計算は同じ） | yenPerDailyMinute × savedMinutes | 読み (b) の時間の、初年度の人件費。会社の得ではなく、人件費に直した量であることを名前に出す（R6） |
| `savedOverTunedWageYen` | 新設 | yenPerDailyMinute × savedOverTunedMinutes | 安い設定の変更に比べて取り戻せる時間の、初年度の人件費 |

## 4. 3節（関係公理）の変更

### 4.1 消す公理

| 名前 | 理由 | 代わりに置くもの |
|---|---|---|
| `cost_eq` | 等号が、「見積もりの額は300万円」と「実際の費用は見積もりを超えない」の2つの判断を含んでいた（R4） | estimate_eq・cost_le_estimate |
| `no_cheaper_fix` | 「5秒以内」で定義した安い案は、効果が生まれる遅れの幅とずれていて、藁人形になっていた（R1） | current_not_incremental・tuned_slow_of_rebuild と方式 tuned |
| `searches_same` | 等式は、主張が使う片側（置き換えで悪くならない）と、不利な結論だけが使う片側（よくならない）を1つにしていた。そのため、有利な証拠（置き換えで回数が減る）が見つかっても等式は崩れ、主張の定理まで示せなくなる（R8） | searches_full_le・searches_full_ge |
| `foundMinutes_same` | 同上 | found_full_le・found_full_ge |
| `missExtra_same` | 同上。余分な時間を層で分けた（R7） | extraNotYet_full_le・extraNotYet_full_ge・extraOther_full_le・extraOther_full_ge |
| `noHit_same` | 同上。有利な証拠（全文検索のほうが語で引ける）で崩れることが、いちばん起こりやすい（R2） | noHit_full_le・noHit_full_ge |
| `overlook_same` | 同上 | overlook_full_le・overlook_full_ge |

### 4.2 型か種類を変える公理

| 名前 | 変化 | 種類 | 命題（日常語） | 型 | @support | 確信度の案 |
|---|---|---|---|---|---|---|
| `search_decomp` | 型を変える | 【自明】 | どの方式でも、1日の探し物の時間 = 回数 ×（見つかった場合の時間 ＋ 層1で見つからない確率 × 層1の余分な時間 ＋（見つからない確率 − 層1で見つからない確率）× 層2・層3の余分な時間） | `∀ M : Method, searchMinutes M = searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M + ((missProb M).val - (pNotYet M).val) * extraOtherMinutes M)` | — | 1 |
| `miss_compose` | 種類を【仮定】から【自明】に変える。型は変えない | 【自明】 | どの方式でも、見つからない確率 = 1 −（1 − 層1）×（1 − 層2）×（1 − 層3） | 変えない | — | 1 |
| `notYet_le_of_fast` | 前提を1つ足す | 【仮定】 | どの方式でも、保存から検索に出るまで5秒以内で、しかも移行で欠けた記事がないなら、まだ検索に出ていない記事を探すものは0.1%以下 | `∀ M : Method, indexDelaySec M ≤ 5 → IndexComplete M → (pNotYet M).val ≤ 1 / 1000` | なし | 0.05 |
| `missExtra_current_ge` → `extraNotYet_current_ge` | 名前と型を変える | 【仮定】 | いまの検索で、層1で見つからなかった探し物1回は、見つかった場合より5分以上余分に検索で使う | 5 ≤ extraNotYetMinutes .current | なし | 0.05 |
| `approvable_of_net` | 型を変える | 【仮定】 | 置き換えで会社が得る値打ち（安い設定の変更に比べた分）が初年度の費用を上回るなら、部長が承認する理由はそろう | firstYearCost < gainYen → Approvable | なし | 0.05 |

### 4.3 docstring だけを変える公理（型・種類・確信度は変えない）

| 名前 | 変えるところ |
|---|---|
| `search_current_eq` | 論拠と弱い点（4.5節）。@confidence 0.75 と @reviewer の行は、そのまま残す |
| `delay_current_ge_workday` | 弱い点と要ファクト（4.5節）。@confidence 0.3 と @reviewer の行は、そのまま残す |
| `notYet_ge_of_slow` | 当てはめる方式に tuned が入ること、弱い点、要ファクト（4.5節） |
| `prodDelay_le_test` | 論拠と要ファクト（4.5節） |
| `beneficiaries_ge` | 論拠（4.5節） |
| `workDays_ge` | 命題の読み（初年度に使える日数）、論拠、弱い点、要ファクト、向き（4.5節） |
| `noHit_current_le` | 命題の読み（条件付きの確率）と弱い点（4.5節） |
| `overlook_current_le` | 命題の読み（条件付きの確率）と弱い点（4.5節） |

### 4.4 新しく置く公理

| 名前 | 種類 | 命題（日常語） | 型 | @support | 確信度の案 |
|---|---|---|---|---|---|
| `estimate_eq` | 【実験】 | 移行の初年度費用の見積もりの額は300万円 | estimateYen = 3000000 | F4 | 事実の値（user_asserted なので 0.6） |
| `cost_le_estimate` | 【仮定】 | 置き換えの初年度に実際に追加で要る費用は、見積もりの額を超えない | firstYearCost ≤ estimateYen | なし | 0.05 |
| `searchesPerDay_nonneg` | 【自明】 | どの方式でも、1日の探し物の回数は0以上 | ∀ M : Method, 0 ≤ searchesPerDay M | — | 1 |
| `fullText_complete` | 【仮定】 | 置き換えた後の検索は、Wiki のすべての記事を、閲覧できる人の検索に出る状態で索引に持つ（移行で欠けない） | IndexComplete .fullText | なし | 0.05 |
| `extraNotYet_nonneg` | 【仮定】 | いまの検索で、層1で見つからなかった探し物の余分な時間は0以上 | 0 ≤ extraNotYetMinutes .current | なし | 0.05 |
| `extraOther_nonneg` | 【仮定】 | いまの検索で、層2・層3で見つからなかった探し物の余分な時間は0以上 | 0 ≤ extraOtherMinutes .current | なし | 0.05 |
| `extraOther_le_notYet` | 【仮定】 | いまの検索で、層2・層3で見つからなかったときの余分な時間は、層1で見つからなかったときの余分な時間を超えない | extraOtherMinutes .current ≤ extraNotYetMinutes .current | なし | 0.05 |
| `searches_full_le` | 【仮定】 | 置き換えても、1人1日の探し物の回数は増えない | searchesPerDay .fullText ≤ searchesPerDay .current | なし | 0.05 |
| `searches_full_ge` | 【仮定】 | 置き換えても、1人1日の探し物の回数は減らない | searchesPerDay .current ≤ searchesPerDay .fullText | なし | 0.05 |
| `found_full_le` | 【仮定】 | 置き換えても、見つかった探し物1回の時間は延びない | foundMinutes .fullText ≤ foundMinutes .current | なし | 0.05 |
| `found_full_ge` | 【仮定】 | 置き換えても、見つかった探し物1回の時間は縮まない | foundMinutes .current ≤ foundMinutes .fullText | なし | 0.05 |
| `extraNotYet_full_le` | 【仮定】 | 置き換えても、層1で見つからなかったときの余分な時間は延びない | extraNotYetMinutes .fullText ≤ extraNotYetMinutes .current | なし | 0.05 |
| `extraNotYet_full_ge` | 【仮定】 | 置き換えても、層1で見つからなかったときの余分な時間は縮まない | extraNotYetMinutes .current ≤ extraNotYetMinutes .fullText | なし | 0.05 |
| `extraOther_full_le` | 【仮定】 | 置き換えても、層2・層3で見つからなかったときの余分な時間は延びない | extraOtherMinutes .fullText ≤ extraOtherMinutes .current | なし | 0.05 |
| `extraOther_full_ge` | 【仮定】 | 置き換えても、層2・層3で見つからなかったときの余分な時間は縮まない | extraOtherMinutes .current ≤ extraOtherMinutes .fullText | なし | 0.05 |
| `noHit_full_le` | 【仮定】 | 置き換えても、索引に入っている記事を語で引けない確率は上がらない | (pNoHit .fullText).val ≤ (pNoHit .current).val | なし | 0.05 |
| `noHit_full_ge` | 【仮定】 | 置き換えても、索引に入っている記事を語で引けない確率は下がらない | (pNoHit .current).val ≤ (pNoHit .fullText).val | なし | 0.05 |
| `overlook_full_le` | 【仮定】 | 置き換えても、引けた記事を見落とす確率は上がらない | (pOverlook .fullText).val ≤ (pOverlook .current).val | なし | 0.05 |
| `overlook_full_ge` | 【仮定】 | 置き換えても、引けた記事を見落とす確率は下がらない | (pOverlook .current).val ≤ (pOverlook .fullText).val | なし | 0.05 |
| `searches_tuned_ge` | 【仮定】 | 安い設定の変更をしても、1人1日の探し物の回数は減らない | searchesPerDay .current ≤ searchesPerDay .tuned | なし | 0.05 |
| `found_tuned_ge` | 【仮定】 | 安い設定の変更をしても、見つかった探し物1回の時間は縮まない | foundMinutes .current ≤ foundMinutes .tuned | なし | 0.05 |
| `extraNotYet_tuned_ge` | 【仮定】 | 安い設定の変更をしても、層1で見つからなかったときの余分な時間は縮まない | extraNotYetMinutes .current ≤ extraNotYetMinutes .tuned | なし | 0.05 |
| `extraOther_tuned_ge` | 【仮定】 | 安い設定の変更をしても、層2・層3で見つからなかったときの余分な時間は縮まない | extraOtherMinutes .current ≤ extraOtherMinutes .tuned | なし | 0.05 |
| `noHit_tuned_ge` | 【仮定】 | 安い設定の変更をしても、語で引けない確率は下がらない | (pNoHit .current).val ≤ (pNoHit .tuned).val | なし | 0.05 |
| `overlook_tuned_ge` | 【仮定】 | 安い設定の変更をしても、見落とす確率は下がらない | (pOverlook .current).val ≤ (pOverlook .tuned).val | なし | 0.05 |
| `current_not_incremental` | 【仮定】 | いまの検索の仕組みは、記事を保存するたびに、その記事だけを索引に足すことができない | ¬ CurrentIncremental | なし | 0.05 |
| `tuned_slow_of_rebuild` | 【仮定】 | いまの仕組みが保存のたびに索引へ足せないなら、300万円より安い設定の変更では、保存から検索に出るまでを8時間（28800秒）より短くできない | ¬ CurrentIncremental → 28800 ≤ indexDelaySec .tuned | なし | 0.05 |
| `gain_ge_wage` | 【仮定】 | 置き換えで会社が得る値打ちは、安い設定の変更に比べて取り戻せる時間の人件費を下回らない | savedOverTunedWageYen ≤ gainYen | なし | 0.05 |

### 4.5 論拠・弱い点・要ファクト・向き（docstring に写す）

**estimate_eq**（【実験】）
論拠: 移行の初年度費用の見積もりは300万円（F4）。estimate.md は、この見積もりが構築と移行作業を含むと書く。
弱い点: 金額はユーザーの証言で、見積書はユーザーの手元にある（F4 の notes）。
Writer への注: 1周目の cost_eq の確信度は、Reviewer が 0.6 から 0.3 に下げた。理由は「F4 が支えるのは見積もりの額まで」だった。この公理は、F4 が支えるその部分だけを切り出したものなので、値は F4 の値（0.6）になる。残りの判断（実際の費用は見積もりを超えない）は cost_le_estimate（0.05）に移る。費用の経路の確信度は 0.3 から 0.05 に下がる。下げられた値を戻す変更ではない。

**cost_le_estimate**（【仮定】）
@support なし（見積もりが、初年度に追加で要る費用のすべてを含むことを述べた事実はない。F4 は額だけを述べる）
論拠: estimate.md は、見積もりが構築と移行作業を含むと書く。主な費用は見積もりに入っている。
弱い点: 社内の担当者の作業時間や、運用の費用（サーバー、保守、使用料）が入っているかは分からない。実際の費用が見積もりを超えることもある。
要ファクト: 見積書で、費用に含まれる範囲（社内の作業時間、運用の費用、使用料）を確かめる。estimate.md の「構築と移行作業を含む」を事実として登録する。
向き: 新方式に有利。見積もりを超える分を見込まない。

**searchesPerDay_nonneg**（【自明】）
論拠: 回数は負にならない。

**fullText_complete**（【仮定】）
@support なし（移行の前後で、記事数と閲覧の権限を突き合わせた記録はない）
論拠: 移行の作業には、記事と閲覧の権限を移すことが含まれる（estimate.md の「移行作業」）。
弱い点: 本番の記事は約3万件ある（trial.md）。移行で記事や添付、閲覧の権限が欠けると、その記事は遅れによらず検索に出ない。
要ファクト: 移行の試験で、移行の前後の記事数と閲覧の権限を突き合わせる。
向き: 新方式に有利。新方式だけに起こる失敗を見込まない。

**extraNotYet_current_ge**（【仮定】。旧名 missExtra_current_ge）
@support なし（層1で見つからなかったときの余分な時間を聞いた記録はない）
論拠: 当日の記事が検索に出ないときは、出ていないと気づくまで、語を変えて何度も探し直す。
弱い点: 5分は案の値。早くあきらめて書いた人に聞けば、検索で使う時間は短い（そのあと人に聞く時間は、モデルの時間に入らない）。
要ファクト: アンケートか聞き取りで、「当日の記事が検索に出なかったとき、検索に余分に何分使ったか」を聞く。見つからなかったとき全般ではなく、層1の失敗に向けて聞く。
向き: 量の仮定。大きいほど新方式に有利。

**extraNotYet_nonneg**（【仮定】）
@support なし（同上）
論拠: 探す記事が出てこないときは、見つかったときより検索に長くかかる。
弱い点: 検索で使う時間だけを数えるので、すぐにあきらめれば、見つかったとき（記事を開いて読む時間を含む）より短いことがある。
要ファクト: extraNotYet_current_ge と同じ聞き取りで確かめる。
向き: 符号だけの仮定。extraNotYet_current_ge から導けるが、不利な結論の定理が「5分以上」という量の仮定を通らずに済むように、別に置く。
Writer への注: 主張の側の証明では、この公理を使わず、符号は extraNotYet_current_ge から出す。不利な結論の側の証明では、extraNotYet_current_ge を使わず、この公理を使う。

**extraOther_nonneg**（【仮定】）
@support なし（層2・層3で見つからなかったときの余分な時間を聞いた記録はない）
論拠: 語が合わないときや見落としたときも、見つかるまでより長く探す。
弱い点: すぐにあきらめれば、見つかったときより短いことがある。
要ファクト: 見つからなかったときの余分な時間を、理由（当日の記事か、語が合わないか、見落としか）ごとに聞く。
向き: 符号だけの仮定。主張の側と不利な結論の側の両方で、積の大小をそろえるために使う。

**extraOther_le_notYet**（【仮定】）
@support なし（同上）
論拠: 語が合わないときや見落としたときは、語を変えれば見つかることが多い。当日の記事は、どう探しても出てこないので、探し直しが長くなる。
弱い点: 語を変えても見つからず、長く探し続けることもある。
要ファクト: extraOther_nonneg と同じ聞き取りで、2つの時間を比べる。
向き: 新方式に有利。置き換えで層1の失敗が減ると、その一部は層2・層3の失敗に移る（記事は出るが、語で引けない、見落とす）。その分の余分な時間を小さく見る。

**searches_full_le・searches_full_ge**（【仮定】2つ。@support なし（試験導入の前後で検索の回数を比べた記録はない））
論拠（2つに共通）: 探し物の回数は仕事の中身で決まり、検索の仕組みでは大きく変わらない。
要ファクト（共通）: 試験導入の前後で、1人1日あたりの検索の回数を比べる。
searches_full_le の弱い点: 検索が役に立つようになると、人に聞く代わりに検索を使う回数が増える。向き: 新方式に有利（主張の側が使う）。
searches_full_ge の弱い点: 探し直しが減れば、回数は減る。向き: 新方式に不利（不利な結論の定理だけが使う）。

**found_full_le・found_full_ge**（【仮定】2つ。@support なし（同じ探し物にかかる時間を2つの方式で測った記録はない））
論拠（共通）: 見つかった後に記事を開いて読む時間は、記事で決まる。
要ファクト（共通）: 試験環境で、同じ探し物にかかる時間を2つの方式で測る。
found_full_le の弱い点: 本文の語でも引けると結果が増え、選ぶ時間が延びる。向き: 新方式に有利。
found_full_ge の弱い点: 並びがよくなれば、見つかるまでが短くなる。向き: 新方式に不利。

**extraNotYet_full_le・extraNotYet_full_ge**（【仮定】2つ。@support なし（層1で見つからなかったときの時間を2つの方式で比べた記録はない））
論拠（共通）: 当日の記事が出ないときの探し直し方は、検索の仕組みに依らない。
弱い点（共通）: 置き換えた後は層1の失敗がまれ（0.1%以下）なので、この時間が効くのはその分だけである。
要ファクト（共通）: extraNotYet_current_ge と同じ聞き取り。
向き: extraNotYet_full_le は新方式に有利、extraNotYet_full_ge は新方式に不利。

**extraOther_full_le・extraOther_full_ge**（【仮定】2つ。@support なし（見つからなかったときの探し直しの時間を2つの方式で比べた記録はない））
論拠（共通）: 語が合わないときや見落としたときの探し直し方は、検索の仕組みで大きく変わらない。
要ファクト（共通）: 試験環境で、見つからなかったときの探し直しの時間を2つの方式で比べる。
extraOther_full_le の弱い点: 結果が増えると、探し直しで結果を見直す時間が延びる。向き: 新方式に有利。
extraOther_full_ge の弱い点: 本文の語でも引けると、探し直しが早く済む。向き: 新方式に不利。

**noHit_full_le**（【仮定】。@support なし（同じ検索語で2つの方式を比べた記録はない））
論拠: 全文検索エンジンは、本文の語でも引ける。いまの検索が本文の語で引けないなら、置き換えで下がる。いまの検索も本文の語で引ける（03-reader.json は「いまの検索の仕組み」を Elasticsearch の言い換えとしている）なら、同じ程度になる。どちらでも上がりはしない、とみなす。
弱い点: 置き換えた後は、その日に書かれた新しい記事も索引に入る。新しい記事ほど語で引けにくい（題名や使う語が固まっていない）なら、索引に入っている記事のうちで引けない割合は上がる。1周目は miss_compose の弱い点に書いていたこの重なりを、ここに移した。語の切り方しだいで、「言葉が少し違うと見つからない」（survey-2026.md の設問6で回答者の35%）が増えることもある。
要ファクト: 同じ検索語の組を試験環境で2つの方式に入れ、引けた割合を、新しい記事と古い記事に分けて比べる。
向き: 新方式に有利（主張の側が使う）。

**noHit_full_ge**（【仮定】。@support なし（同じ検索語で2つの方式を比べた記録はない））
論拠: 事実がないので、置き換えで語で引けるようになる分を見込まない。
弱い点: いまの検索が本文の語で引けないなら、置き換えで層2はよくなり、この公理は崩れる。そのときは効果が層1の外からも生まれ、不利な結論 unfav_saved_le_gap は示せなくなる（新方式に有利な向きに外れる）。
要ファクト: いまの検索の仕組みが本文の語で引けるかを、情報システム部に確かめる（R2）。noHit_full_le と同じ比べ方もする。
向き: 新方式に不利（不利な結論の定理だけが使う）。

**overlook_full_le・overlook_full_ge**（【仮定】2つ。@support なし（同じ探し物で見落としを2つの方式で比べた記録はない））
要ファクト（共通）: 試験環境で社員に同じ探し物をしてもらい、結果の中から見つけられた割合を2つの方式で比べる。
overlook_full_le の論拠: 結果の並びの見やすさは、画面で決まる。弱い点: 本文の語でも引けると結果が増え、見落としが増える。「検索結果の並び順が役に立たない」は、設問6で回答者の22%。向き: 新方式に有利。
overlook_full_ge の論拠: 事実がないので、並びがよくなる分を見込まない。弱い点: 全文検索エンジンの並び（語の合い方の強い順）で見落としが減るなら崩れる。向き: 新方式に不利。

**searches_tuned_ge・found_tuned_ge・extraNotYet_tuned_ge・extraOther_tuned_ge・noHit_tuned_ge・overlook_tuned_ge**（【仮定】6つ。@support なし（設定の変更で何が変わるかを確かめた記録はない））
論拠（6つに共通）: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
要ファクト（共通）: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き（共通）: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。
弱い点（個別）:
searches_tuned_ge は、当日の記事が見つかるようになって探し直しが減れば、回数が減る。
found_tuned_ge は、設定の変更と同時に並びの設定も直せば、短くなる。
extraNotYet_tuned_ge は、遅れが短くなって「もう少し待てば出る」と分かれば、探し直しが短くなる。
extraOther_tuned_ge は、設定の変更と同時に語の引き方や並びの設定も直せば、短くなる。
noHit_tuned_ge は、設定の変更と同時に語の切り方（辞書）も直せば、下がる。
overlook_tuned_ge は、設定の変更と同時に並びの設定も直せば、下がる。

**current_not_incremental**（【仮定】）
@support なし（いまの検索の仕組みの種類と、索引の更新の仕方を確かめた記録はない）
論拠: 02-context/sources.md の聞き取りメモは「いまの検索は、夜間に1回だけ索引を作り直している」と書く。保存のたびに索引へ足せるなら、作り直しを待つ必要はない。
弱い点: 03-reader.json の avoid_terms は、Elasticsearch を「いまの検索の仕組み」に言い換えるよう指定している。いまの仕組みが Elasticsearch なら、記事ごとに索引へ足せるのが普通で、この公理は誤りになる（棄却の候補）。夜間の作り直しは、仕組みの制約ではなく、設定かもしれない。03-reader.json と聞き取りメモは 06-facts.json の事実ではないので、@against にも @support にも置けない。
要ファクト: いまの検索の仕組みが何か（Elasticsearch か）、記事を保存のたびに索引へ足す設定があるか、夜間に作り直している理由を、情報システム部に確かめる。聞き取りメモの「夜間に1回だけ索引を作り直している」を事実として登録する。
向き: C0 に有利。

**tuned_slow_of_rebuild**（【仮定】）
@support なし（作り直しにかかる時間と、間隔を短くする費用を確かめた記録はない）
論拠: 索引の丸ごとの作り直しには時間と負荷がかかるので、勤務時間中に何度も回せない。
弱い点: 本番の記事は約3万件（trial.md）で、作り直しが数分で済むなら、1時間おきにも回せる。そうなら、安い設定の変更で当日の記事の問題（層1）のほとんどが解け、C0 は示せなくなる。
要ファクト: 作り直し1回にかかる時間と負荷、勤務時間中に回せるか、間隔を短くする費用を、情報システム部に確かめる。
向き: C0 に有利。

**gain_ge_wage**（【仮定】）
@support なし（取り戻した時間を会社の値打ちとして数える基準を確かめた記録はない）
論拠: 会社は社員の時間に人件費を払っている。取り戻した時間がほかの仕事に使われれば、少なくとも人件費の分の値打ちを生む。
弱い点: 取り戻せる時間は1人1日約1.3分で、細切れの時間はほかの仕事に回らないことがある。費用対効果に厳しい読者（03-reader.json）が、最初に尋ねうる点である。
要ファクト: 社内のほかの投資の判断で、節約した時間を人件費で金額に直しているか、部会がその換算を認めるかを、ユーザーに確かめる。
向き: 新方式に有利。

**approvable_of_net**（【仮定】。型を変える）
@support なし（部会での予算の判断の基準を確かめた記録はない）
論拠: 読者は費用対効果に厳しく、承認するかどうかを判断できることを求めている（03-reader.json）。gainYen は安い設定の変更に比べた値打ちなので、「もっと安い方法で足りるのでは」という問いにも答えている。安い設定の変更の費用（0円以上）を差し引かずに比べるので、差額で比べるより厳しい比べ方になる。
弱い点: 03-reader.json は読者像で、06-facts.json の事実ではない。予算の枠や、ほかの案件との優先度で判断が変わりうる。
要ファクト: 部会での予算の判断の基準（費用対効果のほかに、予算の枠や優先度があるか）を、ユーザーに確かめる。
向き: 新方式に有利（判断の基準）。

**search_decomp**（【自明】。型を変える）
論拠: foundMinutes を「見つかった探し物1回の平均の時間」、それに extraNotYetMinutes を足したものを「層1で見つからなかった探し物1回の平均の時間」、extraOtherMinutes を足したものを「層2・層3で見つからなかった探し物1回の平均の時間」と決めれば、全確率の公式でそのまま成り立つ。層1で見つからない確率は pNotYet、層2・層3で見つからない確率は missProb − pNotYet で、2つは重ならない。

**miss_compose**（【自明】に変える。型は変えない）
論拠: pNoHit を「索引に入っている記事のうち、語で引けない割合」、pOverlook を「引けた記事のうち、見落とす割合」という条件付きの確率として宣言した（3.1節）。見つかるのは、索引に入っていて、語で引けて、見落とさないときだけなので、見つかる確率 =（1 − 層1）×（1 − 層2）×（1 − 層3）は、確率の連鎖律そのものである。3つの層が独立だという判断は要らない。
Writer への注: @support・@confidence・弱い点・要ファクトの行は消す。1周目の弱い点（新しい記事ほど語で引けにくい、という重なり）は、方式によって条件付きの確率が変わる、という判断として noHit_full_le の弱い点に移した。この変更で上がる主張の確信度はない（どの主張も、ほかの 0.05 の公理に頼る）。手戻りの一覧からは1つ減る。

**notYet_le_of_fast**（前提を1つ足す）
弱い点に足す: 移行で欠けた記事は、遅れによらず検索に出ない。その分は前提の IndexComplete に分け、fullText_complete に置いた。
ほかの論拠・弱い点・要ファクト・向きは、1周目のまま。

**search_current_eq**（docstring だけ）
論拠: 社内アンケート2026の設問5「検索で探し物をするのに、1日に何分くらい使っていますか」の、回答者412名の平均が20分（survey-2026.md）。設問の範囲は「検索で探し物をする時間」で、searchMinutes の範囲（3.1節で、検索で使う時間に限った）と同じ。
弱い点: 自己申告の平均。中央値は15分で、長く答えた人が平均を引き上げている。検索の外でほかの場所を探す時間や、人に聞いて待つ時間は、設問にもモデルにも入らない（新方式に不利な向き）。
Writer への注: @confidence 0.75 と @reviewer の行は、消したり書き換えたりしない。範囲が合ったかは、Reviewer が設問5の文面で確かめる。

**delay_current_ge_workday**（docstring だけ）
弱い点に足す: 聞き取りメモ（sources.md）は、「昨日書いた手順が検索で見つからない」という問い合わせが続いたと書く。夜間に作り直しているなら、昨日の記事は今日には検索に出るはずで、食い違う。原因は、作り直しの失敗か、層2・層3（語で引けない、並びで埋もれる）かもしれない。
要ファクト（書き直す）: 聞き取りメモの「いまの検索は、夜間に1回だけ索引を作り直している」を事実として登録し、設定で確かめる（登録すれば @support に足せる）。「昨日書いた手順が見つからない」の原因を、問い合わせの記録で確かめる。
Writer への注: @confidence 0.3 と @reviewer の行は、そのまま残す。

**notYet_ge_of_slow**（docstring だけ）
命題の「どの方式でも」に、tuned が入ることを書く。論拠は1周目のまま。
弱い点に足す: 結論が崩れる境目は、ほかの値をいまの案のままにすると約5.8%（current と比べる C3 でも、tuned と比べる C0 でも同じ）。「昨日書いた手順が見つからない」の原因が層2・層3なら、その日の記事を探す割合は10%を下回りうる。
要ファクトに足す: 問い合わせの原因を確かめる（delay_current_ge_workday と同じ）。
向き: 中立（どの方式にも同じ形で当てはめる）。ただし10%という量は、大きいほど新方式に有利。

**prodDelay_le_test**（docstring だけ）
論拠に足す: 試験環境は「本番と同じ構成」（trial.md）で、違うのは記事の数だけである。
要ファクトに足す: 本番の記事数（約3万件、trial.md）の環境で測る。trial.md の「本番と同じ構成」を事実として登録する。

**beneficiaries_ge**（docstring だけ）
論拠に足す: アンケートの対象は全社員480名で、回答者は412名（survey-2026.md）。回答者だけを数えるのは、新方式に不利な向きの置き方である。

**workDays_ge**（docstring だけ。型は変えない）
命題: 初年度のうち、置き換えた検索を使える勤務日数は200日以上。
論拠: 年間の勤務日数は200日より多い。移行の期間を差し引いても、200日を下回らない見込み。
弱い点: 移行に2か月ほどかかれば、200日を下回りうる。
要ファクト: 会社の年間の所定労働日数と、移行にかかる期間を確かめる。
向き: 新方式に有利。1周目は「控えめな値」としていたが、比べているのは初年度の費用と初年度の効果で、移行の期間の分だけ日数は減る（R8）。

**noHit_current_le**（docstring だけ）
命題の読み: 索引に入っている記事のうちで、語で引けない割合（条件付きの確率）。
弱い点に足す: survey-2026.md の設問6で、回答者の35%が「言葉が少し違うと見つからない」を挙げた。回答者に占める割合で、探し物1回あたりの割合ではない。

**overlook_current_le**（docstring だけ）
命題の読み: 引けた記事のうちで、見落とす割合（条件付きの確率）。
弱い点に足す: survey-2026.md の設問6で、回答者の22%が「検索結果の並び順が役に立たない」を挙げた。回答者に占める割合で、探し物1回あたりの割合ではない。

## 5. 4節（「同じとみなす」置き方）の置き直し

model-plan.md の4節の表を、次の表に置き換える。公理ごとの論拠と弱い点は 4.5節にある。

| 置き方 | 公理 | 向き | 使う定理 |
|---|---|---|---|
| 置き換えは、層1のほかの点で悪くならない | searches_full_le・found_full_le・extraNotYet_full_le・extraOther_full_le・noHit_full_le・overlook_full_le | 新方式に有利 | 主張の側（saved_ge_gap から claim_C3_saved と claim_C0_approvable まで） |
| 置き換えは、層1のほかの点でよくならない | searches_full_ge・found_full_ge・extraNotYet_full_ge・extraOther_full_ge・noHit_full_ge・overlook_full_ge | 新方式に不利 | 不利な結論の定理だけ（unfav_saved_le_gap は6つ、unfav_saved_le_lost はそのうち4つ） |
| 安い設定の変更は、層1のほかの点でよくならない | searches_tuned_ge・found_tuned_ge・extraNotYet_tuned_ge・extraOther_tuned_ge・noHit_tuned_ge・overlook_tuned_ge | C0 に有利 | C0 の側だけ（savedOverTuned_ge_gap から claim_C0_approvable まで） |
| 探す記事の新しさは、方式に依らない | notYet_ge_of_slow・notYet_le_of_fast（どの方式にも同じ形で当てはめる） | 中立 | 両方の側 |

向きの片寄りの確かめ（1周目の「有利な向きに1つ片寄っている」を数え直した）:

- 主張の側（C3 の読み b と C0）が使う「同じとみなす」置き方は、すべて新方式に有利な片側である。主張は下限を示すので、こうなる。1周目は、等式を片側ごとに数えていなかったので、片寄りを小さく見積もっていた。
- 「同じとみなす」置き方の外で、有利な向きに置いたもの: cost_le_estimate、gain_ge_wage、workDays_ge、prodDelay_le_test、fullText_complete、extraOther_le_notYet、current_not_incremental、tuned_slow_of_rebuild、approvable_of_net。1周目は、このうち費用・人件費の換算・日数を、数えていないか「不利」と数えていた（R8）。
- 不利な向きに置いたもの: beneficiaries_ge（480名のうち回答者の412名だけを数える）、時間を「検索で使う時間」に限ったこと（3.1節）、いまの検索の維持費を差し引かない firstYearCost、安い設定の変更の費用を差し引かない approvable_of_net。
- miss_compose は【自明】にしたので、向きを持たない。1周目に「独立とみなすのは不利な向き」と数えたのは、排反と比べたときだけの話で、誤りだった（R8）。重なりの懸念は、noHit_full_le（有利な片側）の弱い点に移った。
- 符号だけの仮定（extraNotYet_nonneg、extraOther_nonneg）は、向きを数えない。
- まとめ: 主張の値は、有利な向きの仮定に片寄っている。これを隠さず、ステージ6で先に確かめる順（10節）に反映した。

## 6. 5節（定理の計画）の変更

### 6.1 定理ごとの変更

| 定理 | 変化 | 示すこと | 使う判断（関係公理と、途中の定理） | 種類 |
|---|---|---|---|---|
| `notYet_tuned_ge` | 新設（印なし） | 安い設定の変更をしても、まだ検索に出ていない記事を探す確率は 1/10 以上 | current_not_incremental・tuned_slow_of_rebuild・notYet_ge_of_slow | [確率] |
| `notYet_fullText_le` | 使う判断を変える（示すことは同じ） | 置き換えた後、まだ検索に出ていない記事を探す確率は 1/1000 以下 | testDelay_le_five・prodDelay_le_test・fullText_complete・notYet_le_of_fast | [確率] |
| `miss_current_ge` | 削除 | lost_ge が使わなくなった | — | — |
| `lost_ge` | 証明を変える（示すことは同じ: 2 ≤ lostMinutes） | 失われている時間（読み a）は1人1日2分以上。4回 × 1/10 × 5分で、層2・層3の分は0以上なので落とす | searches_current_ge・notYet_current_ge・extraNotYet_current_ge・extraOther_nonneg・miss_compose | [確率] |
| `saved_only_from_notYet` | 削除 | 等式は、主張が使う片側と不利な結論が使う片側を1つにしていた（R9）。下限の saved_ge_gap と、上界の unfav_saved_le_gap に分ける | — | — |
| `saved_ge_gap` | 新設（印なし） | searchesPerDay .current ×（pNotYet .current の値 − pNotYet .fullText の値）×（extraNotYetMinutes .current − missAfterIndex .current × extraOtherMinutes .current）≤ savedMinutes | search_decomp・miss_compose・searchesPerDay_nonneg・foundMinutes_nonneg・searches_full_le・found_full_le・extraNotYet_full_le・extraOther_full_le・noHit_full_le・overlook_full_le・extraNotYet_current_ge（符号だけ）・extraOther_nonneg | [確率] |
| `saved_ge` | 使う判断を変える（示すことは同じ: 792/625 ≤ savedMinutes） | 取り戻せる時間（読み b）は1人1日1.2672分以上。4回 × 99/1000 ×（16/25 × 5分） | saved_ge_gap・searches_current_ge・extraNotYet_current_ge・extraOther_le_notYet・extraOther_nonneg・noHit_current_le・overlook_current_le・notYet_current_ge・notYet_fullText_le | [確率] |
| `savedOverTuned_ge_gap` | 新設（印なし） | searchesPerDay .current ×（pNotYet .tuned の値 − pNotYet .fullText の値）×（extraNotYetMinutes .current − missAfterIndex .current × extraOtherMinutes .current）≤ savedOverTunedMinutes | saved_ge_gap と同じ判断に、searches_tuned_ge・found_tuned_ge・extraNotYet_tuned_ge・extraOther_tuned_ge・noHit_tuned_ge・overlook_tuned_ge を足したもの | [確率] |
| `savedOverTuned_ge` | 新設（印なし） | 安い設定の変更に比べて取り戻せる時間は、1人1日1.2672分以上 | savedOverTuned_ge_gap・searches_current_ge・extraNotYet_current_ge・extraOther_le_notYet・extraOther_nonneg・noHit_current_le・overlook_current_le・notYet_tuned_ge・notYet_fullText_le | [確率] |
| `yenPerDailyMinute_ge` | docstring の「1年で」を「初年度に」に変える | 4,120,000円以上 | 変えない（beneficiaries_ge・workDays_ge・wage_ge） | [決定論] |
| `claim_C3_saved` | 型と使う判断を変える（@claim C3） | firstYearCost < savedWageYen | cost_le_estimate・estimate_eq・yenPerDailyMinute_ge・saved_ge | [確率] |
| `claim_C3_lost` | 型と使う判断を変える（@claim C3） | firstYearCost < lostWageYen | cost_le_estimate・estimate_eq・yenPerDailyMinute_ge・lost_ge | [確率] |
| `claim_C0_approvable` | 使う判断を変える（@claim C0。型は Approvable のまま） | 来期予算で300万円を承認する理由がそろう。firstYearCost ≤ 300万円 < 5,220,864円 ≤ savedOverTunedWageYen ≤ gainYen から、approvable_of_net で示す。claim_C3_saved は使わない | approvable_of_net・gain_ge_wage・cost_le_estimate・estimate_eq・yenPerDailyMinute_ge・savedOverTuned_ge | [確率] |
| `baseline_lost_le_survey` | 使う判断を変える（@baseline。示すことは同じ: lostMinutes ≤ 20） | いまの検索の失われている時間を、アンケートの20分より大きく置いていない。lostMinutes = 20 − 回数 × 見つかった場合の時間 | search_current_eq・search_decomp・foundMinutes_nonneg・searchesPerDay_nonneg（1周目の searches_current_ge は使わない） | [決定論] |
| `unfav_saved_le_gap` | 新設（印なし。docstring の先頭に [不利]） | savedMinutes ≤ searchesPerDay .current ×（pNotYet .current の値 − pNotYet .fullText の値）×（extraNotYetMinutes .current − missAfterIndex .current × extraOtherMinutes .current） | search_decomp・miss_compose・searchesPerDay_nonneg・foundMinutes_nonneg・searches_full_ge・found_full_ge・extraNotYet_full_ge・extraOther_full_ge・noHit_full_ge・overlook_full_ge・extraNotYet_nonneg・extraOther_nonneg | [不利] |
| `unfav_saved_le_lost` | 使う判断を変える（示すことは同じ: savedMinutes ≤ lostMinutes） | 取り戻せる時間は、失われている時間を超えない | search_decomp・miss_compose・searchesPerDay_nonneg・foundMinutes_nonneg・searches_full_ge・found_full_ge・extraNotYet_full_ge・extraOther_full_ge・extraNotYet_nonneg・extraOther_nonneg | [不利] |

変えない定理: notYet_current_ge、claim_C1_many、claim_C2_soon、claim_C2_faster、unfav_saved_le_survey（[不利] のまま）、数の補題 rat_mul_le_mul。

Writer への注（証明の道筋。3節の公理だけで示せることを確かめた）:

- miss_compose から、missProb M の値 − pNotYet M の値 =（1 − pNotYet M の値）× missAfterIndex M が、式の変形で出る。これを search_decomp に入れると、searchMinutes M = 回数 ×（見つかった場合の時間 ＋ 層1の確率 × 層1の余分な時間 ＋（1 − 層1の確率）× missAfterIndex M × 層2・層3の余分な時間）になる。
- saved_ge_gap: fullText の各量を、片側の公理で current の値に置き換えた上界を作る。missAfterIndex .fullText ≤ missAfterIndex .current は、noHit_full_le・overlook_full_le と Prob の範囲から出る。積の大小には、符号（searchesPerDay_nonneg、foundMinutes_nonneg、extraOther_nonneg、extraNotYet_current_ge から出る 0 ≤ extraNotYetMinutes .current）が要る。上界を searchMinutes .current から引くと、下限の式になる。
- savedOverTuned_ge_gap: tuned の側は、tuned の6つの片側の公理で、current の値に置き換えた下界を作る（向きは fullText と逆）。fullText の側は saved_ge_gap と同じ上界を使う。
- saved_ge と savedOverTuned_ge: extraOther_le_notYet と missAfterIndex .current ≥ 0 から、（extraNotYetMinutes − missAfterIndex × extraOtherMinutes）≥（1 − missAfterIndex）× extraNotYetMinutes。1 − missAfterIndex .current ≥ 16/25 は noHit_current_le・overlook_current_le から出る。
- unfav_saved_le_gap: saved_ge_gap の向きを逆にしたもの。fullText の各量を、_full_ge の公理で current の値に置き換えた下界を作る。符号は extraNotYet_nonneg と extraOther_nonneg から出し、extraNotYet_current_ge は使わない。
- unfav_saved_le_lost: savedMinutes ≤ lostMinutes は、回数(current) × 見つかった場合の時間(current) ≤ searchMinutes .fullText と同じ。searches_full_ge・found_full_ge・extraNotYet_full_ge・extraOther_full_ge と符号から出る。
- 積の単調性は grind で解けないので、rat_mul_le_mul などの補題で示す（lean-modeling.md）。

### 6.2 計算の値（Reviewer が、CLI の値や証人と照らすため）

| 量 | 値 | 費用（300万円）との比 |
|---|---|---|
| yenPerDailyMinute の下限 | 4,120,000円 | — |
| lostMinutes の下限 | 2分。lostWageYen は 8,240,000円以上 | 約2.7倍 |
| savedMinutes の下限 | 1.2672分。savedWageYen は 5,220,864円以上 | 約1.74倍 |
| savedOverTunedMinutes の下限 | 1.2672分。savedOverTunedWageYen は 5,220,864円以上 | 約1.74倍 |
| 結論が崩れる境目（取り戻せる時間） | 1人1日 約0.728分（約44秒） | — |
| 結論が崩れる境目（層1） | ほかの値をいまの案のままにすると、取り戻せる時間の初年度の人件費は 4,120,000円 × 4回 × 5分 × 16/25 ×（層1の差）= 52,736,000円 ×（層1の差）になる。これが300万円を超えるには、層1の差が約5.69%より大きいこと、つまり current（C3）か tuned（C0）の層1の確率が約5.8%より大きいことが要る | — |

### 6.3 証人の値（Writer が Model.lean を書くときの参考）

| 量 | current | tuned | fullText |
|---|---|---|---|
| indexDelaySec（秒） | 86400 | 86400 | 4.2 |
| pNotYet | 1/10 | 1/10 | 1/1000 |
| pNoHit・pOverlook | 1/5 | 1/5 | 1/5 |
| missProb | 53/125 | 53/125 | 1127/3125 |
| searchesPerDay（回） | 4 | 4 | 4 |
| foundMinutes（分） | 72/25 | 72/25 | 72/25 |
| extraNotYetMinutes・extraOtherMinutes（分） | 5 | 5 | 5 |
| searchMinutes（分。search_decomp の式で計算） | 20 | 20 | 18.7328 |
| IndexComplete | 真 | 真 | 真 |

- 方式によらない量: testDelaySec 4.2、beneficiaries 412、workDays 200、wagePerHour 3000、estimateYen 3,000,000、firstYearCost 3,000,000、manyMinutes 20、gainYen 5,220,864。CurrentIncremental は偽。
- 計算の値: savedMinutes と savedOverTunedMinutes は 1.2672、lostMinutes は 4 ×（1/10 × 5 ＋ 81/250 × 5）= 8.48、missAfterIndex はどの方式でも 9/25。
- Approvable は、firstYearCost < gainYen と定義する（R13。11節）。

## 7. 6節（比べる相手と、予想される不利な結論）の変更

比べる相手:

- C3 の比べる相手は、いまのまま（current）で変えない。確認の定理 baseline_lost_le_survey も残す（使う判断だけ変える）。
- C0 の比べる相手を、いまの仕組みのままでできる、300万円より安い設定の変更（tuned）にする。1周目は「3つ目の方式としては入れない」としたが、R1 のとおり、効果は層1の差からしか生まれない。安い案を遅れの量で層1の確率につながないと、「もっと安い方法はない」が藁人形になる。tuned を方式に足せば、∀ M の公理（notYet_ge_of_slow など）がそのまま当たるので、層1の確率へのつながりに新しい公理が要らない。
- 安い案の境目は8時間で、notYet_ge_of_slow の境目と同じにした。安い案が8時間以上なら、層1の失敗はいまと同じ下限（10%以上）で残る。8時間未満にできるなら、tuned_slow_of_rebuild が誤りになり、C0 は示せなくなる。遅れの値の範囲を隙間なく2つに分けるので、「5秒に届かない安い案は代わりにならない」という隠れた判断はなくなる。
- tuned が藁人形でないことは、tuned の定義（300万円より安い変更のうち、いちばん速いもの）と、その速さについての2つの【仮定】（current_not_incremental、tuned_slow_of_rebuild）で決まる。@baseline の定理は置かない。確かめる中身がこの2つの【仮定】そのもので、定理にしても言い換えになるからである。

予想される不利な結論（1周目の6節の一覧を置き換える）:

1. 取り戻せる時間は、層1の差に比例する分を超えない（unfav_saved_le_gap。[不利]）。層1の差が縮めば、効果もそれだけ縮む。安い設定の変更で層1の差が縮めば、置き換えの効果もそれだけ小さい。主張の側が使う有利な片側（_full_le）も、量の仮定（4回、5分、10%）も通らない。
2. 取り戻せる時間は、失われている時間を超えない（unfav_saved_le_lost。[不利]）。C3 を読み (a) で費用と比べると、効果を大きく見せることになる。本文では読み (b) の数字を使う。
3. 取り戻せる時間は、1日20分を超えない（unfav_saved_le_survey。[不利]。1周目のまま）。
4. 結論には境目がある（6.2節）。取り戻せる時間が1人1日約44秒を下回るか、current や tuned の層1の確率が約5.8%を下回ると、費用に届かない。これは定理にせず、計算の値と notYet_ge_of_slow の弱い点に置く（理由は9節）。
5. C0 の要は、tuned_slow_of_rebuild と current_not_incremental である。いまの仕組みが Elasticsearch で、保存のたびに索引へ足す設定があるなら、C0 は示せない。
6. 主張の値は、置き換えが層1のほかの点で悪くならない、という有利な片側（5節）に頼っている。
7. C2 は本番で確かめていない（1周目のまま）。

## 8. 失敗の台帳（ledger.json）の変更

ledger.json を書き直した。変えたのは次の4つである。

- methods を3つ（current、tuned、fullText）にして、Method のコンストラクタに合わせた。どの行にも3つの欄を書いた。
- 失敗でない量の行（foundMinutes、searchMinutes）を外した（R12）。探し物の回数（searchesPerDay）の行も外した。回数は失敗が起こる機会の数で、失敗そのものではないからである。3つの量の置き方は、5節と6節にある。
- 新方式だけに起こる失敗の行を2つ足した。本番の記事数と負荷で索引の更新が遅れる行と、移行で記事や閲覧の権限が欠ける行である。いまの検索と安い設定の変更の欄には、「起こらない」と理由を書いた。
- 余分な時間の行を、層1で見つからなかったときと、層2・層3で見つからなかったときの2行に分けた（R7）。

## 9. 採らない指摘と、ほかのステージに送る指摘（この節はモデルを変えない）

R9 のうち、「層1の差が0以下なら、取り戻せる時間は0以下」と境目（約5.8%）を定理にする点は、採らない。notYet_current_ge（1/10 以上）と notYet_fullText_le（1/1000 以下）から、前提「層1の差が0以下」は公理から否定できる。境目の前提（層1の確率が約5.8%を下回る）も、notYet_ge_of_slow の10%と食い違う。前提がいつも偽の定理は、何も言っていない（ガイドの「Writer の約束」）。人数や日数の上限の公理を足しても、この空回りは直らない。代わりに、前提を持たない上界 unfav_saved_le_gap を [不利] の定理として置き、境目は 6.2節の計算の値と notYet_ge_of_slow の弱い点に置く。

R2 のうち、「いまの検索は本文の語で引けない（または引ける）」を別の宣言や公理にする点は、採らない。どの定理の筋道にも入らないからである。等式を片側に分けたので、主張の側は noHit_full_le（置き換えで、語で引けない確率は上がらない）だけを使う。この片側のもっともらしさは、いまの検索が本文を引けても引けなくても変わらない。本文を引けるかどうかで崩れうるのは noHit_full_ge（不利な結論の側）で、その弱い点と要ファクトに書いた。どの定理も使わない公理を置くと、ステージ6で確かめても主張の値が動かない。R2 の残りの2つ（いまの仕組みの種類、作り直しの間隔と費用）は、C0 の筋道の上の current_not_incremental と tuned_slow_of_rebuild に置いた。3つ目（昨日書いた手順が見つからない）は、delay_current_ge_workday と notYet_ge_of_slow の弱い点と要ファクトに置いた。

R3・R5 で下げられた確信度は、戻さない。search_current_eq は、設問5の文面に合わせて searchMinutes の範囲を直したが、@reviewer で下げた値を Planner や Writer が戻すことはしない。delay_current_ge_workday は、聞き取りメモを事実として登録するまで上げられない（ステージ6）。

R10（claim_C1_many）は、ステージ5で決める。C1 を数字の文（「社員は検索で探し物をするのに1日平均20分使っている」）に言い換えるなら、many_threshold_le は要らなくなり、claim_C1_many は search_current_eq だけで示せる。モデルは、そのときに直す。

R11（claim_C2_soon の「すぐ」）は、ステージ5で決める。「試験環境では5秒以内」と「本番でも当日中」に分けるなら、そのときに定理を分ける。この周は、testDelaySec の宣言に「20件の最大」と書くだけにした。

R14（目的の「大きく減らせる」）は、ステージ5で決める。モデルの下限は1人1日約1.27分（20分の約6%）で、「大きく」を支える定理はない。本文では、取り戻せる時間を数字で言うか、「大きく」を使わない。

R15 は、素材（survey-2026.md、trial.md、estimate.md）が 02-context に入ったので、引用を確かめられるようになった。06-facts.json の事実の status は変わらない。素材にあって、公理の論拠や要ファクトに引いたが事実として登録されていないものは、ステージ6で登録する（10節）。

R5 の関連で、04-analysis.md は「探し物に1日平均20分」と書き、設問5の「検索で」が落ちている。ステージ11で本文を書くときは、「検索で探し物をするのに」と書く。

## 10. ステージ6で先に確かめる順

Reviewer の C0 の見立て（C3 の量より先に、いまの仕組みについての事実を集める）に合わせた。

1. いまの検索の仕組みについての事実（R2）。いまの仕組みは何か（Elasticsearch か）と、保存のたびに索引へ足せるか（current_not_incremental）。作り直し1回にかかる時間と、間隔を短くする費用（tuned_slow_of_rebuild）。「昨日書いた手順が見つからない」の原因。C0 は、この2つの【仮定】のどちらかが崩れると示せなくなる。
2. その日に保存された記事を探す割合（notYet_ge_of_slow の10%。境目は約5.8%）。
3. 主張の側が使う有利な片側。崩れやすい順に、noHit_full_le（新しい記事ほど語で引けにくい）、overlook_full_le（結果が増えて見落とす）、searches_full_le（回数が増える）。
4. 費用と値打ち（cost_le_estimate、gain_ge_wage、workDays_ge）。
5. 素材にあって、まだ事実として登録していないもの。sources.md の聞き取りメモ（夜間に1回だけ索引を作り直している、昨日書いた手順が見つからない）、survey-2026.md の設問5の中央値15分と設問6の残りの行、trial.md の「本番と同じ構成」と「約3万件」、estimate.md の「構築と移行作業を含む」。

## 11. 証人（Model.lean）の見通し

- Method に tuned が増えるので、方式ごとの値に tuned の値を足す（6.3節の表）。tuned の値は、遅れも含めて current と同じにする。
- CurrentIncremental は偽、IndexComplete はどの方式でも真にする。
- Approvable は、firstYearCost < gainYen と定義する（R13）。これで approvable_of_net は、前提が崩れれば結論も崩れる世界で試される。gainYen を Approvable より前に宣言するので、証人でもこの定義を書ける。
- 前提が成り立つ例: tuned_slow_of_rebuild（CurrentIncremental が偽）、notYet_le_of_fast（fullText で 4.2秒、IndexComplete が真）、notYet_ge_of_slow（current と tuned で 86400秒）、approvable_of_net（3,000,000 < 5,220,864）。
- 主張の定理（claim_C0_approvable、claim_C1_many、claim_C2_soon、claim_C2_faster、claim_C3_saved、claim_C3_lost）は、どれも前提を持たない。
- Argument.lean の冒頭の「主張と定理の対応」「印のない定理」の表と、「設計書（model-plan.md）との違い」を、この差分に合わせて書き直す。

## 12. 数え方

【実験】3、【経験則】2、【自明】5、【仮定】37、合わせて47（1周目は26）。
増えた21の内訳は3つある。

- 等式を片側に分けた。5つの等式を消して12の片側を足したので、7つ増えた。
- 安い設定の変更と比べるための公理を置いた。no_cheaper_fix を消して8つ（current_not_incremental、tuned_slow_of_rebuild と、tuned の片側6つ）を足したので、7つ増えた。
- 費用・値打ち・移行・余分な時間の分け方と、符号の公理を置いた。cost_eq を消して8つ（estimate_eq、cost_le_estimate、gain_ge_wage、fullText_complete、extraNotYet_nonneg、extraOther_nonneg、extraOther_le_notYet、searchesPerDay_nonneg）を足したので、7つ増えた。

数そのものは物差しにしない。
