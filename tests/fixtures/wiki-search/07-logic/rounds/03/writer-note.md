# Writer の作業の報告（3周目）

3周目の差分の設計書（model-plan-delta.md）の「## 変更」の表の1〜41行のとおりに、Argument.lean と Model.lean を直した。
model-plan.md や2周目の差分と食い違うところは、3周目の差分に従った。差分に名前の出ない宣言・公理・定理は変えていない（節の見出しのコメントは、1か所直し、`_tuned_le` の節に1か所足した。下に書く）。

## 書いたもの

- `07-logic/Argument.lean`
  - §2 宣言（24個）
    - `indexDelaySec` を `maxDelaySec` にし、docstring を差分の2節の文（勤務時間中に保存した記事の、いちばん長い遅れ）にした。
    - 足した: `DaytimeUpdate`（`IndexComplete` の後）、`pSameDay`・`pStale`（`pNotYet` の後）。
    - `testDelaySec` の docstring の宣言名を `maxDelaySec` に直した。
  - §4 関係公理（57個。【実験】3・【経験則】2・【自明】8・【仮定】44。差分の7節の数と一致する）
    - 消した3つ: `delay_current_ge_workday`・`notYet_ge_of_slow`・`tuned_slow_of_rebuild`。
    - 名前を変えて別の公理にした3つ: `prodDelay_le_test` → `prodMaxDelay_le_test`、`notYet_le_of_fast` → `notYet_le_of_maxFast`、
      `search_current_eq` → `searchTime_current_eq`。前の公理の `@confidence` の行と `@reviewer` の行は写していない（差分の「Writer への注」）。
      `searchTime_current_eq` は【実験】なので、確信度の行を書いていない。
    - 足した13個: `current_no_daytime`（【経験則】、F2、案 0.3）、`maxDelay_of_noDaytime`・`stale_of_noDaytime`・`notYet_ge_sameDay_stale`（【自明】）、
      `sameDay_current_ge`・`sameDay_tuned_ge`・`tuned_no_daytime_of_rebuild`（【仮定】）、`_tuned_le` の6つ（【仮定】）。
    - docstring だけを変えた8つ: `testDelay_le_five`・`extraNotYet_current_ge`・`searches_current_ge`・`wage_ge`・`noHit_current_le`・`overlook_current_le`・
      `approvable_of_net`・`fullText_complete`（差分の3節の末尾のとおり）。
    - 差分で「共通」とまとめてあった `_tuned_le` の論拠・要ファクト・向きは、6つの公理ごとに全文を書いた。
    - 節の見出しのコメント「【仮定】安い設定の変更の速さ」を「【仮定】安い設定の変更で、勤務時間中に索引を更新できるか」にした。
      中身の公理が「遅れ」から「勤務時間中に更新できるか」に変わったため。見出しはコメントで、検査にも証人にも関わらない。
  - §5 定理
    - `notYet_current_ge`・`notYet_tuned_ge`: 差分の「証明の道筋」のとおり、`rat_mul_le_mul` で 1/10 × 1 ≤ `pSameDay` × `pStale` ≤ `pNotYet` を示した。
      docstring に「（その日の記事を探す 1/10 以上 × まだ出ていない 1）」を足した。示すことは変えていない。
    - `notYet_fullText_le`・`claim_C2_soon`・`claim_C2_faster`・`claim_C1_many`・`baseline_lost_le_survey`・`unfav_saved_le_survey`: 使う公理と宣言の名前を替えた。
      `claim_C2_soon`・`claim_C2_faster` は型も替わったので、docstring を「勤務時間中に保存した記事の、いちばん長い遅れ」に合わせた。
    - `unfav_savedOverTuned_le_gap`（[不利]、印なし）を `unfav_saved_le_gap` の後に足した。`unfav_saved_le_gap` を途中の定理として使った（差分で許されている）。
    - `claim_C1_many` の `@restates` の行は、そのまま残した。
  - 冒頭: 設計書の一覧、書き方の約束（「印は行頭に書く。CLI は行頭の印だけを読む」を足した）、主張と定理の対応表の C2 の行、
    印のない定理の表（`unfav_savedOverTuned_le_gap` を足した）、「設計書（model-plan.md）との違い」を書き直した。
- `07-logic/Model.lean`（証人）
  - axiom 81個（宣言24・関係公理57）を、同じ名前・同じ型の `def` / `theorem` に差し替えた。
  - §5 は axiom を含まないので、Argument.lean から機械的に写した（手で写し直していないので、行の食い違いはない）。
  - 冒頭の証人の表に `DaytimeUpdate`・`pSameDay`・`pStale` を足し、`maxDelaySec` に直した。
  - 末尾の `example` を11個にした（下の「証人の世界」）。

## 設計書と違うところ

Argument.lean の冒頭の「設計書（model-plan.md）との違い」にも同じことを書いた。

1. **`current_no_daytime` の向きの行。** 差分の設計書は「新方式に有利（C3 と C0 の層1の下限を決める）」としている。
   実際には、C0 の筋道は安い設定の変更の層1の下限を `tuned_no_daytime_of_rebuild` から出すので、`current_no_daytime` を通らない。
   `report.json` の `claim_C0_approvable` の依存する公理にも出ない。代わりに `claim_C2_faster` が使う。
   そこで「新方式に有利（C3 の層1の下限と、C2 の項2（いまより早く検索に出る）を決める）」と書いた。手戻りの一覧でも、この公理の行き先は C2・C3 になっている。
2. **`sameDay_tuned_ge` の向きの行。** 差分の文には、消した公理との比べ（「2周目までの notYet_ge_of_slow は「中立」としていたが」）と指摘の番号（R16）が入っている。
   消した公理の名前が docstring に残ると、読む人がその公理を探すことになるので、いまの判断だけを書いた。
   「「社員がどれだけ新しい記事を探すかは方式に依らない」という判断のうち、安い設定の変更に当てはめる部分は C0 に有利な向きなので、その片側だけを置いた」。
   2周目に `workDays_ge` の向きから1周目との比べを外したのと同じ扱いで、意味は変えていない。
3. **証人の `pStale .fullText`。** 差分の見通しの 1/100 を 1/200 にした（下の「証人の世界」）。
4. **2周目の記述の訂正。** 2周目に Argument.lean の冒頭とこのファイルに書いた「CLI は docstring の中の印の語を、文の途中でも印として読む」は誤りだった。
   CLI（`leansrc.py` の `_ids_on_lines` など）は `^[ \t]*@support` の形で、行の先頭の印だけを読む。ガイドの「関係公理と定理の印」の記述と同じ。
   印の語を含む差分の文を言い換えて写したのは、差分の設計書の「Writer への注」の指示に従ったためである。2周目に言い換えた文（`current_not_incremental` の弱い点など）は、そのままにした。

差分の設計書が、命題を変えるのに名前を変えていない公理は、この周にはない。使う宣言の意味が変わった公理は、差分のとおり、すべて名前を変えるか消している。

## 定理が依存する関係公理の確かめ

`report.json`（`#print axioms` から CLI が出したもの）で、差分の4節の「使う判断」と突き合わせた。すべて一致した。

- `notYet_current_ge`: `notYet_ge_sameDay_stale`・`stale_of_noDaytime`・`current_no_daytime`・`sameDay_current_ge`。
- `notYet_tuned_ge`: `notYet_ge_sameDay_stale`・`stale_of_noDaytime`・`tuned_no_daytime_of_rebuild`・`current_not_incremental`・`sameDay_current_ge`・`sameDay_tuned_ge`。
- `claim_C2_faster`: `current_no_daytime`・`maxDelay_of_noDaytime`・`prodMaxDelay_le_test`・`testDelay_le_five`。
- `claim_C0_approvable`: `current_no_daytime` を含まない（上の「設計書と違うところ」の1）。
- `unfav_savedOverTuned_le_gap`: `search_decomp`・`miss_compose`・`searchesPerDay_nonneg`・`foundMinutes_nonneg`・`_tuned_le` の6つ・`_full_ge` の6つ・
  `extraNotYet_nonneg`・`extraOther_nonneg` の18個だけ。`extraNotYet_current_ge`・`_tuned_ge`・`_full_le` を通らない。
  `0 ≤ searchesPerDay .tuned` は `searchesPerDay_nonneg .tuned` から取った（`savedOverTuned_ge_gap` のように `_tuned_ge` から出すと、主張の側の片側を通ってしまうため）。

## 証人の世界

差分の「証人の見通しの変更」のとおりにした。1か所だけ変えた。

| 量 | 差分の見通し | 証人 | 理由 |
|---|---|---|---|
| `pStale .fullText` | 1/100 | 1/200 | `notYet_ge_sameDay_stale` が、置き換えた後で 1/2000 < 1/1000 と真に成り立つ。見通しでは3つとも等号だった |

- `pStale .fullText` を縛る公理はほかにない（`stale_of_noDaytime` の前提は、置き換えた後では成り立たない）。ほかの計算の値は変わらない。
- `notYet_ge_sameDay_stale` の current と tuned、`sameDay_current_ge`・`sameDay_tuned_ge` は等号のままにした。`pNotYet` を 1/10 にすると、
  `stale_of_noDaytime` と `notYet_ge_sameDay_stale` から `pSameDay` は 1/10 以下、`sameDay_current_ge`・`sameDay_tuned_ge` から 1/10 以上になり、等号しか残らない。
  `pNotYet` を変えると、計算の値（1.2672分など）が差分の値と照らせなくなる。
- `stale_of_noDaytime` は 1 = 1 の等号。`Prob` の範囲で、1 より大きくはできない。
- `maxDelaySec` は前の周の `indexDelaySec` の値のまま（86400、43200、4）。`maxDelay_of_noDaytime` の結論は current と tuned で真に成り立つ。
- 末尾の `example`: `¬ DaytimeUpdate .current`・`¬ DaytimeUpdate .tuned`（`maxDelay_of_noDaytime` と `stale_of_noDaytime` の前提）、
  `28800 < maxDelaySec .current`・`28800 < maxDelaySec .tuned`（前の周の2つの example の名前を直し、結論が真に成り立つことを示す形にした）、
  `pSameDay .fullText × pStale .fullText < pNotYet .fullText`、`maxDelaySec .fullText ≤ 5` と `IndexComplete .fullText`（`notYet_le_of_maxFast` の前提）、
  `¬ CurrentIncremental`（`tuned_no_daytime_of_rebuild` の前提）、`firstYearCost < gainYen`（`approvable_of_net` の前提）、計算の値の2つ。
- 主張の定理は、どれも前提を持たない。

## 門の結果

`python3 .claude/skills/cyrus/scripts/cyrus.py --doc wiki-search lean`: エラー 0 件・警告 0 件・参考 0 件。

- 証人: 81個の型がすべて一致、元の行はすべて同じ順で残っている（missing_lines 0）、Lean 標準の3公理以外に依存しない。
- 主張ごとの確信度: C0 0.05、C1 0.05、C2 0.05、C3 0.05（どれも hypothesis）。前の周から上がった主張はない。
- 原子命題 57（【自明】8・【実験】3・【経験則】2・【仮定】44）。主張の定理が使う 43、`@beyond`・`@baseline` だけが使う 0、使われない 14。
- 公理の値: `searchTime_current_eq` 0.95（F1 の値。前の公理の Reviewer の値 0.75 は、名前を変えたので引き継いでいない）、`testDelay_le_five` 0.95、
  `estimate_eq` 0.6、`current_no_daytime` 0.3、`beneficiaries_ge` 0.9、【自明】8つは 1、【仮定】44はすべて 0.05。
- `searchTime_current_eq` が 0.95 になったので、`baseline_lost_le_survey`（`@baseline`）と `unfav_saved_le_survey`（[不利]）の値は 0.75 から 0.95 に上がった。
  主張の値は変わらない（C1 は `many_threshold_le` の 0.05 で決まる）。差分の設計書の見通しのとおり。

## 検査について・Reviewer に伝えたい点

- **「使われない」14の原子は、設計どおり。** `_full_ge` の6つ・`_tuned_le` の6つ・`extraNotYet_nonneg`・`searchMinutes_nonneg` で、どれも [不利] の定理だけが使う。
  [不利] の定理には印を付けないので、CLI は公理の使用に数えず、手戻りの一覧で「主張 なし」と出る。決まりどおりの動きで、検査の誤りではない。
- **公理系の全体は、安い設定の変更でも6つの量が変わらないことを仮定している。** `_tuned_ge` と `_tuned_le` を両方置いたので、合わせると
  `searchesPerDay`・`foundMinutes`・`extraNotYetMinutes`・`extraOtherMinutes`・`pNoHit`・`pOverlook` の `tuned` と `current` は等しくなる（`_full_le`・`_full_ge` と同じ組み方）。
  主張の定理は `_tuned_ge` だけ、不利な結論の定理は `_tuned_le` だけに頼る。
- **`fullText_complete` の論拠は、閲覧の権限にふれなくなった。** 命題（`IndexComplete .fullText`）は「記事と閲覧の権限が欠けない」のままで、
  論拠は記事を移すことだけを述べ、権限は弱い点に移った。差分の設計書のとおりで、命題は変えていない。
- 検査が誤っていると思う点は、この周にはない。
