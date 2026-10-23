"""記録の集まりを数える（集計）。

同じ種類の記録（事例、ログ、チケット、回答、コミットなど）が複数あるとき、1件ずつ分類するのは LLM
（cyrus-fact-checker の仕事 C）が行い、数えるのは CLI が行う。分類の表（Markdown）を読み、件数と
分類ごとの数を返す。ステージ6の門は、06-facts.json の `tally` をこの数と照らす（半決定論）。

分類の表の形:

| # | 記録 | 分類 | 根拠 |
| --- | --- | --- | --- |
| E1 | 月替わり画面の認識のずれ | 伝わらない | 説明を2往復しても噛み合わなかった |

- 「分類」（「区分」「カテゴリ」でもよい）の列がある表をすべて読み、行を足し合わせる。
- 1つの記録が複数の分類に当たるときは「、」で区切る。どれにも当たらない記録は「該当なし」と書く（行を消さない）。
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from . import mdparse

LABEL_COLUMNS = ("分類", "区分", "カテゴリ")
LABEL_SPLIT_RE = re.compile(r"[、,／/]")


@dataclass
class Tally:
    total: int = 0                      # 記録の数（表の本文の行数）
    counts: dict[str, int] = field(default_factory=dict)   # 分類ごとの数（複数の分類に当たる記録は、それぞれに数える）
    column: str = ""                    # 読んだ列の名前
    unlabeled: list[int] = field(default_factory=list)     # 分類が空の行（本文の行番号。1始まり）
    error: str = ""                     # 読めなかった理由

    def to_dict(self) -> dict:
        d = {"total": self.total, "counts": dict(sorted(self.counts.items(), key=lambda kv: (-kv[1], kv[0])))}
        if self.unlabeled:
            d["unlabeled_rows"] = self.unlabeled
        if self.error:
            d["error"] = self.error
        return d


def read_items(path: Path) -> Tally:
    """分類の表を読んで数える。"""
    if not path.exists():
        return Tally(error=f"{path} がありません。")
    return count_text(path.read_text(encoding="utf-8"))


def count_text(text: str) -> Tally:
    tables = [b for b in mdparse.parse(text) if b.kind == "table" and b.rows]
    if not tables:
        return Tally(error="表がありません。")
    counts: Counter[str] = Counter()
    total = 0
    unlabeled: list[int] = []
    column = ""
    for t in tables:
        header = t.rows[0]
        idx = next((i for i, h in enumerate(header) if any(k in h for k in LABEL_COLUMNS)), None)
        if idx is None:
            continue
        column = column or header[idx]
        for row in t.rows[1:]:
            total += 1
            cell = row[idx].strip() if idx < len(row) else ""
            labels = [x.strip() for x in LABEL_SPLIT_RE.split(cell) if x.strip()]
            if not labels:
                unlabeled.append(total)
            for lab in labels:
                counts[lab] += 1
    if not column:
        return Tally(error="「" + "」「".join(LABEL_COLUMNS) + "」のいずれかの列がある表がありません。")
    return Tally(total=total, counts=dict(counts), column=column, unlabeled=unlabeled)


def same_counts(declared: dict, counted: dict[str, int]) -> bool:
    """06-facts.json に書いた counts と、CLI が数えた counts が一致するか（0 の分類は無視する）。"""
    if not isinstance(declared, dict):
        return False
    try:
        d = {str(k): int(v) for k, v in declared.items() if int(v) != 0}
    except (TypeError, ValueError):
        return False
    return d == {k: v for k, v in counted.items() if v != 0}


RATIO_RE = re.compile(r"(\d+\s*件中|のうち\s*\d+|\d+\s*割|\d+(?:\.\d+)?\s*[%％]|\d+\s*分の\s*\d+)")


def looks_like_ratio(statement: str) -> bool:
    """「19件中8件」「約3割」「62%」のような、数えた結果らしい言い方か。"""
    return bool(isinstance(statement, str) and RATIO_RE.search(statement))
