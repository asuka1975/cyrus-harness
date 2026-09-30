"""読者ペルソナ（03-reader.json）から検査の閾値と語彙辞書を作る。"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

# 知識レベルごとの基準。数値は日本語の実務文書ガイドラインでよく使われる目安に合わせた。
BASE_PROFILES = {
    "novice": {
        "sentence_warn": 60, "sentence_error": 100,
        "paragraph_warn": 200, "paragraph_error": 350,
        "new_terms_per_section": 3, "chars_per_minute": 400,
    },
    "intermediate": {
        "sentence_warn": 70, "sentence_error": 110,
        "paragraph_warn": 250, "paragraph_error": 400,
        "new_terms_per_section": 4, "chars_per_minute": 500,
    },
    "expert": {
        "sentence_warn": 80, "sentence_error": 120,
        "paragraph_warn": 300, "paragraph_error": 450,
        "new_terms_per_section": 6, "chars_per_minute": 600,
    },
}

COMMON_LIMITS = {
    "commas_per_sentence": 4,       # 読点がこれを超えたら節が多すぎる
    "long_no_comma": 50,            # 読点のない文の長さ上限
    "kanji_run": 6,                 # 漢字の連続
    "kanji_ratio_doc": 0.40,
    "kanji_ratio_paragraph": 0.50,
    "paren_length": 25,
    "list_items": 7,
    "list_depth": 2,
    "table_cols": 6,
    "table_rows": 12,
    "heading_length": 30,
    "section_chars": 1500,
    "top_sections": 7,
}


@dataclass
class ReaderProfile:
    level: str = "intermediate"
    limits: dict = field(default_factory=dict)
    known_terms: set[str] = field(default_factory=set)
    unknown_terms: set[str] = field(default_factory=set)
    avoid_terms: list[dict] = field(default_factory=list)
    time_budget_min: float | None = None
    source: str = "default"

    def knows(self, term: str) -> bool:
        t = term.lower()
        return any(t == k.lower() for k in self.known_terms)

    def must_define(self, term: str) -> bool:
        t = term.lower()
        return any(t == k.lower() for k in self.unknown_terms)


def build_profile(reader: dict | None) -> ReaderProfile:
    reader = reader or {}
    level = reader.get("knowledge_level", "intermediate")
    if level not in BASE_PROFILES:
        level = "intermediate"
    limits = dict(COMMON_LIMITS)
    limits.update(BASE_PROFILES[level])
    ctx = reader.get("reading_context", {}) or {}
    if ctx.get("reading_mode") == "skim":
        limits["paragraph_warn"] -= 50
        limits["paragraph_error"] -= 50
    if ctx.get("medium") == "mobile":
        limits["paragraph_warn"] -= 50
        limits["paragraph_error"] -= 50
        limits["table_cols"] = 4
    avoid = []
    for a in reader.get("avoid_terms", []) or []:
        if isinstance(a, str):
            avoid.append({"term": a, "replace": ""})
        elif isinstance(a, dict) and a.get("term"):
            avoid.append({"term": a["term"], "replace": a.get("replace", "")})
    budget = ctx.get("time_budget_min")
    return ReaderProfile(
        level=level,
        limits=limits,
        known_terms=set(reader.get("known_terms", []) or []),
        unknown_terms=set(reader.get("unknown_terms", []) or []),
        avoid_terms=avoid,
        time_budget_min=float(budget) if isinstance(budget, (int, float)) and budget > 0 else None,
        source="03-reader.json" if reader else "default",
    )


def load_profile(path: Path | None) -> ReaderProfile:
    if path and path.exists():
        try:
            return build_profile(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            pass
    return build_profile(None)
