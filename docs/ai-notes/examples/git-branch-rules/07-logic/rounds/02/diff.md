# 差分と対応表（rounds/01 → いま）

`cyrus logic-round diff` が機械で作った。Reviewer は、差分の設計書の行が当たっているか、設計書にない変更がないかを確かめる。

## 変わった宣言

変化の種類: 「変更」はコードが変わった。「変更（印）」は `@confidence`・`@reviewer`・`@support`・【】などの印の行だけが変わった（`@reviewer` の行が消えていないかを見る）。「変更（説明だけ）」は docstring の説明だけが変わった。

| ファイル | 宣言 | 変化 |
|---|---|---|
| Argument.lean | `FollowsFlow` | 変更 |
| Argument.lean | `Op` | 変更（説明だけ） |
| Argument.lean | `admin_exempt_by_default` | 削除 |
| Argument.lean | `approval_covers_content` | 変更（印） |
| Argument.lean | `approvedBy` | 変更（説明だけ） |
| Argument.lean | `approved_change_can_break` | 変更（印） |
| Argument.lean | `approver_not_author` | 変更（印） |
| Argument.lean | `bypassDisallowed` | 追加 |
| Argument.lean | `bypass_exempt_by_default` | 追加 |
| Argument.lean | `bypassesProtection` | 追加 |
| Argument.lean | `c0_team_flow` | 変更 |
| Argument.lean | `c1_direct_push_can_stop_team` | 変更 |
| Argument.lean | `c3_flow_reviews_every_entry` | 削除 |
| Argument.lean | `c3_own_changes_approved_by_other` | 追加 |
| Argument.lean | `c3_own_changes_reviewed_by_other` | 追加 |
| Argument.lean | `c5_only_pr_route_when_protected` | 変更 |
| Argument.lean | `directPushBlocked` | 追加 |
| Argument.lean | `hasCheckedRecipe` | 削除 |
| Argument.lean | `hasFixedRecipe` | 追加 |
| Argument.lean | `inPRWhenApproved` | 変更（説明だけ） |
| Argument.lean | `incident_direct_push_broke_build` | 削除 |
| Argument.lean | `incident_direct_push_stopped_team` | 追加 |
| Argument.lean | `isAdmin` | 削除 |
| Argument.lean | `main_entry_has_op` | 削除 |
| Argument.lean | `merge_content_origin` | 変更（印） |
| Argument.lean | `newcomer_can_commit` | 変更（印） |
| Argument.lean | `newcomer_no_bypass` | 追加 |
| Argument.lean | `newcomer_not_admin` | 削除 |
| Argument.lean | `next_month_block_requires_pr` | 追加 |
| Argument.lean | `protectedMain` | 変更（説明だけ） |
| Argument.lean | `protectionCoversAdmins` | 削除 |
| Argument.lean | `protection_only_approved_pr` | 変更 |
| Argument.lean | `protection_rejects_push` | 変更 |
| Argument.lean | `pushRejected` | 変更（説明だけ） |
| Argument.lean | `push_joins_pr` | 変更（印） |
| Argument.lean | `pushedAfterApproval` | 変更（説明だけ） |
| Argument.lean | `pushed_after_not_seen` | 変更（印） |
| Argument.lean | `recipe_create_branch` | 変更 |
| Argument.lean | `recipe_doable` | 変更 |
| Argument.lean | `recipe_open_pr` | 変更 |
| Argument.lean | `recipe_push_branch` | 変更 |
| Argument.lean | `recipe_push_fix` | 変更 |
| Argument.lean | `recipe_request_review` | 変更 |
| Argument.lean | `recipe_squash_merge` | 変更 |
| Argument.lean | `recipe_update_main` | 変更 |
| Argument.lean | `u1_push_after_approval_unseen` | 変更（印） |
| Argument.lean | `u3_merge_needs_another_person` | 変更 |
| Argument.lean | `u4_admin_still_unblocked` | 削除 |
| Argument.lean | `u4_bypasser_still_unblocked` | 追加 |
| Argument.lean | `u5_nonfollower_unreviewed_entry` | 追加 |
| Argument.lean | `unrejected_push_lands` | 変更（説明だけ） |
| Model.lean | `FollowsFlow` | 変更 |
| Model.lean | `Op` | 変更（説明だけ） |
| Model.lean | `admin_exempt_by_default` | 削除 |
| Model.lean | `approval_covers_content` | 変更（印） |
| Model.lean | `approvedBy` | 変更（説明だけ） |
| Model.lean | `approved_change_can_break` | 変更 |
| Model.lean | `approver_not_author` | 変更（印） |
| Model.lean | `bringing_changes_main` | 変更 |
| Model.lean | `bringing_needs_doing` | 変更 |
| Model.lean | `bringsInVia` | 変更 |
| Model.lean | `bypassDisallowed` | 追加 |
| Model.lean | `bypass_exempt_by_default` | 追加 |
| Model.lean | `bypassesProtection` | 追加 |
| Model.lean | `c0_team_flow` | 変更 |
| Model.lean | `c1_direct_push_can_stop_team` | 変更 |
| Model.lean | `c3_flow_reviews_every_entry` | 削除 |
| Model.lean | `c3_own_changes_approved_by_other` | 追加 |
| Model.lean | `c3_own_changes_reviewed_by_other` | 追加 |
| Model.lean | `c5_only_pr_route_when_protected` | 変更 |
| Model.lean | `directPushBlocked` | 追加 |
| Model.lean | `direct_write_skips_pr` | 変更 |
| Model.lean | `doesOp` | 変更 |
| Model.lean | `hasCheckedRecipe` | 削除 |
| Model.lean | `hasFixedRecipe` | 追加 |
| Model.lean | `inPRWhenApproved` | 変更（説明だけ） |
| Model.lean | `incident_direct_push_broke_build` | 削除 |
| Model.lean | `incident_direct_push_stopped_team` | 追加 |
| Model.lean | `isAdmin` | 削除 |
| Model.lean | `main_entry_has_op` | 削除 |
| Model.lean | `merge_content_origin` | 変更（印） |
| Model.lean | `newcomer_can_commit` | 変更（印） |
| Model.lean | `newcomer_no_bypass` | 追加 |
| Model.lean | `newcomer_not_admin` | 削除 |
| Model.lean | `next_month_block_requires_pr` | 追加 |
| Model.lean | `protectedMain` | 変更（説明だけ） |
| Model.lean | `protectionCoversAdmins` | 削除 |
| Model.lean | `protection_only_approved_pr` | 変更 |
| Model.lean | `protection_rejects_push` | 変更 |
| Model.lean | `pushRejected` | 変更（説明だけ） |
| Model.lean | `push_joins_pr` | 変更（印） |
| Model.lean | `pushedAfterApproval` | 変更（説明だけ） |
| Model.lean | `pushed_after_not_seen` | 変更（印） |
| Model.lean | `recipe_create_branch` | 変更 |
| Model.lean | `recipe_doable` | 変更 |
| Model.lean | `recipe_open_pr` | 変更 |
| Model.lean | `recipe_push_branch` | 変更 |
| Model.lean | `recipe_push_fix` | 変更 |
| Model.lean | `recipe_request_review` | 変更 |
| Model.lean | `recipe_squash_merge` | 変更 |
| Model.lean | `recipe_update_main` | 変更 |
| Model.lean | `squash_brings_all_pr` | 変更 |
| Model.lean | `squash_content_from_pr` | 変更 |
| Model.lean | `triesDirectPush` | 変更 |
| Model.lean | `u1_push_after_approval_unseen` | 変更（印） |
| Model.lean | `u3_merge_needs_another_person` | 変更 |
| Model.lean | `u4_admin_still_unblocked` | 削除 |
| Model.lean | `u4_bypasser_still_unblocked` | 追加 |
| Model.lean | `u5_nonfollower_unreviewed_entry` | 追加 |
| Model.lean | `unrejected_push_lands` | 変更 |

宣言の外（見出し・説明のコメントなど）で変わった行: 80

## 差分の設計書（model-plan-delta.md）の行と差分の対応

| # | 設計書の行 | 挙げた名前 | 当たった変更 |
|---|---|---|---|
| 1 | ／ D1 ／ H1 ／ `FollowsFlow` に月を1つ目の引数として足し、「その月に流れを守る」にする（型は M… | `FollowsFlow` | `FollowsFlow` |
| 2 | ／ D2 ／ H2・L1 ／ `FollowsFlow` の (c) の説明を、C3 の括弧書きに合わせて書き直す。「s… | `FollowsFlow` | `FollowsFlow` |
| 3 | ／ D3 ／ L1 ／ `approvedBy`・`inPRWhenApproved`・`pushedAfterAppr… | `approvedBy`, `inPRWhenApproved`, `pushedAfterApproval` | `approvedBy`, `inPRWhenApproved`, `pushedAfterApproval` |
| 4 | ／ D4 ／ H1・M1 ／ `Op` の説明で、直接の書き込み（directWriteMain）を「プルリクエストのマ… | `Op` | `Op` |
| 5 | ／ D5 ／ M3 ／ `isAdmin` を消し、`bypassesProtection`（Person → Prop… | `bypassesProtection`, `isAdmin` | `bypassesProtection`, `isAdmin` |
| 6 | ／ D6 ／ M3 ／ `protectionCoversAdmins` を消し、`bypassDisallowed`（… | `bypassDisallowed`, `protectionCoversAdmins` | `bypassDisallowed`, `protectionCoversAdmins` |
| 7 | ／ D7 ／ M4 ／ `directPushBlocked`（Month → Prop）を足す。意味は「その月、mai… | `directPushBlocked` | `directPushBlocked` |
| 8 | ／ D8 ／ M4 ／ `protectedMain` の意味を「その月、main のブランチ保護で『Require a… | `protectedMain` | `protectedMain` |
| 9 | ／ D9 ／ L4 ／ `pushRejected` の説明に「設定の水準の述語。手元の main が古いときに Git… | `pushRejected` | `pushRejected` |
| 10 | ／ D10 ／ L2 ／ `hasCheckedRecipe` を消し、`hasFixedRecipe`（Op → Pr… | `hasCheckedRecipe`, `hasFixedRecipe` | `hasCheckedRecipe`, `hasFixedRecipe` |
| 11 | ／ A1 ／ M6 ／ `incident_direct_push_broke_build` を消し、`incident… | `incident_direct_push_broke_build`, `incident_direct_push_stopped_team` | `incident_direct_push_broke_build`, `incident_direct_push_stopped_team` |
| 12 | ／ A2 ／ H1・M1 ／ `main_entry_has_op` を消す。読み (i)（main に入る変更すべて）… | `main_entry_has_op` | `main_entry_has_op` |
| 13 | ／ A3 ／ L1 ／ `merge_content_origin`・`pushed_after_not_seen`・`… | `approval_covers_content`, `merge_content_origin`, `push_joins_pr`, `pushed_after_not_seen` | `approval_covers_content`, `merge_content_origin`, `push_joins_pr`, `pushed_after_not_seen` |
| 14 | ／ A4 ／ M2 ／ `approval_covers_content` に「要ファクト: 社内で、プルリクエストを承… | `approval_covers_content` | `approval_covers_content` |
| 15 | ／ A5 ／ M3 ／ `protection_rejects_push`・`protection_only_appro… | `protection_only_approved_pr`, `protection_rejects_push` | `protection_only_approved_pr`, `protection_rejects_push` |
| 16 | ／ A6 ／ M3 ／ `newcomer_not_admin` を消し、`newcomer_no_bypass`（【仮… | `newcomer_no_bypass`, `newcomer_not_admin` | `newcomer_no_bypass`, `newcomer_not_admin` |
| 17 | ／ A7 ／ M3 ／ `admin_exempt_by_default` を消し、`bypass_exempt_by_… | `admin_exempt_by_default`, `bypass_exempt_by_default` | `admin_exempt_by_default`, `bypass_exempt_by_default` |
| 18 | ／ A8 ／ M4 ／ `next_month_block_requires_pr`（【仮定】）を足す。命題は「来月、直… | `next_month_block_requires_pr` | `next_month_block_requires_pr` |
| 19 | ／ A9 ／ L4 ／ `unrejected_push_lands` の弱い点を「手元の main が古いと、GitH… | `unrejected_push_lands` | `unrejected_push_lands` |
| 20 | ／ A10 ／ L2 ／ `recipe_update_main`・`recipe_create_branch`・`re… | `recipe_create_branch`, `recipe_doable`, `recipe_open_pr`, `recipe_push_branch`, `recipe_push_fix`, `recipe_request_review`, `recipe_squash_merge`, `recipe_update_main` | `recipe_create_branch`, `recipe_doable`, `recipe_open_pr`, `recipe_push_branch`, `recipe_push_fix`, `recipe_request_review`, `recipe_squash_merge`, `recipe_update_main` |
| 21 | ／ A11 ／ L2 ／ `recipe_doable` の命題を「決まった短い操作がある操作のうち、本人が行うものは、… | `recipe_doable` | `recipe_doable` |
| 22 | ／ T1 ／ M6 ／ `c1_direct_push_can_stop_team` を、A1 の新しい公理だけで示す。… | `c1_direct_push_can_stop_team` | `c1_direct_push_can_stop_team` |
| 23 | ／ T2 ／ H1・M1 ／ `c3_flow_reviews_every_entry` を消す。読み (i) の定理で… | `c3_flow_reviews_every_entry` | `c3_flow_reviews_every_entry` |
| 24 | ／ T3 ／ H1・M1・H2 ／ `c3_own_changes_approved_by_other` を足す（@cl… | `c3_own_changes_approved_by_other` | `c3_own_changes_approved_by_other` |
| 25 | ／ T4 ／ H1・M1・M2 ／ `c3_own_changes_reviewed_by_other` を足す（@cl… | `c3_own_changes_reviewed_by_other` | `c3_own_changes_reviewed_by_other` |
| 26 | ／ T5 ／ M4 ／ `c5_only_pr_route_when_protected` の前提を「来月、直接 pus… | `c5_only_pr_route_when_protected` | `c5_only_pr_route_when_protected` |
| 27 | ／ T6 ／ H1・M4 ／ `c0_team_flow` の C3 の項を T3・T4 の結論の2つに、C5 の項を … | `c0_team_flow` | `c0_team_flow` |
| 28 | ／ T7 ／ L1 ／ `u1_push_after_approval_unseen` の説明を「最後の承認のあとに p… | `u1_push_after_approval_unseen` | `u1_push_after_approval_unseen` |
| 29 | ／ T8 ／ H1 ／ `u3_merge_needs_another_person` の型の「流れを守る」を、D1 の… | `u3_merge_needs_another_person` | `u3_merge_needs_another_person` |
| 30 | ／ T9 ／ M3・L6 ／ `u4_admin_still_unblocked` を消し、`u4_bypasser_s… | `u4_admin_still_unblocked`, `u4_bypasser_still_unblocked` | `u4_admin_still_unblocked`, `u4_bypasser_still_unblocked` |
| 31 | ／ T10 ／ 新設（C3 の読みの変更に伴う） ／ `u5_nonfollower_unreviewed_entry`… | `u5_nonfollower_unreviewed_entry` | `u5_nonfollower_unreviewed_entry` |

## 設計書に名前の出ていない変更

- `approved_change_can_break`
- `approver_not_author`
- `newcomer_can_commit`

## 差分（unified diff）

```diff
--- rounds/01/Argument.lean
+++ Argument.lean
@@ -2,5 +2,5 @@
 # 論証のモデル: 新人向け Gitブランチ運用ルール
 
-設計書: `07-logic/model-plan.md`。主張: `05-claims.json`。事実: `06-facts.json`。
+設計書: `07-logic/model-plan.md`（1周目）と `07-logic/model-plan-delta.md`（2周目の差分）。主張: `05-claims.json`。事実: `06-facts.json`。
 
 ## 書き方の約束（ガイド `stages/07-logic.md` の「Writer の約束」の要約）
@@ -20,5 +20,5 @@
 
 種類: [決定論] Prop の世界、[確率] 確率・期待値の比較、[件数] 件数の比較、[不利] 書き手の結論に不利な定理。
-比較の文の主張はないので、すべて [決定論] で組む（設計書1節）。
+比較の文の主張はないので、すべて [決定論] で組む（設計書1節、差分の設計書0節）。
 
 | 主張 | 主張の文 | 定理 | 種類 |
@@ -27,27 +27,30 @@
 | C1 | main への直接 push は、チーム全員の作業を止めたり、未レビューの変更を本番に出しかけたりする危険がある。 | `c1_direct_push_can_stop_team`、`c1_direct_push_unreviewed_release` | [決定論] |
 | C2 | 直接 push は今月はまだ仕組みで止められないので、一人ひとりが流れを守る必要がある。 | `c2_only_self_stops_this_month` | [決定論] |
-| C3 | この流れを守るかぎり、main に入る変更はすべて、マージ前にほかの人のレビューと承認を通る。 | `c3_flow_reviews_every_entry`（補題 `flow_changes_main_only_by_merge`、印なし） | [決定論] |
+| C3 | この流れ（承認のあとに commit を足したら、もう一度レビューを頼むことを含む）を自分が守るかぎり、自分が main に入れる変更はすべて、マージ前にほかの人のレビューと承認を通る。 | `c3_own_changes_approved_by_other`（承認の項）、`c3_own_changes_reviewed_by_other`（レビューの項）（補題 `flow_changes_main_only_by_merge`、印なし） | [決定論] |
 | C4 | コンフリクト（同じ箇所の変更の衝突）が起きなければ、社内の決まりに沿った手順で、新人でも最初から最後まで自分で進められる。 | `c4_flow_follows_rules`、`c4_newcomer_can_do_own_steps` | [決定論] |
 | C5 | 来月、仕組みで直接 push が拒否されるようになっても、この流れを知っておく必要がある。 | `c5_only_pr_route_when_protected` | [決定論] |
-| （C3 の限界） | 承認のあとに push した変更は、承認した人に見られないまま main に入る | `u1_push_after_approval_unseen`（印なし） | [不利] |
+| （C3 の限界） | 最後の承認のあとに push した変更は、古い承認のままマージすると、承認した人に見られないまま main に入る | `u1_push_after_approval_unseen`（印なし） | [不利] |
 | （C0・01-intent の限界） | 流れを守っても、全員の作業を止める変更が main に入りうる | `u2_reviewed_change_can_stop_team`（印なし） | [不利] |
 | （C4 の限界） | マージまで進むには、ほかの人の承認が要る | `u3_merge_needs_another_person`（印なし） | [不利] |
-| （C5 の限界） | 保護が入っても、管理者の直接 push は（管理者に効かせる設定がなければ）通る | `u4_admin_still_unblocked`（印なし） | [不利] |
+| （C5 の限界） | 保護が入っても、保護を迂回できる人の直接 push は（その人にも効かせる設定がなければ）通る | `u4_bypasser_still_unblocked`（印なし） | [不利] |
+| （C3 の限界） | 流れを守らない人の直接の書き込みで、承認を得たプルリクエストを通らない変更が main に入ったことがある（C3 は自分の変更にしか言えない） | `u5_nonfollower_unreviewed_entry`（印なし） | [不利] |
 
 ## 設計書（model-plan.md）との違い
+
+この周でも残る違いだけを書く（差分の設計書 8節の指示）。
 
 1. 関係公理 `bringing_enters_main`（【自明】「ある操作で変更を main に入れたなら、その変更は main に入っている」）を足した。
    設計書の `main_feeds_release`・`broken_main_stops_team` は「main に入った変更」（`entersMain`）についての公理だが、
-   それを使う定理（C1・C2・U2）は「直接書き込んだ」「squash merge で入れた」（`bringsInVia`）から出発する。
-   設計書には `entersMain` から `bringsInVia` への向き（`main_entry_has_op`）しかなく、逆の向きがないと定理を示せない。
+   それを使う定理（C1 の2つ目・C2・U2）は「直接書き込んだ」「squash merge で入れた」（`bringsInVia`）から出発する。
+   設計書には `bringsInVia` から `entersMain` への向きの公理がなく、それがないと定理を示せない。
    `bringsInVia` の意味（その操作で、その変更を main に入れる）から、語の定義として言えるので【自明】にした。
 2. `merge_content_origin` に、前提「`q` がそのプルリクエストを承認した」（`approvedBy pr q`）を足した。
-   「承認の時点」は、承認した人がいて初めて決まるため。公理は設計書の文より弱くなる（前提が増える）。
-3. `u3_merge_needs_another_person` は、設計書の「あわせて `doneByAuthor .approve = false`」を、定理の結論の `∧` の1項目として入れた。
-4. 帰納型に `deriving DecidableEq` を付けた（`teamFlow` に含まれるかどうかを `decide` で確かめるためと、証人の証明のため）。
-5. 証人（`Model.lean`）の世界を、設計書5節の見通しと変えた。見通しでは `approvedBy`・`pushedAfterApproval`・`isAdmin`・`protectedMain` が
-   いつも偽で、`merge_content_origin`・`approval_covers_content`・`approver_not_author`・U1 の3つの公理・`protection_rejects_push`・
-   `admin_exempt_by_default` などの前提が一度も成り立たない（空回りする）。証人では、人を4人（新人・レビューする人・管理者・流れを守らない人）、
-   プルリクエストを2本（承認のあとに push がないもの・あるもの）にし、来月だけ保護を有効にして、これらの前提が成り立つ例を持たせた。
+   「最後の承認の時点」は、承認した人がいて初めて決まるため。公理は設計書の文より弱くなる（前提が増える）。
+3. 帰納型に `deriving DecidableEq` を付けた（`teamFlow` に含まれるかどうかを `decide` で確かめるためと、証人の証明のため）。
+4. 支える事実のない【仮定】4つの `@confidence` を、設計書の案より下げて 0.05 にした。
+   `approver_not_author`（案 0.8）、`approved_change_can_break`（案 0.5）、`newcomer_can_commit`（案 0.6）、`recipe_doable`（案 0.5）。
+   証拠のない【仮定】は、案によらず CLI の値が 0.05 になるため、案も 0.05 と書く決まりに合わせた。命題と型は変えていない。計算した確信度も変わらない。
+5. 証人（`Model.lean`）に、差分の設計書8節にない例を足した。今月、人 3 が変更 4 を直接 push しようとし、拒否されずに main に直接書き込む。
+   1周目の証人では `triesDirectPush` が先月にしかなく、C2 の定理の前提が一度も成り立たなかったため。あわせて `doesOp` を、`bringsInVia` の各場合と人 1 の承認に合わせて並べた。
 -/
 
@@ -70,6 +73,7 @@
 `pushBranch` は `git push -u origin <ブランチ名>`、`openPR` はプルリクエストを作ること、`requestReview` はレビューする人の指定、
 `pushFix` は指摘に応える commit を同じブランチへ push すること、`approve` はレビューする人の承認、`squashMerge` は squash merge、
-`otherMerge` は squash 以外の方法でのマージ、`directWriteMain` は main への直接の書き込み（push と、GitHub の画面での直接編集の両方）。
-この語彙で main を変える操作が尽きるという判断は、型には置かず、関係公理 `main_entry_has_op` に置く。 -/
+`otherMerge` は squash 以外の方法でのマージ、`directWriteMain` は main への直接の書き込み
+（プルリクエストのマージによらずに main の中身を変える書き込みすべて。push、GitHub の画面での直接編集、API など、手段を問わない）。
+main を変える手段がこの語彙に尽きるのは、直接の書き込みを「マージ以外のすべて」と定義したことによる（語の定義）。 -/
 inductive Op where
   | updateMain
@@ -126,6 +130,6 @@
 axiom newcomer : Person
 
-/-- その人がリポジトリの管理者である。 -/
-axiom isAdmin : Person → Prop
+/-- その人は、ブランチ保護の制限を受けない立場にある（リポジトリの管理者の権限か、保護を迂回する権限を持つ役割）。 -/
+axiom bypassesProtection : Person → Prop
 
 /-- その人がリポジトリに push できる権限を持っている。 -/
@@ -150,12 +154,16 @@
 axiom triesDirectPush : Month → Person → Change → Prop
 
-/-- その月、その人の main への直接 push を GitHub が拒否する。 -/
+/-- その月、その人の main への直接 push を GitHub が拒否する。
+設定の水準の述語。手元の main が古いときに GitHub が fast-forward でない push を断るような、1回ごとの拒否は含まない。 -/
 axiom pushRejected : Month → Person → Prop
 
-/-- その月、main にブランチ保護（「Require a pull request before merging」）が有効になっている。 -/
+/-- その月、main への直接 push を拒否する設定が GitHub に入っている（どの設定かは問わない）。 -/
+axiom directPushBlocked : Month → Prop
+
+/-- その月、main のブランチ保護で「Require a pull request before merging」が、必要な承認数1以上で有効になっている。 -/
 axiom protectedMain : Month → Prop
 
-/-- その月の保護の設定が、管理者にも効くようになっている。 -/
-axiom protectionCoversAdmins : Month → Prop
+/-- その月の保護の設定が、迂回できる立場の人にも効くようになっている。 -/
+axiom bypassDisallowed : Month → Prop
 
 /-- その月、その人がそのプルリクエストを squash merge する。 -/
@@ -165,11 +173,11 @@
 axiom inPRAtMerge : Change → PR → Prop
 
-/-- マージの前に、その人がそのプルリクエストを承認した。 -/
+/-- マージの前に、その人がそのプルリクエストを1回以上承認した。 -/
 axiom approvedBy : PR → Person → Prop
 
-/-- その人が承認した時点で、その変更がプルリクエストに入っていた。 -/
+/-- その人の、マージ前の最後の承認の時点で、その変更がプルリクエストに入っていた。 -/
 axiom inPRWhenApproved : Change → PR → Person → Prop
 
-/-- その人の承認のあとに、その変更がプルリクエストのブランチに push された。 -/
+/-- その人の、マージ前の最後の承認のあとに、その変更がプルリクエストのブランチに push された。 -/
 axiom pushedAfterApproval : Change → PR → Person → Prop
 
@@ -192,6 +200,6 @@
 axiom releaseCandidate : Change → Prop
 
-/-- その操作を行う決まったコマンドか画面の操作があり、その動きを確かめてある。 -/
-axiom hasCheckedRecipe : Op → Prop
+/-- その操作を行う、決まった短いコマンドか画面の操作がある。 -/
+axiom hasFixedRecipe : Op → Prop
 
 /-- 新人が、その操作を自分で行える。 -/
@@ -243,13 +251,13 @@
   bringsInVia m p .directWriteMain c
 
-/-- 文書の言う「流れを守る」。次の3つを満たすこと。
+/-- 文書の言う「その月に流れを守る」。その月について、次の3つを満たすこと。
 (a) する操作はすべて `teamFlow` に含まれる（main への直接の書き込みも、squash 以外のマージもしない）。
 (b) squash merge するのは、自分が出したプルリクエストだけ。
-(c) squash merge するプルリクエストには、承認した人 `q` がいて、その承認のあとに push された変更がない
-（承認のあとに push したら、承認を受け直してからマージする）。 -/
-def FollowsFlow (p : Person) : Prop :=
-  (∀ m o, doesOp m p o → o ∈ teamFlow) ∧
-  (∀ m pr, squashMerges m p pr → author pr = p) ∧
-  (∀ m pr, squashMerges m p pr → ∃ q, approvedBy pr q ∧ ∀ c, ¬ pushedAfterApproval c pr q)
+(c) squash merge するプルリクエストには、承認した人 `q` がいて、`q` の最後の承認のあとに push された変更がない
+（承認のあとに commit を足したら、もう一度レビューを頼み、承認を受け直してからマージする）。 -/
+def FollowsFlow (m : Month) (p : Person) : Prop :=
+  (∀ o, doesOp m p o → o ∈ teamFlow) ∧
+  (∀ pr, squashMerges m p pr → author pr = p) ∧
+  (∀ pr, squashMerges m p pr → ∃ q, approvedBy pr q ∧ ∀ c, ¬ pushedAfterApproval c pr q)
 
 /-! ## §4 関係公理 -/
@@ -257,9 +265,9 @@
 /-! ### C1・C2: 直接 push の危険 -/
 
-/-- 【実験】先月、main に直接書き込まれ、ビルドを壊した変更がある。
+/-- 【実験】先月、main に直接書き込まれ、チーム全員の作業を止めた変更がある。
 @support F1
-論拠: 先月の1回目の事故（F1）。
+論拠: 先月の1回目の事故で、main に直接 push した変更のために、半日チーム全員の作業が止まった（F1）。1件の事実から存在を言うだけで、一般化を含まない。
 弱い点: 依頼者の証言だけで、社内の事故記録は確かめていない（F1）。 -/
-axiom incident_direct_push_broke_build : ∃ p c, directlyWrites .lastMonth p c ∧ breaksBuild c
+axiom incident_direct_push_stopped_team : ∃ p c, directlyWrites .lastMonth p c ∧ stopsTeam c
 
 /-- 【自明】main に直接書き込んだ変更は、承認を得たプルリクエストを通っていない。
@@ -295,16 +303,8 @@
 @confidence 0.6
 論拠: 拒否されない push は受け入れられる。先月の直接 push は実際に main に入った（F1・F2）。
-弱い点: 手元の main が古いと、git が push を断る（`git pull` のあとなら通る）。 -/
+弱い点: 手元の main が古いと、GitHub が fast-forward でない push を断る（`git pull` のあとなら通る）。この拒否は、設定の水準の拒否（`pushRejected`）には入らない。 -/
 axiom unrejected_push_lands : ∀ m p c, triesDirectPush m p c → ¬ pushRejected m p → directlyWrites m p c
 
-/-! ### C3: 流れを守れば、main に入る変更はレビューを通る -/
-
-/-- 【仮定】main に入る変更には、それを入れた人と、`Op` の語彙のどれかの操作がある。
-@support なし（GitHub で main の中身を変える方法を並べた事実と、社内の自動の仕組みについての事実が、まだない）
-@confidence 0.7
-論拠: main の中身は、誰かが何かの操作をしたときにしか変わらない。`Op` は直接の書き込み・squash merge・それ以外のマージを含む。
-弱い点: 語彙の外の操作（API での書き込みなど）が `directWriteMain` に入るかは、定義の広さによる。ボットが流れを守らずに main に書き込むなら、C3 の条件「全員が流れを守る」が成り立たない。
-要ファクト: GitHub で main の中身を変える方法が、直接の書き込み（push・画面での直接編集）と、プルリクエストのマージ（squash とそれ以外）に尽きることを GitHub Docs で確かめる。あわせて、社内に main へ書き込む自動の仕組み（ボットなど）があるかをユーザーに確かめる。 -/
-axiom main_entry_has_op : ∀ m c, entersMain m c → ∃ p o, bringsInVia m p o c
+/-! ### C3: 流れを守れば、自分が main に入れる変更はレビューと承認を通る -/
 
 /-- 【自明】ある操作で変更を main に入れたなら、その人はその操作をしている。
@@ -365,22 +365,23 @@
 axiom squash_content_from_pr : ∀ m p c, bringsInVia m p .squashMerge c → ∃ pr, squashMerges m p pr ∧ inPRAtMerge c pr
 
-/-- 【経験則】マージの時点でプルリクエストに入っている変更は、そのプルリクエストを承認した人の承認の時点で入っていたか、承認のあとに push されたかのどちらか。
+/-- 【経験則】マージの時点でプルリクエストに入っている変更は、そのプルリクエストを承認した人の最後の承認の時点で入っていたか、最後の承認のあとに push されたかのどちらか。
 @support F6 F8
 @confidence 0.8
 論拠: プルリクエストの中身はブランチの commit で（F6）、ブランチに push した commit は自動で加わる（F8）。
-弱い点: 画面の「Update branch」や、レビューする人の提案を画面で取り込む commit も、承認のあとに中身を変える。これらを push とみなせば成り立つ。 -/
+弱い点: 画面の「Update branch」や、レビューする人の提案を画面で取り込む commit も、最後の承認のあとに中身を変える。これらを push とみなせば成り立つ。 -/
 axiom merge_content_origin : ∀ c pr q, inPRAtMerge c pr → approvedBy pr q → inPRWhenApproved c pr q ∨ pushedAfterApproval c pr q
 
-/-- 【経験則】承認の時点でプルリクエストに入っていた変更は、承認した人が見たうえで承認している。
+/-- 【経験則】承認した人の最後の承認の時点でプルリクエストに入っていた変更は、その人が見たうえで承認している。
 @support F6
 @confidence 0.05
 @reviewer 0.05 ← 0.7 理由: F6 が述べるのは「プルリクエストは、マージの前に変更を話し合い、レビューできる機能」ということだけで、承認した人が中身を見たうえで承認しているか（社内での承認の出し方）は述べていない。この公理が言う人の振る舞いを支える事実がない。
 論拠: プルリクエストは、マージの前に変更を話し合い、レビューする機能（F6）で、承認はその中身に対して出す。
-弱い点: 中身を読まずに承認することはありうる。社内で承認がどう出されているかは確かめていない。 -/
+弱い点: 中身を読まずに承認することはありうる。社内で承認がどう出されているかは確かめていない。F6 は、プルリクエストがレビューのための機能であることを述べるだけで、承認する人の振る舞いは述べていない（F6）。
+要ファクト: 社内で、プルリクエストを承認する人が、差分（変更の中身）を読んでから承認しているかを、ユーザーに確かめる。承認のあとに足された commit を、頼み直したレビューで読んでいるかも含む。 -/
 axiom approval_covers_content : ∀ c pr q, approvedBy pr q → inPRWhenApproved c pr q → reviewedBy c q
 
 /-- 【仮定】プルリクエストを承認した人は、それを出した本人ではない。
 @support なし（本人が自分のプルリクエストを承認できないことを確かめた事実が、まだない）
-@confidence 0.8
+@confidence 0.05
 論拠: 「ほかの人のレビュー」の「ほかの人」を支える。
 弱い点: 事実がまだない。
@@ -390,5 +391,5 @@
 /-! ### U1: 承認のあとの push（不利な結論のため） -/
 
-/-- 【実験】承認のあとに push された変更も、マージの時点でプルリクエストに入っている。
+/-- 【実験】最後の承認のあとに push された変更も、マージの時点でプルリクエストに入っている。
 @support F8
 論拠: プルリクエストを出したあとに同じブランチへ push した commit は、自動で加わる（F8）。
@@ -401,6 +402,6 @@
 axiom squash_brings_all_pr : ∀ m p pr c, squashMerges m p pr → inPRAtMerge c pr → bringsInVia m p .squashMerge c
 
-/-- 【自明】承認のあとに push された変更は、承認の時点ではプルリクエストに入っていなかった。
-論拠: 承認のあとに加わったものは、承認の時点ではまだない（時の前後の定義）。 -/
+/-- 【自明】ある人の最後の承認のあとに push された変更は、その人の最後の承認の時点ではプルリクエストに入っていなかった。
+論拠: 最後の承認のあとに加わったものは、その承認の時点ではまだない（時の前後の定義）。 -/
 axiom pushed_after_not_seen : ∀ c pr q, pushedAfterApproval c pr q → ¬ inPRWhenApproved c pr q
 
@@ -409,5 +410,5 @@
 /-- 【仮定】承認を得たプルリクエストの squash merge で main に入り、ビルドを壊す変更がある。
 @support なし（社内で、承認を受けてマージした変更がビルドを壊した記録が、まだない）
-@confidence 0.5
+@confidence 0.05
 論拠: レビューは人が読むもので、見落としがありうる。
 弱い点: 社内の事例がまだない。
@@ -449,46 +450,46 @@
 /-! ### C4: 新人が自分で進められること -/
 
-/-- 【実験】手元の main を最新にする操作（`git switch main` と `git pull`）があり、動きを確かめてある。
+/-- 【実験】手元の main を最新にする、決まった操作（`git switch main` と `git pull`）がある。
 @support F15
 論拠: 実行して確かめた（F15）。
 弱い点: GitHub ではなく手元のリモートで確かめた（F15）。 -/
-axiom recipe_update_main : hasCheckedRecipe .updateMain
-
-/-- 【実験】ブランチを作って移る操作（`git switch -c`）があり、動きを確かめてある。
+axiom recipe_update_main : hasFixedRecipe .updateMain
+
+/-- 【実験】ブランチを作って移る、決まった操作（`git switch -c`）がある。
 @support F10
 論拠: 実行して確かめた（F10）。
 弱い点: git 2.23 より古い git にはこのコマンドがない。 -/
-axiom recipe_create_branch : hasCheckedRecipe .createBranch
-
-/-- 【実験】作業ブランチを GitHub に送る操作（`git push -u origin <ブランチ名>`）があり、動きを確かめてある。
+axiom recipe_create_branch : hasFixedRecipe .createBranch
+
+/-- 【実験】作業ブランチを GitHub に送る、決まった操作（`git push -u origin <ブランチ名>`）がある。
 @support F13
 論拠: 実行して確かめた（F13）。
 弱い点: GitHub ではなく手元のリモートで確かめた（F13）。GitHub への認証の手間は含まない。 -/
-axiom recipe_push_branch : hasCheckedRecipe .pushBranch
-
-/-- 【実験】push したブランチからプルリクエストを作る画面の操作があり、確かめてある。
+axiom recipe_push_branch : hasFixedRecipe .pushBranch
+
+/-- 【実験】push したブランチからプルリクエストを作る、決まった画面の操作がある。
 @support F14
 論拠: GitHub Docs（F14）。 -/
-axiom recipe_open_pr : hasCheckedRecipe .openPR
-
-/-- 【実験】レビューする人（Reviewers）を指定する画面の操作があり、確かめてある。
+axiom recipe_open_pr : hasFixedRecipe .openPR
+
+/-- 【実験】レビューする人（Reviewers）を指定する、決まった画面の操作がある。
 @support F14
 論拠: GitHub Docs（F14）。 -/
-axiom recipe_request_review : hasCheckedRecipe .requestReview
-
-/-- 【実験】同じブランチに push すればプルリクエストに加わることを確かめてある。
+axiom recipe_request_review : hasFixedRecipe .requestReview
+
+/-- 【実験】指摘に応える commit を同じブランチに送る、決まった操作（commit と push）がある。
 @support F8
-論拠: GitHub Docs（F8）。操作そのものは commit と push で、新人が知っている。 -/
-axiom recipe_push_fix : hasCheckedRecipe .pushFix
-
-/-- 【実験】squash merge する画面の操作（「Squash and merge」）があり、動きを確かめてある。
+論拠: 同じブランチに push すればプルリクエストに加わる（GitHub Docs、F8）。操作そのものは commit と push で、新人が知っている。 -/
+axiom recipe_push_fix : hasFixedRecipe .pushFix
+
+/-- 【実験】squash merge する、決まった画面の操作（「Squash and merge」）がある。
 @support F12
 論拠: GitHub Docs（F12）。画面のボタンは「Squash and merge」。
 弱い点: ボタンを押せるかはリポジトリの権限による。 -/
-axiom recipe_squash_merge : hasCheckedRecipe .squashMerge
+axiom recipe_squash_merge : hasFixedRecipe .squashMerge
 
 /-- 【仮定】新人は、作業ブランチに自分で commit できる。
 @support なし（読者像に書いてあるだけで、事実として登録されていない）
-@confidence 0.6
+@confidence 0.05
 論拠: 03-reader.json に「Git で commit と push はできる」とある。
 弱い点: 06-facts.json に事実として登録されていないので、`@support` にできない。
@@ -503,29 +504,29 @@
 axiom newcomer_can_write : canWrite newcomer
 
-/-- 【仮定】決まった操作があり動きを確かめてある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える。
+/-- 【仮定】決まった短い操作がある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える。
 @support なし（新人が文書の手順どおりに進めた記録が、まだない）
-@confidence 0.5
-論拠: 1つずつの操作は、決まったコマンドか画面の操作で済み、文書で説明する。
+@confidence 0.05
+論拠: 1つずつの操作は、決まったコマンドか画面の操作で済む。文書は、流れの各操作を、その決まった操作で説明する。
 弱い点: 新人に実際に通してもらった記録がない。ブランチ・プルリクエスト・マージ・レビューは読者の知らない語（03-reader.json）なので、本文での説明の出来に左右される。
 要ファクト: 新人（または同じくらいの経験の人）に、文書の手順どおりにプルリクエストを1本通してもらい、詰まった操作を記録する。 -/
-axiom recipe_doable : ∀ o, hasCheckedRecipe o → doneByAuthor o = true → canWrite newcomer → noConflict → canDo o
+axiom recipe_doable : ∀ o, hasFixedRecipe o → doneByAuthor o = true → canWrite newcomer → noConflict → canDo o
 
 /-! ### C5: 保護が入ったあとの経路 -/
 
-/-- 【実験】保護が有効な月は、管理者でない人の直接 push は拒否される。
+/-- 【実験】保護が有効な月は、保護を迂回できない人の直接 push は拒否される。
 @support F4
 @confidence 0.75
 @reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人は、だれでも拒否される」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
 論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
-弱い点: 初期設定では管理者に効かない（F4）。 -/
-axiom protection_rejects_push : ∀ m p, protectedMain m → ¬ isAdmin p → pushRejected m p
-
-/-- 【実験】保護が有効な月に、管理者でない人が main に入れる変更は、承認を得たプルリクエストを通ったものだけ。
+弱い点: 初期設定では、管理者などには効かない（F4）。その人たちは、迂回できる立場として前提で除いてある。 -/
+axiom protection_rejects_push : ∀ m p, protectedMain m → ¬ bypassesProtection p → pushRejected m p
+
+/-- 【実験】保護が有効な月に、保護を迂回できない人が main に入れる変更は、承認を得たプルリクエストを通ったものだけ。
 @support F4
 @confidence 0.75
 @reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人が入れる変更は、どれも承認を得たプルリクエストを通る」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
 論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
-弱い点: 初期設定では管理者に効かない（F4）。 -/
-axiom protection_only_approved_pr : ∀ m p o c, protectedMain m → ¬ isAdmin p → bringsInVia m p o c → viaApprovedPR c
+弱い点: 初期設定では、管理者などには効かない（F4）。その人たちは、迂回できる立場として前提で除いてある。 -/
+axiom protection_only_approved_pr : ∀ m p o c, protectedMain m → ¬ bypassesProtection p → bringsInVia m p o c → viaApprovedPR c
 
 /-- 【実験】承認を得たプルリクエストで入った変更は、main 以外のブランチから出したプルリクエストで入っている。
@@ -534,18 +535,27 @@
 axiom pr_needs_work_branch : ∀ c, viaApprovedPR c → fromWorkBranch c
 
-/-- 【仮定】新人はリポジトリの管理者ではない。
-@support なし（新人の権限を確かめた事実が、まだない）
-@confidence 0.8
-論拠: 新人に管理者の権限を渡すことはふつうない。
+/-- 【仮定】新人は、保護を迂回できる立場にない（管理者の権限も、迂回の権限も持たない）。
+@support なし（新人のリポジトリでの役割を確かめた事実が、まだない）
+@confidence 0.05
+論拠: 新人に、管理者の権限や、保護を迂回する権限を渡すことは、ふつうない。
 弱い点: 事実がまだない。
-要ファクト: 新人のリポジトリでの権限が管理者でないことを、ユーザーに確かめる。 -/
-axiom newcomer_not_admin : ¬ isAdmin newcomer
-
-/-! ### U4: 管理者は来月も止まらない（不利な結論のため） -/
-
-/-- 【実験】保護の設定が管理者に効くようになっていなければ、管理者の直接 push は拒否されない。
+要ファクト: 新人のリポジトリでの役割（権限）が、管理者でも、保護を迂回できる役割でもないことを、ユーザーに確かめる。 -/
+axiom newcomer_no_bypass : ¬ bypassesProtection newcomer
+
+/-- 【仮定】来月、直接 push を拒否する設定が入るなら、それは承認1名以上のプルリクエストを必須にする保護である。
+@support なし（F3 は「直接 push を拒否する設定に来月変える予定」と述べるだけで、どの設定を入れるか、必要な承認数をいくつにするかは述べていない。F7 は社内の決まりで、GitHub の設定ではない）
+@confidence 0.05
+論拠: main への直接 push を止める設定としてふつう使うのは、マージの前にプルリクエストを必須にする保護で、社内の決まり（承認1名以上）とも合う。
+弱い点: 承認を求めずに直接 push だけを止める設定（承認数 0 や、push できる人を限る設定など）もありうる。その場合、C5 の結論は「承認を得たプルリクエストだけ」ではなく「プルリクエストを通ったものだけ」に弱まる。
+要ファクト: 来月 main に入れる設定が「Require a pull request before merging」か、必要な承認数を1以上にするかを、ユーザーに確かめる。 -/
+axiom next_month_block_requires_pr : directPushBlocked .nextMonth → protectedMain .nextMonth
+
+/-! ### U4: 保護を迂回できる人は来月も止まらない（不利な結論のため） -/
+
+/-- 【実験】保護の設定が迂回できる立場の人にも効くようになっていなければ、その人の直接 push は拒否されない。
 @support F4
-論拠: 初期設定では、保護の制限は管理者に効かない（F4）。 -/
-axiom admin_exempt_by_default : ∀ m p, isAdmin p → ¬ protectionCoversAdmins m → ¬ pushRejected m p
+論拠: 初期設定では、保護の制限は、リポジトリの管理者の権限を持つ人に効かない（F4）。迂回の権限を持つ役割は、その権限の意味から、制限を受けない。
+弱い点: F4 の引用が直接述べるのは、管理者の権限を持つ人だけである。迂回の権限を持つ役割は、F4 の「管理者など」に含めて読んでいる（F4）。 -/
+axiom bypass_exempt_by_default : ∀ m p, bypassesProtection p → ¬ bypassDisallowed m → ¬ pushRejected m p
 
 /-! ## §5 主張の定理 -/
@@ -555,6 +565,6 @@
 /-- @claim C1 [決定論] main への直接の書き込みで、チーム全員の作業が止まることがある（先月、実際に起きた）。 -/
 theorem c1_direct_push_can_stop_team : ∃ m p c, directlyWrites m p c ∧ stopsTeam c := by
-  obtain ⟨p, c, hw, hb⟩ := incident_direct_push_broke_build
-  exact ⟨.lastMonth, p, c, hw, broken_main_stops_team .lastMonth c (bringing_enters_main _ _ _ _ hw) hb⟩
+  obtain ⟨p, c, hw, hs⟩ := incident_direct_push_stopped_team
+  exact ⟨.lastMonth, p, c, hw, hs⟩
 
 /-- @claim C1 [決定論] main に直接書き込んだ変更は、承認を得たプルリクエストを通らないまま、本番に出る候補になる。 -/
@@ -594,24 +604,32 @@
   · rfl
 
-/-- @claim C3 [決定論] 全員が流れを守るかぎり、main に入る変更はすべて、squash merge したプルリクエストに入っていて、
-そのプルリクエストを、マージした本人とは別の人が承認し、その人がその変更を見たうえで承認している。 -/
-theorem c3_flow_reviews_every_entry :
-    (∀ p, FollowsFlow p) → ∀ m c, entersMain m c →
-      ∃ p pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q := by
-  intro hflow m c hc
-  obtain ⟨p, o, hb⟩ := main_entry_has_op m c hc
-  obtain ⟨hops, hauth, happ⟩ := hflow p
-  have hmem : o ∈ teamFlow := hops m o (bringing_needs_doing m p o c hb)
+/-- @claim C3 [決定論] その月に流れを守る人が、その月に main に入れる変更は、どれも、その人が squash merge したプルリクエストに入っていて、
+その人とは別の人が承認していて、その別の人の最後の承認の時点で、その変更はプルリクエストに入っていた（C3 の「ほかの人の承認を通る」）。 -/
+theorem c3_own_changes_approved_by_other :
+    ∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
+      ∃ pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ inPRWhenApproved c pr q := by
+  intro m p hflow o c hb
+  obtain ⟨hops, hauth, happ⟩ := hflow
+  have hmem : o ∈ teamFlow := hops o (bringing_needs_doing m p o c hb)
   have ho : o = .squashMerge := flow_changes_main_only_by_merge o hmem (bringing_changes_main m p o c hb)
   subst ho
   obtain ⟨pr, hsq, hin⟩ := squash_content_from_pr m p c hb
-  obtain ⟨q, hq, hfresh⟩ := happ m pr hsq
+  obtain ⟨q, hq, hfresh⟩ := happ pr hsq
   have hseen : inPRWhenApproved c pr q := by
     rcases merge_content_origin c pr q hin hq with h | h
     · exact h
     · exact absurd h (hfresh c)
-  refine ⟨p, pr, q, hsq, hin, hq, ?_, approval_covers_content c pr q hq hseen⟩
+  refine ⟨pr, q, hsq, hin, hq, ?_, hseen⟩
   intro hqp
-  exact approver_not_author pr q hq (hqp.trans (hauth m pr hsq).symm)
+  exact approver_not_author pr q hq (hqp.trans (hauth pr hsq).symm)
+
+/-- @claim C3 [決定論] その月に流れを守る人が、その月に main に入れる変更は、どれも、その人が squash merge したプルリクエストを
+その人とは別の人が承認していて、その別の人がその変更を見たうえで承認している（C3 の「ほかの人のレビューを通る」）。 -/
+theorem c3_own_changes_reviewed_by_other :
+    ∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
+      ∃ pr q, squashMerges m p pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q := by
+  intro m p hflow o c hb
+  obtain ⟨pr, q, hsq, _, hq, hne, hseen⟩ := c3_own_changes_approved_by_other m p hflow o c hb
+  exact ⟨pr, q, hsq, hq, hne, approval_covers_content c pr q hq hseen⟩
 
 /-! ### C4 -/
@@ -651,14 +669,15 @@
 /-! ### C5 -/
 
-/-- @claim C5 [決定論] 来月、保護が有効になれば、新人の直接 push は拒否され、新人が main に入れられる変更は、
+/-- @claim C5 [決定論] 来月、main への直接 push を拒否する設定が入れば、新人の直接 push は拒否され、新人が main に入れられる変更は、
 作業ブランチから出して承認を得たプルリクエストを通ったものだけになる。 -/
 theorem c5_only_pr_route_when_protected :
-    protectedMain .nextMonth →
+    directPushBlocked .nextMonth →
       pushRejected .nextMonth newcomer ∧
         ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c := by
-  intro hprot
-  refine ⟨protection_rejects_push _ _ hprot newcomer_not_admin, ?_⟩
+  intro hblock
+  have hprot : protectedMain .nextMonth := next_month_block_requires_pr hblock
+  refine ⟨protection_rejects_push _ _ hprot newcomer_no_bypass, ?_⟩
   intro o c hb
-  have hv : viaApprovedPR c := protection_only_approved_pr _ _ _ _ hprot newcomer_not_admin hb
+  have hv : viaApprovedPR c := protection_only_approved_pr _ _ _ _ hprot newcomer_no_bypass hb
   exact ⟨hv, pr_needs_work_branch c hv⟩
 
@@ -672,18 +691,23 @@
     (∀ p c, triesDirectPush .thisMonth p c →
       directlyWrites .thisMonth p c ∧ ¬ viaApprovedPR c ∧ releaseCandidate c ∧ (breaksBuild c → stopsTeam c)) ∧
-    ((∀ p, FollowsFlow p) → ∀ m c, entersMain m c →
-      ∃ p pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q) ∧
+    (∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
+      ∃ pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ inPRWhenApproved c pr q) ∧
+    (∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
+      ∃ pr q, squashMerges m p pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q) ∧
     (ruleMinApprovals ≤ flowMinApprovals ∧ flowMergeMethod = ruleMergeMethod ∧ flowMerger = ruleMerger ∧
       ∀ k, ruleAllowsPrefix (flowPrefix k)) ∧
     (noConflict → ∀ o, o ∈ teamFlow → doneByAuthor o = true → canDo o) ∧
-    (protectedMain .nextMonth →
+    (directPushBlocked .nextMonth →
       pushRejected .nextMonth newcomer ∧
         ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c) :=
   ⟨by decide, c1_direct_push_can_stop_team, c1_direct_push_unreviewed_release, c2_only_self_stops_this_month,
-    c3_flow_reviews_every_entry, c4_flow_follows_rules, c4_newcomer_can_do_own_steps, c5_only_pr_route_when_protected⟩
+    c3_own_changes_approved_by_other, c3_own_changes_reviewed_by_other, c4_flow_follows_rules,
+    c4_newcomer_can_do_own_steps, c5_only_pr_route_when_protected⟩
 
 /-! ### 不利な結論（主張にしない。印なし） -/
 
-/-- [不利] 承認のあとに push した変更は、そのプルリクエストを squash merge すると main に入るが、承認した人の承認の時点ではプルリクエストに入っていなかった。 -/
+/-- [不利] 最後の承認のあとに push した変更は、そのプルリクエストを squash merge すると main に入るが、
+承認した人の最後の承認の時点ではプルリクエストに入っていなかった。
+レビューを頼み直しても、古い承認のままマージすれば、足した commit は承認を通らない。 -/
 theorem u1_push_after_approval_unseen :
     ∀ m p pr q c, pushedAfterApproval c pr q → squashMerges m p pr →
@@ -698,21 +722,32 @@
   exact ⟨m, p, c, hb, hv, broken_main_stops_team m c (bringing_enters_main _ _ _ _ hb) hbr⟩
 
-/-- [不利] 承認は本人が行う操作ではなく、流れを守ってマージまで進むには、本人とは別の人の承認が要る。 -/
+/-- [不利] 承認は本人が行う操作ではなく、その月に流れを守ってマージまで進むには、本人とは別の人の承認が要る。 -/
 theorem u3_merge_needs_another_person :
     doneByAuthor .approve = false ∧
-      ∀ m p pr, FollowsFlow p → squashMerges m p pr → ∃ q, approvedBy pr q ∧ q ≠ p := by
+      ∀ m p pr, FollowsFlow m p → squashMerges m p pr → ∃ q, approvedBy pr q ∧ q ≠ p := by
   refine ⟨rfl, ?_⟩
   intro m p pr hflow hsq
   obtain ⟨_, hauth, happ⟩ := hflow
-  obtain ⟨q, hq, _⟩ := happ m pr hsq
+  obtain ⟨q, hq, _⟩ := happ pr hsq
   refine ⟨q, hq, ?_⟩
   intro hqp
-  exact approver_not_author pr q hq (hqp.trans (hauth m pr hsq).symm)
-
-/-- [不利] 保護の設定が管理者に効くようになっていなければ、管理者が直接 push しようとした変更は、main に直接書き込まれる。 -/
-theorem u4_admin_still_unblocked :
-    ∀ m p c, isAdmin p → ¬ protectionCoversAdmins m → triesDirectPush m p c → directlyWrites m p c := by
-  intro m p c hadm hcov ht
-  exact unrejected_push_lands m p c ht (admin_exempt_by_default m p hadm hcov)
+  exact approver_not_author pr q hq (hqp.trans (hauth pr hsq).symm)
+
+/-- [不利] 保護の設定が迂回できる立場の人にも効くようになっていなければ、その人が直接 push しようとした変更は、main に直接書き込まれる。 -/
+theorem u4_bypasser_still_unblocked :
+    ∀ m p c, bypassesProtection p → ¬ bypassDisallowed m → triesDirectPush m p c → directlyWrites m p c := by
+  intro m p c hbyp hdis ht
+  exact unrejected_push_lands m p c ht (bypass_exempt_by_default m p hbyp hdis)
+
+/-- [不利] 流れを守らない人の直接の書き込みで、承認を得たプルリクエストを通らない変更が main に入ったことがある。
+C3 は、自分が流れを守ることで自分の変更を守るだけで、ほかの人のこうした変更は防がない。 -/
+theorem u5_nonfollower_unreviewed_entry :
+    ∃ m p c, directlyWrites m p c ∧ ¬ viaApprovedPR c ∧ ¬ FollowsFlow m p := by
+  obtain ⟨p, c, hw, _⟩ := incident_direct_push_stopped_team
+  refine ⟨.lastMonth, p, c, hw, direct_write_skips_pr _ _ _ hw, ?_⟩
+  intro hflow
+  obtain ⟨hops, _, _⟩ := hflow
+  have hmem : Op.directWriteMain ∈ teamFlow := hops _ (bringing_needs_doing _ _ _ _ hw)
+  exact absurd hmem (by decide)
 
 end
--- rounds/01/Model.lean
+++ Model.lean
@@ -2,5 +2,5 @@
 # 証人: 新人向け Gitブランチ運用ルール
 
-`Argument.lean` のすべての `axiom` を、同じ名前・同じ型の具体的な `def` / `theorem` に差し替えた写し。公理系が無矛盾であることの証拠。
+`Argument.lean` のすべての `axiom` を、同じ名前・同じ型の具体的な `abbrev` / `def` / `theorem` に差し替えた写し。公理系が無矛盾であることの証拠。
 axiom 以外の行は、`Argument.lean` と同じ順で残す。`instance`・`attribute`・`open`・`set_option` は足さない。
 
@@ -9,16 +9,27 @@
 型: `Person`・`Change`・`PR` はどれも `Nat`。
 
-- 人: 0 は新人（`newcomer`）で、流れを守る。1 はレビューする人で、承認だけをする。2 は管理者。3 は流れを守らない人（先月、直接書き込んだ人）。
-- 変更: 0 は先月、人 3 が main に直接書き込み、ビルドを壊した変更。1 はプルリクエスト 0 に入っていて、承認の時点からあった変更。
-  2 はプルリクエスト 1 に、承認のあとに push された変更（ビルドを壊す）。
+- 人: 0 は新人（`newcomer`）で、どの月も流れを守る。1 はレビューする人で、承認だけをする。
+  2 は保護を迂回できる人（`bypassesProtection`）。3 は流れを守らない人。
+- 変更:
+  - 0 は先月、人 3 が main に直接書き込み、ビルドを壊し、チーム全員を止めた変更。
+  - 1 はプルリクエスト 0 に、承認の時点からあった変更。
+  - 2 はプルリクエスト 1 に、承認のあとに push された変更（ビルドを壊す）。
+  - 3 は来月、人 2 が直接 push しようとして、拒否されずに main に直接書き込む変更（ビルドを壊さない）。
+  - 4 は今月、人 3 が直接 push しようとして、拒否されずに main に直接書き込む変更（ビルドを壊さない）。
 - プルリクエスト: 0 は新人が出し、新人が squash merge する。1 は人 3 が出し、人 3 が squash merge する。どちらも人 1 が承認する。
-- 月: 今月までは保護がなく、来月は保護が有効（管理者には効かない）。
-
-関係公理の前提が実際に成り立つ例を持たせてある。
-- 直接の書き込み（変更 0）と、承認を得たプルリクエストの squash merge（変更 1・2）の両方がある。
+  squash merge は月によらない（どの月にもある）。
+- 月: 直接 push を拒否する設定（`directPushBlocked`）と保護（`protectedMain`）は、来月だけ。保護を迂回できる人にも効かせる設定（`bypassDisallowed`）は、どの月にもない。
+
+関係公理と主張の定理の前提が、実際に成り立つ例を持たせてある（`Model.lean` の写しに `example` を足して、Lean で確かめた。本体には足していない）。
+- C2: 今月、人 3 が変更 4 を直接 push しようとする（`triesDirectPush .thisMonth 3 4`）。
+- C3・U3: 人 0 は、どの月も `FollowsFlow m 0` を満たす。今月、人 0 はプルリクエスト 0 を squash merge して、変更 1 を main に入れる。
+  承認した人 1 は人 0 と別の人で、人 1 の最後の承認の時点で変更 1 は入っていた（`reviewedBy 1 1` も成り立つ）。
+- C5: 来月、`directPushBlocked` が成り立つ。来月も人 0 はプルリクエスト 0 を squash merge し、変更 1 は承認を得たプルリクエストを通っている。
+- U1: 変更 2 は、人 1 の最後の承認のあとに push され、人 3 の squash merge で main に入る。人 3 は、どの月も流れを守らない。
+- U4: 人 2 は保護を迂回でき、来月、変更 3 を直接 push しようとし、拒否されない。
+- U5: 先月の人 3 は、変更 0 を直接書き込み、流れを守っていない。
+- 直接の書き込み（変更 0・3・4）と、承認を得たプルリクエストの squash merge（変更 1・2）の両方がある。
 - 承認の時点で入っていた変更（1）と、承認のあとに push された変更（2）の両方がある。
-- 承認した人（1）は、出した人（0・3）と別の人。
-- 管理者（2）がいて、来月の保護で直接 push を拒否される人（管理者以外）と、拒否されない人（管理者）の両方がいる。
-- `FollowsFlow` は人 0・1・2 で成り立ち、人 3 で成り立たない（C3 の前提「全員が流れを守る」は、この世界では成り立たない）。
+- 来月の保護で直接 push を拒否される人（2 以外）と、拒否されない人（2）の両方がいる。
 -/
 
@@ -41,6 +52,7 @@
 `pushBranch` は `git push -u origin <ブランチ名>`、`openPR` はプルリクエストを作ること、`requestReview` はレビューする人の指定、
 `pushFix` は指摘に応える commit を同じブランチへ push すること、`approve` はレビューする人の承認、`squashMerge` は squash merge、
-`otherMerge` は squash 以外の方法でのマージ、`directWriteMain` は main への直接の書き込み（push と、GitHub の画面での直接編集の両方）。
-この語彙で main を変える操作が尽きるという判断は、型には置かず、関係公理 `main_entry_has_op` に置く。 -/
+`otherMerge` は squash 以外の方法でのマージ、`directWriteMain` は main への直接の書き込み
+（プルリクエストのマージによらずに main の中身を変える書き込みすべて。push、GitHub の画面での直接編集、API など、手段を問わない）。
+main を変える手段がこの語彙に尽きるのは、直接の書き込みを「マージ以外のすべて」と定義したことによる（語の定義）。 -/
 inductive Op where
   | updateMain
@@ -97,6 +109,6 @@
 def newcomer : Person := 0
 
-/-- その人がリポジトリの管理者である。 -/
-def isAdmin (p : Person) : Prop := p = 2
+/-- その人は、ブランチ保護の制限を受けない立場にある（リポジトリの管理者の権限か、保護を迂回する権限を持つ役割）。 -/
+def bypassesProtection (p : Person) : Prop := p = 2
 
 /-- その人がリポジトリに push できる権限を持っている。 -/
@@ -107,10 +119,13 @@
 
 /-- その月、その人がその操作をする。 -/
-def doesOp (_m : Month) (p : Person) (o : Op) : Prop :=
-  (p = 0 ∧ o = .squashMerge) ∨ (p = 1 ∧ o = .approve) ∨ p = 3
+def doesOp (m : Month) (p : Person) (o : Op) : Prop :=
+  (m = .lastMonth ∧ p = 3 ∧ o = .directWriteMain) ∨ (m = .thisMonth ∧ p = 3 ∧ o = .directWriteMain) ∨
+    (m = .nextMonth ∧ p = 2 ∧ o = .directWriteMain) ∨ (p = 0 ∧ o = .squashMerge) ∨ (p = 3 ∧ o = .squashMerge) ∨
+    (p = 1 ∧ o = .approve)
 
 /-- その月、その人がその操作で、その変更を GitHub の main に入れる。 -/
 def bringsInVia (m : Month) (p : Person) (o : Op) (c : Change) : Prop :=
-  (m = .lastMonth ∧ p = 3 ∧ o = .directWriteMain ∧ c = 0) ∨ (p = 0 ∧ o = .squashMerge ∧ c = 1) ∨
+  (m = .lastMonth ∧ p = 3 ∧ o = .directWriteMain ∧ c = 0) ∨ (m = .thisMonth ∧ p = 3 ∧ o = .directWriteMain ∧ c = 4) ∨
+    (m = .nextMonth ∧ p = 2 ∧ o = .directWriteMain ∧ c = 3) ∨ (p = 0 ∧ o = .squashMerge ∧ c = 1) ∨
     (p = 3 ∧ o = .squashMerge ∧ c = 2)
 
@@ -122,14 +137,19 @@
 
 /-- その月、その人がその変更を main に直接 push しようとする。 -/
-def triesDirectPush (m : Month) (p : Person) (c : Change) : Prop := m = .lastMonth ∧ p = 3 ∧ c = 0
-
-/-- その月、その人の main への直接 push を GitHub が拒否する。 -/
+def triesDirectPush (m : Month) (p : Person) (c : Change) : Prop :=
+  (m = .lastMonth ∧ p = 3 ∧ c = 0) ∨ (m = .thisMonth ∧ p = 3 ∧ c = 4) ∨ (m = .nextMonth ∧ p = 2 ∧ c = 3)
+
+/-- その月、その人の main への直接 push を GitHub が拒否する。
+設定の水準の述語。手元の main が古いときに GitHub が fast-forward でない push を断るような、1回ごとの拒否は含まない。 -/
 def pushRejected (m : Month) (p : Person) : Prop := m = .nextMonth ∧ p ≠ 2
 
-/-- その月、main にブランチ保護（「Require a pull request before merging」）が有効になっている。 -/
+/-- その月、main への直接 push を拒否する設定が GitHub に入っている（どの設定かは問わない）。 -/
+def directPushBlocked (m : Month) : Prop := m = .nextMonth
+
+/-- その月、main のブランチ保護で「Require a pull request before merging」が、必要な承認数1以上で有効になっている。 -/
 def protectedMain (m : Month) : Prop := m = .nextMonth
 
-/-- その月の保護の設定が、管理者にも効くようになっている。 -/
-def protectionCoversAdmins (_m : Month) : Prop := False
+/-- その月の保護の設定が、迂回できる立場の人にも効くようになっている。 -/
+def bypassDisallowed (_m : Month) : Prop := False
 
 /-- その月、その人がそのプルリクエストを squash merge する。 -/
@@ -139,11 +159,11 @@
 def inPRAtMerge (c : Change) (pr : PR) : Prop := (pr = 0 ∧ c = 1) ∨ (pr = 1 ∧ c = 2)
 
-/-- マージの前に、その人がそのプルリクエストを承認した。 -/
+/-- マージの前に、その人がそのプルリクエストを1回以上承認した。 -/
 def approvedBy (_pr : PR) (q : Person) : Prop := q = 1
 
-/-- その人が承認した時点で、その変更がプルリクエストに入っていた。 -/
+/-- その人の、マージ前の最後の承認の時点で、その変更がプルリクエストに入っていた。 -/
 def inPRWhenApproved (c : Change) (pr : PR) (_q : Person) : Prop := pr = 0 ∧ c = 1
 
-/-- その人の承認のあとに、その変更がプルリクエストのブランチに push された。 -/
+/-- その人の、マージ前の最後の承認のあとに、その変更がプルリクエストのブランチに push された。 -/
 def pushedAfterApproval (c : Change) (pr : PR) (_q : Person) : Prop := pr = 1 ∧ c = 2
 
@@ -166,6 +186,6 @@
 def releaseCandidate (_c : Change) : Prop := True
 
-/-- その操作を行う決まったコマンドか画面の操作があり、その動きを確かめてある。 -/
-def hasCheckedRecipe (o : Op) : Prop := o ≠ .directWriteMain
+/-- その操作を行う、決まった短いコマンドか画面の操作がある。 -/
+def hasFixedRecipe (o : Op) : Prop := o ≠ .directWriteMain
 
 /-- 新人が、その操作を自分で行える。 -/
@@ -217,13 +237,13 @@
   bringsInVia m p .directWriteMain c
 
-/-- 文書の言う「流れを守る」。次の3つを満たすこと。
+/-- 文書の言う「その月に流れを守る」。その月について、次の3つを満たすこと。
 (a) する操作はすべて `teamFlow` に含まれる（main への直接の書き込みも、squash 以外のマージもしない）。
 (b) squash merge するのは、自分が出したプルリクエストだけ。
-(c) squash merge するプルリクエストには、承認した人 `q` がいて、その承認のあとに push された変更がない
-（承認のあとに push したら、承認を受け直してからマージする）。 -/
-def FollowsFlow (p : Person) : Prop :=
-  (∀ m o, doesOp m p o → o ∈ teamFlow) ∧
-  (∀ m pr, squashMerges m p pr → author pr = p) ∧
-  (∀ m pr, squashMerges m p pr → ∃ q, approvedBy pr q ∧ ∀ c, ¬ pushedAfterApproval c pr q)
+(c) squash merge するプルリクエストには、承認した人 `q` がいて、`q` の最後の承認のあとに push された変更がない
+（承認のあとに commit を足したら、もう一度レビューを頼み、承認を受け直してからマージする）。 -/
+def FollowsFlow (m : Month) (p : Person) : Prop :=
+  (∀ o, doesOp m p o → o ∈ teamFlow) ∧
+  (∀ pr, squashMerges m p pr → author pr = p) ∧
+  (∀ pr, squashMerges m p pr → ∃ q, approvedBy pr q ∧ ∀ c, ¬ pushedAfterApproval c pr q)
 
 /-! ## §4 関係公理 -/
@@ -231,9 +251,9 @@
 /-! ### C1・C2: 直接 push の危険 -/
 
-/-- 【実験】先月、main に直接書き込まれ、ビルドを壊した変更がある。
+/-- 【実験】先月、main に直接書き込まれ、チーム全員の作業を止めた変更がある。
 @support F1
-論拠: 先月の1回目の事故（F1）。
+論拠: 先月の1回目の事故で、main に直接 push した変更のために、半日チーム全員の作業が止まった（F1）。1件の事実から存在を言うだけで、一般化を含まない。
 弱い点: 依頼者の証言だけで、社内の事故記録は確かめていない（F1）。 -/
-theorem incident_direct_push_broke_build : ∃ p c, directlyWrites .lastMonth p c ∧ breaksBuild c :=
+theorem incident_direct_push_stopped_team : ∃ p c, directlyWrites .lastMonth p c ∧ stopsTeam c :=
   ⟨3, 0, Or.inl ⟨rfl, rfl, rfl, rfl⟩, Or.inl rfl⟩
 
@@ -241,5 +261,9 @@
 論拠: 「直接の書き込み」とは、プルリクエストを通さずに main を変えること（語の定義）。 -/
 theorem direct_write_skips_pr : ∀ m p c, directlyWrites m p c → ¬ viaApprovedPR c := by
-  rintro m p c (⟨_, _, _, rfl⟩ | ⟨_, h, _⟩ | ⟨_, h, _⟩)
+  rintro m p c (⟨_, _, _, rfl⟩ | ⟨_, _, _, rfl⟩ | ⟨_, _, _, rfl⟩ | ⟨_, h, _⟩ | ⟨_, h, _⟩)
+  · unfold viaApprovedPR
+    decide
+  · unfold viaApprovedPR
+    decide
   · unfold viaApprovedPR
     decide
@@ -280,32 +304,29 @@
 @confidence 0.6
 論拠: 拒否されない push は受け入れられる。先月の直接 push は実際に main に入った（F1・F2）。
-弱い点: 手元の main が古いと、git が push を断る（`git pull` のあとなら通る）。 -/
+弱い点: 手元の main が古いと、GitHub が fast-forward でない push を断る（`git pull` のあとなら通る）。この拒否は、設定の水準の拒否（`pushRejected`）には入らない。 -/
 theorem unrejected_push_lands : ∀ m p c, triesDirectPush m p c → ¬ pushRejected m p → directlyWrites m p c := by
-  rintro m p c ⟨rfl, rfl, rfl⟩ _
-  exact Or.inl ⟨rfl, rfl, rfl, rfl⟩
-
-/-! ### C3: 流れを守れば、main に入る変更はレビューを通る -/
-
-/-- 【仮定】main に入る変更には、それを入れた人と、`Op` の語彙のどれかの操作がある。
-@support なし（GitHub で main の中身を変える方法を並べた事実と、社内の自動の仕組みについての事実が、まだない）
-@confidence 0.7
-論拠: main の中身は、誰かが何かの操作をしたときにしか変わらない。`Op` は直接の書き込み・squash merge・それ以外のマージを含む。
-弱い点: 語彙の外の操作（API での書き込みなど）が `directWriteMain` に入るかは、定義の広さによる。ボットが流れを守らずに main に書き込むなら、C3 の条件「全員が流れを守る」が成り立たない。
-要ファクト: GitHub で main の中身を変える方法が、直接の書き込み（push・画面での直接編集）と、プルリクエストのマージ（squash とそれ以外）に尽きることを GitHub Docs で確かめる。あわせて、社内に main へ書き込む自動の仕組み（ボットなど）があるかをユーザーに確かめる。 -/
-theorem main_entry_has_op : ∀ m c, entersMain m c → ∃ p o, bringsInVia m p o c :=
-  fun _ _ h => h
+  rintro m p c (⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩) _
+  · exact Or.inl ⟨rfl, rfl, rfl, rfl⟩
+  · exact Or.inr (Or.inl ⟨rfl, rfl, rfl, rfl⟩)
+  · exact Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl, rfl⟩))
+
+/-! ### C3: 流れを守れば、自分が main に入れる変更はレビューと承認を通る -/
 
 /-- 【自明】ある操作で変更を main に入れたなら、その人はその操作をしている。
 論拠: 語の定義（「操作で入れた」なら、その操作をしている）。 -/
 theorem bringing_needs_doing : ∀ m p o c, bringsInVia m p o c → doesOp m p o := by
-  rintro m p o c (⟨_, rfl, _, _⟩ | ⟨rfl, rfl, _⟩ | ⟨rfl, rfl, _⟩)
-  · exact Or.inr (Or.inr rfl)
-  · exact Or.inl ⟨rfl, rfl⟩
-  · exact Or.inr (Or.inr rfl)
+  rintro m p o c (⟨rfl, rfl, rfl, _⟩ | ⟨rfl, rfl, rfl, _⟩ | ⟨rfl, rfl, rfl, _⟩ | ⟨rfl, rfl, _⟩ | ⟨rfl, rfl, _⟩)
+  · exact Or.inl ⟨rfl, rfl, rfl⟩
+  · exact Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)
+  · exact Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩))
+  · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨rfl, rfl⟩)))
+  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨rfl, rfl⟩))))
 
 /-- 【自明】変更を main に入れた操作は、main の中身を変える操作である。
 論拠: 語の定義（「操作で main に入れた」なら、その操作は main を変えている）。 -/
 theorem bringing_changes_main : ∀ m p o c, bringsInVia m p o c → changesMain o := by
-  rintro m p o c (⟨_, _, rfl, _⟩ | ⟨_, rfl, _⟩ | ⟨_, rfl, _⟩)
+  rintro m p o c (⟨_, _, rfl, _⟩ | ⟨_, _, rfl, _⟩ | ⟨_, _, rfl, _⟩ | ⟨_, rfl, _⟩ | ⟨_, rfl, _⟩)
+  · exact Or.inl rfl
+  · exact Or.inl rfl
   · exact Or.inl rfl
   · exact Or.inr (Or.inl rfl)
@@ -376,14 +397,16 @@
 論拠: squash merge は、プルリクエストの commit を1つにまとめて取り込み先に加える（F12）。 -/
 theorem squash_content_from_pr : ∀ m p c, bringsInVia m p .squashMerge c → ∃ pr, squashMerges m p pr ∧ inPRAtMerge c pr := by
-  rintro m p c (⟨_, _, h, _⟩ | ⟨rfl, _, rfl⟩ | ⟨rfl, _, rfl⟩)
+  rintro m p c (⟨_, _, h, _⟩ | ⟨_, _, h, _⟩ | ⟨_, _, h, _⟩ | ⟨rfl, _, rfl⟩ | ⟨rfl, _, rfl⟩)
+  · cases h
+  · cases h
   · cases h
   · exact ⟨0, Or.inl ⟨rfl, rfl⟩, Or.inl ⟨rfl, rfl⟩⟩
   · exact ⟨1, Or.inr ⟨rfl, rfl⟩, Or.inr ⟨rfl, rfl⟩⟩
 
-/-- 【経験則】マージの時点でプルリクエストに入っている変更は、そのプルリクエストを承認した人の承認の時点で入っていたか、承認のあとに push されたかのどちらか。
+/-- 【経験則】マージの時点でプルリクエストに入っている変更は、そのプルリクエストを承認した人の最後の承認の時点で入っていたか、最後の承認のあとに push されたかのどちらか。
 @support F6 F8
 @confidence 0.8
 論拠: プルリクエストの中身はブランチの commit で（F6）、ブランチに push した commit は自動で加わる（F8）。
-弱い点: 画面の「Update branch」や、レビューする人の提案を画面で取り込む commit も、承認のあとに中身を変える。これらを push とみなせば成り立つ。 -/
+弱い点: 画面の「Update branch」や、レビューする人の提案を画面で取り込む commit も、最後の承認のあとに中身を変える。これらを push とみなせば成り立つ。 -/
 theorem merge_content_origin : ∀ c pr q, inPRAtMerge c pr → approvedBy pr q → inPRWhenApproved c pr q ∨ pushedAfterApproval c pr q := by
   rintro c pr q (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩) _
@@ -391,9 +414,11 @@
   · exact Or.inr ⟨rfl, rfl⟩
 
-/-- 【経験則】承認の時点でプルリクエストに入っていた変更は、承認した人が見たうえで承認している。
+/-- 【経験則】承認した人の最後の承認の時点でプルリクエストに入っていた変更は、その人が見たうえで承認している。
 @support F6
-@confidence 0.7
+@confidence 0.05
+@reviewer 0.05 ← 0.7 理由: F6 が述べるのは「プルリクエストは、マージの前に変更を話し合い、レビューできる機能」ということだけで、承認した人が中身を見たうえで承認しているか（社内での承認の出し方）は述べていない。この公理が言う人の振る舞いを支える事実がない。
 論拠: プルリクエストは、マージの前に変更を話し合い、レビューする機能（F6）で、承認はその中身に対して出す。
-弱い点: 中身を読まずに承認することはありうる。社内で承認がどう出されているかは確かめていない。 -/
+弱い点: 中身を読まずに承認することはありうる。社内で承認がどう出されているかは確かめていない。F6 は、プルリクエストがレビューのための機能であることを述べるだけで、承認する人の振る舞いは述べていない（F6）。
+要ファクト: 社内で、プルリクエストを承認する人が、差分（変更の中身）を読んでから承認しているかを、ユーザーに確かめる。承認のあとに足された commit を、頼み直したレビューで読んでいるかも含む。 -/
 theorem approval_covers_content : ∀ c pr q, approvedBy pr q → inPRWhenApproved c pr q → reviewedBy c q := by
   rintro c pr q rfl ⟨_, rfl⟩
@@ -402,5 +427,5 @@
 /-- 【仮定】プルリクエストを承認した人は、それを出した本人ではない。
 @support なし（本人が自分のプルリクエストを承認できないことを確かめた事実が、まだない）
-@confidence 0.8
+@confidence 0.05
 論拠: 「ほかの人のレビュー」の「ほかの人」を支える。
 弱い点: 事実がまだない。
@@ -413,5 +438,5 @@
 /-! ### U1: 承認のあとの push（不利な結論のため） -/
 
-/-- 【実験】承認のあとに push された変更も、マージの時点でプルリクエストに入っている。
+/-- 【実験】最後の承認のあとに push された変更も、マージの時点でプルリクエストに入っている。
 @support F8
 論拠: プルリクエストを出したあとに同じブランチへ push した commit は、自動で加わる（F8）。
@@ -426,11 +451,11 @@
 theorem squash_brings_all_pr : ∀ m p pr c, squashMerges m p pr → inPRAtMerge c pr → bringsInVia m p .squashMerge c := by
   rintro m p pr c (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩) (⟨h, rfl⟩ | ⟨h, rfl⟩)
-  · exact Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)
+  · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)))
   · exact absurd h (by decide)
   · exact absurd h (by decide)
-  · exact Or.inr (Or.inr ⟨rfl, rfl, rfl⟩)
-
-/-- 【自明】承認のあとに push された変更は、承認の時点ではプルリクエストに入っていなかった。
-論拠: 承認のあとに加わったものは、承認の時点ではまだない（時の前後の定義）。 -/
+  · exact Or.inr (Or.inr (Or.inr (Or.inr ⟨rfl, rfl, rfl⟩)))
+
+/-- 【自明】ある人の最後の承認のあとに push された変更は、その人の最後の承認の時点ではプルリクエストに入っていなかった。
+論拠: 最後の承認のあとに加わったものは、その承認の時点ではまだない（時の前後の定義）。 -/
 theorem pushed_after_not_seen : ∀ c pr q, pushedAfterApproval c pr q → ¬ inPRWhenApproved c pr q := by
   rintro c pr q ⟨rfl, rfl⟩ ⟨h, _⟩
@@ -441,10 +466,10 @@
 /-- 【仮定】承認を得たプルリクエストの squash merge で main に入り、ビルドを壊す変更がある。
 @support なし（社内で、承認を受けてマージした変更がビルドを壊した記録が、まだない）
-@confidence 0.5
+@confidence 0.05
 論拠: レビューは人が読むもので、見落としがありうる。
 弱い点: 社内の事例がまだない。
 要ファクト: 社内で、承認を受けてマージした変更で main のビルドが壊れたことがあるかを、ユーザーに確かめる。 -/
 theorem approved_change_can_break : ∃ m p c, bringsInVia m p .squashMerge c ∧ viaApprovedPR c ∧ breaksBuild c :=
-  ⟨.thisMonth, 3, 2, Or.inr (Or.inr ⟨rfl, rfl, rfl⟩), Or.inr rfl, Or.inr rfl⟩
+  ⟨.thisMonth, 3, 2, Or.inr (Or.inr (Or.inr (Or.inr ⟨rfl, rfl, rfl⟩))), Or.inr rfl, Or.inr rfl⟩
 
 /-! ### C4: 社内の決まりに沿うこと -/
@@ -486,60 +511,60 @@
 /-! ### C4: 新人が自分で進められること -/
 
-/-- 【実験】手元の main を最新にする操作（`git switch main` と `git pull`）があり、動きを確かめてある。
+/-- 【実験】手元の main を最新にする、決まった操作（`git switch main` と `git pull`）がある。
 @support F15
 論拠: 実行して確かめた（F15）。
 弱い点: GitHub ではなく手元のリモートで確かめた（F15）。 -/
-theorem recipe_update_main : hasCheckedRecipe .updateMain := by
-  unfold hasCheckedRecipe
-  decide
-
-/-- 【実験】ブランチを作って移る操作（`git switch -c`）があり、動きを確かめてある。
+theorem recipe_update_main : hasFixedRecipe .updateMain := by
+  unfold hasFixedRecipe
+  decide
+
+/-- 【実験】ブランチを作って移る、決まった操作（`git switch -c`）がある。
 @support F10
 論拠: 実行して確かめた（F10）。
 弱い点: git 2.23 より古い git にはこのコマンドがない。 -/
-theorem recipe_create_branch : hasCheckedRecipe .createBranch := by
-  unfold hasCheckedRecipe
-  decide
-
-/-- 【実験】作業ブランチを GitHub に送る操作（`git push -u origin <ブランチ名>`）があり、動きを確かめてある。
+theorem recipe_create_branch : hasFixedRecipe .createBranch := by
+  unfold hasFixedRecipe
+  decide
+
+/-- 【実験】作業ブランチを GitHub に送る、決まった操作（`git push -u origin <ブランチ名>`）がある。
 @support F13
 論拠: 実行して確かめた（F13）。
 弱い点: GitHub ではなく手元のリモートで確かめた（F13）。GitHub への認証の手間は含まない。 -/
-theorem recipe_push_branch : hasCheckedRecipe .pushBranch := by
-  unfold hasCheckedRecipe
-  decide
-
-/-- 【実験】push したブランチからプルリクエストを作る画面の操作があり、確かめてある。
+theorem recipe_push_branch : hasFixedRecipe .pushBranch := by
+  unfold hasFixedRecipe
+  decide
+
+/-- 【実験】push したブランチからプルリクエストを作る、決まった画面の操作がある。
 @support F14
 論拠: GitHub Docs（F14）。 -/
-theorem recipe_open_pr : hasCheckedRecipe .openPR := by
-  unfold hasCheckedRecipe
-  decide
-
-/-- 【実験】レビューする人（Reviewers）を指定する画面の操作があり、確かめてある。
+theorem recipe_open_pr : hasFixedRecipe .openPR := by
+  unfold hasFixedRecipe
+  decide
+
+/-- 【実験】レビューする人（Reviewers）を指定する、決まった画面の操作がある。
 @support F14
 論拠: GitHub Docs（F14）。 -/
-theorem recipe_request_review : hasCheckedRecipe .requestReview := by
-  unfold hasCheckedRecipe
-  decide
-
-/-- 【実験】同じブランチに push すればプルリクエストに加わることを確かめてある。
+theorem recipe_request_review : hasFixedRecipe .requestReview := by
+  unfold hasFixedRecipe
+  decide
+
+/-- 【実験】指摘に応える commit を同じブランチに送る、決まった操作（commit と push）がある。
 @support F8
-論拠: GitHub Docs（F8）。操作そのものは commit と push で、新人が知っている。 -/
-theorem recipe_push_fix : hasCheckedRecipe .pushFix := by
-  unfold hasCheckedRecipe
-  decide
-
-/-- 【実験】squash merge する画面の操作（「Squash and merge」）があり、動きを確かめてある。
+論拠: 同じブランチに push すればプルリクエストに加わる（GitHub Docs、F8）。操作そのものは commit と push で、新人が知っている。 -/
+theorem recipe_push_fix : hasFixedRecipe .pushFix := by
+  unfold hasFixedRecipe
+  decide
+
+/-- 【実験】squash merge する、決まった画面の操作（「Squash and merge」）がある。
 @support F12
 論拠: GitHub Docs（F12）。画面のボタンは「Squash and merge」。
 弱い点: ボタンを押せるかはリポジトリの権限による。 -/
-theorem recipe_squash_merge : hasCheckedRecipe .squashMerge := by
-  unfold hasCheckedRecipe
+theorem recipe_squash_merge : hasFixedRecipe .squashMerge := by
+  unfold hasFixedRecipe
   decide
 
 /-- 【仮定】新人は、作業ブランチに自分で commit できる。
 @support なし（読者像に書いてあるだけで、事実として登録されていない）
-@confidence 0.6
+@confidence 0.05
 論拠: 03-reader.json に「Git で commit と push はできる」とある。
 弱い点: 06-facts.json に事実として登録されていないので、`@support` にできない。
@@ -556,11 +581,11 @@
 theorem newcomer_can_write : canWrite newcomer := trivial
 
-/-- 【仮定】決まった操作があり動きを確かめてある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える。
+/-- 【仮定】決まった短い操作がある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える。
 @support なし（新人が文書の手順どおりに進めた記録が、まだない）
-@confidence 0.5
-論拠: 1つずつの操作は、決まったコマンドか画面の操作で済み、文書で説明する。
+@confidence 0.05
+論拠: 1つずつの操作は、決まったコマンドか画面の操作で済む。文書は、流れの各操作を、その決まった操作で説明する。
 弱い点: 新人に実際に通してもらった記録がない。ブランチ・プルリクエスト・マージ・レビューは読者の知らない語（03-reader.json）なので、本文での説明の出来に左右される。
 要ファクト: 新人（または同じくらいの経験の人）に、文書の手順どおりにプルリクエストを1本通してもらい、詰まった操作を記録する。 -/
-theorem recipe_doable : ∀ o, hasCheckedRecipe o → doneByAuthor o = true → canWrite newcomer → noConflict → canDo o := by
+theorem recipe_doable : ∀ o, hasFixedRecipe o → doneByAuthor o = true → canWrite newcomer → noConflict → canDo o := by
   intro o _ h _ _
   unfold canDo
@@ -571,18 +596,24 @@
 /-! ### C5: 保護が入ったあとの経路 -/
 
-/-- 【実験】保護が有効な月は、管理者でない人の直接 push は拒否される。
+/-- 【実験】保護が有効な月は、保護を迂回できない人の直接 push は拒否される。
 @support F4
+@confidence 0.75
+@reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人は、だれでも拒否される」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
 論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
-弱い点: 初期設定では管理者に効かない（F4）。 -/
-theorem protection_rejects_push : ∀ m p, protectedMain m → ¬ isAdmin p → pushRejected m p :=
-  fun _ _ hm ha => ⟨hm, ha⟩
-
-/-- 【実験】保護が有効な月に、管理者でない人が main に入れる変更は、承認を得たプルリクエストを通ったものだけ。
+弱い点: 初期設定では、管理者などには効かない（F4）。その人たちは、迂回できる立場として前提で除いてある。 -/
+theorem protection_rejects_push : ∀ m p, protectedMain m → ¬ bypassesProtection p → pushRejected m p :=
+  fun _ _ hm hb => ⟨hm, hb⟩
+
+/-- 【実験】保護が有効な月に、保護を迂回できない人が main に入れる変更は、承認を得たプルリクエストを通ったものだけ。
 @support F4
+@confidence 0.75
+@reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人が入れる変更は、どれも承認を得たプルリクエストを通る」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
 論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
-弱い点: 初期設定では管理者に効かない（F4）。 -/
-theorem protection_only_approved_pr : ∀ m p o c, protectedMain m → ¬ isAdmin p → bringsInVia m p o c → viaApprovedPR c := by
-  rintro m p o c hm _ (⟨rfl, _, _, _⟩ | ⟨_, _, rfl⟩ | ⟨_, _, rfl⟩)
+弱い点: 初期設定では、管理者などには効かない（F4）。その人たちは、迂回できる立場として前提で除いてある。 -/
+theorem protection_only_approved_pr : ∀ m p o c, protectedMain m → ¬ bypassesProtection p → bringsInVia m p o c → viaApprovedPR c := by
+  rintro m p o c hm hb (⟨rfl, _, _, _⟩ | ⟨rfl, _, _, _⟩ | ⟨_, rfl, _, _⟩ | ⟨_, _, rfl⟩ | ⟨_, _, rfl⟩)
   · cases hm
+  · cases hm
+  · exact absurd rfl hb
   · exact Or.inl rfl
   · exact Or.inr rfl
@@ -594,20 +625,30 @@
   fun _ h => h
 
-/-- 【仮定】新人はリポジトリの管理者ではない。
-@support なし（新人の権限を確かめた事実が、まだない）
-@confidence 0.8
-論拠: 新人に管理者の権限を渡すことはふつうない。
+/-- 【仮定】新人は、保護を迂回できる立場にない（管理者の権限も、迂回の権限も持たない）。
+@support なし（新人のリポジトリでの役割を確かめた事実が、まだない）
+@confidence 0.05
+論拠: 新人に、管理者の権限や、保護を迂回する権限を渡すことは、ふつうない。
 弱い点: 事実がまだない。
-要ファクト: 新人のリポジトリでの権限が管理者でないことを、ユーザーに確かめる。 -/
-theorem newcomer_not_admin : ¬ isAdmin newcomer := by
-  unfold isAdmin newcomer
-  decide
-
-/-! ### U4: 管理者は来月も止まらない（不利な結論のため） -/
-
-/-- 【実験】保護の設定が管理者に効くようになっていなければ、管理者の直接 push は拒否されない。
+要ファクト: 新人のリポジトリでの役割（権限）が、管理者でも、保護を迂回できる役割でもないことを、ユーザーに確かめる。 -/
+theorem newcomer_no_bypass : ¬ bypassesProtection newcomer := by
+  unfold bypassesProtection newcomer
+  decide
+
+/-- 【仮定】来月、直接 push を拒否する設定が入るなら、それは承認1名以上のプルリクエストを必須にする保護である。
+@support なし（F3 は「直接 push を拒否する設定に来月変える予定」と述べるだけで、どの設定を入れるか、必要な承認数をいくつにするかは述べていない。F7 は社内の決まりで、GitHub の設定ではない）
+@confidence 0.05
+論拠: main への直接 push を止める設定としてふつう使うのは、マージの前にプルリクエストを必須にする保護で、社内の決まり（承認1名以上）とも合う。
+弱い点: 承認を求めずに直接 push だけを止める設定（承認数 0 や、push できる人を限る設定など）もありうる。その場合、C5 の結論は「承認を得たプルリクエストだけ」ではなく「プルリクエストを通ったものだけ」に弱まる。
+要ファクト: 来月 main に入れる設定が「Require a pull request before merging」か、必要な承認数を1以上にするかを、ユーザーに確かめる。 -/
+theorem next_month_block_requires_pr : directPushBlocked .nextMonth → protectedMain .nextMonth :=
+  fun h => h
+
+/-! ### U4: 保護を迂回できる人は来月も止まらない（不利な結論のため） -/
+
+/-- 【実験】保護の設定が迂回できる立場の人にも効くようになっていなければ、その人の直接 push は拒否されない。
 @support F4
-論拠: 初期設定では、保護の制限は管理者に効かない（F4）。 -/
-theorem admin_exempt_by_default : ∀ m p, isAdmin p → ¬ protectionCoversAdmins m → ¬ pushRejected m p := by
+論拠: 初期設定では、保護の制限は、リポジトリの管理者の権限を持つ人に効かない（F4）。迂回の権限を持つ役割は、その権限の意味から、制限を受けない。
+弱い点: F4 の引用が直接述べるのは、管理者の権限を持つ人だけである。迂回の権限を持つ役割は、F4 の「管理者など」に含めて読んでいる（F4）。 -/
+theorem bypass_exempt_by_default : ∀ m p, bypassesProtection p → ¬ bypassDisallowed m → ¬ pushRejected m p := by
   rintro m p hp _ ⟨_, hne⟩
   exact hne hp
@@ -619,6 +660,6 @@
 /-- @claim C1 [決定論] main への直接の書き込みで、チーム全員の作業が止まることがある（先月、実際に起きた）。 -/
 theorem c1_direct_push_can_stop_team : ∃ m p c, directlyWrites m p c ∧ stopsTeam c := by
-  obtain ⟨p, c, hw, hb⟩ := incident_direct_push_broke_build
-  exact ⟨.lastMonth, p, c, hw, broken_main_stops_team .lastMonth c (bringing_enters_main _ _ _ _ hw) hb⟩
+  obtain ⟨p, c, hw, hs⟩ := incident_direct_push_stopped_team
+  exact ⟨.lastMonth, p, c, hw, hs⟩
 
 /-- @claim C1 [決定論] main に直接書き込んだ変更は、承認を得たプルリクエストを通らないまま、本番に出る候補になる。 -/
@@ -658,24 +699,32 @@
   · rfl
 
-/-- @claim C3 [決定論] 全員が流れを守るかぎり、main に入る変更はすべて、squash merge したプルリクエストに入っていて、
-そのプルリクエストを、マージした本人とは別の人が承認し、その人がその変更を見たうえで承認している。 -/
-theorem c3_flow_reviews_every_entry :
-    (∀ p, FollowsFlow p) → ∀ m c, entersMain m c →
-      ∃ p pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q := by
-  intro hflow m c hc
-  obtain ⟨p, o, hb⟩ := main_entry_has_op m c hc
-  obtain ⟨hops, hauth, happ⟩ := hflow p
-  have hmem : o ∈ teamFlow := hops m o (bringing_needs_doing m p o c hb)
+/-- @claim C3 [決定論] その月に流れを守る人が、その月に main に入れる変更は、どれも、その人が squash merge したプルリクエストに入っていて、
+その人とは別の人が承認していて、その別の人の最後の承認の時点で、その変更はプルリクエストに入っていた（C3 の「ほかの人の承認を通る」）。 -/
+theorem c3_own_changes_approved_by_other :
+    ∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
+      ∃ pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ inPRWhenApproved c pr q := by
+  intro m p hflow o c hb
+  obtain ⟨hops, hauth, happ⟩ := hflow
+  have hmem : o ∈ teamFlow := hops o (bringing_needs_doing m p o c hb)
   have ho : o = .squashMerge := flow_changes_main_only_by_merge o hmem (bringing_changes_main m p o c hb)
   subst ho
   obtain ⟨pr, hsq, hin⟩ := squash_content_from_pr m p c hb
-  obtain ⟨q, hq, hfresh⟩ := happ m pr hsq
+  obtain ⟨q, hq, hfresh⟩ := happ pr hsq
   have hseen : inPRWhenApproved c pr q := by
     rcases merge_content_origin c pr q hin hq with h | h
     · exact h
     · exact absurd h (hfresh c)
-  refine ⟨p, pr, q, hsq, hin, hq, ?_, approval_covers_content c pr q hq hseen⟩
+  refine ⟨pr, q, hsq, hin, hq, ?_, hseen⟩
   intro hqp
-  exact approver_not_author pr q hq (hqp.trans (hauth m pr hsq).symm)
+  exact approver_not_author pr q hq (hqp.trans (hauth pr hsq).symm)
+
+/-- @claim C3 [決定論] その月に流れを守る人が、その月に main に入れる変更は、どれも、その人が squash merge したプルリクエストを
+その人とは別の人が承認していて、その別の人がその変更を見たうえで承認している（C3 の「ほかの人のレビューを通る」）。 -/
+theorem c3_own_changes_reviewed_by_other :
+    ∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
+      ∃ pr q, squashMerges m p pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q := by
+  intro m p hflow o c hb
+  obtain ⟨pr, q, hsq, _, hq, hne, hseen⟩ := c3_own_changes_approved_by_other m p hflow o c hb
+  exact ⟨pr, q, hsq, hq, hne, approval_covers_content c pr q hq hseen⟩
 
 /-! ### C4 -/
@@ -715,14 +764,15 @@
 /-! ### C5 -/
 
-/-- @claim C5 [決定論] 来月、保護が有効になれば、新人の直接 push は拒否され、新人が main に入れられる変更は、
+/-- @claim C5 [決定論] 来月、main への直接 push を拒否する設定が入れば、新人の直接 push は拒否され、新人が main に入れられる変更は、
 作業ブランチから出して承認を得たプルリクエストを通ったものだけになる。 -/
 theorem c5_only_pr_route_when_protected :
-    protectedMain .nextMonth →
+    directPushBlocked .nextMonth →
       pushRejected .nextMonth newcomer ∧
         ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c := by
-  intro hprot
-  refine ⟨protection_rejects_push _ _ hprot newcomer_not_admin, ?_⟩
+  intro hblock
+  have hprot : protectedMain .nextMonth := next_month_block_requires_pr hblock
+  refine ⟨protection_rejects_push _ _ hprot newcomer_no_bypass, ?_⟩
   intro o c hb
-  have hv : viaApprovedPR c := protection_only_approved_pr _ _ _ _ hprot newcomer_not_admin hb
+  have hv : viaApprovedPR c := protection_only_approved_pr _ _ _ _ hprot newcomer_no_bypass hb
   exact ⟨hv, pr_needs_work_branch c hv⟩
 
@@ -736,18 +786,23 @@
     (∀ p c, triesDirectPush .thisMonth p c →
       directlyWrites .thisMonth p c ∧ ¬ viaApprovedPR c ∧ releaseCandidate c ∧ (breaksBuild c → stopsTeam c)) ∧
-    ((∀ p, FollowsFlow p) → ∀ m c, entersMain m c →
-      ∃ p pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q) ∧
+    (∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
+      ∃ pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ inPRWhenApproved c pr q) ∧
+    (∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
+      ∃ pr q, squashMerges m p pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q) ∧
     (ruleMinApprovals ≤ flowMinApprovals ∧ flowMergeMethod = ruleMergeMethod ∧ flowMerger = ruleMerger ∧
       ∀ k, ruleAllowsPrefix (flowPrefix k)) ∧
     (noConflict → ∀ o, o ∈ teamFlow → doneByAuthor o = true → canDo o) ∧
-    (protectedMain .nextMonth →
+    (directPushBlocked .nextMonth →
       pushRejected .nextMonth newcomer ∧
         ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c) :=
   ⟨by decide, c1_direct_push_can_stop_team, c1_direct_push_unreviewed_release, c2_only_self_stops_this_month,
-    c3_flow_reviews_every_entry, c4_flow_follows_rules, c4_newcomer_can_do_own_steps, c5_only_pr_route_when_protected⟩
+    c3_own_changes_approved_by_other, c3_own_changes_reviewed_by_other, c4_flow_follows_rules,
+    c4_newcomer_can_do_own_steps, c5_only_pr_route_when_protected⟩
 
 /-! ### 不利な結論（主張にしない。印なし） -/
 
-/-- [不利] 承認のあとに push した変更は、そのプルリクエストを squash merge すると main に入るが、承認した人の承認の時点ではプルリクエストに入っていなかった。 -/
+/-- [不利] 最後の承認のあとに push した変更は、そのプルリクエストを squash merge すると main に入るが、
+承認した人の最後の承認の時点ではプルリクエストに入っていなかった。
+レビューを頼み直しても、古い承認のままマージすれば、足した commit は承認を通らない。 -/
 theorem u1_push_after_approval_unseen :
     ∀ m p pr q c, pushedAfterApproval c pr q → squashMerges m p pr →
@@ -762,21 +817,32 @@
   exact ⟨m, p, c, hb, hv, broken_main_stops_team m c (bringing_enters_main _ _ _ _ hb) hbr⟩
 
-/-- [不利] 承認は本人が行う操作ではなく、流れを守ってマージまで進むには、本人とは別の人の承認が要る。 -/
+/-- [不利] 承認は本人が行う操作ではなく、その月に流れを守ってマージまで進むには、本人とは別の人の承認が要る。 -/
 theorem u3_merge_needs_another_person :
     doneByAuthor .approve = false ∧
-      ∀ m p pr, FollowsFlow p → squashMerges m p pr → ∃ q, approvedBy pr q ∧ q ≠ p := by
+      ∀ m p pr, FollowsFlow m p → squashMerges m p pr → ∃ q, approvedBy pr q ∧ q ≠ p := by
   refine ⟨rfl, ?_⟩
   intro m p pr hflow hsq
   obtain ⟨_, hauth, happ⟩ := hflow
-  obtain ⟨q, hq, _⟩ := happ m pr hsq
+  obtain ⟨q, hq, _⟩ := happ pr hsq
   refine ⟨q, hq, ?_⟩
   intro hqp
-  exact approver_not_author pr q hq (hqp.trans (hauth m pr hsq).symm)
-
-/-- [不利] 保護の設定が管理者に効くようになっていなければ、管理者が直接 push しようとした変更は、main に直接書き込まれる。 -/
-theorem u4_admin_still_unblocked :
-    ∀ m p c, isAdmin p → ¬ protectionCoversAdmins m → triesDirectPush m p c → directlyWrites m p c := by
-  intro m p c hadm hcov ht
-  exact unrejected_push_lands m p c ht (admin_exempt_by_default m p hadm hcov)
+  exact approver_not_author pr q hq (hqp.trans (hauth pr hsq).symm)
+
+/-- [不利] 保護の設定が迂回できる立場の人にも効くようになっていなければ、その人が直接 push しようとした変更は、main に直接書き込まれる。 -/
+theorem u4_bypasser_still_unblocked :
+    ∀ m p c, bypassesProtection p → ¬ bypassDisallowed m → triesDirectPush m p c → directlyWrites m p c := by
+  intro m p c hbyp hdis ht
+  exact unrejected_push_lands m p c ht (bypass_exempt_by_default m p hbyp hdis)
+
+/-- [不利] 流れを守らない人の直接の書き込みで、承認を得たプルリクエストを通らない変更が main に入ったことがある。
+C3 は、自分が流れを守ることで自分の変更を守るだけで、ほかの人のこうした変更は防がない。 -/
+theorem u5_nonfollower_unreviewed_entry :
+    ∃ m p c, directlyWrites m p c ∧ ¬ viaApprovedPR c ∧ ¬ FollowsFlow m p := by
+  obtain ⟨p, c, hw, _⟩ := incident_direct_push_stopped_team
+  refine ⟨.lastMonth, p, c, hw, direct_write_skips_pr _ _ _ hw, ?_⟩
+  intro hflow
+  obtain ⟨hops, _, _⟩ := hflow
+  have hmem : Op.directWriteMain ∈ teamFlow := hops _ (bringing_needs_doing _ _ _ _ hw)
+  exact absurd hmem (by decide)
 
 end
```
