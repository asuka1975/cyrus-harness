/-!
# 論証構造: 新人向け Gitブランチ運用ルール

cyrus が 05-claims.json と 06-facts.json から作った雛形です。
- 事実（fact_）の確からしさは 06-facts.json の status から自動で決まります。
- 推論規則（rule_）には `@confidence 0〜1` と、その推論が成り立つ理由を書いてください。
- 隠れた前提に気づいたら assume_ 公理として明示し、確からしさを付けてください。
- 主張（P_C…）そのものを公理にしてはいけません。theorem claim_… として導きます。
-/

-- ========== 命題 ==========
/-- F1: 先月、新人が main に直接 push した1回目の事故では、ビルドが壊れ、半日チーム全員の作業が止まった。 -/
axiom P_F1 : Prop
/-- F2: 先月、新人が main に直接 push した2回目の事故では、未レビューの変更が本番に出かけ、リリース直前に気づいて戻した。 -/
axiom P_F2 : Prop
/-- F3: 社内の GitHub では、main への直接 push を拒否する設定に来月変える予定で、今はまだ拒否されない。 -/
axiom P_F3 : Prop
/-- F4: GitHub のブランチ保護ルールで「Require a pull request before merging」を有効にすると、main などの保護したブランチには、プルリクエストを通して承認を得た変更しか入れられなくなる。ただし初期設定では、リポジトリの管理者などにはこの制限が効かない。 -/
axiom P_F4 : Prop
/-- F5: 作業ブランチに commit しても、main ブランチの内容は変わらない。 -/
axiom P_F5 : Prop
/-- F6: GitHub のプルリクエストは、あるブランチで行った変更を別のブランチ（main など）へマージするよう提案する機能で、マージする前に変更を話し合い、レビューできる。 -/
axiom P_F6 : Prop
/-- F7: 社内では、プルリクエストをマージするには1名以上の承認が必要である。 -/
axiom P_F7 : Prop
/-- F8: プルリクエストを出したあとに同じブランチへ commit を push すると、その commit はプルリクエストに自動で加わる。 -/
axiom P_F8 : Prop
/-- F9: 社内の作業ブランチの名前は feature/<内容> または fix/<内容> とする。 -/
axiom P_F9 : Prop
/-- F10: git switch -c <ブランチ名> で、今いる場所から新しいブランチを作り、そこに移れる。 -/
axiom P_F10 : Prop
/-- F11: 社内では、承認後にプルリクエストを出した本人が squash merge でマージする。 -/
axiom P_F11 : Prop
/-- F12: GitHub の squash merge は、プルリクエストの commit を1つの commit にまとめて取り込み先のブランチに加える。 -/
axiom P_F12 : Prop
/-- F13: git push -u origin <ブランチ名> で、手元の作業ブランチを GitHub（リモート）に送り、同じ名前のブランチを作れる。 -/
axiom P_F13 : Prop
/-- F14: GitHub の画面で、push したブランチからプルリクエストを作り、レビューする人（Reviewers）を指定できる。 -/
axiom P_F14 : Prop
/-- F15: git switch main のあと git pull を実行すると、手元の main がリモートの最新の状態になる。 -/
axiom P_F15 : Prop
/-- C0: 変更は main に直接 push せず、作業ブランチを切り、プルリクエストを出し、1名以上の承認を受けてから、自分で squash merge して main に取り込む。 -/
axiom P_C0 : Prop
/-- C1: main への直接 push は、チーム全員の作業を止めたり、未レビューの変更を本番に出しかけたりする危険がある。 -/
axiom P_C1 : Prop
/-- C2: 直接 push は今月はまだ仕組みで止められないので、一人ひとりが流れを守る必要がある。 -/
axiom P_C2 : Prop
/-- C3: この流れを守るかぎり、main に入る変更はすべて、マージ前にほかの人のレビューと承認を通る。 -/
axiom P_C3 : Prop
/-- C4: コンフリクト（同じ箇所の変更の衝突）が起きなければ、社内の決まりに沿った手順で、新人でも最初から最後まで自分で進められる。 -/
axiom P_C4 : Prop
/-- C5: 来月、仕組みで直接 push が拒否されるようになっても、この流れを知っておく必要がある。 -/
axiom P_C5 : Prop

-- ========== 事実（Fact Verification の結果） ==========
/-- @fact F1 status=user_asserted confidence=0.6 -/
axiom fact_F1 : P_F1
/-- @fact F2 status=user_asserted confidence=0.6 -/
axiom fact_F2 : P_F2
/-- @fact F3 status=user_asserted confidence=0.6 -/
axiom fact_F3 : P_F3
/-- @fact F4 status=verified confidence=0.95 -/
axiom fact_F4 : P_F4
/-- @fact F5 status=verified confidence=0.95 -/
axiom fact_F5 : P_F5
/-- @fact F6 status=verified confidence=0.95 -/
axiom fact_F6 : P_F6
/-- @fact F7 status=user_asserted confidence=0.6 -/
axiom fact_F7 : P_F7
/-- @fact F8 status=verified confidence=0.95 -/
axiom fact_F8 : P_F8
/-- @fact F9 status=user_asserted confidence=0.6 -/
axiom fact_F9 : P_F9
/-- @fact F10 status=verified confidence=0.95 -/
axiom fact_F10 : P_F10
/-- @fact F11 status=user_asserted confidence=0.6 -/
axiom fact_F11 : P_F11
/-- @fact F12 status=verified confidence=0.95 -/
axiom fact_F12 : P_F12
/-- @fact F13 status=verified confidence=0.95 -/
axiom fact_F13 : P_F13
/-- @fact F14 status=verified confidence=0.95 -/
axiom fact_F14 : P_F14
/-- @fact F15 status=verified confidence=0.95 -/
axiom fact_F15 : P_F15

-- ========== 隠れた前提 ==========
/-- A1: main はチーム全員が作業を始める起点であり、本番に出す変更のもとでもある。 -/
axiom P_A1 : Prop
/-- @confidence 0.85 一般的なブランチ運用の前提で、F2（main の変更が本番に出かけた）とも整合する。社内の構成を直接確かめてはいない。 -/
axiom assume_A1 : P_A1

/-- A2: 仕組みで止まらない今月は、メンバーが「承認前にマージせず、main に直接 push もしない」という決まりを守る。 -/
axiom P_A2 : Prop
/-- @confidence 0.65 今は人の運用だけで守られている。先月2回守られなかったので高くは見積もらない。 -/
axiom assume_A2 : P_A2

/-- A3: 新人は GitHub のアカウントを持ち、リポジトリに push してプルリクエストを出す権限がある。 -/
axiom P_A3 : Prop
/-- @confidence 0.8 新人が main に直接 push できた事実（F1, F2）から、書き込み権限はあると考えられる。 -/
axiom assume_A3 : P_A3

/-- A4: 承認後に commit を足したときは、マージ前にもう一度レビューしてもらう。 -/
axiom P_A4 : Prop
/-- @confidence 0.6 F8 により承認後の commit もプルリクエストに入る。承認が自動で取り消されるかは社内の設定しだいで不明なので、本文では勧めとして書く。 -/
axiom assume_A4 : P_A4

/-- A5: プルリクエストでレビューを通せば、ビルドを壊す変更や意図しない変更は、main に入る前に見つかる見込みが高い。 -/
axiom P_A5 : Prop
/-- @confidence 0.65 レビューは見落としを減らすが、必ず見つけるとは限らない。自動ビルド（CI）の有無は未確認。 -/
axiom assume_A5 : P_A5

/-- A6: ブランチ保護は直接 push を拒否するだけで、正しい手順は教えない。 -/
axiom P_A6 : Prop
/-- @confidence 0.8 F4 の仕組みの説明からそう言える。拒否されたときの画面の文言は確かめていない。 -/
axiom assume_A6 : P_A6

/-- A7: 社員は社内ルール（F7, F9, F11）に従う。 -/
axiom P_A7 : Prop
/-- @confidence 0.9 社内ルールとして決まっている。 -/
axiom assume_A7 : P_A7

-- ========== 推論規則と主張 ==========
/-- @confidence 0.7 実際の2件の事故が、作業の停止（F1）と未レビューの変更の本番への流出の手前（F2）を示す。main が共有の起点で本番のもと（A1）なので、誰の直接 push でも起こりうる。ただし2件からの一般化である。 -/
axiom rule_C1 : P_F1 ∧ P_F2 ∧ P_A1 → P_C1
theorem claim_C1 : P_C1 := rule_C1 ⟨fact_F1, fact_F2, assume_A1⟩

/-- @confidence 0.8 直接 push は危険で（C1）、それを止める仕組みが今月はまだない（F3）。したがって本人が避けるしかない。 -/
axiom rule_C2 : P_F3 ∧ P_C1 → P_C2
theorem claim_C2 : P_C2 := rule_C2 ⟨fact_F3, claim_C1⟩

/-- @confidence 0.85 ブランチへの commit は main を変えず（F5）、main への取り込みはプルリクエストで行い（F6）、承認が要る（F7）。指摘への対応も同じプルリクエストに入る（F8）。決まりが守られ（A2）、承認後の追加 commit も見てもらう（A4）なら、main に入る変更はすべてレビューと承認を通る。 -/
axiom rule_C3 : P_F5 ∧ P_F6 ∧ P_F7 ∧ P_F8 ∧ P_A2 ∧ P_A4 → P_C3
theorem claim_C3 : P_C3 := rule_C3 ⟨fact_F5, fact_F6, fact_F7, fact_F8, assume_A2, assume_A4⟩

/-- @confidence 0.8 main の更新（F15）、ブランチの作成（F9, F10）、push（F13）、プルリクエストの作成とレビュー依頼（F14）、マージ（F11, F12）の各手順がそろい、権限もある（A3）。コンフリクトの場面は範囲外として主張から外している。 -/
axiom rule_C4 : P_F9 ∧ P_F10 ∧ P_F11 ∧ P_F12 ∧ P_F13 ∧ P_F14 ∧ P_F15 ∧ P_A3 → P_C4
theorem claim_C4 : P_C4 := rule_C4 ⟨fact_F9, fact_F10, fact_F11, fact_F12, fact_F13, fact_F14, fact_F15, assume_A3⟩

/-- @confidence 0.75 来月入る仕組み（F3, F4）は直接 push を拒否するだけで、手順は教えない（A6）。流れを知らなければ作業が止まる。また初期設定では管理者には制限が効かない（F4）。 -/
axiom rule_C5 : P_F3 ∧ P_F4 ∧ P_A6 → P_C5
theorem claim_C5 : P_C5 := rule_C5 ⟨fact_F3, fact_F4, assume_A6⟩

/-- @confidence 0.8 直接 push には危険があり（C1）、今月は自分で避けるしかなく（C2）、来月以降も流れは必要（C5）。この流れなら変更はレビューを通り（C3）、レビューで問題が見つかる見込みが高い（A5）。新人でも実行でき（C4）、社内ルールでもある（A7）。 -/
axiom rule_C0 : P_C1 ∧ P_C2 ∧ P_C3 ∧ P_C4 ∧ P_C5 ∧ P_A5 ∧ P_A7 → P_C0
theorem claim_C0 : P_C0 := rule_C0 ⟨claim_C1, claim_C2, claim_C3, claim_C4, claim_C5, assume_A5, assume_A7⟩
