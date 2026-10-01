/-!
# 論証のモデル: 新人向け Gitブランチ運用ルール

設計書: `07-logic/model-plan.md`。主張: `05-claims.json`。事実: `06-facts.json`。

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
比較の文の主張はないので、すべて [決定論] で組む（設計書1節）。

| 主張 | 主張の文 | 定理 | 種類 |
|---|---|---|---|
| C0 | 変更は main に直接 push せず、作業ブランチを切り、プルリクエストを出し、1名以上の承認を受けてから、自分で squash merge して main に取り込む。 | `c0_team_flow` | [決定論] |
| C1 | main への直接 push は、チーム全員の作業を止めたり、未レビューの変更を本番に出しかけたりする危険がある。 | `c1_direct_push_can_stop_team`、`c1_direct_push_unreviewed_release` | [決定論] |
| C2 | 直接 push は今月はまだ仕組みで止められないので、一人ひとりが流れを守る必要がある。 | `c2_only_self_stops_this_month` | [決定論] |
| C3 | この流れを守るかぎり、main に入る変更はすべて、マージ前にほかの人のレビューと承認を通る。 | `c3_flow_reviews_every_entry`（補題 `flow_changes_main_only_by_merge`、印なし） | [決定論] |
| C4 | コンフリクト（同じ箇所の変更の衝突）が起きなければ、社内の決まりに沿った手順で、新人でも最初から最後まで自分で進められる。 | `c4_flow_follows_rules`、`c4_newcomer_can_do_own_steps` | [決定論] |
| C5 | 来月、仕組みで直接 push が拒否されるようになっても、この流れを知っておく必要がある。 | `c5_only_pr_route_when_protected` | [決定論] |
| （C3 の限界） | 承認のあとに push した変更は、承認した人に見られないまま main に入る | `u1_push_after_approval_unseen`（印なし） | [不利] |
| （C0・01-intent の限界） | 流れを守っても、全員の作業を止める変更が main に入りうる | `u2_reviewed_change_can_stop_team`（印なし） | [不利] |
| （C4 の限界） | マージまで進むには、ほかの人の承認が要る | `u3_merge_needs_another_person`（印なし） | [不利] |
| （C5 の限界） | 保護が入っても、管理者の直接 push は（管理者に効かせる設定がなければ）通る | `u4_admin_still_unblocked`（印なし） | [不利] |

## 設計書（model-plan.md）との違い

1. 関係公理 `bringing_enters_main`（【自明】「ある操作で変更を main に入れたなら、その変更は main に入っている」）を足した。
   設計書の `main_feeds_release`・`broken_main_stops_team` は「main に入った変更」（`entersMain`）についての公理だが、
   それを使う定理（C1・C2・U2）は「直接書き込んだ」「squash merge で入れた」（`bringsInVia`）から出発する。
   設計書には `entersMain` から `bringsInVia` への向き（`main_entry_has_op`）しかなく、逆の向きがないと定理を示せない。
   `bringsInVia` の意味（その操作で、その変更を main に入れる）から、語の定義として言えるので【自明】にした。
2. `merge_content_origin` に、前提「`q` がそのプルリクエストを承認した」（`approvedBy pr q`）を足した。
   「承認の時点」は、承認した人がいて初めて決まるため。公理は設計書の文より弱くなる（前提が増える）。
3. `u3_merge_needs_another_person` は、設計書の「あわせて `doneByAuthor .approve = false`」を、定理の結論の `∧` の1項目として入れた。
4. 帰納型に `deriving DecidableEq` を付けた（`teamFlow` に含まれるかどうかを `decide` で確かめるためと、証人の証明のため）。
5. 証人（`Model.lean`）の世界を、設計書5節の見通しと変えた。見通しでは `approvedBy`・`pushedAfterApproval`・`isAdmin`・`protectedMain` が
   いつも偽で、`merge_content_origin`・`approval_covers_content`・`approver_not_author`・U1 の3つの公理・`protection_rejects_push`・
   `admin_exempt_by_default` などの前提が一度も成り立たない（空回りする）。証人では、人を4人（新人・レビューする人・管理者・流れを守らない人）、
   プルリクエストを2本（承認のあとに push がないもの・あるもの）にし、来月だけ保護を有効にして、これらの前提が成り立つ例を持たせた。
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
`otherMerge` は squash 以外の方法でのマージ、`directWriteMain` は main への直接の書き込み（push と、GitHub の画面での直接編集の両方）。
この語彙で main を変える操作が尽きるという判断は、型には置かず、関係公理 `main_entry_has_op` に置く。 -/
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

/-- その人がリポジトリの管理者である。 -/
axiom isAdmin : Person → Prop

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

/-- その月、その人の main への直接 push を GitHub が拒否する。 -/
axiom pushRejected : Month → Person → Prop

/-- その月、main にブランチ保護（「Require a pull request before merging」）が有効になっている。 -/
axiom protectedMain : Month → Prop

/-- その月の保護の設定が、管理者にも効くようになっている。 -/
axiom protectionCoversAdmins : Month → Prop

/-- その月、その人がそのプルリクエストを squash merge する。 -/
axiom squashMerges : Month → Person → PR → Prop

/-- マージの時点で、その変更がそのプルリクエストに入っている。 -/
axiom inPRAtMerge : Change → PR → Prop

/-- マージの前に、その人がそのプルリクエストを承認した。 -/
axiom approvedBy : PR → Person → Prop

/-- その人が承認した時点で、その変更がプルリクエストに入っていた。 -/
axiom inPRWhenApproved : Change → PR → Person → Prop

/-- その人の承認のあとに、その変更がプルリクエストのブランチに push された。 -/
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

/-- その操作を行う決まったコマンドか画面の操作があり、その動きを確かめてある。 -/
axiom hasCheckedRecipe : Op → Prop

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

/-- 文書の言う「流れを守る」。次の3つを満たすこと。
(a) する操作はすべて `teamFlow` に含まれる（main への直接の書き込みも、squash 以外のマージもしない）。
(b) squash merge するのは、自分が出したプルリクエストだけ。
(c) squash merge するプルリクエストには、承認した人 `q` がいて、その承認のあとに push された変更がない
（承認のあとに push したら、承認を受け直してからマージする）。 -/
def FollowsFlow (p : Person) : Prop :=
  (∀ m o, doesOp m p o → o ∈ teamFlow) ∧
  (∀ m pr, squashMerges m p pr → author pr = p) ∧
  (∀ m pr, squashMerges m p pr → ∃ q, approvedBy pr q ∧ ∀ c, ¬ pushedAfterApproval c pr q)

/-! ## §4 関係公理 -/

/-! ### C1・C2: 直接 push の危険 -/

/-- 【実験】先月、main に直接書き込まれ、ビルドを壊した変更がある。
@support F1
論拠: 先月の1回目の事故（F1）。
弱い点: 依頼者の証言だけで、社内の事故記録は確かめていない（F1）。 -/
axiom incident_direct_push_broke_build : ∃ p c, directlyWrites .lastMonth p c ∧ breaksBuild c

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
弱い点: 手元の main が古いと、git が push を断る（`git pull` のあとなら通る）。 -/
axiom unrejected_push_lands : ∀ m p c, triesDirectPush m p c → ¬ pushRejected m p → directlyWrites m p c

/-! ### C3: 流れを守れば、main に入る変更はレビューを通る -/

/-- 【仮定】main に入る変更には、それを入れた人と、`Op` の語彙のどれかの操作がある。
@support なし（GitHub で main の中身を変える方法を並べた事実と、社内の自動の仕組みについての事実が、まだない）
@confidence 0.7
論拠: main の中身は、誰かが何かの操作をしたときにしか変わらない。`Op` は直接の書き込み・squash merge・それ以外のマージを含む。
弱い点: 語彙の外の操作（API での書き込みなど）が `directWriteMain` に入るかは、定義の広さによる。ボットが流れを守らずに main に書き込むなら、C3 の条件「全員が流れを守る」が成り立たない。
要ファクト: GitHub で main の中身を変える方法が、直接の書き込み（push・画面での直接編集）と、プルリクエストのマージ（squash とそれ以外）に尽きることを GitHub Docs で確かめる。あわせて、社内に main へ書き込む自動の仕組み（ボットなど）があるかをユーザーに確かめる。 -/
axiom main_entry_has_op : ∀ m c, entersMain m c → ∃ p o, bringsInVia m p o c

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

/-- 【経験則】マージの時点でプルリクエストに入っている変更は、そのプルリクエストを承認した人の承認の時点で入っていたか、承認のあとに push されたかのどちらか。
@support F6 F8
@confidence 0.8
論拠: プルリクエストの中身はブランチの commit で（F6）、ブランチに push した commit は自動で加わる（F8）。
弱い点: 画面の「Update branch」や、レビューする人の提案を画面で取り込む commit も、承認のあとに中身を変える。これらを push とみなせば成り立つ。 -/
axiom merge_content_origin : ∀ c pr q, inPRAtMerge c pr → approvedBy pr q → inPRWhenApproved c pr q ∨ pushedAfterApproval c pr q

/-- 【経験則】承認の時点でプルリクエストに入っていた変更は、承認した人が見たうえで承認している。
@support F6
@confidence 0.05
@reviewer 0.05 ← 0.7 理由: F6 が述べるのは「プルリクエストは、マージの前に変更を話し合い、レビューできる機能」ということだけで、承認した人が中身を見たうえで承認しているか（社内での承認の出し方）は述べていない。この公理が言う人の振る舞いを支える事実がない。
論拠: プルリクエストは、マージの前に変更を話し合い、レビューする機能（F6）で、承認はその中身に対して出す。
弱い点: 中身を読まずに承認することはありうる。社内で承認がどう出されているかは確かめていない。 -/
axiom approval_covers_content : ∀ c pr q, approvedBy pr q → inPRWhenApproved c pr q → reviewedBy c q

/-- 【仮定】プルリクエストを承認した人は、それを出した本人ではない。
@support なし（本人が自分のプルリクエストを承認できないことを確かめた事実が、まだない）
@confidence 0.8
論拠: 「ほかの人のレビュー」の「ほかの人」を支える。
弱い点: 事実がまだない。
要ファクト: GitHub では、プルリクエストを出した本人が自分のプルリクエストを承認できないことを GitHub Docs で確かめる。 -/
axiom approver_not_author : ∀ pr q, approvedBy pr q → q ≠ author pr

/-! ### U1: 承認のあとの push（不利な結論のため） -/

/-- 【実験】承認のあとに push された変更も、マージの時点でプルリクエストに入っている。
@support F8
論拠: プルリクエストを出したあとに同じブランチへ push した commit は、自動で加わる（F8）。
弱い点: いったん加わった commit を強制的な push で消すと、マージの時点には残らない。 -/
axiom push_joins_pr : ∀ c pr q, pushedAfterApproval c pr q → inPRAtMerge c pr

/-- 【実験】squash merge すると、マージの時点でプルリクエストに入っている変更は、すべて main に入る。
@support F12
論拠: squash merge は、プルリクエストの commit を1つにまとめて取り込み先に加える（F12）。 -/
axiom squash_brings_all_pr : ∀ m p pr c, squashMerges m p pr → inPRAtMerge c pr → bringsInVia m p .squashMerge c

/-- 【自明】承認のあとに push された変更は、承認の時点ではプルリクエストに入っていなかった。
論拠: 承認のあとに加わったものは、承認の時点ではまだない（時の前後の定義）。 -/
axiom pushed_after_not_seen : ∀ c pr q, pushedAfterApproval c pr q → ¬ inPRWhenApproved c pr q

/-! ### U2: 流れを守っても壊れうる（不利な結論のため） -/

/-- 【仮定】承認を得たプルリクエストの squash merge で main に入り、ビルドを壊す変更がある。
@support なし（社内で、承認を受けてマージした変更がビルドを壊した記録が、まだない）
@confidence 0.5
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

/-- 【実験】手元の main を最新にする操作（`git switch main` と `git pull`）があり、動きを確かめてある。
@support F15
論拠: 実行して確かめた（F15）。
弱い点: GitHub ではなく手元のリモートで確かめた（F15）。 -/
axiom recipe_update_main : hasCheckedRecipe .updateMain

/-- 【実験】ブランチを作って移る操作（`git switch -c`）があり、動きを確かめてある。
@support F10
論拠: 実行して確かめた（F10）。
弱い点: git 2.23 より古い git にはこのコマンドがない。 -/
axiom recipe_create_branch : hasCheckedRecipe .createBranch

/-- 【実験】作業ブランチを GitHub に送る操作（`git push -u origin <ブランチ名>`）があり、動きを確かめてある。
@support F13
論拠: 実行して確かめた（F13）。
弱い点: GitHub ではなく手元のリモートで確かめた（F13）。GitHub への認証の手間は含まない。 -/
axiom recipe_push_branch : hasCheckedRecipe .pushBranch

/-- 【実験】push したブランチからプルリクエストを作る画面の操作があり、確かめてある。
@support F14
論拠: GitHub Docs（F14）。 -/
axiom recipe_open_pr : hasCheckedRecipe .openPR

/-- 【実験】レビューする人（Reviewers）を指定する画面の操作があり、確かめてある。
@support F14
論拠: GitHub Docs（F14）。 -/
axiom recipe_request_review : hasCheckedRecipe .requestReview

/-- 【実験】同じブランチに push すればプルリクエストに加わることを確かめてある。
@support F8
論拠: GitHub Docs（F8）。操作そのものは commit と push で、新人が知っている。 -/
axiom recipe_push_fix : hasCheckedRecipe .pushFix

/-- 【実験】squash merge する画面の操作（「Squash and merge」）があり、動きを確かめてある。
@support F12
論拠: GitHub Docs（F12）。画面のボタンは「Squash and merge」。
弱い点: ボタンを押せるかはリポジトリの権限による。 -/
axiom recipe_squash_merge : hasCheckedRecipe .squashMerge

/-- 【仮定】新人は、作業ブランチに自分で commit できる。
@support なし（読者像に書いてあるだけで、事実として登録されていない）
@confidence 0.6
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

/-- 【仮定】決まった操作があり動きを確かめてある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える。
@support なし（新人が文書の手順どおりに進めた記録が、まだない）
@confidence 0.5
論拠: 1つずつの操作は、決まったコマンドか画面の操作で済み、文書で説明する。
弱い点: 新人に実際に通してもらった記録がない。ブランチ・プルリクエスト・マージ・レビューは読者の知らない語（03-reader.json）なので、本文での説明の出来に左右される。
要ファクト: 新人（または同じくらいの経験の人）に、文書の手順どおりにプルリクエストを1本通してもらい、詰まった操作を記録する。 -/
axiom recipe_doable : ∀ o, hasCheckedRecipe o → doneByAuthor o = true → canWrite newcomer → noConflict → canDo o

/-! ### C5: 保護が入ったあとの経路 -/

/-- 【実験】保護が有効な月は、管理者でない人の直接 push は拒否される。
@support F4
@confidence 0.75
@reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人は、だれでも拒否される」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
弱い点: 初期設定では管理者に効かない（F4）。 -/
axiom protection_rejects_push : ∀ m p, protectedMain m → ¬ isAdmin p → pushRejected m p

/-- 【実験】保護が有効な月に、管理者でない人が main に入れる変更は、承認を得たプルリクエストを通ったものだけ。
@support F4
@confidence 0.75
@reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人が入れる変更は、どれも承認を得たプルリクエストを通る」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
弱い点: 初期設定では管理者に効かない（F4）。 -/
axiom protection_only_approved_pr : ∀ m p o c, protectedMain m → ¬ isAdmin p → bringsInVia m p o c → viaApprovedPR c

/-- 【実験】承認を得たプルリクエストで入った変更は、main 以外のブランチから出したプルリクエストで入っている。
@support F6
論拠: プルリクエストは、異なる2つのブランチの間でしか作れない（F6 の出典の引用）。 -/
axiom pr_needs_work_branch : ∀ c, viaApprovedPR c → fromWorkBranch c

/-- 【仮定】新人はリポジトリの管理者ではない。
@support なし（新人の権限を確かめた事実が、まだない）
@confidence 0.8
論拠: 新人に管理者の権限を渡すことはふつうない。
弱い点: 事実がまだない。
要ファクト: 新人のリポジトリでの権限が管理者でないことを、ユーザーに確かめる。 -/
axiom newcomer_not_admin : ¬ isAdmin newcomer

/-! ### U4: 管理者は来月も止まらない（不利な結論のため） -/

/-- 【実験】保護の設定が管理者に効くようになっていなければ、管理者の直接 push は拒否されない。
@support F4
論拠: 初期設定では、保護の制限は管理者に効かない（F4）。 -/
axiom admin_exempt_by_default : ∀ m p, isAdmin p → ¬ protectionCoversAdmins m → ¬ pushRejected m p

/-! ## §5 主張の定理 -/

/-! ### C1 -/

/-- @claim C1 [決定論] main への直接の書き込みで、チーム全員の作業が止まることがある（先月、実際に起きた）。 -/
theorem c1_direct_push_can_stop_team : ∃ m p c, directlyWrites m p c ∧ stopsTeam c := by
  obtain ⟨p, c, hw, hb⟩ := incident_direct_push_broke_build
  exact ⟨.lastMonth, p, c, hw, broken_main_stops_team .lastMonth c (bringing_enters_main _ _ _ _ hw) hb⟩

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

/-- @claim C3 [決定論] 全員が流れを守るかぎり、main に入る変更はすべて、squash merge したプルリクエストに入っていて、
そのプルリクエストを、マージした本人とは別の人が承認し、その人がその変更を見たうえで承認している。 -/
theorem c3_flow_reviews_every_entry :
    (∀ p, FollowsFlow p) → ∀ m c, entersMain m c →
      ∃ p pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q := by
  intro hflow m c hc
  obtain ⟨p, o, hb⟩ := main_entry_has_op m c hc
  obtain ⟨hops, hauth, happ⟩ := hflow p
  have hmem : o ∈ teamFlow := hops m o (bringing_needs_doing m p o c hb)
  have ho : o = .squashMerge := flow_changes_main_only_by_merge o hmem (bringing_changes_main m p o c hb)
  subst ho
  obtain ⟨pr, hsq, hin⟩ := squash_content_from_pr m p c hb
  obtain ⟨q, hq, hfresh⟩ := happ m pr hsq
  have hseen : inPRWhenApproved c pr q := by
    rcases merge_content_origin c pr q hin hq with h | h
    · exact h
    · exact absurd h (hfresh c)
  refine ⟨p, pr, q, hsq, hin, hq, ?_, approval_covers_content c pr q hq hseen⟩
  intro hqp
  exact approver_not_author pr q hq (hqp.trans (hauth m pr hsq).symm)

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

/-- @claim C5 [決定論] 来月、保護が有効になれば、新人の直接 push は拒否され、新人が main に入れられる変更は、
作業ブランチから出して承認を得たプルリクエストを通ったものだけになる。 -/
theorem c5_only_pr_route_when_protected :
    protectedMain .nextMonth →
      pushRejected .nextMonth newcomer ∧
        ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c := by
  intro hprot
  refine ⟨protection_rejects_push _ _ hprot newcomer_not_admin, ?_⟩
  intro o c hb
  have hv : viaApprovedPR c := protection_only_approved_pr _ _ _ _ hprot newcomer_not_admin hb
  exact ⟨hv, pr_needs_work_branch c hv⟩

/-! ### C0 -/

/-- @claim C0 [決定論] 文書の手順は main への直接の書き込みを含まず、C1〜C5 の性質をすべて持つ。 -/
theorem c0_team_flow :
    Op.directWriteMain ∉ teamFlow ∧
    (∃ m p c, directlyWrites m p c ∧ stopsTeam c) ∧
    (∀ m p c, directlyWrites m p c → ¬ viaApprovedPR c ∧ releaseCandidate c) ∧
    (∀ p c, triesDirectPush .thisMonth p c →
      directlyWrites .thisMonth p c ∧ ¬ viaApprovedPR c ∧ releaseCandidate c ∧ (breaksBuild c → stopsTeam c)) ∧
    ((∀ p, FollowsFlow p) → ∀ m c, entersMain m c →
      ∃ p pr q, squashMerges m p pr ∧ inPRAtMerge c pr ∧ approvedBy pr q ∧ q ≠ p ∧ reviewedBy c q) ∧
    (ruleMinApprovals ≤ flowMinApprovals ∧ flowMergeMethod = ruleMergeMethod ∧ flowMerger = ruleMerger ∧
      ∀ k, ruleAllowsPrefix (flowPrefix k)) ∧
    (noConflict → ∀ o, o ∈ teamFlow → doneByAuthor o = true → canDo o) ∧
    (protectedMain .nextMonth →
      pushRejected .nextMonth newcomer ∧
        ∀ o c, bringsInVia .nextMonth newcomer o c → viaApprovedPR c ∧ fromWorkBranch c) :=
  ⟨by decide, c1_direct_push_can_stop_team, c1_direct_push_unreviewed_release, c2_only_self_stops_this_month,
    c3_flow_reviews_every_entry, c4_flow_follows_rules, c4_newcomer_can_do_own_steps, c5_only_pr_route_when_protected⟩

/-! ### 不利な結論（主張にしない。印なし） -/

/-- [不利] 承認のあとに push した変更は、そのプルリクエストを squash merge すると main に入るが、承認した人の承認の時点ではプルリクエストに入っていなかった。 -/
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

/-- [不利] 承認は本人が行う操作ではなく、流れを守ってマージまで進むには、本人とは別の人の承認が要る。 -/
theorem u3_merge_needs_another_person :
    doneByAuthor .approve = false ∧
      ∀ m p pr, FollowsFlow p → squashMerges m p pr → ∃ q, approvedBy pr q ∧ q ≠ p := by
  refine ⟨rfl, ?_⟩
  intro m p pr hflow hsq
  obtain ⟨_, hauth, happ⟩ := hflow
  obtain ⟨q, hq, _⟩ := happ m pr hsq
  refine ⟨q, hq, ?_⟩
  intro hqp
  exact approver_not_author pr q hq (hqp.trans (hauth m pr hsq).symm)

/-- [不利] 保護の設定が管理者に効くようになっていなければ、管理者が直接 push しようとした変更は、main に直接書き込まれる。 -/
theorem u4_admin_still_unblocked :
    ∀ m p c, isAdmin p → ¬ protectionCoversAdmins m → triesDirectPush m p c → directlyWrites m p c := by
  intro m p c hadm hcov ht
  exact unrejected_push_lands m p c ht (admin_exempt_by_default m p hadm hcov)

end

end GitBranchRules
