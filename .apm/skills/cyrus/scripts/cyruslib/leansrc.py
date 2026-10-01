"""Lean 4 のソースを、検査に必要な粒度で読む（コメントの除去、宣言と docstring の対応、名前空間、印の解析）。

型が命題かどうかや、原子命題の数などの意味の判定はここでは行わない。それは Lean に問い合わせる（leancheck.py）。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

KINDS = ("自明", "実験", "経験則", "仮定")
FACT_ID = r"F\d+[a-z]?"

DECL_RE = re.compile(
    r"^(?P<attrs>(?:@\[[^\]]*\]\s*)*)(?P<mods>(?:(?:private|protected|noncomputable|unsafe|partial|nonrec)\s+)*)"
    r"(?P<kw>axiom|theorem|lemma|def|abbrev|instance|inductive|structure|class|opaque)\b\s*(?P<name>[^\s:({\[⦃]*)"
)
SCOPE_RE = re.compile(r"^(?:(?P<nc>noncomputable)\s+)?(?P<kw>namespace|section|end)\b[ \t]*(?P<name>[^\s-]*)")


def mask_comments(src: str) -> tuple[str, list[tuple[int, int, str]]]:
    """コメントと文字列の中身を空白にした文字列と、docstring（/-- … -/）の一覧（開始位置、終了位置、本文）を返す。

    改行と位置は保つので、行番号はもとのソースと一致する。
    """
    out = list(src)
    docs: list[tuple[int, int, str]] = []
    i, n = 0, len(src)

    def blank(a: int, b: int) -> None:
        for k in range(a, b):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        c = src[i]
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            blank(i + 1, min(j, n))
            i = j + 1
        elif src.startswith("--", i):
            j = src.find("\n", i)
            j = n if j < 0 else j
            blank(i, j)
            i = j
        elif src.startswith("/-", i):
            is_doc = src.startswith("/--", i) and not src.startswith("/--/", i)
            depth, j = 1, i + 2
            while j < n and depth:
                if src.startswith("/-", j):
                    depth += 1
                    j += 2
                elif src.startswith("-/", j):
                    depth -= 1
                    j += 2
                else:
                    j += 1
            if is_doc:
                docs.append((i, j, src[i + 3: max(i + 3, j - 2)].strip()))
            blank(i, j)
            i = j
        else:
            i += 1
    return "".join(out), docs


@dataclass
class Decl:
    kw: str            # axiom / theorem / def / inductive …
    name: str          # ソースに書いた名前
    full: str          # 名前空間を含めた名前
    line: int          # キーワードのある行（1始まり）
    end_line: int      # 宣言の最後の行
    doc: str = ""
    doc_line: int = 0  # docstring の最初の行（なければ line と同じ）
    sig: str = ""      # 名前の後ろから宣言の終わりまで（コメントを除いたもの）

    @property
    def short(self) -> str:
        return self.full.rsplit(".", 1)[-1]


@dataclass
class Source:
    text: str
    masked: str
    decls: list[Decl] = field(default_factory=list)
    namespace_lines: int = 0  # 最初の namespace の行（0始まり。なければ最初のコードの行）

    def block(self, d: Decl) -> str:
        """宣言の docstring から宣言の終わりまでの原文。"""
        return "\n".join(self.lines[d.doc_line - 1:d.end_line])

    def by_kw(self, *kws: str) -> list[Decl]:
        return [d for d in self.decls if d.kw in kws]

    @property
    def lines(self) -> list[str]:
        return self.text.split("\n")


def parse(text: str) -> Source:
    masked, docs = mask_comments(text)
    mlines = masked.split("\n")
    # 行の開始位置
    starts = [0]
    for ln in mlines[:-1]:
        starts.append(starts[-1] + len(ln) + 1)
    doc_by_end_line: dict[int, tuple[int, str]] = {}
    for a, b, body in docs:
        doc_by_end_line[text.count("\n", 0, b)] = (text.count("\n", 0, a) + 1, body)

    scope: list[tuple[str, str]] = []  # (namespace|section, 名前)
    src = Source(text, masked)
    first_code = None
    decls: list[Decl] = []
    for idx, ml in enumerate(mlines):
        if not ml.strip():
            continue
        if ml[0] in " \t":
            continue  # 字下げされた行は、前の宣言の続き
        if first_code is None and not ml.startswith("import"):
            first_code = idx
        sm = SCOPE_RE.match(ml)
        if sm:
            kw, name = sm.group("kw"), sm.group("name")
            if kw == "namespace":
                scope.append(("namespace", name))
            elif kw == "section":
                scope.append(("section", name))
            else:  # end
                if name:
                    while scope and scope[-1][1] != name:
                        scope.pop()
                if scope:
                    scope.pop()
            continue
        dm = DECL_RE.match(ml)
        if not dm or not dm.group("name"):
            continue
        name = dm.group("name")
        ns = ".".join(n for k, n in scope if k == "namespace" and n)
        if name.startswith("_root_."):
            full = name[len("_root_."):]
        else:
            full = f"{ns}.{name}" if ns else name
        # 直前の docstring（空行・属性をはさまずに続くもの）
        doc, doc_line = "", idx + 1
        j = idx - 1
        while j >= 0 and not mlines[j].strip() and j not in doc_by_end_line:
            j -= 1
        if j in doc_by_end_line:
            doc_line, doc = doc_by_end_line[j]
        decls.append(Decl(dm.group("kw"), name, full, idx + 1, idx + 1, doc, doc_line))
    # 宣言の終わり: 次の「字下げのない行」の直前まで
    top_lines = [i for i, ml in enumerate(mlines) if ml.strip() and ml[0] not in " \t"]
    for d in decls:
        k = d.line - 1
        nxt = next((t for t in top_lines if t > k), len(mlines))
        end = nxt - 1
        while end > k and not mlines[end].strip():
            end -= 1
        d.end_line = end + 1
        body = "\n".join(mlines[k:end + 1])
        pos = body.find(d.name, len(DECL_RE.match(mlines[k]).group(0)) - len(d.name))
        d.sig = body[pos + len(d.name):].strip() if pos >= 0 else ""
    src.decls = decls
    src.namespace_lines = next((i for i, ml in enumerate(mlines) if ml.startswith("namespace ")), first_code or 0)
    return src


def split_binders(sig: str) -> tuple[str, str]:
    """`(x : T) : P x` を、束縛 `(x : T)` と型 `P x` に分ける（括弧の外の最初の `:` で）。"""
    depth = 0
    for i, ch in enumerate(sig):
        if ch in "([{⦃":
            depth += 1
        elif ch in ")]}⦄":
            depth -= 1
        elif ch == ":" and depth == 0 and not sig.startswith(":=", i):
            return sig[:i].strip(), sig[i + 1:].strip()
    return "", sig.strip()


def type_text(d: Decl) -> str:
    """公理の型を、1行の Lean の式として返す（束縛があれば ∀ で包む）。"""
    binders, typ = split_binders(d.sig)
    typ = re.sub(r"\s+", " ", typ)
    binders = re.sub(r"\s+", " ", binders)
    return f"∀ {binders}, {typ}" if binders else typ


# ---------------------------------------------------------------- docstring の印


@dataclass
class ReviewerMark:
    value: float | None
    original: float | None
    reason: str
    raw: str


@dataclass
class AxiomMarks:
    kind: str | None
    support: list[str]
    against: list[str]
    confidence: list[float]
    reviewer: list[ReviewerMark]
    needs_fact: bool
    weak_point_facts: list[str]


REVIEWER_RE = re.compile(r"^[ \t]*@reviewer\s+(?P<v>\S+)\s*(?:←|<-)\s*(?P<o>[^\s理]+)\s*(?:理由\s*[:：]\s*(?P<r>.*))?", re.M)


def _float(s: str) -> float | None:
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def _ids_on_lines(doc: str, tag: str) -> list[str]:
    ids: list[str] = []
    for m in re.finditer(rf"^[ \t]*@{tag}\b([^\n]*)", doc, re.M):
        if m.group(1).strip().startswith("なし"):
            continue  # 「@support なし（理由）」の理由に出る事実 ID は、支えではない
        ids += re.findall(FACT_ID + r"(?![0-9a-z])", m.group(1))
    return sorted(set(ids), key=fact_sort_key)


def fact_sort_key(fid: str):
    m = re.match(r"F(\d+)([a-z]?)", fid)
    return (int(m.group(1)), m.group(2)) if m else (10**9, fid)


def axiom_marks(doc: str) -> AxiomMarks:
    km = re.search(r"【(" + "|".join(KINDS) + r")】", doc)
    weak = []
    wm = re.search(r"弱い点\s*[:：](.*?)(?=\n\s*(?:要ファクト|論拠|@)|\Z)", doc, re.S)
    if wm:
        weak = sorted(set(re.findall(FACT_ID + r"(?![0-9a-z])", wm.group(1))), key=fact_sort_key)
    return AxiomMarks(
        kind=km.group(1) if km else None,
        support=_ids_on_lines(doc, "support"),
        against=_ids_on_lines(doc, "against"),
        confidence=[float(x) for x in re.findall(r"^[ \t]*@confidence\s+([0-9]*\.?[0-9]+)", doc, re.M)],
        reviewer=[ReviewerMark(_float(m.group("v")), _float(m.group("o")), (m.group("r") or "").strip(), m.group(0))
                  for m in REVIEWER_RE.finditer(doc)] + [
                     ReviewerMark(None, None, "", m.group(0)) for m in re.finditer(r"^[ \t]*@reviewer\b[^\n]*", doc, re.M)
                     if not REVIEWER_RE.match(m.group(0))],
        needs_fact="要ファクト" in doc,
        weak_point_facts=weak,
    )


@dataclass
class TheoremMarks:
    claims: list[str]
    beyond: list[str]
    baseline: bool
    restates: list[str]


def theorem_marks(doc: str) -> TheoremMarks:
    claims: list[str] = []
    for m in re.finditer(r"^[ \t]*@claim\b((?:[ \t,、]*C\d+)+)", doc, re.M):
        claims += re.findall(r"C\d+", m.group(1))
    beyond: list[str] = []
    for m in re.finditer(r"^[ \t]*@beyond\b((?:[ \t,、]*C\d+)*)", doc, re.M):
        beyond += re.findall(r"C\d+", m.group(1)) or ["*"]
    return TheoremMarks(
        claims=list(dict.fromkeys(claims)),
        beyond=list(dict.fromkeys(beyond)),
        baseline=bool(re.search(r"^[ \t]*@baseline\b", doc, re.M)),
        restates=re.findall(r"^[ \t]*@restates\s+([A-Za-z_][A-Za-z0-9_'.]*)", doc, re.M),
    )
