"""拾い読み（周辺視野）ビューの生成。

Cognitive Load Check で、読者が「飛び飛びに目を留めただけ」で内容をつかめるかを試すための入力を作る。

- outline: 見出し、各段落の最初の文、箇条書きの頭、表の見出し行、図のキャプション
  （中心視野で順にとらえる「見出し読み・頭読み」を模す）
- pickup: 漢字・カタカナ・英数字の連なりだけを残す（周辺視野で目に飛び込む語だけを模す）
- local:  各段落を焦点にして、前後の段落を pickup でぼかした形にする
  （焦点の外がぼやけていても、その段落が理解できるかを試す）
"""

from __future__ import annotations

import hashlib

from . import jatext, mdparse


def text_hash(text: str) -> str:
    """原稿の指紋。拾い読みテストがどの版の原稿で行われたかを確かめるために使う。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


HEAD_ITEM_CHARS = 20


def outline_view(text: str) -> str:
    out: list[str] = []
    for b in mdparse.parse(text):
        if b.kind == "heading":
            out.append(f"{'#' * b.level} {jatext.strip_inline(b.text)}")
        elif b.kind in ("paragraph", "quote"):
            ss = jatext.split_sentences(jatext.strip_inline(b.text))
            if ss:
                out.append(ss[0] + (" …" if len(ss) > 1 else ""))
        elif b.kind == "list":
            for it in b.items:
                if it.depth == 1:
                    t = jatext.strip_inline(it.text)
                    out.append("- " + (t[:HEAD_ITEM_CHARS] + "…" if len(t) > HEAD_ITEM_CHARS else t))
        elif b.kind == "table" and b.rows:
            out.append("| " + " | ".join(jatext.strip_inline(c) for c in b.rows[0]) + " |（表・{}行）".format(len(b.rows) - 1))
        elif b.kind == "image":
            out.append(f"［図］{b.text}")
        elif b.kind == "code":
            out.append(f"［コード・{b.lang or 'text'}］")
    return "\n".join(out) + "\n"


def _blur(b: mdparse.Block) -> str:
    if b.kind == "heading":
        return f"{'#' * b.level} {jatext.pickup(jatext.strip_inline(b.text))}"
    if b.kind == "list":
        return "\n".join("- " + jatext.pickup(jatext.strip_inline(it.text)) for it in b.items)
    if b.kind == "table":
        return "\n".join("| " + " | ".join(jatext.pickup(jatext.strip_inline(c)) for c in r) + " |" for r in b.rows)
    if b.kind == "code":
        return "［コード］"
    if b.kind == "image":
        return f"［図］{jatext.pickup(b.text)}"
    return jatext.pickup(jatext.strip_inline(b.text))


def pickup_view(text: str) -> str:
    return "\n\n".join(x for x in (_blur(b) for b in mdparse.parse(text)) if x.strip()) + "\n"


def local_view(text: str) -> str:
    blocks = [b for b in mdparse.parse(text) if b.kind != "hr"]
    out: list[str] = []
    heading_path: list[mdparse.Block] = []
    n = 0
    for i, b in enumerate(blocks):
        if b.kind == "heading":
            while heading_path and heading_path[-1].level >= b.level:
                heading_path.pop()
            heading_path.append(b)
            continue
        if b.kind != "paragraph":
            continue
        n += 1
        prev_b = next((blocks[j] for j in range(i - 1, -1, -1) if blocks[j].kind != "heading"), None)
        next_b = next((blocks[j] for j in range(i + 1, len(blocks)) if blocks[j].kind != "heading"), None)
        out.append(f"## 焦点 {n}（{b.line}行目）")
        out.append("見出し: " + " > ".join(jatext.strip_inline(h.text) for h in heading_path))
        if prev_b is not None:
            out.append("（前・ぼかし）" + _blur(prev_b).replace("\n", " "))
        out.append("（焦点）" + jatext.strip_inline(b.text))
        if next_b is not None:
            out.append("（後・ぼかし）" + _blur(next_b).replace("\n", " "))
        out.append("")
    return "\n".join(out) + "\n"


VIEWS = {"outline": outline_view, "pickup": pickup_view, "local": local_view}
