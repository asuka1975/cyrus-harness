# ステージ12: 認知負荷を下げる（Cognitive Load Check）

フェーズ: 仕上げ 1/2　成果物: `12-cogload.json`（原稿 `draft.md` をその場で直す）　承認: 不要

## ねらい

原稿を、読者の認知の限界に照らして検査し、直します。次の3つの層で見ます。

| 層 | 見るもの | 方法 |
| --- | --- | --- |
| 文・語（短期記憶） | 文の長さ、読点の数、漢字の連続、二重否定、括弧の長さ、1節あたりの新しい用語の数 | `cyrus lint`（決定論） |
| 構造（中期記憶・見通し） | 段落の長さ、見出しの階層、箇条書きの数、表の大きさ、図表の参照、前後への参照 | `cyrus lint`（決定論） |
| 視覚（中心視野・周辺視野） | 拾い読みで要点が伝わるか、焦点の外がぼやけていても段落が読めるか | `cyrus skim` ＋ サブエージェント（非決定論） |
| 視覚（画面での見え方） | 画面に描いた文書を、目が留まる箇所だけくっきり・それ以外をぼかした画像で見て、要点と見た目の構造が伝わるか | `cyrus vision`（画像化とぼかしは決定論、読み手は別のモデル。既定は Gemini） |

## 進め方

### 1. 決定論の検査

1. `cyrus lint --json` の `metrics` を `12-cogload.json` の `metrics_before` に記録する。
2. `cyrus lint` のエラーをすべて直し、警告もできるだけ直す。直し方は `references/japanese-style.md` を参照。
   - 長い文 → 2〜3文に分ける。条件と結論を分ける。
   - 長い段落 → 話題の切れ目で分ける。並列の内容は箇条書きにする。
   - 新しい用語が多い節 → 節を分けるか、言い換えで減らす。
   - 「後述」「前述」 → その場で書くか、節の名前で示す。

### 2. 拾い読みテスト（周辺視野）

1. `cyrus skim` を実行し、`skim/outline.md`（見出しと段落の最初の文）と `skim/pickup.md`（漢字・カタカナ・英数字だけ）を作る。表示される**原稿の指紋**を `skim_test.draft_hash` に記録する。
2. `cyrus-skim-reader` サブエージェントを起動する。渡すのは**この2つのファイルのパスと、読者ペルソナの要点だけ**。原稿や設計ファイルのパスは渡さない。
   サブエージェントは、読み取れた内容を「全体の要約」と「節ごとの要点」で返す。
3. `cyrus-alignment-judge` サブエージェントを起動し、`09-storyline.json`（意図したメッセージ）と、拾い読みの結果を照合してもらう。節ごとに yes / partial / no、C0 が伝わったかを返す。
4. 判定を `skim_test` に記録する。再現率（yes=1, partial=0.5）が 70% 未満、または C0 が伝わっていなければ、伝わらなかった節の**見出しと段落の最初の文**を直し、手順1からやり直す。
5. **拾い読みテストは、完了時点の原稿で行われている必要がある。** テストのあとで draft.md を直したら、指紋が変わるので完了条件を満たさなくなる。原稿の修正（決定論の検査・局所テスト・ペルソナ通読・画像テストによる修正）をすべて終えてから、最後にもう一度、テキストと画像の拾い読みテストを行うのが効率的です。

### 3. 画像での拾い読みテスト（別のモデル）

テキストの拾い読みテストでは、文字の並びしか見えません。実際の読者は画面を見ます。見出しの大きさ、太字、図、余白、表やコードの囲みが、目の動きを決めます。
そこで、原稿を画像にし、目が留まる箇所（見出し、段落の最初の文、太字、箇条書きの頭、図表とキャプション、コードの1行目）だけをくっきり、そのすぐ横を少しぼかし、それ以外を読めないほどぼかします。これを、原稿を書いた Claude とは別のモデルに読ませます。既定の読み手は、agy 経由の Gemini です。読み手のコマンドは設定ファイルで変えられます（このあとの「読み手を変える」）。

1. `cyrus vision` を実行する。次のことが自動で行われる。
   - 読者の読む媒体（03-reader.json の reading_context.medium）に合わせた幅で画面に描き、一画面ずつの画像（`skim/visual/page-XX.png`）と全体の縮小図（`overview.png`）を作る。
   - 画像だけを一時ディレクトリに移し、読み手に読ませる（原稿の場所は知らせない）。
   - 結果を `skim/visual/reader-result.json` に保存し、原稿の指紋を表示する。
   - 時間は1分ほどかかる。
2. `cyrus-alignment-judge` に、`09-storyline.json` と `05-claims.json` のパス、`reader-result.json` の `result` を渡して照合してもらう。
3. 判定を `visual_test` に記録する。`draft_hash` には表示された指紋を、`reader_model` には reader-result.json の model（model がなければ reader）を書く。
4. 読み手の `visual_notes`（目に飛び込んだもの・目立たなかった重要な点・見た目の構造の問題）を読み、直す。対応を `visual_notes_resolution` に書く。よくある直し方は次のとおり。
   - 重要な注意が目立たない → 段落の最初の文に出す。太字にするのは1節に1か所まで。
   - 手順の順序が見えない → 番号付きリストか、見出しに番号を付ける。
   - 図が何を言っているかわからない → キャプションに結論を書く（「図1: 変更は必ず承認を経て main に入る」）。
5. 再現率が 70% 未満、または C0 が伝わっていなければ、直してから手順1をやり直す。

Chrome か読み手のコマンドが使えない環境では、`visual_test` に `{"skipped_reason": "理由"}` とだけ書けば省略できます（使える環境では省略できません）。

#### 読み手を変える（cyrus.config.json）

読み手は、プロジェクトのルートに置いた `cyrus.config.json` で変えられます。別の場所のファイルを使うときは、環境変数 `CYRUS_CONFIG` でそのファイルを指します。
Claude Code のように、LLM をエージェントとして動かせるコマンドなら使えます。次は Claude Code を読み手にする例です。

```json
{
  "vision": {
    "reader": {
      "name": "Claude Code",
      "command": ["claude", "-p", "--output-format", "json", "--json-schema", "{schema}",
                  "--model", "{model}", "--permission-mode", "plan", "--tools", "Read"],
      "model": "sonnet",
      "timeout": 600
    }
  }
}
```

`cyrus vision --show-command` を実行すると、読み手を起動せずに、組み立てたコマンドを確かめられます。環境変数は名前だけを表示します。

| 項目 | 意味 |
| --- | --- |
| `command` | 起動するコマンドと引数のリスト。シェルは通さない。省略すると既定の agy を使う |
| `name` | 表示と記録に使う読み手の名前。省略するとコマンドの名前になる |
| `model` | `{model}` に入るモデル名。`cyrus vision --model` で渡したほうが優先される |
| `env` | 起動するときに設定する環境変数。値が `null` の変数は、消してから起動する |
| `timeout` | 読み手を待つ秒数。既定は900秒 |

`command` の引数には、次の置き換えを書けます。

| 置き換え | 入るもの |
| --- | --- |
| `{prompt}` | 読み手への指示。どの引数にも書かなければ、標準入力で渡す |
| `{workdir}` | 画像だけを置いた一時ディレクトリ。読み手は、ここを作業ディレクトリにして起動する |
| `{schema}` | 回答の JSON スキーマ（文字列） |
| `{schema_file}` | 回答の JSON スキーマを書いたファイルのパス |
| `{model}` | モデル名 |
| `{timeout}` | 待つ秒数 |

これ以外の `{名前}` を書くと、設定の誤りとして止まります。引数でも、`env` の値と同じく `${変数名}` と先頭の `~` を展開します。
`{schema}` も `{schema_file}` も書かなければ、回答の形はプロンプトで伝えます。
回答は標準出力から読み取ります。agy や Claude Code の JSON 出力のほか、回答の JSON だけでも、文章の中の ```json の囲みでも構いません。

`env` の値では、`${変数名}` と先頭の `~` を展開します。たとえば次のように書きます。

```json
"env": {
  "CLAUDE_CONFIG_DIR": "~/.claude-cyrus-reader",
  "HTTPS_PROXY": "${CORP_PROXY}",
  "CLAUDECODE": null
}
```

1行目は読み手専用の設定ディレクトリを使う例、2行目はいまの環境変数から値を写す例、3行目は変数を消してから起動する例です。

読み手を選ぶときは、次の2つを守ってください。

- **読み取り専用で起動する。** 権限確認を省略するオプション（`--dangerously-skip-permissions` など）は使わない。plan モードにするか、使えるツールをファイルの読み取りだけに絞る。cyrus が守るのは、作業ディレクトリに画像しか置かないことと、指示に原稿の場所を書かないことだけです。
- **書き手と違うモデルにする。** 読み手を Claude にすると、書き手と同じモデルが読み手を演じる偏りが戻ります。Claude Code を使うなら、せめて書き手と違うモデル（書き手が Opus なら Sonnet など）を指定してください。

`command` を書かなければ、既定の agy を使います。このときは、`name`・`model`・`env`・`timeout` だけを変えられます。環境変数 `CYRUS_AGY`（agy の場所）と `CYRUS_AGY_MODEL`（モデル）も使えます。

### 4. 局所テスト（中心視野）

1. `skim/local.md` は、各段落を焦点にし、前後の段落をぼかしたもの。
2. `cyrus-persona-reader` に通読してもらうとき、あわせてこのファイルも渡し、「前後がぼやけていると意味が取れない段落」を挙げてもらう。
3. 挙がった段落は、指示語を名詞に置き換える、前提を1文補う、などで自立させる。結果を `local_test.unclear_paragraphs` に記録する。

### 5. ペルソナ通読

1. `cyrus-persona-reader` に、`draft.md` と `03-reader.json` のパスを渡し、読者になりきって通読してもらう。
2. つまずいた箇所、戻って読み直した箇所、答えが見つからなかった疑問、`success_criteria` を満たせたかが返ってくる。
3. 指摘ごとに、どう直したか（または直さない理由）を `persona_review.issues[].resolution` に書く。

### 6. 仕上げ

- もう一度 `cyrus lint --json` を実行し、`metrics_after` に記録する。`changes` に主な変更点を3〜7行で書く。

## 成果物 `12-cogload.json`

```json
{
  "metrics_before": {"avg_sentence_length": 48.2, "...": "..."},
  "metrics_after": {"avg_sentence_length": 36.5, "...": "..."},
  "skim_test": {
    "draft_hash": "cyrus skim が表示した原稿の指紋",
    "reader_summary": "拾い読みした読者が再構成した全体の要約",
    "main_claim_recovered": true,
    "sections": [{"id": "S1", "recovered": "yes", "note": ""}]
  },
  "visual_test": {
    "draft_hash": "cyrus vision が表示した原稿の指紋",
    "reader_model": "gemini-3.8-flash-medium",
    "main_claim_recovered": true,
    "sections": [{"id": "S1", "recovered": "yes", "note": ""}],
    "visual_notes_resolution": "読み手の見た目の指摘にどう対応したか"
  },
  "local_test": {"unclear_paragraphs": [{"line": 42, "problem": "…", "fix": "…"}]},
  "persona_review": {"issues": [{"where": "S2 第2段落", "problem": "…", "resolution": "…"}]},
  "changes": ["長い文を12文分割した", "…"]
}
```

## 完了条件

- `draft.md` に lint のエラーがない。
- いまの draft.md で行った拾い読みテスト（テキスト・画像の両方）の再現率が 70% 以上で、C0 が伝わっている。
- ペルソナの指摘すべてに resolution がある。
- `cyrus check` でエラーが0になったら `cyrus advance`。
