"""認知負荷の決定論的検査（lint）。

ルール ID の接頭辞:
  JA: 文・語のレベル（短期記憶・処理負荷）
  ST: 構造のレベル（見通し・中期記憶・視覚的なまとまり）
"""

from __future__ import annotations

import re
from collections import Counter

from . import jatext, mdparse, terms
from .issues import Issue, excerpt
from .reader import ReaderProfile, build_profile

DOUBLE_NEGATIVE = re.compile(
    r"(ないわけでは(ない|ありません)|なくは(ない|ありません)|ないとは(限ら|言え|いえ|限り)|"
    r"ないことは(ない|ありません)|ないでもない|なくもない|ざるを得(ない|ません)|"
    r"ないわけには(いかない|いきません)|ないではいられ)"
)
FAR_REFERENCE = re.compile(r"(後述|前述|上述|先述|下記|上記)")
PARA_HEAD_DEMONSTRATIVE = re.compile(r"^(これ|それ|あれ|これら|それら)(は|が|を|に|で|の|も)")
FIG_REF = re.compile(r"(図|表)\s*([0-9０-９]+)")
FIG_DEF = re.compile(r"^\s*\**\s*(図|表)\s*([0-9０-９]+)\s*\**\s*[：:．.　 ]")
NOUNISH_END = re.compile(r"[㐀-鿿ァ-ーA-Za-z0-9）)」]$")


FORMAL_NOUN_END = ("こと", "もの", "ところ", "とき", "ため", "かた", "まで", "から")


def _nounish(heading: str) -> bool:
    h = heading.rstrip("？?！!。")
    return bool(NOUNISH_END.search(h)) or h.endswith(FORMAL_NOUN_END)


def _norm_num(s: str) -> str:
    return s.translate(str.maketrans("０１２３４５６７８９", "0123456789"))


def _check_sentence(s: str, line: int, prof: ReaderProfile, issues: list[Issue], in_list: bool = False) -> None:
    L = prof.limits
    length = jatext.visible_length(s)
    if length > L["sentence_error"]:
        issues.append(Issue("JA001", "error", f"文が長すぎます（{length}字 > {L['sentence_error']}字）。2〜3文に分けてください。",
                            line, excerpt(s)))
    elif length > L["sentence_warn"]:
        issues.append(Issue("JA001", "warn", f"文が長めです（{length}字 > {L['sentence_warn']}字）。分けられないか検討してください。",
                            line, excerpt(s)))
    commas = s.count("、") + s.count("，")
    if commas > L["commas_per_sentence"] and not in_list:
        issues.append(Issue("JA002", "warn", f"読点が{commas}個あり、1文に節が多すぎます。", line, excerpt(s),
                            "箇条書きにするか文を分けてください。"))
    if commas == 0 and length > L["long_no_comma"]:
        issues.append(Issue("JA003", "warn", f"{length}字の文に読点がありません。意味の切れ目に読点を打つと読みやすくなります。",
                            line, excerpt(s)))
    run = jatext.longest_kanji_run(s)
    if len(run) >= L["kanji_run"]:
        issues.append(Issue("JA004", "warn", f"漢字が{len(run)}字続いています（{run}）。助詞を補うか、言い換えてください。",
                            line, excerpt(s)))
    m = DOUBLE_NEGATIVE.search(s)
    if m:
        issues.append(Issue("JA008", "warn", f"二重否定「{m.group(0)}」は読み手の処理を重くします。肯定文にしてください。",
                            line, excerpt(s)))
    for pm in re.finditer(r"[（(]([^（）()]*)[）)]", s):
        inner = pm.group(1)
        if jatext.visible_length(inner) > L["paren_length"]:
            issues.append(Issue("JA009", "warn", f"括弧の中が{jatext.visible_length(inner)}字あります。本文に出すか、別の文にしてください。",
                                line, excerpt(pm.group(0))))
    if re.search(r"[（(][^）)]*[（(]", s):
        issues.append(Issue("JA009", "warn", "括弧が入れ子になっています。", line, excerpt(s)))
    m = FAR_REFERENCE.search(s)
    if m:
        issues.append(Issue("JA011", "info", f"「{m.group(0)}」は読者に記憶の保持や視線の移動を求めます。その場で書くか、節名で示してください。",
                            line, excerpt(s)))


def lint_text(text: str, profile: ReaderProfile | None = None) -> tuple[list[Issue], dict]:
    prof = profile or build_profile(None)
    L = prof.limits
    blocks = mdparse.parse(text)
    issues: list[Issue] = []

    # ---- 見出し構造 ----
    heads = mdparse.headings(blocks)
    h1 = [h for h in heads if h.level == 1]
    if len(h1) > 1:
        issues.append(Issue("ST003", "error", f"H1 見出しが{len(h1)}個あります。タイトルは1つにしてください。", h1[1].line))
    prev_level = None
    for h in heads:
        if prev_level is not None and h.level > prev_level + 1:
            issues.append(Issue("ST001", "error", f"見出しレベルが H{prev_level} から H{h.level} に飛んでいます。", h.line, h.text))
        prev_level = h.level
        hl = jatext.visible_length(jatext.strip_inline(h.text))
        if hl > L["heading_length"]:
            issues.append(Issue("ST008", "warn", f"見出しが長すぎます（{hl}字）。見出しは拾い読みの手がかりなので短くしてください。",
                                h.line, h.text))
    top_level = min((h.level for h in heads if h.level > 1), default=2)
    top = [h for h in heads if h.level == top_level]
    if len(top) > L["top_sections"]:
        issues.append(Issue("ST002", "warn", f"最上位の節が{len(top)}個あります（目安は{L['top_sections']}個まで）。まとめられないか検討してください。"))

    # 同じ親を持つ見出しの形（名詞で終わるか、文で終わるか）の揃い
    groups: dict[tuple, list[mdparse.Block]] = {}
    parent_stack: list[mdparse.Block] = []
    for h in heads:
        while parent_stack and parent_stack[-1].level >= h.level:
            parent_stack.pop()
        key = (parent_stack[-1].line if parent_stack else 0, h.level)
        groups.setdefault(key, []).append(h)
        parent_stack.append(h)
    for sib in groups.values():
        if len(sib) < 3:
            continue
        kinds = ["noun" if _nounish(jatext.strip_inline(h.text)) else "phrase" for h in sib]
        c = Counter(kinds)
        if len(c) > 1:
            minority = min(c, key=c.get)
            odd = [h for h, k in zip(sib, kinds) if k == minority]
            issues.append(Issue("ST012", "info", "同じ階層の見出しで、名詞止めと文の形が混ざっています。形を揃えると構造がつかみやすくなります。",
                                odd[0].line, " / ".join(h.text for h in sib)))

    # ---- 節ごとの検査 ----
    styles: list[tuple[str, int, str]] = []
    endings: list[tuple[str, int, str]] = []
    all_text_parts: list[str] = []
    n_sentences = 0
    sentence_lengths: list[int] = []
    para_lengths: list[int] = []

    first_terms = terms.first_occurrences(blocks)

    for sec in mdparse.sections(blocks):
        sec_chars = 0
        new_terms_here = []
        content_blocks = [b for b in sec.blocks if b.kind != "hr"]
        for b in content_blocks:
            if b.kind in ("paragraph", "quote"):
                plain = jatext.strip_inline(b.text)
                plen = jatext.visible_length(plain)
                sec_chars += plen
                all_text_parts.append(plain)
                if b.kind == "paragraph":
                    para_lengths.append(plen)
                    if plen > L["paragraph_error"]:
                        issues.append(Issue("ST004", "error", f"段落が長すぎます（{plen}字 > {L['paragraph_error']}字）。分けてください。",
                                            b.line, excerpt(plain)))
                    elif plen > L["paragraph_warn"]:
                        issues.append(Issue("ST004", "warn", f"段落が長めです（{plen}字 > {L['paragraph_warn']}字）。",
                                            b.line, excerpt(plain)))
                    ratio = jatext.kanji_ratio(plain)
                    if plen >= 40 and ratio > L["kanji_ratio_paragraph"]:
                        issues.append(Issue("JA005", "warn", f"段落の漢字の割合が{ratio:.0%}です。ひらがなにひらくか言い換えてください。",
                                            b.line, excerpt(plain)))
                    m = PARA_HEAD_DEMONSTRATIVE.match(plain)
                    if m:
                        issues.append(Issue("JA010", "info", f"段落が指示語「{m.group(1)}」で始まっています。何を指すか名詞で書くと、読者が前の段落を思い出さずに済みます。",
                                            b.line, excerpt(plain)))
                for s in jatext.split_sentences(plain):
                    n_sentences += 1
                    sentence_lengths.append(jatext.visible_length(s))
                    _check_sentence(s, b.line, prof, issues)
                    if b.kind == "paragraph" and not FIG_DEF.match(plain):  # 図表のキャプションは体言止めが慣例
                        st = jatext.sentence_style(s)
                        if st != "neutral":
                            styles.append((st, b.line, s))
                        endings.append((jatext.sentence_ending(s), b.line, s))
                endings.append(("<break>", b.line, ""))
            elif b.kind == "list":
                items = b.items
                top_items = [it for it in items if it.depth == 1]
                if len(top_items) > L["list_items"]:
                    issues.append(Issue("ST006", "warn", f"箇条書きが{len(top_items)}項目あります（目安は{L['list_items']}項目まで）。グループに分けてください。",
                                        b.line))
                depth = max((it.depth for it in items), default=1)
                if depth > L["list_depth"]:
                    issues.append(Issue("ST006", "warn", f"箇条書きの入れ子が{depth}段あります（目安は{L['list_depth']}段まで）。",
                                        b.line))
                for it in items:
                    plain = jatext.strip_inline(it.text)
                    sec_chars += jatext.visible_length(plain)
                    all_text_parts.append(plain)
                    for s in jatext.split_sentences(plain):
                        n_sentences += 1
                        sentence_lengths.append(jatext.visible_length(s))
                        _check_sentence(s, it.line, prof, issues, in_list=True)
                endings.append(("<break>", b.line, ""))
            elif b.kind == "table":
                cols = max((len(r) for r in b.rows), default=0)
                rows = len(b.rows) - 1
                if cols > L["table_cols"]:
                    issues.append(Issue("ST007", "warn", f"表の列が{cols}列あります（目安は{L['table_cols']}列まで）。", b.line))
                if rows > L["table_rows"]:
                    issues.append(Issue("ST007", "warn", f"表の行が{rows}行あります（目安は{L['table_rows']}行まで）。分けるか要点だけにしてください。", b.line))
                for r in b.rows:
                    for c in r:
                        plain = jatext.strip_inline(c)
                        sec_chars += jatext.visible_length(plain)
                        all_text_parts.append(plain)
                endings.append(("<break>", b.line, ""))
            else:
                endings.append(("<break>", b.line, ""))
            if b.kind in ("paragraph", "list", "table", "quote"):
                end = b.end_line or b.line
                for key, occ in first_terms.items():
                    if b.line <= occ.line <= end and occ.kind != "code":
                        if not prof.knows(occ.term) and occ.term not in terms.COMMON_WORDS:
                            new_terms_here.append(occ.term)
        if sec_chars > L["section_chars"]:
            issues.append(Issue("ST005", "warn", f"節「{sec.title}」の本文が{sec_chars}字あり、小見出しがありません。小見出しで区切ってください。",
                                sec.heading.line if sec.heading else 1))
        uniq_new = list(dict.fromkeys(new_terms_here))
        if len(uniq_new) > L["new_terms_per_section"]:
            issues.append(Issue("ST011", "warn",
                                f"節「{sec.title}」に新しい用語が{len(uniq_new)}個出てきます（目安は{L['new_terms_per_section']}個まで）。"
                                "一度に覚える語が多いと短期記憶があふれます。",
                                sec.heading.line if sec.heading else 1, "、".join(uniq_new[:8])))

    # ---- 文体の混在 ----
    c = Counter(s for s, _, _ in styles)
    if c.get("desumasu") and c.get("plain"):
        major = "desumasu" if c["desumasu"] >= c["plain"] else "plain"
        minor = "plain" if major == "desumasu" else "desumasu"
        label = {"desumasu": "です・ます", "plain": "だ・である"}
        odd = [(ln, s) for st, ln, s in styles if st == minor]
        sev = "error" if len(odd) >= 2 else "warn"
        for ln, s in odd[:10]:
            issues.append(Issue("JA006", sev, f"文体が混ざっています。この文書は主に「{label[major]}」体ですが、この文は「{label[minor]}」体です。",
                                ln, excerpt(s)))

    # ---- 同じ文末の連続 ----
    run: list[tuple[str, int, str]] = []
    for e in endings + [("<break>", 0, "")]:
        if run and e[0] == run[-1][0] and e[0] != "<break>":
            run.append(e)
            continue
        if len(run) >= 3:
            issues.append(Issue("JA007", "warn", f"同じ文末「…{run[0][0]}」が{len(run)}文続いています。単調になり、区切りが見えにくくなります。",
                                run[0][1], excerpt(run[0][2])))
        run = [e] if e[0] != "<break>" else []

    # ---- 図表の参照 ----
    defined: dict[str, int] = {}
    referenced: dict[str, int] = {}
    for b in blocks:
        if b.kind == "image":
            for m in FIG_REF.finditer(b.text):
                defined.setdefault(m.group(1) + _norm_num(m.group(2)), b.line)
            continue
        if b.kind == "code":
            continue
        texts = [(b.line, b.text)] if b.kind != "list" else [(it.line, it.text) for it in b.items]
        for ln, t in texts:
            dm = FIG_DEF.match(jatext.strip_inline(t))
            def_key = dm.group(1) + _norm_num(dm.group(2)) if dm else None
            if def_key:
                defined.setdefault(def_key, ln)
            for m in FIG_REF.finditer(t):
                key = m.group(1) + _norm_num(m.group(2))
                if key == def_key and m.start() < 6:
                    continue
                referenced.setdefault(key, ln)
    for key, ln in referenced.items():
        if key not in defined:
            issues.append(Issue("ST010", "error", f"本文が「{key}」を参照していますが、{key}のキャプションが見つかりません。", ln))
    for key, ln in defined.items():
        if key not in referenced:
            issues.append(Issue("ST010", "warn", f"{key}は本文から参照されていません。読者は図表をいつ見ればよいかわかりません。", ln))

    # ---- 文書全体 ----
    full = "".join(all_text_parts)
    total_chars = jatext.visible_length(full)
    kr = jatext.kanji_ratio(full)
    if total_chars >= 200 and kr > L["kanji_ratio_doc"]:
        issues.append(Issue("JA005", "warn", f"文書全体の漢字の割合が{kr:.0%}です（目安は{L['kanji_ratio_doc']:.0%}以下）。"))
    minutes = total_chars / L["chars_per_minute"] if L["chars_per_minute"] else 0
    if prof.time_budget_min and minutes > prof.time_budget_min * 1.2:
        issues.append(Issue("ST013", "warn", f"推定読了時間が約{minutes:.1f}分で、読者が使える時間（{prof.time_budget_min:g}分）を超えています。削るか要約を先頭に置いてください。"))

    metrics = {
        "profile": prof.level,
        "chars": total_chars,
        "sentences": n_sentences,
        "avg_sentence_length": round(sum(sentence_lengths) / len(sentence_lengths), 1) if sentence_lengths else 0,
        "max_sentence_length": max(sentence_lengths, default=0),
        "paragraphs": len(para_lengths),
        "avg_paragraph_length": round(sum(para_lengths) / len(para_lengths), 1) if para_lengths else 0,
        "headings": len(heads),
        "kanji_ratio": round(kr, 3),
        "reading_minutes": round(minutes, 1),
        "styles": dict(c),
    }
    return issues, metrics
