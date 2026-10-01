/-!
# 証人: 新人向け Gitブランチ運用ルール

`Argument.lean` のすべての `axiom` を、同じ名前・同じ型の具体的な `abbrev` / `def` / `theorem` に差し替えた写し。公理系が無矛盾であることの証拠。
axiom 以外の行は、`Argument.lean` と同じ順で残す。`instance`・`attribute`・`open`・`set_option` は足さない。

## 証人の世界

型: `Person`・`Change`・`PR` はどれも `Nat`。

- 人: 0 は新人（`newcomer`）で、どの月も流れを守る。1 はレビューする人で、承認だけをする。
  2 は保護を迂回できる人（`bypassesProtection`）。3 は流れを守らない人。
- 変更:
  - 0 は先月、人 3 が main に直接書き込み、ビルドを壊し、チーム全員を止めた変更。
  - 1 はプルリクエスト 0 に、承認の時点からあった変更。
  - 2 はプルリクエスト 1 に、承認のあとに push された変更（ビルドを壊す）。
  - 3 は来月、人 2 が直接 push しようとして、拒否されずに main に直接書き込む変更（ビルドを壊さない）。
  - 4 は今月、人 3 が直接 push しようとして、拒否されずに main に直接書き込む変更（ビルドを壊さない）。
- プルリクエスト: 0 は新人が出し、新人が squash merge する。1 は人 3 が出し、人 3 が squash merge する。どちらも人 1 が承認する。
  squash merge は月によらない（どの月にもある）。
- 月: 直接 push を拒否する設定（`directPushBlocked`）と保護（`protectedMain`）は、来月だけ。保護を迂回できる人にも効かせる設定（`bypassDisallowed`）は、どの月にもない。

関係公理と主張の定理の前提が、実際に成り立つ例を持たせてある（`Model.lean` の写しに `example` を足して、Lean で確かめた。本体には足していない）。
- C2: 今月、人 3 が変更 4 を直接 push しようとする（`triesDirectPush .thisMonth 3 4`）。
- C3・U3: 人 0 は、どの月も `FollowsFlow m 0` を満たす。今月、人 0 はプルリクエスト 0 を squash merge して、変更 1 を main に入れる。
  承認した人 1 は人 0 と別の人で、人 1 の最後の承認の時点で変更 1 は入っていた（`reviewedBy 1 1` も成り立つ）。
- C5: 来月、`directPushBlocked` が成り立つ。来月も人 0 はプルリクエスト 0 を squash merge し、変更 1 は承認を得たプルリクエストを通っている。
- U1: 変更 2 は、人 1 の最後の承認のあとに push され、人 3 の squash merge で main に入る。人 3 は、どの月も流れを守らない。
- U4: 人 2 は保護を迂回でき、来月、変更 3 を直接 push しようとし、拒否されない。
- U5: 先月の人 3 は、変更 0 を直接書き込み、流れを守っていない。
- 直接の書き込み（変更 0・3・4）と、承認を得たプルリクエストの squash merge（変更 1・2）の両方がある。
- 承認の時点で入っていた変更（1）と、承認のあとに push された変更（2）の両方がある。
- 来月の保護で直接 push を拒否される人（2 以外）と、拒否されない人（2）の両方がいる。
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
abbrev Person : Type := Nat

/-- main に入りうる変更（commit の中身）。 -/
abbrev Change : Type := Nat

/-- プルリクエスト。 -/
abbrev PR : Type := Nat

/-- この文書の読者（今年入社の新人）。 -/
def newcomer : Person := 0

/-- その人は、ブランチ保護の制限を受けない立場にある（リポジトリの管理者の権限か、保護を迂回する権限を持つ役割）。 -/
def bypassesProtection (p : Person) : Prop := p = 2

/-- その人がリポジトリに push できる権限を持っている。 -/
def canWrite (_p : Person) : Prop := True

/-- そのプルリクエストを出した人。 -/
def author (pr : PR) : Person := if pr = 1 then 3 else 0

/-- その月、その人がその操作をする。 -/
def doesOp (m : Month) (p : Person) (o : Op) : Prop :=
  (m = .lastMonth ∧ p = 3 ∧ o = .directWriteMain) ∨ (m = .thisMonth ∧ p = 3 ∧ o = .directWriteMain) ∨
    (m = .nextMonth ∧ p = 2 ∧ o = .directWriteMain) ∨ (p = 0 ∧ o = .squashMerge) ∨ (p = 3 ∧ o = .squashMerge) ∨
    (p = 1 ∧ o = .approve)

/-- その月、その人がその操作で、その変更を GitHub の main に入れる。 -/
def bringsInVia (m : Month) (p : Person) (o : Op) (c : Change) : Prop :=
  (m = .lastMonth ∧ p = 3 ∧ o = .directWriteMain ∧ c = 0) ∨ (m = .thisMonth ∧ p = 3 ∧ o = .directWriteMain ∧ c = 4) ∨
    (m = .nextMonth ∧ p = 2 ∧ o = .directWriteMain ∧ c = 3) ∨ (p = 0 ∧ o = .squashMerge ∧ c = 1) ∨
    (p = 3 ∧ o = .squashMerge ∧ c = 2)

/-- その月、その変更が main に入る（誰の操作かは問わない）。 -/
def entersMain (m : Month) (c : Change) : Prop := ∃ p o, bringsInVia m p o c

/-- その操作は、GitHub の main の中身を変える。 -/
def changesMain (o : Op) : Prop := o = .directWriteMain ∨ o = .squashMerge ∨ o = .otherMerge

/-- その月、その人がその変更を main に直接 push しようとする。 -/
def triesDirectPush (m : Month) (p : Person) (c : Change) : Prop :=
  (m = .lastMonth ∧ p = 3 ∧ c = 0) ∨ (m = .thisMonth ∧ p = 3 ∧ c = 4) ∨ (m = .nextMonth ∧ p = 2 ∧ c = 3)

/-- その月、その人の main への直接 push を GitHub が拒否する。
設定の水準の述語。手元の main が古いときに GitHub が fast-forward でない push を断るような、1回ごとの拒否は含まない。 -/
def pushRejected (m : Month) (p : Person) : Prop := m = .nextMonth ∧ p ≠ 2

/-- その月、main への直接 push を拒否する設定が GitHub に入っている（どの設定かは問わない）。 -/
def directPushBlocked (m : Month) : Prop := m = .nextMonth

/-- その月、main のブランチ保護で「Require a pull request before merging」が、必要な承認数1以上で有効になっている。 -/
def protectedMain (m : Month) : Prop := m = .nextMonth

/-- その月の保護の設定が、迂回できる立場の人にも効くようになっている。 -/
def bypassDisallowed (_m : Month) : Prop := False

/-- その月、その人がそのプルリクエストを squash merge する。 -/
def squashMerges (_m : Month) (p : Person) (pr : PR) : Prop := (p = 0 ∧ pr = 0) ∨ (p = 3 ∧ pr = 1)

/-- マージの時点で、その変更がそのプルリクエストに入っている。 -/
def inPRAtMerge (c : Change) (pr : PR) : Prop := (pr = 0 ∧ c = 1) ∨ (pr = 1 ∧ c = 2)

/-- マージの前に、その人がそのプルリクエストを1回以上承認した。 -/
def approvedBy (_pr : PR) (q : Person) : Prop := q = 1

/-- その人の、マージ前の最後の承認の時点で、その変更がプルリクエストに入っていた。 -/
def inPRWhenApproved (c : Change) (pr : PR) (_q : Person) : Prop := pr = 0 ∧ c = 1

/-- その人の、マージ前の最後の承認のあとに、その変更がプルリクエストのブランチに push された。 -/
def pushedAfterApproval (c : Change) (pr : PR) (_q : Person) : Prop := pr = 1 ∧ c = 2

/-- その人が、その変更を見たうえで承認した。 -/
def reviewedBy (c : Change) (q : Person) : Prop := c = 1 ∧ q = 1

/-- その変更は、承認を得たプルリクエストを通って main に入った。 -/
def viaApprovedPR (c : Change) : Prop := c = 1 ∨ c = 2

/-- その変更は、main 以外のブランチ（作業ブランチ）から出したプルリクエストで入った。 -/
def fromWorkBranch (c : Change) : Prop := c = 1 ∨ c = 2

/-- その変更で、main のビルドが壊れる。 -/
def breaksBuild (c : Change) : Prop := c = 0 ∨ c = 2

/-- その変更のせいで、チーム全員の作業が止まる。 -/
def stopsTeam (c : Change) : Prop := c = 0 ∨ c = 2

/-- その変更が、次のリリースで本番に出る候補になる。 -/
def releaseCandidate (_c : Change) : Prop := True

/-- その操作を行う、決まった短いコマンドか画面の操作がある。 -/
def hasFixedRecipe (o : Op) : Prop := o ≠ .directWriteMain

/-- 新人が、その操作を自分で行える。 -/
def canDo (o : Op) : Prop := o ≠ .approve

/-- 作業のあいだにコンフリクトが起きない（C4 の条件）。 -/
def noConflict : Prop := True

/-- 社内の決まりで、マージに必要な承認の最少人数。 -/
def ruleMinApprovals : Nat := 1

/-- 社内の決まりのマージの方法。 -/
def ruleMergeMethod : MergeMethod := .squash

/-- 社内の決まりでマージする人。 -/
def ruleMerger : Merger := .prAuthor

/-- 社内の決まりで、そのブランチ名の頭を使ってよい。 -/
def ruleAllowsPrefix (k : BranchPrefix) : Prop := k ≠ .other

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
theorem incident_direct_push_stopped_team : ∃ p c, directlyWrites .lastMonth p c ∧ stopsTeam c :=
  ⟨3, 0, Or.inl ⟨rfl, rfl, rfl, rfl⟩, Or.inl rfl⟩

/-- 【自明】main に直接書き込んだ変更は、承認を得たプルリクエストを通っていない。
論拠: 「直接の書き込み」とは、プルリクエストを通さずに main を変えること（語の定義）。 -/
theorem direct_write_skips_pr : ∀ m p c, directlyWrites m p c → ¬ viaApprovedPR c := by
  rintro m p c (⟨_, _, _, rfl⟩ | ⟨_, _, _, rfl⟩ | ⟨_, _, _, rfl⟩ | ⟨_, h, _⟩ | ⟨_, h, _⟩)
  · unfold viaApprovedPR
    decide
  · unfold viaApprovedPR
    decide
  · unfold viaApprovedPR
    decide
  · cases h
  · cases h

/-- 【自明】ある操作で変更を main に入れたなら、その変更は main に入っている。
論拠: `bringsInVia` は「その操作で、その変更を main に入れる」、`entersMain` は「誰の操作かを問わず main に入る」で、前者から後者が語の定義として言える。 -/
theorem bringing_enters_main : ∀ m p o c, bringsInVia m p o c → entersMain m c :=
  fun _ p o _ h => ⟨p, o, h⟩

/-- 【経験則】main に入った変更は、次のリリースで本番に出る候補になる。
@support F2
@confidence 0.6
論拠: main は本番に出すもとになる。F2 では、main に入った未レビューの変更が本番に出かけた。
弱い点: 事例は1件（F2）。リリースの前に止める確認があれば本番には出ないが、候補になることは変わらない。 -/
theorem main_feeds_release : ∀ m c, entersMain m c → releaseCandidate c :=
  fun _ _ _ => trivial

/-- 【経験則】main に入った変更がビルドを壊すなら、チーム全員の作業が止まる。
@support F1
@confidence 0.6
論拠: main は全員の作業の土台。F1 ではビルドが壊れて半日全員が止まった。
弱い点: 事例は1件（F1）。main を取り込まずに作業している人は、すぐには止まらない。 -/
theorem broken_main_stops_team : ∀ m c, entersMain m c → breaksBuild c → stopsTeam c :=
  fun _ _ _ h => h

/-- 【実験】今月は、誰の直接 push も GitHub に拒否されない。
@support F3
論拠: F3。
弱い点: 依頼者の証言（F3）。 -/
theorem no_rejection_this_month : ∀ p, ¬ pushRejected .thisMonth p := by
  rintro p ⟨h, _⟩
  cases h

/-- 【経験則】直接 push しようとして、拒否されなければ、その変更は main に直接書き込まれる。
@support F1 F2
@confidence 0.6
論拠: 拒否されない push は受け入れられる。先月の直接 push は実際に main に入った（F1・F2）。
弱い点: 手元の main が古いと、GitHub が fast-forward でない push を断る（`git pull` のあとなら通る）。この拒否は、設定の水準の拒否（`pushRejected`）には入らない。 -/
theorem unrejected_push_lands : ∀ m p c, triesDirectPush m p c → ¬ pushRejected m p → directlyWrites m p c := by
  rintro m p c (⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩) _
  · exact Or.inl ⟨rfl, rfl, rfl, rfl⟩
  · exact Or.inr (Or.inl ⟨rfl, rfl, rfl, rfl⟩)
  · exact Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl, rfl⟩))

/-! ### C3: 流れを守れば、自分が main に入れる変更はレビューと承認を通る -/

/-- 【自明】ある操作で変更を main に入れたなら、その人はその操作をしている。
論拠: 語の定義（「操作で入れた」なら、その操作をしている）。 -/
theorem bringing_needs_doing : ∀ m p o c, bringsInVia m p o c → doesOp m p o := by
  rintro m p o c (⟨rfl, rfl, rfl, _⟩ | ⟨rfl, rfl, rfl, _⟩ | ⟨rfl, rfl, rfl, _⟩ | ⟨rfl, rfl, _⟩ | ⟨rfl, rfl, _⟩)
  · exact Or.inl ⟨rfl, rfl, rfl⟩
  · exact Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)
  · exact Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩))
  · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨rfl, rfl⟩)))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨rfl, rfl⟩))))

/-- 【自明】変更を main に入れた操作は、main の中身を変える操作である。
論拠: 語の定義（「操作で main に入れた」なら、その操作は main を変えている）。 -/
theorem bringing_changes_main : ∀ m p o c, bringsInVia m p o c → changesMain o := by
  rintro m p o c (⟨_, _, rfl, _⟩ | ⟨_, _, rfl, _⟩ | ⟨_, _, rfl, _⟩ | ⟨_, rfl, _⟩ | ⟨_, rfl, _⟩)
  · exact Or.inl rfl
  · exact Or.inl rfl
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inl rfl)

/-- 【自明】`git switch main` と `git pull` は、GitHub の main を変えない。
論拠: `git pull` は GitHub から取り込む操作で、GitHub に送る手順を含まない（コマンドの定義）。 -/
theorem update_main_keeps_main : ¬ changesMain .updateMain := by
  unfold changesMain
  decide

/-- 【自明】`git switch -c` でブランチを作っても、GitHub の main は変わらない。
論拠: `git switch -c` は手元でブランチを作るだけで、GitHub に何も送らない。 -/
theorem create_branch_keeps_main : ¬ changesMain .createBranch := by
  unfold changesMain
  decide

/-- 【実験】作業ブランチへの commit は、main を変えない。
@support F5
論拠: F5 で、作業ブランチに commit しても main の中身が変わらないことを実行して確かめた。
弱い点: 手元での確認（F5）。まちがえて main の上で commit すると成り立たない（その後の push は `directWriteMain` にあたる）。 -/
theorem commit_keeps_main : ¬ changesMain .commitOnBranch := by
  unfold changesMain
  decide

/-- 【経験則】作業ブランチを push しても、GitHub の main は変わらない。
@support F5 F13
@confidence 0.9
論拠: `git push -u origin <ブランチ名>` は同じ名前のブランチを作る（F13）ので、main には書き込まない。
弱い点: F13 は GitHub ではなく手元のリモートで確かめた。 -/
theorem push_branch_keeps_main : ¬ changesMain .pushBranch := by
  unfold changesMain
  decide

/-- 【実験】プルリクエストを作っても、main は変わらない。
@support F6
論拠: プルリクエストは、マージするよう「提案する」機能で、マージは別に行う（F6）。 -/
theorem open_pr_keeps_main : ¬ changesMain .openPR := by
  unfold changesMain
  decide

/-- 【自明】レビューを依頼しても、main は変わらない。
論拠: レビューする人を指定するだけの操作。 -/
theorem request_review_keeps_main : ¬ changesMain .requestReview := by
  unfold changesMain
  decide

/-- 【経験則】指摘に応える commit を同じブランチに push しても、main は変わらない。
@support F8 F13
@confidence 0.9
論拠: 同じブランチへの push はプルリクエストに加わる（F8）。送り先は作業ブランチ（F13）。
弱い点: 送り先をまちがえて main にすると成り立たない（それは `directWriteMain` にあたる）。 -/
theorem push_fix_keeps_main : ¬ changesMain .pushFix := by
  unfold changesMain
  decide

/-- 【経験則】承認しても、main は変わらない（マージは別の操作）。
@support F6
@confidence 0.8
論拠: プルリクエストでは、レビューとマージは別の段階（F6）。
弱い点: 自動マージ（auto-merge）を有効にしていると、承認がマージのきっかけになる。 -/
theorem approve_keeps_main : ¬ changesMain .approve := by
  unfold changesMain
  decide

/-- 【実験】squash merge で main に入る変更は、そのとき squash merge したプルリクエストに入っていた変更である。
@support F12
論拠: squash merge は、プルリクエストの commit を1つにまとめて取り込み先に加える（F12）。 -/
theorem squash_content_from_pr : ∀ m p c, bringsInVia m p .squashMerge c → ∃ pr, squashMerges m p pr ∧ inPRAtMerge c pr := by
  rintro m p c (⟨_, _, h, _⟩ | ⟨_, _, h, _⟩ | ⟨_, _, h, _⟩ | ⟨rfl, _, rfl⟩ | ⟨rfl, _, rfl⟩)
  · cases h
  · cases h
  · cases h
  · exact ⟨0, Or.inl ⟨rfl, rfl⟩, Or.inl ⟨rfl, rfl⟩⟩
  · exact ⟨1, Or.inr ⟨rfl, rfl⟩, Or.inr ⟨rfl, rfl⟩⟩

/-- 【経験則】マージの時点でプルリクエストに入っている変更は、そのプルリクエストを承認した人の最後の承認の時点で入っていたか、最後の承認のあとに push されたかのどちらか。
@support F6 F8
@confidence 0.8
論拠: プルリクエストの中身はブランチの commit で（F6）、ブランチに push した commit は自動で加わる（F8）。
弱い点: 画面の「Update branch」や、レビューする人の提案を画面で取り込む commit も、最後の承認のあとに中身を変える。これらを push とみなせば成り立つ。 -/
theorem merge_content_origin : ∀ c pr q, inPRAtMerge c pr → approvedBy pr q → inPRWhenApproved c pr q ∨ pushedAfterApproval c pr q := by
  rintro c pr q (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩) _
  · exact Or.inl ⟨rfl, rfl⟩
  · exact Or.inr ⟨rfl, rfl⟩

/-- 【経験則】承認した人の最後の承認の時点でプルリクエストに入っていた変更は、その人が見たうえで承認している。
@support F6
@confidence 0.05
@reviewer 0.05 ← 0.7 理由: F6 が述べるのは「プルリクエストは、マージの前に変更を話し合い、レビューできる機能」ということだけで、承認した人が中身を見たうえで承認しているか（社内での承認の出し方）は述べていない。この公理が言う人の振る舞いを支える事実がない。
論拠: プルリクエストは、マージの前に変更を話し合い、レビューする機能（F6）で、承認はその中身に対して出す。
弱い点: 中身を読まずに承認することはありうる。社内で承認がどう出されているかは確かめていない。F6 は、プルリクエストがレビューのための機能であることを述べるだけで、承認する人の振る舞いは述べていない（F6）。
要ファクト: 社内で、プルリクエストを承認する人が、差分（変更の中身）を読んでから承認しているかを、ユーザーに確かめる。承認のあとに足された commit を、頼み直したレビューで読んでいるかも含む。 -/
theorem approval_covers_content : ∀ c pr q, approvedBy pr q → inPRWhenApproved c pr q → reviewedBy c q := by
  rintro c pr q rfl ⟨_, rfl⟩
  exact ⟨rfl, rfl⟩

/-- 【仮定】プルリクエストを承認した人は、それを出した本人ではない。
@support なし（本人が自分のプルリクエストを承認できないことを確かめた事実が、まだない）
@confidence 0.05
論拠: 「ほかの人のレビュー」の「ほかの人」を支える。
弱い点: 事実がまだない。
要ファクト: GitHub では、プルリクエストを出した本人が自分のプルリクエストを承認できないことを GitHub Docs で確かめる。 -/
theorem approver_not_author : ∀ pr q, approvedBy pr q → q ≠ author pr := by
  rintro pr q rfl
  unfold author
  split <;> decide

/-! ### U1: 承認のあとの push（不利な結論のため） -/

/-- 【実験】最後の承認のあとに push された変更も、マージの時点でプルリクエストに入っている。
@support F8
論拠: プルリクエストを出したあとに同じブランチへ push した commit は、自動で加わる（F8）。
弱い点: いったん加わった commit を強制的な push で消すと、マージの時点には残らない。 -/
theorem push_joins_pr : ∀ c pr q, pushedAfterApproval c pr q → inPRAtMerge c pr := by
  rintro c pr q ⟨rfl, rfl⟩
  exact Or.inr ⟨rfl, rfl⟩

/-- 【実験】squash merge すると、マージの時点でプルリクエストに入っている変更は、すべて main に入る。
@support F12
論拠: squash merge は、プルリクエストの commit を1つにまとめて取り込み先に加える（F12）。 -/
theorem squash_brings_all_pr : ∀ m p pr c, squashMerges m p pr → inPRAtMerge c pr → bringsInVia m p .squashMerge c := by
  rintro m p pr c (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩) (⟨h, rfl⟩ | ⟨h, rfl⟩)
  · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)))
  · exact absurd h (by decide)
  · exact absurd h (by decide)
  · exact Or.inr (Or.inr (Or.inr (Or.inr ⟨rfl, rfl, rfl⟩)))

/-- 【自明】ある人の最後の承認のあとに push された変更は、その人の最後の承認の時点ではプルリクエストに入っていなかった。
論拠: 最後の承認のあとに加わったものは、その承認の時点ではまだない（時の前後の定義）。 -/
theorem pushed_after_not_seen : ∀ c pr q, pushedAfterApproval c pr q → ¬ inPRWhenApproved c pr q := by
  rintro c pr q ⟨rfl, rfl⟩ ⟨h, _⟩
  exact absurd h (by decide)

/-! ### U2: 流れを守っても壊れうる（不利な結論のため） -/

/-- 【仮定】承認を得たプルリクエストの squash merge で main に入り、ビルドを壊す変更がある。
@support なし（社内で、承認を受けてマージした変更がビルドを壊した記録が、まだない）
@confidence 0.05
論拠: レビューは人が読むもので、見落としがありうる。
弱い点: 社内の事例がまだない。
要ファクト: 社内で、承認を受けてマージした変更で main のビルドが壊れたことがあるかを、ユーザーに確かめる。 -/
theorem approved_change_can_break : ∃ m p c, bringsInVia m p .squashMerge c ∧ viaApprovedPR c ∧ breaksBuild c :=
  ⟨.thisMonth, 3, 2, Or.inr (Or.inr (Or.inr (Or.inr ⟨rfl, rfl, rfl⟩))), Or.inr rfl, Or.inr rfl⟩

/-! ### C4: 社内の決まりに沿うこと -/

/-- 【実験】マージに必要な承認の最少人数は1人。
@support F7
論拠: 依頼者の証言した社内の決まり（F7）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F7）。 -/
theorem rule_min_approvals : ruleMinApprovals = 1 := rfl

/-- 【実験】社内のマージの方法は squash merge。
@support F11
論拠: 依頼者の証言した社内の決まり（F11）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F11）。 -/
theorem rule_merge_method : ruleMergeMethod = .squash := rfl

/-- 【実験】社内でマージするのは、プルリクエストを出した本人。
@support F11
論拠: 依頼者の証言した社内の決まり（F11）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F11）。 -/
theorem rule_merger : ruleMerger = .prAuthor := rfl

/-- 【実験】ブランチ名の頭に `feature` を使ってよい。
@support F9
論拠: 依頼者の証言した社内の決まり（F9）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F9）。 -/
theorem rule_prefix_feature : ruleAllowsPrefix .feature := by
  unfold ruleAllowsPrefix
  decide

/-- 【実験】ブランチ名の頭に `fix` を使ってよい。
@support F9
論拠: 依頼者の証言した社内の決まり（F9）。
弱い点: 証言だけで、社内の規程の文書は確かめていない（F9）。 -/
theorem rule_prefix_fix : ruleAllowsPrefix .fix := by
  unfold ruleAllowsPrefix
  decide

/-! ### C4: 新人が自分で進められること -/

/-- 【実験】手元の main を最新にする、決まった操作（`git switch main` と `git pull`）がある。
@support F15
論拠: 実行して確かめた（F15）。
弱い点: GitHub ではなく手元のリモートで確かめた（F15）。 -/
theorem recipe_update_main : hasFixedRecipe .updateMain := by
  unfold hasFixedRecipe
  decide

/-- 【実験】ブランチを作って移る、決まった操作（`git switch -c`）がある。
@support F10
論拠: 実行して確かめた（F10）。
弱い点: git 2.23 より古い git にはこのコマンドがない。 -/
theorem recipe_create_branch : hasFixedRecipe .createBranch := by
  unfold hasFixedRecipe
  decide

/-- 【実験】作業ブランチを GitHub に送る、決まった操作（`git push -u origin <ブランチ名>`）がある。
@support F13
論拠: 実行して確かめた（F13）。
弱い点: GitHub ではなく手元のリモートで確かめた（F13）。GitHub への認証の手間は含まない。 -/
theorem recipe_push_branch : hasFixedRecipe .pushBranch := by
  unfold hasFixedRecipe
  decide

/-- 【実験】push したブランチからプルリクエストを作る、決まった画面の操作がある。
@support F14
論拠: GitHub Docs（F14）。 -/
theorem recipe_open_pr : hasFixedRecipe .openPR := by
  unfold hasFixedRecipe
  decide

/-- 【実験】レビューする人（Reviewers）を指定する、決まった画面の操作がある。
@support F14
論拠: GitHub Docs（F14）。 -/
theorem recipe_request_review : hasFixedRecipe .requestReview := by
  unfold hasFixedRecipe
  decide

/-- 【実験】指摘に応える commit を同じブランチに送る、決まった操作（commit と push）がある。
@support F8
論拠: 同じブランチに push すればプルリクエストに加わる（GitHub Docs、F8）。操作そのものは commit と push で、新人が知っている。 -/
theorem recipe_push_fix : hasFixedRecipe .pushFix := by
  unfold hasFixedRecipe
  decide

/-- 【実験】squash merge する、決まった画面の操作（「Squash and merge」）がある。
@support F12
論拠: GitHub Docs（F12）。画面のボタンは「Squash and merge」。
弱い点: ボタンを押せるかはリポジトリの権限による。 -/
theorem recipe_squash_merge : hasFixedRecipe .squashMerge := by
  unfold hasFixedRecipe
  decide

/-- 【仮定】新人は、作業ブランチに自分で commit できる。
@support なし（読者像に書いてあるだけで、事実として登録されていない）
@confidence 0.05
論拠: 03-reader.json に「Git で commit と push はできる」とある。
弱い点: 06-facts.json に事実として登録されていないので、`@support` にできない。
要ファクト: 03-reader.json の「新人は Git で commit と push ができる」を、ユーザーの証言として 06-facts.json に登録する。 -/
theorem newcomer_can_commit : canDo .commitOnBranch := by
  unfold canDo
  decide

/-- 【経験則】新人は、リポジトリに push できる権限を持っている。
@support F1 F2
@confidence 0.6
論拠: 先月、新人が main に直接 push できた（F1・F2）ので、新人には push の権限がある。
弱い点: 先月の新人と、今年の読者が同じ権限とは限らない（F1・F2）。 -/
theorem newcomer_can_write : canWrite newcomer := trivial

/-- 【仮定】決まった短い操作がある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える。
@support なし（新人が文書の手順どおりに進めた記録が、まだない）
@confidence 0.05
論拠: 1つずつの操作は、決まったコマンドか画面の操作で済む。文書は、流れの各操作を、その決まった操作で説明する。
弱い点: 新人に実際に通してもらった記録がない。ブランチ・プルリクエスト・マージ・レビューは読者の知らない語（03-reader.json）なので、本文での説明の出来に左右される。
要ファクト: 新人（または同じくらいの経験の人）に、文書の手順どおりにプルリクエストを1本通してもらい、詰まった操作を記録する。 -/
theorem recipe_doable : ∀ o, hasFixedRecipe o → doneByAuthor o = true → canWrite newcomer → noConflict → canDo o := by
  intro o _ h _ _
  unfold canDo
  intro heq
  subst heq
  exact absurd h (by decide)

/-! ### C5: 保護が入ったあとの経路 -/

/-- 【実験】保護が有効な月は、保護を迂回できない人の直接 push は拒否される。
@support F4
@confidence 0.75
@reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人は、だれでも拒否される」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
弱い点: 初期設定では、管理者などには効かない（F4）。その人たちは、迂回できる立場として前提で除いてある。 -/
theorem protection_rejects_push : ∀ m p, protectedMain m → ¬ bypassesProtection p → pushRejected m p :=
  fun _ _ hm hb => ⟨hm, hb⟩

/-- 【実験】保護が有効な月に、保護を迂回できない人が main に入れる変更は、承認を得たプルリクエストを通ったものだけ。
@support F4
@confidence 0.75
@reviewer 0.75 ← 0.95 理由: F4 は、初期設定で制限が効かないのは「リポジトリの管理者など」と述べ、除かれるのは管理者だけではない（バイパスの権限を持つ役割など）。公理の「管理者でない人が入れる変更は、どれも承認を得たプルリクエストを通る」は F4 より強く、F4 は一部しか支えない（partially_verified 相当の値にした）。元の案は、書き手の案がない実験の公理なので、CLI が計算した値。
論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
弱い点: 初期設定では、管理者などには効かない（F4）。その人たちは、迂回できる立場として前提で除いてある。 -/
theorem protection_only_approved_pr : ∀ m p o c, protectedMain m → ¬ bypassesProtection p → bringsInVia m p o c → viaApprovedPR c := by
  rintro m p o c hm hb (⟨rfl, _, _, _⟩ | ⟨rfl, _, _, _⟩ | ⟨_, rfl, _, _⟩ | ⟨_, _, rfl⟩ | ⟨_, _, rfl⟩)
  · cases hm
  · cases hm
  · exact absurd rfl hb
  · exact Or.inl rfl
  · exact Or.inr rfl

/-- 【実験】承認を得たプルリクエストで入った変更は、main 以外のブランチから出したプルリクエストで入っている。
@support F6
論拠: プルリクエストは、異なる2つのブランチの間でしか作れない（F6 の出典の引用）。 -/
theorem pr_needs_work_branch : ∀ c, viaApprovedPR c → fromWorkBranch c :=
  fun _ h => h

/-- 【仮定】新人は、保護を迂回できる立場にない（管理者の権限も、迂回の権限も持たない）。
@support なし（新人のリポジトリでの役割を確かめた事実が、まだない）
@confidence 0.05
論拠: 新人に、管理者の権限や、保護を迂回する権限を渡すことは、ふつうない。
弱い点: 事実がまだない。
要ファクト: 新人のリポジトリでの役割（権限）が、管理者でも、保護を迂回できる役割でもないことを、ユーザーに確かめる。 -/
theorem newcomer_no_bypass : ¬ bypassesProtection newcomer := by
  unfold bypassesProtection newcomer
  decide

/-- 【仮定】来月、直接 push を拒否する設定が入るなら、それは承認1名以上のプルリクエストを必須にする保護である。
@support なし（F3 は「直接 push を拒否する設定に来月変える予定」と述べるだけで、どの設定を入れるか、必要な承認数をいくつにするかは述べていない。F7 は社内の決まりで、GitHub の設定ではない）
@confidence 0.05
論拠: main への直接 push を止める設定としてふつう使うのは、マージの前にプルリクエストを必須にする保護で、社内の決まり（承認1名以上）とも合う。
弱い点: 承認を求めずに直接 push だけを止める設定（承認数 0 や、push できる人を限る設定など）もありうる。その場合、C5 の結論は「承認を得たプルリクエストだけ」ではなく「プルリクエストを通ったものだけ」に弱まる。
要ファクト: 来月 main に入れる設定が「Require a pull request before merging」か、必要な承認数を1以上にするかを、ユーザーに確かめる。 -/
theorem next_month_block_requires_pr : directPushBlocked .nextMonth → protectedMain .nextMonth :=
  fun h => h

/-! ### U4: 保護を迂回できる人は来月も止まらない（不利な結論のため） -/

/-- 【実験】保護の設定が迂回できる立場の人にも効くようになっていなければ、その人の直接 push は拒否されない。
@support F4
論拠: 初期設定では、保護の制限は、リポジトリの管理者の権限を持つ人に効かない（F4）。迂回の権限を持つ役割は、その権限の意味から、制限を受けない。
弱い点: F4 の引用が直接述べるのは、管理者の権限を持つ人だけである。迂回の権限を持つ役割は、F4 の「管理者など」に含めて読んでいる（F4）。 -/
theorem bypass_exempt_by_default : ∀ m p, bypassesProtection p → ¬ bypassDisallowed m → ¬ pushRejected m p := by
  rintro m p hp _ ⟨_, hne⟩
  exact hne hp

/-! ## §5 主張の定理 -/

/-! ### C1 -/

/-- @claim C1 [決定論] main への直接の書き込みで、チーム全員の作業が止まることがある（先月、実際に起きた）。 -/
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
