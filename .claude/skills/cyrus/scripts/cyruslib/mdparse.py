"""行番号つきの簡易 Markdown ブロックパーサ。

検査に必要な粒度（見出し・段落・リスト・表・コード・引用・図）だけを扱う。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
FENCE_RE = re.compile(r"^\s*(```|~~~)(.*)$")
IMAGE_LINE_RE = re.compile(r"^\s*!\[([^\]]*)\]\(([^)]*)\)\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


@dataclass
class ListItem:
    line: int
    depth: int
    text: str
    ordered: bool = False


@dataclass
class Block:
    kind: str  # heading / paragraph / list / table / code / quote / image / hr
    line: int
    text: str = ""
    level: int = 0
    items: list[ListItem] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    lang: str = ""
    end_line: int = 0


@dataclass
class Section:
    """見出し 1 つと、次の同レベル以上の見出しまでの範囲。"""
    heading: Block | None
    blocks: list[Block]

    @property
    def title(self) -> str:
        return self.heading.text if self.heading else "（冒頭）"


def _split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def parse(text: str) -> list[Block]:
    lines = text.split("\n")
    blocks: list[Block] = []
    i = 0
    n = len(lines)

    # YAML front matter は読み飛ばす
    if n and lines[0].strip() == "---":
        for j in range(1, n):
            if lines[j].strip() == "---":
                i = j + 1
                break

    para: list[str] = []
    para_start = 0

    def flush_para(end: int) -> None:
        nonlocal para
        if para:
            blocks.append(Block("paragraph", para_start + 1, "".join(s.strip() for s in para), end_line=end))
            para = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        m = FENCE_RE.match(line)
        if m:
            flush_para(i)
            fence = m.group(1)
            lang = m.group(2).strip()
            start = i
            body = []
            i += 1
            while i < n and not lines[i].strip().startswith(fence):
                body.append(lines[i])
                i += 1
            blocks.append(Block("code", start + 1, "\n".join(body), lang=lang, end_line=i + 1))
            i += 1
            continue

        if not stripped:
            flush_para(i)
            i += 1
            continue

        m = HEADING_RE.match(line)
        if m:
            flush_para(i)
            blocks.append(Block("heading", i + 1, m.group(2).strip(), level=len(m.group(1)), end_line=i + 1))
            i += 1
            continue

        if re.match(r"^\s*([-*_])(\s*\1){2,}\s*$", line) and not para:
            blocks.append(Block("hr", i + 1, end_line=i + 1))
            i += 1
            continue

        m = IMAGE_LINE_RE.match(line)
        if m:
            flush_para(i)
            blocks.append(Block("image", i + 1, m.group(1), end_line=i + 1))
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]):
            flush_para(i)
            start = i
            rows = [_split_row(line)]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i]))
                i += 1
            blocks.append(Block("table", start + 1, "\n".join(lines[start:i]), rows=rows, end_line=i))
            continue

        if stripped.startswith(">"):
            flush_para(i)
            start = i
            body = []
            while i < n and lines[i].strip().startswith(">"):
                body.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append(Block("quote", start + 1, "".join(body), end_line=i))
            continue

        m = LIST_RE.match(line)
        if m and not para:
            start = i
            items: list[ListItem] = []
            indents: list[int] = []
            while i < n:
                lm = LIST_RE.match(lines[i])
                if lm:
                    indent = len(lm.group(1).replace("\t", "    "))
                    while indents and indent < indents[-1]:
                        indents.pop()
                    if not indents or indent > indents[-1]:
                        indents.append(indent)
                    items.append(ListItem(i + 1, len(indents), lm.group(3).strip(), lm.group(2)[0].isdigit()))
                    i += 1
                elif lines[i].strip() and lines[i].startswith((" ", "\t")) and items:
                    items[-1].text += lines[i].strip()
                    i += 1
                else:
                    break
            blocks.append(Block("list", start + 1, "\n".join(it.text for it in items), items=items, end_line=i))
            continue

        if not para:
            para_start = i
        para.append(line)
        i += 1

    flush_para(n)
    return blocks


def sections(blocks: list[Block], max_level: int = 6) -> list[Section]:
    """見出しごとにブロックをまとめる（入れ子にはしない。各見出しの直下だけを持つ）。"""
    out: list[Section] = [Section(None, [])]
    for b in blocks:
        if b.kind == "heading" and b.level <= max_level:
            out.append(Section(b, []))
        else:
            out[-1].blocks.append(b)
    if not out[0].blocks:
        out.pop(0)
    return out


def headings(blocks: list[Block]) -> list[Block]:
    return [b for b in blocks if b.kind == "heading"]
