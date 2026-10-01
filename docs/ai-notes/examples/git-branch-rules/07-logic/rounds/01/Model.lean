/-!
# 証人: 新人向け Gitブランチ運用ルール

`Argument.lean` のすべての `axiom` を、同じ名前・同じ型の具体的な `def` / `theorem` に差し替えた写し。公理系が無矛盾であることの証拠。
axiom 以外の行は、`Argument.lean` と同じ順で残す。`instance`・`attribute`・`open`・`set_option` は足さない。

## 証人の世界

型: `Person`・`Change`・`PR` はどれも `Nat`。

- 人: 0 は新人（`newcomer`）で、流れを守る。1 はレビューする人で、承認だけをする。2 は管理者。3 は流れを守らない人（先月、直接書き込んだ人）。
- 変更: 0 は先月、人 3 が main に直接書き込み、ビルドを壊した変更。1 はプルリクエスト 0 に入っていて、承認の時点からあった変更。
  2 はプルリクエスト 1 に、承認のあとに push された変更（ビルドを壊す）。
- プルリクエスト: 0 は新人が出し、新人が squash merge する。1 は人 3 が出し、人 3 が squash merge する。どちらも人 1 が承認する。
- 月: 今月までは保護がなく、来月は保護が有効（管理者には効かない）。

関係公理の前提が実際に成り立つ例を持たせてある。
- 直接の書き込み（変更 0）と、承認を得たプルリクエストの squash merge（変更 1・2）の両方がある。
- 承認の時点で入っていた変更（1）と、承認のあとに push された変更（2）の両方がある。
- 承認した人（1）は、出した人（0・3）と別の人。
- 管理者（2）がいて、来月の保護で直接 push を拒否される人（管理者以外）と、拒否されない人（管理者）の両方がいる。
- `FollowsFlow` は人 0・1・2 で成り立ち、人 3 で成り立たない（C3 の前提「全員が流れを守る」は、この世界では成り立たない）。
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
abbrev Person : Type := Nat

/-- main に入りうる変更（commit の中身）。 -/
abbrev Change : Type := Nat

/-- プルリクエスト。 -/
abbrev PR : Type := Nat

/-- この文書の読者（今年入社の新人）。 -/
def newcomer : Person := 0

/-- その人がリポジトリの管理者である。 -/
def isAdmin (p : Person) : Prop := p = 2

/-- その人がリポジトリに push できる権限を持っている。 -/
def canWrite (_p : Person) : Prop := True

/-- そのプルリクエストを出した人。 -/
def author (pr : PR) : Person := if pr = 1 then 3 else 0

/-- その月、その人がその操作をする。 -/
def doesOp (_m : Month) (p : Person) (o : Op) : Prop :=
  (p = 0 ∧ o = .squashMerge) ∨ (p = 1 ∧ o = .approve) ∨ p = 3

/-- その月、その人がその操作で、その変更を GitHub の main に入れる。 -/
def bringsInVia (m : Month) (p : Person) (o : Op) (c : Change) : Prop :=
  (m = .lastMonth ∧ p = 3 ∧ o = .directWriteMain ∧ c = 0) ∨ (p = 0 ∧ o = .squashMerge ∧ c = 1) ∨
    (p = 3 ∧ o = .squashMerge ∧ c = 2)

/-- その月、その変更が main に入る（誰の操作かは問わない）。 -/
def entersMain (m : Month) (c : Change) : Prop := ∃ p o, bringsInVia m p o c

/-- その操作は、GitHub の main の中身を変える。 -/
def changesMain (o : Op) : Prop := o = .directWriteMain ∨ o = .squashMerge ∨ o = .otherMerge

/-- その月、その人がその変更を main に直接 push しようとする。 -/
def triesDirectPush (m : Month) (p : Person) (c : Change) : Prop := m = .lastMonth ∧ p = 3 ∧ c = 0

/-- その月、その人の main への直接 push を GitHub が拒否する。 -/
def pushRejected (m : Month) (p : Person) : Prop := m = .nextMonth ∧ p ≠ 2

/-- その月、main にブランチ保護（「Require a pull request before merging」）が有効になっている。 -/
def protectedMain (m : Month) : Prop := m = .nextMonth

/-- その月の保護の設定が、管理者にも効くようになっている。 -/
def protectionCoversAdmins (_m : Month) : Prop := False

/-- その月、その人がそのプルリクエストを squash merge する。 -/
def squashMerges (_m : Month) (p : Person) (pr : PR) : Prop := (p = 0 ∧ pr = 0) ∨ (p = 3 ∧ pr = 1)

/-- マージの時点で、その変更がそのプルリクエストに入っている。 -/
def inPRAtMerge (c : Change) (pr : PR) : Prop := (pr = 0 ∧ c = 1) ∨ (pr = 1 ∧ c = 2)

/-- マージの前に、その人がそのプルリクエストを承認した。 -/
def approvedBy (_pr : PR) (q : Person) : Prop := q = 1

/-- その人が承認した時点で、その変更がプルリクエストに入っていた。 -/
def inPRWhenApproved (c : Change) (pr : PR) (_q : Person) : Prop := pr = 0 ∧ c = 1

/-- その人の承認のあとに、その変更がプルリクエストのブランチに push された。 -/
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

/-- その操作を行う決まったコマンドか画面の操作があり、その動きを確かめてある。 -/
def hasCheckedRecipe (o : Op) : Prop := o ≠ .directWriteMain

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
theorem incident_direct_push_broke_build : ∃ p c, directlyWrites .lastMonth p c ∧ breaksBuild c :=
  ⟨3, 0, Or.inl ⟨rfl, rfl, rfl, rfl⟩, Or.inl rfl⟩

/-- 【自明】main に直接書き込んだ変更は、承認を得たプルリクエストを通っていない。
論拠: 「直接の書き込み」とは、プルリクエストを通さずに main を変えること（語の定義）。 -/
theorem direct_write_skips_pr : ∀ m p c, directlyWrites m p c → ¬ viaApprovedPR c := by
  rintro m p c (⟨_, _, _, rfl⟩ | ⟨_, h, _⟩ | ⟨_, h, _⟩)
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
弱い点: 手元の main が古いと、git が push を断る（`git pull` のあとなら通る）。 -/
theorem unrejected_push_lands : ∀ m p c, triesDirectPush m p c → ¬ pushRejected m p → directlyWrites m p c := by
  rintro m p c ⟨rfl, rfl, rfl⟩ _
  exact Or.inl ⟨rfl, rfl, rfl, rfl⟩

/-! ### C3: 流れを守れば、main に入る変更はレビューを通る -/

/-- 【仮定】main に入る変更には、それを入れた人と、`Op` の語彙のどれかの操作がある。
@support なし（GitHub で main の中身を変える方法を並べた事実と、社内の自動の仕組みについての事実が、まだない）
@confidence 0.7
論拠: main の中身は、誰かが何かの操作をしたときにしか変わらない。`Op` は直接の書き込み・squash merge・それ以外のマージを含む。
弱い点: 語彙の外の操作（API での書き込みなど）が `directWriteMain` に入るかは、定義の広さによる。ボットが流れを守らずに main に書き込むなら、C3 の条件「全員が流れを守る」が成り立たない。
要ファクト: GitHub で main の中身を変える方法が、直接の書き込み（push・画面での直接編集）と、プルリクエストのマージ（squash とそれ以外）に尽きることを GitHub Docs で確かめる。あわせて、社内に main へ書き込む自動の仕組み（ボットなど）があるかをユーザーに確かめる。 -/
theorem main_entry_has_op : ∀ m c, entersMain m c → ∃ p o, bringsInVia m p o c :=
  fun _ _ h => h

/-- 【自明】ある操作で変更を main に入れたなら、その人はその操作をしている。
論拠: 語の定義（「操作で入れた」なら、その操作をしている）。 -/
theorem bringing_needs_doing : ∀ m p o c, bringsInVia m p o c → doesOp m p o := by
  rintro m p o c (⟨_, rfl, _, _⟩ | ⟨rfl, rfl, _⟩ | ⟨rfl, rfl, _⟩)
  · exact Or.inr (Or.inr rfl)
  · exact Or.inl ⟨rfl, rfl⟩
  · exact Or.inr (Or.inr rfl)

/-- 【自明】変更を main に入れた操作は、main の中身を変える操作である。
論拠: 語の定義（「操作で main に入れた」なら、その操作は main を変えている）。 -/
theorem bringing_changes_main : ∀ m p o c, bringsInVia m p o c → changesMain o := by
  rintro m p o c (⟨_, _, rfl, _⟩ | ⟨_, rfl, _⟩ | ⟨_, rfl, _⟩)
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
  rintro m p c (⟨_, _, h, _⟩ | ⟨rfl, _, rfl⟩ | ⟨rfl, _, rfl⟩)
  · cases h
  · exact ⟨0, Or.inl ⟨rfl, rfl⟩, Or.inl ⟨rfl, rfl⟩⟩
  · exact ⟨1, Or.inr ⟨rfl, rfl⟩, Or.inr ⟨rfl, rfl⟩⟩

/-- 【経験則】マージの時点でプルリクエストに入っている変更は、そのプルリクエストを承認した人の承認の時点で入っていたか、承認のあとに push されたかのどちらか。
@support F6 F8
@confidence 0.8
論拠: プルリクエストの中身はブランチの commit で（F6）、ブランチに push した commit は自動で加わる（F8）。
弱い点: 画面の「Update branch」や、レビューする人の提案を画面で取り込む commit も、承認のあとに中身を変える。これらを push とみなせば成り立つ。 -/
theorem merge_content_origin : ∀ c pr q, inPRAtMerge c pr → approvedBy pr q → inPRWhenApproved c pr q ∨ pushedAfterApproval c pr q := by
  rintro c pr q (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩) _
  · exact Or.inl ⟨rfl, rfl⟩
  · exact Or.inr ⟨rfl, rfl⟩

/-- 【経験則】承認の時点でプルリクエストに入っていた変更は、承認した人が見たうえで承認している。
@support F6
@confidence 0.7
論拠: プルリクエストは、マージの前に変更を話し合い、レビューする機能（F6）で、承認はその中身に対して出す。
弱い点: 中身を読まずに承認することはありうる。社内で承認がどう出されているかは確かめていない。 -/
theorem approval_covers_content : ∀ c pr q, approvedBy pr q → inPRWhenApproved c pr q → reviewedBy c q := by
  rintro c pr q rfl ⟨_, rfl⟩
  exact ⟨rfl, rfl⟩

/-- 【仮定】プルリクエストを承認した人は、それを出した本人ではない。
@support なし（本人が自分のプルリクエストを承認できないことを確かめた事実が、まだない）
@confidence 0.8
論拠: 「ほかの人のレビュー」の「ほかの人」を支える。
弱い点: 事実がまだない。
要ファクト: GitHub では、プルリクエストを出した本人が自分のプルリクエストを承認できないことを GitHub Docs で確かめる。 -/
theorem approver_not_author : ∀ pr q, approvedBy pr q → q ≠ author pr := by
  rintro pr q rfl
  unfold author
  split <;> decide

/-! ### U1: 承認のあとの push（不利な結論のため） -/

/-- 【実験】承認のあとに push された変更も、マージの時点でプルリクエストに入っている。
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
  · exact Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)
  · exact absurd h (by decide)
  · exact absurd h (by decide)
  · exact Or.inr (Or.inr ⟨rfl, rfl, rfl⟩)

/-- 【自明】承認のあとに push された変更は、承認の時点ではプルリクエストに入っていなかった。
論拠: 承認のあとに加わったものは、承認の時点ではまだない（時の前後の定義）。 -/
theorem pushed_after_not_seen : ∀ c pr q, pushedAfterApproval c pr q → ¬ inPRWhenApproved c pr q := by
  rintro c pr q ⟨rfl, rfl⟩ ⟨h, _⟩
  exact absurd h (by decide)

/-! ### U2: 流れを守っても壊れうる（不利な結論のため） -/

/-- 【仮定】承認を得たプルリクエストの squash merge で main に入り、ビルドを壊す変更がある。
@support なし（社内で、承認を受けてマージした変更がビルドを壊した記録が、まだない）
@confidence 0.5
論拠: レビューは人が読むもので、見落としがありうる。
弱い点: 社内の事例がまだない。
要ファクト: 社内で、承認を受けてマージした変更で main のビルドが壊れたことがあるかを、ユーザーに確かめる。 -/
theorem approved_change_can_break : ∃ m p c, bringsInVia m p .squashMerge c ∧ viaApprovedPR c ∧ breaksBuild c :=
  ⟨.thisMonth, 3, 2, Or.inr (Or.inr ⟨rfl, rfl, rfl⟩), Or.inr rfl, Or.inr rfl⟩

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

/-- 【実験】手元の main を最新にする操作（`git switch main` と `git pull`）があり、動きを確かめてある。
@support F15
論拠: 実行して確かめた（F15）。
弱い点: GitHub ではなく手元のリモートで確かめた（F15）。 -/
theorem recipe_update_main : hasCheckedRecipe .updateMain := by
  unfold hasCheckedRecipe
  decide

/-- 【実験】ブランチを作って移る操作（`git switch -c`）があり、動きを確かめてある。
@support F10
論拠: 実行して確かめた（F10）。
弱い点: git 2.23 より古い git にはこのコマンドがない。 -/
theorem recipe_create_branch : hasCheckedRecipe .createBranch := by
  unfold hasCheckedRecipe
  decide

/-- 【実験】作業ブランチを GitHub に送る操作（`git push -u origin <ブランチ名>`）があり、動きを確かめてある。
@support F13
論拠: 実行して確かめた（F13）。
弱い点: GitHub ではなく手元のリモートで確かめた（F13）。GitHub への認証の手間は含まない。 -/
theorem recipe_push_branch : hasCheckedRecipe .pushBranch := by
  unfold hasCheckedRecipe
  decide

/-- 【実験】push したブランチからプルリクエストを作る画面の操作があり、確かめてある。
@support F14
論拠: GitHub Docs（F14）。 -/
theorem recipe_open_pr : hasCheckedRecipe .openPR := by
  unfold hasCheckedRecipe
  decide

/-- 【実験】レビューする人（Reviewers）を指定する画面の操作があり、確かめてある。
@support F14
論拠: GitHub Docs（F14）。 -/
theorem recipe_request_review : hasCheckedRecipe .requestReview := by
  unfold hasCheckedRecipe
  decide

/-- 【実験】同じブランチに push すればプルリクエストに加わることを確かめてある。
@support F8
論拠: GitHub Docs（F8）。操作そのものは commit と push で、新人が知っている。 -/
theorem recipe_push_fix : hasCheckedRecipe .pushFix := by
  unfold hasCheckedRecipe
  decide

/-- 【実験】squash merge する画面の操作（「Squash and merge」）があり、動きを確かめてある。
@support F12
論拠: GitHub Docs（F12）。画面のボタンは「Squash and merge」。
弱い点: ボタンを押せるかはリポジトリの権限による。 -/
theorem recipe_squash_merge : hasCheckedRecipe .squashMerge := by
  unfold hasCheckedRecipe
  decide

/-- 【仮定】新人は、作業ブランチに自分で commit できる。
@support なし（読者像に書いてあるだけで、事実として登録されていない）
@confidence 0.6
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

/-- 【仮定】決まった操作があり動きを確かめてある操作のうち、本人が行うものは、新人が push の権限を持ち、コンフリクトが起きなければ、新人が自分で行える。
@support なし（新人が文書の手順どおりに進めた記録が、まだない）
@confidence 0.5
論拠: 1つずつの操作は、決まったコマンドか画面の操作で済み、文書で説明する。
弱い点: 新人に実際に通してもらった記録がない。ブランチ・プルリクエスト・マージ・レビューは読者の知らない語（03-reader.json）なので、本文での説明の出来に左右される。
要ファクト: 新人（または同じくらいの経験の人）に、文書の手順どおりにプルリクエストを1本通してもらい、詰まった操作を記録する。 -/
theorem recipe_doable : ∀ o, hasCheckedRecipe o → doneByAuthor o = true → canWrite newcomer → noConflict → canDo o := by
  intro o _ h _ _
  unfold canDo
  intro heq
  subst heq
  exact absurd h (by decide)

/-! ### C5: 保護が入ったあとの経路 -/

/-- 【実験】保護が有効な月は、管理者でない人の直接 push は拒否される。
@support F4
論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
弱い点: 初期設定では管理者に効かない（F4）。 -/
theorem protection_rejects_push : ∀ m p, protectedMain m → ¬ isAdmin p → pushRejected m p :=
  fun _ _ hm ha => ⟨hm, ha⟩

/-- 【実験】保護が有効な月に、管理者でない人が main に入れる変更は、承認を得たプルリクエストを通ったものだけ。
@support F4
論拠: 保護を有効にすると、承認を得たプルリクエストを通してしか変更を入れられない（F4）。
弱い点: 初期設定では管理者に効かない（F4）。 -/
theorem protection_only_approved_pr : ∀ m p o c, protectedMain m → ¬ isAdmin p → bringsInVia m p o c → viaApprovedPR c := by
  rintro m p o c hm _ (⟨rfl, _, _, _⟩ | ⟨_, _, rfl⟩ | ⟨_, _, rfl⟩)
  · cases hm
  · exact Or.inl rfl
  · exact Or.inr rfl

/-- 【実験】承認を得たプルリクエストで入った変更は、main 以外のブランチから出したプルリクエストで入っている。
@support F6
論拠: プルリクエストは、異なる2つのブランチの間でしか作れない（F6 の出典の引用）。 -/
theorem pr_needs_work_branch : ∀ c, viaApprovedPR c → fromWorkBranch c :=
  fun _ h => h

/-- 【仮定】新人はリポジトリの管理者ではない。
@support なし（新人の権限を確かめた事実が、まだない）
@confidence 0.8
論拠: 新人に管理者の権限を渡すことはふつうない。
弱い点: 事実がまだない。
要ファクト: 新人のリポジトリでの権限が管理者でないことを、ユーザーに確かめる。 -/
theorem newcomer_not_admin : ¬ isAdmin newcomer := by
  unfold isAdmin newcomer
  decide

/-! ### U4: 管理者は来月も止まらない（不利な結論のため） -/

/-- 【実験】保護の設定が管理者に効くようになっていなければ、管理者の直接 push は拒否されない。
@support F4
論拠: 初期設定では、保護の制限は管理者に効かない（F4）。 -/
theorem admin_exempt_by_default : ∀ m p, isAdmin p → ¬ protectionCoversAdmins m → ¬ pushRejected m p := by
  rintro m p hp _ ⟨_, hne⟩
  exact hne hp

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
