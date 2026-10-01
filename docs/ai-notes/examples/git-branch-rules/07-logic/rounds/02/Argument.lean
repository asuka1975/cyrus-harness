/-!
# 論証のモデル: 新人向け Gitブランチ運用ルール

設計書: `07-logic/model-plan.md`（1周目）と `07-logic/model-plan-delta.md`（2周目の差分）。主張: `05-claims.json`。事実: `06-facts.json`。

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
比較の文の主張はないので、すべて [決定論] で組む（設計書1節、差分の設計書0節）。

| 主張 | 主張の文 | 定理 | 種類 |
|---|---|---|---|
| C0 | 変更は main に直接 push せず、作業ブランチを切り、プルリクエストを出し、1名以上の承認を受けてから、自分で squash merge して main に取り込む。 | `c0_team_flow` | [決定論] |
| C1 | main への直接 push は、チーム全員の作業を止めたり、未レビューの変更を本番に出しかけたりする危険がある。 | `c1_direct_push_can_stop_team`、`c1_direct_push_unreviewed_release` | [決定論] |
| C2 | 直接 push は今月はまだ仕組みで止められないので、一人ひとりが流れを守る必要がある。 | `c2_only_self_stops_this_month` | [決定論] |
| C3 | この流れ（承認のあとに commit を足したら、もう一度レビューを頼むことを含む）を自分が守るかぎり、自分が main に入れる変更はすべて、マージ前にほかの人のレビューと承認を通る。 | `c3_own_changes_approved_by_other`（承認の項）、`c3_own_changes_reviewed_by_other`（レビューの項）（補題 `flow_changes_main_only_by_merge`、印なし） | [決定論] |
| C4 | コンフリクト（同じ箇所の変更の衝突）が起きなければ、社内の決まりに沿った手順で、新人でも最初から最後まで自分で進められる。 | `c4_flow_follows_rules`、`c4_newcomer_can_do_own_steps` | [決定論] |
| C5 | 来月、仕組みで直接 push が拒否されるようになっても、この流れを知っておく必要がある。 | `c5_only_pr_route_when_protected` | [決定論] |
| （C3 の限界） | 最後の承認のあとに push した変更は、古い承認のままマージすると、承認した人に見られないまま main に入る | `u1_push_after_approval_unseen`（印なし） | [不利] |
| （C0・01-intent の限界） | 流れを守っても、全員の作業を止める変更が main に入りうる | `u2_reviewed_change_can_stop_team`（印なし） | [不利] |
| （C4 の限界） | マージまで進むには、ほかの人の承認が要る | `u3_merge_needs_another_person`（印なし） | [不利] |
| （C5 の限界） | 保護が入っても、保護を迂回できる人の直接 push は（その人にも効かせる設定がなければ）通る | `u4_bypasser_still_unblocked`（印なし） | [不利] |
| （C3 の限界） | 流れを守らない人の直接の書き込みで、承認を得たプルリクエストを通らない変更が main に入ったことがある（C3 は自分の変更にしか言えない） | `u5_nonfollower_unreviewed_entry`（印なし） | [不利] |

## 設計書（model-plan.md）との違い

この周でも残る違いだけを書く（差分の設計書 8節の指示）。

1. 関係公理 `bringing_enters_main`（【自明】「ある操作で変更を main に入れたなら、その変更は main に入っている」）を足した。
   設計書の `main_feeds_release`・`broken_main_stops_team` は「main に入った変更」（`entersMain`）についての公理だが、
   それを使う定理（C1 の2つ目・C2・U2）は「直接書き込んだ」「squash merge で入れた」（`bringsInVia`）から出発する。
   設計書には `bringsInVia` から `entersMain` への向きの公理がなく、それがないと定理を示せない。
   `bringsInVia` の意味（その操作で、その変更を main に入れる）から、語の定義として言えるので【自明】にした。
2. `merge_content_origin` に、前提「`q` がそのプルリクエストを承認した」（`approvedBy pr q`）を足した。
   「最後の承認の時点」は、承認した人がいて初めて決まるため。公理は設計書の文より弱くなる（前提が増える）。
3. 帰納型に `deriving DecidableEq` を付けた（`teamFlow` に含まれるかどうかを `decide` で確かめるためと、証人の証明のため）。
4. 支える事実のない【仮定】4つの `@confidence` を、設計書の案より下げて 0.05 にした。
   `approver_not_author`（案 0.8）、`approved_change_can_break`（案 0.5）、`newcomer_can_commit`（案 0.6）、`recipe_doable`（案 0.5）。
   証拠のない【仮定】は、案によらず CLI の値が 0.05 になるため、案も 0.05 と書く決まりに合わせた。命題と型は変えていない。計算した確信度も変わらない。
5. 証人（`Model.lean`）に、差分の設計書8節にない例を足した。今月、人 3 が変更 4 を直接 push しようとし、拒否されずに main に直接書き込む。
   1周目の証人では `triesDirectPush` が先月にしかなく、C2 の定理の前提が一度も成り立たなかったため。あわせて `doesOp` を、`bringsInVia` の各場合と人 1 の承認に合わせて並べた。
-/

namespace GitBranchRules

-- 公理で宣言した関数に依存する定義は実行できないので、すべて計算不能として扱う
noncomputable section

/-! ## §1 帰納型（定義） -/

/-- 文書が扱う時期（先月・今月・来月）。 -/
inductive Month where
  | lastMonth
  | thisMonth
  | nextMonth
  deriving DecidableEq

/-- 文書が扱う操作の語彙。
`updateMain` は `git switch main` と `git pull`、`createBranch` は `git switch -c`、`commitOnBranch` は作業ブランチへの commit、
`pushBranch` は `git push -u origin <ブランチ名>`、`openPR` はプルリクエストを作ること、`requestReview` はレビューする人の指定、
`pushFix` は指摘に応える commit を同じブランチへ push すること、`approve` はレビューする人の承認、`squashMerge` は squash merge、
`otherMerge` は squash 以外の方法でのマージ、`directWriteMain` は main への直接の書き込み
（プルリクエストのマージによらずに main の中身を変える書き込みすべて。push、GitHub の画面での直接編集、API など、手段を問わない）。
main を変える手段がこの語彙に尽きるのは、直接の書き込みを「マージ以外のすべて」と定義したことによる（語の定義）。 -/
inductive Op where
  | updateMain
  | createBranch
  | commitOnBranch
  | pushBranch
  | openPR
  | requestReview
  | pushFix
  | approve
  | squashMerge
  | otherMerge
  | directWriteMain
  deriving DecidableEq

/-- ブランチ名の頭。`other` は決まりにない名前。 -/
inductive BranchPrefix where
  | feature
  | fix
  | other
  deriving DecidableEq

/-- 作業の種類（新しい機能か、不具合の修正か）。 -/
inductive WorkKind where
  | newFeature
  | bugFix
  deriving DecidableEq

/-- マージの方法。 -/
inductive MergeMethod where
  | squash
  | mergeCommit
  | rebase
  deriving DecidableEq

/-- マージする人（プルリクエストを出した本人か、ほかの人か）。 -/
inductive Merger where
  | prAuthor
  | someoneElse
  deriving DecidableEq

/-! ## §2 宣言（中身を決めない型・関数・定数） -/

/-- チームの人。新人、レビューする人、管理者を含む。main に書き込む自動の仕組み（ボットなど）があれば、それも含む。 -/
axiom Person : Type

/-- main に入りうる変更（commit の中身）。 -/
axiom Change : Type

/-- プルリクエスト。 -/
axiom PR : Type

/-- この文書の読者（今年入社の新人）。 -/
axiom newcomer : Person

/-- その人は、ブランチ保護の制限を受けない立場にある（リポジトリの管理者の権限か、保護を迂回する権限を持つ役割）。 -/
axiom bypassesProtection : Person → Prop

/-- その人がリポジトリに push できる権限を持っている。 -/
axiom canWrite : Person → Prop

/-- そのプルリクエストを出した人。 -/
axiom author : PR → Person

/-- その月、その人がその操作をする。 -/
axiom doesOp : Month → Person → Op → Prop

/-- その月、その人がその操作で、その変更を GitHub の main に入れる。 -/
axiom bringsInVia : Month → Person → Op → Change → Prop

/-- その月、その変更が main に入る（誰の操作かは問わない）。 -/
axiom entersMain : Month → Change → Prop

/-- その操作は、GitHub の main の中身を変える。 -/
axiom changesMain : Op → Prop

/-- その月、その人がその変更を main に直接 push しようとする。 -/
axiom triesDirectPush : Month → Person → Change → Prop

/-- その月、その人の main への直接 push を GitHub が拒否する。
設定の水準の述語。手元の main が古いときに GitHub が fast-forward でない push を断るような、1回ごとの拒否は含まない。 -/
axiom pushRejected : Month → Person → Prop

/-- その月、main への直接 push を拒否する設定が GitHub に入っている（どの設定かは問わない）。 -/
axiom directPushBlocked : Month → Prop

/-- その月、main のブランチ保護で「Require a pull request before merging」が、必要な承認数1以上で有効になっている。 -/
axiom protectedMain : Month → Prop

/-- その月の保護の設定が、迂回できる立場の人にも効くようになっている。 -/
axiom bypassDisallowed : Month → Prop

/-- その月、その人がそのプルリクエストを squash merge する。 -/
axiom squashMerges : Month → Person → PR → Prop

/-- マージの時点で、その変更がそのプルリクエストに入っている。 -/
axiom inPRAtMerge : Change → PR → Prop

/-- マージの前に、その人がそのプルリクエストを1回以上承認した。 -/
axiom approvedBy : PR → Person → Prop

/-- その人の、マージ前の最後の承認の時点で、その変更がプルリクエストに入っていた。 -/
axiom inPRWhenApproved : Change → PR → Person → Prop

/-- その人の、マージ前の最後の承認のあとに、その変更がプルリクエストのブランチに push された。 -/
axiom pushedAfterApproval : Change → PR → Person → Prop

/-- その人が、その変更を見たうえで承認した。 -/
axiom reviewedBy : Change → Person → Prop

/-- その変更は、承認を得たプルリクエストを通って main に入った。 -/
axiom viaApprovedPR : Change → Prop

/-- その変更は、main 以外のブランチ（作業ブランチ）から出したプルリクエストで入った。 -/
axiom fromWorkBranch : Change → Prop

/-- その変更で、main のビルドが壊れる。 -/
axiom breaksBuild : Change → Prop

/-- その変更のせいで、チーム全員の作業が止まる。 -/
axiom stopsTeam : Change → Prop

/-- その変更が、次のリリースで本番に出る候補になる。 -/
axiom releaseCandidate : Change → Prop

/-- その操作を行う、決まった短いコマンドか画面の操作がある。 -/
axiom hasFixedRecipe : Op → Prop

/-- 新人が、その操作を自分で行える。 -/
axiom canDo : Op → Prop

/-- 作業のあいだにコンフリクトが起きない（C4 の条件）。 -/
axiom noConflict : Prop

/-- 社内の決まりで、マージに必要な承認の最少人数。 -/
axiom ruleMinApprovals : Nat

/-- 社内の決まりのマージの方法。 -/
axiom ruleMergeMethod : MergeMethod

/-- 社内の決まりでマージする人。 -/
axiom ruleMerger : Merger

/-- 社内の決まりで、そのブランチ名の頭を使ってよい。 -/
axiom ruleAllowsPrefix : BranchPrefix → Prop

/-! ## §3 計算の def（手順だけ。判断を入れない） -/

/-- 文書が勧める操作の一覧。`pushFix` は指摘があったときだけ行う。
モデルでは「流れの中で使ってよい操作」として、含まれるかどうかだけを使う（順序は `FollowsFlow` の条件で表す）。 -/
def teamFlow : List Op :=
  [.updateMain, .createBranch, .commitOnBranch, .pushBranch, .openPR, .requestReview, .pushFix, .approve, .squashMerge]

/-- 文書の指示で、その操作をプルリクエストを出した本人が行うか。`approve` だけはレビューする人が行う。 -/
def doneByAuthor : Op → Bool
  | .approve => false
  | _ => true

/-- 文書が指示するブランチ名の頭。 -/
def flowPrefix : WorkKind → BranchPrefix
  | .newFeature => .feature
  | .bugFix => .fix

/-- 文書が指示するマージの方法。 -/
def flowMergeMethod : MergeMethod := .squash

/-- 文書が指示するマージする人。 -/
def flowMerger : Merger := .prAuthor

/-- 文書が指示する承認の最少人数。 -/
def flowMinApprovals : Nat := 1

/-- 略記: その月、その人がその変更を main に直接書き込む。 -/
def directlyWrites (m : Month) (p : Person) (c : Change) : Prop :=
  bringsInVia m p .directWriteMain c

/-- 文書の言う「その月に流れを守る」。その月について、次の3つを満たすこと。
(a) する操作はすべて `teamFlow` に含まれる（main への直接の書き込みも、squash 以外のマージもしない）。
(b) squash merge するのは、自分が出したプルリクエストだけ。
(c) squash merge するプルリクエストには、承認した人 `q` がいて、`q` の最後の承認のあとに push された変更がない
（承認のあとに commit を足したら、もう一度レビューを頼み、承認を受け直してからマージする）。 -/
def FollowsFlow (m : Month) (p : Person) : Prop :=
  (∀ o, doesOp m p o → o ∈ teamFlow) ∧
  (∀ pr, squashMerges m p pr → author pr = p) ∧
  (∀ pr, squashMerges m p pr → ∃ q, approvedBy pr q ∧ ∀ c, ¬ pushedAfterApproval c pr q)

/-! ## §4 関係公理 -/

/-! ### C1・C2: 直接 push の危険 -/

/-- 【実験】先月、main に直接書き込まれ、チーム全員の作業を止めた変更がある。
@support F1
論拠: 先月の1回目の事故で、main に直接 push した変更のために、半日チーム全員の作業が止まった（F1）。1件の事実から存在を言うだけで、一般化を含まない。
弱い点: 依頼者の証言だけで、社内の事故記録は確かめていない（F1）。 -/
axiom incident_direct_push_stopped_team : ∃ p c, directlyWrites .lastMonth p c ∧ stopsTeam c

/-- 【自明】main に直接書き込んだ変更は、承認を得たプルリクエストを通っていない。
論拠: 「直接の書き込み」とは、プルリクエストを通さずに main を変えること（語の定義）。 -/
axiom direct_write_skips_pr : ∀ m p c, directlyWrites m p c → ¬ viaApprovedPR c

/-- 【自明】ある操作で変更を main に入れたなら、その変更は main に入っている。
論拠: `bringsInVia` は「その操作で、その変更を main に入れる」、`entersMain` は「誰の操作かを問わず main に入る」で、前者から後者が語の定義として言える。 -/
axiom bringing_enters_main : ∀ m p o c, bringsInVia m p o c → entersMain m c

/-- 【経験則】main に入った変更は、次のリリースで本番に出る候補になる。
@support F2
@confidence 0.6
論拠: main は本番に出すもとになる。F2 では、main に入った未レビューの変更が本番に出かけた。
弱い点: 事例は1件（F2）。リリースの前に止める確認があれば本番には出ないが、候補になることは変わらない。 -/
axiom main_feeds_release : ∀ m c, entersMain m c → releaseCandidate c

/-- 【経験則】main に入った変更がビルドを壊すなら、チーム全員の作業が止まる。
@support F1
@confidence 0.6
論拠: main は全員の作業の土台。F1 ではビルドが壊れて半日全員が止まった。
弱い点: 事例は1件（F1）。main を取り込まずに作業している人は、すぐには止まらない。 -/
axiom broken_main_stops_team : ∀ m c, entersMain m c → breaksBuild c → stopsTeam c

/-- 【実験】今月は、誰の直接 push も GitHub に拒否されない。
@support F3
論拠: F3。
弱い点: 依頼者の証言（F3）。 -/
axiom no_rejection_this_month : ∀ p, ¬ pushRejected .thisMonth p

/-- 【経験則】直接 push しようとして、拒否されなければ、その変更は main に直接書き込まれる。
@support F1 F2
@confidence 0.6
論拠: 拒否されない push は受け入れられる。先月の直接 push は実際に main に入った（F1・F2）。
弱い点: 手元の main が古いと、GitHub が fast-forward でない push を断る（`git pull` のあとなら通る）。この拒否は、設定の水準の拒否（`pushRejected`）には入らない。 -/
axiom unrejected_push_lands : ∀ m p c, triesDirectPush m p c → ¬ pushRejected m p → directlyWrites m p c

/-! ### C3: 流れを守れば、自分が main に入れる変更はレビューと承認を通る -/

/-- 【自明】ある操作で変更を main に入れたなら、その人はその操作をしている。
論拠: 語の定義（「操作で入れた」なら、その操作をしている）。 -/
axiom bringing_needs_doing : ∀ m p o c, bringsInVia m p o c → doesOp m p o

/-- 【自明】変更を main に入れた操作は、main の中身を変える操作である。
論拠: 語の定義（「操作で main に入れた」なら、その操作は main を変えている）。 -/
axiom bringing_changes_main : ∀ m p o c, bringsInVia m p o c → changesMain o

/-- 【自明】`git switch main` と `git pull` は、GitHub の main を変えない。
論拠: `git pull` は GitHub から取り込む操作で、GitHub に送る手順を含まない（コマンドの定義）。 -/
axiom update_main_keeps_main : ¬ changesMain .updateMain

/-- 【自明】`git switch -c` でブランチを作っても、GitHub の main は変わらない。
論拠: `git switch -c` は手元でブランチを作るだけで、GitHub に何も送らない。 -/
axiom create_branch_keeps_main : ¬ changesMain .createBranch

/-- 【実験】作業ブランチへの commit は、main を変えない。
@support F5
論拠: F5 で、作業ブランチに commit しても main の中身が変わらないことを実行して確かめた。
弱い点: 手元での確認（F5）。まちがえて main の上で commit すると成り立たない（その後の push は `directWriteMain` にあたる）。 -/
axiom commit_keeps_main : ¬ changesMain .commitOnBranch

/-- 【経験則】作業ブランチを push しても、GitHub の main は変わらない。
@support F5 F13
@confidence 0.9
論拠: `git push -u origin <ブランチ名>` は同じ名前のブランチを作る（F13）ので、main には書き込まない。
弱い点: F13 は GitHub ではなく手元のリモートで確かめた。 -/
axiom push_branch_keeps_main : ¬ changesMain .pushBranch

/-- 【実験】プルリクエストを作っても、main は変わらない。
@support F6
論拠: プルリクエストは、マージするよう「提案する」機能で、マージは別に行う（F6）。 -/
axiom open_pr_keeps_main : ¬ changesMain .openPR

/-- 【自明】レビューを依頼しても、main は変わらない。
論拠: レビューする人を指定するだけの操作。 -/
axiom request_review_keeps_main : ¬ changesMain .requestReview

/-- 【経験則】指摘に応える commit を同じブランチに push しても、main は変わらない。
@support F8 F13
@confidence 0.9
論拠: 同じブランチへの push はプルリクエストに加わる（F8）。送り先は作業ブランチ（F13）。
弱い点: 送り先をまちがえて main にすると成り立たない（それは `directWriteMain` にあたる）。 -/
axiom push_fix_keeps_main : ¬ changesMain .pushFix

/-- 【経験則】承認しても、main は変わらない（マージは別の操作）。
@support F6
@confidence 0.8
論拠: プルリクエストでは、レビューとマージは別の段階（F6）。
弱い点: 自動マージ（auto-merge）を有効にしていると、承認がマージのきっかけになる。 -/
axiom approve_keeps_main : ¬ changesMain .approve

/-- 【実験】squash merge で main に入る変更は、そのとき squash merge したプルリクエストに入っていた変更である。
@support F12
論拠: squash merge は、プルリクエストの commit を1つにまとめて取り込み先に加える（F12）。 -/
axiom squash_content_from_pr : ∀ m p c, bringsInVia m p .squashMerge c → ∃ pr, squashMerges m p pr ∧ inPRAtMerge c pr

/-- 【経験則】マージの時点でプルリクエストに入っている変更は、そのプルリクエストを承認した人の最後の承認の時点で入っていたか、最後の承認のあとに push されたかのどちらか。
@support F6 F8
@confidence 0.8
論拠: プルリクエストの中身はブランチの commit で（F6）、ブランチに push した commit は自動で加わる（F8）。
弱い点: 画面の「Update branch」や、レビューする人の提案を画面で取り込む commit も、最後の承認のあとに中身を変える。これらを push とみなせば成り立つ。 -/
axiom merge_content_origin : ∀ c pr q, inPRAtMerge c pr → approvedBy pr q → inPRWhenApproved c pr q ∨ pushedAfterApproval c pr q

/-- 【経験則】承認した人の最後の承認の時点でプルリクエストに入っていた変更は、その人が見たうえで承認している。
@support F6
@confidence 0.05
@reviewer 0.05 ← 0.7 理由: F6 が述べるのは「プルリクエストは、マージの前に変更を話し合い、レビューできる機能」ということだけで、承認した人が中身を見たうえで承認しているか（社内での承認の出し方）は述べていない。この公理が言う人の振る舞いを支える事実がない。
論拠: プルリクエストは、マージの前に変更を話し合い、レビューする機能（F6）で、承認はその中身に対して出す。
弱い点: 中身を読まずに承認することはありうる。社内で承認がどう出されているかは確かめていない。F6 は、プルリクエストがレビューのための機能であることを述べるだけで、承認する人の振る舞いは述べていない（F6）。
要ファクト: 社内で、プルリクエストを承認する人が、差分（変更の中身）を読んでから承認しているかを、ユーザーに確かめる。承認のあとに足された commit を、頼み直したレビューで読んでいるかも含む。 -/
axiom approval_covers_content : ∀ c pr q, approvedBy pr q → inPRWhenApproved c pr q → reviewedBy c q

/-- 【仮定】プルリクエストを承認した人は、それを出した本人ではない。
@support なし（本人が自分のプルリクエストを承認できないことを確かめた事実が、まだない）
@confidence 0.05
論拠: 「ほかの人のレビュー」の「ほかの人」を支える。
弱い点: 事実がまだない。
要ファクト: GitHub では、プルリクエストを出した本人が自分のプルリクエストを承認できないことを GitHub Docs で確かめる。 -/
axiom approver_not_author : ∀ pr q, approvedBy pr q → q ≠ author pr

/-! ### U1: 承認のあとの push（不利な結論のため） -/

/-- 【実験】最後の承認のあとに push された変更も、マージの時点でプルリクエストに入っている。
@support F8
論拠: プルリクエストを出したあとに同じブランチへ push した commit は、自動で加わる（F8）。
弱い点: いったん加わった commit を強制的な push で消すと、マージの時点には残らない。 -/
axiom push_joins_pr : ∀ c pr q, pushedAfterApproval c pr q → inPRAtMerge c pr

/-- 【実験】squash merge すると、マージの時点でプルリクエストに入っている変更は、すべて main に入る。
@support F12
論拠: squash merge は、プルリクエストの commit を1つにまとめて取り込み先に加える（F12）。 -/
axiom squash_brings_all_pr : ∀ m p pr c, squashMerges m p pr → inPRAtMerge c pr → bringsInVia m p .squashMerge c

/-- 【自明】ある人の最後の承認のあとに push された変更は、その人の最後の承認の時点ではプルリクエストに入っていなかった。
論拠: 最後の承認のあとに加わったものは、その承認の時点ではまだない（時の前後の定義）。 -/
axiom pushed_after_not_seen : ∀ c pr q, pushedAfterApproval c pr q → ¬ inPRWhenApproved c pr q

/-! ### U2: 流れを守っても壊れうる（不利な結論のため） -/

/-- 【仮定】承認を得たプルリクエストの squash merge で main に入り、ビルドを壊す変更がある。
@support なし（社内で、承認を受けてマージした変更がビルドを壊した記録が、まだない）
@confidence 0.05
論拠: レビューは人が読むもので、見落としがありうる。
弱い点: 社内の事例がまだない。
要ファクト: 社内で、承認を受けてマージした変更で main のビルドが壊れたことがあるかを、ユーザーに確かめる。 -/
axiom approved_change_can_break : ∃ m p c, bringsInVia m p .squashMerge c ∧ viaApprovedPR c ∧ breaksBuild c

/-! ### C4: 社内の決まりに沿うこと -/

/-- 【実験】マージに必要な承認の最少人数は1人。
@support F7
論拠: 依頼者の証言した社内の決まり（F7）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F7）。 -/
axiom rule_min_approvals : ruleMinApprovals = 1

/-- 【実験】社内のマージの方法は squash merge。
@support F11
論拠: 依頼者の証言した社内の決まり（F11）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F11）。 -/
axiom rule_merge_method : ruleMergeMethod = .squash

/-- 【実験】社内でマージするのは、プルリクエストを出した本人。
@support F11
論拠: 依頼者の証言した社内の決まり（F11）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F11）。 -/
axiom rule_merger : ruleMerger = .prAuthor

/-- 【実験】ブランチ名の頭に `feature` を使ってよい。
@support F9
論拠: 依頼者の証言した社内の決まり（F9）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F9）。 -/
axiom rule_prefix_feature : ruleAllowsPrefix .feature

/-- 【実験】ブランチ名の頭に `fix` を使ってよい。
@support F9
論拠: 依頼者の証言した社内の決まり（F9）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F9）。 -/
axiom rule_prefix_fix : ruleAllowsPrefix .fix

/-! ### C4: 新人が自分で進められること -/

/-- 【実験】手元の main を最新にする、決まった操作（`git switch main` と `git pull`）がある。
@support F15
論拠: 実行して確かめた（F15）。
弱い点: GitHub ではなく手元のリモートで確かめた（F15）。 -/
axiom recipe_update_main : hasFixedRecipe .updateMain

/-- 【実験】ブランチを作って移る、決まった操作（`git switch -c`）がある。
@support F10
論拠: 実行して確かめた（F10）。
弱い点: git 2.23 より古い git にはこのコマンドがない。 -/
axiom recipe_create_branch : hasFixedRecipe .createBranch

/-- 【実験】作業ブランチを GitHub に送る、決まった操作（`git push -u origin <ブランチ名>`）がある。
@support F13
論拠: 実行して確かめた（F13）。
弱い点: GitHub ではなく手元のリモートで確かめた（F13）。GitHub への認証の手間は含まない。 -/
axiom recipe_push_branch : hasFixedRecipe .pushBranch

/-- 【実験】push したブランチからプルリクエストを作る、決まった画面の操作がある。
@support F14
論拠: GitHub Docs（F14）。 -/
axiom recipe_open_pr : hasFixedRecipe .openPR

/-- 【実験】レビューする人（Reviewers）を指定する、決まった画面の操作がある。
@support F14
論拠: GitHub Docs（F14）。 -/
axiom recipe_request_review : hasFixedRecipe .requestReview

/-- 【実験】指摘に応える commit を同じブランチに送る、決まった操作（commit と push）がある。
@support F8
論拠: 同じブランチに push すればプルリクエストに加わる（GitHub Docs、F8）。操作そのものは commit と push で、新人が知っている。 -/
axiom recipe_push_fix : hasFixedRecipe .pushFix

/-- 【実験】squash merge する、決まった画面の操作（「Squash and merge」）がある。
@support F12
論拠: GitHub Docs（F12）。画面のボタンは「Squash and merge」。
弱い点: ボタンを押せるかはリポジトリの権限による。 -/
axiom recipe_squash_merge : hasFixedRecipe .squashMerge

/-- 【仮定】新人は、作業ブランチに自分で commit できる。
@support なし（読者像に書いてあるだけで、事実として登録されていない）
@confidence 0.05
論拠: 03-reader.json に「Git で commit と push はできる」とある。
弱い点: 06-facts.json に事実として登録されていないので、`@support` にできない。
要ファクト: 03-reader.json の「新人は Git で commit と push ができる」を、ユーザーの証言として 06-facts.json に登録する。 -/
axiom newcomer_can_commit : canDo .commitOnBranch

/-- 【経験則】新人は、リポジトリに push できる権限を持っている。
@support F1 F2
@confidence 0.6
論拠: 先月、新人が main に直接 push できた（F1・F2）ので、新人には push の権限がある。
弱い点: 先月の新人と、今年の読者が同じ権限とは限らない（F1・F2）。 -/
axiom newcomer_can_write : canWrite newcomer

/-- 【仮定】決まった短い操作がある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える。
@support なし（新人が文書の手順どおりに進めた記録が、まだない）
@confidence 0.05
論拠: 1つずつの操作は、決まったコマンドか画面の操作で済む。文書は、流れの各操作を、その決まった操作で説明する。
弱い点: 新人に実際に通してもらった記録がない。ブランチ・プルリクエスト・マージ・レビューは読者の知らない語（03-reader.json）なので、本文での説明の出来に左右される。
要ファクト: 新人（または同じくらいの経験の人）に、文書の手順どおりにプルリクエストを1本通してもらい、詰まった操作を記録する。 -/
axiom recipe_doable : ∀ o, hasFixedRecipe o → doneByAuthor o = true → canWrite newcomer → noConflict → canDo o

/-! ### C5: 保護が入ったあとの経路 -/

/-- 【実験】保護が有効な月は、保護を迂回できない人の直接 push は拒否される。
@support F4
@confidence 0.75
@reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人は、だれでも拒否される」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
弱い点: 初期設定では、管理者などには効かない（F4）。その人たちは、迂回できる立場として前提で除いてある。 -/
axiom protection_rejects_push : ∀ m p, protectedMain m → ¬ bypassesProtection p → pushRejected m p

/-- 【実験】保護が有効な月に、保護を迂回できない人が main に入れる変更は、承認を得たプルリクエストを通ったものだけ。
@support F4
@confidence 0.75
@reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人が入れる変更は、どれも承認を得たプルリクエストを通る」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
弱い点: 初期設定では、管理者などには効かない（F4）。その人たちは、迂回できる立場として前提で除いてある。 -/
axiom protection_only_approved_pr : ∀ m p o c, protectedMain m → ¬ bypassesProtection p → bringsInVia m p o c → viaApprovedPR c

/-- 【実験】承認を得たプルリクエストで入った変更は、main 以外のブランチから出したプルリクエストで入っている。
@support F6
論拠: プルリクエストは、異なる2つのブランチの間でしか作れない（F6 の出典の引用）。 -/
axiom pr_needs_work_branch : ∀ c, viaApprovedPR c → fromWorkBranch c

/-- 【仮定】新人は、保護を迂回できる立場にない（管理者の権限も、迂回の権限も持たない）。
@support なし（新人のリポジトリでの役割を確かめた事実が、まだない）
@confidence 0.05
論拠: 新人に、管理者の権限や、保護を迂回する権限を渡すことは、ふつうない。
弱い点: 事実がまだない。
要ファクト: 新人のリポジトリでの役割（権限）が、管理者でも、保護を迂回できる役割でもないことを、ユーザーに確かめる。 -/
axiom newcomer_no_bypass : ¬ bypassesProtection newcomer

/-- 【仮定】来月、直接 push を拒否する設定が入るなら、それは承認1名以上のプルリクエストを必須にする保護である。
@support なし（F3 は「直接 push を拒否する設定に来月変える予定」と述べるだけで、どの設定を入れるか、必要な承認数をいくつにするかは述べていない。F7 は社内の決まりで、GitHub の設定ではない）
@confidence 0.05
論拠: main への直接 push を止める設定としてふつう使うのは、マージの前にプルリクエストを必須にする保護で、社内の決まり（承認1名以上）とも合う。
弱い点: 承認を求めずに直接 push だけを止める設定（承認数 0 や、push できる人を限る設定など）もありうる。その場合、C5 の結論は「承認を得たプルリクエストだけ」ではなく「プルリクエストを通ったものだけ」に弱まる。
要ファクト: 来月 main に入れる設定が「Require a pull request before merging」か、必要な承認数を1以上にするかを、ユーザーに確かめる。 -/
axiom next_month_block_requires_pr : directPushBlocked .nextMonth → protectedMain .nextMonth

/-! ### U4: 保護を迂回できる人は来月も止まらない（不利な結論のため） -/

/-- 【実験】保護の設定が迂回できる立場の人にも効くようになっていなければ、その人の直接 push は拒否されない。
@support F4
論拠: 初期設定では、保護の制限は、リポジトリの管理者の権限を持つ人に効かない（F4）。迂回の権限を持つ役割は、その権限の意味から、制限を受けない。
弱い点: F4 の引用が直接述べるのは、管理者の権限を持つ人だけである。迂回の権限を持つ役割は、F4 の「管理者など」に含めて読んでいる（F4）。 -/
axiom bypass_exempt_by_default : ∀ m p, bypassesProtection p → ¬ bypassDisallowed m → ¬ pushRejected m p

/-! ## §5 主張の定理 -/

/-! ### C1 -/

/-- @claim C1 [決定論] main への直接の書き込みで、チーム全員の作業が止まることがある（先月、実際に起きた）。
@restates incident_direct_push_stopped_team 理由: C1 の「全員の作業を止める危険がある」は、F1 の事故1件がそのまま示す（危険があることは、起きたことが1回あれば言える）。1周目の M6 で、1件の事例からの全称（`broken_main_stops_team`）を通さず、事実から直接示すよう求めた結果の形で、言い換えであることは意図どおり。値は F1（user_asserted）で決まる。 -/
theorem c1_direct_push_can_stop_team : ∃ m p c, directlyWrites m p c ∧ stopsTeam c := by
  obtain ⟨p, c, hw, hs⟩ := incident_direct_push_stopped_team
  exact ⟨.lastMonth, p, c, hw, hs⟩

/-- @claim C1 [決定論] main に直接書き込んだ変更は、承認を得たプルリクエストを通らないまま、本番に出る候補になる。 -/
theorem c1_direct_push_unreviewed_release :
    ∀ m p c, directlyWrites m p c → ¬ viaApprovedPR c ∧ releaseCandidate c := by
  intro m p c hw
  exact ⟨direct_write_skips_pr m p c hw, main_feeds_release m c (bringing_enters_main _ _ _ _ hw)⟩

/-! ### C2 -/

/-- @claim C2 [決定論] 今月、main に直接 push しようとすれば、何にも止められずに main に入り、
承認を得たプルリクエストを通らないまま本番の候補になり、ビルドを壊すならチーム全員を止める。止めるのは本人がしないことだけ。 -/
theorem c2_only_self_stops_this_month :
    ∀ p c, triesDirectPush .thisMonth p c →
      directlyWrites .thisMonth p c ∧ ¬ viaApprovedPR c ∧ releaseCandidate c ∧ (breaksBuild c → stopsTeam c) := by
  intro p c ht
  have hw : directlyWrites .thisMonth p c := unrejected_push_lands .thisMonth p c ht (no_rejection_this_month p)
  have he : entersMain .thisMonth c := bringing_enters_main _ _ _ _ hw
  exact ⟨hw, direct_write_skips_pr _ _ _ hw, main_feeds_release _ _ he, broken_main_stops_team _ _ he⟩

/-! ### C3 -/

/-- [決定論] 補題: 流れの操作のうち main を変えるのは squash merge だけ。 -/
theorem flow_changes_main_only_by_merge :
    ∀ o, o ∈ teamFlow → changesMain o → o = .squashMerge := by
  intro o hmem hch
  simp only [teamFlow, List.mem_cons, List.not_mem_nil, or_false] at hmem
  rcases hmem with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact absurd hch update_main_keeps_main
  · exact absurd hch create_branch_keeps_main
  · exact absurd hch commit_keeps_main
  · exact absurd hch push_branch_keeps_main
  · exact absurd hch open_pr_keeps_main
  · exact absurd hch request_review_keeps_main
  · exact absurd hch push_fix_keeps_main
  · exact absurd hch approve_keeps_main
  · rfl

/-- @claim C3 [決定論] その月に流れを守る人が、その月に main に入れる変更は、どれも、その人が squash merge したプルリクエストに入っていて、
その人とは別の人が承認していて、その別の人の最後の承認の時点で、その変更はプルリクエストに入っていた（C3 の「ほかの人の承認を通る」）。 -/
theorem c3_own_changes_approved_by_other :
    ∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
      ∃ pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ inPRWhenApproved c pr q := by
  intro m p hflow o c hb
  obtain ⟨hops, hauth, happ⟩ := hflow
  have hmem : o ∈ teamFlow := hops o (bringing_needs_doing m p o c hb)
  have ho : o = .squashMerge := flow_changes_main_only_by_merge o hmem (bringing_changes_main m p o c hb)
  subst ho
  obtain ⟨pr, hsq, hin⟩ := squash_content_from_pr m p c hb
  obtain ⟨q, hq, hfresh⟩ := happ pr hsq
  have hseen : inPRWhenApproved c pr q := by
    rcases merge_content_origin c pr q hin hq with h | h
    · exact h
    · exact absurd h (hfresh c)
  refine ⟨pr, q, hsq, hin, hq, ?_, hseen⟩
  intro hqp
  exact approver_not_author pr q hq (hqp.trans (hauth pr hsq).symm)

/-- @claim C3 [決定論] その月に流れを守る人が、その月に main に入れる変更は、どれも、その人が squash merge したプルリクエストを
その人とは別の人が承認していて、その別の人がその変更を見たうえで承認している（C3 の「ほかの人のレビューを通る」）。 -/
theorem c3_own_changes_reviewed_by_other :
    ∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
      ∃ pr q, squashMerges m p pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q := by
  intro m p hflow o c hb
  obtain ⟨pr, q, hsq, _, hq, hne, hseen⟩ := c3_own_changes_approved_by_other m p hflow o c hb
  exact ⟨pr, q, hsq, hq, hne, approval_covers_content c pr q hq hseen⟩

/-! ### C4 -/

/-- @claim C4 [決定論] 文書の手順は、社内の決まり（承認の人数・マージの方法・マージする人・ブランチ名の頭）に沿う。 -/
theorem c4_flow_follows_rules :
    ruleMinApprovals ≤ flowMinApprovals ∧ flowMergeMethod = ruleMergeMethod ∧ flowMerger = ruleMerger ∧
      ∀ k, ruleAllowsPrefix (flowPrefix k) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [rule_min_approvals]
    exact Nat.le_refl _
  · rw [rule_merge_method]
    rfl
  · rw [rule_merger]
    rfl
  · intro k
    cases k
    · exact rule_prefix_feature
    · exact rule_prefix_fix

/-- @claim C4 [決定論] コンフリクトが起きなければ、流れの操作のうち本人が行うものは、すべて新人が自分で行える。 -/
theorem c4_newcomer_can_do_own_steps :
    noConflict → ∀ o, o ∈ teamFlow → doneByAuthor o = true → canDo o := by
  intro hnc o hmem hown
  simp only [teamFlow, List.mem_cons, List.not_mem_nil, or_false] at hmem
  rcases hmem with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact recipe_doable _ recipe_update_main hown newcomer_can_write hnc
  · exact recipe_doable _ recipe_create_branch hown newcomer_can_write hnc
  · exact newcomer_can_commit
  · exact recipe_doable _ recipe_push_branch hown newcomer_can_write hnc
  · exact recipe_doable _ recipe_open_pr hown newcomer_can_write hnc
  · exact recipe_doable _ recipe_request_review hown newcomer_can_write hnc
  · exact recipe_doable _ recipe_push_fix hown newcomer_can_write hnc
  · exact absurd hown (by decide)
  · exact recipe_doable _ recipe_squash_merge hown newcomer_can_write hnc

/-! ### C5 -/

/-- @claim C5 [決定論] 来月、main への直接 push を拒否する設定が入れば、新人の直接 push は拒否され、新人が main に入れられる変更は、
作業ブランチから出して承認を得たプルリクエストを通ったものだけになる。 -/
theorem c5_only_pr_route_when_protected :
    directPushBlocked .nextMonth →
      pushRejected .nextMonth newcomer ∧
        ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c := by
  intro hblock
  have hprot : protectedMain .nextMonth := next_month_block_requires_pr hblock
  refine ⟨protection_rejects_push _ _ hprot newcomer_no_bypass, ?_⟩
  intro o c hb
  have hv : viaApprovedPR c := protection_only_approved_pr _ _ _ _ hprot newcomer_no_bypass hb
  exact ⟨hv, pr_needs_work_branch c hv⟩

/-! ### C0 -/

/-- @claim C0 [決定論] 文書の手順は main への直接の書き込みを含まず、C1〜C5 の性質をすべて持つ。 -/
theorem c0_team_flow :
    Op.directWriteMain ∉ teamFlow ∧
    (∃ m p c, directlyWrites m p c ∧ stopsTeam c) ∧
    (∀ m p c, directlyWrites m p c → ¬ viaApprovedPR c ∧ releaseCandidate c) ∧
    (∀ p c, triesDirectPush .thisMonth p c →
      directlyWrites .thisMonth p c ∧ ¬ viaApprovedPR c ∧ releaseCandidate c ∧ (breaksBuild c → stopsTeam c)) ∧
    (∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
      ∃ pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ inPRWhenApproved c pr q) ∧
    (∀ m p, FollowsFlow m p → ∀ o c, bringsInVia m p o c →
      ∃ pr q, squashMerges m p pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q) ∧
    (ruleMinApprovals ≤ flowMinApprovals ∧ flowMergeMethod = ruleMergeMethod ∧ flowMerger = ruleMerger ∧
      ∀ k, ruleAllowsPrefix (flowPrefix k)) ∧
    (noConflict → ∀ o, o ∈ teamFlow → doneByAuthor o = true → canDo o) ∧
    (directPushBlocked .nextMonth →
      pushRejected .nextMonth newcomer ∧
        ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c) :=
  ⟨by decide, c1_direct_push_can_stop_team, c1_direct_push_unreviewed_release, c2_only_self_stops_this_month,
    c3_own_changes_approved_by_other, c3_own_changes_reviewed_by_other, c4_flow_follows_rules,
    c4_newcomer_can_do_own_steps, c5_only_pr_route_when_protected⟩

/-! ### 不利な結論（主張にしない。印なし） -/

/-- [不利] 最後の承認のあとに push した変更は、そのプルリクエストを squash merge すると main に入るが、
承認した人の最後の承認の時点ではプルリクエストに入っていなかった。
レビューを頼み直しても、古い承認のままマージすれば、足した commit は承認を通らない。 -/
theorem u1_push_after_approval_unseen :
    ∀ m p pr q c, pushedAfterApproval c pr q → squashMerges m p pr →
      bringsInVia m p .squashMerge c ∧ ¬ inPRWhenApproved c pr q := by
  intro m p pr q c hpush hsq
  exact ⟨squash_brings_all_pr m p pr c hsq (push_joins_pr c pr q hpush), pushed_after_not_seen c pr q hpush⟩

/-- [不利] 承認を得たプルリクエストの squash merge で入った変更でも、チーム全員の作業を止めることがある。 -/
theorem u2_reviewed_change_can_stop_team :
    ∃ m p c, bringsInVia m p .squashMerge c ∧ viaApprovedPR c ∧ stopsTeam c := by
  obtain ⟨m, p, c, hb, hv, hbr⟩ := approved_change_can_break
  exact ⟨m, p, c, hb, hv, broken_main_stops_team m c (bringing_enters_main _ _ _ _ hb) hbr⟩

/-- [不利] 承認は本人が行う操作ではなく、その月に流れを守ってマージまで進むには、本人とは別の人の承認が要る。 -/
theorem u3_merge_needs_another_person :
    doneByAuthor .approve = false ∧
      ∀ m p pr, FollowsFlow m p → squashMerges m p pr → ∃ q, approvedBy pr q ∧ q ≠ p := by
  refine ⟨rfl, ?_⟩
  intro m p pr hflow hsq
  obtain ⟨_, hauth, happ⟩ := hflow
  obtain ⟨q, hq, _⟩ := happ pr hsq
  refine ⟨q, hq, ?_⟩
  intro hqp
  exact approver_not_author pr q hq (hqp.trans (hauth pr hsq).symm)

/-- [不利] 保護の設定が迂回できる立場の人にも効くようになっていなければ、その人が直接 push しようとした変更は、main に直接書き込まれる。 -/
theorem u4_bypasser_still_unblocked :
    ∀ m p c, bypassesProtection p → ¬ bypassDisallowed m → triesDirectPush m p c → directlyWrites m p c := by
  intro m p c hbyp hdis ht
  exact unrejected_push_lands m p c ht (bypass_exempt_by_default m p hbyp hdis)

/-- [不利] 流れを守らない人の直接の書き込みで、承認を得たプルリクエストを通らない変更が main に入ったことがある。
C3 は、自分が流れを守ることで自分の変更を守るだけで、ほかの人のこうした変更は防がない。 -/
theorem u5_nonfollower_unreviewed_entry :
    ∃ m p c, directlyWrites m p c ∧ ¬ viaApprovedPR c ∧ ¬ FollowsFlow m p := by
  obtain ⟨p, c, hw, _⟩ := incident_direct_push_stopped_team
  refine ⟨.lastMonth, p, c, hw, direct_write_skips_pr _ _ _ hw, ?_⟩
  intro hflow
  obtain ⟨hops, _, _⟩ := hflow
  have hmem : Op.directWriteMain ∈ teamFlow := hops _ (bringing_needs_doing _ _ _ _ hw)
  exact absurd hmem (by decide)

end

end GitBranchRules
