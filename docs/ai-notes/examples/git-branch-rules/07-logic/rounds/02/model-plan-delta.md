# 差分の設計書（2周目）: 新人向け Gitブランチ運用ルール

Logical Model Planner が書く。
1周目の `review.md`（差し戻し 高 2・中 6・低 6）と、ステージ5で変わった C3 の文に答える。
この文書に書いていない部分は、`model-plan.md`（1周目）のとおりにする。`model-plan.md` は書き換えない。

変更は、1〜4節の表に1行に1つずつ書く。表の行に `` ` `` で挙げた名前は、`Argument.lean` で実際に変わる宣言だけにしてある。
新しい公理の中身、定理の型の見当、証人、採らない指摘などは、表の外（行頭に `-` や `|` を置かない文）に書く。

## 0. この周の前提

C3 の文は、ステージ5でユーザーが次のように決めた（05-claims.json）。

「この流れ（承認のあとに commit を足したら、もう一度レビューを頼むことを含む）を自分が守るかぎり、自分が main に入れる変更はすべて、マージ前にほかの人のレビューと承認を通る。」

読みは、1周目の M1 の (ii) にあたる。主語は「自分」で、範囲は「自分が main に入れる変更」。流れには再レビューが入る。
1周目の読み (i)（全員が守れば、main に入る変更はすべて）は、主張ではなくなった。

主張の形は変わらない。C3 は能力の文（全称）で、決定論で組む。ほかの主張の文も変わっていない。
比較の文はないので、失敗の台帳（ledger.json）は作らない。「同じとみなす」置き方の節と比べる相手は、1周目と同じく「比較なし」。

### 流れの (c) を「承認を受け直してからマージする」と読む理由

C3 の括弧書きは「もう一度レビューを頼む」と言う。
これを「頼むだけで、古い承認のままマージしてよい」と読むと、C3 は偽になる。
U1（`u1_push_after_approval_unseen`、確信度 0.95）により、承認のあとに足した commit は、承認の時点ではプルリクエストに入っていないまま main に入るからである。
C3 の「自分が main に入れる変更はすべて…承認を通る」が成り立つ読みは、「頼み直したレビューで承認を受け直してから、マージする」だけである。
この読みは、C0 の「1名以上の承認を受けてから、自分で squash merge」とも合う。マージの直前の承認が、足した commit も覆うからである。
そこで `FollowsFlow` の (c) を、この読みで定義する（1節の D2）。本文でも「承認を受け直してからマージする」と書く（7節）。

## 1. 宣言と def の変更

| # | 指摘 | 変更 |
|---|---|---|
| D1 | H1 | `FollowsFlow` に月を1つ目の引数として足し、「その月に流れを守る」にする（型は Month → Person → Prop）。(a)(b)(c) の中の「∀ m」を外し、その月のことだけを言う。先月の事故は「先月、その人は守っていなかった」とだけ両立し、今月や来月に守る人の前提を否定しない |
| D2 | H2・L1 | `FollowsFlow` の (c) の説明を、C3 の括弧書きに合わせて書き直す。「squash merge するプルリクエストには、承認した人 q がいて、q の最後の承認のあとに push された変更がない（承認のあとに commit を足したら、もう一度レビューを頼み、承認を受け直してからマージする）」。式の形は変えない |
| D3 | L1 | `approvedBy`・`inPRWhenApproved`・`pushedAfterApproval` の意味を、「その人の、マージ前の最後の承認」を基準にする。1つ目は「マージの前に、その人がそのプルリクエストを1回以上承認した」、2つ目は「その人の最後の承認の時点で、その変更がプルリクエストに入っていた」、3つ目は「その人の最後の承認のあとに、その変更がプルリクエストのブランチに push された」。型は変えない。これで、同じ人に承認を受け直せば、前の承認のあとの push は3つ目に当たらなくなり、(c) が型で表せる |
| D4 | H1・M1 | `Op` の説明で、直接の書き込み（directWriteMain）を「プルリクエストのマージによらずに main の中身を変える書き込みすべて（push、GitHub の画面での直接編集、API など、手段を問わない）」と定義し直す。「この語彙で main を変える操作が尽きるという判断は関係公理に置く」の文を、「main を変える手段がこの語彙に尽きるのは、直接の書き込みを『マージ以外のすべて』と定義したことによる（語の定義）」に置き換える。コンストラクタは変えない |
| D5 | M3 | `isAdmin` を消し、`bypassesProtection`（Person → Prop）を足す。意味は「その人は、ブランチ保護の制限を受けない立場にある（リポジトリの管理者の権限か、保護を迂回する権限を持つ役割）」。F4 の「管理者など」の「など」を入れるため |
| D6 | M3 | `protectionCoversAdmins` を消し、`bypassDisallowed`（Month → Prop）を足す。意味は「その月の保護の設定が、迂回できる立場の人にも効くようになっている」 |
| D7 | M4 | `directPushBlocked`（Month → Prop）を足す。意味は「その月、main への直接 push を拒否する設定が GitHub に入っている（どの設定かは問わない）」。C5 の条件「仕組みで直接 push が拒否されるようになる」をそのまま写したもの |
| D8 | M4 | `protectedMain` の意味を「その月、main のブランチ保護で『Require a pull request before merging』が、必要な承認数1以上で有効になっている」にする。承認数 0 の設定は含めない（含めると、保護が入れば承認を得たものだけ、という公理が F4 の引用より強くなる） |
| D9 | L4 | `pushRejected` の説明に「設定の水準の述語。手元の main が古いときに GitHub が fast-forward でない push を断るような、1回ごとの拒否は含まない」を足す |
| D10 | L2 | `hasCheckedRecipe` を消し、`hasFixedRecipe`（Op → Prop）を足す。意味は「その操作を行う、決まった短いコマンドか画面の操作がある」。「動きを確かめてある」は証拠の側のことなので宣言から外し、各公理の @support と論拠に任せる |

## 2. 関係公理の変更

| # | 指摘 | 変更 |
|---|---|---|
| A1 | M6 | `incident_direct_push_broke_build` を消し、`incident_direct_push_stopped_team`（【実験】F1）を足す。命題は「先月、main に直接書き込まれ、チーム全員の作業を止めた変更がある」。中身は3節 |
| A2 | H1・M1 | `main_entry_has_op` を消す。読み (i)（main に入る変更すべて）のためだけの公理で、読み (ii) の定理は使わない。誤りと分かったのではなく、主張の読みが変わって要らなくなったので、棄却ではない（rejected.json には入れない） |
| A3 | L1 | `merge_content_origin`・`pushed_after_not_seen`・`push_joins_pr`・`approval_covers_content` の命題と論拠の「承認の時点」「承認のあと」を、「その人の最後の承認の時点」「最後の承認のあと」に書き換える（D3 に合わせる）。型・種類・@support・確信度の行は変えない |
| A4 | M2 | `approval_covers_content` に「要ファクト: 社内で、プルリクエストを承認する人が、差分（変更の中身）を読んでから承認しているかを、ユーザーに確かめる。承認のあとに足された commit を、頼み直したレビューで読んでいるかも含む」を足す。弱い点に「F6 は、プルリクエストがレビューのための機能であることを述べるだけで、承認する人の振る舞いは述べていない（F6）」を足す。種類（【経験則】）・@support・@confidence 0.05・@reviewer の行は変えない |
| A5 | M3 | `protection_rejects_push`・`protection_only_approved_pr` の型の「管理者でない」を「保護を迂回できない」（D5 の述語の否定）に替える。docstring の1行目の命題文も「保護を迂回できない人の…」に直す。弱い点を「初期設定では、管理者などには効かない（F4）。その人たちは、迂回できる立場として前提で除いてある」にする。@confidence 0.75 と @reviewer の行は変えない。値を見直すかは Reviewer が決める |
| A6 | M3 | `newcomer_not_admin` を消し、`newcomer_no_bypass`（【仮定】）を足す。命題は「新人は、保護を迂回できる立場にない（管理者の権限も、迂回の権限も持たない）」。中身は3節 |
| A7 | M3 | `admin_exempt_by_default` を消し、`bypass_exempt_by_default`（【実験】F4）を足す。命題は「保護の設定が迂回できる立場の人にも効くようになっていなければ、その人の直接 push は拒否されない」。中身は3節 |
| A8 | M4 | `next_month_block_requires_pr`（【仮定】）を足す。命題は「来月、直接 push を拒否する設定が入るなら、それは承認1名以上のプルリクエストを必須にする保護である」。中身は3節 |
| A9 | L4 | `unrejected_push_lands` の弱い点を「手元の main が古いと、GitHub が fast-forward でない push を断る（git pull のあとなら通る）。この拒否は、設定の水準の拒否（pushRejected）には入らない」に書き換える |
| A10 | L2 | `recipe_update_main`・`recipe_create_branch`・`recipe_push_branch`・`recipe_open_pr`・`recipe_request_review`・`recipe_push_fix`・`recipe_squash_merge`・`recipe_doable` の型の述語を、D10 の新しい述語に替える。命題の「動きを確かめてある」「確かめてある」を消す（確かめたことは @support と論拠に残す）。種類と @support は変えない |
| A11 | L2 | `recipe_doable` の命題を「決まった短い操作がある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える」にし、論拠に「文書は、流れの各操作を、その決まった操作で説明する」を足す |

## 3. 足す公理の中身

**`incident_direct_push_stopped_team`（A1）**
種類: 【実験】。型の見当: `∃ p c, directlyWrites .lastMonth p c ∧ stopsTeam c`。@support F1。確信度: 事実の値。
論拠: 先月の1回目の事故で、main に直接 push した変更のために、半日チーム全員の作業が止まった（F1）。1件の事実から存在を言うだけで、一般化を含まない。
弱い点: 依頼者の証言だけで、社内の事故記録は確かめていない（F1）。

**`next_month_block_requires_pr`（A8）**
種類: 【仮定】。型の見当: `directPushBlocked .nextMonth → protectedMain .nextMonth`。
@support なし（F3 は「直接 push を拒否する設定に来月変える予定」と述べるだけで、どの設定を入れるか、必要な承認数をいくつにするかは述べていない。F7 は社内の決まりで、GitHub の設定ではない）。
確信度の案: 0.05。
論拠: main への直接 push を止める設定としてふつう使うのは、マージの前にプルリクエストを必須にする保護で、社内の決まり（承認1名以上）とも合う。
弱い点: 承認を求めずに直接 push だけを止める設定（承認数 0 や、push できる人を限る設定など）もありうる。その場合、C5 の結論は「承認を得たプルリクエストだけ」ではなく「プルリクエストを通ったものだけ」に弱まる。
要ファクト: 来月 main に入れる設定が「Require a pull request before merging」か、必要な承認数を1以上にするかを、ユーザーに確かめる。

**`newcomer_no_bypass`（A6）**
種類: 【仮定】。型の見当: `¬ bypassesProtection newcomer`。
@support なし（新人のリポジトリでの役割を確かめた事実が、まだない）。確信度の案: 0.05。
論拠: 新人に、管理者の権限や、保護を迂回する権限を渡すことは、ふつうない。
弱い点: 事実がまだない。
要ファクト: 新人のリポジトリでの役割（権限）が、管理者でも、保護を迂回できる役割でもないことを、ユーザーに確かめる。

**`bypass_exempt_by_default`（A7）**
種類: 【実験】。型の見当: `∀ m p, bypassesProtection p → ¬ bypassDisallowed m → ¬ pushRejected m p`。@support F4。確信度: 事実の値。
論拠: 初期設定では、保護の制限は、リポジトリの管理者の権限を持つ人に効かない（F4）。迂回の権限を持つ役割は、その権限の意味から、制限を受けない。
弱い点: F4 の引用が直接述べるのは、管理者の権限を持つ人だけである。迂回の権限を持つ役割は、F4 の「管理者など」に含めて読んでいる（F4）。

1周目の3節の表の【仮定】は、この周のあと次の6個になる。`approver_not_author`・`approved_change_can_break`・`newcomer_can_commit`・`recipe_doable`・`newcomer_no_bypass`・`next_month_block_requires_pr`。

## 4. 定理の変更

| # | 指摘 | 変更 |
|---|---|---|
| T1 | M6 | `c1_direct_push_can_stop_team` を、A1 の新しい公理だけで示す。型は変えない。全称の「main のビルドが壊れればチーム全員が止まる」は、C2 と U2 だけが使う |
| T2 | H1・M1 | `c3_flow_reviews_every_entry` を消す。読み (i) の定理で、前提がいつも偽だった |
| T3 | H1・M1・H2 | `c3_own_changes_approved_by_other` を足す（@claim C3、[決定論]）。C3 の項「ほかの人の承認を通る」 |
| T4 | H1・M1・M2 | `c3_own_changes_reviewed_by_other` を足す（@claim C3、[決定論]）。C3 の項「ほかの人のレビューを通る」 |
| T5 | M4 | `c5_only_pr_route_when_protected` の前提を「来月、直接 push を拒否する設定が入る」（D7 の述語）に替える。名前は変えない |
| T6 | H1・M4 | `c0_team_flow` の C3 の項を T3・T4 の結論の2つに、C5 の項を T5 の新しい型に替える |
| T7 | L1 | `u1_push_after_approval_unseen` の説明を「最後の承認のあとに push した変更は…」にし、「レビューを頼み直しても、古い承認のままマージすれば、足した commit は承認を通らない」を足す。型は変えない |
| T8 | H1 | `u3_merge_needs_another_person` の型の「流れを守る」を、D1 の月つきの形にする |
| T9 | M3・L6 | `u4_admin_still_unblocked` を消し、`u4_bypasser_still_unblocked` を足す（[不利]） |
| T10 | 新設（C3 の読みの変更に伴う） | `u5_nonfollower_unreviewed_entry` を足す（[不利]）。C3 が自分の変更にしか言えないことの歯止め |

## 5. 定理の計画（変わるものだけ）

主張の定理の前提は、C1〜C5 の文の条件（「守るかぎり」「起きなければ」「拒否されるようになっても」）だけにする。現実についての判断は、関係公理の側に置く。
下のどの定理も、3節と1周目3節の公理（この差分で消したものを除く）と、2節の宣言・def だけで示せることを確かめた。Writer が公理を補う必要はない。

**C1: `c1_direct_push_can_stop_team`**（@claim C1、[決定論]。型は変えない）
使う判断: `incident_direct_push_stopped_team` だけ。

**C3 の項「ほかの人の承認を通る」: `c3_own_changes_approved_by_other`**（@claim C3、[決定論]）
型の見当: `∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c → ∃ pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ inPRWhenApproved c pr q`
日常語: その月に流れを守る人が、その月に main に入れる変更は、どれも、その人が squash merge したプルリクエストに入っていて、その人とは別の人が承認していて、その別の人の最後の承認の時点で、その変更はプルリクエストに入っていた。
使う判断: 補題 `flow_changes_main_only_by_merge` の8つ（`update_main_keeps_main`・`create_branch_keeps_main`・`commit_keeps_main`・`push_branch_keeps_main`・`open_pr_keeps_main`・`request_review_keeps_main`・`push_fix_keeps_main`・`approve_keeps_main`）、`bringing_needs_doing`、`bringing_changes_main`、`squash_content_from_pr`、`merge_content_origin`、`approver_not_author`。`main_entry_has_op` は使わない。
道筋: `bringing_needs_doing` と (a) で、その操作は流れに含まれる。`bringing_changes_main` と補題で、その操作は squash merge になる。`squash_content_from_pr` でプルリクエスト pr を得る。(c) で、承認した人 q を得る（q の最後の承認のあとの push はない）。`merge_content_origin` の2つの枝のうち、「最後の承認のあとに push された」は (c) で閉じ、「最後の承認の時点で入っていた」が残る。q ≠ p は、`approver_not_author` と (b) から出る。

**C3 の項「ほかの人のレビューを通る」: `c3_own_changes_reviewed_by_other`**（@claim C3、[決定論]）
型の見当: `∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c → ∃ pr q, squashMerges m p pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q`
使う判断: 上の定理の判断すべてと、`approval_covers_content`。上の定理の結論に `approval_covers_content` を1回当てれば示せる。

C3 の2つの定理の型は `∀ m p` で、主張の「自分」を、読者のだれにでも当てはまる形にしたもの。新人に固有の公理を使っていないので、主張より強くはない。

**C5: `c5_only_pr_route_when_protected`**（@claim C5、[決定論]。名前は変えない）
型の見当: `directPushBlocked .nextMonth → pushRejected .nextMonth newcomer ∧ ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c`
使う判断: `next_month_block_requires_pr`、`protection_rejects_push`、`protection_only_approved_pr`、`pr_needs_work_branch`、`newcomer_no_bypass`。
前提は、C5 の文の条件をそのまま写したもの。「その設定が、承認1名以上のプルリクエストを必須にする保護である」という判断は、定理の引数から `next_month_block_requires_pr` に移した。

**C0: `c0_team_flow`**（@claim C0、[決定論]）
結論の `∧` の項を、直接の書き込みが流れに含まれないこと、C1 の2つ、C2、C3 の2つ（T3・T4 の型）、C4 の2つ、C5（T5 の型）にする。証明は、それぞれの定理を並べるだけ。

**U1: `u1_push_after_approval_unseen`**（[不利]。型は変えない）
使う判断は変わらない（`push_joins_pr`・`squash_brings_all_pr`・`pushed_after_not_seen`）。

**U3: `u3_merge_needs_another_person`**（[不利]）
型の見当: `doneByAuthor .approve = false ∧ ∀ m p pr, FollowsFlow m p → squashMerges m p pr → ∃ q, approvedBy pr q ∧ q ≠ p`
使う判断: `approver_not_author`。

**U4: `u4_bypasser_still_unblocked`**（[不利]）
型の見当: `∀ m p c, bypassesProtection p → ¬ bypassDisallowed m → triesDirectPush m p c → directlyWrites m p c`
使う判断: `bypass_exempt_by_default`、`unrejected_push_lands`。

**U5: `u5_nonfollower_unreviewed_entry`**（[不利]。新しい）
型の見当: `∃ m p c, directlyWrites m p c ∧ ¬ viaApprovedPR c ∧ ¬ FollowsFlow m p`
日常語: 流れを守らない人の直接の書き込みで、承認を得たプルリクエストを通らない変更が main に入ったことがある。C3 は、自分が守ることで自分の変更を守るだけで、ほかの人のこうした変更は防がない。
使う判断: `incident_direct_push_stopped_team`、`direct_write_skips_pr`、`bringing_needs_doing`（あとは、流れの一覧に直接の書き込みが含まれないことの計算）。主張に有利な向きの仮定を通らない。

変えない定理: `c1_direct_push_unreviewed_release`、`c2_only_self_stops_this_month`、補題 `flow_changes_main_only_by_merge`、`c4_flow_follows_rules`、`c4_newcomer_can_do_own_steps`、`u2_reviewed_change_can_stop_team`。C4 の2つ目は、使う公理の述語の名前が変わる（A10）だけで、定理の文と証明は変わらない。

`@beyond` と `@baseline` の定理は、1周目と同じく置かない。

## 6. 「同じとみなす」置き方（変更点）

比較の文はないので、方式どうしで同じとみなす量はない（1周目と同じ）。1周目の4節の表を、次のように足し、直す。

`next_month_block_requires_pr` を足す。来月の「直接 push を拒否する設定」を、承認1名以上のプルリクエストを必須にする保護とみなす。理由は、社内の決まり（承認1名以上）と合う、ふつうの設定だから。向きは主張の側（C5）。証拠がないので確信度は 0.05。

`approval_covers_content` は、主張の側のまま。ただし、使うのは C3 のレビューの項（T4）だけになった。承認の項（T3）は使わない。

`broken_main_stops_team` は、C1 の道筋から外れた（T1）。使うのは C2（主張の側）と U2（反対の側）だけ。

`bypass_exempt_by_default` は、「同じとみなす」置き方ではなく F4 の事実である。U4 だけが使い、反対の側に働く。

片寄りの確認: 並べたものは、まだ主張の側に片寄っている。埋め合わせは1周目のとおりにする（証拠のないものは 0.05 にしてステージ6に戻す、不利な結論を有利な仮定を通らずに導く）。この周で U5 を足した。U5 は F1 の事実と語の定義だけで導く。

## 7. 比べる相手と、予想される不利な結論（変更点）

比べる相手: 比較なし（変わらない）。

U1 は、流れの一部になった。本文では「承認のあとに commit を足したら、もう一度レビューを頼み、承認を受け直してからマージする」と書く。「頼む」で止めると、古い承認のままマージしてよいと読まれ、足した commit は承認を通らない（U1）。社内で、新しい commit を push すると承認を取り消す設定が有効かは分からない（F14 の notes）。そのため、設定に頼らない書き方にする。

U5（新しい、[不利]）: C3 は、自分の変更についての文である。本文で「main に入る変更はすべてレビューを通る」と書かない。ほかの人が直接 push すれば、未レビューの変更は入りうる（先月の事故）。これは C2 の「一人ひとりが流れを守る必要がある」につながる。

U4 は、名前を `u4_bypasser_still_unblocked` に変えた。来月からも「全員の直接 push が止まる」とは書けない。止まらないのは、管理者だけでなく、保護を迂回できる役割の人も含む。

C5 について: 来月の設定の種類は分からない（`next_month_block_requires_pr`、0.05）。事実が集まるまで、本文で「来月からは、承認を得たプルリクエストしか入らない」と言い切らない。

C5 の本文の範囲（L3 に関わる注意）: 本文で C5 を書くときは、「来月からも、新人が main に変更を入れる道は、この流れ（作業ブランチから出して承認を得たプルリクエスト）だけ」までにとどめる。保護がブランチ名や squash merge まで強制するとは書かない。

1周目6節の「そのほかの注意」のうち、直接の書き込みと `main_entry_has_op` についての注記は、次に置き換える。直接の書き込みは、push だけでなく、GitHub の画面での直接編集や API での書き込みも含む（D4）。「main に直接 push しない」だけを書くと、画面での直接編集が残る。本文で「main を直接変えない」まで広げるかは、ステージ8〜11で判断する。

U2・U3 と、コンフリクトの注意は変わらない。

## 8. 証人の見通し（Writer へ）

1周目の証人（人 0〜3、プルリクエスト 0・1、変更 0〜2）を土台にし、次を満たすように直す。

H1 の再発を防ぐ点: 人 0（新人）は、どの月も `FollowsFlow m 0` を満たす。今月、人 0 はプルリクエスト 0 を squash merge して、変更 1 を main に入れる。これで、C3 の2つの定理の前提が成り立ち、結論に実例がある。公理のうち存在を言うものは、`incident_direct_push_stopped_team`（先月、直接書き込んだ人がいる）と `approved_change_can_break` だけで、どちらも「その月に流れを守る人」を否定しない。

人 3 は、先月 main に直接書き込み（変更 0）、その変更はチーム全員を止める。`incident_direct_push_stopped_team` と U5 の例になる。先月の人 3 は流れを守っていない。

L6: 人 2 を、保護を迂回できる人（`bypassesProtection`）にする。来月、人 2 は変更 3 を直接 push しようとし（`triesDirectPush`）、拒否されずに main に直接書き込む（`bringsInVia` の直接の書き込み、変更 3）。`bringing_needs_doing` のために、`doesOp` でも来月の人 2 の直接の書き込みを真にする。変更 3 はビルドを壊さないことにすれば、`broken_main_stops_team` と食い違わない。`bypassDisallowed` はいつも偽にする。これで U4 の前提が成り立つ。

`directPushBlocked` と `protectedMain` は、来月だけ真にする。`next_month_block_requires_pr` と C5 の前提が成り立つ。

`hasFixedRecipe` は、直接の書き込み以外で真にする（1周目の `hasCheckedRecipe` と同じ）。

`approvedBy`・`inPRWhenApproved`・`pushedAfterApproval` の具体物は、1周目のままでよい。最後の承認を基準にしても、証人の値は変わらない。

`Model.lean` への写し方: `Argument.lean` の axiom 以外の行を直したら、同じ変更を `Model.lean` に写す。写す向きは `Argument.lean` から `Model.lean` だけにする。`Argument.lean` の docstring にある `@reviewer` の行と、Reviewer が書き換えた `@confidence` は、`Model.lean` の古い docstring から写し戻して消さない。`Model.lean` の冒頭の「C3 の前提は、この世界では成り立たない」の文は消し、上の見通しに合わせる。

`Argument.lean` の冒頭: 「主張と定理の対応」の表を、05-claims.json の新しい C3 の文と、この周の定理の名前に直す。「設計書との違い」は、この周でも残る違いだけにする。

## 9. 採らない指摘と、この周でモデルを変えない指摘

**M5（C4 の文が定理より強い）:** この周ではモデルを変えない。C4 の文は 05-claims.json で変わっていない。文を直すのはステージ5の仕事で、ユーザーが決める。中の指摘なので、周は続けてよい。オーケストレータが、ステージの終わりの手戻りのときに、U3 と合わせてユーザーに見せる（例:「承認をもらうこと以外は、自分で進められる」）。後半の「順序どおりに進められるか」は、読者が文書の順に進められるかという問題で、`recipe_doable` の要ファクト（新人に手順どおりに1本通してもらう）で確かめる。順序を型に入れても、判断は同じ公理に戻るので、宣言は足さない。

**L3（C5 の「知っておく必要がある」までの橋）:** 採らない。「必要がある」は規範の部分で、1周目の1節で、C0 の「この手順を採るべきだ」と同じく関係公理にしないと決めた部分にあたる。モデルが支えるのは、「来月も、新人が main に入れる道は、承認を得たプルリクエストの流れだけ」まで。本文をそこにとどめる注意を、7節に書いた。保護がブランチ名や squash merge を強制しないことは、C5 の定理の結論にも道筋にも入らないので、公理にしない。

**L5（U2 の公理の事実）:** モデルは変えない。ステージ6の手戻りで、社内で承認を受けてマージした変更がビルドを壊したことがあるかを、ユーザーに確かめる（要ファクトは1周目のまま）。U2 の値が低くても、「壊さずに済む」を支える定理はない。本文でそう書かないことは変わらない。

**L6:** 証人の指示（8節）で答えた。Writer の仕事。

**H2:** ステージ5でユーザーが決めた（再レビュー込み）。モデルでは、0節の理由と D2 で答えた。

**M2 の「別の道」（手続きの読み）:** C3 を「承認」と「レビュー」の2つの項に分けて、両方を置いた（T3・T4）。T3 は `approval_covers_content` を使わない。

## 10. 確かめること（Reviewer へ）

(c) の読み: 0節の理由で、「頼み直したレビューで承認を受け直してからマージする」と読んだ。Reviewer が、C3 が成り立つ別の読みがあると判断したら、ステージ5で確かめる。

C0 の文: C0 の文には、再レビューが書かれていない。`c0_team_flow` は、C3 と同じ `FollowsFlow` を「この流れ」として使う。C0 の文を流れの要約とし、C3 の括弧書きが流れの細部を足す、と読んだ。本文では、C0 の手順の中に再レビューを入れる。

C3 の2つの項: 「レビューを通る」を「承認した人が中身を見た」と読んだ。04-analysis.md の「もう一度見てもらうよう勧める」と同じ向きである。「提示されて承認された」だけの意味なら、T4 は主張より強い定理になる。その場合はステージ5で確かめ、T4 を消す。

消した宣言: `main_entry_has_op` と `c3_flow_reviews_every_entry` は棄却ではない。主張の読みが変わって要らなくなった。`incident_direct_push_broke_build` も、A1 の公理に置き換えただけで、誤りと分かったのではない。

保護の2つの公理: 型は F4 に合わせて直した（A5）。`@reviewer` の行と値 0.75 は変えていない。値を見直すかは Reviewer が決める。

## 11. 値の見通し

この周の変更で、どの主張の値も上がらない見込み。C0 0.05、C1 0.6、C2 0.6、C3 0.05、C4 0.05、C5 0.05。

C3 の承認の項（T3）は、`approver_not_author`（0.05）で止まる。GitHub Docs で「プルリクエストを出した本人は、自分のプルリクエストを承認できない」を確かめれば、`merge_content_origin`・`approve_keeps_main` の 0.8 まで上がる見込み。レビューの項（T4）は、`approval_covers_content` にユーザーの証言が要る。

C5 は、`newcomer_no_bypass` と `next_month_block_requires_pr`（どちらも 0.05）で止まる。事実が集まっても、上限は保護の2つの公理の 0.75。

手戻りの一覧の見込みは7個。`approval_covers_content`・`approver_not_author`・`approved_change_can_break`・`newcomer_can_commit`・`recipe_doable`・`newcomer_no_bypass`・`next_month_block_requires_pr`。`main_entry_has_op` は消えて一覧から外れ、`next_month_block_requires_pr` が入る。

次の周で高の指摘が0になれば、`cyrus logic-round close` はループを止める見込み。
