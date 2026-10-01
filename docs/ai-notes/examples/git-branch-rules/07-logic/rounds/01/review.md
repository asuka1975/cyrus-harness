判定: 差し戻し（高 2・中 6・低 6）

# 監査の報告（1周目）: 新人向け Gitブランチ運用ルール

監査した版: `Argument.lean`・`Model.lean`（門のエラー 0）、`report.json`・`hints.json`（2026-09-30 の `cyrus lean`）。
私の書き換え（確信度を3つ下げた）のあとに `cyrus lean` を実行し、門のエラーが 0 のままであることを確かめた。

## 要点

- **C3 の定理は空回りしている（高）。** 公理から「全員が流れを守る」の否定が導ける。そのため `c3_flow_reviews_every_entry` は、結論を何に置き換えても証明できる。`c0_team_flow` の C3 の項も同じ。`report.json` の C3 の依存の一覧（15個）は、書き手の証明の道筋であって、この定理に本当に必要なものではない。
- **C3 の「流れ」が、C0 の流れより強い（高）。** `FollowsFlow` の (c) は「承認のあとに push したら、承認を受け直す」を含む。これは 05-claims.json の C0 にも C3 にもない。C0 の字義どおりの流れでは、U1（確信度 0.95）によって C3 が成り立たない。
- 確信度を3つ下げた。`approval_covers_content`（0.7 → 0.05）、`protection_rejects_push`・`protection_only_approved_pr`（0.95 → 0.75）。主張の値は変わらない（C0・C3・C5 はもともと 0.05）。手戻りの一覧は6個から7個になった。

## 指摘の表

| ID | 対象 | 重大度 | 監査項目 | 要点 | 戻す先 |
|---|---|---|---|---|---|
| H1 | `FollowsFlow`、`c3_flow_reviews_every_entry`、`c0_team_flow` | 高 | 18・12 | C3 の前提 `∀ p, FollowsFlow p` は公理から否定できる。`incident_direct_push_broke_build`（先月だれかが main に直接書き込んだ）と `bringing_needs_doing` から、その人の `doesOp .lastMonth p .directWriteMain` が出る。`FollowsFlow` の (a) は月を問わず「する操作はすべて `teamFlow` に含まれる」を求めるので、その人は流れを守っていない。したがって C3 の定理は、どの世界でも前提が偽で、何も言っていない（下の「H1 の検算」）。証人（`Model.lean`）の冒頭にも「C3 の前提はこの世界では成り立たない」とあり、書き手は気づいていたが、問題としては記録されていない | Planner |
| H2 | `FollowsFlow` の (c)、`c3_flow_reviews_every_entry`、C0・C3 | 高 | 1・12 | `FollowsFlow` の (c) の後半「承認のあとに push された変更がない（受け直してからマージする）」は、C0 の文（「1名以上の承認を受けてから、自分で squash merge」）にない。字義どおりの C0 の流れでは、承認のあとに push した変更がレビューなしで main に入る（U1、確信度 0.95。F14 の notes のとおり、承認を取り消す設定が有効かは分からない）。つまり、C3 は字義どおりの流れでは成り立たず、def に置いた「流れの読み」によって成り立っている。ガイドの「主張の文が2通りに読めるとき」にあたるので、ステージ5で確かめる必要がある | ステージ5（と Planner） |
| M1 | `c3_flow_reviews_every_entry`、`main_entry_has_op` | 中 | 12・14 | C3 の「この流れを守るかぎり」には2つの読みがある。(i) チームの全員が守れば、main に入る変更はすべてレビューを通る（いまのモデル）。(ii) 自分が守れば、自分が main に入れる変更はレビューを通る。読者（新人）に向く文としては (ii) が自然。(ii) は `main_entry_has_op`（証拠がない【仮定】）を使わずに示せ、H1 の空回りも起きない。どちらの読みかはステージ5で決めることなので、それまでは両方の読みに `@claim` を置く | ステージ5・Planner |
| M2 | `approval_covers_content` | 中 | 4・8 | F6 は「プルリクエストは変更を話し合い、レビューできる機能」と述べるだけで、承認した人が中身を見たうえで承認しているかは述べていない。この公理は、社内の人の振る舞いについての判断で、設計書4節でも主張に有利な向きの「同じとみなす」置き方に挙がっている。0.7 → 0.05 に下げた。ステージ6で、社内で承認する人が差分を読んでから承認しているかをユーザーに確かめる。別の道として、C3 の「レビューと承認を通る」を手続きの意味（承認の時点でその変更がプルリクエストに入っていた）と読むなら、結論を `inPRWhenApproved` にして、この公理を使わない形にできる | ステージ6・Planner |
| M3 | `protection_rejects_push`、`protection_only_approved_pr`、`newcomer_not_admin` | 中 | 4・14 | F4 は、初期設定で保護の制限が効かないのは「リポジトリの管理者など」と述べる。除かれるのは管理者だけではない（保護を迂回する権限を持つ役割など）。2つの公理は「管理者でない人は、だれでも止められる」と言い、F4 より強い。0.95 → 0.75 に下げた。Planner は、`isAdmin` を「保護を迂回できる」（管理者か、迂回の権限を持つ役割）に広げ、`newcomer_not_admin` を「新人は保護を迂回できない」にし、要ファクトもそれに合わせる | Planner・ステージ6 |
| M4 | `c5_only_pr_route_when_protected` の前提 `protectedMain .nextMonth` | 中 | 1 | C5 の条件は「仕組みで直接 push が拒否されるようになっても」、F3 は「直接 push を拒否する設定に来月変える予定」。一方、`protectedMain` は「Require a pull request before merging が有効」という特定の設定を指し、結論の「承認を得たプルリクエストを通ったものだけ」はこの設定（と必要な承認数が1以上であること）に依存する。社内が来月どの設定を入れるかは事実にない。定理の引数に「その設定が入る」という判断が置かれている。【仮定】の関係公理（「来月の設定は Require a pull request before merging で、承認1名以上」、要ファクト: ユーザーに設定を確かめる）にするか、前提を「直接 push が拒否される」だけにして結論を弱める | Planner・ステージ6 |
| M5 | `c4_newcomer_can_do_own_steps`、C4 | 中 | 12 | C4 は「新人でも最初から最後まで自分で進められる」と言うが、定理は `approve` を除いた操作についてだけ言う。U3 のとおり、マージまで進むにはほかの人の承認が要る。定理は主張より弱く、主張の文が言い過ぎている。ステージ5で「承認をもらうこと以外は、自分で進められる」などに直す（設計書6節の U3 の注意と同じ向き）。あわせて、定理は操作を1つずつ行えることしか言わず、順序どおりに進められること（次に何をするかが分かること）は言っていない | ステージ5 |
| M6 | `c1_direct_push_can_stop_team`、`broken_main_stops_team` | 中 | 8・6 | C1 の「全員の作業を止める危険」は、F1 がそのまま述べている（直接 push した変更で、半日全員が止まった）。それなのにモデルは、「ビルドを壊した変更がある」と、全称の「main のビルドが壊れれば、チーム全員が止まる」を組み合わせて示している。全称は1件の事例からの一般化で、主張に有利な向き（設計書4節）であり、自分の弱い点に例外（main を取り込まない人は止まらない）を書いている。確信度は、【経験則】の一般化として弱い点を書いてあるので 0.6 のまま残した。ただ、C1 の存在の定理は、F1 から直接の存在の公理（【実験】F1）で示し、全称は C2 の `breaksBuild c → stopsTeam c` の項と U2 にだけ使うほうがよい | Planner |
| L1 | `pushedAfterApproval`、`inPRWhenApproved` | 低 | 1 | どちらも「どの承認か」を引数に取らない。同じ人 `q` が承認を受け直した場合、1回目の承認のあとに push した変更は `pushedAfterApproval c pr q` のままになる。そのため、`FollowsFlow` の docstring の「承認を受け直してからマージする」が型で表せない。「その人の最後の承認のあとに」と定義するか、承認の出来事を引数に取る | Planner |
| L2 | `hasCheckedRecipe`、`recipe_doable` | 低 | 1・13 | `hasCheckedRecipe` の「動きを確かめてある」は、書き手が確かめたかという証拠の側の性質で、現実の世界の性質ではない。`recipe_doable` は「確かめた操作は、新人ができる」とつないでいるが、確かめたかどうかは新人の能力に効かない。現実の条件（決まった短いコマンドか画面の操作があり、文書で説明している）を宣言にする。C4 の中身は、ほぼ `recipe_doable` 1つが担っている。【仮定】で要ファクトもあるので、言い換えとして退けはしない | Planner |
| L3 | `c5_only_pr_route_when_protected`、C5 | 低 | 14 | C5 の「この流れを知っておく必要がある」までの橋がない。定理が示すのは「保護が入れば、新人が入れられるのは承認を得たプルリクエストの経路だけ」まで。04-analysis.md の論点「仕組みは push を拒否するだけで、正しい流れは教えない」は関係公理になっていない。また、保護が強制するのはプルリクエストと承認だけで、ブランチ名や squash merge は強制しない | Planner |
| L4 | `unrejected_push_lands` | 低 | 4 | 弱い点の「手元の main が古いと、git が push を断る」は、実際には GitHub の側が断る（fast-forward でない push の拒否）。`pushRejected` は「その月、その人の push を拒否する」という設定の水準の述語で、1回ごとの拒否を表さない。値に効くほどではないが、弱い点の書き方を直す | Planner |
| L5 | `approved_change_can_break`、`u2_reviewed_change_can_stop_team` | 低 | 10 | 手戻りの一覧で `claims` が空なので、後回しにされやすい。しかし U2 は、01-intent.md の「この流れを守れば、自分の変更で他の人の作業を壊さずに済む」に歯止めをかける唯一の定理。ステージ6では、この公理の事実（承認を受けてマージした変更でビルドが壊れたことがあるか）も集める。なお、U2 の値が低くても「壊さずに済む」を支える定理はないので、ステージ11 でそう書いてはいけないことは変わらない | ステージ6 |
| L6 | 証人（`Model.lean`）、`u4_admin_still_unblocked` | 低 | 18 | 証人では、管理者（人 2）が直接 push しようとする例がない（`triesDirectPush` は先月の人 3 だけ）。U4 は証人の中で前提が一度も成り立たない。関係公理の空回りではないので低。管理者が来月直接 push しようとする例を足す | Writer |

### H1 の検算

`Argument.lean` の公理だけから、次が Lean で示せた（`#print axioms` では、依存する関係公理は `incident_direct_push_broke_build` と `bringing_needs_doing` だけ）。

```lean
theorem not_everyone_follows : ¬ (∀ p, FollowsFlow p) := by
  intro h
  obtain ⟨p, c, hw, _⟩ := incident_direct_push_broke_build
  have hdo := bringing_needs_doing _ _ _ _ hw
  have hmem := (h p).1 _ _ hdo
  exact absurd hmem (by decide)

theorem c3_vacuous (Q : Prop) : (∀ p, FollowsFlow p) → Q := fun h => absurd h not_everyone_follows
```

直す向き（Planner へ）:

- `FollowsFlow` に月を引数として持たせ（その月に流れを守る）、C3 を月ごとに述べる。先月の事故は「先月は全員が守っていたわけではない」と両立する。
- M1 の (ii)（本人が守れば、本人の変更は）の読みも置く。
- 証人には、全員が流れを守る月があり、その月に main に入る変更がある例を持たせる。そうしないと、2周目も証人の中で C3 が空回りする。

### H2 について（ステージ5で確かめること）

- 字義どおりの C0 の流れでは、C3 は U1 で破れる。ステージ5で、次のどちらかをユーザーに確かめる。
  - C0 に「承認のあとに push したら、もう一度承認を受けてからマージする」を入れる（04-analysis.md の論点「もう一度見てもらうよう勧める」と同じ向き）。こうすれば `FollowsFlow` の (c) が主張と一致する。
  - C3 を「承認の時点でプルリクエストに入っていた変更は」と弱める。
- 確かめるまで、Planner は、字義どおりの流れで示せる形（弱めた C3）にも `@claim C3` を置く。主張の値は、小さいほうになる。

## 確信度を下げた公理

| 公理 | 元の値 → 新しい値 | 理由 |
|---|---|---|
| `approval_covers_content` | 0.7 → 0.05 | F6 は、プルリクエストがレビューのための機能であることを述べるだけで、承認した人が中身を見たうえで承認しているか（社内での承認の出し方）は述べていない。この公理が言う人の振る舞いを支える事実がない（M2） |
| `protection_rejects_push` | 0.95 → 0.75 | F4 は「管理者など」には制限が効かないと述べる。「管理者でない人は、だれでも拒否される」は F4 より強く、F4 は一部しか支えない（M3）。元の案は、書き手の案がない【実験】なので CLI の値 0.95 とした |
| `protection_only_approved_pr` | 0.95 → 0.75 | 同上（M3） |

いずれも `@reviewer` の行を足し、`@confidence` を同じ値にした。書き換えのあと `cyrus lean` で門のエラーは 0。

## `@against` を付けた公理と、棄却を提案する公理

- `@against` は付けていない。06-facts.json の事実で、どの公理にも反対の向きを述べるものはなかった（M3 の F4 は、同じ事実のうち公理が拾っていない部分で、反対の証拠ではなく「一部しか支えない」として扱った）。
- 棄却を提案する公理はない。

## 主張ごとの見立て

| 主張 | report.json の値 | 見立て |
|---|---|---|
| C0 | 0.05（hypothesis） | 0.05 に同意。ただし C3 の項は H1 で空回りしているので、C0 の「C3 の性質を持つ」は、いまのモデルでは何も支えられていない。C0 の規範の部分（この手順を採るべきだ）をモデルに入れないのは、設計書1節のとおりで妥当 |
| C1 | 0.6（moderate） | 0.6 に同意（F1・F2 は user_asserted）。M6 を直しても値は変わらない見込み。`c1_direct_push_unreviewed_release` は言い換えではない（下の「手がかりへの見立て」） |
| C2 | 0.6（moderate） | 0.6 に同意（F1〜F3 は user_asserted）。「止めるのは本人がしないことだけ」は、「しようとすれば必ず入る」という含意の形で定理に入っている |
| C3 | 0.05（hypothesis） | 値より前に、定理が空回りしていて主張を支えていない（H1）。読みの問題（H2・M1）もある。H1 を直しても、値は `main_entry_has_op`・`approver_not_author`・`approval_covers_content` の事実が集まるまで 0.05 |
| C4 | 0.05（hypothesis） | 0.05 に同意（`newcomer_can_commit`・`recipe_doable`）。`c4_flow_follows_rules` だけなら 0.6。主張の文が定理より強い（M5） |
| C5 | 0.05（hypothesis） | 0.05 に同意（`newcomer_not_admin`）。新人の権限の事実が集まっても、M3 の書き換えで上限は 0.75。定理の前提が主張の条件より強い（M4） |

手戻りの一覧（私の書き換えのあと）: `main_entry_has_op`・`approval_covers_content`・`approver_not_author`・`approved_change_can_break`・`newcomer_can_commit`・`recipe_doable`・`newcomer_not_admin` の7個。

## 手がかりへの見立て（hints.json）

- `single_atom_claim`（`c1_direct_push_unreviewed_release`、値を決める公理は `main_feeds_release` だけ）: 言い換えではないと判断した。`main_feeds_release` は「main に入った変更は、本番に出る候補になる」という main の役割についての一般の性質で、直接の書き込みも承認も含まない。主張の「未レビューのまま」の部分は、語の定義（`direct_write_skips_pr`）から来る。`@restates` は付けていない。ただし、「main から本番に出す」という社内のリリースの仕方は F2 から読み取っているだけなので、ステージ6でユーザーの証言として登録すると支えが直接になる。
- `unused_axiom` の5つ（`push_joins_pr`・`squash_brings_all_pr`・`pushed_after_not_seen`・`approved_change_can_break`・`admin_exempt_by_default`）: どれも [不利] の定理（U1・U2・U4）だけが使う。設計書5節のとおりで、問題ではない。
- 手がかりに出なかったが見たもの: 【自明】8つに強い仮定は紛れていない（`direct_write_skips_pr`・`pushed_after_not_seen` は語の定義）。`commit_keeps_main` は【実験】F5 だが、F5 は手元の main についての確認で、GitHub の main が変わらないことは commit が手元の操作であることから自明に言える。値には効かない。

## 比較の公平さ

- 比較の文の主張はないので、失敗の台帳（ledger.json）はない。対比の相手の「直接 push」は、先月2回現実に起きた行動（F1・F2）で、藁人形ではない。
- 設計書4節は、「同じとみなす」置き方がすべて主張に有利な向きに片寄っていることを自ら書き、証拠のないものは 0.05 になると約束していた。そのうち `approval_covers_content` だけが 0.7 のまま残っていたので、M2 で下げた。
- 不利な結論 U1〜U4 は、有利な向きの弱い仮定を経由していない（U2 の `broken_main_stops_team`、U4 の `unrejected_push_lands` は、そこでは不利な向きに働く）。ただし U1（0.95）は、H2 のとおり C3 そのものを字義どおりの読みで破る結論で、「限界」にとどまらない。

## 書き手の振る舞い

- 設計書との違い5点（Argument.lean の冒頭）を確かめた。`bringing_enters_main` は語の定義として【自明】でよい。`merge_content_origin` に前提を足したのは公理を弱める向きで、問題はない。証人の世界を豊かにしたことで、関係公理の前提が成り立つ例ができた（よい変更）。ただ、その結果わかった「C3 の前提が証人で成り立たない」ことは、設計書との違いにも問題としても書かれていなかった（H1）。
- 検査を通すためのラベルの変更や、公理の省略は見当たらなかった。
- Writer への注意: 私が書き換えたのは `Argument.lean` の3つの公理の docstring（`@confidence` と `@reviewer`）だけで、`Model.lean` の同じ docstring は古いまま（`approval_covers_content` は `@confidence 0.7`、保護の2つは `@confidence` なし）。門（LG022）は docstring を比べないので通るが、2周目に `Model.lean` から docstring を写し戻すと `@reviewer` の行が消える。写すのは `Argument.lean` から `Model.lean` への向きだけにする。
