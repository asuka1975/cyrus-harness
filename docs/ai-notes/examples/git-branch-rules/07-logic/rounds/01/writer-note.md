# Writer の作業の報告（1周目）

## 書いたもの

- `07-logic/Argument.lean`: 設計書（`model-plan.md`）の2節の宣言・def、3節の関係公理、5節の定理を、そのまま Lean にした。
  - §1 帰納型6つ（`Month`・`Op`・`BranchPrefix`・`WorkKind`・`MergeMethod`・`Merger`）。
  - §2 宣言33（型3つと、定数・関係30）。
  - §3 def 8つ（`teamFlow`・`doneByAuthor`・`flowPrefix`・`flowMergeMethod`・`flowMerger`・`flowMinApprovals`・`directlyWrites`・`FollowsFlow`）。
  - §4 関係公理46（【自明】8・【実験】23・【経験則】9・【仮定】6）。設計書3節の45に、`bringing_enters_main` を1つ足した（下の「設計書との違い」1）。
  - §5 定理14。`@claim` の定理9つ（C0 1・C1 2・C2 1・C3 1・C4 2・C5 1）、印なしの補題1つ（`flow_changes_main_only_by_merge`）、印なしの [不利] 4つ（`u1_`〜`u4_`）。
  - `@confidence` には設計書3節の案を、そのまま書いた。【実験】と【自明】には書いていない（設計書どおり）。
  - `@support なし（…）` の括弧の中には、事実 ID を書いていない（CLI がその行の ID を支えの事実として読むため）。
- `07-logic/Model.lean`（証人）: `Argument.lean` の axiom 79 個を、同じ名前・同じ型の `abbrev`（型3つ）・`def`（定数と関係30）・`theorem`（関係公理46）に差し替えた。
  axiom 以外の行は、`Argument.lean` から機械的に写した（冒頭の説明のコメントだけ差し替えた）。
  - 2周目から証人を直すときの注意: 門（LG022）は、`namespace` の行から後の、axiom 以外のコードの行（コメントと docstring を除く）が `Argument.lean` と1字も違わず同じ順で並ぶことを求める。
    `Argument.lean` の定義・定理・証明の行を変えたら、`Model.lean` の同じ行も同じに直し、差し替えるのは axiom の行だけにする。

## 設計書との違いと理由

`Argument.lean` の冒頭の「設計書（model-plan.md）との違い」と同じ内容。

1. **`bringing_enters_main`（【自明】）を足した。** `main_feeds_release`・`broken_main_stops_team` は「main に入った変更」（`entersMain`）についての公理だが、
   それを使う C1・C2・U2 の定理は「直接書き込んだ」「squash merge で入れた」（`bringsInVia`）から出発する。設計書には `entersMain → ∃ bringsInVia`（`main_entry_has_op`）の向きしかなく、
   逆の向きがないと定理を示せなかった。「その操作で、その変更を main に入れる」から「その変更が main に入る」は語の定義として言えるので【自明】にした。
   別の書き方として、2つの公理を `bringsInVia` で直接書く方法もあったが、設計書の「main に入った変更」という文に合わせるため、こちらにした。確信度には効かない（【自明】は 1）。
2. **`merge_content_origin` に前提 `approvedBy pr q` を足した。** 「承認の時点」は承認した人がいて初めて決まるため。設計書の文より弱い公理になる。
3. **`u3_merge_needs_another_person` は、`doneByAuthor .approve = false` を結論の `∧` の1項目にした。** 設計書の「あわせて」を1つの定理にまとめた。
4. **帰納型に `deriving DecidableEq` を付けた。** `c0_team_flow` の `.directWriteMain ∉ teamFlow` を `decide` で示すためと、証人の証明のため。
5. **証人の世界を、設計書5節の見通しから変えた。** 見通しでは `approvedBy`・`pushedAfterApproval`・`isAdmin`・`protectedMain` がいつも偽で、
   `merge_content_origin`・`approval_covers_content`・`approver_not_author`・`push_joins_pr`・`pushed_after_not_seen`・`protection_rejects_push`・`protection_only_approved_pr`・`admin_exempt_by_default` の前提が一度も成り立たない。
   証人では次の世界にした。
   - 人: 0 新人（流れを守る）、1 レビューする人（承認だけ）、2 管理者、3 流れを守らない人（先月、main に直接書き込んだ）。
   - 変更: 0 は人 3 の直接の書き込みでビルドを壊す。1 はプルリクエスト 0 に承認の時点からあった。2 はプルリクエスト 1 に承認のあとに push され、ビルドを壊す。
   - プルリクエスト: 0 は新人が出して squash merge、1 は人 3 が出して squash merge。どちらも人 1 が承認。
   - 月: 来月だけ保護が有効（管理者には効かない）。
   これで、上の公理の前提が成り立つ例がある。`FollowsFlow` は人 0・1・2 で成り立ち、人 3 で成り立たないことを、`Model.lean` の写しに `example` を足して Lean で確かめた（本体には足していない）。
   したがって証人の世界では、C3 の前提「全員が流れを守る」は成り立たず、C3 の定理は証人の中では空回りする。
   先月の直接の書き込み（`incident_direct_push_broke_build`）がある世界では、`FollowsFlow` が月を問わないので、全員が流れを守る世界は作れない。

## 門の結果

`python3 .claude/skills/cyrus/scripts/cyrus.py --doc git-branch-rules lean`: エラー 0 件・警告 0 件・参考 0 件。
証人: axiom 79 個すべての型が一致、写しの欠け 0 行、Lean 標準の公理以外への依存なし。

主張ごとの確信度（設計書1節の見込みと同じ）:

| 主張 | 確信度 | 値を決める公理 |
|---|---|---|
| C0 | 0.05 | 証拠のない【仮定】（`main_entry_has_op`・`approver_not_author`・`newcomer_can_commit`・`recipe_doable`・`newcomer_not_admin`） |
| C1 | 0.6 | `incident_direct_push_broke_build`・`broken_main_stops_team`・`main_feeds_release`（F1・F2 が user_asserted） |
| C2 | 0.6 | `no_rejection_this_month`・`unrejected_push_lands`・`broken_main_stops_team`・`main_feeds_release`（F1〜F3 が user_asserted） |
| C3 | 0.05 | `main_entry_has_op`・`approver_not_author` |
| C4 | 0.05 | `newcomer_can_commit`・`recipe_doable`（`c4_flow_follows_rules` だけなら 0.6） |
| C5 | 0.05 | `newcomer_not_admin` |

主張の定理が使わない公理は5つ（`push_joins_pr`・`squash_brings_all_pr`・`pushed_after_not_seen`・`approved_change_can_break`・`admin_exempt_by_default`）。
どれも [不利] の定理だけが使うもので、設計書6節のとおり。
[不利] の定理の値: U1 0.95、U2 0.05、U3 0.05、U4 0.6。

## 検査が誤っていると思う点

なし。門のエラーを避けるために、ラベル・公理・定理の形を変えたところはない。
