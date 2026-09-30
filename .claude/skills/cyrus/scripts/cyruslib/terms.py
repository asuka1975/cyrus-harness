"""用語の抽出と「初出で定義されているか」の判定。"""

from __future__ import annotations

import re
from dataclasses import dataclass

from . import jatext, mdparse

KATAKANA_TERM = re.compile(r"[ァ-ヺー・]{3,}")
LATIN_TERM = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z][A-Za-z0-9_+#.\-]*[A-Za-z0-9+#]|(?<![A-Za-z0-9_])[A-Z](?![A-Za-z0-9_])")

# 読者がほぼ確実に知っているとみなす語（誤検知を減らすための最小限の辞書）
COMMON_WORDS = {
    "データ", "ユーザー", "ユーザ", "メール", "ファイル", "システム", "サービス", "チーム", "プロジェクト",
    "ページ", "リスト", "テスト", "ルール", "コスト", "メンバー", "スケジュール", "イメージ", "ポイント",
    "サイト", "ボタン", "メモ", "ミス", "トラブル", "チェック", "スタート", "ゴール", "テーマ", "タイプ",
    "ケース", "パターン", "レベル", "グループ", "メリット", "デメリット", "リスク", "スピード", "タスク",
    "ツール", "アプリ", "パソコン", "インターネット", "ウェブ", "ソフト", "ソフトウェア", "コンピュータ",
    "コンピューター", "クリック", "ログイン", "パスワード", "アカウント", "ダウンロード", "アップロード",
    "オンライン", "サポート", "マニュアル", "トップ", "ホーム", "プラン", "コメント", "ミーティング",
    "スライド", "グラフ", "カテゴリ", "カテゴリー", "キーワード", "メニュー", "クラウド",
    "エラー", "カタカナ", "スマホ", "メッセージ", "コピー", "フォーマット", "サイズ", "バージョン",
}


def extract_terms(text: str) -> list[str]:
    """カタカナ語と英字語を候補として取り出す。"""
    out = []
    for m in KATAKANA_TERM.finditer(text):
        t = m.group(0).strip("・")
        if len(t) >= 3 and set(t) != {"ー"}:
            out.append(t)
    for m in LATIN_TERM.finditer(text):
        t = m.group(0)
        if len(t) >= 2:
            out.append(t)
    return out


def term_pattern(term: str) -> re.Pattern:
    """用語を探す正規表現。英字の語は単語の境界で、大文字小文字を区別せずに一致させる（PR が prefix に一致しないように）。"""
    if term.isascii():
        return re.compile(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", re.IGNORECASE)
    return re.compile(re.escape(term))


@dataclass
class Occurrence:
    term: str
    line: int
    sentence: str
    kind: str  # 出現したブロックの種類


def _definition_patterns(term: str) -> list[re.Pattern]:
    t = re.escape(term)
    return [
        re.compile(t + r"\s*[（(][^）)]{2,}[）)]"),                 # 用語（説明）
        re.compile(r"[（(]\s*" + t + r"\s*[）)]"),                   # 説明（用語）
        re.compile(r"「?" + t + r"」?\s*(とは|というのは|は[^。]*?(のこと|を指し|を意味))"),
        re.compile(r"のことを?、?\s*「?" + t + r"」?\s*(と呼|とい|と言)"),
        re.compile(r"「?" + t + r"」?\s*(と呼び|と呼ぶ|と呼ば|といいます|と言います|という。)"),
        re.compile(r"^\**" + t + r"\**\s*[:：]"),                     # 定義リスト形式
    ]


def is_definition(term: str, sentence: str) -> bool:
    return any(p.search(sentence) for p in _definition_patterns(term))


CODE_SPAN = re.compile(r"`[^`]*`")
PATH_LIKE = re.compile(r"(?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]*|(?<![A-Za-z0-9])[A-Za-z0-9_\-]+\.(?:md|json|py|lean|ya?ml|txt|toml|js|ts|sh)(?![A-Za-z0-9])|https?://\S+")
MASK = "□"


def mask_code(text: str) -> str:
    """インラインコード・ファイルパス・URL を伏せる。これらは語彙ではないので、用語の検査から外す。"""
    return PATH_LIKE.sub(MASK, CODE_SPAN.sub(MASK, text))


def iter_sentences(blocks: list[mdparse.Block]):
    """(行番号, 文, ブロック種別) を本文順に返す。見出しとコードは除き、インラインコードとパスは伏せる。"""
    for b in blocks:
        if b.kind in ("paragraph", "quote"):
            for s in jatext.split_sentences(jatext.strip_inline(mask_code(b.text))):
                yield b.line, s, b.kind
        elif b.kind == "list":
            for it in b.items:
                raw = mask_code(it.text)
                plain = jatext.strip_inline(raw)
                # **用語**: 説明 の形は定義として扱えるように、太字記法を残した形でも判定する
                yield it.line, plain if not re.match(r"^\*\*[^*]+\*\*\s*[:：]", raw) else raw.replace("**", ""), "list"
        elif b.kind == "table":
            for r_i, row in enumerate(b.rows):
                if r_i == 0:
                    continue
                yield b.line + r_i + 1, "：".join(jatext.strip_inline(mask_code(c)) for c in row), "table"


def find_occurrences(blocks: list[mdparse.Block], term: str) -> list[Occurrence]:
    occ = []
    pat = term_pattern(term)
    for line, s, kind in iter_sentences(blocks):
        if pat.search(s):
            occ.append(Occurrence(term, line, s, kind))
    return occ


def first_occurrences(blocks: list[mdparse.Block]) -> dict[str, Occurrence]:
    seen: dict[str, Occurrence] = {}
    for line, s, kind in iter_sentences(blocks):
        for t in extract_terms(s):
            key = t.lower() if t.isascii() else t
            if key not in seen:
                seen[key] = Occurrence(t, line, s, kind)
    return seen


def definition_status(blocks: list[mdparse.Block], term: str) -> tuple[str, Occurrence | None, Occurrence | None]:
    """用語の定義状況を返す。

    戻り値の状態:
      - "absent": 本文に出てこない
      - "ok": 初出の文で定義されている
      - "late": 定義はあるが初出より後
      - "undefined": 定義がない
    """
    occ = find_occurrences(blocks, term)
    if not occ:
        return "absent", None, None
    first = occ[0]
    if is_definition(term, first.sentence):
        return "ok", first, first
    for o in occ[1:]:
        if is_definition(term, o.sentence):
            return "late", first, o
    return "undefined", first, None
