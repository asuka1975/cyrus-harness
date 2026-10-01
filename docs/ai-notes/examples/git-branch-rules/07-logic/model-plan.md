# 論証の設計書: 新人向け Gitブランチ運用ルール

Logical Model Planner が書く。Lean Writer はこれに従って `Argument.lean` と `Model.lean` を書く。

## 1. 主張の形と論証の深さ

05-claims.json には主張の形の指定がない。主張の文から次のように判断した。

| 主張 | 主張の文 | 形（能力の文／比較の文） | 論証の世界（決定論／確率・件数） | 理由 |
|---|---|---|---|---|
| C0 | 変更は main に直接 push せず、作業ブランチを切り、プルリクエストを出し、1名以上の承認を受けてから、自分で squash merge して main に取り込む。 | 能力の文 | 決定論 | 手順の指示で、ほかの方式と確率や件数で比べる語（「より」「少ない」「確率」）がない。モデルでは「この手順が C1〜C5 の性質をすべて持ち、社内の決まり（F7・F9・F11）に沿う」ことを示す定理として置く。「この手順を採るべきだ」という規範の部分は文書の目的（01-intent.md）であり、関係公理にはしない |
| C1 | main への直接 push は、チーム全員の作業を止めたり、未レビューの変更を本番に出しかけたりする危険がある。 | 能力の文（起こりうること） | 決定論 | 「危険がある」は、起こりうることを言う文。どのくらいの確率で起こるかも、流れを守る場合の何倍危ないかも言っていない。実際に起きた事故（F1・F2）が、起こりうることの証拠になる。04-analysis.md の論点でも「待ち時間と戻す手間を比べる数字はない。本文では比較せず」と決めている。流れの側との対比は、C3（流れなら必ずレビューを通る）と決定論で組む |
| C2 | 直接 push は今月はまだ仕組みで止められないので、一人ひとりが流れを守る必要がある。 | 能力の文（必要条件） | 決定論 | 「今月は GitHub が拒否しない」（F3）から「直接 push を止めるのは本人がしないことだけ」を導く文。確率を比べない |
| C3 | この流れを守るかぎり、main に入る変更はすべて、マージ前にほかの人のレビューと承認を通る。 | 能力の文（全称） | 決定論 | 「すべて」「通る」という全称の文で、例外の割合を言っていない。流れの定義と、git と GitHub の動き（F5・F6・F8・F12）から決定論で導ける形 |
| C4 | コンフリクト（同じ箇所の変更の衝突）が起きなければ、社内の決まりに沿った手順で、新人でも最初から最後まで自分で進められる。 | 能力の文 | 決定論 | 「進められる」は、できるかどうかの文。コンフリクトが起きないことを条件にした形 |
| C5 | 来月、仕組みで直接 push が拒否されるようになっても、この流れを知っておく必要がある。 | 能力の文（必要条件） | 決定論 | 保護の設定が入ると、main に変更を入れる経路が「承認を得たプルリクエスト」だけになる（F4）ことから導く。確率を比べない |

比較の文の主張はない。したがって、確率の世界（層・確率・「同じとみなす」判断）は作らず、失敗の台帳（`ledger.json`）も作らない。Prop と Bool だけで組む。

1周目の確信度の見込み（CLI の決まりどおりに計算した場合）: C1・C2 は 0.6（F1〜F3 が user_asserted のため）。C3・C4・C5 と、それらをまとめる C0 は、証拠のない【仮定】を通るので 0.05。どの【仮定】が値を決めるかは3節の「要ファクト」の欄にある。

## 2. コンポーネント（宣言）

比較の文がないので、方式の型（`Method`）は作らない。下の表の「方式を引数に取るか」はすべて「—」。

### 型と語彙

| 名前 | 型 | 何を表すか | 方式を引数に取るか |
|---|---|---|---|
| `Person` | `axiom Person : Type` | チームの人。新人、レビューする人、管理者を含む。main に書き込む自動の仕組み（ボットなど）があれば、それも含む | — |
| `Change` | `axiom Change : Type` | main に入りうる変更（commit の中身） | — |
| `PR` | `axiom PR : Type` | プルリクエスト | — |
| `Month` | inductive: `lastMonth` `thisMonth` `nextMonth` | 文書が扱う時期（先月・今月・来月） | — |
| `Op` | inductive: `updateMain` `createBranch` `commitOnBranch` `pushBranch` `openPR` `requestReview` `pushFix` `approve` `squashMerge` `otherMerge` `directWriteMain` | 文書が扱う操作の語彙。`updateMain` は `git switch main` と `git pull`、`createBranch` は `git switch -c`、`pushBranch` は `git push -u origin <ブランチ名>`、`pushFix` は指摘に応える commit を同じブランチへ push すること、`approve` はレビューする人の承認、`otherMerge` は squash 以外の方法でのマージ、`directWriteMain` は main への直接の書き込み（push と、GitHub の画面での直接編集の両方）。この語彙で main を変える操作が尽きるという判断は、型には置かず、関係公理 `main_entry_has_op` に置く | — |
| `BranchPrefix` | inductive: `feature` `fix` `other` | ブランチ名の頭。`other` は決まりにない名前 | — |
| `WorkKind` | inductive: `newFeature` `bugFix` | 作業の種類（新しい機能か、不具合の修正か） | — |
| `MergeMethod` | inductive: `squash` `mergeCommit` `rebase` | マージの方法 | — |
| `Merger` | inductive: `prAuthor` `someoneElse` | マージする人（プルリクエストを出した本人か、ほかの人か） | — |

### 定数と関係（中身を決めない宣言）

| 名前 | 型 | 何を表すか | 方式を引数に取るか |
|---|---|---|---|
| `newcomer` | `Person` | この文書の読者（今年入社の新人） | — |
| `isAdmin` | `Person → Prop` | その人がリポジトリの管理者である | — |
| `canWrite` | `Person → Prop` | その人がリポジトリに push できる権限を持っている | — |
| `author` | `PR → Person` | そのプルリクエストを出した人 | — |
| `doesOp` | `Month → Person → Op → Prop` | その月、その人がその操作をする | — |
| `bringsInVia` | `Month → Person → Op → Change → Prop` | その月、その人がその操作で、その変更を GitHub の main に入れる | — |
| `entersMain` | `Month → Change → Prop` | その月、その変更が main に入る（誰の操作かは問わない） | — |
| `changesMain` | `Op → Prop` | その操作は、GitHub の main の中身を変える | — |
| `triesDirectPush` | `Month → Person → Change → Prop` | その月、その人がその変更を main に直接 push しようとする | — |
| `pushRejected` | `Month → Person → Prop` | その月、その人の main への直接 push を GitHub が拒否する | — |
| `protectedMain` | `Month → Prop` | その月、main にブランチ保護（「Require a pull request before merging」）が有効になっている | — |
| `protectionCoversAdmins` | `Month → Prop` | その月の保護の設定が、管理者にも効くようになっている | — |
| `squashMerges` | `Month → Person → PR → Prop` | その月、その人がそのプルリクエストを squash merge する | — |
| `inPRAtMerge` | `Change → PR → Prop` | マージの時点で、その変更がそのプルリクエストに入っている | — |
| `approvedBy` | `PR → Person → Prop` | マージの前に、その人がそのプルリクエストを承認した | — |
| `inPRWhenApproved` | `Change → PR → Person → Prop` | その人が承認した時点で、その変更がプルリクエストに入っていた | — |
| `pushedAfterApproval` | `Change → PR → Person → Prop` | その人の承認のあとに、その変更がプルリクエストのブランチに push された | — |
| `reviewedBy` | `Change → Person → Prop` | その人が、その変更を見たうえで承認した | — |
| `viaApprovedPR` | `Change → Prop` | その変更は、承認を得たプルリクエストを通って main に入った | — |
| `fromWorkBranch` | `Change → Prop` | その変更は、main 以外のブランチ（作業ブランチ）から出したプルリクエストで入った | — |
| `breaksBuild` | `Change → Prop` | その変更で、main のビルドが壊れる | — |
| `stopsTeam` | `Change → Prop` | その変更のせいで、チーム全員の作業が止まる | — |
| `releaseCandidate` | `Change → Prop` | その変更が、次のリリースで本番に出る候補になる | — |
| `hasCheckedRecipe` | `Op → Prop` | その操作を行う決まったコマンドか画面の操作があり、その動きを確かめてある | — |
| `canDo` | `Op → Prop` | 新人が、その操作を自分で行える | — |
| `noConflict` | `Prop` | 作業のあいだにコンフリクトが起きない（C4 の条件） | — |
| `ruleMinApprovals` | `Nat` | 社内の決まりで、マージに必要な承認の最少人数 | — |
| `ruleMergeMethod` | `MergeMethod` | 社内の決まりのマージの方法 | — |
| `ruleMerger` | `Merger` | 社内の決まりでマージする人 | — |
| `ruleAllowsPrefix` | `BranchPrefix → Prop` | 社内の決まりで、そのブランチ名の頭を使ってよい | — |

### def（文書が勧める手順そのもの。現実についての判断ではない）

C0 が勧める手順を、定義として置く。どれも「文書が何を指示するか」を書いたもので、現実についての判断を含まない。現実との関係（決まりに沿うか、新人にできるか、main をどう変えるか）は、すべて関係公理の側に置く。

| 名前 | 型 | 何を表すか | 方式を引数に取るか |
|---|---|---|---|
| `teamFlow` | `List Op` | 文書が勧める操作の一覧: `[updateMain, createBranch, commitOnBranch, pushBranch, openPR, requestReview, pushFix, approve, squashMerge]`。`pushFix` は指摘があったときだけ行う。モデルでは「流れの中で使ってよい操作」として、含まれるかどうかだけを使う（順序は `FollowsFlow` の条件で表す） | — |
| `doneByAuthor` | `Op → Bool` | その操作をプルリクエストを出した本人が行うか。`approve` だけが `false`（レビューする人が行う） | — |
| `flowPrefix` | `WorkKind → BranchPrefix` | 文書が指示するブランチ名の頭（`newFeature` なら `feature`、`bugFix` なら `fix`） | — |
| `flowMergeMethod` | `MergeMethod` | 文書が指示するマージの方法（`squash`） | — |
| `flowMerger` | `Merger` | 文書が指示するマージする人（`prAuthor`） | — |
| `flowMinApprovals` | `Nat` | 文書が指示する承認の最少人数（1） | — |
| `directlyWrites` | `Month → Person → Change → Prop` | 略記: `bringsInVia m p .directWriteMain c` | — |
| `FollowsFlow` | `Person → Prop` | その人が流れを守っている。次の3つを満たすこと。(a) する操作はすべて `teamFlow` に含まれる（main への直接の書き込みも、squash 以外のマージもしない）。(b) squash merge するのは、自分が出したプルリクエストだけ（`author pr = p`）。(c) squash merge するプルリクエストには、承認した人 `q` がいて、その承認のあとに push された変更がない（承認のあとに push したら、承認を受け直してからマージする） | — |

`FollowsFlow` の (c) の後半（承認のあとに push したら受け直す）は、6節の不利な結論 U1 から必要になる条件。04-analysis.md の論点（「もう一度見てもらうよう勧める」）とも一致する。

## 3. 関係公理（原子命題ごと）

1行に原子命題1つ。【実験】の確信度は CLI が事実の status から決めるので「（事実の値）」と書く。【自明】は 1。
論拠と弱い点は、表の下の「論拠と弱い点」に公理ごとに書く。弱い点に書いた事実 ID は、すべて `@support` にも入れてある（入れていない ID は弱い点に書かない）。

### C1・C2: 直接 push の危険

| 名前 | 種類 | 命題（日常語） | 支える事実 | 確信度の案 | 要ファクト |
|---|---|---|---|---|---|
| `incident_direct_push_broke_build` | 【実験】 | 先月、main に直接書き込まれ、ビルドを壊した変更がある（`∃ p c, directlyWrites .lastMonth p c ∧ breaksBuild c`） | F1 | （事実の値） | — |
| `direct_write_skips_pr` | 【自明】 | main に直接書き込んだ変更は、承認を得たプルリクエストを通っていない | — | 1 | — |
| `main_feeds_release` | 【経験則】 | main に入った変更は、次のリリースで本番に出る候補になる | F2 | 0.6 | — |
| `broken_main_stops_team` | 【経験則】 | main に入った変更がビルドを壊すなら、チーム全員の作業が止まる | F1 | 0.6 | — |
| `no_rejection_this_month` | 【実験】 | 今月は、誰の直接 push も GitHub に拒否されない | F3 | （事実の値） | — |
| `unrejected_push_lands` | 【経験則】 | 直接 push しようとして、拒否されなければ、その変更は main に直接書き込まれる | F1, F2 | 0.6 | — |

### C3: 流れを守れば、main に入る変更はレビューを通る

| 名前 | 種類 | 命題（日常語） | 支える事実 | 確信度の案 | 要ファクト |
|---|---|---|---|---|---|
| `main_entry_has_op` | 【仮定】 | main に入る変更には、それを入れた人と、`Op` の語彙のどれかの操作がある（`∀ m c, entersMain m c → ∃ p o, bringsInVia m p o c`） | なし | 0.7 | GitHub で main の中身を変える方法が、直接の書き込み（push・画面での直接編集）と、プルリクエストのマージ（squash とそれ以外）に尽きることを GitHub Docs で確かめる。あわせて、社内に main へ書き込む自動の仕組み（ボットなど）があるかをユーザーに確かめる |
| `bringing_needs_doing` | 【自明】 | ある操作で変更を main に入れたなら、その人はその操作をしている | — | 1 | — |
| `bringing_changes_main` | 【自明】 | 変更を main に入れた操作は、main の中身を変える操作である | — | 1 | — |
| `update_main_keeps_main` | 【自明】 | `git switch main` と `git pull` は、GitHub の main を変えない | — | 1 | — |
| `create_branch_keeps_main` | 【自明】 | `git switch -c` でブランチを作っても、GitHub の main は変わらない | — | 1 | — |
| `commit_keeps_main` | 【実験】 | 作業ブランチへの commit は、main を変えない | F5 | （事実の値） | — |
| `push_branch_keeps_main` | 【経験則】 | 作業ブランチを push しても、GitHub の main は変わらない | F5, F13 | 0.9 | — |
| `open_pr_keeps_main` | 【実験】 | プルリクエストを作っても、main は変わらない | F6 | （事実の値） | — |
| `request_review_keeps_main` | 【自明】 | レビューを依頼しても、main は変わらない | — | 1 | — |
| `push_fix_keeps_main` | 【経験則】 | 指摘に応える commit を同じブランチに push しても、main は変わらない | F8, F13 | 0.9 | — |
| `approve_keeps_main` | 【経験則】 | 承認しても、main は変わらない（マージは別の操作） | F6 | 0.8 | — |
| `squash_content_from_pr` | 【実験】 | squash merge で main に入る変更は、そのとき squash merge したプルリクエストに入っていた変更である | F12 | （事実の値） | — |
| `merge_content_origin` | 【経験則】 | マージの時点でプルリクエストに入っている変更は、承認の時点で入っていたか、承認のあとに push されたかのどちらか（`∨` の公理） | F6, F8 | 0.8 | — |
| `approval_covers_content` | 【経験則】 | 承認の時点でプルリクエストに入っていた変更は、承認した人が見たうえで承認している | F6 | 0.7 | — |
| `approver_not_author` | 【仮定】 | プルリクエストを承認した人は、それを出した本人ではない | なし | 0.8 | GitHub では、プルリクエストを出した本人が自分のプルリクエストを承認できないことを GitHub Docs で確かめる |

### U1: 承認のあとの push（6節の不利な結論）

| 名前 | 種類 | 命題（日常語） | 支える事実 | 確信度の案 | 要ファクト |
|---|---|---|---|---|---|
| `push_joins_pr` | 【実験】 | 承認のあとに push された変更も、マージの時点でプルリクエストに入っている | F8 | （事実の値） | — |
| `squash_brings_all_pr` | 【実験】 | squash merge すると、マージの時点でプルリクエストに入っている変更は、すべて main に入る | F12 | （事実の値） | — |
| `pushed_after_not_seen` | 【自明】 | 承認のあとに push された変更は、承認の時点ではプルリクエストに入っていなかった | — | 1 | — |

### U2: 流れを守っても壊れうる（6節の不利な結論）

| 名前 | 種類 | 命題（日常語） | 支える事実 | 確信度の案 | 要ファクト |
|---|---|---|---|---|---|
| `approved_change_can_break` | 【仮定】 | 承認を得たプルリクエストの squash merge で main に入り、ビルドを壊す変更がある（`∃ m p c, bringsInVia m p .squashMerge c ∧ viaApprovedPR c ∧ breaksBuild c`） | なし | 0.5 | 社内で、承認を受けてマージした変更で main のビルドが壊れたことがあるかを、ユーザーに確かめる |

### C4: 社内の決まりに沿うこと

| 名前 | 種類 | 命題（日常語） | 支える事実 | 確信度の案 | 要ファクト |
|---|---|---|---|---|---|
| `rule_min_approvals` | 【実験】 | マージに必要な承認の最少人数は1人 | F7 | （事実の値） | — |
| `rule_merge_method` | 【実験】 | 社内のマージの方法は squash merge | F11 | （事実の値） | — |
| `rule_merger` | 【実験】 | 社内でマージするのは、プルリクエストを出した本人 | F11 | （事実の値） | — |
| `rule_prefix_feature` | 【実験】 | ブランチ名の頭に `feature` を使ってよい | F9 | （事実の値） | — |
| `rule_prefix_fix` | 【実験】 | ブランチ名の頭に `fix` を使ってよい | F9 | （事実の値） | — |

### C4: 新人が自分で進められること

| 名前 | 種類 | 命題（日常語） | 支える事実 | 確信度の案 | 要ファクト |
|---|---|---|---|---|---|
| `recipe_update_main` | 【実験】 | 手元の main を最新にする操作（`git switch main` と `git pull`）があり、動きを確かめてある | F15 | （事実の値） | — |
| `recipe_create_branch` | 【実験】 | ブランチを作って移る操作（`git switch -c`）があり、動きを確かめてある | F10 | （事実の値） | — |
| `recipe_push_branch` | 【実験】 | 作業ブランチを GitHub に送る操作（`git push -u origin <ブランチ名>`）があり、動きを確かめてある | F13 | （事実の値） | — |
| `recipe_open_pr` | 【実験】 | push したブランチからプルリクエストを作る画面の操作があり、確かめてある | F14 | （事実の値） | — |
| `recipe_request_review` | 【実験】 | レビューする人（Reviewers）を指定する画面の操作があり、確かめてある | F14 | （事実の値） | — |
| `recipe_push_fix` | 【実験】 | 同じブランチに push すればプルリクエストに加わることを確かめてある | F8 | （事実の値） | — |
| `recipe_squash_merge` | 【実験】 | squash merge する画面の操作（「Squash and merge」）があり、動きを確かめてある | F12 | （事実の値） | — |
| `newcomer_can_commit` | 【仮定】 | 新人は、作業ブランチに自分で commit できる（`canDo .commitOnBranch`） | なし | 0.6 | 03-reader.json の「新人は Git で commit と push ができる」を、ユーザーの証言として 06-facts.json に登録する |
| `newcomer_can_write` | 【経験則】 | 新人は、リポジトリに push できる権限を持っている | F1, F2 | 0.6 | — |
| `recipe_doable` | 【仮定】 | 決まった操作があり動きを確かめてある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える（`∀ o, hasCheckedRecipe o → doneByAuthor o = true → canWrite newcomer → noConflict → canDo o`） | なし | 0.5 | 新人（または同じくらいの経験の人）に、文書の手順どおりにプルリクエストを1本通してもらい、詰まった操作を記録する |

### C5: 保護が入ったあとの経路

| 名前 | 種類 | 命題（日常語） | 支える事実 | 確信度の案 | 要ファクト |
|---|---|---|---|---|---|
| `protection_rejects_push` | 【実験】 | 保護が有効な月は、管理者でない人の直接 push は拒否される | F4 | （事実の値） | — |
| `protection_only_approved_pr` | 【実験】 | 保護が有効な月に、管理者でない人が main に入れる変更は、承認を得たプルリクエストを通ったものだけ | F4 | （事実の値） | — |
| `pr_needs_work_branch` | 【実験】 | 承認を得たプルリクエストで入った変更は、main 以外のブランチから出したプルリクエストで入っている | F6 | （事実の値） | — |
| `newcomer_not_admin` | 【仮定】 | 新人はリポジトリの管理者ではない | なし | 0.8 | 新人のリポジトリでの権限が管理者でないことを、ユーザーに確かめる |

### U4: 管理者は来月も止まらない（6節の不利な結論）

| 名前 | 種類 | 命題（日常語） | 支える事実 | 確信度の案 | 要ファクト |
|---|---|---|---|---|---|
| `admin_exempt_by_default` | 【実験】 | 保護の設定が管理者に効くようになっていなければ、管理者の直接 push は拒否されない | F4 | （事実の値） | — |

### 論拠と弱い点

- `incident_direct_push_broke_build`: 論拠: 先月の1回目の事故（F1）。弱い点: 依頼者の証言だけで、社内の事故記録は確かめていない（F1）。
- `direct_write_skips_pr`: 論拠: 「直接の書き込み」とは、プルリクエストを通さずに main を変えること（語の定義）。
- `main_feeds_release`: 論拠: main は本番に出すもとになる。F2 では、main に入った未レビューの変更が本番に出かけた。弱い点: 事例は1件（F2）。リリースの前に止める確認があれば本番には出ないが、候補になることは変わらない。
- `broken_main_stops_team`: 論拠: main は全員の作業の土台。F1 ではビルドが壊れて半日全員が止まった。弱い点: 事例は1件（F1）。main を取り込まずに作業している人は、すぐには止まらない。
- `no_rejection_this_month`: 論拠: F3。弱い点: 依頼者の証言（F3）。
- `unrejected_push_lands`: 論拠: 拒否されない push は受け入れられる。先月の直接 push は実際に main に入った（F1・F2）。弱い点: 手元の main が古いと、git が push を断る（`git pull` のあとなら通る）。
- `main_entry_has_op`: 論拠: main の中身は、誰かが何かの操作をしたときにしか変わらない。`Op` は直接の書き込み・squash merge・それ以外のマージを含む。弱い点: 語彙の外の操作（API での書き込みなど）が `directWriteMain` に入るかは、定義の広さによる。ボットが流れを守らずに main に書き込むなら、C3 の条件「全員が流れを守る」が成り立たない。
- `bringing_needs_doing`・`bringing_changes_main`: 論拠: 語の定義（「操作で入れた」なら、その操作をしていて、その操作は main を変えている）。
- `update_main_keeps_main`: 論拠: `git pull` は GitHub から取り込む操作で、GitHub に送る手順を含まない（コマンドの定義）。
- `create_branch_keeps_main`: 論拠: `git switch -c` は手元でブランチを作るだけで、GitHub に何も送らない。
- `commit_keeps_main`: 論拠: F5 で、作業ブランチに commit しても main の中身が変わらないことを実行して確かめた。弱い点: 手元での確認（F5）。まちがえて main の上で commit すると成り立たない（その後の push は `directWriteMain` にあたる）。
- `push_branch_keeps_main`: 論拠: `git push -u origin <ブランチ名>` は同じ名前のブランチを作る（F13）ので、main には書き込まない。弱い点: F13 は GitHub ではなく手元のリモートで確かめた。
- `open_pr_keeps_main`: 論拠: プルリクエストは、マージするよう「提案する」機能で、マージは別に行う（F6）。
- `request_review_keeps_main`: 論拠: レビューする人を指定するだけの操作。
- `push_fix_keeps_main`: 論拠: 同じブランチへの push はプルリクエストに加わる（F8）。送り先は作業ブランチ（F13）。弱い点: 送り先をまちがえて main にすると成り立たない（それは `directWriteMain` にあたる）。
- `approve_keeps_main`: 論拠: プルリクエストでは、レビューとマージは別の段階（F6）。弱い点: 自動マージ（auto-merge）を有効にしていると、承認がマージのきっかけになる。
- `squash_content_from_pr`・`squash_brings_all_pr`: 論拠: squash merge は、プルリクエストの commit を1つにまとめて取り込み先に加える（F12）。
- `merge_content_origin`: 論拠: プルリクエストの中身はブランチの commit で（F6）、ブランチに push した commit は自動で加わる（F8）。弱い点: 画面の「Update branch」や、レビューする人の提案を画面で取り込む commit も、承認のあとに中身を変える。これらを push とみなせば成り立つ。
- `approval_covers_content`: 論拠: プルリクエストは、マージの前に変更を話し合い、レビューする機能（F6）で、承認はその中身に対して出す。弱い点: 中身を読まずに承認することはありうる。社内で承認がどう出されているかは確かめていない。
- `approver_not_author`: 論拠: 「ほかの人のレビュー」の「ほかの人」を支える。弱い点: 事実がまだない。
- `push_joins_pr`: 論拠: プルリクエストを出したあとに同じブランチへ push した commit は、自動で加わる（F8）。弱い点: いったん加わった commit を強制的な push で消すと、マージの時点には残らない。
- `pushed_after_not_seen`: 論拠: 承認のあとに加わったものは、承認の時点ではまだない（時の前後の定義）。
- `approved_change_can_break`: 論拠: レビューは人が読むもので、見落としがありうる。弱い点: 社内の事例がまだない。
- `rule_min_approvals`: 論拠: 依頼者の証言した社内の決まり（F7）。弱い点: 証言だけで、社内の規程の文書は確かめていない（F7）。
- `rule_merge_method`・`rule_merger`: 論拠: 依頼者の証言した社内の決まり（F11）。弱い点: 証言だけで、社内の規程の文書は確かめていない（F11）。
- `rule_prefix_feature`・`rule_prefix_fix`: 論拠: 依頼者の証言した社内の決まり（F9）。弱い点: 証言だけで、社内の規程の文書は確かめていない（F9）。
- `recipe_update_main`: 論拠: 実行して確かめた（F15）。弱い点: GitHub ではなく手元のリモートで確かめた（F15）。
- `recipe_create_branch`: 論拠: 実行して確かめた（F10）。弱い点: git 2.23 より古い git にはこのコマンドがない。
- `recipe_push_branch`: 論拠: 実行して確かめた（F13）。弱い点: GitHub ではなく手元のリモートで確かめた（F13）。GitHub への認証の手間は含まない。
- `recipe_open_pr`・`recipe_request_review`: 論拠: GitHub Docs（F14）。
- `recipe_push_fix`: 論拠: GitHub Docs（F8）。操作そのものは commit と push で、新人が知っている。
- `recipe_squash_merge`: 論拠: GitHub Docs（F12）。画面のボタンは「Squash and merge」。弱い点: ボタンを押せるかはリポジトリの権限による。
- `newcomer_can_commit`: 論拠: 03-reader.json に「Git で commit と push はできる」とある。弱い点: 06-facts.json に事実として登録されていないので、`@support` にできない。
- `newcomer_can_write`: 論拠: 先月、新人が main に直接 push できた（F1・F2）ので、新人には push の権限がある。弱い点: 先月の新人と、今年の読者が同じ権限とは限らない（F1・F2）。
- `recipe_doable`: 論拠: 1つずつの操作は、決まったコマンドか画面の操作で済み、文書で説明する。弱い点: 新人に実際に通してもらった記録がない。ブランチ・プルリクエスト・マージ・レビューは読者の知らない語（03-reader.json）なので、本文での説明の出来に左右される。
- `protection_rejects_push`・`protection_only_approved_pr`: 論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。弱い点: 初期設定では管理者に効かない（F4）。
- `pr_needs_work_branch`: 論拠: プルリクエストは、異なる2つのブランチの間でしか作れない（F6 の出典の引用）。
- `newcomer_not_admin`: 論拠: 新人に管理者の権限を渡すことはふつうない。弱い点: 事実がまだない。
- `admin_exempt_by_default`: 論拠: 初期設定では、保護の制限は管理者に効かない（F4）。

## 4. 「同じとみなす」置き方

比較の文がないので、方式どうしで同じとみなす量はない。ただし、論証の中で「ある場合を、別の場合と同じとみなしている」ところがあるので、並べておく。「向き」の欄は、文書の主張の側（流れを守れ）に有利か、その反対の側に有利か。

| 公理 | 何を同じとみなすか | 理由 | どちらの方式に有利な向きか |
|---|---|---|---|
| `broken_main_stops_team`・`main_feeds_release` | 先月の事故1件ずつ（F1・F2）を、一般の場合とみなす | 事故の記録はそれぞれ1件で、ほかの直接 push の結果は数えていない | 主張の側（C1・C2 の危険を支える） |
| `unrejected_push_lands` | 先月の直接 push が通ったことを、今月も同じとみなす | F3 で「今はまだ拒否されない」 | 主張の側（C2） |
| `newcomer_can_write` | 先月の新人の権限を、今年の読者の権限と同じとみなす | 同じ「新人」の立場で、権限の違いを示す事実はない | 主張の側（C4） |
| `push_branch_keeps_main`・`recipe_push_branch`・`recipe_update_main` | 手元のリモートでの確認（F13・F15）を、GitHub でも同じとみなす | git の動きは同じ（F13 の notes） | 主張の側（C3・C4） |
| `approval_covers_content` | 「承認した」を「中身を見た」とみなす | プルリクエストはレビューのための機能（F6） | 主張の側（C3） |
| `recipe_doable` | 「決まった操作があり、動きを確かめてある」を「新人が自分でできる」とみなす | 操作が1つずつ短く、文書で説明する | 主張の側（C4） |

片寄りの確認: 並べたものは、すべて主張の側に有利な向きに片寄っている。反対の側に有利な判断は `approved_change_can_break`（U2 のためだけ）の1つ。
埋め合わせとして、次のようにする。

- 片寄った判断は、どれも【経験則】か【仮定】にして、弱い点を書く。証拠のないものは確信度 0.05 になり、ステージ6に戻る。
- 6節の不利な結論（U1〜U4）は、上の表の判断を、主張に有利な向きでは使わない経路で導く。U1 は `push_joins_pr`・`squash_brings_all_pr`・`pushed_after_not_seen` だけを使う。U2 は `broken_main_stops_team` を使うが、そこでは文書に不利な向きに働く。U4 は `unrejected_push_lands` を使うが、同じく不利な向きに働く。

## 5. 主張の項ごとの定理の計画

| 主張 | 項 | 定理の名前 | 使う判断（関係公理） | 種類 |
|---|---|---|---|---|
| C1 | チーム全員の作業を止める危険 | `c1_direct_push_can_stop_team`（`∃ m p c, directlyWrites m p c ∧ stopsTeam c`） | `incident_direct_push_broke_build`, `broken_main_stops_team` | [決定論] |
| C1 | 未レビューの変更を本番に出しかける危険 | `c1_direct_push_unreviewed_release`（`∀ m p c, directlyWrites m p c → ¬ viaApprovedPR c ∧ releaseCandidate c`） | `direct_write_skips_pr`, `main_feeds_release` | [決定論] |
| C2 | 今月は、止めるのは本人だけ | `c2_only_self_stops_this_month`（`∀ p c, triesDirectPush .thisMonth p c → directlyWrites .thisMonth p c ∧ ¬ viaApprovedPR c ∧ releaseCandidate c ∧ (breaksBuild c → stopsTeam c)`） | `no_rejection_this_month`, `unrejected_push_lands`, `direct_write_skips_pr`, `main_feeds_release`, `broken_main_stops_team` | [決定論] |
| C3 | （補題・印なし）流れの操作で main を変えるのは squash merge だけ | `flow_changes_main_only_by_merge`（`∀ o, o ∈ teamFlow → changesMain o → o = .squashMerge`） | `update_main_keeps_main`, `create_branch_keeps_main`, `commit_keeps_main`, `push_branch_keeps_main`, `open_pr_keeps_main`, `request_review_keeps_main`, `push_fix_keeps_main`, `approve_keeps_main` | [決定論] |
| C3 | 流れを守るかぎり、main に入る変更はすべて、マージ前にほかの人のレビューと承認を通る | `c3_flow_reviews_every_entry`（`(∀ p, FollowsFlow p) → ∀ m c, entersMain m c → ∃ p pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q`） | 補題の公理すべて、`main_entry_has_op`, `bringing_needs_doing`, `bringing_changes_main`, `squash_content_from_pr`, `merge_content_origin`, `approval_covers_content`, `approver_not_author` | [決定論] |
| C4 | 社内の決まりに沿った手順 | `c4_flow_follows_rules`（`ruleMinApprovals ≤ flowMinApprovals ∧ flowMergeMethod = ruleMergeMethod ∧ flowMerger = ruleMerger ∧ ∀ k, ruleAllowsPrefix (flowPrefix k)`） | `rule_min_approvals`, `rule_merge_method`, `rule_merger`, `rule_prefix_feature`, `rule_prefix_fix` | [決定論] |
| C4 | コンフリクトが起きなければ、新人が最初から最後まで自分で進められる | `c4_newcomer_can_do_own_steps`（`noConflict → ∀ o, o ∈ teamFlow → doneByAuthor o = true → canDo o`） | `recipe_update_main`, `recipe_create_branch`, `recipe_push_branch`, `recipe_open_pr`, `recipe_request_review`, `recipe_push_fix`, `recipe_squash_merge`, `newcomer_can_commit`, `newcomer_can_write`, `recipe_doable` | [決定論] |
| C5 | 保護が入っても、main に入れる経路は流れだけ | `c5_only_pr_route_when_protected`（`protectedMain .nextMonth → pushRejected .nextMonth newcomer ∧ ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c`） | `protection_rejects_push`, `protection_only_approved_pr`, `pr_needs_work_branch`, `newcomer_not_admin` | [決定論] |
| C0 | この手順は直接の書き込みを含まず、C1〜C5 の性質をすべて持つ | `c0_team_flow`（`.directWriteMain ∉ teamFlow` と、上の C1〜C5 の定理の結論すべての `∧`） | 上の C1〜C5 の定理が使う公理すべて | [決定論] |
| （C3 の限界） | 承認のあとに push した変更は、承認した人に見られないまま main に入る | `u1_push_after_approval_unseen`（`∀ m p pr q c, pushedAfterApproval c pr q → squashMerges m p pr → bringsInVia m p .squashMerge c ∧ ¬ inPRWhenApproved c pr q`） | `push_joins_pr`, `squash_brings_all_pr`, `pushed_after_not_seen` | [不利] |
| （C0・01-intent の限界） | 流れを守っても、全員の作業を止める変更が main に入りうる | `u2_reviewed_change_can_stop_team`（`∃ m p c, bringsInVia m p .squashMerge c ∧ viaApprovedPR c ∧ stopsTeam c`） | `approved_change_can_break`, `broken_main_stops_team` | [不利] |
| （C4 の限界） | マージまで進むには、ほかの人の承認が要る | `u3_merge_needs_another_person`（`∀ m p pr, FollowsFlow p → squashMerges m p pr → ∃ q, approvedBy pr q ∧ q ≠ p`。あわせて `doneByAuthor .approve = false`） | `approver_not_author` | [不利] |
| （C5 の限界） | 保護が入っても、管理者の直接 push は（管理者に効かせる設定がなければ）通る | `u4_admin_still_unblocked`（`∀ m p c, isAdmin p → ¬ protectionCoversAdmins m → triesDirectPush m p c → directlyWrites m p c`） | `admin_exempt_by_default`, `unrejected_push_lands` | [不利] |

印について（Writer へ）:

- `@claim` を付けるのは C0〜C5 の行の定理だけ（C1 と C4 は2つずつ）。補題 `flow_changes_main_only_by_merge` には印を付けない（`c3_flow_reviews_every_entry` の依存として、その公理が数えられる）。
- 比較の文がないので、`@baseline` の定理は置かない。文書で使う `@beyond` もないので置かない。
- [不利] の定理（`u1_`〜`u4_`）には、付ける印がない。印なしで置く。`push_joins_pr`・`squash_brings_all_pr`・`pushed_after_not_seen`・`approved_change_can_break`・`admin_exempt_by_default` の5つは、[不利] の定理だけが使う公理で、主張の定理には現れない（設計どおり）。
- 定理の引数に置く条件（C3 の `∀ p, FollowsFlow p`、C4 の `noConflict`、C5 の `protectedMain .nextMonth`）は、主張の文そのものの条件（「守るかぎり」「起きなければ」「拒否されるようになっても」）で、現実についての判断ではない。U1・U4 の条件も、場合を指定するだけのもの。
- F3 の「来月変える予定」は予定なので、C5 は「保護が有効なら」という条件の形で示し、予定が実現することには依存させない。

証人（`Model.lean`）の見通し: `Person := Unit`、`PR := Unit`、`Change := Bool` とし、`true` を直接の書き込みで入った変更、`false` を承認済みのプルリクエストの squash merge で入った変更にする。`bringsInVia m p o c := (o = .directWriteMain ∧ c = true) ∨ (o = .squashMerge ∧ c = false)`、`viaApprovedPR c := c = false`、`changesMain o := o = .directWriteMain ∨ o = .squashMerge ∨ o = .otherMerge`、`protectedMain`・`pushRejected`・`isAdmin`・`approvedBy`・`pushedAfterApproval` は `False`、`inPRAtMerge c _ := c = false`、`entersMain`・`squashMerges`・`breaksBuild`・`stopsTeam`・`releaseCandidate`・`hasCheckedRecipe`・`canDo`・`canWrite`・`noConflict`・`fromWorkBranch`・`ruleAllowsPrefix`・`doesOp` は `True`、残りの関係（`inPRWhenApproved`・`reviewedBy`・`protectionCoversAdmins`）は何でもよい、`triesDirectPush _ _ c := c = true`、決まりの定数は決まりどおりの値。これで存在の公理（`incident_direct_push_broke_build`・`approved_change_can_break`）と、全称の公理（`direct_write_skips_pr` など）が同時に成り立つ。

## 6. 比べる相手と、予想される不利な結論

比べる相手: 比較なし。
ただし、C1・C0 は「直接 push」と「流れ」を対比している。対比の相手の直接 push は、先月2回、現実に起きた行動（F1・F2）で、藁人形ではない。`c1_direct_push_can_stop_team` が F1 からそれを示す。

予想される不利な結論（5節の [不利] の定理）と、後のステージで気をつけること:

- **U1（C3 の限界）:** 承認のあとに同じブランチへ push した変更は、自動でプルリクエストに加わり（F8）、squash merge で main に入る（F12）。その変更は、承認した人に見られていない。C3 が成り立つのは、流れの条件に「承認のあとに push したら、承認を受け直してからマージする」を含めたとき（`FollowsFlow` の (c)）。本文でも、流れの一部としてこれを書く必要がある。社内で「新しい commit を push すると承認を取り消す」設定が有効かは分からない（F14 の notes）ので、設定に頼らず、本人がもう一度見てもらう形にする。
- **U2（C0 と 01-intent の限界）:** 流れが保証するのは「ほかの人のレビューと承認を通る」ことで、「ビルドを壊さない」ことではない。01-intent.md の「この流れを守れば、自分の変更で他の人の作業を壊さずに済む」は、このモデルからは導けない。本文では「レビューを通してから main に入る」までにとどめ、「壊さずに済む」と言い切らない。
- **U3（C4 の限界）:** 承認はレビューする人の操作で、新人の操作ではない。C4 の「最初から最後まで自分で進められる」は「承認をもらうこと以外は」という意味になる。本文では、承認を待つ段階があることと、誰に頼めばよいかを書く。
- **U4（C5 の限界）:** 初期設定では、保護の制限は管理者に効かない（F4）。来月からも「全員の直接 push が止まる」とは書けない。C5 は `newcomer_not_admin`（新人は管理者でない）に依存する。
- **そのほかの注意（定理にはしない）:**
  - `directWriteMain` は、push だけでなく GitHub の画面での直接編集も含む。「main に直接 push しない」だけを書くと、画面での直接編集が残る。本文で「main を直接変えない」まで広げるかは、`main_entry_has_op` の事実を集めたうえで、ステージ8〜11で判断する。
  - コンフリクトが起きた場合は、C4 の条件の外。04-analysis.md で詳しい解き方は載せないと決めているので、本文では「起きたら誰に聞くか」を示す必要がある。
