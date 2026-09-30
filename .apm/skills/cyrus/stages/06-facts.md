# ステージ6: 事実を確かめる（Fact Verification）

フェーズ: インタビュー 6/6　成果物: `06-facts.json`　承認: 不要（反証が出たらユーザーに報告する）

## ねらい

`05-claims.json` の事実（F）を、外部の信頼できる情報源や、あなた自身が実行・計測することで確かめます。
ここで決まる `status` が、ステージ7で主張の確からしさを計算するときの土台になります。

## 進め方

1. 雛形 `06-facts.json` には、すべての事実が `unverified` で並んでいる。
2. 事実を性質で分け、確かめ方を決める。
   - 公開情報で確かめられる → `cyrus-fact-checker` サブエージェントに任せる（複数の事実をまとめて渡してよい。独立した事実のグループは並列に起動してよい）
   - コードやデータを実行すれば確かめられる → あなたが実行し、コマンドと結果を `evidence` に書く（method: `execution`）
   - 社内の数字など、ユーザーにしかわからない → ユーザーに出典を聞く。出典のない証言は `user_asserted`
   - 論理的に導けるだけ → `reasoning`（status は `unverified` か `partially_verified` にとどめる）
3. サブエージェントには、事実の id と statement、`source_hint`、読者の知識レベルを渡し、次の JSON の形で返してもらう。
4. 結果をまとめ、`06-facts.json` に反映する。
5. **反証（refuted）が出たら、すぐユーザーに報告する。** 主張の見直しが必要なので `cyrus back claims` で戻る。事実の言い方を正確にすれば成り立つ場合（例: 「半分」→「4割」）は、05-claims.json の statement を直して戻ってくる。

## status の基準

| status | 意味 | 確からしさ |
| --- | --- | --- |
| `verified` | 信頼できる一次情報源、または実行結果で確認できた | 0.95 |
| `partially_verified` | 一部だけ、または間接的に確認できた | 0.75 |
| `user_asserted` | ユーザーの証言のみ | 0.60 |
| `unverified` | 確認できていない | 0.40 |
| `refuted` | 誤りだと確認した | 0（使えない） |

`confidence` を明示すると、この表の値より低い値を付けられます（高くはできません）。

## 成果物 `06-facts.json`

```json
{
  "facts": [
    {
      "id": "F1",
      "statement": "事実（検証の結果、言い方を正確にしたもの）",
      "status": "verified",
      "method": "web | document | execution | user | reasoning",
      "sources": [{"title": "資料名", "url": "https://…", "accessed": "2026-09-28", "quote": "該当箇所の短い引用"}],
      "evidence": "method が execution のとき: 実行したことと結果",
      "notes": "確認できた範囲、注意点"
    }
  ]
}
```

## 完了条件

- `cyrus check` でエラーが0になったら `cyrus advance`。
- 反証や大きな修正があった場合は、その内容を1〜2行でユーザーに伝えてから進む。
