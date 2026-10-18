# cyrus-harness (記すハーネス)

インタビューを受けながら、読みやすい日本語の文書を AI に書いてもらうための、Claude Code 向けのハーネスです。

あなたがすることは、質問に答えることと、要所で承認することだけです。
Claude が目的と読者を聞き取り、事実を確かめ、論理を検証し、構成を決めて書き、読者の立場で直します。
提案書・解説・手順書・報告書など、読み手が決まっている文書に向いています。

## 特徴

- **半決定論的に進めます。** 判断と文章は Claude が受け持ちます。ステージの順序、成果物の形式、完了条件は CLI が機械的に検査します。検査を通らない限り、次のステージには進みません。
- **主張の論理を Lean 4 で検証します。** 論証を Lean のモデルとして書き、矛盾がないことを確かめ、主張ごとの確信度を計算します。本文でどこまで言い切るかは、この確信度で決めます。
- **認知負荷を測ります。** 文の長さ、漢字の連続、段落や見出しの構造などを lint で調べます。さらに、原稿を見ていない読み手に拾い読みさせ、伝えたいことが伝わるかを確かめます。読み手には、書き手とは別のモデル（既定は Gemini）も使います。
- **言葉を読者に合わせます。** 読者が知っている語と知らない語を辞書として扱い、説明のない専門用語を見つけます。推敲は [yomiyasu](https://github.com/nanaism/yomiyasu) に任せます。

## 流れ

3つのフェーズ、13のステージで進みます。

| フェーズ | ステージ |
| --- | --- |
| インタビュー | 1 目的をつかむ → 2 背景を聞く → 3 読者を描く → 4 伝える情報を選ぶ → 5 主張を組み立てる → 6 事実を確かめる |
| 組み立て | 7 論理を検証する → 8 骨組みを決める → 9 話の流れを決める → 10 見せ方を決める → 11 書く |
| 仕上げ | 12 認知負荷を下げる → 13 言葉を読者に合わせる |

承認を求められるのは、目的・読者・主張・話の流れ・完成版の5か所です。
後のステージで前提の誤りが見つかれば、前のステージに戻ってやり直します。

## 必要なもの

| もの | 使うところ |
| --- | --- |
| [Claude Code](https://claude.com/claude-code) | ハーネスを動かす |
| [APM](https://github.com/microsoft/apm) | インストール |
| Python 3 | CLI。標準ライブラリだけで動きます（3.12 で確認） |
| Lean 4（[elan](https://lean-lang.org/install/)） | ステージ7の論理の検証。省略できません |
| Chrome、Pillow、agy（Gemini を呼ぶ CLI） | ステージ12の、画像での拾い読みテスト。そろっていなければ、理由を書いて省略できます |

画像を読む読み手は、agy（Gemini）のほかのコマンドにも変えられます。
プロジェクトのルートに `cyrus.config.json` を置きます。書き方は [`stages/12-cogload.md`](.apm/skills/cyrus/stages/12-cogload.md) にあります。

## インストール

文書を書きたいプロジェクトで、次のコマンドを実行します。

```bash
apm install asuka1975/cyrus-harness#v0.1.0
```

スキル、サブエージェント、コマンド、フックが Claude Code に入ります。
ステージ13の推敲に使う yomiyasu も、依存として一緒に入ります。別に入れる必要はありません。

`.claude/` がまだないプロジェクトでは、APM が入れ先を判断できません。そのときは `--target claude` を付けてください。

## 使い方

Claude Code を起動して、書きたい文書のテーマを渡します。

```text
/cyrus 新人向けの Git ブランチ運用ルール
```

あとは、Claude の質問に答えていきます。

- 途中でやめても、`/cyrus` だけで続きから再開できます。
- 進み具合は `/cyrus-status` で確かめられます。
- 成果物は `documents/<slug>/` に置かれます。完成版は `documents/<slug>/final.md` です。

## 例

「新人向けの Git ブランチ運用ルール」を題材に、13ステージを最後まで通した成果物の一式を [`docs/ai-notes/examples/git-branch-rules/`](docs/ai-notes/examples/git-branch-rules/) に置いています。
完成版は [`final.md`](docs/ai-notes/examples/git-branch-rules/final.md) です。
ほかのファイルを見ると、各ステージで何が決まったかを追えます。

## 開発

ハーネスの元は `.apm/` にあります。`.claude/` は `apm install` で作られる展開先なので、直接は編集しません。

```bash
apm install                            # .apm/ の変更を .claude/ に展開する
python3 -m unittest discover -s tests  # テストを実行する
```

Lean、yomiyasu、Chrome、Pillow のない環境では、それらを使うテストは飛ばされます。

| 場所 | 中身 |
| --- | --- |
| `.apm/skills/cyrus/` | スキル本体。進め方（`SKILL.md`）、ステージのガイド（`stages/`）、文章の指針（`references/`）、CLI（`scripts/`） |
| `.apm/agents/` | サブエージェント（事実確認、論理モデルの設計・記述・監査、読者役、拾い読み役、照合） |
| `.apm/prompts/` | `/cyrus` と `/cyrus-status` |
| `.apm/hooks/` | 成果物を保存したときの自動検査 |
| `docs/workflow.md` | ワークフローの構想 |
| `docs/ai-notes/` | 実装の設計メモ（AI が書いたもの） |
| `tests/` | テスト |

実装の詳しい説明は [`docs/ai-notes/harness-design.md`](docs/ai-notes/harness-design.md) にあります。

## ライセンス

[MIT](LICENSE)
