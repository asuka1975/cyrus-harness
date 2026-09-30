"""言葉遣いの決定論的検査。

読者の知識集合（03-reader.json の known_terms / unknown_terms / avoid_terms）を辞書として扱い、
読者が知らない語が説明なしに使われていないか、避けるべき語が残っていないかを調べる。
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from . import jatext, mdparse, terms
from .issues import Issue, excerpt
from .reader import ReaderProfile, build_profile

RULES_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "wording-rules.json"


def load_rules(path: Path | None = None) -> dict:
    p = path or RULES_PATH
    return json.loads(p.read_text(encoding="utf-8"))


def _body_sentences(blocks):
    for line, s, kind in terms.iter_sentences(blocks):
        yield line, s


def check_wording(text: str, profile: ReaderProfile | None = None, glossary: dict | None = None,
                  rules: dict | None = None) -> tuple[list[Issue], dict]:
    prof = profile or build_profile(None)
    rules = rules if rules is not None else load_rules()
    glossary = glossary or {}
    blocks = mdparse.parse(text)
    issues: list[Issue] = []
    sentences = list(_body_sentences(blocks))
    heading_text = " ".join(h.text for h in mdparse.headings(blocks))

    # 1) 避けるべき語
    for a in prof.avoid_terms:
        pat = terms.term_pattern(a["term"])
        for line, s in sentences:
            if pat.search(s):
                issues.append(Issue("WD001", "error", f"読者に対して避けるべき語「{a['term']}」が使われています。", line, excerpt(s),
                                    f"「{a['replace']}」に言い換える" if a.get("replace") else "言い換えてください"))
        if pat.search(heading_text):
            issues.append(Issue("WD001", "error", f"見出しに避けるべき語「{a['term']}」が使われています。", None, "",
                                f"「{a['replace']}」に言い換える" if a.get("replace") else ""))

    # 2) 読者が知らない語（読者辞書の unknown_terms と、詳細設計で新出語とした語）が、初出で説明されているか
    must_define = set(prof.unknown_terms) | {g for g in glossary if not prof.knows(g)}
    for t in sorted(must_define):
        status, first, where = terms.definition_status(blocks, t)
        if status == "undefined":
            issues.append(Issue("WD002", "error", f"読者が知らない語「{t}」が説明なしに使われています。", first.line, excerpt(first.sentence),
                                f"初出で「{t}（〜のこと）」のように説明するか、読者が知っている語に言い換えてください。"))
        elif status == "late":
            issues.append(Issue("WD003", "error", f"「{t}」の説明が初出（{first.line}行目）より後（{where.line}行目）にあります。",
                                first.line, excerpt(first.sentence), "初出の位置で説明してください。"))

    # 3) 読者辞書にない語（知っているか判断が必要な語）
    firsts = terms.first_occurrences(blocks)
    unclassified = []
    for key, occ in firsts.items():
        t = occ.term
        if prof.knows(t) or prof.must_define(t) or t in terms.COMMON_WORDS or t in glossary:
            continue
        if terms.is_definition(t, occ.sentence):
            continue
        unclassified.append(occ)
    for occ in unclassified:
        issues.append(Issue("WD004", "info", f"「{occ.term}」は読者辞書にありません。読者が知っている語か判断し、知らなければ説明か言い換えをしてください。",
                            occ.line, excerpt(occ.sentence)))

    # 4) 硬い表現・冗長な表現
    for group, default_sev, rule_id in (("hard", "warn", "WD005"), ("redundant", "info", "WD006")):
        for r in rules.get(group, []):
            pat = re.compile(r["pattern"])
            sev = r.get("severity", default_sev)
            for line, s in sentences:
                m = pat.search(s)
                if m:
                    issues.append(Issue(rule_id, sev, f"「{m.group(0)}」: {r.get('reason', '')}", line, excerpt(s), r.get("suggest", "")))

    # 5) 表記ゆれ
    body = "\n".join(s for _, s in sentences) + "\n" + heading_text
    for group in rules.get("variants", []):
        found = {v: len(re.findall(re.escape(v) + ("(?!ー)" if v.endswith(("バ", "ザ", "タ", "リ", "ダ", "ス")) else ""), body)) for v in group}
        present = {v: c for v, c in found.items() if c}
        if len(present) > 1:
            issues.append(Issue("WD007", "warn", "表記ゆれがあります: " + "／".join(f"{v}（{c}回）" for v, c in present.items()),
                                None, "", "どちらかに統一してください。"))
    # 英字の大文字小文字のゆれ（GitHub / github など）
    latin = Counter()
    forms: dict[str, set[str]] = {}
    for _, s in sentences:
        for m in terms.LATIN_TERM.finditer(s):
            w = m.group(0)
            if len(w) < 2:
                continue
            latin[w.lower()] += 1
            forms.setdefault(w.lower(), set()).add(w)
    for k, fs in forms.items():
        if len(fs) > 1:
            issues.append(Issue("WD007", "warn", "英字の表記ゆれがあります: " + "／".join(sorted(fs)), None, "", "どれかに統一してください。"))
    # 全角英数字
    for line, s in sentences:
        if re.search(r"[０-９Ａ-Ｚａ-ｚ]", s):
            issues.append(Issue("WD008", "warn", "全角の英数字が使われています。半角に統一してください。", line, excerpt(s)))

    summary = {
        "unknown_terms_checked": len(prof.unknown_terms),
        "avoid_terms_checked": len(prof.avoid_terms),
        "unclassified_terms": [o.term for o in unclassified],
    }
    return issues, summary


def glossary_from_detail(detail: dict | None) -> dict:
    out = {}
    for sec in (detail or {}).get("sections", []) or []:
        for t in sec.get("new_terms", []) or []:
            if isinstance(t, dict) and t.get("term"):
                out[t["term"]] = t.get("definition", "")
    return out
