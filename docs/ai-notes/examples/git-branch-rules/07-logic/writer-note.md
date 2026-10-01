# Writer の作業の報告（2周目）

## 書いたもの

差分の設計書（`model-plan-delta.md`）の表の行を、1行ずつ `Argument.lean` に写した。表にない部分は1周目のまま。

- `07-logic/Argument.lean`
  - 宣言（D1〜D10）: `isAdmin` を `bypassesProtection` に、`protectionCoversAdmins` を `bypassDisallowed` に、`hasCheckedRecipe` を `hasFixedRecipe` に替えた。`directPushBlocked` を足した。
    `FollowsFlow` を `Month → Person → Prop` にし、(a)(b)(c) の中の `∀ m` を外した。(c) の説明を「承認を受け直してからマージする」に書き直した。
    `approvedBy`・`inPRWhenApproved`・`pushedAfterApproval`・`protectedMain`・`pushRejected`・`Op` の説明を、D3・D4・D8・D9 のとおりに直した。
    `Op` の説明の最後の文は、消した `main_entry_has_op` を指していたので、D4 の文（語の定義による）に置き換えた。
  - 関係公理（A1〜A11）: 消したものは `incident_direct_push_broke_build`・`main_entry_has_op`・`newcomer_not_admin`・`admin_exempt_by_default`。
    足したものは `incident_direct_push_stopped_team`（【実験】F1）・`newcomer_no_bypass`（【仮定】）・`bypass_exempt_by_default`（【実験】F4）・`next_month_block_requires_pr`（【仮定】）。
    `merge_content_origin`・`pushed_after_not_seen`・`push_joins_pr`・`approval_covers_content` の文を「最後の承認」に直した（型は同じ）。
    `approval_covers_content` に、弱い点の1文と要ファクトを足した（種類・@support・@confidence 0.05・@reviewer の行はそのまま）。
    `protection_rejects_push`・`protection_only_approved_pr` の型の `¬ isAdmin p` を `¬ bypassesProtection p` に替え、1行目と弱い点を直した（@confidence 0.75 と @reviewer の行はそのまま）。
    `unrejected_push_lands` の弱い点を A9 の文にした。`recipe_*` の8つの型の述語を `hasFixedRecipe` に替え、文から「確かめてある」を外した。`recipe_doable` の文と論拠を A11 のとおりにした。
  - 定理（T1〜T10）: `c3_flow_reviews_every_entry` と `u4_admin_still_unblocked` を消した。
    `c3_own_changes_approved_by_other`（@claim C3）・`c3_own_changes_reviewed_by_other`（@claim C3）・`u4_bypasser_still_unblocked`（[不利]）・`u5_nonfollower_unreviewed_entry`（[不利]）を足した。
    `c1_direct_push_can_stop_team` は `incident_direct_push_stopped_team` だけで示した。`c5_only_pr_route_when_protected` の前提を `directPushBlocked .nextMonth` に替え、`next_month_block_requires_pr` を通して示した。
    `c0_team_flow` の結論を9項（C3 を2項、C5 を新しい型）にした。`u3_merge_needs_another_person` を月つきの `FollowsFlow` にした。`u1_push_after_approval_unseen` の説明を T7 のとおりにした。
  - 冒頭の「主張と定理の対応」を、新しい C3 の文と、この周の定理の名前に直した。「設計書との違い」を、この周でも残る違いだけにした。
  - 数: 公理 80（宣言 34・関係公理 46。【自明】8・【実験】23・【経験則】9・【仮定】6）。`@claim` の定理 9（C0 1・C1 2・C2 1・C3 2・C4 2・C5 1）、印なしの補題 1、[不利] 5。
- `07-logic/Model.lean`（証人）: `Argument.lean` から、axiom の行だけを差し替える台本で作った（80個）。axiom 以外の行と docstring は `Argument.lean` のまま。冒頭の説明だけ書き直した。

## 設計書との違いと理由

`Argument.lean` の冒頭の「設計書（model-plan.md）との違い」と同じ内容。1〜3は1周目から残るもの、4・5はこの周で足したもの（5は下の「証人」）。

1. **`bringing_enters_main`（【自明】）を足している。** `main_feeds_release`・`broken_main_stops_team` は `entersMain` についての公理で、それを使う定理（C1 の2つ目・C2・U2）は `bringsInVia` から始まる。
   設計書には `bringsInVia` から `entersMain` への向きの公理がない。C1 の1つ目は、この周から `incident_direct_push_stopped_team` だけを使うので、この公理を使わない。
2. **`merge_content_origin` に前提 `approvedBy pr q` を足している。** 「最後の承認の時点」は承認した人がいて初めて決まるため。
3. **帰納型に `deriving DecidableEq` を付けている。**
4. **支える事実のない【仮定】4つの `@confidence` を 0.05 にした。** `approver_not_author`（設計書の案 0.8）、`approved_change_can_break`（0.5）、`newcomer_can_commit`（0.6）、`recipe_doable`（0.5）。
   Writer の決まり（支える事実のない【経験則】【仮定】の案は 0.05 と書く）に合わせた。どれも `@reviewer` の行はない。CLI の値はもとから 0.05 なので、確信度は変わらない。
   差分の設計書の表にない変更なので、`logic-round diff` では対応する行のない変更として出る。

1周目の「違い」のうち、`u3_merge_needs_another_person` の結論の形は、差分の設計書5節の型になったので外した。
証人の世界の違い（1周目の5）は、差分の設計書8節に従ったので外し、8節に足したことだけを5に書いた。

## 証人

差分の設計書8節のとおりにした。8節にないことで足したのは次の2つ。

- **今月の直接 push の例（変更 4）を足した。** 1周目の証人では `triesDirectPush` が先月にしかなく、C2 の定理の前提 `triesDirectPush .thisMonth p c` が一度も成り立たなかった（C2 が証人の中で空回りしていた）。
  今月、人 3 が変更 4 を直接 push しようとし、拒否されずに main に直接書き込むようにした。変更 4 はビルドを壊さない。
- **`doesOp` を、`bringsInVia` の各場合と、人 1 の承認に合わせて書いた。** 1周目は「人 3 はどの操作もする」だったが、人 2 の来月の直接の書き込みと、人 3 の今月の直接の書き込みを足すので、場合ごとに並べた。

squash merge（`squashMerges` と `bringsInVia` の squash の場合）は、1周目と同じく月によらない。これで、来月も人 0 がプルリクエスト 0 を squash merge し、`protection_only_approved_pr` と C5 の結論に、来月の実例がある
（来月の人 2 の直接の書き込みは、`¬ bypassesProtection` の前提で除かれるため、それだけでは実例にならない）。

次のことを、`Model.lean` の写しに `example` を足して Lean で確かめた（本体には足していない）。

- どの月も `FollowsFlow m 0` が成り立つ。どの月も `FollowsFlow m 3` は成り立たない。
- C3: 今月、人 0 は変更 1 を squash merge で入れ、プルリクエスト 0・承認した人 1 で、結論のすべての項（`inPRWhenApproved 1 0 1`・`reviewedBy 1 1` を含む）が成り立つ。
- C2: `triesDirectPush .thisMonth 3 4`。C4: `noConflict`。C5: `directPushBlocked .nextMonth` と、来月の人 0 の squash merge（変更 1、`viaApprovedPR 1`）。
- U1: `pushedAfterApproval 2 1 1` と `squashMerges .thisMonth 3 1`。U4: `bypassesProtection 2`・`¬ bypassDisallowed .nextMonth`・`triesDirectPush .nextMonth 2 3`。
- 関係公理の前提: 来月に拒否される人（0）と拒否されない人（2）、今月に拒否されない push、最後の承認のあとに push された変更（2）と、承認の時点で入っていた変更（1）、ビルドを壊す変更（0・2）と壊さない変更（3・4）。

## 門の結果

`python3 .claude/skills/cyrus/scripts/cyrus.py --doc git-branch-rules lean`: エラー 0 件・警告 0 件・参考 0 件。
証人: axiom 80 個すべての型が一致、写しの欠け 0 行、Lean 標準の公理以外への依存なし。

| 主張 | 確信度 | 値を決める公理 |
|---|---|---|
| C0 | 0.05 | `approval_covers_content`・`approver_not_author`・`newcomer_can_commit`・`recipe_doable`・`newcomer_no_bypass`・`next_month_block_requires_pr` |
| C1 | 0.6 | `incident_direct_push_stopped_team`・`main_feeds_release` |
| C2 | 0.6 | `no_rejection_this_month`・`unrejected_push_lands`・`broken_main_stops_team`・`main_feeds_release` |
| C3 | 0.05 | `approver_not_author`（承認の項）、それに `approval_covers_content`（レビューの項） |
| C4 | 0.05 | `newcomer_can_commit`・`recipe_doable` |
| C5 | 0.05 | `newcomer_no_bypass`・`next_month_block_requires_pr` |

差分の設計書11節の見通しと同じ。
印なしの定理の値: 補題 0.8、U1 0.95、U2 0.05、U3 0.05、U4 0.6、U5 0.6。
手戻りの一覧は7個（`approval_covers_content`・`approver_not_author`・`approved_change_can_break`・`newcomer_can_commit`・`recipe_doable`・`newcomer_no_bypass`・`next_month_block_requires_pr`）。
主張の定理が使わない公理は5つ（`push_joins_pr`・`squash_brings_all_pr`・`pushed_after_not_seen`・`approved_change_can_break`・`bypass_exempt_by_default`）。どれも [不利] の定理だけが使う。

## 検査やガイドが誤っていると思う点、気づいた点

1. **名前を変えずに型を変えた公理がある（差分の設計書とガイドの食い違い）。** ガイド（`stages/07-logic.md` の「2周目から」）は、公理の命題（型）を変えるときは名前も変えると書く。
   差分の設計書 A5 は、`protection_rejects_push`・`protection_only_approved_pr` の型を `¬ isAdmin p` から `¬ bypassesProtection p` に替え、名前と `@reviewer` の行（0.75 ← 0.95）を残すよう指示している。
   Writer は `@reviewer` の行を消せないので、設計書に従った。その結果、Reviewer が下げた理由（「管理者など」の「など」）はこの周の型で答えられているのに、値は 0.75 より上に戻れない（Reviewer は下げるだけ）。
   値を見直す道を残すなら、次の周で Planner が名前を変える判断をする必要がある。いまは C5 が 0.05 の【仮定】2つで決まるので、主張の値には効かない。
   `recipe_*` の8つと `recipe_doable` も、述語の名前が変わって型が変わったが、名前はそのまま（A10・A11 の指示）。これらには `@reviewer` の行がないので、値への影響はない。
2. **`c1_direct_push_can_stop_team` は、公理 `incident_direct_push_stopped_team` に月を入れただけの証明になった。** 差分の設計書 T1 のとおり。手がかりで言い換えの候補に出ると思う。
3. **門では見つからない空回りを1つ直した。** 1周目の証人で C2 の前提が一度も成り立たなかった（上の「証人」）。証人で主張の定理の前提が成り立つかは、門が見ていない。今回は写しに `example` を足して確かめたが、この確かめは成果物に残らない。
