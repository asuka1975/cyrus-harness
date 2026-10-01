# 差分と対応表（rounds/01 → いま）

`cyrus logic-round diff` が機械で作った。Reviewer は、差分の設計書の行が当たっているか、設計書にない変更がないかを確かめる。

## 変わった宣言

変化の種類: 「変更」はコード（公理の型、定理の文と証明、def）が変わった。「変更（印）」は `@confidence`・`@reviewer`・`@support`・【】などの印の行だけが変わった（`@reviewer` の行が消えていないかを見る）。「変更（説明だけ）」は docstring の説明だけが変わった。

| ファイル | 宣言 | 変化 |
|---|---|---|
| Argument.lean | `CheaperFix` | 削除 |
| Argument.lean | `CurrentIncremental` | 追加 |
| Argument.lean | `IndexComplete` | 追加 |
| Argument.lean | `Method` | 変更 |
| Argument.lean | `approvable_of_net` | 変更 |
| Argument.lean | `baseline_lost_le_survey` | 変更 |
| Argument.lean | `beneficiaries_ge` | 変更（説明だけ） |
| Argument.lean | `benefitYen` | 削除 |
| Argument.lean | `claim_C0_approvable` | 変更 |
| Argument.lean | `claim_C3_lost` | 変更 |
| Argument.lean | `claim_C3_saved` | 変更 |
| Argument.lean | `cost_eq` | 削除 |
| Argument.lean | `cost_le_estimate` | 追加 |
| Argument.lean | `current_not_incremental` | 追加 |
| Argument.lean | `delay_current_ge_workday` | 変更（印） |
| Argument.lean | `estimateYen` | 追加 |
| Argument.lean | `estimate_eq` | 追加 |
| Argument.lean | `extraNotYetMinutes` | 追加 |
| Argument.lean | `extraNotYet_current_ge` | 追加 |
| Argument.lean | `extraNotYet_full_ge` | 追加 |
| Argument.lean | `extraNotYet_full_le` | 追加 |
| Argument.lean | `extraNotYet_nonneg` | 追加 |
| Argument.lean | `extraNotYet_tuned_ge` | 追加 |
| Argument.lean | `extraOtherMinutes` | 追加 |
| Argument.lean | `extraOther_full_ge` | 追加 |
| Argument.lean | `extraOther_full_le` | 追加 |
| Argument.lean | `extraOther_le_notYet` | 追加 |
| Argument.lean | `extraOther_nonneg` | 追加 |
| Argument.lean | `extraOther_tuned_ge` | 追加 |
| Argument.lean | `firstYearCost` | 変更（説明だけ） |
| Argument.lean | `foundMinutes` | 変更（説明だけ） |
| Argument.lean | `foundMinutes_same` | 削除 |
| Argument.lean | `found_full_ge` | 追加 |
| Argument.lean | `found_full_le` | 追加 |
| Argument.lean | `found_tuned_ge` | 追加 |
| Argument.lean | `fullText_complete` | 追加 |
| Argument.lean | `gainYen` | 追加 |
| Argument.lean | `gain_ge_wage` | 追加 |
| Argument.lean | `lostMinutes` | 変更 |
| Argument.lean | `lostWageYen` | 追加 |
| Argument.lean | `lostYen` | 削除 |
| Argument.lean | `lost_ge` | 変更 |
| Argument.lean | `missAfterIndex` | 追加 |
| Argument.lean | `missAfterIndex_nonneg` | 追加 |
| Argument.lean | `missExtraMinutes` | 削除 |
| Argument.lean | `missExtra_current_ge` | 削除 |
| Argument.lean | `missExtra_same` | 削除 |
| Argument.lean | `miss_compose` | 変更（印） |
| Argument.lean | `miss_current_ge` | 削除 |
| Argument.lean | `miss_sub_notYet` | 追加 |
| Argument.lean | `noHit_current_le` | 変更（印） |
| Argument.lean | `noHit_full_ge` | 追加 |
| Argument.lean | `noHit_full_le` | 追加 |
| Argument.lean | `noHit_same` | 削除 |
| Argument.lean | `noHit_tuned_ge` | 追加 |
| Argument.lean | `no_cheaper_fix` | 削除 |
| Argument.lean | `notYet_fullText_le` | 変更 |
| Argument.lean | `notYet_ge_of_slow` | 変更（印） |
| Argument.lean | `notYet_le_of_fast` | 変更 |
| Argument.lean | `notYet_tuned_ge` | 追加 |
| Argument.lean | `overlook_current_le` | 変更（印） |
| Argument.lean | `overlook_full_ge` | 追加 |
| Argument.lean | `overlook_full_le` | 追加 |
| Argument.lean | `overlook_same` | 削除 |
| Argument.lean | `overlook_tuned_ge` | 追加 |
| Argument.lean | `pNoHit` | 変更（説明だけ） |
| Argument.lean | `pOverlook` | 変更（説明だけ） |
| Argument.lean | `prodDelay_le_test` | 変更（印） |
| Argument.lean | `savedOverTunedMinutes` | 追加 |
| Argument.lean | `savedOverTunedWageYen` | 追加 |
| Argument.lean | `savedOverTuned_ge` | 追加 |
| Argument.lean | `savedOverTuned_ge_gap` | 追加 |
| Argument.lean | `savedWageYen` | 追加 |
| Argument.lean | `saved_ge` | 変更 |
| Argument.lean | `saved_ge_gap` | 追加 |
| Argument.lean | `saved_only_from_notYet` | 削除 |
| Argument.lean | `searchMinutes` | 変更（説明だけ） |
| Argument.lean | `search_current_eq` | 変更（印） |
| Argument.lean | `search_decomp` | 変更 |
| Argument.lean | `search_layers` | 追加 |
| Argument.lean | `searchesPerDay_nonneg` | 追加 |
| Argument.lean | `searches_full_ge` | 追加 |
| Argument.lean | `searches_full_le` | 追加 |
| Argument.lean | `searches_same` | 削除 |
| Argument.lean | `searches_tuned_ge` | 追加 |
| Argument.lean | `testDelaySec` | 変更（説明だけ） |
| Argument.lean | `tuned_slow_of_rebuild` | 追加 |
| Argument.lean | `unfav_saved_le_gap` | 追加 |
| Argument.lean | `unfav_saved_le_lost` | 変更 |
| Argument.lean | `workDays` | 変更（説明だけ） |
| Argument.lean | `workDays_ge` | 変更（印） |
| Argument.lean | `yenPerDailyMinute` | 変更（説明だけ） |
| Argument.lean | `yenPerDailyMinute_ge` | 変更（説明だけ） |
| Model.lean | `Approvable` | 変更 |
| Model.lean | `CheaperFix` | 削除 |
| Model.lean | `CurrentIncremental` | 追加 |
| Model.lean | `IndexComplete` | 追加 |
| Model.lean | `Method` | 変更 |
| Model.lean | `approvable_of_net` | 変更 |
| Model.lean | `baseline_lost_le_survey` | 変更 |
| Model.lean | `beneficiaries_ge` | 変更（説明だけ） |
| Model.lean | `benefitYen` | 削除 |
| Model.lean | `claim_C0_approvable` | 変更 |
| Model.lean | `claim_C1_many` | 変更（印） |
| Model.lean | `claim_C3_lost` | 変更 |
| Model.lean | `claim_C3_saved` | 変更 |
| Model.lean | `cost_eq` | 削除 |
| Model.lean | `cost_le_estimate` | 追加 |
| Model.lean | `current_not_incremental` | 追加 |
| Model.lean | `delay_current_ge_workday` | 変更（説明だけ） |
| Model.lean | `estimateYen` | 追加 |
| Model.lean | `estimate_eq` | 追加 |
| Model.lean | `extraNotYetMinutes` | 追加 |
| Model.lean | `extraNotYet_current_ge` | 追加 |
| Model.lean | `extraNotYet_full_ge` | 追加 |
| Model.lean | `extraNotYet_full_le` | 追加 |
| Model.lean | `extraNotYet_nonneg` | 追加 |
| Model.lean | `extraNotYet_tuned_ge` | 追加 |
| Model.lean | `extraOtherMinutes` | 追加 |
| Model.lean | `extraOther_full_ge` | 追加 |
| Model.lean | `extraOther_full_le` | 追加 |
| Model.lean | `extraOther_le_notYet` | 追加 |
| Model.lean | `extraOther_nonneg` | 追加 |
| Model.lean | `extraOther_tuned_ge` | 追加 |
| Model.lean | `firstYearCost` | 変更 |
| Model.lean | `foundMinutes` | 変更（説明だけ） |
| Model.lean | `foundMinutes_same` | 削除 |
| Model.lean | `found_full_ge` | 追加 |
| Model.lean | `found_full_le` | 追加 |
| Model.lean | `found_tuned_ge` | 追加 |
| Model.lean | `fullText_complete` | 追加 |
| Model.lean | `gainYen` | 追加 |
| Model.lean | `gain_ge_wage` | 追加 |
| Model.lean | `indexDelaySec` | 変更 |
| Model.lean | `lostMinutes` | 変更 |
| Model.lean | `lostWageYen` | 追加 |
| Model.lean | `lostYen` | 削除 |
| Model.lean | `lost_ge` | 変更 |
| Model.lean | `manyMinutes` | 変更 |
| Model.lean | `many_threshold_le` | 変更 |
| Model.lean | `missAfterIndex` | 追加 |
| Model.lean | `missAfterIndex_nonneg` | 追加 |
| Model.lean | `missExtraMinutes` | 削除 |
| Model.lean | `missExtra_current_ge` | 削除 |
| Model.lean | `missExtra_same` | 削除 |
| Model.lean | `missProb` | 変更 |
| Model.lean | `miss_compose` | 変更 |
| Model.lean | `miss_current_ge` | 削除 |
| Model.lean | `miss_sub_notYet` | 追加 |
| Model.lean | `noHit_current_le` | 変更（説明だけ） |
| Model.lean | `noHit_full_ge` | 追加 |
| Model.lean | `noHit_full_le` | 追加 |
| Model.lean | `noHit_same` | 削除 |
| Model.lean | `noHit_tuned_ge` | 追加 |
| Model.lean | `no_cheaper_fix` | 削除 |
| Model.lean | `notYet_fullText_le` | 変更 |
| Model.lean | `notYet_ge_of_slow` | 変更 |
| Model.lean | `notYet_le_of_fast` | 変更 |
| Model.lean | `notYet_tuned_ge` | 追加 |
| Model.lean | `overlook_current_le` | 変更（説明だけ） |
| Model.lean | `overlook_full_ge` | 追加 |
| Model.lean | `overlook_full_le` | 追加 |
| Model.lean | `overlook_same` | 削除 |
| Model.lean | `overlook_tuned_ge` | 追加 |
| Model.lean | `pNoHit` | 変更（説明だけ） |
| Model.lean | `pNotYet` | 変更 |
| Model.lean | `pOverlook` | 変更（説明だけ） |
| Model.lean | `prodDelay_le_test` | 変更 |
| Model.lean | `savedOverTunedMinutes` | 追加 |
| Model.lean | `savedOverTunedWageYen` | 追加 |
| Model.lean | `savedOverTuned_ge` | 追加 |
| Model.lean | `savedOverTuned_ge_gap` | 追加 |
| Model.lean | `savedWageYen` | 追加 |
| Model.lean | `saved_ge` | 変更 |
| Model.lean | `saved_ge_gap` | 追加 |
| Model.lean | `saved_only_from_notYet` | 削除 |
| Model.lean | `searchMinutes` | 変更 |
| Model.lean | `searchMinutes_nonneg` | 変更 |
| Model.lean | `search_current_eq` | 変更 |
| Model.lean | `search_decomp` | 変更 |
| Model.lean | `search_layers` | 追加 |
| Model.lean | `searchesPerDay` | 変更（説明だけ） |
| Model.lean | `searchesPerDay_nonneg` | 追加 |
| Model.lean | `searches_current_ge` | 変更（説明だけ） |
| Model.lean | `searches_full_ge` | 追加 |
| Model.lean | `searches_full_le` | 追加 |
| Model.lean | `searches_same` | 削除 |
| Model.lean | `searches_tuned_ge` | 追加 |
| Model.lean | `testDelay_le_five` | 変更（説明だけ） |
| Model.lean | `tuned_slow_of_rebuild` | 追加 |
| Model.lean | `unfav_saved_le_gap` | 追加 |
| Model.lean | `unfav_saved_le_lost` | 変更 |
| Model.lean | `wage_ge` | 変更（説明だけ） |
| Model.lean | `workDays` | 変更（説明だけ） |
| Model.lean | `workDays_ge` | 変更（説明だけ） |
| Model.lean | `yenPerDailyMinute` | 変更（説明だけ） |
| Model.lean | `yenPerDailyMinute_ge` | 変更（説明だけ） |

宣言の外（見出し・説明のコメントなど）で変わった行: 297

## 差分の設計書（model-plan-delta.md）の行と差分の対応

| # | 設計書の行 | 挙げた名前 | 当たった変更 |
|---|---|---|---|
| 1 | ／ `Method` ／ コンストラクタを1つ足す ／ 型（コンストラクタ current・tuned・fullText… | `Method` | `Method` |
| 2 | ／ `pNoHit` ／ docstring を変える ／ 変えない ／ 層2。索引に入っている記事を探したとき、入れた… | `pNoHit` | `pNoHit` |
| 3 | ／ `pOverlook` ／ docstring を変える ／ 変えない ／ 層3。引けた記事を、結果の中で見落とす確… | `pOverlook` | `pOverlook` |
| 4 | ／ `searchMinutes` ／ docstring を変える ／ 変えない ／ 社員1人が1日に、検索で探し物を… | `searchMinutes` | `searchMinutes` |
| 5 | ／ `foundMinutes` ／ docstring を変える ／ 変えない ／ 見つかった探し物1回に、検索で使う… | `foundMinutes` | `foundMinutes` |
| 6 | ／ `missExtraMinutes` → `extraNotYetMinutes` ／ 名前と意味を変える ／ Me… | `extraNotYetMinutes`, `missExtraMinutes` | `extraNotYetMinutes`, `missExtraMinutes` |
| 7 | ／ `extraOtherMinutes` ／ 新設 ／ Method → Rat ／ 層2か層3で見つからなかった（語… | `extraOtherMinutes` | `extraOtherMinutes` |
| 8 | ／ `testDelaySec` ／ docstring を変える ／ 変えない ／ 試験環境の全文検索エンジンに記事を… | `testDelaySec` | `testDelaySec` |
| 9 | ／ `workDays` ／ docstring を変える ／ 変えない ／ 初年度のうち、置き換えた検索を使える勤務日… | `workDays` | `workDays` |
| 10 | ／ `estimateYen` ／ 新設 ／ Rat ／ 移行の初年度費用の見積もりの額（円）。置き換える側にだけ現れる… | `estimateYen` | `estimateYen` |
| 11 | ／ `firstYearCost` ／ docstring を変える ／ 変えない ／ 置き換えの初年度に、実際に追加で… | `firstYearCost` | `firstYearCost` |
| 12 | ／ `gainYen` ／ 新設。Approvable より前に宣言する ／ Rat ／ 置き換えたとき、安い設定の変更… | `gainYen` | `gainYen` |
| 13 | ／ `CurrentIncremental` ／ 新設 ／ Prop ／ いまの検索の仕組みは、記事を保存するたびに、そ… | `CurrentIncremental` | `CurrentIncremental` |
| 14 | ／ `IndexComplete` ／ 新設 ／ Method → Prop ／ その方式の検索が、Wiki のすべての… | `IndexComplete` | `IndexComplete` |
| 15 | ／ `CheaperFix` ／ 削除 ／ — ／ 比べる相手を tuned にしたので要らない（R1） ／ | `CheaperFix` | `CheaperFix` |
| 16 | ／ `missAfterIndex` ／ 新設 ／ 1 −（1 − pNoHit M の値）×（1 − pOverloo… | `missAfterIndex` | `missAfterIndex` |
| 17 | ／ `lostMinutes` ／ 計算を変える ／ current の searchesPerDay ×（pNotYe… | `lostMinutes` | `lostMinutes` |
| 18 | ／ `savedOverTunedMinutes` ／ 新設 ／ searchMinutes .tuned − sear… | `savedOverTunedMinutes` | `savedOverTunedMinutes` |
| 19 | ／ `yenPerDailyMinute` ／ docstring を変える（計算は同じ） ／ 変えない ／ 1人1日1… | `yenPerDailyMinute` | `yenPerDailyMinute` |
| 20 | ／ `lostYen` → `lostWageYen` ／ 名前を変える（計算は同じ） ／ yenPerDailyMin… | `lostWageYen`, `lostYen` | `lostWageYen`, `lostYen` |
| 21 | ／ `benefitYen` → `savedWageYen` ／ 名前を変える（計算は同じ） ／ yenPerDail… | `benefitYen`, `savedWageYen` | `benefitYen`, `savedWageYen` |
| 22 | ／ `savedOverTunedWageYen` ／ 新設 ／ yenPerDailyMinute × savedOv… | `savedOverTunedWageYen` | `savedOverTunedWageYen` |
| 23 | ／ `cost_eq` ／ 等号が、「見積もりの額は300万円」と「実際の費用は見積もりを超えない」の2つの判断を含んで… | `cost_eq` | `cost_eq` |
| 24 | ／ `no_cheaper_fix` ／ 「5秒以内」で定義した安い案は、効果が生まれる遅れの幅とずれていて、藁人形にな… | `no_cheaper_fix` | `no_cheaper_fix` |
| 25 | ／ `searches_same` ／ 等式は、主張が使う片側（置き換えで悪くならない）と、不利な結論だけが使う片側（よ… | `searches_same` | `searches_same` |
| 26 | ／ `foundMinutes_same` ／ 同上 ／ found_full_le・found_full_ge ／ | `foundMinutes_same` | `foundMinutes_same` |
| 27 | ／ `missExtra_same` ／ 同上。余分な時間を層で分けた（R7） ／ extraNotYet_full_l… | `missExtra_same` | `missExtra_same` |
| 28 | ／ `noHit_same` ／ 同上。有利な証拠（全文検索のほうが語で引ける）で崩れることが、いちばん起こりやすい（R… | `noHit_same` | `noHit_same` |
| 29 | ／ `overlook_same` ／ 同上 ／ overlook_full_le・overlook_full_ge ／ | `overlook_same` | `overlook_same` |
| 30 | ／ `search_decomp` ／ 型を変える ／ 【自明】 ／ どの方式でも、1日の探し物の時間 = 回数 ×（見… | `search_decomp` | `search_decomp` |
| 31 | ／ `miss_compose` ／ 種類を【仮定】から【自明】に変える。型は変えない ／ 【自明】 ／ どの方式でも、… | `miss_compose` | `miss_compose` |
| 32 | ／ `notYet_le_of_fast` ／ 前提を1つ足す ／ 【仮定】 ／ どの方式でも、保存から検索に出るまで5… | `notYet_le_of_fast` | `notYet_le_of_fast` |
| 33 | ／ `missExtra_current_ge` → `extraNotYet_current_ge` ／ 名前と型を変… | `extraNotYet_current_ge`, `missExtra_current_ge` | `extraNotYet_current_ge`, `missExtra_current_ge` |
| 34 | ／ `approvable_of_net` ／ 型を変える ／ 【仮定】 ／ 置き換えで会社が得る値打ち（安い設定の変更… | `approvable_of_net` | `approvable_of_net` |
| 35 | ／ `search_current_eq` ／ 論拠と弱い点（4.5節）。@confidence 0.75 と @rev… | `search_current_eq` | `search_current_eq` |
| 36 | ／ `delay_current_ge_workday` ／ 弱い点と要ファクト（4.5節）。@confidence 0… | `delay_current_ge_workday` | `delay_current_ge_workday` |
| 37 | ／ `notYet_ge_of_slow` ／ 当てはめる方式に tuned が入ること、弱い点、要ファクト（4.5節）… | `notYet_ge_of_slow` | `notYet_ge_of_slow` |
| 38 | ／ `prodDelay_le_test` ／ 論拠と要ファクト（4.5節） ／ | `prodDelay_le_test` | `prodDelay_le_test` |
| 39 | ／ `beneficiaries_ge` ／ 論拠（4.5節） ／ | `beneficiaries_ge` | `beneficiaries_ge` |
| 40 | ／ `workDays_ge` ／ 命題の読み（初年度に使える日数）、論拠、弱い点、要ファクト、向き（4.5節） ／ | `workDays_ge` | `workDays_ge` |
| 41 | ／ `noHit_current_le` ／ 命題の読み（条件付きの確率）と弱い点（4.5節） ／ | `noHit_current_le` | `noHit_current_le` |
| 42 | ／ `overlook_current_le` ／ 命題の読み（条件付きの確率）と弱い点（4.5節） ／ | `overlook_current_le` | `overlook_current_le` |
| 43 | ／ `estimate_eq` ／ 【実験】 ／ 移行の初年度費用の見積もりの額は300万円 ／ estimateYen… | `estimate_eq` | `estimate_eq` |
| 44 | ／ `cost_le_estimate` ／ 【仮定】 ／ 置き換えの初年度に実際に追加で要る費用は、見積もりの額を超え… | `cost_le_estimate` | `cost_le_estimate` |
| 45 | ／ `searchesPerDay_nonneg` ／ 【自明】 ／ どの方式でも、1日の探し物の回数は0以上 ／ ∀ … | `searchesPerDay_nonneg` | `searchesPerDay_nonneg` |
| 46 | ／ `fullText_complete` ／ 【仮定】 ／ 置き換えた後の検索は、Wiki のすべての記事を、閲覧でき… | `fullText_complete` | `fullText_complete` |
| 47 | ／ `extraNotYet_nonneg` ／ 【仮定】 ／ いまの検索で、層1で見つからなかった探し物の余分な時間は… | `extraNotYet_nonneg` | `extraNotYet_nonneg` |
| 48 | ／ `extraOther_nonneg` ／ 【仮定】 ／ いまの検索で、層2・層3で見つからなかった探し物の余分な時… | `extraOther_nonneg` | `extraOther_nonneg` |
| 49 | ／ `extraOther_le_notYet` ／ 【仮定】 ／ いまの検索で、層2・層3で見つからなかったときの余分… | `extraOther_le_notYet` | `extraOther_le_notYet` |
| 50 | ／ `searches_full_le` ／ 【仮定】 ／ 置き換えても、1人1日の探し物の回数は増えない ／ sear… | `searches_full_le` | `searches_full_le` |
| 51 | ／ `searches_full_ge` ／ 【仮定】 ／ 置き換えても、1人1日の探し物の回数は減らない ／ sear… | `searches_full_ge` | `searches_full_ge` |
| 52 | ／ `found_full_le` ／ 【仮定】 ／ 置き換えても、見つかった探し物1回の時間は延びない ／ found… | `found_full_le` | `found_full_le` |
| 53 | ／ `found_full_ge` ／ 【仮定】 ／ 置き換えても、見つかった探し物1回の時間は縮まない ／ found… | `found_full_ge` | `found_full_ge` |
| 54 | ／ `extraNotYet_full_le` ／ 【仮定】 ／ 置き換えても、層1で見つからなかったときの余分な時間は… | `extraNotYet_full_le` | `extraNotYet_full_le` |
| 55 | ／ `extraNotYet_full_ge` ／ 【仮定】 ／ 置き換えても、層1で見つからなかったときの余分な時間は… | `extraNotYet_full_ge` | `extraNotYet_full_ge` |
| 56 | ／ `extraOther_full_le` ／ 【仮定】 ／ 置き換えても、層2・層3で見つからなかったときの余分な時… | `extraOther_full_le` | `extraOther_full_le` |
| 57 | ／ `extraOther_full_ge` ／ 【仮定】 ／ 置き換えても、層2・層3で見つからなかったときの余分な時… | `extraOther_full_ge` | `extraOther_full_ge` |
| 58 | ／ `noHit_full_le` ／ 【仮定】 ／ 置き換えても、索引に入っている記事を語で引けない確率は上がらない … | `noHit_full_le` | `noHit_full_le` |
| 59 | ／ `noHit_full_ge` ／ 【仮定】 ／ 置き換えても、索引に入っている記事を語で引けない確率は下がらない … | `noHit_full_ge` | `noHit_full_ge` |
| 60 | ／ `overlook_full_le` ／ 【仮定】 ／ 置き換えても、引けた記事を見落とす確率は上がらない ／ (p… | `overlook_full_le` | `overlook_full_le` |
| 61 | ／ `overlook_full_ge` ／ 【仮定】 ／ 置き換えても、引けた記事を見落とす確率は下がらない ／ (p… | `overlook_full_ge` | `overlook_full_ge` |
| 62 | ／ `searches_tuned_ge` ／ 【仮定】 ／ 安い設定の変更をしても、1人1日の探し物の回数は減らない … | `searches_tuned_ge` | `searches_tuned_ge` |
| 63 | ／ `found_tuned_ge` ／ 【仮定】 ／ 安い設定の変更をしても、見つかった探し物1回の時間は縮まない ／… | `found_tuned_ge` | `found_tuned_ge` |
| 64 | ／ `extraNotYet_tuned_ge` ／ 【仮定】 ／ 安い設定の変更をしても、層1で見つからなかったときの… | `extraNotYet_tuned_ge` | `extraNotYet_tuned_ge` |
| 65 | ／ `extraOther_tuned_ge` ／ 【仮定】 ／ 安い設定の変更をしても、層2・層3で見つからなかったと… | `extraOther_tuned_ge` | `extraOther_tuned_ge` |
| 66 | ／ `noHit_tuned_ge` ／ 【仮定】 ／ 安い設定の変更をしても、語で引けない確率は下がらない ／ (pN… | `noHit_tuned_ge` | `noHit_tuned_ge` |
| 67 | ／ `overlook_tuned_ge` ／ 【仮定】 ／ 安い設定の変更をしても、見落とす確率は下がらない ／ (p… | `overlook_tuned_ge` | `overlook_tuned_ge` |
| 68 | ／ `current_not_incremental` ／ 【仮定】 ／ いまの検索の仕組みは、記事を保存するたびに、そ… | `current_not_incremental` | `current_not_incremental` |
| 69 | ／ `tuned_slow_of_rebuild` ／ 【仮定】 ／ いまの仕組みが保存のたびに索引へ足せないなら、30… | `tuned_slow_of_rebuild` | `tuned_slow_of_rebuild` |
| 70 | ／ `gain_ge_wage` ／ 【仮定】 ／ 置き換えで会社が得る値打ちは、安い設定の変更に比べて取り戻せる時間の… | `gain_ge_wage` | `gain_ge_wage` |
| 71 | ／ `notYet_tuned_ge` ／ 新設（印なし） ／ 安い設定の変更をしても、まだ検索に出ていない記事を探す確… | `notYet_tuned_ge` | `notYet_tuned_ge` |
| 72 | ／ `notYet_fullText_le` ／ 使う判断を変える（示すことは同じ） ／ 置き換えた後、まだ検索に出てい… | `notYet_fullText_le` | `notYet_fullText_le` |
| 73 | ／ `miss_current_ge` ／ 削除 ／ lost_ge が使わなくなった ／ — ／ — ／ | `miss_current_ge` | `miss_current_ge` |
| 74 | ／ `lost_ge` ／ 証明を変える（示すことは同じ: 2 ≤ lostMinutes） ／ 失われている時間（読み… | `lost_ge` | `lost_ge` |
| 75 | ／ `saved_only_from_notYet` ／ 削除 ／ 等式は、主張が使う片側と不利な結論が使う片側を1つに… | `saved_only_from_notYet` | `saved_only_from_notYet` |
| 76 | ／ `saved_ge_gap` ／ 新設（印なし） ／ searchesPerDay .current ×（pNotY… | `saved_ge_gap` | `saved_ge_gap` |
| 77 | ／ `saved_ge` ／ 使う判断を変える（示すことは同じ: 792/625 ≤ savedMinutes） ／ 取… | `saved_ge` | `saved_ge` |
| 78 | ／ `savedOverTuned_ge_gap` ／ 新設（印なし） ／ searchesPerDay .curren… | `savedOverTuned_ge_gap` | `savedOverTuned_ge_gap` |
| 79 | ／ `savedOverTuned_ge` ／ 新設（印なし） ／ 安い設定の変更に比べて取り戻せる時間は、1人1日1.… | `savedOverTuned_ge` | `savedOverTuned_ge` |
| 80 | ／ `yenPerDailyMinute_ge` ／ docstring の「1年で」を「初年度に」に変える ／ 4,1… | `yenPerDailyMinute_ge` | `yenPerDailyMinute_ge` |
| 81 | ／ `claim_C3_saved` ／ 型と使う判断を変える（@claim C3） ／ firstYearCost <… | `claim_C3_saved` | `claim_C3_saved` |
| 82 | ／ `claim_C3_lost` ／ 型と使う判断を変える（@claim C3） ／ firstYearCost < … | `claim_C3_lost` | `claim_C3_lost` |
| 83 | ／ `claim_C0_approvable` ／ 使う判断を変える（@claim C0。型は Approvable の… | `claim_C0_approvable` | `claim_C0_approvable` |
| 84 | ／ `baseline_lost_le_survey` ／ 使う判断を変える（@baseline。示すことは同じ: lo… | `baseline_lost_le_survey` | `baseline_lost_le_survey` |
| 85 | ／ `unfav_saved_le_gap` ／ 新設（印なし。docstring の先頭に [不利]） ／ saved… | `unfav_saved_le_gap` | `unfav_saved_le_gap` |
| 86 | ／ `unfav_saved_le_lost` ／ 使う判断を変える（示すことは同じ: savedMinutes ≤ l… | `unfav_saved_le_lost` | `unfav_saved_le_lost` |

## 命題が変わったのに名前が同じで、`@reviewer` が残っている公理

前の周の Reviewer の判断は、変わった命題には当てはまらない。名前を変えて別の公理にするべきか確かめる。

なし

## 設計書に名前の出ていない変更

- `missAfterIndex_nonneg`
- `miss_sub_notYet`
- `search_layers`

## 差分（unified diff）

```diff
--- rounds/01/Argument.lean
+++ Argument.lean
@@ -2,5 +2,5 @@
 # 論証のモデル: 社内Wiki検索の刷新提案
 
-設計書: `07-logic/model-plan.md`。主張: `05-claims.json`。事実: `06-facts.json`。
+設計書: `07-logic/model-plan.md` と、2周目の差分の設計書 `07-logic/model-plan-delta.md`。主張: `05-claims.json`。事実: `06-facts.json`。
 
 ## 書き方の約束（ガイド `stages/07-logic.md` の「Writer の約束」の要約）
@@ -23,30 +23,53 @@
 | 主張 | 主張の文 | 定理 | 種類 |
 |---|---|---|---|
-| C0 | 社内Wikiの検索を全文検索エンジンに置き換えるため、来期予算で300万円を承認してほしい | `claim_C0_approvable` | [確率] |
+| C0 | 社内Wikiの検索を全文検索エンジンに置き換えるため、来期予算で300万円を承認してほしい | `claim_C0_approvable`（比べる相手は、いまの仕組みのままでできる安い設定の変更 `tuned`） | [確率] |
 | C1 | いまの検索では、社員が探し物に多くの時間を使っている | `claim_C1_many` | [決定論] |
 | C2 | 置き換えれば、書いた記事がすぐ検索に出るようになる | `claim_C2_soon`（項1: 5秒以内）、`claim_C2_faster`（項2: いまより早い） | [決定論] |
-| C3 | 費用は、失われている時間に比べて小さい | `claim_C3_lost`（読み a: 失われている時間）、`claim_C3_saved`（読み b: 取り戻せる時間） | [確率] |
-
-印のない定理:
+| C3 | 費用は、失われている時間に比べて小さい | `claim_C3_lost`（読み a: 失われている時間）、`claim_C3_saved`（読み b: いまのままと比べて取り戻せる時間） | [確率] |
+
+主張の定理のほかの定理（`@claim` の印がないもの。`baseline_lost_le_survey` だけに `@baseline` の印を付けている）:
 
 | 定理 | 示すこと | 種類 |
 |---|---|---|
-| `baseline_lost_le_survey` | いまの検索の「失われている時間」を、アンケートの1日20分より大きく置いていない（比べる相手の確認） | [決定論] |
+| `rat_mul_le_mul` | 0 以上の数どうしの不等式を掛け合わせる（数の補題） | — |
+| `missAfterIndex_nonneg` | 層2か層3で失敗する確率は 0 以上（確率の範囲から出る式の補題） | — |
+| `miss_sub_notYet` | 見つからない確率 − 層1の確率 =（1 − 層1の確率）× 層2か層3で失敗する確率（`miss_compose` の式の変形） | — |
+| `search_layers` | 1日の探し物の時間を、層1の確率と「層2か層3で失敗する確率」で書き直した式（`search_decomp` と `miss_compose` の式の変形） | — |
+| `notYet_current_ge` | いまの検索で、まだ検索に出ていない記事を探す確率は 1/10 以上 | [確率] |
+| `notYet_tuned_ge` | 安い設定の変更をしても、まだ検索に出ていない記事を探す確率は 1/10 以上 | [確率] |
+| `notYet_fullText_le` | 置き換えた後、まだ検索に出ていない記事を探す確率は 1/1000 以下 | [確率] |
+| `lost_ge` | 失われている時間（読み a）は1人1日2分以上 | [確率] |
+| `saved_ge_gap` | 取り戻せる時間（読み b）は、層1の差に比例する式以上 | [確率] |
+| `saved_ge` | 取り戻せる時間（読み b）は1人1日1.2672分以上 | [確率] |
+| `savedOverTuned_ge_gap` | 安い設定の変更に比べて取り戻せる時間は、層1の差に比例する式以上 | [確率] |
+| `savedOverTuned_ge` | 安い設定の変更に比べて取り戻せる時間は1人1日1.2672分以上 | [確率] |
+| `yenPerDailyMinute_ge` | 1人1日1分の時間は、初年度に4,120,000円以上の人件費になる | [決定論] |
+| `baseline_lost_le_survey` | いまの検索の「失われている時間」を、アンケートの1日20分より大きく置いていない（比べる相手の確認。`@baseline`） | [決定論] |
 | `unfav_saved_le_survey` | 取り戻せる時間は、1日20分を超えない | [不利] |
+| `unfav_saved_le_gap` | 取り戻せる時間は、層1の差に比例する式を超えない | [不利] |
 | `unfav_saved_le_lost` | 取り戻せる時間は、失われている時間を超えない | [不利] |
-| `saved_only_from_notYet` | 取り戻せる時間は、層1（まだ検索に出ない）の確率の差からだけ生まれる | [確率]（[不利] の読みもある） |
-
-`baseline_lost_le_survey` には `@baseline` の印を付けている。
 
 ## 設計書（model-plan.md）との違い
 
-- 数の補題 `rat_mul_le_mul`（0 以上の数どうしの不等式を掛け合わせる）を §5 の先頭に足した。関係公理を使わない数学の補題で、
-  標準ライブラリの `grind` が積の単調性を解けないために置いた。現実についての判断は含まない。
-- 設計書の4節に載っている「同じとみなす」置き方の公理（`noHit_same`・`overlook_same`・`searches_same`・`foundMinutes_same`・
-  `missExtra_same`・`notYet_ge_of_slow`・`notYet_le_of_fast`）の docstring に「向き:」の行を足し、4節の向きを写した。
-- 設計書の3.1節は、`*_same` の5つの論拠と弱い点を「4節」に預けている。そこで、この5つの弱い点は、4節の向きの説明と
-  6節の不利な結論の説明から書いた。`missExtra_same` だけは設計書に弱い点の材料がないので、
-  「探し直しの時間は検索の仕組みで変わりうる（どちらの向きにも）」と、中立の向きに合わせて書いた。
-- ほかは、宣言・計算の def・関係公理・定理の名前と型、定理が使う関係公理は、設計書の2節・3節・5節のとおり。
+2周目は、model-plan.md と model-plan-delta.md が食い違うところは、差分の設計書に従った。そのうえでの違い:
+
+- 数の補題 `rat_mul_le_mul`（0 以上の数どうしの不等式を掛け合わせる）を §5 の先頭に置いている（1周目から）。
+  関係公理を使わない数学の補題で、標準ライブラリの `grind` が積の単調性を解けないために置いた。現実についての判断は含まない。
+- 式の補題を3つ足した。どれも設計書の6.1節の「Writer への注」に書かれた式の変形を、定理として切り出したもので、新しい判断は含まない。
+  - `missAfterIndex_nonneg`: `pNoHit`・`pOverlook` の確率の範囲（`Prob` の型）だけから出る。関係公理を使わない。
+  - `miss_sub_notYet`: 【自明】の `miss_compose` だけを使う。
+  - `search_layers`: 【自明】の `search_decomp` と `miss_compose` だけを使う。
+  - 3つとも、`saved_ge_gap`・`savedOverTuned_ge_gap`・`unfav_saved_le_gap`・`unfav_saved_le_lost`・`lost_ge` の証明で、同じ変形を繰り返さないために置いた。
+- `savedOverTuned_ge_gap` は、`saved_ge_gap` を途中の定理として使って示した（差分の6.1節の「saved_ge_gap と同じ判断に、tuned の6つを足したもの」のとおり、依存する関係公理は同じになる）。
+- `search_current_eq` の1行目（命題の文）を「検索で探し物をするのに使う時間」に直した。差分の設計書は論拠と弱い点だけを変えるとしているが、
+  3.1節で `searchMinutes` の意味を「検索で使う時間」に限ったので、1行目をそれに合わせた。
+- 差分の5節で向きを数え直した公理のうち、docstring に「向き:」の行がなかった `prodDelay_le_test`（新方式に有利）と `beneficiaries_ge`（新方式に不利）に、「向き:」の行を足した。
+- CLI は docstring の中の印の語を、文の途中でも印として読む。そこで、差分の設計書の文のうち印の語を含むものは、言い換えて写した。
+  `delay_current_ge_workday` の要ファクトの「（登録すれば @support に足せる）」は「（登録すれば、支える事実に足せる）」、
+  `current_not_incremental` の弱い点の「@against にも @support にも置けない」は「反対の証拠にも支える事実にも置けない」と書いた。
+- 重なる文を1つにまとめた（`prodDelay_le_test` の要ファクトの「本番の記事数の環境で測る」、`beneficiaries_ge` の論拠の「回答者だけを数えるのは不利な向き」）。
+  `workDays_ge` の向きの行からは、1周目との比べ（「1周目は控えめな値としていたが」）を外し、いまの判断だけを書いた。意味は変えていない。
+- 差分の設計書は、型を変える公理のうち `search_decomp`・`notYet_le_of_fast`・`approvable_of_net` の名前を変えていない。この3つには `@reviewer` の行がないので、
+  名前はそのままにした（`miss_compose` は種類だけを変え、型は変えていない）。
 -/
 
@@ -58,7 +81,12 @@
 /-! ## §1 帰納型（定義） -/
 
-/-- 比べる2つの方式。`current` はいまの検索の仕組み、`fullText` は置き換えた後の全文検索エンジン。 -/
+/-- 比べる3つの方式。
+`current` は、いまの検索の仕組み（中身が Elasticsearch などの全文検索エンジンかは、06-facts.json にない）。
+`tuned` は、いまの検索の仕組みのまま、300万円より安い費用でできる設定の変更（索引を作り直す間隔を短くする、保存のたびに索引へ足す、など）を、
+保存から検索に出るまでがいちばん短くなるように施したもの。そうした変更ができないなら、いまのままと同じもの。
+`fullText` は、置き換えた後の全文検索エンジン。 -/
 inductive Method where
   | current
+  | tuned
   | fullText
 
@@ -74,15 +102,21 @@
 axiom indexDelaySec : Method → Rat
 
-/-- 試験環境の全文検索エンジンで測った、保存から検索に出るまでの時間（秒）。
-本番の `indexDelaySec .fullText` とは別の量。試験環境の全文検索エンジンだけの量なので、方式を取らない。 -/
+/-- 試験環境の全文検索エンジンに記事を20件保存して測った、保存から検索に出るまでの時間の最大（秒）。F3 の最大4.2秒に当たる。
+本番の `indexDelaySec .fullText` とは別の量なので、方式を取らない。 -/
 axiom testDelaySec : Rat
+
+/-- いまの検索の仕組みは、記事を保存するたびに、その記事だけを索引に足せる（索引を丸ごと作り直さずに更新できる）。 -/
+axiom CurrentIncremental : Prop
+
+/-- その方式の検索が、Wiki のすべての記事を、閲覧できる人の検索に出る状態で索引に持っている（移行で記事や閲覧の権限が欠けていない）。 -/
+axiom IndexComplete : Method → Prop
 
 /-- 層1。探し物1回で、探す記事が、検索の時点でまだ検索に出ていない確率。 -/
 axiom pNotYet : Method → Prob
 
-/-- 層2。検索に出る状態の記事が、入れた語で引けない確率。 -/
+/-- 層2。索引に入っている記事を探したとき、入れた語でその記事を引けない確率。索引に入っていることを条件とした、条件付きの確率。 -/
 axiom pNoHit : Method → Prob
 
-/-- 層3。引けた記事を、結果の中で見落とす確率。 -/
+/-- 層3。引けた記事を、結果の中で見落とす確率。引けたことを条件とした、条件付きの確率。 -/
 axiom pOverlook : Method → Prob
 
@@ -94,13 +128,17 @@
 axiom searchesPerDay : Method → Rat
 
-/-- 見つかった探し物1回にかかる時間（分）。 -/
+/-- 見つかった探し物1回に、検索で使う時間（分）。 -/
 axiom foundMinutes : Method → Rat
 
-/-- 見つからなかった探し物1回で、見つかった場合より余分に探し物に使う時間（分）。
-探し直しや、ほかの場所を探す時間を含む。 -/
-axiom missExtraMinutes : Method → Rat
-
-/-- 社員1人が1日に探し物に使う時間（分）。F1 の「1日平均20分」は、この量の `current` の値。
-回数と時間への分け方は、関係公理 `search_decomp` に置く。 -/
+/-- 層1で見つからなかった（探す記事が、まだ検索に出ていなかった）探し物1回で、見つかった場合より余分に検索で使う時間（分）。
+検索の外の時間は入らない。 -/
+axiom extraNotYetMinutes : Method → Rat
+
+/-- 層2か層3で見つからなかった（語で引けなかった、見落とした）探し物1回で、見つかった場合より余分に検索で使う時間（分）。
+検索の外の時間は入らない。 -/
+axiom extraOtherMinutes : Method → Rat
+
+/-- 社員1人が1日に、検索で探し物をするのに使う時間（分）。検索の外でほかの場所を探す時間や、人に聞いて返事を待つ時間は入らない。
+F1 の「1日平均20分」は、この量の `current` の値。回数と時間への分け方は、関係公理 `search_decomp` に置く。 -/
 axiom searchMinutes : Method → Rat
 
@@ -109,5 +147,5 @@
 axiom beneficiaries : Rat
 
-/-- 1年の勤務日数。会社の量なので、方式を取らない。 -/
+/-- 初年度のうち、置き換えた検索を使える勤務日数（移行の期間を除く）。会社の量なので、方式を取らない。 -/
 axiom workDays : Rat
 
@@ -115,5 +153,9 @@
 axiom wagePerHour : Rat
 
-/-- 置き換えの初年度に、追加で必要な費用（円）。置き換える側にだけ現れる量なので、方式を取らない。 -/
+/-- 移行の初年度費用の見積もりの額（円）。置き換える側にだけ現れる量なので、方式を取らない。 -/
+axiom estimateYen : Rat
+
+/-- 置き換えの初年度に、実際に追加で必要になる費用（円）。置き換える側にだけ現れる量なので、方式を取らない。
+見積もりの額とは別の量で、2つの関係は関係公理 `cost_le_estimate` に置く。 -/
 axiom firstYearCost : Rat
 
@@ -121,6 +163,6 @@
 axiom manyMinutes : Rat
 
-/-- いまの検索の仕組みのまま、300万円より安い費用で、保存から検索に出るまでを5秒以内にできる。 -/
-axiom CheaperFix : Prop
+/-- 置き換えたとき、安い設定の変更（`tuned`）をした場合に比べて、会社が初年度に得る値打ち（円）。2つの方式の差の量なので、方式を取らない。 -/
+axiom gainYen : Rat
 
 /-- 部長が、来期予算で300万円を承認する理由がそろっている。 -/
@@ -129,7 +171,14 @@
 /-! ## §3 計算の def（手順だけ。判断を入れない） -/
 
-/-- 読み (a) の「失われている時間」（分）: いまの検索の、1日の探し物の回数 × 見つからない確率 × 見つからなかった1回の余分な時間。 -/
+/-- 方式 M で、索引に入っている記事を探して、層2か層3で失敗する確率: 1 −（1 − 層2の確率）×（1 − 層3の確率）。 -/
+def missAfterIndex (M : Method) : Rat :=
+  1 - (1 - (pNoHit M).val) * (1 - (pOverlook M).val)
+
+/-- 読み (a) の「失われている時間」（分）: いまの検索の、1日の探し物の回数 ×（層1で見つからない確率 × 層1の余分な時間 ＋
+（見つからない確率 − 層1で見つからない確率）× 層2・層3の余分な時間）。
+いまの検索で、見つからなかった探し物のために1人1日に余分に検索で使っている時間。 -/
 def lostMinutes : Rat :=
-  searchesPerDay .current * (missProb .current).val * missExtraMinutes .current
+  searchesPerDay .current * ((pNotYet .current).val * extraNotYetMinutes .current
+    + ((missProb .current).val - (pNotYet .current).val) * extraOtherMinutes .current)
 
 /-- 読み (b) の「取り戻せる時間」（分）: 1人1日の探し物の時間の、いまの検索と置き換えた後の差。 -/
@@ -137,26 +186,34 @@
   searchMinutes .current - searchMinutes .fullText
 
-/-- 1人1日1分の時間が、1年で何円の人件費になるか: 人数 × 勤務日数 × 1時間あたりの人件費 ÷ 60。 -/
+/-- 置き換えで、安い設定の変更をした場合に比べて、1人1日に取り戻せる時間（分）: 1人1日の探し物の時間の、安い設定の変更と置き換えた後の差。 -/
+def savedOverTunedMinutes : Rat :=
+  searchMinutes .tuned - searchMinutes .fullText
+
+/-- 1人1日1分の時間が、初年度（`workDays` の日数）でいくらの人件費になるか: 人数 × 勤務日数 × 1時間あたりの人件費 ÷ 60。 -/
 def yenPerDailyMinute : Rat :=
   beneficiaries * workDays * wagePerHour / 60
 
-/-- 読み (a) の時間の、1年分の人件費（円）。 -/
-def lostYen : Rat :=
+/-- 読み (a) の時間の、初年度の人件費（円）。 -/
+def lostWageYen : Rat :=
   yenPerDailyMinute * lostMinutes
 
-/-- 読み (b) の時間の、1年分の人件費（円）。 -/
-def benefitYen : Rat :=
+/-- 読み (b) の時間の、初年度の人件費（円）。会社の得ではなく、人件費に直した量。 -/
+def savedWageYen : Rat :=
   yenPerDailyMinute * savedMinutes
 
+/-- 安い設定の変更に比べて取り戻せる時間の、初年度の人件費（円）。 -/
+def savedOverTunedWageYen : Rat :=
+  yenPerDailyMinute * savedOverTunedMinutes
+
 /-! ## §4 関係公理 -/
 
 /-! ### 【実験】 -/
 
-/-- 【実験】いまの検索では、社員1人が1日に探し物に使う時間は20分。
+/-- 【実験】いまの検索では、社員1人が1日に、検索で探し物をするのに使う時間は20分。
 @support F1
 @confidence 0.75
 @reviewer 0.75 ← 0.95 理由: F1 が述べるのは「検索で探し物をするのに」使う時間。モデルの searchMinutes は、search_decomp と missExtraMinutes の宣言を通して、検索が失敗したあとに「ほかの場所を探す時間」も含む。F1 の20分がその時間を含むかは、設問5の文面（02-context/survey-2026.md。02-context に無い）で確かめられず、04-analysis.md は「探し物に1日平均20分」と書いて範囲が揺れている。数は確かめられ、範囲の一致は確かめられないので、partially_verified 相当にする
-論拠: 社内アンケート2026の設問5の集計で、1日平均20分。
-弱い点: 回答者412名の自己申告の平均。F1 の「探し物に使う時間」に入らない時間（人に聞いて返事を待つ時間など）は、モデルでも数えない（新方式に不利な向き）。 -/
+論拠: 社内アンケート2026の設問5「検索で探し物をするのに、1日に何分くらい使っていますか」の、回答者412名の平均が20分（survey-2026.md）。設問の範囲は「検索で探し物をする時間」で、`searchMinutes` の範囲（検索で使う時間に限った）と同じ。
+弱い点: 自己申告の平均。中央値は15分で、長く答えた人が平均を引き上げている。検索の外でほかの場所を探す時間や、人に聞いて待つ時間は、設問にもモデルにも入らない（新方式に不利な向き）。 -/
 axiom search_current_eq : searchMinutes .current = 20
 
@@ -167,12 +224,9 @@
 axiom testDelay_le_five : testDelaySec ≤ 5
 
-/-- 【実験】置き換えの初年度の費用は300万円。
+/-- 【実験】移行の初年度費用の見積もりの額は300万円。
 @support F4
-@confidence 0.3
-@reviewer 0.3 ← 0.6 理由: F4 が述べるのは「見積もりの金額が300万円」まで（ユーザーの証言）。宣言 firstYearCost は「初年度に追加で必要な費用」で、見積もりが社内作業・運用費を含むこと、実際の費用が見積もりを超えないことを述べた事実はない。等号のうち、見積もりの額は F4 で支えられ、見積もりが追加の費用のすべてであることは支えられない。見積書も 02-context/estimate.md に無く確かめられない
-論拠: 移行の初年度費用の見積もりが300万円。
-弱い点: 金額はユーザーの証言（F4 は user_asserted）。見積もりに、移行の社内作業の時間や、2年目以降の保守の費用が入っているかは分からない。
-要ファクト: 見積書で、金額と、費用に含まれる範囲を確かめる。 -/
-axiom cost_eq : firstYearCost = 3000000
+論拠: 移行の初年度費用の見積もりは300万円（F4）。estimate.md は、この見積もりが構築と移行作業を含むと書く。
+弱い点: 金額はユーザーの証言で、見積書はユーザーの手元にある（F4 の notes）。 -/
+axiom estimate_eq : estimateYen = 3000000
 
 /-! ### 【経験則】 -/
@@ -183,6 +237,6 @@
 @reviewer 0.3 ← 0.6 理由: F2 は不満の理由の割合で、遅れを測っていない。F2 が支えるのは「当日の記事が出ないことが多い」までで、8時間という下限は述べておらず、原因が遅れか並び（層3）かも分けていない。直接の根拠になりうる「夜間に1回だけ索引を作り直している」（02-context/sources.md の聞き取りメモ）は 06-facts.json に登録されていない
 論拠: F2 で、不満の理由の1位が「当日の記事が出てこない」（回答者の48%）。遅れが数分なら、この言い方にはならない。その日のうちに出ない、つまり勤務時間の1日分ほど遅れていると読める。
-弱い点: F2 は不満の理由で、遅れを測ったものではない。当日の記事が出ない原因が、並び（層3。新しい記事が結果の下のほうに出る）である可能性もある。
-要ファクト: いまの検索の、検索の対象を更新する間隔を、設定で確かめる。 -/
+弱い点: F2 は不満の理由で、遅れを測ったものではない。当日の記事が出ない原因が、並び（層3。新しい記事が結果の下のほうに出る）である可能性もある。聞き取りメモ（sources.md）は、「昨日書いた手順が検索で見つからない」という問い合わせが続いたと書く。夜間に作り直しているなら、昨日の記事は今日には検索に出るはずで、食い違う。原因は、作り直しの失敗か、層2・層3（語で引けない、並びで埋もれる）かもしれない。
+要ファクト: 聞き取りメモの「いまの検索は、夜間に1回だけ索引を作り直している」を事実として登録し、設定で確かめる（登録すれば、支える事実に足せる）。「昨日書いた手順が見つからない」の原因を、問い合わせの記録で確かめる。 -/
 axiom delay_current_ge_workday : 28800 ≤ indexDelaySec .current
 
@@ -190,14 +244,16 @@
 @support F1
 @confidence 0.9
-論拠: F1 の平均は回答者412名のもの（F1 の notes）。回答者は社員で、置き換え後も同じ検索を使う。社員全体ではなく回答者だけを数えるので、新方式に不利な向きの置き方になる。
-弱い点: 回答者のなかに、異動や退職で検索を使わなくなる人がいる。 -/
+論拠: F1 の平均は回答者412名のもの（F1 の notes）。回答者は社員で、置き換え後も同じ検索を使う。アンケートの対象は全社員480名で（survey-2026.md）、回答者の412名だけを数えるのは、新方式に不利な向きの置き方である。
+弱い点: 回答者のなかに、異動や退職で検索を使わなくなる人がいる。
+向き: 新方式に不利（効果を受ける人を少なめに数える）。 -/
 axiom beneficiaries_ge : 412 ≤ beneficiaries
 
 /-! ### 【自明】 -/
 
-/-- 【自明】どの方式でも、1日の探し物の時間 = 回数 ×（見つかった場合の時間 ＋ 見つからない確率 × 余分な時間）。
-論拠: `foundMinutes` を「見つかった探し物1回の平均の時間」、`missExtraMinutes` を「見つからなかった探し物1回の平均の余分な時間」と決めれば、全確率の公式でそのまま成り立つ。 -/
+/-- 【自明】どの方式でも、1日の探し物の時間 = 回数 ×（見つかった場合の時間 ＋ 層1で見つからない確率 × 層1の余分な時間 ＋（見つからない確率 − 層1で見つからない確率）× 層2・層3の余分な時間）。
+論拠: `foundMinutes` を「見つかった探し物1回の平均の時間」、それに `extraNotYetMinutes` を足したものを「層1で見つからなかった探し物1回の平均の時間」、`extraOtherMinutes` を足したものを「層2・層3で見つからなかった探し物1回の平均の時間」と決めれば、全確率の公式でそのまま成り立つ。層1で見つからない確率は `pNotYet`、層2・層3で見つからない確率は `missProb` − `pNotYet` で、2つは重ならない。 -/
 axiom search_decomp : ∀ M : Method,
-  searchMinutes M = searchesPerDay M * (foundMinutes M + (missProb M).val * missExtraMinutes M)
+  searchMinutes M = searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M
+    + ((missProb M).val - (pNotYet M).val) * extraOtherMinutes M)
 
 /-- 【自明】どの方式でも、1日の探し物の時間は0以上。
@@ -209,4 +265,13 @@
 axiom foundMinutes_nonneg : ∀ M : Method, 0 ≤ foundMinutes M
 
+/-- 【自明】どの方式でも、1日の探し物の回数は0以上。
+論拠: 回数は負にならない。 -/
+axiom searchesPerDay_nonneg : ∀ M : Method, 0 ≤ searchesPerDay M
+
+/-- 【自明】どの方式でも、探し物1回が見つからない確率 = 1 −（1 − 層1の確率）×（1 − 層2の確率）×（1 − 層3の確率）。
+論拠: `pNoHit` を「索引に入っている記事のうち、語で引けない割合」、`pOverlook` を「引けた記事のうち、見落とす割合」という条件付きの確率として宣言した。見つかるのは、索引に入っていて、語で引けて、見落とさないときだけなので、見つかる確率 =（1 − 層1）×（1 − 層2）×（1 − 層3）は、確率の連鎖律そのものである。3つの層が独立だという判断は要らない。 -/
+axiom miss_compose : ∀ M : Method,
+  (missProb M).val = 1 - (1 - (pNotYet M).val) * (1 - (pNoHit M).val) * (1 - (pOverlook M).val)
+
 /-! ### 【仮定】層1: まだ検索に出ない -/
 
@@ -214,75 +279,114 @@
 @support なし（本番と同じ記事数の環境で測った記録はない）
 @confidence 0.05
-論拠: 保存から検索に出るまでの時間は、主に検索の対象を更新する間隔で決まり、記事の数には大きく依らない、という一般の考え。
+論拠: 保存から検索に出るまでの時間は、主に検索の対象を更新する間隔で決まり、記事の数には大きく依らない、という一般の考え。試験環境は「本番と同じ構成」（trial.md）で、違うのは記事の数だけである。
 弱い点: 本番の記事数での計測ではない（F3 の notes）。記事が多いと更新に時間がかかることがある。
-要ファクト: 本番と同じ記事数の環境で、保存から検索に出るまでの時間を測る。 -/
+要ファクト: 本番の記事数（約3万件、trial.md）の環境で、保存から検索に出るまでの時間を測る。trial.md の「本番と同じ構成」を事実として登録する。
+向き: 新方式に有利。 -/
 axiom prodDelay_le_test : indexDelaySec .fullText ≤ testDelaySec
 
-/-- 【仮定】どの方式でも、保存から検索に出るまで8時間（28800秒）以上かかるなら、探し物のうち、まだ検索に出ていない記事を探すものは10%以上。
+/-- 【仮定】どの方式でも（いまの検索、安い設定の変更、置き換えた後のどれでも）、保存から検索に出るまで8時間（28800秒）以上かかるなら、探し物のうち、まだ検索に出ていない記事を探すものは10%以上。
 @support なし（探し物1回あたりの、その日の記事を探す割合を数えた記録はない）
 @confidence 0.05
 論拠: 遅れが8時間以上あれば、その日に保存された記事は、その日のうちには検索に出ない。F2 で48%が「当日の記事が出てこない」を挙げていて、当日の記事を探すことは珍しくない。
-向き: 中立。どの方式にも同じ形で当てはめる。社員がどれだけ新しい記事を探すかは、社員の仕事で決まり、検索の仕組みに依らない（設計書の4節）。
-弱い点: F2 は回答者に占める割合で、探し物1回あたりの割合は、どの事実にもない。10%は案の値で、`claim_C3_saved` が崩れる境目は約5.8%（設計書の5節）。
-要ファクト: いまの検索の記録（検索と閲覧の記録）で、探し物のうち、その日に保存された記事を探していたものの割合を数える。 -/
+向き: 中立。どの方式にも同じ形で当てはめる。社員がどれだけ新しい記事を探すかは、社員の仕事で決まり、検索の仕組みに依らない。ただし10%という量は、大きいほど新方式に有利。
+弱い点: F2 は回答者に占める割合で、探し物1回あたりの割合は、どの事実にもない。10%は案の値。結論が崩れる境目は、ほかの値をいまの案のままにすると約5.8%（current と比べる C3 でも、tuned と比べる C0 でも同じ）。「昨日書いた手順が見つからない」の原因が層2・層3なら、その日の記事を探す割合は10%を下回りうる。
+要ファクト: いまの検索の記録（検索と閲覧の記録）で、探し物のうち、その日に保存された記事を探していたものの割合を数える。「昨日書いた手順が見つからない」という問い合わせの原因を、問い合わせの記録で確かめる（delay_current_ge_workday と同じ）。 -/
 axiom notYet_ge_of_slow : ∀ M : Method, 28800 ≤ indexDelaySec M → 1 / 10 ≤ (pNotYet M).val
 
-/-- 【仮定】どの方式でも、保存から検索に出るまで5秒以内なら、まだ検索に出ていない記事を探すものは0.1%以下。
+/-- 【仮定】どの方式でも、保存から検索に出るまで5秒以内で、しかも移行で欠けた記事がないなら、まだ検索に出ていない記事を探すものは0.1%以下。
 @support なし（保存の直後に、その記事を探す検索を数えた記録はない）
 @confidence 0.05
 論拠: 記事を保存してから5秒以内に、その記事を探す人はほとんどいない。
 向き: 中立。どの方式にも同じ形で当てはめる。社員がどれだけ新しい記事を探すかは、社員の仕事で決まり、検索の仕組みに依らない（設計書の4節）。
-弱い点: 書いた本人が、保存した直後に検索で確かめることはある。
+弱い点: 書いた本人が、保存した直後に検索で確かめることはある。移行で欠けた記事は、遅れによらず検索に出ない。その分は前提の `IndexComplete` に分け、`fullText_complete` に置いた。
 要ファクト: 記事の保存から5秒以内に、その記事を探す検索がどれだけあるかを、記録で数える。 -/
-axiom notYet_le_of_fast : ∀ M : Method, indexDelaySec M ≤ 5 → (pNotYet M).val ≤ 1 / 1000
+axiom notYet_le_of_fast : ∀ M : Method, indexDelaySec M ≤ 5 → IndexComplete M → (pNotYet M).val ≤ 1 / 1000
+
+/-- 【仮定】置き換えた後の検索は、Wiki のすべての記事を、閲覧できる人の検索に出る状態で索引に持つ（移行で欠けない）。
+@support なし（移行の前後で、記事数と閲覧の権限を突き合わせた記録はない）
+@confidence 0.05
+論拠: 移行の作業には、記事と閲覧の権限を移すことが含まれる（estimate.md の「移行作業」）。
+弱い点: 本番の記事は約3万件ある（trial.md）。移行で記事や添付、閲覧の権限が欠けると、その記事は遅れによらず検索に出ない。
+要ファクト: 移行の試験で、移行の前後の記事数と閲覧の権限を突き合わせる。
+向き: 新方式に有利。新方式だけに起こる失敗を見込まない。 -/
+axiom fullText_complete : IndexComplete .fullText
+
+/-! ### 【仮定】安い設定の変更の速さ -/
+
+/-- 【仮定】いまの検索の仕組みは、記事を保存するたびに、その記事だけを索引に足すことができない。
+@support なし（いまの検索の仕組みの種類と、索引の更新の仕方を確かめた記録はない）
+@confidence 0.05
+論拠: 02-context/sources.md の聞き取りメモは「いまの検索は、夜間に1回だけ索引を作り直している」と書く。保存のたびに索引へ足せるなら、作り直しを待つ必要はない。
+弱い点: 03-reader.json の avoid_terms は、Elasticsearch を「いまの検索の仕組み」に言い換えるよう指定している。いまの仕組みが Elasticsearch なら、記事ごとに索引へ足せるのが普通で、この公理は誤りになる（棄却の候補）。夜間の作り直しは、仕組みの制約ではなく、設定かもしれない。03-reader.json と聞き取りメモは 06-facts.json の事実ではないので、反対の証拠にも支える事実にも置けない。
+要ファクト: いまの検索の仕組みが何か（Elasticsearch か）、記事を保存のたびに索引へ足す設定があるか、夜間に作り直している理由を、情報システム部に確かめる。聞き取りメモの「夜間に1回だけ索引を作り直している」を事実として登録する。
+向き: C0 に有利。 -/
+axiom current_not_incremental : ¬ CurrentIncremental
+
+/-- 【仮定】いまの仕組みが保存のたびに索引へ足せないなら、300万円より安い設定の変更では、保存から検索に出るまでを8時間（28800秒）より短くできない。
+@support なし（作り直しにかかる時間と、間隔を短くする費用を確かめた記録はない）
+@confidence 0.05
+論拠: 索引の丸ごとの作り直しには時間と負荷がかかるので、勤務時間中に何度も回せない。
+弱い点: 本番の記事は約3万件（trial.md）で、作り直しが数分で済むなら、1時間おきにも回せる。そうなら、安い設定の変更で当日の記事の問題（層1）のほとんどが解け、C0 は示せなくなる。
+要ファクト: 作り直し1回にかかる時間と負荷、勤務時間中に回せるか、間隔を短くする費用を、情報システム部に確かめる。
+向き: C0 に有利。 -/
+axiom tuned_slow_of_rebuild : ¬ CurrentIncremental → 28800 ≤ indexDelaySec .tuned
 
 /-! ### 【仮定】層2・層3: いまの検索の値 -/
 
-/-- 【仮定】いまの検索で、検索に出る状態の記事が、入れた語で引けない確率は20%以下。
+/-- 【仮定】いまの検索で、索引に入っている記事のうちで、入れた語で引けない割合（索引に入っていることを条件とした確率）は20%以下。
 @support なし（結果が0件だった検索の割合を数えた記録はない）
 @confidence 0.05
 論拠: いまの検索でも、探し物の多くは見つかっている（見つからなければ、1日20分では収まらない）。
-弱い点: 20%は案の値。
+弱い点: 20%は案の値。survey-2026.md の設問6で、回答者の35%が「言葉が少し違うと見つからない」を挙げた。回答者に占める割合で、探し物1回あたりの割合ではない。
 要ファクト: 検索の記録で、結果が0件だった検索の割合を数える。アンケートで、見つからなかった理由を聞く。 -/
 axiom noHit_current_le : (pNoHit .current).val ≤ 1 / 5
 
-/-- 【仮定】いまの検索で、引けた記事を結果の中で見落とす確率は20%以下。
+/-- 【仮定】いまの検索で、引けた記事のうちで、結果の中で見落とす割合（引けたことを条件とした確率）は20%以下。
 @support なし（結果は出たが記事を開かずに終わった検索を数えた記録はない）
 @confidence 0.05
 論拠: いまの検索でも、探し物の多くは見つかっている（見つからなければ、1日20分では収まらない）。
-弱い点: 20%は案の値。
+弱い点: 20%は案の値。survey-2026.md の設問6で、回答者の22%が「検索結果の並び順が役に立たない」を挙げた。回答者に占める割合で、探し物1回あたりの割合ではない。
 要ファクト: 検索の記録で、結果は出たが、どの記事も開かずに終わった検索の割合を数える。 -/
 axiom overlook_current_le : (pOverlook .current).val ≤ 1 / 5
 
-/-! ### 【仮定】層2・層3: 同じとみなす -/
-
-/-- 【仮定】語で引けない確率は、方式によらず同じ。
+/-! ### 【仮定】層2・層3: 置き換えで悪くならない（主張の側が使う片側） -/
+
+/-- 【仮定】置き換えても、索引に入っている記事を語で引けない確率は上がらない。
 @support なし（同じ検索語で2つの方式を比べた記録はない）
 @confidence 0.05
-論拠: 事実がないので、方式による違いを見込まない。
-向き: 新方式に不利。全文検索エンジンは本文の語でも引けるので下がる見込みがあるが、それを見込まない。
-弱い点: 全文検索エンジンのほうが語で引けるなら、層2からも効果が生まれ、取り戻せる時間は増える。
-要ファクト: 同じ検索語の組を、試験環境で2つの方式に入れ、引けた割合を比べる。 -/
-axiom noHit_same : pNoHit .fullText = pNoHit .current
-
-/-- 【仮定】見落とす確率は、方式によらず同じ。
+論拠: 全文検索エンジンは、本文の語でも引ける。いまの検索が本文の語で引けないなら、置き換えで下がる。いまの検索も本文の語で引ける（03-reader.json は「いまの検索の仕組み」を Elasticsearch の言い換えとしている）なら、同じ程度になる。どちらでも上がりはしない、とみなす。
+弱い点: 置き換えた後は、その日に書かれた新しい記事も索引に入る。新しい記事ほど語で引けにくい（題名や使う語が固まっていない）なら、索引に入っている記事のうちで引けない割合は上がる。1周目は miss_compose の弱い点に書いていたこの重なりを、ここに移した。語の切り方しだいで、「言葉が少し違うと見つからない」（survey-2026.md の設問6で回答者の35%）が増えることもある。
+要ファクト: 同じ検索語の組を試験環境で2つの方式に入れ、引けた割合を、新しい記事と古い記事に分けて比べる。
+向き: 新方式に有利（主張の側が使う）。 -/
+axiom noHit_full_le : (pNoHit .fullText).val ≤ (pNoHit .current).val
+
+/-- 【仮定】置き換えても、引けた記事を見落とす確率は上がらない。
 @support なし（同じ探し物で見落としを2つの方式で比べた記録はない）
 @confidence 0.05
-論拠: 事実がないので、方式による違いを見込まない。
-向き: 新方式に有利。本文の語でも引けると結果が増え、見落としが増える可能性を見込まない。
-弱い点: 全文検索エンジンで結果が増えて見落としが増えるなら、取り戻せる時間は小さくなる。
-要ファクト: 試験環境で社員に同じ探し物をしてもらい、結果の中から見つけられた割合を2つの方式で比べる。 -/
-axiom overlook_same : pOverlook .fullText = pOverlook .current
-
-/-! ### 【仮定】層の合成 -/
-
-/-- 【仮定】どの方式でも、探し物1回が見つからない確率 = 1 −（層1で失敗しない確率 × 層2で失敗しない確率 × 層3で失敗しない確率）。3つの層の失敗は独立。
-@support なし（見つからなかった探し物の理由の重なりを数えた記録はない）
-@confidence 0.05
-論拠: 記事がまだ出ていないこと、語で引けないこと、見落とすことは、別々の原因で起こる。3つの層の失敗が互いに重ならない（排反）とみなす置き方に比べると、独立とみなすほうが、取り戻せる時間を小さく見積もる（新方式に不利な向き）。
-弱い点: 新しい記事ほど語で引けにくい、などの重なりがありうる。
-要ファクト: 見つからなかった探し物の理由を1件ずつ記録し、理由が重なる割合を確かめる。 -/
-axiom miss_compose : ∀ M : Method,
-  (missProb M).val = 1 - (1 - (pNotYet M).val) * (1 - (pNoHit M).val) * (1 - (pOverlook M).val)
+論拠: 結果の並びの見やすさは、画面で決まる。
+弱い点: 本文の語でも引けると結果が増え、見落としが増える。「検索結果の並び順が役に立たない」は、設問6で回答者の22%。
+要ファクト: 試験環境で社員に同じ探し物をしてもらい、結果の中から見つけられた割合を2つの方式で比べる。
+向き: 新方式に有利（主張の側が使う）。 -/
+axiom overlook_full_le : (pOverlook .fullText).val ≤ (pOverlook .current).val
+
+/-! ### 【仮定】層2・層3: 置き換えでよくならない（不利な結論の側だけが使う片側） -/
+
+/-- 【仮定】置き換えても、索引に入っている記事を語で引けない確率は下がらない。
+@support なし（同じ検索語で2つの方式を比べた記録はない）
+@confidence 0.05
+論拠: 事実がないので、置き換えで語で引けるようになる分を見込まない。
+弱い点: いまの検索が本文の語で引けないなら、置き換えで層2はよくなり、この公理は崩れる。そのときは効果が層1の外からも生まれ、不利な結論 unfav_saved_le_gap は示せなくなる（新方式に有利な向きに外れる）。
+要ファクト: いまの検索の仕組みが本文の語で引けるかを、情報システム部に確かめる。同じ検索語の組を試験環境で2つの方式に入れ、引けた割合を、新しい記事と古い記事に分けて比べる。
+向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
+axiom noHit_full_ge : (pNoHit .current).val ≤ (pNoHit .fullText).val
+
+/-- 【仮定】置き換えても、引けた記事を見落とす確率は下がらない。
+@support なし（同じ探し物で見落としを2つの方式で比べた記録はない）
+@confidence 0.05
+論拠: 事実がないので、並びがよくなる分を見込まない。
+弱い点: 全文検索エンジンの並び（語の合い方の強い順）で見落としが減るなら崩れる。
+要ファクト: 試験環境で社員に同じ探し物をしてもらい、結果の中から見つけられた割合を2つの方式で比べる。
+向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
+axiom overlook_full_ge : (pOverlook .current).val ≤ (pOverlook .fullText).val
 
 /-! ### 【仮定】時間: いまの検索の値 -/
@@ -296,49 +400,190 @@
 axiom searches_current_ge : 4 ≤ searchesPerDay .current
 
-/-- 【仮定】いまの検索で、見つからなかった探し物1回は、見つかった場合より5分以上余分にかかる。
-@support なし（見つからなかったときの余分な時間を聞いた記録はない）
-@confidence 0.05
-論拠: 見つからないときは、語を変えて探し直したり、ほかの場所を探したりする。
-弱い点: 5分は案の値。
-要ファクト: アンケートで、探し物が見つからなかったときに余分にかかる時間を聞く。 -/
-axiom missExtra_current_ge : 5 ≤ missExtraMinutes .current
-
-/-! ### 【仮定】時間: 同じとみなす -/
-
-/-- 【仮定】探し物の回数は、方式によらず同じ。
+/-- 【仮定】いまの検索で、層1で見つからなかった（探す記事がまだ検索に出ていなかった）探し物1回は、見つかった場合より5分以上余分に検索で使う。
+@support なし（層1で見つからなかったときの余分な時間を聞いた記録はない）
+@confidence 0.05
+論拠: 当日の記事が検索に出ないときは、出ていないと気づくまで、語を変えて何度も探し直す。
+弱い点: 5分は案の値。早くあきらめて書いた人に聞けば、検索で使う時間は短い（そのあと人に聞く時間は、モデルの時間に入らない）。
+要ファクト: アンケートか聞き取りで、「当日の記事が検索に出なかったとき、検索に余分に何分使ったか」を聞く。見つからなかったとき全般ではなく、層1の失敗に向けて聞く。
+向き: 量の仮定。大きいほど新方式に有利。 -/
+axiom extraNotYet_current_ge : 5 ≤ extraNotYetMinutes .current
+
+/-- 【仮定】いまの検索で、層1で見つからなかった探し物の余分な時間は0以上。
+@support なし（層1で見つからなかったときの余分な時間を聞いた記録はない）
+@confidence 0.05
+論拠: 探す記事が出てこないときは、見つかったときより検索に長くかかる。
+弱い点: 検索で使う時間だけを数えるので、すぐにあきらめれば、見つかったとき（記事を開いて読む時間を含む）より短いことがある。
+要ファクト: extraNotYet_current_ge と同じ聞き取り（当日の記事が検索に出なかったとき、検索に余分に何分使ったか）で確かめる。
+向き: 符号だけの仮定。extraNotYet_current_ge から導けるが、不利な結論の定理が「5分以上」という量の仮定を通らずに済むように、別に置く。 -/
+axiom extraNotYet_nonneg : 0 ≤ extraNotYetMinutes .current
+
+/-- 【仮定】いまの検索で、層2・層3で見つからなかった（語で引けなかった、見落とした）探し物の余分な時間は0以上。
+@support なし（層2・層3で見つからなかったときの余分な時間を聞いた記録はない）
+@confidence 0.05
+論拠: 語が合わないときや見落としたときも、見つかるまでより長く探す。
+弱い点: すぐにあきらめれば、見つかったときより短いことがある。
+要ファクト: 見つからなかったときの余分な時間を、理由（当日の記事か、語が合わないか、見落としか）ごとに聞く。
+向き: 符号だけの仮定。主張の側と不利な結論の側の両方で、積の大小をそろえるために使う。 -/
+axiom extraOther_nonneg : 0 ≤ extraOtherMinutes .current
+
+/-- 【仮定】いまの検索で、層2・層3で見つからなかったときの余分な時間は、層1で見つからなかったときの余分な時間を超えない。
+@support なし（層2・層3で見つからなかったときの余分な時間を聞いた記録はない）
+@confidence 0.05
+論拠: 語が合わないときや見落としたときは、語を変えれば見つかることが多い。当日の記事は、どう探しても出てこないので、探し直しが長くなる。
+弱い点: 語を変えても見つからず、長く探し続けることもある。
+要ファクト: 見つからなかったときの余分な時間を、理由（当日の記事か、語が合わないか、見落としか）ごとに聞き（extraOther_nonneg と同じ聞き取り）、2つの時間を比べる。
+向き: 新方式に有利。置き換えで層1の失敗が減ると、その一部は層2・層3の失敗に移る（記事は出るが、語で引けない、見落とす）。その分の余分な時間を小さく見る。 -/
+axiom extraOther_le_notYet : extraOtherMinutes .current ≤ extraNotYetMinutes .current
+
+/-! ### 【仮定】時間: 置き換えで悪くならない（主張の側が使う片側） -/
+
+/-- 【仮定】置き換えても、1人1日の探し物の回数は増えない。
 @support なし（試験導入の前後で検索の回数を比べた記録はない）
 @confidence 0.05
 論拠: 探し物の回数は仕事の中身で決まり、検索の仕組みでは大きく変わらない。
-向き: 新方式に有利。見つかりやすくなって検索の回数が増え、時間が増える分を見込まない。
-弱い点: 置き換えで検索が使いやすくなると、回数が増えることがある。そのときは、取り戻せる時間はさらに小さくなる（設計書の6節）。
-要ファクト: 試験導入の前後で、1人1日あたりの検索の回数を比べる。 -/
-axiom searches_same : searchesPerDay .fullText = searchesPerDay .current
-
-/-- 【仮定】見つかった探し物1回の時間は、方式によらず同じ。
+弱い点: 検索が役に立つようになると、人に聞く代わりに検索を使う回数が増える。
+要ファクト: 試験導入の前後で、1人1日あたりの検索の回数を比べる。
+向き: 新方式に有利（主張の側が使う）。 -/
+axiom searches_full_le : searchesPerDay .fullText ≤ searchesPerDay .current
+
+/-- 【仮定】置き換えても、見つかった探し物1回の時間は延びない。
 @support なし（同じ探し物にかかる時間を2つの方式で測った記録はない）
 @confidence 0.05
 論拠: 見つかった後に記事を開いて読む時間は、記事で決まる。
-向き: 決まらない。結果が増えて選ぶ時間が延びれば新方式に有利な置き方、並びがよくなって縮めば新方式に不利な置き方。
-弱い点: 見つかる探し物まで速くなるなら、取り戻せる時間は増え、`unfav_saved_le_lost` は崩れることがある。
-要ファクト: 試験環境で、同じ探し物にかかる時間を2つの方式で測る。 -/
-axiom foundMinutes_same : foundMinutes .fullText = foundMinutes .current
-
-/-- 【仮定】見つからなかった探し物の余分な時間は、方式によらず同じ。
-@support なし（見つからなかった後の行動を聞いた記録はない）
-@confidence 0.05
-論拠: 見つからなかった後の行動（探し直す、ほかの場所を探す）は、検索の仕組みに依らない。
-向き: 中立。
-弱い点: 探し直しの時間は、検索の仕組みで変わりうる（探し直しが速くなれば短くなり、結果が増えて選ぶのに手間取れば長くなる）。
-要ファクト: 見つからなかった後に何をしているか（探し直す・ほかの場所を探す）を、アンケートで聞く。 -/
-axiom missExtra_same : missExtraMinutes .fullText = missExtraMinutes .current
+弱い点: 本文の語でも引けると結果が増え、選ぶ時間が延びる。
+要ファクト: 試験環境で、同じ探し物にかかる時間を2つの方式で測る。
+向き: 新方式に有利（主張の側が使う）。 -/
+axiom found_full_le : foundMinutes .fullText ≤ foundMinutes .current
+
+/-- 【仮定】置き換えても、層1で見つからなかったときの余分な時間は延びない。
+@support なし（層1で見つからなかったときの時間を2つの方式で比べた記録はない）
+@confidence 0.05
+論拠: 当日の記事が出ないときの探し直し方は、検索の仕組みに依らない。
+弱い点: 置き換えた後は層1の失敗がまれ（0.1%以下）なので、この時間が効くのはその分だけである。
+要ファクト: アンケートか聞き取りで、「当日の記事が検索に出なかったとき、検索に余分に何分使ったか」を聞く（extraNotYet_current_ge と同じ聞き取り）。
+向き: 新方式に有利（主張の側が使う）。 -/
+axiom extraNotYet_full_le : extraNotYetMinutes .fullText ≤ extraNotYetMinutes .current
+
+/-- 【仮定】置き換えても、層2・層3で見つからなかったときの余分な時間は延びない。
+@support なし（見つからなかったときの探し直しの時間を2つの方式で比べた記録はない）
+@confidence 0.05
+論拠: 語が合わないときや見落としたときの探し直し方は、検索の仕組みで大きく変わらない。
+弱い点: 結果が増えると、探し直しで結果を見直す時間が延びる。
+要ファクト: 試験環境で、見つからなかったときの探し直しの時間を2つの方式で比べる。
+向き: 新方式に有利（主張の側が使う）。 -/
+axiom extraOther_full_le : extraOtherMinutes .fullText ≤ extraOtherMinutes .current
+
+/-! ### 【仮定】時間: 置き換えでよくならない（不利な結論の側だけが使う片側） -/
+
+/-- 【仮定】置き換えても、1人1日の探し物の回数は減らない。
+@support なし（試験導入の前後で検索の回数を比べた記録はない）
+@confidence 0.05
+論拠: 探し物の回数は仕事の中身で決まり、検索の仕組みでは大きく変わらない。
+弱い点: 探し直しが減れば、回数は減る。
+要ファクト: 試験導入の前後で、1人1日あたりの検索の回数を比べる。
+向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
+axiom searches_full_ge : searchesPerDay .current ≤ searchesPerDay .fullText
+
+/-- 【仮定】置き換えても、見つかった探し物1回の時間は縮まない。
+@support なし（同じ探し物にかかる時間を2つの方式で測った記録はない）
+@confidence 0.05
+論拠: 見つかった後に記事を開いて読む時間は、記事で決まる。
+弱い点: 並びがよくなれば、見つかるまでが短くなる。
+要ファクト: 試験環境で、同じ探し物にかかる時間を2つの方式で測る。
+向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
+axiom found_full_ge : foundMinutes .current ≤ foundMinutes .fullText
+
+/-- 【仮定】置き換えても、層1で見つからなかったときの余分な時間は縮まない。
+@support なし（層1で見つからなかったときの時間を2つの方式で比べた記録はない）
+@confidence 0.05
+論拠: 当日の記事が出ないときの探し直し方は、検索の仕組みに依らない。
+弱い点: 置き換えた後は層1の失敗がまれ（0.1%以下）なので、この時間が効くのはその分だけである。
+要ファクト: アンケートか聞き取りで、「当日の記事が検索に出なかったとき、検索に余分に何分使ったか」を聞く（extraNotYet_current_ge と同じ聞き取り）。
+向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
+axiom extraNotYet_full_ge : extraNotYetMinutes .current ≤ extraNotYetMinutes .fullText
+
+/-- 【仮定】置き換えても、層2・層3で見つからなかったときの余分な時間は縮まない。
+@support なし（見つからなかったときの探し直しの時間を2つの方式で比べた記録はない）
+@confidence 0.05
+論拠: 語が合わないときや見落としたときの探し直し方は、検索の仕組みで大きく変わらない。
+弱い点: 本文の語でも引けると、探し直しが早く済む。
+要ファクト: 試験環境で、見つからなかったときの探し直しの時間を2つの方式で比べる。
+向き: 新方式に不利（不利な結論の定理だけが使う）。 -/
+axiom extraOther_full_ge : extraOtherMinutes .current ≤ extraOtherMinutes .fullText
+
+/-! ### 【仮定】安い設定の変更は、層1のほかの点でよくならない（C0 の側だけが使う片側） -/
+
+/-- 【仮定】安い設定の変更をしても、1人1日の探し物の回数は減らない。
+@support なし（設定の変更で何が変わるかを確かめた記録はない）
+@confidence 0.05
+論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
+弱い点: 当日の記事が見つかるようになって探し直しが減れば、回数が減る。
+要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
+向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
+axiom searches_tuned_ge : searchesPerDay .current ≤ searchesPerDay .tuned
+
+/-- 【仮定】安い設定の変更をしても、見つかった探し物1回の時間は縮まない。
+@support なし（設定の変更で何が変わるかを確かめた記録はない）
+@confidence 0.05
+論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
+弱い点: 設定の変更と同時に並びの設定も直せば、短くなる。
+要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
+向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
+axiom found_tuned_ge : foundMinutes .current ≤ foundMinutes .tuned
+
+/-- 【仮定】安い設定の変更をしても、層1で見つからなかったときの余分な時間は縮まない。
+@support なし（設定の変更で何が変わるかを確かめた記録はない）
+@confidence 0.05
+論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
+弱い点: 遅れが短くなって「もう少し待てば出る」と分かれば、探し直しが短くなる。
+要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
+向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
+axiom extraNotYet_tuned_ge : extraNotYetMinutes .current ≤ extraNotYetMinutes .tuned
+
+/-- 【仮定】安い設定の変更をしても、層2・層3で見つからなかったときの余分な時間は縮まない。
+@support なし（設定の変更で何が変わるかを確かめた記録はない）
+@confidence 0.05
+論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
+弱い点: 設定の変更と同時に語の引き方や並びの設定も直せば、短くなる。
+要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
+向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
+axiom extraOther_tuned_ge : extraOtherMinutes .current ≤ extraOtherMinutes .tuned
+
+/-- 【仮定】安い設定の変更をしても、索引に入っている記事を語で引けない確率は下がらない。
+@support なし（設定の変更で何が変わるかを確かめた記録はない）
+@confidence 0.05
+論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
+弱い点: 設定の変更と同時に語の切り方（辞書）も直せば、下がる。
+要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
+向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
+axiom noHit_tuned_ge : (pNoHit .current).val ≤ (pNoHit .tuned).val
+
+/-- 【仮定】安い設定の変更をしても、引けた記事を見落とす確率は下がらない。
+@support なし（設定の変更で何が変わるかを確かめた記録はない）
+@confidence 0.05
+論拠: 安い設定の変更は、索引を更新する時機だけを変える。検索の画面、語の引き方、並び方、社員の探し方は変えない。
+弱い点: 設定の変更と同時に並びの設定も直せば、下がる。
+要ファクト: 設定の変更で、索引の更新の時機のほかに何が変わるかを、情報システム部に確かめる。
+向き: C0 に有利。安い設定の変更が、層1のほかの点でもよくなる分を見込まない。 -/
+axiom overlook_tuned_ge : (pOverlook .current).val ≤ (pOverlook .tuned).val
 
 /-! ### 【仮定】金額に直す -/
 
-/-- 【仮定】1年の勤務日数は200日以上。
-@support なし（会社の年間の所定労働日数を確かめた記録はない）
-@confidence 0.05
-論拠: 多くの会社の年間の勤務日数は200日より多いので、控えめな値にした。
-弱い点: 初年度は移行の期間があれば、新しい検索を使える日数は減る。
-要ファクト: 会社の年間の所定労働日数を、人事に確かめる。 -/
+/-- 【仮定】置き換えの初年度に実際に追加で要る費用は、見積もりの額を超えない。
+@support なし（見積もりが、初年度に追加で要る費用のすべてを含むことを述べた事実はない。F4 は額だけを述べる）
+@confidence 0.05
+論拠: estimate.md は、見積もりが構築と移行作業を含むと書く。主な費用は見積もりに入っている。
+弱い点: 社内の担当者の作業時間や、運用の費用（サーバー、保守、使用料）が入っているかは分からない。実際の費用が見積もりを超えることもある。
+要ファクト: 見積書で、費用に含まれる範囲（社内の作業時間、運用の費用、使用料）を確かめる。estimate.md の「構築と移行作業を含む」を事実として登録する。
+向き: 新方式に有利。見積もりを超える分を見込まない。 -/
+axiom cost_le_estimate : firstYearCost ≤ estimateYen
+
+/-- 【仮定】初年度のうち、置き換えた検索を使える勤務日数は200日以上。
+@support なし（会社の年間の所定労働日数と、移行にかかる期間を確かめた記録はない）
+@confidence 0.05
+論拠: 年間の勤務日数は200日より多い。移行の期間を差し引いても、200日を下回らない見込み。
+弱い点: 移行に2か月ほどかかれば、200日を下回りうる。
+要ファクト: 会社の年間の所定労働日数と、移行にかかる期間を確かめる。
+向き: 新方式に有利。比べているのは初年度の費用と初年度の効果で、移行の期間の分だけ日数は減る。 -/
 axiom workDays_ge : 200 ≤ workDays
 
@@ -351,4 +596,13 @@
 axiom wage_ge : 3000 ≤ wagePerHour
 
+/-- 【仮定】置き換えで会社が得る値打ちは、安い設定の変更に比べて取り戻せる時間の人件費を下回らない。
+@support なし（取り戻した時間を会社の値打ちとして数える基準を確かめた記録はない）
+@confidence 0.05
+論拠: 会社は社員の時間に人件費を払っている。取り戻した時間がほかの仕事に使われれば、少なくとも人件費の分の値打ちを生む。
+弱い点: 取り戻せる時間は1人1日約1.3分で、細切れの時間はほかの仕事に回らないことがある。費用対効果に厳しい読者（03-reader.json）が、最初に尋ねうる点である。
+要ファクト: 社内のほかの投資の判断で、節約した時間を人件費で金額に直しているか、部会がその換算を認めるかを、ユーザーに確かめる。
+向き: 新方式に有利。 -/
+axiom gain_ge_wage : savedOverTunedWageYen ≤ gainYen
+
 /-! ### 【仮定】読者の判断 -/
 
@@ -361,23 +615,16 @@
 axiom many_threshold_le : manyMinutes ≤ 20
 
-/-- 【仮定】いまの検索の仕組みのまま、300万円より安く、保存から検索に出るまでを5秒以内にする方法はない。
-@support なし（いまの仕組みで更新の間隔を短くできるかを確かめた記録はない）
-@confidence 0.05
-論拠: 06-facts.json に、いまの仕組みで遅れを短くできるという事実はない。
-弱い点: いまの仕組みの設定を変えるだけで、更新の間隔を短くできる可能性がある。そうなら、置き換えの効果（層1の差）の多くは、安い方法でも得られる（`saved_only_from_notYet`）。
-要ファクト: いまの仕組みで更新の間隔を短くできるか、できるならその費用を、情報システム部の担当者に確かめる。 -/
-axiom no_cheaper_fix : ¬ CheaperFix
-
-/-- 【仮定】1年分の取り戻せる時間の人件費が初年度の費用を上回り、しかも、もっと安い方法がないなら、部長が承認する理由はそろう。
+/-- 【仮定】置き換えで会社が得る値打ち（安い設定の変更に比べた分）が初年度の費用を上回るなら、部長が承認する理由はそろう。
 @support なし（部会での予算の判断の基準を確かめた記録はない）
 @confidence 0.05
-論拠: 読者は費用対効果に厳しく、「承認するかどうかを判断できる」ことを求めている（03-reader.json）。
+論拠: 読者は費用対効果に厳しく、承認するかどうかを判断できることを求めている（03-reader.json）。`gainYen` は安い設定の変更に比べた値打ちなので、「もっと安い方法で足りるのでは」という問いにも答えている。安い設定の変更の費用（0円以上）を差し引かずに比べるので、差額で比べるより厳しい比べ方になる。
 弱い点: 03-reader.json は読者像で、06-facts.json の事実ではない。予算の枠や、ほかの案件との優先度で判断が変わりうる。
-要ファクト: 部会での予算の判断の基準を、ユーザーに確かめる（費用対効果のほかに、予算の枠や、ほかの案件との優先度があるか）。 -/
-axiom approvable_of_net : firstYearCost < benefitYen → ¬ CheaperFix → Approvable
+要ファクト: 部会での予算の判断の基準（費用対効果のほかに、予算の枠や優先度があるか）を、ユーザーに確かめる。
+向き: 新方式に有利（判断の基準）。 -/
+axiom approvable_of_net : firstYearCost < gainYen → Approvable
 
 /-! ## §5 主張の定理 -/
 
-/-! ### 数の補題（関係公理を使わない） -/
+/-! ### 数と式の補題 -/
 
 /-- 0 以上の数どうしの不等式は、掛け合わせても成り立つ（a ≤ b、c ≤ d ならば a × c ≤ b × d）。 -/
@@ -388,4 +635,32 @@
   grind
 
+/-- どの方式でも、層2か層3で失敗する確率は 0 以上（層2・層3の確率の範囲だけから出る）。 -/
+theorem missAfterIndex_nonneg : ∀ M : Method, 0 ≤ missAfterIndex M := by
+  intro M
+  unfold missAfterIndex
+  have hb0 := (pNoHit M).nonneg
+  have hb1 := (pNoHit M).le_one
+  have hc0 := (pOverlook M).nonneg
+  have hc1 := (pOverlook M).le_one
+  have hx : (1 - (pNoHit M).val) * (1 - (pOverlook M).val) ≤ 1 * 1 :=
+    rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+  grind
+
+/-- どの方式でも、見つからない確率 − 層1の確率 =（1 − 層1の確率）× 層2か層3で失敗する確率（`miss_compose` の式の変形）。 -/
+theorem miss_sub_notYet : ∀ M : Method,
+    (missProb M).val - (pNotYet M).val = (1 - (pNotYet M).val) * missAfterIndex M := by
+  intro M
+  unfold missAfterIndex
+  rw [miss_compose M]
+  grind
+
+/-- どの方式でも、1日の探し物の時間 = 回数 ×（見つかった場合の時間 ＋ 層1の確率 × 層1の余分な時間 ＋
+（1 − 層1の確率）× 層2か層3で失敗する確率 × 層2・層3の余分な時間）（`search_decomp` と `miss_compose` の式の変形）。 -/
+theorem search_layers : ∀ M : Method,
+    searchMinutes M = searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M
+      + (1 - (pNotYet M).val) * missAfterIndex M * extraOtherMinutes M) := by
+  intro M
+  rw [search_decomp M, miss_sub_notYet M]
+
 /-! ### 途中の定理 -/
 
@@ -393,4 +668,8 @@
 theorem notYet_current_ge : 1 / 10 ≤ (pNotYet .current).val :=
   notYet_ge_of_slow .current delay_current_ge_workday
+
+/-- 安い設定の変更をしても、まだ検索に出ていない記事を探す確率は 1/10 以上。 -/
+theorem notYet_tuned_ge : 1 / 10 ≤ (pNotYet .tuned).val :=
+  notYet_ge_of_slow .tuned (tuned_slow_of_rebuild current_not_incremental)
 
 /-- 置き換えた後、まだ検索に出ていない記事を探す確率は 1/1000 以下。 -/
@@ -398,70 +677,213 @@
   have h1 := prodDelay_le_test
   have h2 := testDelay_le_five
-  exact notYet_le_of_fast .fullText (by grind)
-
-/-- いまの検索で、探し物1回が見つからない確率は 1/10 以上（層2・層3の値によらず、層1の確率以上になる）。 -/
-theorem miss_current_ge : 1 / 10 ≤ (missProb .current).val := by
-  have hm := miss_compose .current
-  have ha := notYet_current_ge
-  have ha1 := (pNotYet .current).le_one
-  have hb0 := (pNoHit .current).nonneg
-  have hb1 := (pNoHit .current).le_one
-  have hc0 := (pOverlook .current).nonneg
-  have hc1 := (pOverlook .current).le_one
-  have hx : (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) ≤ 1 * 1 :=
-    rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
-  have hy : (1 - (pNotYet .current).val) * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val))
-      ≤ (1 - (pNotYet .current).val) * (1 * 1) :=
-    Rat.mul_le_mul_of_nonneg_left hx (by grind)
-  grind
-
-/-- いまの検索の「失われている時間」（読み a）は、1人1日2分以上（4回 × 1/10 × 5分）。 -/
+  exact notYet_le_of_fast .fullText (by grind) fullText_complete
+
+/-- いまの検索の「失われている時間」（読み a）は、1人1日2分以上（4回 × 1/10 × 5分。層2・層3の分は0以上なので落とす）。 -/
 theorem lost_ge : 2 ≤ lostMinutes := by
   unfold lostMinutes
   have hs := searches_current_ge
-  have hm := miss_current_ge
-  have he := missExtra_current_ge
-  have h1 : 4 * (1 / 10) ≤ searchesPerDay .current * (missProb .current).val :=
-    rat_mul_le_mul (by grind) hs (by grind) hm
-  have h2 : 4 * (1 / 10) * 5 ≤ searchesPerDay .current * (missProb .current).val * missExtraMinutes .current :=
-    rat_mul_le_mul (by grind) h1 (by grind) he
-  grind
-
-/-- 取り戻せる時間（読み b）= 回数 × 余分な時間 ×（層2で失敗しない確率 × 層3で失敗しない確率）×（層1の確率の差）。
-取り戻せる時間は、層1の差からだけ生まれる。 -/
-theorem saved_only_from_notYet :
-    savedMinutes = searchesPerDay .current * missExtraMinutes .current
-      * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val))
-      * ((pNotYet .current).val - (pNotYet .fullText).val) := by
+  have ha := notYet_current_ge
+  have he := extraNotYet_current_ge
+  have ho := extraOther_nonneg
+  have hL := miss_sub_notYet .current
+  have hA := missAfterIndex_nonneg .current
+  have ha1 := (pNotYet .current).le_one
+  have hm : 0 ≤ (missProb .current).val - (pNotYet .current).val := by
+    rw [hL]
+    exact Rat.mul_nonneg (by grind) hA
+  have h1 : (1 / 10) * 5 ≤ (pNotYet .current).val * extraNotYetMinutes .current :=
+    rat_mul_le_mul (by grind) ha (by grind) he
+  have h2 : 0 ≤ ((missProb .current).val - (pNotYet .current).val) * extraOtherMinutes .current :=
+    Rat.mul_nonneg hm ho
+  have h3 : 4 * ((1 / 10) * 5) ≤ searchesPerDay .current * ((pNotYet .current).val * extraNotYetMinutes .current
+      + ((missProb .current).val - (pNotYet .current).val) * extraOtherMinutes .current) :=
+    rat_mul_le_mul (by grind) hs (by grind) (by grind)
+  grind
+
+/-- 取り戻せる時間（読み b）は、回数(いま) ×（層1の確率の差）×（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）以上。
+置き換えた後の量を、主張の側の片側の公理で、いまの検索の値に置き換えた上界から出す。 -/
+theorem saved_ge_gap :
+    searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val)
+      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current)
+      ≤ savedMinutes := by
   unfold savedMinutes
-  rw [search_decomp .current, search_decomp .fullText, miss_compose .current, miss_compose .fullText,
-    searches_same, foundMinutes_same, missExtra_same, noHit_same, overlook_same]
-  grind
-
-/-- 取り戻せる時間（読み b）は、1人1日 792/625 分（1.2672分）以上（4回 × 5分 ×（4/5 × 4/5）×（1/10 − 1/1000））。 -/
+  rw [search_layers .current, search_layers .fullText]
+  have hsf := searchesPerDay_nonneg .fullText
+  have hfc := foundMinutes_nonneg .current
+  have he1 := extraNotYet_current_ge
+  have he2 := extraOther_nonneg
+  have hs := searches_full_le
+  have hf := found_full_le
+  have hx1 := extraNotYet_full_le
+  have hx2 := extraOther_full_le
+  have hb := noHit_full_le
+  have hc := overlook_full_le
+  have hAf := missAfterIndex_nonneg .fullText
+  have hAc := missAfterIndex_nonneg .current
+  have hp0 := (pNotYet .fullText).nonneg
+  have hp1 := (pNotYet .fullText).le_one
+  have hA : missAfterIndex .fullText ≤ missAfterIndex .current := by
+    unfold missAfterIndex
+    have hb1 := (pNoHit .current).le_one
+    have hc1 := (pOverlook .current).le_one
+    have hx : (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val)
+        ≤ (1 - (pNoHit .fullText).val) * (1 - (pOverlook .fullText).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have h1 : (pNotYet .fullText).val * extraNotYetMinutes .fullText
+      ≤ (pNotYet .fullText).val * extraNotYetMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_left hx1 hp0
+  have h2a : missAfterIndex .fullText * extraOtherMinutes .fullText
+      ≤ missAfterIndex .fullText * extraOtherMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_left hx2 hAf
+  have h2b : missAfterIndex .fullText * extraOtherMinutes .current
+      ≤ missAfterIndex .current * extraOtherMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_right hA he2
+  have h3 : (1 - (pNotYet .fullText).val) * (missAfterIndex .fullText * extraOtherMinutes .fullText)
+      ≤ (1 - (pNotYet .fullText).val) * (missAfterIndex .current * extraOtherMinutes .current) :=
+    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
+  have hG : foundMinutes .fullText + (pNotYet .fullText).val * extraNotYetMinutes .fullText
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .fullText * extraOtherMinutes .fullText
+      ≤ foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have hG0a : 0 ≤ (pNotYet .fullText).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 (by grind)
+  have hG0b : 0 ≤ (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current :=
+    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
+  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have h4 := Rat.mul_le_mul_of_nonneg_left hG hsf
+  have h5 := Rat.mul_le_mul_of_nonneg_right hs hG0
+  grind
+
+/-- 取り戻せる時間（読み b）は、1人1日 792/625 分（1.2672分）以上（4回 ×（1/10 − 1/1000）×（16/25 × 5分））。 -/
 theorem saved_ge : 792 / 625 ≤ savedMinutes := by
-  rw [saved_only_from_notYet]
+  have hg := saved_ge_gap
   have hs := searches_current_ge
-  have he := missExtra_current_ge
+  have he1 := extraNotYet_current_ge
+  have hle := extraOther_le_notYet
+  have he2 := extraOther_nonneg
   have hb := noHit_current_le
   have hc := overlook_current_le
   have ha := notYet_current_ge
   have hf := notYet_fullText_le
-  have hx : (4 / 5) * (4 / 5) ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
-    rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
-  have h1 : 4 * 5 ≤ searchesPerDay .current * missExtraMinutes .current :=
-    rat_mul_le_mul (by grind) hs (by grind) he
-  have h2 : 4 * 5 * ((4 / 5) * (4 / 5))
-      ≤ searchesPerDay .current * missExtraMinutes .current
-        * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val)) :=
-    rat_mul_le_mul (by grind) h1 (by grind) hx
-  have h3 : 4 * 5 * ((4 / 5) * (4 / 5)) * (1 / 10 - 1 / 1000)
-      ≤ searchesPerDay .current * missExtraMinutes .current
-        * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val))
-        * ((pNotYet .current).val - (pNotYet .fullText).val) :=
-    rat_mul_le_mul (by grind) h2 (by grind) (by grind)
-  grind
-
-/-- 1人1日1分の時間は、1年で 4,120,000円以上の人件費になる（412人 × 200日 × 3,000円 ÷ 60）。 -/
+  have hAc := missAfterIndex_nonneg .current
+  have h1A : 16 / 25 ≤ 1 - missAfterIndex .current := by
+    unfold missAfterIndex
+    have hx : (4 / 5) * (4 / 5) ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have hAe : missAfterIndex .current * extraOtherMinutes .current
+      ≤ missAfterIndex .current * extraNotYetMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_left hle hAc
+  have hq : (16 / 25) * 5 ≤ (1 - missAfterIndex .current) * extraNotYetMinutes .current :=
+    rat_mul_le_mul (by grind) h1A (by grind) he1
+  have hK : (16 / 25) * 5 ≤ extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have hP : 1 / 10 - 1 / 1000 ≤ (pNotYet .current).val - (pNotYet .fullText).val := by grind
+  have h1 : 4 * (1 / 10 - 1 / 1000) ≤ searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val) :=
+    rat_mul_le_mul (by grind) hs (by grind) hP
+  have h2 : 4 * (1 / 10 - 1 / 1000) * ((16 / 25) * 5)
+      ≤ searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val)
+        * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) :=
+    rat_mul_le_mul (by grind) h1 (by grind) hK
+  grind
+
+/-- 安い設定の変更に比べて取り戻せる時間は、回数(いま) ×（層1の確率の差。安い設定の変更と置き換えた後）×
+（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）以上。
+安い設定の変更の量を、C0 の側の片側の公理で、いまの検索の値に置き換えた下界を、`saved_ge_gap` に足して出す。 -/
+theorem savedOverTuned_ge_gap :
+    searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val)
+      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current)
+      ≤ savedOverTunedMinutes := by
+  have hg := saved_ge_gap
+  unfold savedMinutes at hg
+  unfold savedOverTunedMinutes
+  have hSc := search_layers .current
+  have hSt := search_layers .tuned
+  have hsc := searchesPerDay_nonneg .current
+  have hfc := foundMinutes_nonneg .current
+  have he1 := extraNotYet_current_ge
+  have he2 := extraOther_nonneg
+  have hs := searches_tuned_ge
+  have hf := found_tuned_ge
+  have hx1 := extraNotYet_tuned_ge
+  have hx2 := extraOther_tuned_ge
+  have hb := noHit_tuned_ge
+  have hc := overlook_tuned_ge
+  have hAt := missAfterIndex_nonneg .tuned
+  have hAc := missAfterIndex_nonneg .current
+  have hp0 := (pNotYet .tuned).nonneg
+  have hp1 := (pNotYet .tuned).le_one
+  have hA : missAfterIndex .current ≤ missAfterIndex .tuned := by
+    unfold missAfterIndex
+    have hb1 := (pNoHit .tuned).le_one
+    have hc1 := (pOverlook .tuned).le_one
+    have hx : (1 - (pNoHit .tuned).val) * (1 - (pOverlook .tuned).val)
+        ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have h1 : (pNotYet .tuned).val * extraNotYetMinutes .current
+      ≤ (pNotYet .tuned).val * extraNotYetMinutes .tuned :=
+    Rat.mul_le_mul_of_nonneg_left hx1 hp0
+  have h2a : missAfterIndex .current * extraOtherMinutes .current
+      ≤ missAfterIndex .tuned * extraOtherMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_right hA he2
+  have h2b : missAfterIndex .tuned * extraOtherMinutes .current
+      ≤ missAfterIndex .tuned * extraOtherMinutes .tuned :=
+    Rat.mul_le_mul_of_nonneg_left hx2 hAt
+  have h3 : (1 - (pNotYet .tuned).val) * (missAfterIndex .current * extraOtherMinutes .current)
+      ≤ (1 - (pNotYet .tuned).val) * (missAfterIndex .tuned * extraOtherMinutes .tuned) :=
+    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
+  have hG : foundMinutes .current + (pNotYet .tuned).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current
+      ≤ foundMinutes .tuned + (pNotYet .tuned).val * extraNotYetMinutes .tuned
+        + (1 - (pNotYet .tuned).val) * missAfterIndex .tuned * extraOtherMinutes .tuned := by
+    grind
+  have hG0a : 0 ≤ (pNotYet .tuned).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 (by grind)
+  have hG0b : 0 ≤ (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current :=
+    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
+  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .tuned).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have h4 := Rat.mul_le_mul_of_nonneg_right hs hG0
+  have h5 := Rat.mul_le_mul_of_nonneg_left hG (by grind : 0 ≤ searchesPerDay .tuned)
+  grind
+
+/-- 安い設定の変更に比べて取り戻せる時間は、1人1日 792/625 分（1.2672分）以上（4回 ×（1/10 − 1/1000）×（16/25 × 5分））。 -/
+theorem savedOverTuned_ge : 792 / 625 ≤ savedOverTunedMinutes := by
+  have hg := savedOverTuned_ge_gap
+  have hs := searches_current_ge
+  have he1 := extraNotYet_current_ge
+  have hle := extraOther_le_notYet
+  have he2 := extraOther_nonneg
+  have hb := noHit_current_le
+  have hc := overlook_current_le
+  have ha := notYet_tuned_ge
+  have hf := notYet_fullText_le
+  have hAc := missAfterIndex_nonneg .current
+  have h1A : 16 / 25 ≤ 1 - missAfterIndex .current := by
+    unfold missAfterIndex
+    have hx : (4 / 5) * (4 / 5) ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have hAe : missAfterIndex .current * extraOtherMinutes .current
+      ≤ missAfterIndex .current * extraNotYetMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_left hle hAc
+  have hq : (16 / 25) * 5 ≤ (1 - missAfterIndex .current) * extraNotYetMinutes .current :=
+    rat_mul_le_mul (by grind) h1A (by grind) he1
+  have hK : (16 / 25) * 5 ≤ extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have hP : 1 / 10 - 1 / 1000 ≤ (pNotYet .tuned).val - (pNotYet .fullText).val := by grind
+  have h1 : 4 * (1 / 10 - 1 / 1000) ≤ searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val) :=
+    rat_mul_le_mul (by grind) hs (by grind) hP
+  have h2 : 4 * (1 / 10 - 1 / 1000) * ((16 / 25) * 5)
+      ≤ searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val)
+        * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) :=
+    rat_mul_le_mul (by grind) h1 (by grind) hK
+  grind
+
+/-- 1人1日1分の時間は、初年度に 4,120,000円以上の人件費になる（412人 × 200日 × 3,000円 ÷ 60）。 -/
 theorem yenPerDailyMinute_ge : 4120000 ≤ yenPerDailyMinute := by
   unfold yenPerDailyMinute
@@ -476,27 +898,39 @@
 /-! ### 主張の定理 -/
 
-/-- @claim C3 [確率] 読み (b): 初年度の費用は、置き換えで取り戻せる時間の1年分の人件費より小さい。 -/
-theorem claim_C3_saved : firstYearCost < benefitYen := by
-  unfold benefitYen
+/-- @claim C3 [確率] 読み (b): 初年度の費用は、置き換えで（いまのままと比べて）取り戻せる時間の初年度の人件費より小さい。 -/
+theorem claim_C3_saved : firstYearCost < savedWageYen := by
+  unfold savedWageYen
   have hy := yenPerDailyMinute_ge
   have hs := saved_ge
-  have hc := cost_eq
+  have hc := cost_le_estimate
+  have he := estimate_eq
   have h : 4120000 * (792 / 625) ≤ yenPerDailyMinute * savedMinutes :=
     rat_mul_le_mul (by grind) hy (by grind) hs
   grind
 
-/-- @claim C3 [確率] 読み (a): 初年度の費用は、いまの検索で失われている時間の1年分の人件費より小さい。 -/
-theorem claim_C3_lost : firstYearCost < lostYen := by
-  unfold lostYen
+/-- @claim C3 [確率] 読み (a): 初年度の費用は、いまの検索で失われている時間の初年度の人件費より小さい。 -/
+theorem claim_C3_lost : firstYearCost < lostWageYen := by
+  unfold lostWageYen
   have hy := yenPerDailyMinute_ge
   have hl := lost_ge
-  have hc := cost_eq
+  have hc := cost_le_estimate
+  have he := estimate_eq
   have h : 4120000 * 2 ≤ yenPerDailyMinute * lostMinutes :=
     rat_mul_le_mul (by grind) hy (by grind) hl
   grind
 
-/-- @claim C0 [確率] 来期予算で300万円を承認する理由がそろう。 -/
-theorem claim_C0_approvable : Approvable :=
-  approvable_of_net claim_C3_saved no_cheaper_fix
+/-- @claim C0 [確率] 来期予算で300万円を承認する理由がそろう。
+初年度の費用 ≤ 300万円 < 5,220,864円 ≤ 安い設定の変更に比べて取り戻せる時間の人件費 ≤ 会社が得る値打ち、から示す。 -/
+theorem claim_C0_approvable : Approvable := by
+  apply approvable_of_net
+  have hy := yenPerDailyMinute_ge
+  have hs := savedOverTuned_ge
+  have hg := gain_ge_wage
+  have hc := cost_le_estimate
+  have he := estimate_eq
+  unfold savedOverTunedWageYen at hg
+  have h : 4120000 * (792 / 625) ≤ yenPerDailyMinute * savedOverTunedMinutes :=
+    rat_mul_le_mul (by grind) hy (by grind) hs
+  grind
 
 /-- @claim C1 [決定論] いまの検索で1人1日に探し物に使う時間は、「多い」の境目以上。
@@ -520,12 +954,13 @@
 /-! ### 比べる相手の確認と、不利な結論 -/
 
-/-- @baseline いまの検索の「失われている時間」（読み a）を、アンケートの1日20分より大きく置いていない。 -/
+/-- @baseline いまの検索の「失われている時間」（読み a）を、アンケートの1日20分より大きく置いていない。
+失われている時間 = 20 − 回数 × 見つかった場合の時間。 -/
 theorem baseline_lost_le_survey : lostMinutes ≤ 20 := by
   unfold lostMinutes
   have hd := search_decomp .current
   have he := search_current_eq
-  have hs := searches_current_ge
+  have hs := searchesPerDay_nonneg .current
   have hf := foundMinutes_nonneg .current
-  have h0 : 0 ≤ searchesPerDay .current * foundMinutes .current := Rat.mul_nonneg (by grind) hf
+  have h0 : 0 ≤ searchesPerDay .current * foundMinutes .current := Rat.mul_nonneg hs hf
   grind
 
@@ -537,13 +972,88 @@
   grind
 
+/-- [不利] 置き換えで取り戻せる時間（読み b）は、回数(いま) ×（層1の確率の差）×（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）を超えない。
+層1の差が縮めば、効果もそれだけ縮む。置き換えた後の量を、不利な結論の側の片側の公理で、いまの検索の値に置き換えた下界から出す。
+主張の側の片側の公理（`_full_le`）も、量の仮定（4回、5分、10%）も通らない。 -/
+theorem unfav_saved_le_gap :
+    savedMinutes ≤ searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val)
+      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) := by
+  unfold savedMinutes
+  rw [search_layers .current, search_layers .fullText]
+  have hsf := searchesPerDay_nonneg .fullText
+  have hfc := foundMinutes_nonneg .current
+  have he1 := extraNotYet_nonneg
+  have he2 := extraOther_nonneg
+  have hs := searches_full_ge
+  have hf := found_full_ge
+  have hx1 := extraNotYet_full_ge
+  have hx2 := extraOther_full_ge
+  have hb := noHit_full_ge
+  have hc := overlook_full_ge
+  have hAf := missAfterIndex_nonneg .fullText
+  have hAc := missAfterIndex_nonneg .current
+  have hp0 := (pNotYet .fullText).nonneg
+  have hp1 := (pNotYet .fullText).le_one
+  have hA : missAfterIndex .current ≤ missAfterIndex .fullText := by
+    unfold missAfterIndex
+    have hb1 := (pNoHit .fullText).le_one
+    have hc1 := (pOverlook .fullText).le_one
+    have hx : (1 - (pNoHit .fullText).val) * (1 - (pOverlook .fullText).val)
+        ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have h1 : (pNotYet .fullText).val * extraNotYetMinutes .current
+      ≤ (pNotYet .fullText).val * extraNotYetMinutes .fullText :=
+    Rat.mul_le_mul_of_nonneg_left hx1 hp0
+  have h2a : missAfterIndex .current * extraOtherMinutes .current
+      ≤ missAfterIndex .fullText * extraOtherMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_right hA he2
+  have h2b : missAfterIndex .fullText * extraOtherMinutes .current
+      ≤ missAfterIndex .fullText * extraOtherMinutes .fullText :=
+    Rat.mul_le_mul_of_nonneg_left hx2 hAf
+  have h3 : (1 - (pNotYet .fullText).val) * (missAfterIndex .current * extraOtherMinutes .current)
+      ≤ (1 - (pNotYet .fullText).val) * (missAfterIndex .fullText * extraOtherMinutes .fullText) :=
+    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
+  have hG : foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current
+      ≤ foundMinutes .fullText + (pNotYet .fullText).val * extraNotYetMinutes .fullText
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .fullText * extraOtherMinutes .fullText := by
+    grind
+  have hG0a : 0 ≤ (pNotYet .fullText).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 he1
+  have hG0b : 0 ≤ (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current :=
+    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
+  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have h4 := Rat.mul_le_mul_of_nonneg_right hs hG0
+  have h5 := Rat.mul_le_mul_of_nonneg_left hG hsf
+  grind
+
 /-- [不利] 置き換えで取り戻せる時間（読み b）は、いまの検索で失われている時間（読み a）を超えない。 -/
 theorem unfav_saved_le_lost : savedMinutes ≤ lostMinutes := by
   unfold savedMinutes lostMinutes
-  rw [search_decomp .current, search_decomp .fullText, searches_same, foundMinutes_same, missExtra_same]
-  have hs := searches_current_ge
-  have he := missExtra_current_ge
-  have hm := (missProb .fullText).nonneg
-  have h0 : 0 ≤ searchesPerDay .current * (missProb .fullText).val * missExtraMinutes .current :=
-    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hm) (by grind)
+  rw [search_decomp .current, search_decomp .fullText]
+  have hsf := searchesPerDay_nonneg .fullText
+  have hfc := foundMinutes_nonneg .current
+  have he1 := extraNotYet_nonneg
+  have he2 := extraOther_nonneg
+  have hs := searches_full_ge
+  have hf := found_full_ge
+  have hx1 := extraNotYet_full_ge
+  have hx2 := extraOther_full_ge
+  have hL := miss_sub_notYet .fullText
+  have hAf := missAfterIndex_nonneg .fullText
+  have hp0 := (pNotYet .fullText).nonneg
+  have hp1 := (pNotYet .fullText).le_one
+  have hm : 0 ≤ (missProb .fullText).val - (pNotYet .fullText).val := by
+    rw [hL]
+    exact Rat.mul_nonneg (by grind) hAf
+  have hq1 : 0 ≤ (pNotYet .fullText).val * extraNotYetMinutes .fullText := Rat.mul_nonneg hp0 (by grind)
+  have hq2 : 0 ≤ ((missProb .fullText).val - (pNotYet .fullText).val) * extraOtherMinutes .fullText :=
+    Rat.mul_nonneg hm (by grind)
+  have hI : foundMinutes .current ≤ foundMinutes .fullText + (pNotYet .fullText).val * extraNotYetMinutes .fullText
+      + ((missProb .fullText).val - (pNotYet .fullText).val) * extraOtherMinutes .fullText := by
+    grind
+  have h4 := Rat.mul_le_mul_of_nonneg_right hs hfc
+  have h5 := Rat.mul_le_mul_of_nonneg_left hI hsf
   grind
 
--- rounds/01/Model.lean
+++ Model.lean
@@ -4,32 +4,65 @@
 `Argument.lean` のすべての `axiom` を、同じ名前・同じ型の具体的な `def` / `theorem` に差し替えた写し。公理系が無矛盾であることの証拠。
 axiom 以外の行は、`Argument.lean` と同じ順で残している。`instance`・`attribute`・`open`・`set_option` は足していない。
-
-## 証人の世界（設計書 model-plan.md の5節の値の例のとおり）
-
-| 量 | current | fullText |
-|---|---|---|
-| `indexDelaySec`（秒） | 86400 | 4.2 |
-| `pNotYet` | 1/10 | 1/1000 |
-| `pNoHit`・`pOverlook` | 1/5 | 1/5 |
-| `missProb` | 53/125（0.424） | 1127/3125（0.36064） |
-| `searchesPerDay`（回） | 4 | 4 |
-| `foundMinutes`（分） | 72/25（2.88） | 72/25（2.88） |
-| `missExtraMinutes`（分） | 5 | 5 |
-| `searchMinutes`（分。`search_decomp` の式で計算） | 20 | 18.7328 |
-
-方式によらない量: `testDelaySec` 4.2、`beneficiaries` 412、`workDays` 200、`wagePerHour` 3000、`firstYearCost` 3,000,000、
-`manyMinutes` 20。`CheaperFix` は偽、`Approvable` は真。
-
-この世界で、関係公理の前提は空回りしない。
-
-- `notYet_ge_of_slow` の前提（遅れ 28800 秒以上）は `current` で成り立ち（86400 秒）、結論 1/10 ≤ 1/10 が成り立つ。
-- `notYet_le_of_fast` の前提（遅れ 5 秒以内）は `fullText` で成り立ち（4.2 秒）、結論 1/1000 ≤ 1/1000 が成り立つ。
-- `approvable_of_net` の前提は2つとも成り立つ（`benefitYen` = 4,120,000 × 1.2672 = 5,220,864 円 > 3,000,000 円、`CheaperFix` は偽）。
-- `savedMinutes` = 1.2672 分、`lostMinutes` = 8.48 分。
-
-多くの量は、関係公理の境目の値に置いている（回数 4、余分な時間 5、層1の確率 1/10 と 1/1000、層2・層3の確率 1/5、
-人数 412、日数 200、人件費 3000、境目 20）。境目の値でも、主張の定理の真の不等式（費用 < 1年分の人件費など）は余裕をもって成り立つ。
-真に成り立つ不等式もある（`testDelay_le_five` は 4.2 < 5、`delay_current_ge_workday` は 28800 < 86400、
-`searchMinutes_nonneg`・`foundMinutes_nonneg` は 0 より大きい）。
+末尾に、関係公理の前提が成り立つことを示す `example` を足した。
+
+## 証人の世界（差分の設計書 model-plan-delta.md の6.3節の値をもとにした）
+
+| 量 | current | tuned | fullText |
+|---|---|---|---|
+| `indexDelaySec`（秒） | 86400 | 43200 | 4 |
+| `pNotYet` | 1/10 | 1/10 | 1/1000 |
+| `pNoHit`・`pOverlook` | 1/5 | 1/5 | 1/5 |
+| `missProb` | 53/125（0.424） | 53/125 | 1127/3125（0.36064） |
+| `missAfterIndex`（計算） | 9/25 | 9/25 | 9/25 |
+| `searchesPerDay`（回） | 4 | 4 | 4 |
+| `foundMinutes`（分） | 72/25（2.88） | 72/25 | 72/25 |
+| `extraNotYetMinutes`・`extraOtherMinutes`（分） | 5 | 5 | 5 |
+| `searchMinutes`（分。`search_decomp` の式で計算） | 20 | 20 | 18.7328 |
+| `IndexComplete` | 真 | 真 | 真 |
+
+方式によらない量: `testDelaySec` 4.2、`beneficiaries` 412、`workDays` 200、`wagePerHour` 3000、`estimateYen` 3,000,000、
+`firstYearCost` 2,800,000、`manyMinutes` 15、`gainYen` 6,000,000。`CurrentIncremental` は偽。
+`Approvable` は「`firstYearCost` < `gainYen`」と定義した（前提が崩れれば結論も崩れる世界で、`approvable_of_net` を試す）。
+
+計算の値: `savedMinutes` と `savedOverTunedMinutes` は 1.2672 分、`lostMinutes` は 8.48 分、`yenPerDailyMinute` は 4,120,000 円、
+`savedWageYen` と `savedOverTunedWageYen` は 5,220,864 円、`lostWageYen` は 34,937,600 円。
+
+### 設計書の6.3節の値から変えたところ
+
+境目ちょうどの値ばかりにしないため、ほかの値に響かない量を、関係公理の不等式が真に成り立つ値にした。
+
+- `indexDelaySec .tuned` を 86400 から 43200 にした（`tuned_slow_of_rebuild` の結論 28800 < 43200 が真に成り立つ。`pNotYet .tuned` は 1/10 のまま）。
+  安い設定の変更は、いまのままより速いが、8時間より短くはならない世界になる。
+- `indexDelaySec .fullText` を 4.2 から 4 にした（`prodDelay_le_test` が 4 < 4.2 で真に成り立つ）。
+- `firstYearCost` を 3,000,000 から 2,800,000 にした（`cost_le_estimate` が真に成り立つ）。
+- `gainYen` を 5,220,864 から 6,000,000 にした（`gain_ge_wage` が真に成り立つ）。
+- `manyMinutes` を 20 から 15 にした（`many_threshold_le` が真に成り立つ）。
+
+### 不等式が、真に成り立つか、境目ちょうどか
+
+- 真に成り立つ（<）: `testDelay_le_five`（4.2 < 5）、`delay_current_ge_workday`（28800 < 86400）、`prodDelay_le_test`（4 < 4.2）、
+  `tuned_slow_of_rebuild`（28800 < 43200）、`cost_le_estimate`、`gain_ge_wage`、`many_threshold_le`、`extraNotYet_nonneg`・`extraOther_nonneg`（0 < 5）、
+  `searchMinutes_nonneg`・`foundMinutes_nonneg`・`searchesPerDay_nonneg`、`missAfterIndex_nonneg`。
+- 境目ちょうど（=）: `notYet_ge_of_slow`（1/10）、`notYet_le_of_fast`（1/1000）、`noHit_current_le`・`overlook_current_le`（1/5）、
+  `searches_current_ge`（4）、`extraNotYet_current_ge`（5）、`extraOther_le_notYet`（5 = 5）、`beneficiaries_ge`（412）、`workDays_ge`（200）、`wage_ge`（3000）。
+  どれも主張の下限を決める量の案の値で、6.3節の値のまま残した。境目の値でも、主張の定理の真の不等式（費用 < 人件費）は余裕をもって成り立つ。
+- `_tuned_ge` の6つも等号で満たしている（`tuned` の層1のほかの量は、いまの検索と同じにした）。
+
+### 公理系そのものが決める等号（証人の選び方ではない）
+
+置き換えの片側の公理は、主張の側（`_full_le`）と不利な結論の側（`_full_ge`）の両方を置いている。
+2つを合わせると、`searchesPerDay`・`foundMinutes`・`extraNotYetMinutes`・`extraOtherMinutes`・`pNoHit`・`pOverlook` の6つの量で、
+`fullText` の値は `current` の値に等しくなる。これはどの証人でも同じで、公理系の全体としては1周目の等式と同じ世界しか許さない。
+片側に分けた効果は、定理ごとの依存（主張の定理は `_full_le` だけ、不利な結論の定理は `_full_ge` だけに頼る）に表れる。
+
+### 前提が空回りしないこと
+
+含意の形の関係公理は、どれも前提が成り立つ例を持つ（末尾の `example`）。
+
+- `notYet_ge_of_slow` の前提（遅れ 28800 秒以上）は、`current`（86400 秒）と `tuned`（43200 秒）で成り立つ。
+- `notYet_le_of_fast` の前提（遅れ 5 秒以内、欠けた記事がない）は、`fullText`（4 秒、`IndexComplete` が真）で成り立つ。
+- `tuned_slow_of_rebuild` の前提（`CurrentIncremental` でない）は成り立つ。
+- `approvable_of_net` の前提（2,800,000 < 6,000,000）は成り立ち、`Approvable` はこの前提そのものなので、前提が崩れれば結論も崩れる。
+- 主張の定理（`claim_C0_approvable`・`claim_C1_many`・`claim_C2_soon`・`claim_C2_faster`・`claim_C3_saved`・`claim_C3_lost`）は、どれも前提を持たない。
 -/
 
@@ -41,7 +74,12 @@
 /-! ## §1 帰納型（定義） -/
 
-/-- 比べる2つの方式。`current` はいまの検索の仕組み、`fullText` は置き換えた後の全文検索エンジン。 -/
+/-- 比べる3つの方式。
+`current` は、いまの検索の仕組み（中身が Elasticsearch などの全文検索エンジンかは、06-facts.json にない）。
+`tuned` は、いまの検索の仕組みのまま、300万円より安い費用でできる設定の変更（索引を作り直す間隔を短くする、保存のたびに索引へ足す、など）を、
+保存から検索に出るまでがいちばん短くなるように施したもの。そうした変更ができないなら、いまのままと同じもの。
+`fullText` は、置き換えた後の全文検索エンジン。 -/
 inductive Method where
   | current
+  | tuned
   | fullText
 
@@ -54,21 +92,30 @@
 /-! ## §2 宣言（中身を決めない型・関数・定数） -/
 
-/-- 証人: 記事の保存から検索に出るまでの秒数。いまの検索は 86400 秒（1日）、置き換えた後は 4.2 秒。 -/
+/-- 証人: 記事の保存から検索に出るまでの秒数。いまの検索は 86400 秒（1日）、安い設定の変更は 43200 秒（半日）、
+置き換えた後は 4 秒（試験環境の最大 4.2 秒より短い）。 -/
 def indexDelaySec : Method → Rat := fun M => match M with
   | .current => 86400
-  | .fullText => 21 / 5
+  | .tuned => 43200
+  | .fullText => 4
 
 /-- 証人: 試験環境の計測値。F3 の最大 4.2 秒。 -/
 def testDelaySec : Rat := 21 / 5
 
-/-- 証人: 層1の確率。いまの検索は 1/10、置き換えた後は 1/1000。 -/
+/-- 証人: いまの仕組みは、保存のたびに索引へ足せない（偽）。 -/
+def CurrentIncremental : Prop := False
+
+/-- 証人: どの方式も、すべての記事を索引に持っている（真）。 -/
+def IndexComplete : Method → Prop := fun _ => True
+
+/-- 証人: 層1の確率。いまの検索と安い設定の変更は 1/10、置き換えた後は 1/1000。 -/
 def pNotYet : Method → Prob := fun M => match M with
   | .current => ⟨1 / 10, by grind, by grind⟩
+  | .tuned => ⟨1 / 10, by grind, by grind⟩
   | .fullText => ⟨1 / 1000, by grind, by grind⟩
 
-/-- 証人: 層2の確率。どちらの方式も 1/5。 -/
+/-- 証人: 層2の確率。どの方式も 1/5。 -/
 def pNoHit : Method → Prob := fun _ => ⟨1 / 5, by grind, by grind⟩
 
-/-- 証人: 層3の確率。どちらの方式も 1/5。 -/
+/-- 証人: 層3の確率。どの方式も 1/5。 -/
 def pOverlook : Method → Prob := fun _ => ⟨1 / 5, by grind, by grind⟩
 
@@ -76,23 +123,28 @@
 def missProb : Method → Prob := fun M => match M with
   | .current => ⟨53 / 125, by grind, by grind⟩
+  | .tuned => ⟨53 / 125, by grind, by grind⟩
   | .fullText => ⟨1127 / 3125, by grind, by grind⟩
 
-/-- 証人: 1人1日の探し物の回数。どちらの方式も 4 回。 -/
+/-- 証人: 1人1日の探し物の回数。どの方式も 4 回。 -/
 def searchesPerDay : Method → Rat := fun _ => 4
 
-/-- 証人: 見つかった探し物1回の時間。どちらの方式も 2.88 分（いまの検索の1日の時間が 20 分になるように決めた）。 -/
+/-- 証人: 見つかった探し物1回の時間。どの方式も 2.88 分（いまの検索の1日の時間が 20 分になるように決めた）。 -/
 def foundMinutes : Method → Rat := fun _ => 72 / 25
 
-/-- 証人: 見つからなかった探し物1回の余分な時間。どちらの方式も 5 分。 -/
-def missExtraMinutes : Method → Rat := fun _ => 5
-
-/-- 証人: 1人1日の探し物の時間。`search_decomp` の式で計算する（いまの検索は 20 分、置き換えた後は 18.7328 分）。 -/
+/-- 証人: 層1で見つからなかった探し物1回の余分な時間。どの方式も 5 分。 -/
+def extraNotYetMinutes : Method → Rat := fun _ => 5
+
+/-- 証人: 層2・層3で見つからなかった探し物1回の余分な時間。どの方式も 5 分。 -/
+def extraOtherMinutes : Method → Rat := fun _ => 5
+
+/-- 証人: 1人1日の探し物の時間。`search_decomp` の式で計算する（いまの検索と安い設定の変更は 20 分、置き換えた後は 18.7328 分）。 -/
 def searchMinutes : Method → Rat := fun M =>
-  searchesPerDay M * (foundMinutes M + (missProb M).val * missExtraMinutes M)
+  searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M
+    + ((missProb M).val - (pNotYet M).val) * extraOtherMinutes M)
 
 /-- 証人: 効果を受ける社員の数。412 人。 -/
 def beneficiaries : Rat := 412
 
-/-- 証人: 1年の勤務日数。200 日。 -/
+/-- 証人: 初年度に置き換えた検索を使える勤務日数。200 日。 -/
 def workDays : Rat := 200
 
@@ -100,21 +152,31 @@
 def wagePerHour : Rat := 3000
 
-/-- 証人: 初年度の費用。3,000,000 円。 -/
-def firstYearCost : Rat := 3000000
-
-/-- 証人: 「多い」の境目。20 分。 -/
-def manyMinutes : Rat := 20
-
-/-- 証人: もっと安い方法は、この世界にはない。 -/
-def CheaperFix : Prop := False
-
-/-- 証人: 承認する理由は、この世界ではそろっている。 -/
-def Approvable : Prop := True
+/-- 証人: 見積もりの額。3,000,000 円。 -/
+def estimateYen : Rat := 3000000
+
+/-- 証人: 実際に追加で要る初年度の費用。2,800,000 円（見積もりより少ない）。 -/
+def firstYearCost : Rat := 2800000
+
+/-- 証人: 「多い」の境目。15 分。 -/
+def manyMinutes : Rat := 15
+
+/-- 証人: 会社が得る値打ち。6,000,000 円（安い設定の変更に比べて取り戻せる時間の人件費 5,220,864 円より多い）。 -/
+def gainYen : Rat := 6000000
+
+/-- 証人: 承認する理由がそろうのは、初年度の費用が会社の得る値打ちより小さいとき（前提が崩れれば、結論も崩れる世界）。 -/
+def Approvable : Prop := firstYearCost < gainYen
 
 /-! ## §3 計算の def（手順だけ。判断を入れない） -/
 
-/-- 読み (a) の「失われている時間」（分）: いまの検索の、1日の探し物の回数 × 見つからない確率 × 見つからなかった1回の余分な時間。 -/
+/-- 方式 M で、索引に入っている記事を探して、層2か層3で失敗する確率: 1 −（1 − 層2の確率）×（1 − 層3の確率）。 -/
+def missAfterIndex (M : Method) : Rat :=
+  1 - (1 - (pNoHit M).val) * (1 - (pOverlook M).val)
+
+/-- 読み (a) の「失われている時間」（分）: いまの検索の、1日の探し物の回数 ×（層1で見つからない確率 × 層1の余分な時間 ＋
+（見つからない確率 − 層1で見つからない確率）× 層2・層3の余分な時間）。
+いまの検索で、見つからなかった探し物のために1人1日に余分に検索で使っている時間。 -/
 def lostMinutes : Rat :=
-  searchesPerDay .current * (missProb .current).val * missExtraMinutes .current
+  searchesPerDay .current * ((pNotYet .current).val * extraNotYetMinutes .current
+    + ((missProb .current).val - (pNotYet .current).val) * extraOtherMinutes .current)
 
 /-- 読み (b) の「取り戻せる時間」（分）: 1人1日の探し物の時間の、いまの検索と置き換えた後の差。 -/
@@ -122,26 +184,34 @@
   searchMinutes .current - searchMinutes .fullText
 
-/-- 1人1日1分の時間が、1年で何円の人件費になるか: 人数 × 勤務日数 × 1時間あたりの人件費 ÷ 60。 -/
+/-- 置き換えで、安い設定の変更をした場合に比べて、1人1日に取り戻せる時間（分）: 1人1日の探し物の時間の、安い設定の変更と置き換えた後の差。 -/
+def savedOverTunedMinutes : Rat :=
+  searchMinutes .tuned - searchMinutes .fullText
+
+/-- 1人1日1分の時間が、初年度（`workDays` の日数）でいくらの人件費になるか: 人数 × 勤務日数 × 1時間あたりの人件費 ÷ 60。 -/
 def yenPerDailyMinute : Rat :=
   beneficiaries * workDays * wagePerHour / 60
 
-/-- 読み (a) の時間の、1年分の人件費（円）。 -/
-def lostYen : Rat :=
+/-- 読み (a) の時間の、初年度の人件費（円）。 -/
+def lostWageYen : Rat :=
   yenPerDailyMinute * lostMinutes
 
-/-- 読み (b) の時間の、1年分の人件費（円）。 -/
-def benefitYen : Rat :=
+/-- 読み (b) の時間の、初年度の人件費（円）。会社の得ではなく、人件費に直した量。 -/
+def savedWageYen : Rat :=
   yenPerDailyMinute * savedMinutes
 
+/-- 安い設定の変更に比べて取り戻せる時間の、初年度の人件費（円）。 -/
+def savedOverTunedWageYen : Rat :=
+  yenPerDailyMinute * savedOverTunedMinutes
+
 /-! ## §4 関係公理 -/
 
 /-! ### 【実験】 -/
 
-/-- 証人: 4 ×（2.88 ＋ 0.424 × 5）= 20。 -/
+/-- 証人: 4 ×（2.88 ＋ 0.1 × 5 ＋（0.424 − 0.1）× 5）= 20。 -/
 theorem search_current_eq : searchMinutes .current = 20 := by
-  show (4 : Rat) * (72 / 25 + 53 / 125 * 5) = 20
-  grind
-
-/-- 証人: 4.2 ≤ 5。 -/
+  show (4 : Rat) * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5) = 20
+  grind
+
+/-- 証人: 4.2 < 5。 -/
 theorem testDelay_le_five : testDelaySec ≤ 5 := by
   show (21 / 5 : Rat) ≤ 5
@@ -149,14 +219,14 @@
 
 /-- 証人: 定義どおり。 -/
-theorem cost_eq : firstYearCost = 3000000 := rfl
+theorem estimate_eq : estimateYen = 3000000 := rfl
 
 /-! ### 【経験則】 -/
 
-/-- 証人: 28800 ≤ 86400。 -/
+/-- 証人: 28800 < 86400。 -/
 theorem delay_current_ge_workday : 28800 ≤ indexDelaySec .current := by
   show (28800 : Rat) ≤ 86400
   grind
 
-/-- 証人: 412 ≤ 412。 -/
+/-- 証人: 412 ≤ 412（境目の値）。 -/
 theorem beneficiaries_ge : 412 ≤ beneficiaries := by
   show (412 : Rat) ≤ 412
@@ -167,14 +237,17 @@
 /-- 証人: `searchMinutes` をこの式で定義したので、定義どおり。 -/
 theorem search_decomp : ∀ M : Method,
-  searchMinutes M = searchesPerDay M * (foundMinutes M + (missProb M).val * missExtraMinutes M) :=
+  searchMinutes M = searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M
+    + ((missProb M).val - (pNotYet M).val) * extraOtherMinutes M) :=
   fun _ => rfl
 
-/-- 証人: 20 と 18.7328 は 0 以上。 -/
+/-- 証人: 20・20・18.7328 は 0 以上。 -/
 theorem searchMinutes_nonneg : ∀ M : Method, 0 ≤ searchMinutes M := by
   intro M
   cases M
-  · show (0 : Rat) ≤ 4 * (72 / 25 + 53 / 125 * 5)
-    grind
-  · show (0 : Rat) ≤ 4 * (72 / 25 + 1127 / 3125 * 5)
+  · show (0 : Rat) ≤ 4 * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5)
+    grind
+  · show (0 : Rat) ≤ 4 * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5)
+    grind
+  · show (0 : Rat) ≤ 4 * (72 / 25 + 1 / 1000 * 5 + (1127 / 3125 - 1 / 1000) * 5)
     grind
 
@@ -185,50 +258,9 @@
   grind
 
-/-! ### 【仮定】層1: まだ検索に出ない -/
-
-/-- 証人: 4.2 ≤ 4.2。 -/
-theorem prodDelay_le_test : indexDelaySec .fullText ≤ testDelaySec := by
-  show (21 / 5 : Rat) ≤ 21 / 5
-  grind
-
-/-- 証人: `current` で前提が成り立ち（86400 秒）、結論 1/10 ≤ 1/10 が成り立つ。`fullText` では前提が成り立たない（4.2 秒）。 -/
-theorem notYet_ge_of_slow : ∀ M : Method, 28800 ≤ indexDelaySec M → 1 / 10 ≤ (pNotYet M).val := by
-  intro M h
-  cases M
-  · show (1 / 10 : Rat) ≤ 1 / 10
-    grind
-  · have h' : (28800 : Rat) ≤ 21 / 5 := h
-    grind
-
-/-- 証人: `fullText` で前提が成り立ち（4.2 秒）、結論 1/1000 ≤ 1/1000 が成り立つ。`current` では前提が成り立たない（86400 秒）。 -/
-theorem notYet_le_of_fast : ∀ M : Method, indexDelaySec M ≤ 5 → (pNotYet M).val ≤ 1 / 1000 := by
-  intro M h
-  cases M
-  · have h' : (86400 : Rat) ≤ 5 := h
-    grind
-  · show (1 / 1000 : Rat) ≤ 1 / 1000
-    grind
-
-/-! ### 【仮定】層2・層3: いまの検索の値 -/
-
-/-- 証人: 1/5 ≤ 1/5。 -/
-theorem noHit_current_le : (pNoHit .current).val ≤ 1 / 5 := by
-  show (1 / 5 : Rat) ≤ 1 / 5
-  grind
-
-/-- 証人: 1/5 ≤ 1/5。 -/
-theorem overlook_current_le : (pOverlook .current).val ≤ 1 / 5 := by
-  show (1 / 5 : Rat) ≤ 1 / 5
-  grind
-
-/-! ### 【仮定】層2・層3: 同じとみなす -/
-
-/-- 証人: どちらの方式も同じ値。 -/
-theorem noHit_same : pNoHit .fullText = pNoHit .current := rfl
-
-/-- 証人: どちらの方式も同じ値。 -/
-theorem overlook_same : pOverlook .fullText = pOverlook .current := rfl
-
-/-! ### 【仮定】層の合成 -/
+/-- 証人: 4 は 0 以上。 -/
+theorem searchesPerDay_nonneg : ∀ M : Method, 0 ≤ searchesPerDay M := by
+  intro _
+  show (0 : Rat) ≤ 4
+  grind
 
 /-- 証人: 1 − 9/10 × 4/5 × 4/5 = 53/125、1 − 999/1000 × 4/5 × 4/5 = 1127/3125。 -/
@@ -239,59 +271,231 @@
   · show (53 / 125 : Rat) = 1 - (1 - 1 / 10) * (1 - 1 / 5) * (1 - 1 / 5)
     grind
+  · show (53 / 125 : Rat) = 1 - (1 - 1 / 10) * (1 - 1 / 5) * (1 - 1 / 5)
+    grind
   · show (1127 / 3125 : Rat) = 1 - (1 - 1 / 1000) * (1 - 1 / 5) * (1 - 1 / 5)
     grind
 
+/-! ### 【仮定】層1: まだ検索に出ない -/
+
+/-- 証人: 4 < 4.2。 -/
+theorem prodDelay_le_test : indexDelaySec .fullText ≤ testDelaySec := by
+  show (4 : Rat) ≤ 21 / 5
+  grind
+
+/-- 証人: いまの検索（86400 秒）と安い設定の変更（43200 秒）で前提が成り立ち、結論 1/10 ≤ 1/10 が成り立つ。
+置き換えた後は前提が成り立たない（4 秒）。 -/
+theorem notYet_ge_of_slow : ∀ M : Method, 28800 ≤ indexDelaySec M → 1 / 10 ≤ (pNotYet M).val := by
+  intro M h
+  cases M
+  · show (1 / 10 : Rat) ≤ 1 / 10
+    grind
+  · show (1 / 10 : Rat) ≤ 1 / 10
+    grind
+  · have h' : (28800 : Rat) ≤ 4 := h
+    grind
+
+/-- 証人: 置き換えた後で前提が2つとも成り立ち（4 秒、欠けた記事なし）、結論 1/1000 ≤ 1/1000 が成り立つ。
+いまの検索と安い設定の変更では、遅れの前提が成り立たない（86400 秒、43200 秒）。 -/
+theorem notYet_le_of_fast : ∀ M : Method, indexDelaySec M ≤ 5 → IndexComplete M → (pNotYet M).val ≤ 1 / 1000 := by
+  intro M h _
+  cases M
+  · have h' : (86400 : Rat) ≤ 5 := h
+    grind
+  · have h' : (43200 : Rat) ≤ 5 := h
+    grind
+  · show (1 / 1000 : Rat) ≤ 1 / 1000
+    grind
+
+/-- 証人: `IndexComplete` はどの方式でも真。 -/
+theorem fullText_complete : IndexComplete .fullText := trivial
+
+/-! ### 【仮定】安い設定の変更の速さ -/
+
+/-- 証人: `CurrentIncremental` は偽。 -/
+theorem current_not_incremental : ¬ CurrentIncremental := fun h => h
+
+/-- 証人: 前提（`CurrentIncremental` は偽）が成り立ち、結論 28800 < 43200 が成り立つ。 -/
+theorem tuned_slow_of_rebuild : ¬ CurrentIncremental → 28800 ≤ indexDelaySec .tuned := by
+  intro _
+  show (28800 : Rat) ≤ 43200
+  grind
+
+/-! ### 【仮定】層2・層3: いまの検索の値 -/
+
+/-- 証人: 1/5 ≤ 1/5（境目の値）。 -/
+theorem noHit_current_le : (pNoHit .current).val ≤ 1 / 5 := by
+  show (1 / 5 : Rat) ≤ 1 / 5
+  grind
+
+/-- 証人: 1/5 ≤ 1/5（境目の値）。 -/
+theorem overlook_current_le : (pOverlook .current).val ≤ 1 / 5 := by
+  show (1 / 5 : Rat) ≤ 1 / 5
+  grind
+
+/-! ### 【仮定】層2・層3: 置き換えで悪くならない（主張の側が使う片側） -/
+
+/-- 証人: どの方式も同じ値（`noHit_full_ge` と合わせると、どの証人でも等しくなる）。 -/
+theorem noHit_full_le : (pNoHit .fullText).val ≤ (pNoHit .current).val := by
+  show (1 / 5 : Rat) ≤ 1 / 5
+  grind
+
+/-- 証人: どの方式も同じ値（`overlook_full_ge` と合わせると、どの証人でも等しくなる）。 -/
+theorem overlook_full_le : (pOverlook .fullText).val ≤ (pOverlook .current).val := by
+  show (1 / 5 : Rat) ≤ 1 / 5
+  grind
+
+/-! ### 【仮定】層2・層3: 置き換えでよくならない（不利な結論の側だけが使う片側） -/
+
+/-- 証人: どの方式も同じ値。 -/
+theorem noHit_full_ge : (pNoHit .current).val ≤ (pNoHit .fullText).val := by
+  show (1 / 5 : Rat) ≤ 1 / 5
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem overlook_full_ge : (pOverlook .current).val ≤ (pOverlook .fullText).val := by
+  show (1 / 5 : Rat) ≤ 1 / 5
+  grind
+
 /-! ### 【仮定】時間: いまの検索の値 -/
 
-/-- 証人: 4 ≤ 4。 -/
+/-- 証人: 4 ≤ 4（境目の値）。 -/
 theorem searches_current_ge : 4 ≤ searchesPerDay .current := by
   show (4 : Rat) ≤ 4
   grind
 
-/-- 証人: 5 ≤ 5。 -/
-theorem missExtra_current_ge : 5 ≤ missExtraMinutes .current := by
+/-- 証人: 5 ≤ 5（境目の値）。 -/
+theorem extraNotYet_current_ge : 5 ≤ extraNotYetMinutes .current := by
   show (5 : Rat) ≤ 5
   grind
 
-/-! ### 【仮定】時間: 同じとみなす -/
-
-/-- 証人: どちらの方式も同じ値。 -/
-theorem searches_same : searchesPerDay .fullText = searchesPerDay .current := rfl
-
-/-- 証人: どちらの方式も同じ値。 -/
-theorem foundMinutes_same : foundMinutes .fullText = foundMinutes .current := rfl
-
-/-- 証人: どちらの方式も同じ値。 -/
-theorem missExtra_same : missExtraMinutes .fullText = missExtraMinutes .current := rfl
+/-- 証人: 0 < 5。 -/
+theorem extraNotYet_nonneg : 0 ≤ extraNotYetMinutes .current := by
+  show (0 : Rat) ≤ 5
+  grind
+
+/-- 証人: 0 < 5。 -/
+theorem extraOther_nonneg : 0 ≤ extraOtherMinutes .current := by
+  show (0 : Rat) ≤ 5
+  grind
+
+/-- 証人: 5 ≤ 5（境目の値）。 -/
+theorem extraOther_le_notYet : extraOtherMinutes .current ≤ extraNotYetMinutes .current := by
+  show (5 : Rat) ≤ 5
+  grind
+
+/-! ### 【仮定】時間: 置き換えで悪くならない（主張の側が使う片側） -/
+
+/-- 証人: どの方式も同じ値。 -/
+theorem searches_full_le : searchesPerDay .fullText ≤ searchesPerDay .current := by
+  show (4 : Rat) ≤ 4
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem found_full_le : foundMinutes .fullText ≤ foundMinutes .current := by
+  show (72 / 25 : Rat) ≤ 72 / 25
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem extraNotYet_full_le : extraNotYetMinutes .fullText ≤ extraNotYetMinutes .current := by
+  show (5 : Rat) ≤ 5
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem extraOther_full_le : extraOtherMinutes .fullText ≤ extraOtherMinutes .current := by
+  show (5 : Rat) ≤ 5
+  grind
+
+/-! ### 【仮定】時間: 置き換えでよくならない（不利な結論の側だけが使う片側） -/
+
+/-- 証人: どの方式も同じ値。 -/
+theorem searches_full_ge : searchesPerDay .current ≤ searchesPerDay .fullText := by
+  show (4 : Rat) ≤ 4
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem found_full_ge : foundMinutes .current ≤ foundMinutes .fullText := by
+  show (72 / 25 : Rat) ≤ 72 / 25
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem extraNotYet_full_ge : extraNotYetMinutes .current ≤ extraNotYetMinutes .fullText := by
+  show (5 : Rat) ≤ 5
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem extraOther_full_ge : extraOtherMinutes .current ≤ extraOtherMinutes .fullText := by
+  show (5 : Rat) ≤ 5
+  grind
+
+/-! ### 【仮定】安い設定の変更は、層1のほかの点でよくならない（C0 の側だけが使う片側） -/
+
+/-- 証人: どの方式も同じ値。 -/
+theorem searches_tuned_ge : searchesPerDay .current ≤ searchesPerDay .tuned := by
+  show (4 : Rat) ≤ 4
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem found_tuned_ge : foundMinutes .current ≤ foundMinutes .tuned := by
+  show (72 / 25 : Rat) ≤ 72 / 25
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem extraNotYet_tuned_ge : extraNotYetMinutes .current ≤ extraNotYetMinutes .tuned := by
+  show (5 : Rat) ≤ 5
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem extraOther_tuned_ge : extraOtherMinutes .current ≤ extraOtherMinutes .tuned := by
+  show (5 : Rat) ≤ 5
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem noHit_tuned_ge : (pNoHit .current).val ≤ (pNoHit .tuned).val := by
+  show (1 / 5 : Rat) ≤ 1 / 5
+  grind
+
+/-- 証人: どの方式も同じ値。 -/
+theorem overlook_tuned_ge : (pOverlook .current).val ≤ (pOverlook .tuned).val := by
+  show (1 / 5 : Rat) ≤ 1 / 5
+  grind
 
 /-! ### 【仮定】金額に直す -/
 
-/-- 証人: 200 ≤ 200。 -/
+/-- 証人: 2,800,000 < 3,000,000。 -/
+theorem cost_le_estimate : firstYearCost ≤ estimateYen := by
+  show (2800000 : Rat) ≤ 3000000
+  grind
+
+/-- 証人: 200 ≤ 200（境目の値）。 -/
 theorem workDays_ge : 200 ≤ workDays := by
   show (200 : Rat) ≤ 200
   grind
 
-/-- 証人: 3000 ≤ 3000。 -/
+/-- 証人: 3000 ≤ 3000（境目の値）。 -/
 theorem wage_ge : 3000 ≤ wagePerHour := by
   show (3000 : Rat) ≤ 3000
   grind
 
+/-- 証人: 安い設定の変更に比べて取り戻せる時間の人件費は 4,120,000 × 1.2672 = 5,220,864 円で、6,000,000 円より少ない。 -/
+theorem gain_ge_wage : savedOverTunedWageYen ≤ gainYen := by
+  show (412 * 200 * 3000 / 60 : Rat)
+      * (4 * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5)
+        - 4 * (72 / 25 + 1 / 1000 * 5 + (1127 / 3125 - 1 / 1000) * 5)) ≤ 6000000
+  grind
+
 /-! ### 【仮定】読者の判断 -/
 
-/-- 証人: 20 ≤ 20。 -/
+/-- 証人: 15 < 20。 -/
 theorem many_threshold_le : manyMinutes ≤ 20 := by
-  show (20 : Rat) ≤ 20
-  grind
-
-/-- 証人: `CheaperFix` は偽。 -/
-theorem no_cheaper_fix : ¬ CheaperFix := fun h => h
-
-/-- 証人: `Approvable` は真。前提も2つとも成り立つ（5,220,864 円 > 3,000,000 円、`CheaperFix` は偽）。 -/
-theorem approvable_of_net : firstYearCost < benefitYen → ¬ CheaperFix → Approvable :=
-  fun _ _ => trivial
+  show (15 : Rat) ≤ 20
+  grind
+
+/-- 証人: `Approvable` を「初年度の費用 < 会社が得る値打ち」と定義したので、前提がそのまま結論になる。前提は成り立つ（2,800,000 円 < 6,000,000 円）。 -/
+theorem approvable_of_net : firstYearCost < gainYen → Approvable :=
+  fun h => h
 
 /-! ## §5 主張の定理 -/
 
-/-! ### 数の補題（関係公理を使わない） -/
+/-! ### 数と式の補題 -/
 
 /-- 0 以上の数どうしの不等式は、掛け合わせても成り立つ（a ≤ b、c ≤ d ならば a × c ≤ b × d）。 -/
@@ -302,4 +506,32 @@
   grind
 
+/-- どの方式でも、層2か層3で失敗する確率は 0 以上（層2・層3の確率の範囲だけから出る）。 -/
+theorem missAfterIndex_nonneg : ∀ M : Method, 0 ≤ missAfterIndex M := by
+  intro M
+  unfold missAfterIndex
+  have hb0 := (pNoHit M).nonneg
+  have hb1 := (pNoHit M).le_one
+  have hc0 := (pOverlook M).nonneg
+  have hc1 := (pOverlook M).le_one
+  have hx : (1 - (pNoHit M).val) * (1 - (pOverlook M).val) ≤ 1 * 1 :=
+    rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+  grind
+
+/-- どの方式でも、見つからない確率 − 層1の確率 =（1 − 層1の確率）× 層2か層3で失敗する確率（`miss_compose` の式の変形）。 -/
+theorem miss_sub_notYet : ∀ M : Method,
+    (missProb M).val - (pNotYet M).val = (1 - (pNotYet M).val) * missAfterIndex M := by
+  intro M
+  unfold missAfterIndex
+  rw [miss_compose M]
+  grind
+
+/-- どの方式でも、1日の探し物の時間 = 回数 ×（見つかった場合の時間 ＋ 層1の確率 × 層1の余分な時間 ＋
+（1 − 層1の確率）× 層2か層3で失敗する確率 × 層2・層3の余分な時間）（`search_decomp` と `miss_compose` の式の変形）。 -/
+theorem search_layers : ∀ M : Method,
+    searchMinutes M = searchesPerDay M * (foundMinutes M + (pNotYet M).val * extraNotYetMinutes M
+      + (1 - (pNotYet M).val) * missAfterIndex M * extraOtherMinutes M) := by
+  intro M
+  rw [search_decomp M, miss_sub_notYet M]
+
 /-! ### 途中の定理 -/
 
@@ -307,4 +539,8 @@
 theorem notYet_current_ge : 1 / 10 ≤ (pNotYet .current).val :=
   notYet_ge_of_slow .current delay_current_ge_workday
+
+/-- 安い設定の変更をしても、まだ検索に出ていない記事を探す確率は 1/10 以上。 -/
+theorem notYet_tuned_ge : 1 / 10 ≤ (pNotYet .tuned).val :=
+  notYet_ge_of_slow .tuned (tuned_slow_of_rebuild current_not_incremental)
 
 /-- 置き換えた後、まだ検索に出ていない記事を探す確率は 1/1000 以下。 -/
@@ -312,70 +548,213 @@
   have h1 := prodDelay_le_test
   have h2 := testDelay_le_five
-  exact notYet_le_of_fast .fullText (by grind)
-
-/-- いまの検索で、探し物1回が見つからない確率は 1/10 以上（層2・層3の値によらず、層1の確率以上になる）。 -/
-theorem miss_current_ge : 1 / 10 ≤ (missProb .current).val := by
-  have hm := miss_compose .current
-  have ha := notYet_current_ge
-  have ha1 := (pNotYet .current).le_one
-  have hb0 := (pNoHit .current).nonneg
-  have hb1 := (pNoHit .current).le_one
-  have hc0 := (pOverlook .current).nonneg
-  have hc1 := (pOverlook .current).le_one
-  have hx : (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) ≤ 1 * 1 :=
-    rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
-  have hy : (1 - (pNotYet .current).val) * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val))
-      ≤ (1 - (pNotYet .current).val) * (1 * 1) :=
-    Rat.mul_le_mul_of_nonneg_left hx (by grind)
-  grind
-
-/-- いまの検索の「失われている時間」（読み a）は、1人1日2分以上（4回 × 1/10 × 5分）。 -/
+  exact notYet_le_of_fast .fullText (by grind) fullText_complete
+
+/-- いまの検索の「失われている時間」（読み a）は、1人1日2分以上（4回 × 1/10 × 5分。層2・層3の分は0以上なので落とす）。 -/
 theorem lost_ge : 2 ≤ lostMinutes := by
   unfold lostMinutes
   have hs := searches_current_ge
-  have hm := miss_current_ge
-  have he := missExtra_current_ge
-  have h1 : 4 * (1 / 10) ≤ searchesPerDay .current * (missProb .current).val :=
-    rat_mul_le_mul (by grind) hs (by grind) hm
-  have h2 : 4 * (1 / 10) * 5 ≤ searchesPerDay .current * (missProb .current).val * missExtraMinutes .current :=
-    rat_mul_le_mul (by grind) h1 (by grind) he
-  grind
-
-/-- 取り戻せる時間（読み b）= 回数 × 余分な時間 ×（層2で失敗しない確率 × 層3で失敗しない確率）×（層1の確率の差）。
-取り戻せる時間は、層1の差からだけ生まれる。 -/
-theorem saved_only_from_notYet :
-    savedMinutes = searchesPerDay .current * missExtraMinutes .current
-      * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val))
-      * ((pNotYet .current).val - (pNotYet .fullText).val) := by
+  have ha := notYet_current_ge
+  have he := extraNotYet_current_ge
+  have ho := extraOther_nonneg
+  have hL := miss_sub_notYet .current
+  have hA := missAfterIndex_nonneg .current
+  have ha1 := (pNotYet .current).le_one
+  have hm : 0 ≤ (missProb .current).val - (pNotYet .current).val := by
+    rw [hL]
+    exact Rat.mul_nonneg (by grind) hA
+  have h1 : (1 / 10) * 5 ≤ (pNotYet .current).val * extraNotYetMinutes .current :=
+    rat_mul_le_mul (by grind) ha (by grind) he
+  have h2 : 0 ≤ ((missProb .current).val - (pNotYet .current).val) * extraOtherMinutes .current :=
+    Rat.mul_nonneg hm ho
+  have h3 : 4 * ((1 / 10) * 5) ≤ searchesPerDay .current * ((pNotYet .current).val * extraNotYetMinutes .current
+      + ((missProb .current).val - (pNotYet .current).val) * extraOtherMinutes .current) :=
+    rat_mul_le_mul (by grind) hs (by grind) (by grind)
+  grind
+
+/-- 取り戻せる時間（読み b）は、回数(いま) ×（層1の確率の差）×（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）以上。
+置き換えた後の量を、主張の側の片側の公理で、いまの検索の値に置き換えた上界から出す。 -/
+theorem saved_ge_gap :
+    searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val)
+      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current)
+      ≤ savedMinutes := by
   unfold savedMinutes
-  rw [search_decomp .current, search_decomp .fullText, miss_compose .current, miss_compose .fullText,
-    searches_same, foundMinutes_same, missExtra_same, noHit_same, overlook_same]
-  grind
-
-/-- 取り戻せる時間（読み b）は、1人1日 792/625 分（1.2672分）以上（4回 × 5分 ×（4/5 × 4/5）×（1/10 − 1/1000））。 -/
+  rw [search_layers .current, search_layers .fullText]
+  have hsf := searchesPerDay_nonneg .fullText
+  have hfc := foundMinutes_nonneg .current
+  have he1 := extraNotYet_current_ge
+  have he2 := extraOther_nonneg
+  have hs := searches_full_le
+  have hf := found_full_le
+  have hx1 := extraNotYet_full_le
+  have hx2 := extraOther_full_le
+  have hb := noHit_full_le
+  have hc := overlook_full_le
+  have hAf := missAfterIndex_nonneg .fullText
+  have hAc := missAfterIndex_nonneg .current
+  have hp0 := (pNotYet .fullText).nonneg
+  have hp1 := (pNotYet .fullText).le_one
+  have hA : missAfterIndex .fullText ≤ missAfterIndex .current := by
+    unfold missAfterIndex
+    have hb1 := (pNoHit .current).le_one
+    have hc1 := (pOverlook .current).le_one
+    have hx : (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val)
+        ≤ (1 - (pNoHit .fullText).val) * (1 - (pOverlook .fullText).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have h1 : (pNotYet .fullText).val * extraNotYetMinutes .fullText
+      ≤ (pNotYet .fullText).val * extraNotYetMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_left hx1 hp0
+  have h2a : missAfterIndex .fullText * extraOtherMinutes .fullText
+      ≤ missAfterIndex .fullText * extraOtherMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_left hx2 hAf
+  have h2b : missAfterIndex .fullText * extraOtherMinutes .current
+      ≤ missAfterIndex .current * extraOtherMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_right hA he2
+  have h3 : (1 - (pNotYet .fullText).val) * (missAfterIndex .fullText * extraOtherMinutes .fullText)
+      ≤ (1 - (pNotYet .fullText).val) * (missAfterIndex .current * extraOtherMinutes .current) :=
+    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
+  have hG : foundMinutes .fullText + (pNotYet .fullText).val * extraNotYetMinutes .fullText
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .fullText * extraOtherMinutes .fullText
+      ≤ foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have hG0a : 0 ≤ (pNotYet .fullText).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 (by grind)
+  have hG0b : 0 ≤ (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current :=
+    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
+  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have h4 := Rat.mul_le_mul_of_nonneg_left hG hsf
+  have h5 := Rat.mul_le_mul_of_nonneg_right hs hG0
+  grind
+
+/-- 取り戻せる時間（読み b）は、1人1日 792/625 分（1.2672分）以上（4回 ×（1/10 − 1/1000）×（16/25 × 5分））。 -/
 theorem saved_ge : 792 / 625 ≤ savedMinutes := by
-  rw [saved_only_from_notYet]
+  have hg := saved_ge_gap
   have hs := searches_current_ge
-  have he := missExtra_current_ge
+  have he1 := extraNotYet_current_ge
+  have hle := extraOther_le_notYet
+  have he2 := extraOther_nonneg
   have hb := noHit_current_le
   have hc := overlook_current_le
   have ha := notYet_current_ge
   have hf := notYet_fullText_le
-  have hx : (4 / 5) * (4 / 5) ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
-    rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
-  have h1 : 4 * 5 ≤ searchesPerDay .current * missExtraMinutes .current :=
-    rat_mul_le_mul (by grind) hs (by grind) he
-  have h2 : 4 * 5 * ((4 / 5) * (4 / 5))
-      ≤ searchesPerDay .current * missExtraMinutes .current
-        * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val)) :=
-    rat_mul_le_mul (by grind) h1 (by grind) hx
-  have h3 : 4 * 5 * ((4 / 5) * (4 / 5)) * (1 / 10 - 1 / 1000)
-      ≤ searchesPerDay .current * missExtraMinutes .current
-        * ((1 - (pNoHit .current).val) * (1 - (pOverlook .current).val))
-        * ((pNotYet .current).val - (pNotYet .fullText).val) :=
-    rat_mul_le_mul (by grind) h2 (by grind) (by grind)
-  grind
-
-/-- 1人1日1分の時間は、1年で 4,120,000円以上の人件費になる（412人 × 200日 × 3,000円 ÷ 60）。 -/
+  have hAc := missAfterIndex_nonneg .current
+  have h1A : 16 / 25 ≤ 1 - missAfterIndex .current := by
+    unfold missAfterIndex
+    have hx : (4 / 5) * (4 / 5) ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have hAe : missAfterIndex .current * extraOtherMinutes .current
+      ≤ missAfterIndex .current * extraNotYetMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_left hle hAc
+  have hq : (16 / 25) * 5 ≤ (1 - missAfterIndex .current) * extraNotYetMinutes .current :=
+    rat_mul_le_mul (by grind) h1A (by grind) he1
+  have hK : (16 / 25) * 5 ≤ extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have hP : 1 / 10 - 1 / 1000 ≤ (pNotYet .current).val - (pNotYet .fullText).val := by grind
+  have h1 : 4 * (1 / 10 - 1 / 1000) ≤ searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val) :=
+    rat_mul_le_mul (by grind) hs (by grind) hP
+  have h2 : 4 * (1 / 10 - 1 / 1000) * ((16 / 25) * 5)
+      ≤ searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val)
+        * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) :=
+    rat_mul_le_mul (by grind) h1 (by grind) hK
+  grind
+
+/-- 安い設定の変更に比べて取り戻せる時間は、回数(いま) ×（層1の確率の差。安い設定の変更と置き換えた後）×
+（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）以上。
+安い設定の変更の量を、C0 の側の片側の公理で、いまの検索の値に置き換えた下界を、`saved_ge_gap` に足して出す。 -/
+theorem savedOverTuned_ge_gap :
+    searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val)
+      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current)
+      ≤ savedOverTunedMinutes := by
+  have hg := saved_ge_gap
+  unfold savedMinutes at hg
+  unfold savedOverTunedMinutes
+  have hSc := search_layers .current
+  have hSt := search_layers .tuned
+  have hsc := searchesPerDay_nonneg .current
+  have hfc := foundMinutes_nonneg .current
+  have he1 := extraNotYet_current_ge
+  have he2 := extraOther_nonneg
+  have hs := searches_tuned_ge
+  have hf := found_tuned_ge
+  have hx1 := extraNotYet_tuned_ge
+  have hx2 := extraOther_tuned_ge
+  have hb := noHit_tuned_ge
+  have hc := overlook_tuned_ge
+  have hAt := missAfterIndex_nonneg .tuned
+  have hAc := missAfterIndex_nonneg .current
+  have hp0 := (pNotYet .tuned).nonneg
+  have hp1 := (pNotYet .tuned).le_one
+  have hA : missAfterIndex .current ≤ missAfterIndex .tuned := by
+    unfold missAfterIndex
+    have hb1 := (pNoHit .tuned).le_one
+    have hc1 := (pOverlook .tuned).le_one
+    have hx : (1 - (pNoHit .tuned).val) * (1 - (pOverlook .tuned).val)
+        ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have h1 : (pNotYet .tuned).val * extraNotYetMinutes .current
+      ≤ (pNotYet .tuned).val * extraNotYetMinutes .tuned :=
+    Rat.mul_le_mul_of_nonneg_left hx1 hp0
+  have h2a : missAfterIndex .current * extraOtherMinutes .current
+      ≤ missAfterIndex .tuned * extraOtherMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_right hA he2
+  have h2b : missAfterIndex .tuned * extraOtherMinutes .current
+      ≤ missAfterIndex .tuned * extraOtherMinutes .tuned :=
+    Rat.mul_le_mul_of_nonneg_left hx2 hAt
+  have h3 : (1 - (pNotYet .tuned).val) * (missAfterIndex .current * extraOtherMinutes .current)
+      ≤ (1 - (pNotYet .tuned).val) * (missAfterIndex .tuned * extraOtherMinutes .tuned) :=
+    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
+  have hG : foundMinutes .current + (pNotYet .tuned).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current
+      ≤ foundMinutes .tuned + (pNotYet .tuned).val * extraNotYetMinutes .tuned
+        + (1 - (pNotYet .tuned).val) * missAfterIndex .tuned * extraOtherMinutes .tuned := by
+    grind
+  have hG0a : 0 ≤ (pNotYet .tuned).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 (by grind)
+  have hG0b : 0 ≤ (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current :=
+    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
+  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .tuned).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .tuned).val) * missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have h4 := Rat.mul_le_mul_of_nonneg_right hs hG0
+  have h5 := Rat.mul_le_mul_of_nonneg_left hG (by grind : 0 ≤ searchesPerDay .tuned)
+  grind
+
+/-- 安い設定の変更に比べて取り戻せる時間は、1人1日 792/625 分（1.2672分）以上（4回 ×（1/10 − 1/1000）×（16/25 × 5分））。 -/
+theorem savedOverTuned_ge : 792 / 625 ≤ savedOverTunedMinutes := by
+  have hg := savedOverTuned_ge_gap
+  have hs := searches_current_ge
+  have he1 := extraNotYet_current_ge
+  have hle := extraOther_le_notYet
+  have he2 := extraOther_nonneg
+  have hb := noHit_current_le
+  have hc := overlook_current_le
+  have ha := notYet_tuned_ge
+  have hf := notYet_fullText_le
+  have hAc := missAfterIndex_nonneg .current
+  have h1A : 16 / 25 ≤ 1 - missAfterIndex .current := by
+    unfold missAfterIndex
+    have hx : (4 / 5) * (4 / 5) ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have hAe : missAfterIndex .current * extraOtherMinutes .current
+      ≤ missAfterIndex .current * extraNotYetMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_left hle hAc
+  have hq : (16 / 25) * 5 ≤ (1 - missAfterIndex .current) * extraNotYetMinutes .current :=
+    rat_mul_le_mul (by grind) h1A (by grind) he1
+  have hK : (16 / 25) * 5 ≤ extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have hP : 1 / 10 - 1 / 1000 ≤ (pNotYet .tuned).val - (pNotYet .fullText).val := by grind
+  have h1 : 4 * (1 / 10 - 1 / 1000) ≤ searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val) :=
+    rat_mul_le_mul (by grind) hs (by grind) hP
+  have h2 : 4 * (1 / 10 - 1 / 1000) * ((16 / 25) * 5)
+      ≤ searchesPerDay .current * ((pNotYet .tuned).val - (pNotYet .fullText).val)
+        * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) :=
+    rat_mul_le_mul (by grind) h1 (by grind) hK
+  grind
+
+/-- 1人1日1分の時間は、初年度に 4,120,000円以上の人件費になる（412人 × 200日 × 3,000円 ÷ 60）。 -/
 theorem yenPerDailyMinute_ge : 4120000 ≤ yenPerDailyMinute := by
   unfold yenPerDailyMinute
@@ -390,29 +769,42 @@
 /-! ### 主張の定理 -/
 
-/-- @claim C3 [確率] 読み (b): 初年度の費用は、置き換えで取り戻せる時間の1年分の人件費より小さい。 -/
-theorem claim_C3_saved : firstYearCost < benefitYen := by
-  unfold benefitYen
+/-- @claim C3 [確率] 読み (b): 初年度の費用は、置き換えで（いまのままと比べて）取り戻せる時間の初年度の人件費より小さい。 -/
+theorem claim_C3_saved : firstYearCost < savedWageYen := by
+  unfold savedWageYen
   have hy := yenPerDailyMinute_ge
   have hs := saved_ge
-  have hc := cost_eq
+  have hc := cost_le_estimate
+  have he := estimate_eq
   have h : 4120000 * (792 / 625) ≤ yenPerDailyMinute * savedMinutes :=
     rat_mul_le_mul (by grind) hy (by grind) hs
   grind
 
-/-- @claim C3 [確率] 読み (a): 初年度の費用は、いまの検索で失われている時間の1年分の人件費より小さい。 -/
-theorem claim_C3_lost : firstYearCost < lostYen := by
-  unfold lostYen
+/-- @claim C3 [確率] 読み (a): 初年度の費用は、いまの検索で失われている時間の初年度の人件費より小さい。 -/
+theorem claim_C3_lost : firstYearCost < lostWageYen := by
+  unfold lostWageYen
   have hy := yenPerDailyMinute_ge
   have hl := lost_ge
-  have hc := cost_eq
+  have hc := cost_le_estimate
+  have he := estimate_eq
   have h : 4120000 * 2 ≤ yenPerDailyMinute * lostMinutes :=
     rat_mul_le_mul (by grind) hy (by grind) hl
   grind
 
-/-- @claim C0 [確率] 来期予算で300万円を承認する理由がそろう。 -/
-theorem claim_C0_approvable : Approvable :=
-  approvable_of_net claim_C3_saved no_cheaper_fix
-
-/-- @claim C1 [決定論] いまの検索で1人1日に探し物に使う時間は、「多い」の境目以上。 -/
+/-- @claim C0 [確率] 来期予算で300万円を承認する理由がそろう。
+初年度の費用 ≤ 300万円 < 5,220,864円 ≤ 安い設定の変更に比べて取り戻せる時間の人件費 ≤ 会社が得る値打ち、から示す。 -/
+theorem claim_C0_approvable : Approvable := by
+  apply approvable_of_net
+  have hy := yenPerDailyMinute_ge
+  have hs := savedOverTuned_ge
+  have hg := gain_ge_wage
+  have hc := cost_le_estimate
+  have he := estimate_eq
+  unfold savedOverTunedWageYen at hg
+  have h : 4120000 * (792 / 625) ≤ yenPerDailyMinute * savedOverTunedMinutes :=
+    rat_mul_le_mul (by grind) hy (by grind) hs
+  grind
+
+/-- @claim C1 [決定論] いまの検索で1人1日に探し物に使う時間は、「多い」の境目以上。
+@restates many_threshold_le 理由: 「1日20分は多い」は読者の判断で、事実から導けない。その判断だけを【仮定】に切り出し、確信度 0.05 のまま主張の値に出しているので、隠してはいない。ステージ5で C1 を数字の文（1日平均20分）に言い換えるまで、このままにする -/
 theorem claim_C1_many : manyMinutes ≤ searchMinutes .current := by
   rw [search_current_eq]
@@ -433,12 +825,13 @@
 /-! ### 比べる相手の確認と、不利な結論 -/
 
-/-- @baseline いまの検索の「失われている時間」（読み a）を、アンケートの1日20分より大きく置いていない。 -/
+/-- @baseline いまの検索の「失われている時間」（読み a）を、アンケートの1日20分より大きく置いていない。
+失われている時間 = 20 − 回数 × 見つかった場合の時間。 -/
 theorem baseline_lost_le_survey : lostMinutes ≤ 20 := by
   unfold lostMinutes
   have hd := search_decomp .current
   have he := search_current_eq
-  have hs := searches_current_ge
+  have hs := searchesPerDay_nonneg .current
   have hf := foundMinutes_nonneg .current
-  have h0 : 0 ≤ searchesPerDay .current * foundMinutes .current := Rat.mul_nonneg (by grind) hf
+  have h0 : 0 ≤ searchesPerDay .current * foundMinutes .current := Rat.mul_nonneg hs hf
   grind
 
@@ -450,13 +843,127 @@
   grind
 
+/-- [不利] 置き換えで取り戻せる時間（読み b）は、回数(いま) ×（層1の確率の差）×（層1の余分な時間 − 層2か層3で失敗する確率 × 層2・層3の余分な時間）を超えない。
+層1の差が縮めば、効果もそれだけ縮む。置き換えた後の量を、不利な結論の側の片側の公理で、いまの検索の値に置き換えた下界から出す。
+主張の側の片側の公理（`_full_le`）も、量の仮定（4回、5分、10%）も通らない。 -/
+theorem unfav_saved_le_gap :
+    savedMinutes ≤ searchesPerDay .current * ((pNotYet .current).val - (pNotYet .fullText).val)
+      * (extraNotYetMinutes .current - missAfterIndex .current * extraOtherMinutes .current) := by
+  unfold savedMinutes
+  rw [search_layers .current, search_layers .fullText]
+  have hsf := searchesPerDay_nonneg .fullText
+  have hfc := foundMinutes_nonneg .current
+  have he1 := extraNotYet_nonneg
+  have he2 := extraOther_nonneg
+  have hs := searches_full_ge
+  have hf := found_full_ge
+  have hx1 := extraNotYet_full_ge
+  have hx2 := extraOther_full_ge
+  have hb := noHit_full_ge
+  have hc := overlook_full_ge
+  have hAf := missAfterIndex_nonneg .fullText
+  have hAc := missAfterIndex_nonneg .current
+  have hp0 := (pNotYet .fullText).nonneg
+  have hp1 := (pNotYet .fullText).le_one
+  have hA : missAfterIndex .current ≤ missAfterIndex .fullText := by
+    unfold missAfterIndex
+    have hb1 := (pNoHit .fullText).le_one
+    have hc1 := (pOverlook .fullText).le_one
+    have hx : (1 - (pNoHit .fullText).val) * (1 - (pOverlook .fullText).val)
+        ≤ (1 - (pNoHit .current).val) * (1 - (pOverlook .current).val) :=
+      rat_mul_le_mul (by grind) (by grind) (by grind) (by grind)
+    grind
+  have h1 : (pNotYet .fullText).val * extraNotYetMinutes .current
+      ≤ (pNotYet .fullText).val * extraNotYetMinutes .fullText :=
+    Rat.mul_le_mul_of_nonneg_left hx1 hp0
+  have h2a : missAfterIndex .current * extraOtherMinutes .current
+      ≤ missAfterIndex .fullText * extraOtherMinutes .current :=
+    Rat.mul_le_mul_of_nonneg_right hA he2
+  have h2b : missAfterIndex .fullText * extraOtherMinutes .current
+      ≤ missAfterIndex .fullText * extraOtherMinutes .fullText :=
+    Rat.mul_le_mul_of_nonneg_left hx2 hAf
+  have h3 : (1 - (pNotYet .fullText).val) * (missAfterIndex .current * extraOtherMinutes .current)
+      ≤ (1 - (pNotYet .fullText).val) * (missAfterIndex .fullText * extraOtherMinutes .fullText) :=
+    Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)
+  have hG : foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current
+      ≤ foundMinutes .fullText + (pNotYet .fullText).val * extraNotYetMinutes .fullText
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .fullText * extraOtherMinutes .fullText := by
+    grind
+  have hG0a : 0 ≤ (pNotYet .fullText).val * extraNotYetMinutes .current := Rat.mul_nonneg hp0 he1
+  have hG0b : 0 ≤ (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current :=
+    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hAc) he2
+  have hG0 : 0 ≤ foundMinutes .current + (pNotYet .fullText).val * extraNotYetMinutes .current
+        + (1 - (pNotYet .fullText).val) * missAfterIndex .current * extraOtherMinutes .current := by
+    grind
+  have h4 := Rat.mul_le_mul_of_nonneg_right hs hG0
+  have h5 := Rat.mul_le_mul_of_nonneg_left hG hsf
+  grind
+
 /-- [不利] 置き換えで取り戻せる時間（読み b）は、いまの検索で失われている時間（読み a）を超えない。 -/
 theorem unfav_saved_le_lost : savedMinutes ≤ lostMinutes := by
   unfold savedMinutes lostMinutes
-  rw [search_decomp .current, search_decomp .fullText, searches_same, foundMinutes_same, missExtra_same]
-  have hs := searches_current_ge
-  have he := missExtra_current_ge
-  have hm := (missProb .fullText).nonneg
-  have h0 : 0 ≤ searchesPerDay .current * (missProb .fullText).val * missExtraMinutes .current :=
-    Rat.mul_nonneg (Rat.mul_nonneg (by grind) hm) (by grind)
+  rw [search_decomp .current, search_decomp .fullText]
+  have hsf := searchesPerDay_nonneg .fullText
+  have hfc := foundMinutes_nonneg .current
+  have he1 := extraNotYet_nonneg
+  have he2 := extraOther_nonneg
+  have hs := searches_full_ge
+  have hf := found_full_ge
+  have hx1 := extraNotYet_full_ge
+  have hx2 := extraOther_full_ge
+  have hL := miss_sub_notYet .fullText
+  have hAf := missAfterIndex_nonneg .fullText
+  have hp0 := (pNotYet .fullText).nonneg
+  have hp1 := (pNotYet .fullText).le_one
+  have hm : 0 ≤ (missProb .fullText).val - (pNotYet .fullText).val := by
+    rw [hL]
+    exact Rat.mul_nonneg (by grind) hAf
+  have hq1 : 0 ≤ (pNotYet .fullText).val * extraNotYetMinutes .fullText := Rat.mul_nonneg hp0 (by grind)
+  have hq2 : 0 ≤ ((missProb .fullText).val - (pNotYet .fullText).val) * extraOtherMinutes .fullText :=
+    Rat.mul_nonneg hm (by grind)
+  have hI : foundMinutes .current ≤ foundMinutes .fullText + (pNotYet .fullText).val * extraNotYetMinutes .fullText
+      + ((missProb .fullText).val - (pNotYet .fullText).val) * extraOtherMinutes .fullText := by
+    grind
+  have h4 := Rat.mul_le_mul_of_nonneg_right hs hfc
+  have h5 := Rat.mul_le_mul_of_nonneg_left hI hsf
+  grind
+
+
+/-! ### 関係公理の前提が、証人の世界で成り立つこと -/
+
+-- `notYet_ge_of_slow` の前提は、いまの検索で成り立つ（86400 秒）。
+example : 28800 ≤ indexDelaySec .current := by
+  show (28800 : Rat) ≤ 86400
+  grind
+
+-- `notYet_ge_of_slow` の前提は、安い設定の変更でも成り立つ（43200 秒）。
+example : 28800 ≤ indexDelaySec .tuned := by
+  show (28800 : Rat) ≤ 43200
+  grind
+
+-- `notYet_le_of_fast` の1つ目の前提は、置き換えた後で成り立つ（4 秒）。
+example : indexDelaySec .fullText ≤ 5 := by
+  show (4 : Rat) ≤ 5
+  grind
+
+-- `notYet_le_of_fast` の2つ目の前提は、置き換えた後で成り立つ（欠けた記事がない）。
+example : IndexComplete .fullText := trivial
+
+-- `tuned_slow_of_rebuild` の前提は成り立つ（いまの仕組みは保存のたびに索引へ足せない）。
+example : ¬ CurrentIncremental := fun h => h
+
+-- `approvable_of_net` の前提は成り立つ（2,800,000 円 < 6,000,000 円）。
+example : firstYearCost < gainYen := by
+  show (2800000 : Rat) < 6000000
+  grind
+
+-- 取り戻せる時間は、主張の定理の下限（1.2672 分）ちょうどで、失われている時間（8.48 分）より短い。
+example : savedMinutes = 792 / 625 := by
+  show (4 : Rat) * (72 / 25 + 1 / 10 * 5 + (53 / 125 - 1 / 10) * 5)
+      - 4 * (72 / 25 + 1 / 1000 * 5 + (1127 / 3125 - 1 / 1000) * 5) = 792 / 625
+  grind
+
+example : lostMinutes = 212 / 25 := by
+  show (4 : Rat) * (1 / 10 * 5 + (53 / 125 - 1 / 10) * 5) = 212 / 25
   grind
 
```
