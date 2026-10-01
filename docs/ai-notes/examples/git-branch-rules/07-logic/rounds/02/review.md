判定: 条件付き合格（高 0・中 3・低 4）

# 監査の報告（2周目・局所修正）: 新人向け Gitブランチ運用ルール

監査した版: `Argument.lean`・`Model.lean`（門のエラー 0）、`report.json`・`hints.json`、`diff.md`（rounds/01 → いま）、`model-plan-delta.md`。
私の書き換えは、`c1_direct_push_can_stop_team` に `@restates` を1行足しただけです。確信度は下げていません。書き換えのあと `cyrus lean` を実行し、門のエラーが 0 のままであることを確かめました。

## 要点

- **1周目の高の指摘は、2つとも解消した。** H1（C3 の前提がいつも偽）は、`FollowsFlow` を月ごとにしたことで解消した。証人では、新人がどの月も流れを守り、今月 main に変更を入れる。前提が公理から否定できないことは、Lean で確かめた（下の「証人と前提の検査」）。H2 は、ステージ5でユーザーが「再レビュー込み」と決めた。
- **残るのは言い回しの差（M7、中、ステージ5）。** C3 の括弧書きは「もう一度レビューを**頼む**」、モデルの流れは「承認を**受け直してから**マージする」。字義どおり「頼むだけ」と読むと、C3 は U1（確信度 0.95）で偽になる。C0 の文には再レビューがまったくない。ステージの終わりに、M5 と一緒にユーザーに確かめる。
- **保護の2つの公理は、命題が変わったのに名前と `@reviewer` が残った（M8、中）。** 新しい命題は F4 がそのまま支える形になり、1周目に私が下げた理由はもう当たらない。しかし Reviewer は値を上げられないので、0.75 のまま固定されている。名前を変えて、改めて監査する。
- 主張の値は、どれも1周目と同じ（C1・C2 が 0.6、ほかは 0.05）。この周で高の指摘は 0 なので、`cyrus logic-round close` はループを止める見込み。手戻りの一覧は7個。

## 指摘の表

| ID | 対象 | 重大度 | 監査項目 | 要点 | 戻す先 |
|---|---|---|---|---|---|
| M5（1周目から） | `c4_newcomer_can_do_own_steps`、C4 | 中 | 12 | C4 の文「新人でも最初から最後まで自分で進められる」は、定理より強い。定理は、承認を除いた操作についてだけ言う（U3）。差分の設計書9節で、ステージの終わりにユーザーに見せることになった。その扱いでよい | ステージ5 |
| M7 | `FollowsFlow` の (c)、`c3_own_changes_approved_by_other`、`c3_own_changes_reviewed_by_other`、`c0_team_flow`、C3・C0 の文 | 中 | 12・1 | 下の「M7 について」 | ステージ5 |
| M8 | `protection_rejects_push`、`protection_only_approved_pr` | 中 | 15・4 | 下の「M8 について」 | Planner（名前を変える）・Writer |
| L5（1周目から） | `approved_change_can_break`、`u2_reviewed_change_can_stop_team` | 低 | 10 | 手戻りの一覧で `claims` が空なので、後回しにされやすい。U2 は 01-intent.md の「自分の変更で他の人の作業を壊さずに済む」に歯止めをかける唯一の定理。ステージ6で、承認を受けてマージした変更がビルドを壊したことがあるかも確かめる | ステージ6 |
| L7 | `approver_not_author`、`approved_change_can_break`、`newcomer_can_commit`、`recipe_doable` | 低 | 15 | 下の「L7 について」 | Writer |
| L8 | 証人（`Model.lean` の末尾） | 低 | 18・19 | ガイドは、主張の定理の前提が成り立つことを示す `example` を、`Model.lean` の末尾に足して記録するよう求めている。Writer は写しで確かめただけで、本体に置いていない（`Model.lean` の冒頭にそう書いてある）。私が写しで確かめた5つ（下の「証人と前提の検査」）を、末尾に置く | Writer |
| L9 | `pushedAfterApproval`、`pushed_after_not_seen`、`approvedBy`、`FollowsFlow` の (c) | 低 | 6・1 | 下の「L9 について」 | Planner |

### M7 について（ステージ5で確かめること）

- 05-claims.json の C3 は「承認のあとに commit を足したら、もう一度レビューを頼むことを含む」。`FollowsFlow` の (c) は「`q` の最後の承認のあとに push された変更がない」、つまり「承認を受け直してからマージする」。
- 「頼むだけで、古い承認のままマージしてよい」と読むと、C3 は偽になる。U1（0.95）により、最後の承認のあとに足した commit は、承認した人に見られないまま main に入る。C3 が成り立つ読みは「受け直してからマージする」だけである。これは差分の設計書0節の論証のとおりで、私も別の読みを見つけられなかった（今月はブランチ保護がないので、古い承認を取り消す設定に頼る読みも成り立たない）。
- C0 の文「1名以上の承認を受けてから、自分で squash merge」には、再レビューがまったくない。一方 `c0_team_flow` は、C3 と同じ `FollowsFlow` を「この流れ」として使う。差分の設計書10節は「C0 の文は流れの要約」と読んだ。読みとしては無理がないが、ユーザーが承認した文とモデルの流れが、文の上では一致していない。
- 高にしない理由: ユーザーは1周目の H2（字義どおりの流れでは C3 が破れる）を見たうえで「再レビュー込み」と決めた。残っているのは言い回しの差で、モデルの読みは、C0 の「承認を受けてからマージ」とも合う。ただし、ユーザーの意図が「頼むだけ」なら、C3 は偽で、主張を決め直す必要がある。
- ユーザーへの問い（1問にまとめた）:「C3 の括弧書きと C0 の手順に、『承認のあとに commit を足したら、もう一度レビューを頼み、**承認を受け直してから**マージする』と書いてよいか」。
- 進め方: この周は高が 0 なので、周は止まる見込み。周を止めて戻る必要はない。ステージの終わりの手戻りで、M5 と一緒にユーザーに見せれば足りる。文が変わっても、モデルの `FollowsFlow` は変えなくてよい。

### M8 について（保護の2つの公理の名前）

- 差分の設計書 A5 は、2つの公理の型の「管理者でない」（`¬ isAdmin p`）を「保護を迂回できない」（`¬ bypassesProtection p`）に替え、名前と `@reviewer` の行を残した。ガイドは「公理の命題（型）を変えるときは、名前も変えて別の公理にする。前の公理の `@reviewer` の判断は引き継がない」としている。呼び出し元の説明では、この決まりは差分の設計書を書いたあとにガイドに足された（ガイドの更新時刻も差分の設計書より後で、説明と矛盾しない）。そうなら Planner の落ち度ではない。ただし直す必要はある。
- 残った `@reviewer` の理由文は、古い命題（「管理者でない人は、だれでも拒否される」）について書いたもので、いまの命題文や弱い点と食い違っている。
- いまの命題についての私の見立て（名前を変えたあと、改めて監査する前提での見込み。値は確定させない）: `bypassesProtection` が F4 の「管理者など」の「など」を含むようになったので、1周目に下げた理由（M3）は当たらない。`protectedMain` が「承認数1以上」を含むようになった（D8）ので、`protection_only_approved_pr` の「承認を得た」も、F4 の1つ目の引用（"collaborators can only push changes to a protected branch via a pull request that is approved by the required number of reviewers"）がそのまま支える。いまのところ、下げる理由は見当たらない。
- 値への効き方: C5 の値は、いまは `newcomer_no_bypass`・`next_month_block_requires_pr`（0.05）で決まる。事実が集まったあと、C5 の上限はこの2つの 0.75（moderate）になる。名前を変えて監査し直せば、0.95（assert）まで上がりうる。
- 直し方: 次の局所修正（ステージ6の手戻りのあと）で、名前を変える。候補は `protection_rejects_nonbypasser_push`・`protection_nonbypasser_only_approved_pr`。`@reviewer` の行は新しい公理に写さない。`c5_only_pr_route_when_protected` の証明と、`Model.lean` の同じ名前の定義も合わせて変える。
- `approval_covers_content` も、D3 で述語の意味（「最後の承認」）が変わり、型と名前は同じまま `@reviewer` が残った。こちらは、私の理由（F6 は承認する人の振る舞いを述べていない）が新しい意味にもそのまま当たるので、変えなくてよい。

### L7 について（Writer が【仮定】の案を 0.05 にしたこと）

- `Argument.lean` の冒頭「設計書との違い」の4で、Writer は支える事実のない【仮定】4つの `@confidence` を、案から 0.05 に下げた（`approver_not_author` 0.8、`approved_change_can_break` 0.5、`newcomer_can_commit` 0.6、`recipe_doable` 0.5）。理由は「案も 0.05 と書く決まりに合わせた」。
- ガイドの決まりは逆である。「支える事実がない【経験則】【仮定】は、案によらず 0.05 になる。案を 0.05 に書き換える必要はない（事実が集まったときの見込みとして残してよい）」。
- いまの値は変わらない。しかし、ステージ6で事実を集めて `@support` を足しても、CLI の値は案と事実の値の小さいほうなので、0.05 のまま上がらない。差分の設計書11節の見込み（`approver_not_author` の事実が集まれば、C3 の承認の項は 0.8 まで上がる）とも食い違う。
- 記録は残っていて、検査を通すための書き換えでもないので、低にした。ステージ6の手戻りのあとの局所修正で `@support` を足すときに、案を元に戻す。

### L9 について（「最後の承認のあとに push された」の読み）

- (i) `pushed_after_not_seen`（【自明】）は、「最後の承認のあとに push された変更は、最後の承認の時点では入っていなかった」と言う。ところが `pushedAfterApproval` は「最後の承認のあとに push された」なので、承認のあとに rebase して強制的に push し直した場合、同じ中身の変更が「承認の時点で入っていた」と「承認のあとに push された」の両方に当たる。そのときこの公理は成り立たない。`pushedAfterApproval` を「最後の承認のあとに**初めて**プルリクエストに加わった（push でも、画面の操作でも）」と定義し直せば、【自明】でよくなる。この公理を使うのは U1（不利な結論）だけで、U1 の中身（新しく足した commit は見られていない）は変わらないので、確信度は下げなかった。
- (ii) (c) は、自分の操作ではなく、プルリクエストの状態についての条件である。ほかの人の push、画面の「Update branch」、提案を取り込む commit も、(c) に当たる。本文では「承認のあとに commit が増えていたら（自分が足したものでなくても）、もう一度レビューを頼み、承認を受け直す」と書くよう、Planner は差分の設計書7節の注意に足す。
- (iii) `approvedBy` は「1回以上承認した」なので、承認のあとに同じ人が「変更を求める」レビューに変えた場合や、承認が取り消された場合を区別しない。C3 の結論（その時点で見て承認した）は崩れないので、今は直さなくてよい。本文の「承認を受けてから」は、承認が生きている状態を指すと読まれる。

### 差分の設計書10節（Reviewer へ）への答え

- (c) の読み: 「承認を受け直してからマージする」のほかに、C3 が成り立つ読みは見つからなかった。文との差は M7。
- C0 の文: 「C0 は流れの要約」という読みに無理はないが、ユーザーが承認した文と一致させる（M7 の問いに含めた）。
- C3 の2つの項: 「レビュー」を「承認した人が中身を見たうえで承認した」（`reviewedBy`）と読むのでよい。C3 の文は「レビュー**と**承認」を並べている。「レビュー」を「提示されて承認された」と読むと、2つの語が同じことを指してしまう。中身を見たと読むのが文の形に合い、04-analysis.md の「もう一度見てもらうよう勧める」とも合う。したがって T4（`c3_own_changes_reviewed_by_other`）は主張より強くなく、`@claim C3` のままでよい。ステージ5で確かめる必要はない。
- 消した宣言: `main_entry_has_op`・`c3_flow_reviews_every_entry`・`incident_direct_push_broke_build` を棄却として扱わないことに同意する（下の「`@against` を付けた公理と、棄却を提案する公理」）。
- 保護の2つの公理: M8。

## 1周目の指摘ごとの状態

| ID | 状態 | 確かめたこと |
|---|---|---|
| H1 | 解消 | `FollowsFlow` を `Month → Person → Prop` にし、(a)(b)(c) をその月だけにした（D1）。先月の事故は「先月、その人は守っていなかった」（U5）とだけ両立する。読み (i) のための `main_entry_has_op` と `c3_flow_reviews_every_entry` は消えた。証人で前提が成り立つことを Lean で確かめた |
| H2 | 一部（M7 に引き継ぐ） | ステージ5でユーザーが「再レビュー込み」と決め、`FollowsFlow` の (c) の説明は C3 の括弧書きに合わせて書き直された（D2）。「頼む」と「受け直してからマージ」の差と、C0 の文が残る |
| M1 | 解消 | ユーザーが読み (ii)（自分が守れば、自分が main に入れる変更は）を選んだ。C3 の2つの定理はこの読みで、`main_entry_has_op` を使わない |
| M2 | 解消（事実はステージ6） | C3 を「承認の項」（T3）と「レビューの項」（T4）に分けた。T3 は `approval_covers_content` を使わない。`approval_covers_content` に要ファクトが足された。値は事実が集まるまで 0.05 |
| M3 | 解消（M8 が残る） | `bypassesProtection`・`bypassDisallowed`・`newcomer_no_bypass`・`bypass_exempt_by_default` で、F4 の「管理者など」を表せるようになった。名前の扱いは M8 |
| M4 | 解消 | C5 の定理の前提を `directPushBlocked .nextMonth`（直接 push を拒否する設定が入る）にし、「その設定は承認1名以上の保護である」という判断を【仮定】`next_month_block_requires_pr`（0.05、要ファクトあり）に移した。定理の引数に判断が残っていない |
| M5 | 残る（ステージ5） | モデルは変えず、ステージの終わりにユーザーに見せる（差分の設計書9節）。その扱いでよい。表に残した |
| M6 | 解消 | `c1_direct_push_can_stop_team` は【実験】F1 の `incident_direct_push_stopped_team` だけで示す。全称の `broken_main_stops_team` は C2 と U2 だけが使う。言い換えであることは意図どおりなので、`@restates` を付けた |
| L1 | 解消（L9 に続きを書いた） | `approvedBy`・`inPRWhenApproved`・`pushedAfterApproval` を「最後の承認」を基準にした（D3）。(c) が「受け直してからマージ」を表せるようになった |
| L2 | 解消 | `hasCheckedRecipe`（証拠の側の性質）を `hasFixedRecipe`（決まった操作がある）に替えた。確かめたことは `@support` と論拠に移った |
| L3 | 解消（採らない理由を認める） | 「知っておく必要がある」は規範の部分で、1周目1節で C0 の「採るべきだ」と同じく関係公理にしないと決めた部分。本文を「来月も、新人が main に入れる道はこの流れだけ」にとどめる注意が差分の設計書7節にある |
| L4 | 解消 | `pushRejected` の説明と `unrejected_push_lands` の弱い点が直った |
| L5 | 残る（ステージ6） | モデルは変えない。表に残した |
| L6 | 解消 | 証人で、人 2（保護を迂回できる人）が来月直接 push しようとし、拒否されずに入る。U4 の前提が成り立つ |

## 確信度を下げた公理

この周は、どの公理も下げていません。新しく足された公理と、命題が変わった公理について、下げなかった理由を残します。

| 公理 | 値 | 下げなかった理由 |
|---|---|---|
| `incident_direct_push_stopped_team` | 0.6 | F1（「直接 push した1回目の事故で、ビルドが壊れ、半日チーム全員の作業が止まった」）がそのまま述べる。1件からの存在の命題で、一般化を含まない。値は F1 の user_asserted で決まる |
| `next_month_block_requires_pr` | 0.05 | 支える事実がなく、すでに 0.05。`@support` の「なし」の理由（F3 は設定の種類と承認数を述べない）も正確 |
| `newcomer_no_bypass` | 0.05 | 支える事実がなく、すでに 0.05 |
| `bypass_exempt_by_default` | 0.95 | F4 の2つ目の引用（"By default, the restrictions of a branch protection rule don't apply to people with admin permissions"）が管理者について直接支える。迂回の権限を持つ役割については、`bypassesProtection` の意味（保護の制限を受けない立場）から言える。弱い点にもそう書いてある。使うのは U4（不利な結論）だけ |
| `protection_rejects_push`・`protection_only_approved_pr` | 0.75 | 命題が変わった。下げる理由は見当たらない。値が 0.75 に固定されている問題は M8 |
| `approval_covers_content` | 0.05 | 述語の意味が「最後の承認」に変わったが、1周目の理由がそのまま当たる。すでに 0.05 |
| `merge_content_origin` | 0.8 | 「最後の承認」に変わっても、F6・F8 の支え方は同じ。画面の操作で中身が変わる場合は弱い点にある（L9 の (ii) と同じこと） |
| `recipe_*` の7つ（【実験】） | 0.95 | 命題が「決まった操作があり、動きを確かめてある」から「決まった操作がある」に弱まった。各事実（F8・F10・F12〜F15）が操作の存在を述べている |
| `recipe_doable` | 0.05 | 支える事実がなく、すでに 0.05 |
| `pushed_after_not_seen` | 1（【自明】） | L9 の (i) のとおり、いまの定義の言い回しでは、push し直した場合に成り立たない。定義を直せば【自明】でよく、使うのは U1 だけで、U1 の中身は変わらないので、下げずに Planner に戻す |

## `@against` を付けた公理と、棄却を提案する公理

- `@against` は付けていない。06-facts.json に、どの公理にも反対の向きを述べる事実はない。反対の証拠の候補もない。
- 棄却を提案する公理はない。消えた `main_entry_has_op`・`incident_direct_push_broke_build` は、誤りと分かったのではなく、主張の読みが変わって要らなくなったか、置き換えられたもの。`rejected.json` に入れないのは正しい。

## 付けた印

- `c1_direct_push_can_stop_team` に `@restates incident_direct_push_stopped_team` を付けた。C1 の「全員の作業を止める危険」は、F1 の事故1件がそのまま示す。1周目の M6 で、事実から直接示すよう求めた形なので、言い換えであることは意図どおり。

## 主張ごとの見立て

| 主張 | report.json の値 | 見立て |
|---|---|---|
| C0 | 0.05（hypothesis） | 0.05 に同意。C3 の項はもう空回りしていない。C0 の文に再レビューがないこと（M7）を、ステージの終わりに確かめる。本文への注意: 直接の書き込みを「マージ以外のすべて」と定義した（D4）ので、モデルの流れは、GitHub の画面で main に直接 commit することも含めて禁じている。C0 の「変更は…squash merge して main に取り込む」はこれを含むと読めるが、本文で「main に直接 push しない」だけを書くと、画面の編集で「main に直接 commit する」を選ぶ道が残る。ステージ8〜11で「main を直接変えない（画面での直接 commit も含む）」と書くか決める |
| C1 | 0.6（moderate） | 0.6 に同意（F1・F2 は user_asserted）。1つ目の定理は F1 の言い換えで、意図どおり（`@restates` を付けた）。2つ目は1周目と同じく言い換えではない |
| C2 | 0.6（moderate） | 0.6 に同意。変更なし。Writer が証人に今月の直接 push の例（人 3・変更 4）を足し、C2 の定理の前提が成り立つ例ができた（よい変更） |
| C3 | 0.05（hypothesis） | 0.05 に同意。前提は証人で成り立ち、何かを言う定理になった。承認の項は `approver_not_author`、レビューの項は `approval_covers_content` の事実待ち。承認の項は、事実が集まれば `merge_content_origin`・`approve_keeps_main` の 0.8 まで上がりうるが、L7 の案を戻さなければ上がらない。主張の文との差は M7 |
| C4 | 0.05（hypothesis） | 0.05 に同意。主張の文が定理より強い（M5）は残る |
| C5 | 0.05（hypothesis） | 0.05 に同意。前提が主張の条件（「仕組みで直接 push が拒否されるようになっても」）と一致した（M4 解消）。事実が集まったあとの上限は、M8 が残るかぎり 0.75 |

手戻りの一覧（いま）: `approval_covers_content`・`approver_not_author`・`approved_change_can_break`・`newcomer_can_commit`・`recipe_doable`・`newcomer_no_bypass`・`next_month_block_requires_pr` の7個。差分の設計書11節の見込みと同じ。

## 証人と前提の検査（監査項目 18・19）

- `Model.lean` の写しの末尾に次を足し、`lean` でコンパイルできることを確かめた（終了コード 0。写しは作業用の場所に置き、本体には足していない）。
  - `∀ m, FollowsFlow m newcomer`（C3・U3 の前提。どの月も新人は流れを守る）
  - `∃ c, bringsInVia .thisMonth newcomer .squashMerge c`（その月に main に入れる変更がある）
  - `∃ pr q, squashMerges .thisMonth newcomer pr ∧ approvedBy pr q ∧ q ≠ newcomer ∧ reviewedBy 1 q`（C3 の結論に実例がある）
  - `directPushBlocked .nextMonth`（C5 の前提）、`noConflict`（C4 の前提）、`triesDirectPush .thisMonth 3 4`（C2 の前提）
- 証人はすべての公理を満たす（門で確かめ済み）。その世界で前提が真なので、前提は公理から否定できない。1周目の H1 のような空回りはない。
- 関係公理の空回り: 前提を持つ公理は、証人でどれも前提が成り立つ例がある。`merge_content_origin` は2つの枝の両方（プルリクエスト 0 の変更 1、プルリクエスト 1 の変更 2）、保護の2つの公理は来月の人 2 以外、`bypass_exempt_by_default` は人 2、`unrejected_push_lands` は3か月それぞれ、`approval_covers_content` は変更 1 と人 1。
- 記録が本体にない点は L8。

## 手がかりへの見立て（hints.json）

- `single_atom_claim`（`c1_direct_push_can_stop_team`）: 言い換え。意図どおりなので `@restates` を付けた（「付けた印」）。この手がかりは `@restates` を付けても消えない（CLI は `proof_is_axiom` の手がかりにだけ印を反映する）。
- `single_atom_claim`（`c1_direct_push_unreviewed_release`）: 1周目と同じく言い換えではない。`main_feeds_release` は main の役割についての一般の性質で、「承認を通らない」の部分は語の定義（`direct_write_skips_pr`）から来る。
- `used_only_by_unmarked_theorems` の5つ（`push_joins_pr`・`squash_brings_all_pr`・`pushed_after_not_seen`・`approved_change_can_break`・`bypass_exempt_by_default`）: どれも U1・U2・U4 だけが使う。設計どおりで、問題ではない。

## 比較の公平さ

- 比較の文の主張はないので、失敗の台帳はない（1周目と同じ）。
- 「同じとみなす」置き方は、まだ主張の側に片寄っている。この周で足された `next_month_block_requires_pr` も主張の側だが、証拠がなく 0.05 で、手戻りの一覧に入っている。
- 不利な結論: U5（新しい）は F1 と語の定義だけで導かれ、有利な向きの仮定を通らない（0.6）。U4 は `bypass_exempt_by_default`（0.95）と `unrejected_push_lands`（0.6）で、不利な向きに働く。U3 は `approver_not_author`（0.05）を通るが、1つ目の項（承認は本人の操作ではない）は文書の手順の定義から出る。U1 は 0.95 のままで、流れに「受け直してからマージ」を入れる根拠になっている。
- 保護の2つの公理（0.75）と `bypass_exempt_by_default`（0.95）は同じ F4 に支えられているのに値が違う。低いほうは主張の側（C5）の公理で、主張に不利な向きの食い違いなので、片寄りではない（M8 で直す）。

## 書き手の振る舞い

- 差分の設計書の31行は、どれも宣言の変更に当たっていた（diff.md の対応表）。設計書に名前の出ていない変更は、【仮定】の案を 0.05 にした3つ（と `recipe_doable`）だけで、「設計書との違い」の4に記録されている（L7）。
- 私が付けた `@reviewer` の行（`approval_covers_content`、保護の2つ）は、どれも残っていた。Writer が行を消して値を戻したところはない。
- 検査を通すためのラベルの変更や、公理の省略は見当たらなかった。消えた公理（`main_entry_has_op`・`incident_direct_push_broke_build`・`isAdmin` の系列）は、どれも差分の設計書に理由がある。
- 証人に設計書にない例（今月の人 3 の直接 push）を足したことは、「設計書との違い」の5に記録されている。C2 の前提が成り立つ例になり、よい変更。
