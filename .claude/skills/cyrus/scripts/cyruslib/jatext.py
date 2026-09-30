"""日本語テキストの基本処理（文字種の判定・文分割・インライン記法の除去）。

形態素解析器を使わず、文字種のヒューリスティクスで近似する。
"""

from __future__ import annotations

import re

KANJI_RE = re.compile(r"[㐀-䶿一-鿿豈-﫿々〆ヶ]")
HIRAGANA_RE = re.compile(r"[ぁ-ゟ]")
KATAKANA_RE = re.compile(r"[ァ-ヺーｦ-ﾟ]")
ALNUM_RE = re.compile(r"[A-Za-z0-9０-９Ａ-Ｚａ-ｚ]")

SENTENCE_END = "。！？"
CLOSERS = "」』）)】〉》"


def is_kanji(ch: str) -> bool:
    return bool(KANJI_RE.match(ch))


def is_hiragana(ch: str) -> bool:
    return bool(HIRAGANA_RE.match(ch))


def is_katakana(ch: str) -> bool:
    return bool(KATAKANA_RE.match(ch))


def char_counts(text: str) -> dict:
    kanji = len(KANJI_RE.findall(text))
    hira = len(HIRAGANA_RE.findall(text))
    kata = len(KATAKANA_RE.findall(text))
    alnum = len(ALNUM_RE.findall(text))
    return {"kanji": kanji, "hiragana": hira, "katakana": kata, "alnum": alnum,
            "letters": kanji + hira + kata + alnum}


def kanji_ratio(text: str) -> float:
    c = char_counts(text)
    return c["kanji"] / c["letters"] if c["letters"] else 0.0


_INLINE_CODE = re.compile(r"`([^`]*)`")
_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_EMPH_STAR = re.compile(r"(\*\*|\*)(?=\S)(.+?)(?<=\S)\1")
# 単語の途中のアンダースコア（partially_verified など）は強調ではない（CommonMark と同じ扱い）
_EMPH_UNDER = re.compile(r"(?<![A-Za-z0-9_])(__|_)(?=\S)(.+?)(?<=\S)\1(?![A-Za-z0-9_])")
_HTML = re.compile(r"<[^>]+>")
_FOOTNOTE = re.compile(r"\[\^[^\]]+\]")


def strip_inline(text: str) -> str:
    """Markdown のインライン記法を取り除き、読者に見える文字列に近づける。"""
    text = _IMAGE.sub(r"\1", text)
    text = _LINK.sub(r"\1", text)
    text = _INLINE_CODE.sub(r"\1", text)
    text = _FOOTNOTE.sub("", text)
    text = _HTML.sub("", text)
    for _ in range(2):
        text = _EMPH_STAR.sub(r"\2", text)
        text = _EMPH_UNDER.sub(r"\2", text)
    return text


def split_sentences(text: str) -> list[str]:
    """句点・感嘆符・疑問符で文に分ける。閉じ括弧が続く場合は括弧までを 1 文とする。

    括弧の中の句点では分割しない。
    """
    sentences: list[str] = []
    buf: list[str] = []
    depth = 0
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        buf.append(ch)
        if ch in "「『（(【":
            depth += 1
        elif ch in "」』）)】" and depth > 0:
            depth -= 1
        if ch in SENTENCE_END and depth == 0:
            while i + 1 < n and text[i + 1] in CLOSERS + SENTENCE_END:
                i += 1
                buf.append(text[i])
            s = "".join(buf).strip()
            if s:
                sentences.append(s)
            buf = []
        i += 1
    rest = "".join(buf).strip()
    if rest:
        sentences.append(rest)
    return sentences


def visible_length(text: str) -> int:
    """空白を除いた文字数。"""
    return len(re.sub(r"\s", "", text))


_DESUMASU = re.compile(
    r"(です|ます|でした|ました|ません|でしょう|ましょう|ください|ませんでした|"
    r"ですか|ますか|ましたか|でしょうか|ませんか|ございます)$"
)
_PARTICLE_TAIL = re.compile(r"(よね|よ|ね|な|ぞ)$")
_TRAILING_PAREN = re.compile(r"[（(][^（）()]*[）)]$")


def sentence_style(sentence: str) -> str:
    """文末の文体を判定する。desumasu（です・ます）/ plain（だ・である）/ neutral（体言止めなど）。"""
    s = sentence.strip()
    s = s.rstrip(SENTENCE_END + CLOSERS + "　 ")
    s = _TRAILING_PAREN.sub("", s).rstrip()
    s = s.rstrip(SENTENCE_END + CLOSERS + "　 ")
    if not s:
        return "neutral"
    base = s
    if _DESUMASU.search(base):
        return "desumasu"
    stripped = _PARTICLE_TAIL.sub("", base)
    if stripped and _DESUMASU.search(stripped):
        return "desumasu"
    last = (stripped or base)[-1]
    if is_hiragana(last):
        return "plain"
    return "neutral"


def sentence_ending(sentence: str, width: int = 4) -> str:
    s = sentence.strip().rstrip(SENTENCE_END + CLOSERS + "　 ")
    return s[-width:]


def longest_kanji_run(text: str) -> str:
    runs = re.findall(r"[㐀-䶿一-鿿豈-﫿々〆ヶ]+", text)
    return max(runs, key=len) if runs else ""


def pickup(text: str) -> str:
    """周辺視野での拾い読みを模して、漢字・カタカナ・英数字の連なりだけを残す。

    ひらがな（主に助詞・活用語尾）を落とすと、目に飛び込みやすい語だけが残る。
    """
    tokens = re.findall(
        r"[㐀-䶿一-鿿豈-﫿々〆ヶ]+|[ァ-ヺー]+|[A-Za-z0-9][A-Za-z0-9.\-+#%]*",
        text,
    )
    return " ".join(tokens)
