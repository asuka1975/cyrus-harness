# 差分と対応表（rounds/02 → いま）

`cyrus logic-round diff` が機械で作った。Reviewer は、差分の設計書の行が当たっているか、設計書にない変更がないかを確かめる。

## 変わった宣言

変化の種類: 「変更」はコード（公理の型、定理の文と証明、def）が変わった。「変更（印）」は `@confidence`・`@reviewer`・`@support`・【】などの印の行だけが変わった（`@reviewer` の行が消えていないかを見る）。「変更（説明だけ）」は docstring の説明だけが変わった。

| ファイル | 宣言 | 変化 |
|---|---|---|
| Argument.lean | `DaytimeUpdate` | 追加 |
| Argument.lean | `approvable_of_net` | 変更（印） |
| Argument.lean | `baseline_lost_le_survey` | 変更 |
| Argument.lean | `claim_C1_many` | 変更 |
| Argument.lean | `claim_C2_faster` | 変更 |
| Argument.lean | `claim_C2_soon` | 変更 |
| Argument.lean | `current_no_daytime` | 追加 |
| Argument.lean | `delay_current_ge_workday` | 削除 |
| Argument.lean | `extraNotYet_current_ge` | 変更（説明だけ） |
| Argument.lean | `extraNotYet_tuned_le` | 追加 |
| Argument.lean | `extraOther_tuned_le` | 追加 |
| Argument.lean | `found_tuned_le` | 追加 |
| Argument.lean | `fullText_complete` | 変更（説明だけ） |
| Argument.lean | `indexDelaySec` | 削除 |
| Argument.lean | `maxDelaySec` | 追加 |
| Argument.lean | `maxDelay_of_noDaytime` | 追加 |
| Argument.lean | `noHit_current_le` | 変更（説明だけ） |
| Argument.lean | `noHit_tuned_le` | 追加 |
| Argument.lean | `notYet_current_ge` | 変更 |
| Argument.lean | `notYet_fullText_le` | 変更 |
| Argument.lean | `notYet_ge_of_slow` | 削除 |
| Argument.lean | `notYet_ge_sameDay_stale` | 追加 |
| Argument.lean | `notYet_le_of_fast` | 削除 |
| Argument.lean | `notYet_le_of_maxFast` | 追加 |
| Argument.lean | `notYet_tuned_ge` | 変更 |
| Argument.lean | `overlook_current_le` | 変更（説明だけ） |
| Argument.lean | `overlook_tuned_le` | 追加 |
| Argument.lean | `pSameDay` | 追加 |
| Argument.lean | `pStale` | 追加 |
| Argument.lean | `prodDelay_le_test` | 削除 |
| Argument.lean | `prodMaxDelay_le_test` | 追加 |
| Argument.lean | `sameDay_current_ge` | 追加 |
| Argument.lean | `sameDay_tuned_ge` | 追加 |
| Argument.lean | `searchTime_current_eq` | 追加 |
| Argument.lean | `search_current_eq` | 削除 |
| Argument.lean | `searches_current_ge` | 変更（説明だけ） |
| Argument.lean | `searches_tuned_le` | 追加 |
| Argument.lean | `stale_of_noDaytime` | 追加 |
| Argument.lean | `testDelaySec` | 変更（説明だけ） |
| Argument.lean | `testDelay_le_five` | 変更（説明だけ） |
| Argument.lean | `tuned_no_daytime_of_rebuild` | 追加 |
| Argument.lean | `tuned_slow_of_rebuild` | 削除 |
| Argument.lean | `unfav_savedOverTuned_le_gap` | 追加 |
| Argument.lean | `unfav_saved_le_survey` | 変更 |
| Argument.lean | `wage_ge` | 変更（説明だけ） |
| Model.lean | `DaytimeUpdate` | 追加 |
| Model.lean | `baseline_lost_le_survey` | 変更 |
| Model.lean | `claim_C1_many` | 変更 |
| Model.lean | `claim_C2_faster` | 変更 |
| Model.lean | `claim_C2_soon` | 変更 |
| Model.lean | `current_no_daytime` | 追加 |
| Model.lean | `delay_current_ge_workday` | 削除 |
| Model.lean | `extraNotYet_tuned_le` | 追加 |
| Model.lean | `extraOther_tuned_le` | 追加 |
| Model.lean | `found_tuned_le` | 追加 |
| Model.lean | `indexDelaySec` | 削除 |
| Model.lean | `maxDelaySec` | 追加 |
| Model.lean | `maxDelay_of_noDaytime` | 追加 |
| Model.lean | `noHit_tuned_le` | 追加 |
| Model.lean | `notYet_current_ge` | 変更 |
| Model.lean | `notYet_fullText_le` | 変更 |
| Model.lean | `notYet_ge_of_slow` | 削除 |
| Model.lean | `notYet_ge_sameDay_stale` | 追加 |
| Model.lean | `notYet_le_of_fast` | 削除 |
| Model.lean | `notYet_le_of_maxFast` | 追加 |
| Model.lean | `notYet_tuned_ge` | 変更 |
| Model.lean | `overlook_tuned_le` | 追加 |
| Model.lean | `pSameDay` | 追加 |
| Model.lean | `pStale` | 追加 |
| Model.lean | `prodDelay_le_test` | 削除 |
| Model.lean | `prodMaxDelay_le_test` | 追加 |
| Model.lean | `sameDay_current_ge` | 追加 |
| Model.lean | `sameDay_tuned_ge` | 追加 |
| Model.lean | `searchTime_current_eq` | 追加 |
| Model.lean | `search_current_eq` | 削除 |
| Model.lean | `searches_tuned_le` | 追加 |
| Model.lean | `stale_of_noDaytime` | 追加 |
| Model.lean | `tuned_no_daytime_of_rebuild` | 追加 |
| Model.lean | `tuned_slow_of_rebuild` | 削除 |
| Model.lean | `unfav_savedOverTuned_le_gap` | 追加 |
| Model.lean | `unfav_saved_le_survey` | 変更 |

宣言の外（見出し・説明のコメントなど）で変わった行: 165

## 差分の設計書（model-plan-delta.md）の行と差分の対応

| # | 設計書の行 | 挙げた名前 | 当たった変更 |
|---|---|---|---|
| 1 | ／ 1 ／ 宣言の名前と意味を変える。「勤務時間中に保存した記事の、いちばん長い遅れ」に決める ／ `indexDela… | `indexDelaySec`, `maxDelaySec` | `indexDelaySec`, `maxDelaySec` |
| 2 | ／ 2 ／ 宣言を足す（Method → Prop） ／ `DaytimeUpdate` ／ R16 ／ | `DaytimeUpdate` | `DaytimeUpdate` |
| 3 | ／ 3 ／ 宣言を足す（Method → Prob） ／ `pSameDay` ／ R16 ／ | `pSameDay` | `pSameDay` |
| 4 | ／ 4 ／ 宣言を足す（Method → Prob） ／ `pStale` ／ R16 ／ | `pStale` | `pStale` |
| 5 | ／ 5 ／ 宣言の docstring の宣言名を直す ／ `testDelaySec` ／ R16 ／ | `testDelaySec` | `testDelaySec` |
| 6 | ／ 6 ／ 公理を消す。current_no_daytime と maxDelay_of_noDaytime に置き換え… | `delay_current_ge_workday` | `delay_current_ge_workday` |
| 7 | ／ 7 ／ 公理を消す。notYet_ge_sameDay_stale・stale_of_noDaytime・sameD… | `notYet_ge_of_slow` | `notYet_ge_of_slow` |
| 8 | ／ 8 ／ 公理を消す。tuned_no_daytime_of_rebuild に置き換える ／ `tuned_slow… | `tuned_slow_of_rebuild` | `tuned_slow_of_rebuild` |
| 9 | ／ 9 ／ 使う宣言の意味が変わったので、名前を変えて別の公理にする ／ `prodDelay_le_test` → `… | `prodDelay_le_test`, `prodMaxDelay_le_test` | `prodDelay_le_test`, `prodMaxDelay_le_test` |
| 10 | ／ 10 ／ 同上 ／ `notYet_le_of_fast` → `notYet_le_of_maxFast` ／ R… | `notYet_le_of_fast`, `notYet_le_of_maxFast` | `notYet_le_of_fast`, `notYet_le_of_maxFast` |
| 11 | ／ 11 ／ 【経験則】を足す ／ `current_no_daytime` ／ R16・R3 ／ | `current_no_daytime` | `current_no_daytime` |
| 12 | ／ 12 ／ 【自明】を足す ／ `maxDelay_of_noDaytime` ／ R16 ／ | `maxDelay_of_noDaytime` | `maxDelay_of_noDaytime` |
| 13 | ／ 13 ／ 【自明】を足す ／ `stale_of_noDaytime` ／ R16 ／ | `stale_of_noDaytime` | `stale_of_noDaytime` |
| 14 | ／ 14 ／ 【自明】を足す ／ `notYet_ge_sameDay_stale` ／ R16 ／ | `notYet_ge_sameDay_stale` | `notYet_ge_sameDay_stale` |
| 15 | ／ 15 ／ 【仮定】を足す ／ `sameDay_current_ge` ／ R16 ／ | `sameDay_current_ge` | `sameDay_current_ge` |
| 16 | ／ 16 ／ 【仮定】を足す（C0 に有利な片側） ／ `sameDay_tuned_ge` ／ R16 ／ | `sameDay_tuned_ge` | `sameDay_tuned_ge` |
| 17 | ／ 17 ／ 【仮定】を足す ／ `tuned_no_daytime_of_rebuild` ／ R16 ／ | `tuned_no_daytime_of_rebuild` | `tuned_no_daytime_of_rebuild` |
| 18 | ／ 18 ／ 【仮定】を足す（C0 に不利な片側） ／ `searches_tuned_le` ／ R17 ／ | `searches_tuned_le` | `searches_tuned_le` |
| 19 | ／ 19 ／ 【仮定】を足す（C0 に不利な片側） ／ `found_tuned_le` ／ R17 ／ | `found_tuned_le` | `found_tuned_le` |
| 20 | ／ 20 ／ 【仮定】を足す（C0 に不利な片側） ／ `extraNotYet_tuned_le` ／ R17 ／ | `extraNotYet_tuned_le` | `extraNotYet_tuned_le` |
| 21 | ／ 21 ／ 【仮定】を足す（C0 に不利な片側） ／ `extraOther_tuned_le` ／ R17 ／ | `extraOther_tuned_le` | `extraOther_tuned_le` |
| 22 | ／ 22 ／ 【仮定】を足す（C0 に不利な片側） ／ `noHit_tuned_le` ／ R17 ／ | `noHit_tuned_le` | `noHit_tuned_le` |
| 23 | ／ 23 ／ 【仮定】を足す（C0 に不利な片側） ／ `overlook_tuned_le` ／ R17 ／ | `overlook_tuned_le` | `overlook_tuned_le` |
| 24 | ／ 24 ／ [不利] の定理を足す（印なし） ／ `unfav_savedOverTuned_le_gap` ／ R1… | `unfav_savedOverTuned_le_gap` | `unfav_savedOverTuned_le_gap` |
| 25 | ／ 25 ／ 使う判断を変える（示すことは同じ） ／ `notYet_current_ge` ／ R16 ／ | `notYet_current_ge` | `notYet_current_ge` |
| 26 | ／ 26 ／ 使う判断を変える（示すことは同じ） ／ `notYet_tuned_ge` ／ R16 ／ | `notYet_tuned_ge` | `notYet_tuned_ge` |
| 27 | ／ 27 ／ 使う公理の名前が変わる ／ `notYet_fullText_le` ／ R16 ／ | `notYet_fullText_le` | `notYet_fullText_le` |
| 28 | ／ 28 ／ 型の宣言名と、使う公理の名前が変わる ／ `claim_C2_soon` ／ R16 ／ | `claim_C2_soon` | `claim_C2_soon` |
| 29 | ／ 29 ／ 型と使う判断を変える ／ `claim_C2_faster` ／ R16 ／ | `claim_C2_faster` | `claim_C2_faster` |
| 30 | ／ 30 ／ 2周目に使う宣言（searchMinutes）の意味を変えたので、名前を変えて別の公理にする ／ `sea… | `searchTime_current_eq`, `search_current_eq` | `searchTime_current_eq`, `search_current_eq` |
| 31 | ／ 31 ／ 使う公理の名前が変わる ／ `claim_C1_many` ／ R20 ／ | `claim_C1_many` | `claim_C1_many` |
| 32 | ／ 32 ／ 使う公理の名前が変わる ／ `baseline_lost_le_survey` ／ R20 ／ | `baseline_lost_le_survey` | `baseline_lost_le_survey` |
| 33 | ／ 33 ／ 使う公理の名前が変わる ／ `unfav_saved_le_survey` ／ R20 ／ | `unfav_saved_le_survey` | `unfav_saved_le_survey` |
| 34 | ／ 34 ／ docstring（弱い点の公理名） ／ `testDelay_le_five` ／ R16 ／ | `testDelay_le_five` | `testDelay_le_five` |
| 35 | ／ 35 ／ docstring（論拠と弱い点） ／ `extraNotYet_current_ge` ／ R8 ／ | `extraNotYet_current_ge` | `extraNotYet_current_ge` |
| 36 | ／ 36 ／ docstring（向きと弱い点） ／ `searches_current_ge` ／ R8 ／ | `searches_current_ge` | `searches_current_ge` |
| 37 | ／ 37 ／ docstring（向きと弱い点） ／ `wage_ge` ／ R8 ／ | `wage_ge` | `wage_ge` |
| 38 | ／ 38 ／ docstring（向き） ／ `noHit_current_le` ／ R8 ／ | `noHit_current_le` | `noHit_current_le` |
| 39 | ／ 39 ／ docstring（向き） ／ `overlook_current_le` ／ R8 ／ | `overlook_current_le` | `overlook_current_le` |
| 40 | ／ 40 ／ docstring（論拠・弱い点・要ファクト） ／ `approvable_of_net` ／ R18 ／ | `approvable_of_net` | `approvable_of_net` |
| 41 | ／ 41 ／ docstring（論拠と弱い点） ／ `fullText_complete` ／ 監査の注記（閲覧の権限… | `fullText_complete` | `fullText_complete` |

## 命題（型）が変わったのに名前が同じ公理

命題を変えたら名前も変えて別の公理にする決まり。`@reviewer` が残っているものは、前の周の Reviewer の判断が、変わった命題には当てはまらない。

なし

## 設計書に名前の出ていない変更

なし

## 差分の全文

行ごとの差分は `07-logic/diff.patch` にある（963 行）。
