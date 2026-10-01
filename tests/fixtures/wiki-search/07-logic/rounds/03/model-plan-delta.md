# 差分の設計書（3周目）

前の周の review.md の指摘に答える。`cyrus logic-round diff` は「## 変更」の表の行だけを、差分との対応表に使う。

- この差分に名前の出ない宣言・公理・定理は変えない。model-plan.md や2周目の差分と食い違うところは、この差分に従う。
- 名前は、表の「対象」の列にだけバッククォートで囲んで挙げた。ほかの節では囲まずに書く。
- 「共通」とまとめて書いた論拠・弱い点・要ファクトは、Writer が公理ごとに展開し、docstring には全文を書く。

## 変更

1行に1つの変更。対象の宣言・公理・定理の名前を `名前` の形で必ず挙げる。

| # | 変更 | 対象 | 答える指摘 |
|---|---|---|---|
| 1 | 宣言の名前と意味を変える。「勤務時間中に保存した記事の、いちばん長い遅れ」に決める | `indexDelaySec` → `maxDelaySec` | R16 |
| 2 | 宣言を足す（Method → Prop） | `DaytimeUpdate` | R16 |
| 3 | 宣言を足す（Method → Prob） | `pSameDay` | R16 |
| 4 | 宣言を足す（Method → Prob） | `pStale` | R16 |
| 5 | 宣言の docstring の宣言名を直す | `testDelaySec` | R16 |
| 6 | 公理を消す。current_no_daytime と maxDelay_of_noDaytime に置き換える | `delay_current_ge_workday` | R16・R3 |
| 7 | 公理を消す。notYet_ge_sameDay_stale・stale_of_noDaytime・sameDay_current_ge・sameDay_tuned_ge に置き換える | `notYet_ge_of_slow` | R16 |
| 8 | 公理を消す。tuned_no_daytime_of_rebuild に置き換える | `tuned_slow_of_rebuild` | R16 |
| 9 | 使う宣言の意味が変わったので、名前を変えて別の公理にする | `prodDelay_le_test` → `prodMaxDelay_le_test` | R16 |
| 10 | 同上 | `notYet_le_of_fast` → `notYet_le_of_maxFast` | R16 |
| 11 | 【経験則】を足す | `current_no_daytime` | R16・R3 |
| 12 | 【自明】を足す | `maxDelay_of_noDaytime` | R16 |
| 13 | 【自明】を足す | `stale_of_noDaytime` | R16 |
| 14 | 【自明】を足す | `notYet_ge_sameDay_stale` | R16 |
| 15 | 【仮定】を足す | `sameDay_current_ge` | R16 |
| 16 | 【仮定】を足す（C0 に有利な片側） | `sameDay_tuned_ge` | R16 |
| 17 | 【仮定】を足す | `tuned_no_daytime_of_rebuild` | R16 |
| 18 | 【仮定】を足す（C0 に不利な片側） | `searches_tuned_le` | R17 |
| 19 | 【仮定】を足す（C0 に不利な片側） | `found_tuned_le` | R17 |
| 20 | 【仮定】を足す（C0 に不利な片側） | `extraNotYet_tuned_le` | R17 |
| 21 | 【仮定】を足す（C0 に不利な片側） | `extraOther_tuned_le` | R17 |
| 22 | 【仮定】を足す（C0 に不利な片側） | `noHit_tuned_le` | R17 |
| 23 | 【仮定】を足す（C0 に不利な片側） | `overlook_tuned_le` | R17 |
| 24 | [不利] の定理を足す（印なし） | `unfav_savedOverTuned_le_gap` | R17 |
| 25 | 使う判断を変える（示すことは同じ） | `notYet_current_ge` | R16 |
| 26 | 使う判断を変える（示すことは同じ） | `notYet_tuned_ge` | R16 |
| 27 | 使う公理の名前が変わる | `notYet_fullText_le` | R16 |
| 28 | 型の宣言名と、使う公理の名前が変わる | `claim_C2_soon` | R16 |
| 29 | 型と使う判断を変える | `claim_C2_faster` | R16 |
| 30 | 2周目に使う宣言（searchMinutes）の意味を変えたので、名前を変えて別の公理にする | `search_current_eq` → `searchTime_current_eq` | R20 |
| 31 | 使う公理の名前が変わる | `claim_C1_many` | R20 |
| 32 | 使う公理の名前が変わる | `baseline_lost_le_survey` | R20 |
| 33 | 使う公理の名前が変わる | `unfav_saved_le_survey` | R20 |
| 34 | docstring（弱い点の公理名） | `testDelay_le_five` | R16 |
| 35 | docstring（論拠と弱い点） | `extraNotYet_current_ge` | R8 |
| 36 | docstring（向きと弱い点） | `searches_current_ge` | R8 |
| 37 | docstring（向きと弱い点） | `wage_ge` | R8 |
| 38 | docstring（向き） | `noHit_current_le` | R8 |
| 39 | docstring（向き） | `overlook_current_le` | R8 |
| 40 | docstring（論拠・弱い点・要ファクト） | `approvable_of_net` | R18 |
| 41 | docstring（論拠と弱い点） | `fullText_complete` | 監査の注記（閲覧の権限） |

## 新しい公理・宣言の中身

### 1. R16 の直し方

- 論証が要る条件は「遅れが8時間以上か」ではなく、「勤務時間中に索引を更新するか」である。これを方式ごとの命題 DaytimeUpdate にし、層1の下限をこれにつなぐ。
- 層1の下限は、「その日の記事を探す確率 × その記事がまだ出ていない確率（条件付き）」で下から押さえる（【自明】）。勤務時間中に更新しない方式では、後ろの確率は1になる（【自明】）。
- 遅れの数は、C2 と、置き換えた後の層1の上界だけに残す。読みは「いちばん長い遅れ」の1つに決め、名前を maxDelaySec に変えた。いまの検索の遅れの下限は、DaytimeUpdate から【自明】で出す。
- 安い変更の途中の案（昼に1回だけ作り直す）は、tuned_no_daytime_of_rebuild を偽にする。いまのままと同じ扱いに、黙って入ることはなくなる。途中の案の層1は、この公理の弱い点に数字で書く（4節の境目）。
- Method の tuned の docstring は変えない。tuned は安い変更のうち記事がいちばん早く検索に出るものなので、勤務時間中に1回でも更新できる安い変更があれば、tuned もそうする。この単調性を tuned_no_daytime_of_rebuild の論拠に書き、命題の意味を固定する。_tuned_ge の6つの命題の意味は変わらない。

### 2. 宣言

| 名前 | 型 | 何を表すか（docstring に写す） |
|---|---|---|
| maxDelaySec（旧 indexDelaySec） | Method → Rat | 勤務時間中に保存した記事が、保存から検索に出るまでにかかる時間の、いちばん長い場合（秒）。勤務時間中のどの時刻に保存しても、この時間のうちには検索に出る。移行で欠けて検索に出ない記事は入れない（IndexComplete に分けた） |
| DaytimeUpdate | Method → Prop | その方式では、勤務時間中（1日8時間、28800秒）に索引が更新され、その日の勤務時間中に保存された記事が、同じ日の勤務時間中に検索に出ることがある |
| pSameDay | Method → Prob | 層1の内訳。探し物1回が、勤務時間中の探し物で、しかも同じ日の勤務時間中に（検索より前に）保存された記事を探すものである確率 |
| pStale | Method → Prob | 勤務時間中に、同じ日の勤務時間中に保存された記事を探したとき、検索の時点でその記事がまだ検索に出ていない確率（そうした探し物であることを条件とした、条件付きの確率） |

- testDelaySec の docstring の「本番の indexDelaySec .fullText とは別の量」を、「本番の maxDelaySec .fullText とは別の量」にする。
- DaytimeUpdate は IndexComplete の後、pSameDay と pStale は pNotYet の後に置く。

### 3. 関係公理

| 名前 | 種類 | 命題（日常語） | 型 | 支える事実 | 確信度の案 |
|---|---|---|---|---|---|
| current_no_daytime | 【経験則】 | いまの検索は、勤務時間中に索引を更新しない | ¬ DaytimeUpdate .current | F2 | 0.3 |
| maxDelay_of_noDaytime | 【自明】 | どの方式でも、勤務時間中に索引を更新しないなら、いちばん長い遅れは8時間以上 | ∀ M : Method, ¬ DaytimeUpdate M → 28800 ≤ maxDelaySec M | — | 1 |
| stale_of_noDaytime | 【自明】 | どの方式でも、勤務時間中に索引を更新しないなら、その日の記事をその日に探すと、必ずまだ出ていない | ∀ M : Method, ¬ DaytimeUpdate M → 1 ≤ (pStale M).val | — | 1 |
| notYet_ge_sameDay_stale | 【自明】 | どの方式でも、その日の記事を探し、しかもまだ出ていない確率は、層1の確率を超えない | ∀ M : Method, (pSameDay M).val * (pStale M).val ≤ (pNotYet M).val | — | 1 |
| sameDay_current_ge | 【仮定】 | いまの検索で、その日の記事を勤務時間中に探す探し物は10%以上 | 1 / 10 ≤ (pSameDay .current).val | なし | 0.05 |
| sameDay_tuned_ge | 【仮定】 | 安い設定の変更をしても、その日の記事を探す割合は減らない | (pSameDay .current).val ≤ (pSameDay .tuned).val | なし | 0.05 |
| tuned_no_daytime_of_rebuild | 【仮定】 | いまの仕組みが保存のたびに索引へ足せないなら、300万円より安い設定の変更では、勤務時間中に索引を1回も更新できない | ¬ CurrentIncremental → ¬ DaytimeUpdate .tuned | なし | 0.05 |
| prodMaxDelay_le_test | 【仮定】 | 本番の記事数でも、置き換えた後のいちばん長い遅れは、試験環境の20件の最大を超えない | maxDelaySec .fullText ≤ testDelaySec | なし | 0.05 |
| notYet_le_of_maxFast | 【仮定】 | どの方式でも、いちばん長い遅れが5秒以内で、移行で欠けた記事もないなら、層1は0.1%以下 | ∀ M : Method, maxDelaySec M ≤ 5 → IndexComplete M → (pNotYet M).val ≤ 1 / 1000 | なし | 0.05 |
| searchTime_current_eq | 【実験】 | いまの検索で、社員1人が1日に検索で探し物をするのに使う時間は20分 | searchMinutes .current = 20 | F1 | （事実の値） |
| searches_tuned_le | 【仮定】 | 安い設定の変更をしても、探し物の回数は増えない | searchesPerDay .tuned ≤ searchesPerDay .current | なし | 0.05 |
| found_tuned_le | 【仮定】 | 安い設定の変更をしても、見つかった探し物1回の時間は延びない | foundMinutes .tuned ≤ foundMinutes .current | なし | 0.05 |
| extraNotYet_tuned_le | 【仮定】 | 安い設定の変更をしても、層1で見つからなかったときの余分な時間は延びない | extraNotYetMinutes .tuned ≤ extraNotYetMinutes .current | なし | 0.05 |
| extraOther_tuned_le | 【仮定】 | 安い設定の変更をしても、層2・層3で見つからなかったときの余分な時間は延びない | extraOtherMinutes .tuned ≤ extraOtherMinutes .current | なし | 0.05 |
| noHit_tuned_le | 【仮定】 | 安い設定の変更をしても、語で引けない確率は上がらない | (pNoHit .tuned).val ≤ (pNoHit .current).val | なし | 0.05 |
| overlook_tuned_le | 【仮定】 | 安い設定の変更をしても、見落とす確率は上がらない | (pOverlook .tuned).val ≤ (pOverlook .current).val | なし | 0.05 |

論拠・弱い点・要ファクト・向き（docstring に写す）:

**current_no_daytime**（【経験則】。支える事実 F2、確信度の案 0.3）
論拠: F2 で、不満の理由の1位が「当日の記事が出てこない」（回答者の48%）。勤務時間中に索引を更新していれば、この不満がいちばん多くはならない。
弱い点: F2 は不満の理由で、索引の更新の仕方を述べていない。原因が並び（層3。新しい記事が結果の下のほうに出る）かもしれない。聞き取りメモ（sources.md）の「昨日書いた手順が検索で見つからない」は、夜間に作り直しているなら昨日の記事は今日には出るはずで、食い違う。原因は、作り直しの失敗か、層2・層3かもしれない。
要ファクト: 聞き取りメモの「いまの検索は、夜間に1回だけ索引を作り直している」を事実として登録し、設定で確かめる。登録すれば、この公理を直接支える。「昨日書いた手順が見つからない」の原因を、問い合わせの記録で確かめる。
向き: 新方式に有利（C3 と C0 の層1の下限を決める）。
（案を 0.3 にする理由: 前の周に Reviewer が delay_current_ge_workday を 0.3 に下げた理由「F2 は当日の記事が出ないことが多い、までを支え、原因を分けていない」は、この公理にも当てはまる。この文は docstring に写さない）

**maxDelay_of_noDaytime**（【自明】）
論拠: 勤務時間中に索引を更新しない方式では、勤務の始まりに保存した記事は、勤務が終わるまで検索に出ない。maxDelaySec はどの時刻に保存した場合も含む「いちばん長い場合」で、勤務時間は DaytimeUpdate の宣言で8時間と決めたので、28800秒以上になる。C2 が使うのは、いまの遅れが5秒より長いことだけである。

**stale_of_noDaytime**（【自明】）
論拠: 勤務時間中に索引を更新しない方式では、その日の勤務時間中に保存された記事は、その日の勤務時間中には検索に出ない。pStale は勤務時間中にその日の記事を探す探し物についての確率なので、1になる。型は下側（1 以上）だけを置く。上側は Prob の範囲で決まる。

**notYet_ge_sameDay_stale**（【自明】）
論拠: pSameDay × pStale は、連鎖律で「勤務時間中にその日の記事を探し、しかもその記事がまだ検索に出ていない」確率になる。これは「探す記事が、検索の時点でまだ検索に出ていない」（pNotYet）の一部なので、全体の確率を超えない。

**sameDay_current_ge**（【仮定】。支える事実なし（探し物1回あたりの、その日の記事を探す割合を数えた記録はない））
論拠: F2 で48%が「当日の記事が出てこない」を挙げていて、その日の記事を探すことは珍しくない。
弱い点: F2 は回答者に占める割合で、探し物1回あたりの割合は、どの事実にもない。10%は案の値。結論が崩れる境目は、ほかの値をいまの案のままにすると約5.8%（C3 でも C0 でも同じ）。「昨日書いた手順が見つからない」の原因が層2・層3なら、10%を下回りうる。
要ファクト: いまの検索の記録（検索と閲覧の記録）で、勤務時間中の探し物のうち、同じ日に保存された記事を探していたものの割合を数える。
向き: 量の仮定。大きいほど新方式に有利。

**sameDay_tuned_ge**（【仮定】。支える事実なし（設定の変更で何が変わるかを確かめた記録はない））
論拠: 社員がどれだけ新しい記事を探すかは、仕事の中身で決まる。安い設定の変更は、索引を更新する時機だけを変える。
弱い点: 設定の変更と一緒に、「当日の記事は翌日に探す」などの使い方を案内すれば、この割合は下がる。
要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き: C0 に有利。2周目までの notYet_ge_of_slow は「中立」としていたが、tuned に当てはめる部分は C0 に有利な向きなので、片側の公理として分けた（R16）。

**tuned_no_daytime_of_rebuild**（【仮定】。支える事実なし（作り直しにかかる時間と負荷、勤務時間中に回す費用を確かめた記録はない））
論拠: 保存のたびに索引へ足せないなら、新しい記事を検索に出すには、索引を丸ごと作り直すしかない。いまの仕組みは、作り直しを夜間に1回だけ回している（sources.md の聞き取りメモ）。夜間に回すのは、作り直しが重く、勤務時間中に回すと検索が止まるか遅くなるからだと考えられる。300万円より安い設定の変更では、この重さは変わらない。tuned は安い変更のうち記事がいちばん早く検索に出るものなので、勤務時間中に1回でも更新できる安い変更があれば、tuned もそうする。だからこの公理は、「300万円より安い変更のどれでも、勤務時間中に索引を1回も更新できない」という意味になる。
弱い点: 本番の記事は約3万件（trial.md）で、作り直しが数分で済み負荷も小さいなら、昼に1回回すのは設定だけでできる。そのとき、この公理は誤りになる。1回だけなら、その日の記事がまだ出ていない確率は約0.63〜0.65（保存と検索の時刻が勤務時間に一様に散らばるとした計算）で、層1は約6.3〜6.5%。C0 が崩れる境目（約5.8%）をわずかに上回る。2回なら約0.5で、境目（約0.58）を下回り、C0 は示せない。夜間に回しているのは、負荷ではなく、ただの設定かもしれない。
要ファクト: 安い設定の変更で、勤務時間中に1回でも索引を作り直せるか。できるなら、1日に何回まで回せて、費用はいくらか。作り直し1回にかかる時間と負荷を、情報システム部に確かめる。
向き: C0 に有利。

**prodMaxDelay_le_test**（【仮定】。旧 prodDelay_le_test）
論拠・要ファクト・向きは旧公理のまま。支える事実なしの理由も旧公理のまま。
弱い点に足す: 試験環境の20件を、勤務時間のいろいろな時刻に散らして保存したかは分からない。20件の最大は、「どの時刻に保存しても」のいちばん長い場合より短いことがある。

**notYet_le_of_maxFast**（【仮定】。旧 notYet_le_of_fast）
命題の文: どの方式でも、勤務時間中に保存した記事が、いちばん長くても5秒で検索に出て、しかも移行で欠けた記事がないなら、まだ検索に出ていない記事を探すものは0.1%以下。
論拠・弱い点・要ファクト・向き・支える事実なしの理由は、旧公理のまま。

**searchTime_current_eq**（【実験】。旧 search_current_eq）
命題の文・支える事実（F1）・論拠・弱い点は、旧公理の docstring のまま（2周目に書き直したもの）。確信度の行と Reviewer の記録の行は写さない（Writer への注）。
（値の見通し: 1周目に下げた理由の2つは、2周目に searchMinutes を「検索で使う時間」に限り、設問5の文面を survey-2026.md で確かめて解消した（2周目の監査の R20）。値は、Reviewer が新しい公理として監査して決める。主張の値は上がらない。C1 は many_threshold_le の 0.05 で決まる。変わるのは、印のない定理 unfav_saved_le_survey と、@baseline の定理 baseline_lost_le_survey の値だけである。この段落は docstring に写さない）

**_tuned_le の6つ**（【仮定】。支える事実なし（設定の変更で何が変わるかを確かめた記録はない））
論拠（共通）: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない（_tuned_ge と同じ論拠）。
要ファクト（共通）: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
向き（共通）: C0 に不利。安い設定の変更が、層1のほかの点で悪くなる分を見込まない。不利な結論の定理 unfav_savedOverTuned_le_gap だけが使う。
弱い点（個別）:
- searches_tuned_le: 設定の変更を社内に知らせると、検索を試す回数が増えることがある。
- found_tuned_le: 作り直しの間隔を短くすると、作り直しの最中に検索が遅くなり、見つかるまでの時間が延びる。
- extraNotYet_tuned_le: 作り直しの最中に検索が遅くなると、探し直しに時間がかかる。
- extraOther_tuned_le: 同じく、作り直しの最中に検索が遅くなると、探し直しに時間がかかる。
- noHit_tuned_le: 作り直しの設定を変えるときに、語の切り方（辞書）の設定も変わり、引けない語が増えることがある。
- overlook_tuned_le: 作り直しの間隔を変えると、並びに使う値の更新も変わり、並びが悪くなることがある。

_tuned_ge の6つと合わせると、6つの量で tuned と current は等しくなる。これは _full_le と _full_ge で2周目の監査が認めた組み方と同じで、主張の側は _tuned_ge だけに、不利な結論の側は _tuned_le だけに頼る。

docstring だけを変える公理（命題・種類・確信度は変えない）:

- testDelay_le_five: 弱い点の「本番への持ち込みは prodDelay_le_test で別に置く」を「prodMaxDelay_le_test で別に置く」にする。
- extraNotYet_current_ge: 論拠を次に差し替える。「その日の記事は、どう語を変えても出てこないので、出ていないと気づくまで探し直しが続く。語を変えて検索し、結果を見直すのに1回1分ほどかかり、5回ほど繰り返すと5分になる。」弱い点に足す。「時間を検索で使う時間に限ったので、あきらめて人に聞くまでの時間だけが入る。数回であきらめる人は2〜3分で済む。境目は、ほかの値をいまの案のままにすると約2.9分。」
- searches_current_ge: 向き「量の仮定。大きいほど新方式に有利（取り戻せる時間は回数に比例する）。」弱い点に足す「境目は、ほかの値をいまの案のままにすると約2.3回。」
- wage_ge: 向き「量の仮定。大きいほど新方式に有利。」弱い点に足す「境目は、ほかの値をいまの案のままにすると約1,724円。」
- noHit_current_le: 向き「量の仮定。小さいほど新方式に有利（層1の失敗が減った分のうち、層2・層3の失敗に移る分が小さくなる）。設問6の35%は、この値がもっと大きい可能性を示す（回答者に占める割合なので、反対の証拠ではない）。」
- overlook_current_le: 向きは noHit_current_le と同じ文で、設問6の数を22%にする。
- approvable_of_net: 論拠の「もっと安い方法で足りるのでは、という問いにも答えている」を、「いまの仕組みの設定を変えるだけで足りるのでは、という問いに答える」にする。弱い点に足す「ほかの製品や、ほかの業者の見積もり（相見積もり）のような、300万円より安い置き換えの案とは比べていない。」要ファクトに足す「より安い置き換えの案があるか（相見積もり）を、ユーザーに確かめる。」
- fullText_complete: 論拠を「移行の作業には、記事を移すことが含まれる（estimate.md の「移行作業」）。」にする。弱い点に足す「estimate.md は、閲覧の権限を移すことにはふれていない。」

### 4. 定理

| 定理 | 示すこと | 使う判断（関係公理と、途中の定理） | 種類 |
|---|---|---|---|
| notYet_current_ge | 1/10 ≤ pNotYet .current（変えない） | notYet_ge_sameDay_stale・stale_of_noDaytime・current_no_daytime・sameDay_current_ge | [確率] |
| notYet_tuned_ge | 1/10 ≤ pNotYet .tuned（変えない） | notYet_ge_sameDay_stale・stale_of_noDaytime・tuned_no_daytime_of_rebuild・current_not_incremental・sameDay_current_ge・sameDay_tuned_ge | [確率] |
| notYet_fullText_le | pNotYet .fullText ≤ 1/1000（変えない） | testDelay_le_five・prodMaxDelay_le_test・fullText_complete・notYet_le_of_maxFast | [確率] |
| claim_C2_soon（@claim C2） | maxDelaySec .fullText ≤ 5 | testDelay_le_five・prodMaxDelay_le_test | [決定論] |
| claim_C2_faster（@claim C2） | maxDelaySec .fullText < maxDelaySec .current | claim_C2_soon・current_no_daytime・maxDelay_of_noDaytime | [決定論] |
| claim_C1_many・baseline_lost_le_survey・unfav_saved_le_survey | 変えない | search_current_eq を searchTime_current_eq に替えるだけ | 変えない |
| unfav_savedOverTuned_le_gap（印なし。docstring の先頭に [不利]） | savedOverTunedMinutes ≤ searchesPerDay .current ×（pNotYet .tuned の値 − pNotYet .fullText の値）×（extraNotYetMinutes .current − missAfterIndex .current × extraOtherMinutes .current） | search_decomp・miss_compose・searchesPerDay_nonneg・foundMinutes_nonneg・_tuned_le の6つ・_full_ge の6つ・extraNotYet_nonneg・extraOther_nonneg（unfav_saved_le_gap を途中で使ってよい） | [不利] |

- unfav_savedOverTuned_le_gap の docstring:「安い設定の変更に比べて取り戻せる時間は、回数(いま) ×（安い設定の変更と置き換えた後の層1の差）×（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）を超えない。安い設定の変更で層1が下がれば、C0 の効果もそれに比例して縮む。主張の側の片側の公理（_full_le、_tuned_ge）も、量の仮定（4回、5分、10%）も通らない。」
- ほかの定理（主張の定理 C0・C3、saved_ge_gap など）は変えない。計算の値（1.2672分、5,220,864円など）も変わらない。どの主張の確信度も上がらない（C0・C1・C2・C3 は 0.05 のまま）。

予想される不利な結論（2周目の7節の一覧を置き換える。定理が示すことだけを書く）:

1. unfav_saved_le_gap: いまのままと比べて取り戻せる時間は、current と fullText の層1の差に比例する式を超えない（C3 の読み b）。
2. unfav_savedOverTuned_le_gap（新）: 安い設定の変更と比べて取り戻せる時間は、tuned と fullText の層1の差に比例する式を超えない（C0）。
3. unfav_saved_le_lost、4. unfav_saved_le_survey: 2周目のまま。
5. 境目（計算の値。定理にしない理由は2周目の9節）: 層1で約5.8%（C3 は current、C0 は tuned）。その日の記事の割合が10%なら、tuned の pStale で約0.58。昼に1回の作り直しで約0.63〜0.65、2回で約0.5。ほかに、回数で約2.3回、単価で約1,724円、層1の余分な時間で約2.9分。
6. C0 の要は、current_not_incremental と tuned_no_daytime_of_rebuild である。
7. C2 は本番で確かめていない（2周目のまま）。

### 5. 向きの数え直し（2周目の5節に足す）

- 「同じとみなす」置き方の表に足す: 「安い設定の変更は、層1のほかの点で悪くならない」＝ _tuned_le の6つ。C0 に不利。unfav_savedOverTuned_le_gap だけが使う。
- 「探す記事の新しさは方式に依らない」の行から notYet_ge_of_slow を外す。この行には notYet_le_of_maxFast だけが残る（中立）。sameDay_tuned_ge は、C0 に有利な片側として数える。
- 有利な向きの一覧に足す: current_no_daytime、sameDay_current_ge、sameDay_tuned_ge、tuned_no_daytime_of_rebuild、searches_current_ge、wage_ge、noHit_current_le、overlook_current_le。一覧から外す: tuned_slow_of_rebuild。名前を替える: prodDelay_le_test を prodMaxDelay_le_test に。
- 主張の値が有利な向きの仮定に片寄っていることは、2周目と同じく隠さない。その順でステージ6で確かめる（次の節）。

### 6. ステージ6で先に確かめる順（2周目の10節を置き換える）

1. いまの仕組みについて（情報システム部）: 勤務時間中に索引を更新しているか（current_no_daytime。聞き取りメモの登録）。保存のたびに索引へ足せるか（current_not_incremental）。安い設定の変更で、勤務時間中に1回でも作り直せるか、何回か、費用はいくらか（tuned_no_daytime_of_rebuild）。「昨日書いた手順が見つからない」の原因。
2. その日の記事を探す割合（sameDay_current_ge。境目は約5.8%）。
3. 主張の側が使う有利な片側（noHit_full_le、overlook_full_le、searches_full_le）。
4. 費用と値打ち（cost_le_estimate、gain_ge_wage、workDays_ge、wage_ge）。
5. 量の仮定（searches_current_ge、extraNotYet_current_ge、noHit_current_le、overlook_current_le）。
6. 素材にあって、まだ事実として登録していないもの（2周目の10節の5のまま）。

### 7. 失敗の台帳と数え方

- ledger.json を直した。層1の行の3つの欄の公理、本番の負荷の行の量の名前（maxDelaySec）、層2・層3・余分な時間の行の tuned の欄と比べ方（_tuned_le を足した）、使う定理（unfav_savedOverTuned_le_gap を足した）。
- 数え方: 【実験】3、【経験則】2、【自明】8、【仮定】44、合わせて57（2周目は47）。消した・名前を変えた公理が6つ、足した公理が16（名前を変えた3つを含む）。数そのものは物差しにしない。

## 採らない指摘

- R16 の「途中の案の層1を、別の【仮定】で置く」: 採らない。置くなら、「勤務時間中の作り直しは1日1回まで」と「1回までなら、その日の記事がまだ出ていない確率は 3/5 以上」の2つの判断が要り、どちらにも事実がない。Reviewer が挙げたもう1つの直し方（「1回も更新できない」の命題に変え、論拠を書き直す）を採り、途中の案は弱い点に数字で書いた。ステージ6で「1回なら更新できる」と分かったら、そのときに途中の案の公理を置く。
- R16 の末尾の @baseline の提案（tuned はいまより遅くならない、を【自明】にする）: 採らない。tuned の遅れは、もうどの公理にも出ない。DaytimeUpdate の形で同じこと（current が勤務時間中に更新するなら tuned も更新する）を【自明】にしても、それを確かめる定理は、その公理の言い換えになる。tuned が藁人形でないかは、tuned_no_daytime_of_rebuild の要ファクト（安い変更で勤務時間中に何回更新できるか）で確かめる。
- R19: この周の対応はない。前の周の3つは Reviewer が改めて監査した。この周は、命題か使う宣言の意味が変わる公理を、すべて名前を変えるか消して置き換えた。
- R2・R3（ステージ6）: 事実の不足なので、この周では値を変えない。R3 の delay_current_ge_workday は消し、current_no_daytime に置き換えた。新しい命題は、聞き取りメモの「夜間に1回だけ作り直す」でそのまま支えられる形になった。確信度の案は 0.3 のままにした（上げるには事実が要る）。R2 の反対の証拠の候補（いまの仕組みが Elasticsearch なら、保存のたびに索引へ足せる）は、current_not_incremental に当たる。
- R10・R11・R14（ステージ5）: 主張の形の問題で、ステージの終わりにユーザーに見せる。R11 に1つ足す。「すぐ」を「数秒のうちに」と読むなら claim_C2_soon（maxDelaySec .fullText ≤ 5）が合い、「その日のうちに」と読むなら DaytimeUpdate .fullText が合う。読みが決まってから定理を直す。

## 証人の見通しの変更

- DaytimeUpdate は current で偽、tuned で偽、fullText で真にする。
- pSameDay はどの方式も 1/10。pStale は current 1、tuned 1、fullText 1/100。pNotYet は変えない（1/10、1/10、1/1000）。notYet_ge_sameDay_stale は3つとも等号で成り立つ（fullText は 1/10 × 1/100 = 1/1000）。
- maxDelaySec は、前の周の indexDelaySec の値のまま（current 86400、tuned 43200、fullText 4）。maxDelay_of_noDaytime の結論は、current と tuned で真に成り立つ。
- _tuned_le の6つは、tuned の値が current と同じなので等号で成り立つ。
- 前提が成り立つことを示す example を足す: ¬ DaytimeUpdate .current と ¬ DaytimeUpdate .tuned（stale_of_noDaytime と maxDelay_of_noDaytime の前提）。¬ CurrentIncremental の example は、tuned_no_daytime_of_rebuild の前提として残す。前の周の「28800 ≤ indexDelaySec …」の2つの example は、宣言の名前を直し、コメントを maxDelay_of_noDaytime の結論に合わせる（消してもよい）。
- 主張の定理は、どれも前提を持たない（変わらない）。

## Writer への注

- 消す公理（delay_current_ge_workday、notYet_ge_of_slow、tuned_slow_of_rebuild）と、名前を変える公理（prodDelay_le_test、notYet_le_of_fast、search_current_eq）の、確信度の行と Reviewer の記録の行は、新しい公理に写さない。ガイドの「命題を変えるときは名前も変えて別の公理にし、前の公理の Reviewer の判断を引き継がない」に当たる。current_no_daytime の確信度の案は 0.3 と書く。searchTime_current_eq は【実験】なので、確信度の行を書かない。
- claim_C1_many の docstring にある、Reviewer の印の行（言い換えの記録）は残す。変えるのは証明の中の公理の名前だけ。
- Method の docstring（tuned の説明）は変えない。
- 差分の文のうち、印の語を含むものは、前の周と同じく言い換えて写す（「支える事実」「反対の証拠」など）。
- 証明の道筋（3節の公理だけで示せることを確かめた）:
  - notYet_current_ge: notYet_ge_sameDay_stale .current と、stale_of_noDaytime .current current_no_daytime（pStale ≥ 1）、sameDay_current_ge（pSameDay ≥ 1/10）から、rat_mul_le_mul で 1/10 × 1 ≤ 積 ≤ pNotYet。
  - notYet_tuned_ge: 同じ形。pSameDay .tuned ≥ 1/10 は sameDay_current_ge と sameDay_tuned_ge から。¬ DaytimeUpdate .tuned は tuned_no_daytime_of_rebuild current_not_incremental から。
  - claim_C2_faster: claim_C2_soon と、maxDelay_of_noDaytime .current current_no_daytime から grind。
  - unfav_savedOverTuned_le_gap: savedOverTunedMinutes = savedMinutes +（searchMinutes .tuned − searchMinutes .current）。search_layers .tuned を、_tuned_le の6つで current の値に置き換えた上界にする（savedOverTuned_ge_gap と向きが逆）。すると、searchMinutes .tuned − searchMinutes .current ≤ 回数(いま) ×（pNotYet .tuned − pNotYet .current）×（extraNotYetMinutes .current − missAfterIndex .current × extraOtherMinutes .current）。これと unfav_saved_le_gap の上界を足すと結論になる。符号は extraNotYet_nonneg・extraOther_nonneg・foundMinutes_nonneg・searchesPerDay_nonneg・Prob の範囲・missAfterIndex_nonneg から出す。extraNotYet_current_ge と _tuned_ge は使わない。
- Argument.lean の冒頭の「主張と定理の対応」「印のない定理」の表と、「設計書（model-plan.md）との違い」を、この差分に合わせて直す。Model.lean には、axiom 以外の変更を同じ順で写し、冒頭の証人の表に DaytimeUpdate・pSameDay・pStale を足す。
