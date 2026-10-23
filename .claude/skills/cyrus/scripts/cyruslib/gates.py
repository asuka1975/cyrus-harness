"""ステージごとの完了条件（ゲート）。

ゲートは決定論的に判定する。LLM が作った成果物の「形」と「つじつま」を機械的に確かめ、
中身の良し悪しの判断はサブエージェントやユーザーとの対話に任せる。
"""

from __future__ import annotations

import json
import re

from . import figure, jatext, leancheck, lint, mdparse, skim, tally, wording, yomiyasu
from .issues import Issue
from .reader import build_profile
from .workspace import Workspace

PLACEHOLDER_RE = re.compile(r"(TODO|TBD|（未記入）|\(未記入\)|<ここに.*?>)")
CLAIM_ID = re.compile(r"^C\d+$")
FACT_ID = re.compile(r"^F\d+[a-z]?$")  # 分けた事実は枝番（F26a）
SECTION_ID = re.compile(r"^S\d+(\.\d+)*$")


# ---------------------------------------------------------------- 共通


def _md_sections(text: str, strip: bool = True) -> dict[str, str]:
    """H2 見出しごとの本文。strip=False なら行頭の字下げも残す（番号付きの項目を読むとき）。"""
    out: dict[str, list[str]] = {}
    cur = None
    in_code = False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
        m = re.match(r"^##\s+(.+?)\s*$", line) if not in_code else None
        if m:
            cur = m.group(1).strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: ("\n".join(v).strip() if strip else "\n".join(v)) for k, v in out.items()}


def _require_md(ws: Workspace, rel: str, headings: list[str]) -> tuple[list[Issue], dict[str, str]]:
    p = ws.path(rel)
    if not p.exists():
        return [Issue("GT000", "error", f"{rel} がありません。`cyrus scaffold` で雛形を作れます。")], {}
    secs = _md_sections(p.read_text(encoding="utf-8"))
    issues = []
    for h in headings:
        match = next((k for k in secs if k.startswith(h)), None)
        if match is None:
            issues.append(Issue("GT001", "error", f"{rel} に「## {h}」の節がありません。"))
        elif not secs[match] or PLACEHOLDER_RE.search(secs[match]):
            issues.append(Issue("GT002", "error", f"{rel} の「{h}」が未記入です。"))
    return issues, secs


def _load_json(ws: Workspace, rel: str) -> tuple[dict | None, list[Issue]]:
    p = ws.path(rel)
    if not p.exists():
        return None, [Issue("GT000", "error", f"{rel} がありません。`cyrus scaffold` で雛形を作れます。")]
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return None, [Issue("GT003", "error", f"{rel} が JSON として読めません: {e}")]
    if PLACEHOLDER_RE.search(json.dumps(data, ensure_ascii=False)):
        return data, [Issue("GT002", "error", f"{rel} に TODO などの未記入箇所が残っています。")]
    return data, []


def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _is(v, coll) -> bool:
    """列挙に含まれる文字列か（リストなど、ハッシュできない値が来ても例外にしない）。"""
    return isinstance(v, str) and v in coll


def _all_claims(claims: dict) -> list[dict]:
    main = dict(claims.get("main_claim") or {})
    main.setdefault("id", "C0")
    return [main] + list(claims.get("claims") or [])


# ---------------------------------------------------------------- 各ステージ


def gate_intent(ws: Workspace) -> list[Issue]:
    issues, secs = _require_md(ws, "01-intent.md", ["目的", "読者", "伝えたいこと", "読後の行動", "種類と形式", "制約"])
    key = next((k for k in secs if k.startswith("伝えたいこと")), None)
    if key and secs[key]:
        first = next((l.strip("-* 　") for l in secs[key].split("\n") if l.strip()), "")
        if jatext.visible_length(first) > 100:
            issues.append(Issue("GT010", "warn", "「伝えたいこと」の最初の行は、100字以内の1文にまとめてください。これが文書全体の軸になります。"))
    return issues


def gate_context(ws: Workspace) -> list[Issue]:
    issues, _ = _require_md(ws, "02-context/sources.md", ["提供された素材", "聞き取りメモ", "未確認の点"])
    return issues


READER_LEVELS = {"novice", "intermediate", "expert"}
MEDIA = {"screen", "mobile", "print", "slide", "mail"}  # mail: メール・チャットで読む（件名と冒頭で要件を示す構成になる）
AUDIENCE_SCOPES = {"internal": "社内", "external": "社外"}
# 読者は読後に何をするか（constructivism の「目的」。構成の系統を決める）
PURPOSES = {"decide": "決める（承認・決定する）", "report": "報告を受ける", "act": "作業する", "learn": "学ぶ", "lookup": "調べる",
            "understand": "理解する", "persuade": "動かされる（依頼・説得）", "verify": "検証する（学術）", "summary": "要点だけ知る"}
MODES = {"skim", "careful", "reference", "headline"}  # 拾い読み／通読／必要なときに引く／冒頭だけ（多忙な決裁者）


def gate_reader(ws: Workspace) -> list[Issue]:
    data, issues = _load_json(ws, "03-reader.json")
    if data is None:
        return issues
    p = data.get("persona") or {}
    for k in ("role", "background"):
        if not _nonempty_str(p.get(k)):
            issues.append(Issue("GT020", "error", f"persona.{k} を書いてください。"))
    if not _is(data.get("knowledge_level"), READER_LEVELS):
        issues.append(Issue("GT021", "error", f"knowledge_level は {sorted(READER_LEVELS)} のいずれかにしてください。"))
    if not _is(data.get("purpose"), PURPOSES):
        issues.append(Issue("GT029", "error", "purpose（読者は読後に何をするか）を次のいずれかにしてください: "
                                              + "、".join(f"{k}（{v}）" for k, v in PURPOSES.items()) + "。構成（ステージ8）を決める軸になります。"))
    if "audience_scope" in data and not _is(data["audience_scope"], AUDIENCE_SCOPES):
        issues.append(Issue("GT029", "error", "audience_scope（社内向けか社外向けか）は internal か external にしてください（省略すると社内）。"))
    for k in ("known_terms", "unknown_terms"):
        if not isinstance(data.get(k), list):
            issues.append(Issue("GT022", "error", f"{k} は語の配列にしてください（空でも可）。"))
    if isinstance(data.get("known_terms"), list) and isinstance(data.get("unknown_terms"), list):
        both = set(data["known_terms"]) & set(data["unknown_terms"])
        if both:
            issues.append(Issue("GT023", "error", f"known_terms と unknown_terms の両方に入っている語があります: {'、'.join(sorted(both))}"))
        if not data["known_terms"] and not data["unknown_terms"]:
            issues.append(Issue("GT024", "warn", "読者の語彙が空です。Wording Check の精度が下がるので、知っている語・知らない語を数語ずつでも入れてください。"))
    for a in data.get("avoid_terms", []) or []:
        if not (isinstance(a, dict) and _nonempty_str(a.get("term"))):
            issues.append(Issue("GT025", "error", "avoid_terms の各要素は {\"term\": ..., \"replace\": ...} にしてください。"))
    ctx = data.get("reading_context") if isinstance(data.get("reading_context"), dict) else {}
    if not _is(ctx.get("medium"), MEDIA):
        issues.append(Issue("GT026", "error", f"reading_context.medium は {sorted(MEDIA)} のいずれかにしてください。"))
    if not _is(ctx.get("reading_mode"), MODES):
        issues.append(Issue("GT026", "error", f"reading_context.reading_mode は {sorted(MODES)} のいずれかにしてください。"))
    if not (isinstance(ctx.get("time_budget_min"), (int, float)) and ctx["time_budget_min"] > 0):
        issues.append(Issue("GT026", "error", "reading_context.time_budget_min（読者が使える時間・分）を正の数で書いてください。"))
    if not _nonempty_str(data.get("motivation")):
        issues.append(Issue("GT027", "error", "motivation（読者がこの文書を読む理由）を書いてください。"))
    for k in ("questions", "success_criteria"):
        v = data.get(k)
        if not (isinstance(v, list) and v and all(_nonempty_str(x) for x in v)):
            issues.append(Issue("GT028", "error", f"{k} を1つ以上書いてください。"))
    return issues


DATASETS_HEADING = "集計できる素材"  # 04-analysis.md の節。同じ種類の記録が複数ある素材を、表で登録する


def datasets_of(text: str) -> dict[str, dict] | None:
    """04-analysis.md の「集計できる素材」の表を読む。節がなければ None。「なし」なら {}。

    表の列は、名前・単位・件数・置き場所・数える観点。名前の列（見出しに「名前」。なければ最初の列）で引く。
    """
    secs = _md_sections(text)
    body = next((v for k, v in secs.items() if k.startswith(DATASETS_HEADING)), None)
    if body is None:
        return None
    out: dict[str, dict] = {}
    for b in mdparse.parse(body):
        if b.kind != "table" or not b.rows:
            continue
        header = b.rows[0]
        name_i = next((i for i, h in enumerate(header) if "名前" in h), 0)
        count_i = next((i for i, h in enumerate(header) if "件数" in h), None)
        loc_i = next((i for i, h in enumerate(header) if "置き場所" in h or "場所" in h), None)
        for row in b.rows[1:]:
            name = row[name_i].strip() if name_i < len(row) else ""
            if not name or re.match(r"^[（(]例[）)]|^例\s*[:：]", name):  # 雛形の例の行は読まない
                continue
            m = re.search(r"\d+", row[count_i]) if count_i is not None and count_i < len(row) else None
            out[name] = {"count": int(m.group(0)) if m else None,
                         "location": row[loc_i].strip() if loc_i is not None and loc_i < len(row) else ""}
    return out


def _datasets(ws: Workspace) -> dict[str, dict]:
    p = ws.path("04-analysis.md")
    if not p.exists():
        return {}
    return datasets_of(p.read_text(encoding="utf-8")) or {}


def gate_analysis(ws: Workspace) -> list[Issue]:
    issues, secs = _require_md(ws, "04-analysis.md", ["素材の要点", "読者に必要な情報", "載せない情報", "不足している情報", "論点", DATASETS_HEADING])
    body = next((v for k, v in secs.items() if k.startswith(DATASETS_HEADING)), None)
    if body and not PLACEHOLDER_RE.search(body):
        ds = datasets_of(ws.path("04-analysis.md").read_text(encoding="utf-8")) or {}
        if not ds and not re.match(r"^\s*[-*]?\s*なし", body):
            issues.append(Issue("GT044", "warn", f"「{DATASETS_HEADING}」は、表（名前・単位・件数・置き場所・数える観点）で書くか、"
                                                 "なければ「なし」と書いてください。同じ種類の記録（事例、ログ、回答など）が複数ある素材は、"
                                                 "1件を選ぶ前に全件を数えます（ステージ5で dataset の事実、ステージ6で集計）。"))
        for name, d in ds.items():
            if d["count"] is None:
                issues.append(Issue("GT044", "warn", f"「{DATASETS_HEADING}」の「{name}」に件数（数字）がありません。"))
    return issues


CLAIM_TYPES = {"fact", "judgement", "proposal", "explanation"}
CLAIM_FORMS = {"capability", "comparison"}  # 能力の文／比較の文（ステージ7の論証の深さを決める）
# 主張の中心（C0）のメッセージ種別（constructivism の「メッセージ種別」。構成の型を決める）
MESSAGE_KINDS = {"proposal": "提言", "decision": "決定の記録", "report": "事実報告", "instruction": "手順指示",
                 "explanation": "概念説明", "comparison": "比較評価", "education": "教育"}


def gate_claims(ws: Workspace) -> list[Issue]:
    data, issues = _load_json(ws, "05-claims.json")
    if data is None:
        return issues
    main = data.get("main_claim") or {}
    if main.get("id", "C0") != "C0" or not _nonempty_str(main.get("text")):
        issues.append(Issue("GT030", "error", "main_claim は id \"C0\" と text（文書全体で最も伝えたい主張）を持たせてください。"))
    if not _is(main.get("message_kind"), MESSAGE_KINDS):
        issues.append(Issue("GT043", "error", "main_claim.message_kind（メッセージの種別）を次のいずれかにしてください: "
                                              + "、".join(f"{k}（{v}）" for k, v in MESSAGE_KINDS.items()) + "。構成（ステージ8）の型を決める軸になります。"))
    claims = _all_claims(data)
    for c in claims:
        if c.get("form") not in CLAIM_FORMS:
            issues.append(Issue("GT042", "error", f"主張 {c.get('id')} の form を capability（能力の文）か comparison（比較の文）にしてください。"
                                                  "比較の文を選ぶと、ステージ7で確率の世界を作ることになります。"))
    facts = data.get("facts") or []
    ids = [c.get("id") for c in claims]
    fids = [f.get("id") for f in facts]
    for i in ids:
        if not (isinstance(i, str) and CLAIM_ID.match(i)):
            issues.append(Issue("GT031", "error", f"主張の id「{i}」は C1, C2… の形にしてください。"))
    for i in fids:
        if not (isinstance(i, str) and FACT_ID.match(i)):
            issues.append(Issue("GT031", "error", f"事実の id「{i}」は F1, F2…（分けた事実は F26a のような枝番）の形にしてください。"))
    for dup in {x for x in ids + fids if (ids + fids).count(x) > 1}:
        issues.append(Issue("GT032", "error", f"id「{dup}」が重複しています。"))
    known = set(ids) | set(fids)
    for f in facts:
        if not _nonempty_str(f.get("statement")):
            issues.append(Issue("GT033", "error", f"事実 {f.get('id')} の statement を書いてください。"))
    parent: dict[str, str] = {}
    for c in claims[1:]:
        cid = c.get("id")
        if not _nonempty_str(c.get("text")):
            issues.append(Issue("GT033", "error", f"主張 {cid} の text を書いてください。"))
        if c.get("type") not in CLAIM_TYPES:
            issues.append(Issue("GT034", "error", f"主張 {cid} の type は {sorted(CLAIM_TYPES)} のいずれかにしてください。"))
        sup = c.get("supports")
        if sup not in ids or sup == cid:
            issues.append(Issue("GT035", "error", f"主張 {cid} の supports（支える上位の主張）が不正です: {sup}"))
        else:
            parent[cid] = sup
        prem = c.get("premises") or []
        if not prem:
            issues.append(Issue("GT036", "error", f"主張 {cid} に premises（根拠となる事実・主張の id）がありません。"))
        for p in prem:
            if p not in known:
                issues.append(Issue("GT037", "error", f"主張 {cid} の前提「{p}」が見つかりません。"))
            if p == cid:
                issues.append(Issue("GT037", "error", f"主張 {cid} が自分自身を前提にしています。"))
    main_prem = main.get("premises") or []
    for p in main_prem:
        if p not in known:
            issues.append(Issue("GT037", "error", f"C0 の前提「{p}」が見つかりません。"))
    # 循環の検出（supports と premises の両方をたどる）
    edges: dict[str, set[str]] = {c.get("id"): set(p for p in (c.get("premises") or []) if p in ids) for c in claims}
    for child, par in parent.items():
        edges.setdefault(par, set()).add(child)
    state: dict[str, int] = {}

    def dfs(u: str) -> bool:
        state[u] = 1
        for v in edges.get(u, ()):
            if state.get(v) == 1 or (state.get(v) is None and dfs(v)):
                return True
        state[u] = 2
        return False

    for u in list(edges):
        if state.get(u) is None and dfs(u):
            issues.append(Issue("GT038", "error", "主張の依存関係が循環しています。supports と premises を見直してください。"))
            break
    top = [c for c in claims[1:] if c.get("supports") == "C0"]
    if not top and not main_prem:
        issues.append(Issue("GT039", "error", "C0 を支える主張（supports: \"C0\"）か、C0 の premises が必要です。"))
    if len(top) > 5:
        issues.append(Issue("GT040", "warn", f"C0 を直接支える主張が{len(top)}個あります。読者が一度に持てるのは3〜4個です。まとめられないか検討してください。"))
    used = {p for c in claims for p in (c.get("premises") or [])}
    for f in fids:
        if f not in used:
            issues.append(Issue("GT041", "warn", f"事実 {f} はどの主張の前提にもなっていません。"))
    # 集計できる素材（04-analysis.md の表）は、全件を数えた事実（dataset）で主張を支える
    datasets = _datasets(ws)
    tallied = {f.get("dataset") for f in facts if _nonempty_str(f.get("dataset"))}
    for name, d in datasets.items():
        if name not in tallied:
            n = f"{d['count']} 件" if d.get("count") else "件数は 04 の表"
            issues.append(Issue("GT045", "warn", f"集計できる素材「{name}」（{n}）を数えた事実がありません。全件を分類して数えた事実を"
                                                 f"（\"dataset\": \"{name}\" を付けて）挙げてください。1件の事例だけでは、傾向や頻度の主張は支えられません。"
                                                 "数えない理由があるなら、04 の表から外して「載せない情報」に理由を書いてください。"))
    for f in facts:
        ds = f.get("dataset")
        if _nonempty_str(ds) and ds not in datasets:
            issues.append(Issue("GT046", "error", f"事実 {f.get('id')} の dataset「{ds}」は、04-analysis.md の「{DATASETS_HEADING}」にありません。"))
    return issues


FACT_STATUS = set(leancheck.STATUS_CONFIDENCE)
FACT_METHODS = {"web", "document", "execution", "user", "reasoning"}


def gate_facts(ws: Workspace) -> list[Issue]:
    data, issues = _load_json(ws, "06-facts.json")
    if data is None:
        return issues
    claims = ws.read_json("05-claims.json") or {}
    expected = {f.get("id"): f for f in claims.get("facts") or []}
    got = {f.get("id"): f for f in data.get("facts") or []}
    for fid in expected:
        if fid not in got:
            issues.append(Issue("GT050", "error", f"事実 {fid} の検証結果がありません。"))
    claim_ids = {c.get("id") for c in _all_claims(claims)}
    for fid in got:
        if fid in expected or got[fid].get("axioms"):
            continue
        backs = got[fid].get("claims")  # ステージ6の調査で足した事実: 支える主張の id
        if isinstance(backs, list) and backs:
            unknown = [c for c in backs if not _is(c, claim_ids)]
            if unknown:
                issues.append(Issue("GT051", "warn", f"事実 {fid} の claims にある {', '.join(map(str, unknown))} は、05-claims.json の主張にありません。"))
            continue
        issues.append(Issue("GT051", "warn", f"事実 {fid} は 05-claims.json にありません。主張側にも追加するか、"
                                             "ステージ6の調査で足した事実なら claims に支える主張の id を、"
                                             "ステージ7の手戻りで集めた事実なら axioms に公理の名前を書いてください。"))
    # ステージ7からの手戻り: 一覧の公理ごとに扱い（事実・棄却・集められなかった記録）があるか
    report = ws.read_json("07-logic/report.json") if ws.path("07-logic/report.json").exists() else None
    history = ws.load().get("history") or []
    back_from_logic = any(h.get("event") == "back" and h.get("from") == "logic" for h in history)
    if report and back_from_logic:
        covered = {a for f in got.values() for a in (f.get("axioms") or [])}
        rejected_doc = ws.read_json("07-logic/rejected.json") or {}
        covered |= {r.get("axiom") for r in rejected_doc.get("rejected") or [] if isinstance(r, dict)}
        open_items = [r["axiom"] for r in report.get("rework") or [] if r.get("axiom") not in covered]
        if open_items:
            issues.append(Issue("GT058", "warn", f"ステージ7の手戻りの一覧のうち {len(open_items)} 個の公理に、扱い（事実の axioms・rejected.json・集められなかった記録）がありません: "
                                                 + "、".join(open_items[:8]) + (" ほか" if len(open_items) > 8 else "")))
    arg = ws.path("07-logic/Argument.lean")
    if arg.exists():
        names = set(re.findall(r"^axiom\s+([A-Za-z_][A-Za-z0-9_'.]*)", arg.read_text(encoding="utf-8"), re.M))
        for fid, f in got.items():
            unknown = [a for a in f.get("axioms") or [] if a not in names]
            if unknown:
                issues.append(Issue("GT059", "warn", f"事実 {fid} の axioms にある {', '.join(unknown)} は、07-logic/Argument.lean の公理にありません。"))
    for fid, f in got.items():
        st = f.get("status")
        if st not in FACT_STATUS:
            issues.append(Issue("GT052", "error", f"事実 {fid} の status は {sorted(FACT_STATUS)} のいずれかにしてください。"))
            continue
        if f.get("method") not in FACT_METHODS:
            issues.append(Issue("GT053", "error", f"事実 {fid} の method は {sorted(FACT_METHODS)} のいずれかにしてください。"))
        if st in ("verified", "partially_verified", "refuted"):
            srcs = f.get("sources") or []
            if f.get("method") == "execution":
                if not _nonempty_str(f.get("evidence")):
                    issues.append(Issue("GT054", "error", f"事実 {fid} は実行で確かめたので、evidence（実行したことと結果）を書いてください。"))
            elif not srcs or not all(isinstance(s, dict) and _nonempty_str(s.get("title")) and (_nonempty_str(s.get("url")) or _nonempty_str(s.get("location"))) for s in srcs):
                issues.append(Issue("GT054", "error", f"事実 {fid} の sources に title と url（または location）を書いてください。"))
        if st == "refuted":
            users = [c.get("id") for c in _all_claims(claims) if fid in (c.get("premises") or [])]
            if users:
                issues.append(Issue("GT055", "error",
                                    f"事実 {fid} は反証されましたが、主張 {', '.join(users)} の前提になっています。"
                                    "`cyrus back claims` で主張を見直してください。"))
        for src in f.get("sources") or []:
            loc = src.get("location", "") if isinstance(src, dict) else ""
            path = re.split(r"[\s　（(]", loc.strip())[0] if isinstance(loc, str) else ""
            if path and "/" in path and not path.startswith(("http", "/")) and not (ws.dir / path).exists():
                issues.append(Issue("GT057", "warn", f"事実 {fid} の出典 {path} が文書のフォルダにありません。素材を 02-context/ に置くか、出典を直してください。"))
        if not _nonempty_str(f.get("notes")) and st != "verified":
            issues.append(Issue("GT056", "warn", f"事実 {fid} が verified でない理由や、確認できた範囲を notes に書いてください。"))
    issues += _check_tallies(ws, got)
    return issues


def _check_tallies(ws: Workspace, got: dict[str, dict]) -> list[Issue]:
    """集計の事実（dataset のある事実）: 分類の表（tally.items）を CLI が数え直し、tally の値と照らす。"""
    issues: list[Issue] = []
    datasets = _datasets(ws)
    for fid, f in got.items():
        st = f.get("status")
        t = f.get("tally")
        if _nonempty_str(f.get("dataset")) and st in ("verified", "partially_verified"):
            ok = (isinstance(t, dict) and _nonempty_str(t.get("items")) and isinstance(t.get("total"), int)
                  and isinstance(t.get("counts"), dict) and t["counts"] and _nonempty_str(t.get("criteria")))
            if not ok:
                issues.append(Issue("GT150", "error", f"事実 {fid} は集計の事実（dataset「{f['dataset']}」）です。tally に items（分類の表のパス。"
                                                      "記録1件に1行、「分類」の列）、total、counts、criteria（分類の基準）を書いてください。"
                                                      "分類は cyrus-fact-checker の仕事 C、数えるのは `cyrus tally <items>` です。"))
                continue
            res = tally.read_items(ws.dir / t["items"])
            if res.error:
                issues.append(Issue("GT151", "error", f"事実 {fid} の分類の表 {t['items']}: {res.error}"))
                continue
            if res.unlabeled:
                issues.append(Issue("GT151", "error", f"事実 {fid} の分類の表 {t['items']} に、分類が空の行があります（{', '.join(map(str, res.unlabeled))} 行目）。"
                                                      "どれにも当たらない記録は「該当なし」と書き、行を消さないでください。"))
                continue
            if res.total != t["total"] or not tally.same_counts(t["counts"], res.counts):
                counted = json.dumps(res.to_dict(), ensure_ascii=False)
                issues.append(Issue("GT152", "error", f"事実 {fid} の tally が、分類の表 {t['items']} を数えた結果と合いません。CLI の集計: {counted}。"
                                                      "tally をこの値にするか、表を直してください（statement の数字も合わせる）。"))
            d = datasets.get(f["dataset"]) or {}
            if d.get("count") and d["count"] != t["total"]:
                issues.append(Issue("GT153", "warn", f"事実 {fid} の tally.total（{t['total']}）が、04-analysis.md の「{f['dataset']}」の件数（{d['count']}）と違います。"
                                                     "記録の漏れか、04 の数え方の違いです。どちらかを直すか、notes に理由を書いてください。"))
        elif st in ("verified", "partially_verified") and not isinstance(t, dict) and tally.looks_like_ratio(f.get("statement", "")):
            quoted = any(re.search(r"\d", str(s.get("quote", ""))) for s in f.get("sources") or [] if isinstance(s, dict))
            if not quoted and not re.search(r"\d", str(f.get("evidence", ""))):
                issues.append(Issue("GT154", "info", f"事実 {fid} は割合や件数を述べていますが、数え方が残っていません。あなたが数えたなら"
                                                     "（04 の「集計できる素材」に登録し）dataset と tally を、出典の数字なら sources の quote にその数字を書いてください。"))
    return issues


def gate_logic(ws: Workspace) -> list[Issue]:
    issues, _ = leancheck.check(ws.dir)
    return issues


STYLES = {"敬体", "常体"}
OUTLINE_ITEM_RE = re.compile(r"^(\d+)\.\s+(.+?)\s*$")  # constructivism の骨子: 「1. 見出し（役割：…／目安：…）」
CHECK_ITEM_RE = re.compile(r"^\s*[-*]\s*\[([ xX])\][ \t]*(.+?)\s*$", re.M)  # constructivism の構成チェック: 「- [x] 項目」（判定理由の行は拾わない。項目文のない行で次の行を拾わないよう、] の後は行内の空白だけ）


def constructivism_dir():
    """constructivism スキル（asuka1975/constructivism）の場所。APM の依存として cyrus と同じ skills/ に入る。"""
    import os
    from pathlib import Path
    from .workspace import SKILL_DIR, project_root
    env = os.environ.get("CYRUS_CONSTRUCTIVISM")
    if env:
        return Path(env) if (Path(env) / "SKILL.md").exists() else None
    for cand in (SKILL_DIR.parent / "constructivism", project_root() / ".claude" / "skills" / "constructivism"):
        if (cand / "SKILL.md").exists():
            return cand
    return None


def outline_headings(md: str) -> list[str]:
    """08-structure.md（constructivism の出力）の「骨子」から、番号付きの見出しを順に取る。

    項目全体が字下げされていてもよいが（dedent する）、「入れる要素」の中の「3.1 …」のような下位の項目は拾わない。
    """
    import textwrap
    secs = _md_sections(md, strip=False)
    body = textwrap.dedent(next((v for k, v in secs.items() if k.startswith("骨子")), ""))
    out = []
    for line in body.split("\n"):
        m = OUTLINE_ITEM_RE.match(line)
        if not m:
            continue
        head = re.split(r"[（(]役割", m.group(2), 1)[0].strip()
        if head:
            out.append(head)
    return out


def selection_style(md: str) -> str | None:
    """08-structure.md の「構成選択結果」にある文体（敬体／常体）。なければ None。"""
    secs = _md_sections(md)
    sel = next((v for k, v in secs.items() if k.startswith("構成選択結果")), "")
    m = re.search(r"文体\s*[：:]\s*(敬体|常体)", sel)
    return m.group(1) if m else None


def gate_structure(ws: Workspace) -> list[Issue]:
    data, issues = _load_json(ws, "08-structure.json")
    if data is None:
        return issues
    if constructivism_dir() is None:
        issues.append(Issue("GT071", "error", "constructivism が見つかりません。`apm install` で入れてください"
                                              "（場所は環境変数 CYRUS_CONSTRUCTIVISM で指定できます）。"))
    md_path = ws.path("08-structure.md")
    outline: list[str] = []
    md_style = None
    if not md_path.exists():
        issues.append(Issue("GT072", "error", "08-structure.md（constructivism の出力）がありません。スキルを呼び、出力をそのまま保存してください。"))
    else:
        md = md_path.read_text(encoding="utf-8")
        secs = _md_sections(md)
        for h in ("構成選択結果", "骨子", "構成チェック"):
            if not any(k.startswith(h) for k in secs):
                issues.append(Issue("GT072", "error", f"08-structure.md に「## {h}」の節がありません。constructivism の出力を3節ともそのまま貼ってください。"))
        if PLACEHOLDER_RE.search(md):
            issues.append(Issue("GT002", "error", "08-structure.md に TODO などの未記入箇所が残っています。"))
        outline = outline_headings(md)
        md_style = selection_style(md)
        if not outline and any(k.startswith("骨子") for k in secs):
            issues.append(Issue("GT073", "error", "08-structure.md の「骨子」に「1. 見出し（役割：…）」の形の項目がありません。"))
        check = next((v for k, v in secs.items() if k.startswith("構成チェック")), None)
        if check is not None:
            items = CHECK_ITEM_RE.findall(check)
            if not items:
                issues.append(Issue("GT075", "warn", "08-structure.md の「構成チェック」に「- [x] 項目」の形の項目がありません。"
                                                     "constructivism の最終チェック（6項目と判定理由）までそのまま貼ってください。"))
            for mark, text in items:
                if not mark.strip():
                    issues.append(Issue("GT075", "warn", f"構成チェックの「{text}」が未達（[ ]）です。constructivism に骨子を直してもらうか、"
                                                         "直せない理由を 08-structure.md の仮定・逸脱に書いてください。"))
    for k in ("genre", "form"):
        if not _nonempty_str(data.get(k)):
            issues.append(Issue("GT074", "error", f"{k}（constructivism の{'採用構成' if k == 'genre' else '型'}）を書いてください。"))
    if not _is(data.get("style"), STYLES):
        issues.append(Issue("GT074", "error", "style は 敬体 か 常体 にしてください（constructivism の「文体」）。"))
    elif md_style and data["style"] != md_style:
        issues.append(Issue("GT074", "error", f"style「{data['style']}」が、constructivism の文体「{md_style}」（08-structure.md の構成選択結果）と違います。"
                                              "写し間違いなら直し、意図して変えるなら 08-structure.md の仮定・逸脱に理由を書いて文体の行も直してください。"))
    if not _nonempty_str(data.get("title")):
        issues.append(Issue("GT060", "error", "title を書いてください。"))
    secs = data.get("sections") or []
    if not secs:
        return issues + [Issue("GT061", "error", "sections が空です。")]
    heads_norm = [_norm_heading(s.get("heading", "")) if isinstance(s, dict) else "" for s in secs]
    positions = []
    for h in outline:
        if _norm_heading(h) not in heads_norm:
            issues.append(Issue("GT073", "error", f"骨子の見出し「{h}」が sections にありません。骨子の見出しはすべて節にします"
                                                  "（変えるなら 08-structure.md の骨子も直し、仮定・逸脱に理由を書く）。"))
        else:
            positions.append(heads_norm.index(_norm_heading(h)))
    if positions != sorted(positions):
        issues.append(Issue("GT073", "error", "sections の順序が 08-structure.md の骨子の順と違います。骨子の順に節を並べます"
                                              "（変えるなら 08-structure.md の骨子も直し、仮定・逸脱に理由を書く）。"))
    ids = [s.get("id") for s in secs]
    if any(not isinstance(s, dict) for s in secs):
        return issues + [Issue("GT061", "error", "sections の各要素はオブジェクトにしてください。")]
    for s in secs:
        if not (isinstance(s.get("id"), str) and SECTION_ID.match(s["id"])):
            issues.append(Issue("GT062", "error", f"節の id「{s.get('id')}」は S1, S2, S2.1 … の形にしてください。"))
        for k in ("heading", "purpose", "reader_question"):
            if not _nonempty_str(s.get(k)):
                issues.append(Issue("GT063", "error", f"節 {s.get('id')} の {k} を書いてください。"))
        if s.get("level") not in (2, 3, 4):
            issues.append(Issue("GT064", "error", f"節 {s.get('id')} の level は 2〜4 にしてください（1 はタイトル）。"))
    for dup in {x for x in ids if ids.count(x) > 1}:
        issues.append(Issue("GT065", "error", f"節の id「{dup}」が重複しています。"))
    heads = [s.get("heading") for s in secs]
    for dup in {x for x in heads if heads.count(x) > 1}:
        issues.append(Issue("GT065", "warn", f"見出し「{dup}」が重複しています。"))
    prev = 1
    for s in secs:
        lv = s.get("level") or 2
        if lv > prev + 1:
            issues.append(Issue("GT066", "error", f"節 {s.get('id')} で見出しレベルが {prev} から {lv} に飛んでいます。"))
        prev = lv
    top = [s for s in secs if s.get("level") == 2]
    if len(top) > 7:
        issues.append(Issue("GT067", "warn", f"最上位の節が{len(top)}個あります。7個以下にまとめると全体を見渡しやすくなります。"))
    claims = ws.read_json("05-claims.json") or {}
    cids = [c.get("id") for c in _all_claims(claims)]
    covered = {c for s in secs for c in (s.get("claims") or [])}
    for c in cids:
        if c not in covered:
            issues.append(Issue("GT068", "error", f"主張 {c} がどの節にも割り当てられていません。"))
    for c in covered - set(cids):
        issues.append(Issue("GT069", "error", f"節が存在しない主張 {c} を参照しています。"))
    first_two = {c for s in top[:2] for c in (s.get("claims") or [])}
    if "C0" not in first_two and data.get("conclusion_first", True):
        issues.append(Issue("GT070", "warn", "主張の中心 C0 が冒頭の2節にありません。結論を先に示すと読者の負荷が下がります"
                                              "（意図的に後に置く場合は conclusion_first: false を設定）。"))
    return issues


def gate_storyline(ws: Workspace) -> list[Issue]:
    data, issues = _load_json(ws, "09-storyline.json")
    if data is None:
        return issues
    if not _nonempty_str(data.get("summary")):
        issues.append(Issue("GT080", "error", "summary（文書全体を一文で）を書いてください。"))
    structure = ws.read_json("08-structure.json") or {}
    sids = [s.get("id") for s in structure.get("sections") or []]
    got = {s.get("id"): s for s in data.get("sections") or []}
    for sid in sids:
        if sid not in got:
            issues.append(Issue("GT081", "error", f"節 {sid} のメッセージがありません。"))
    for sid in got:
        if sid not in sids:
            issues.append(Issue("GT082", "error", f"節 {sid} は 08-structure.json にありません。"))
    order = [s.get("id") for s in data.get("sections") or [] if s.get("id") in sids]
    if order != [s for s in sids if s in got]:
        issues.append(Issue("GT083", "error", "09-storyline.json の節の順序が 08-structure.json と違います。"))
    form = str(structure.get("form") or "")
    pattern = str(data.get("pattern") or "")
    if form and pattern and _norm_heading(form) not in _norm_heading(pattern) and _norm_heading(pattern) not in _norm_heading(form):
        issues.append(Issue("GT088", "warn", f"pattern「{pattern}」が、構成の型「{form}」（08-structure.json の form）と違います。"
                                             "話の型は構成の型に合わせるか、変える理由を pattern に添えてください。"))
    for sid, s in got.items():
        msg = s.get("message", "")
        if not _nonempty_str(msg):
            issues.append(Issue("GT084", "error", f"節 {sid} の message（読者が持ち帰る一文）を書いてください。"))
            continue
        n = jatext.visible_length(msg)
        if n > 120:
            issues.append(Issue("GT085", "error", f"節 {sid} の message が{n}字あります。120字以内の1文にしてください。"))
        elif n > 80:
            issues.append(Issue("GT085", "warn", f"節 {sid} の message が{n}字あります。80字以内が目安です。"))
        if len(jatext.split_sentences(msg)) > 1:
            issues.append(Issue("GT086", "warn", f"節 {sid} の message が複数の文になっています。1文にしてください。"))
        if sid != (sids[0] if sids else None) and not _nonempty_str(s.get("bridge")):
            issues.append(Issue("GT087", "warn", f"節 {sid} の bridge（前の節からのつなぎ）を書いてください。"))
    return issues


BLOCK_KINDS = {"prose", "list", "table", "figure", "code", "callout", "example", "steps"}


def gate_detail(ws: Workspace) -> list[Issue]:
    data, issues = _load_json(ws, "10-detail.json")
    if data is None:
        return issues
    structure = ws.read_json("08-structure.json") or {}
    sids = [s.get("id") for s in structure.get("sections") or []]
    got = {s.get("id"): s for s in data.get("sections") or []}
    prof = build_profile(ws.read_json("03-reader.json"))
    limit = prof.limits["new_terms_per_section"]
    total = 0
    all_new_terms = set()
    for sid in sids:
        if sid not in got:
            issues.append(Issue("GT090", "error", f"節 {sid} の詳細設計がありません。"))
    for sid, s in got.items():
        blocks = s.get("blocks") or []
        if not blocks:
            issues.append(Issue("GT091", "error", f"節 {sid} に blocks がありません。"))
        for b in blocks:
            if b.get("kind") not in BLOCK_KINDS:
                issues.append(Issue("GT092", "error", f"節 {sid} のブロックの kind は {sorted(BLOCK_KINDS)} のいずれかにしてください。"))
            if not _nonempty_str(b.get("plan")):
                issues.append(Issue("GT093", "error", f"節 {sid} のブロックに plan（何をどう見せるか）を書いてください。"))
            if b.get("kind") in ("figure", "table") and not isinstance(b.get("spec"), dict):
                issues.append(Issue("GT094", "error", f"節 {sid} の{b.get('kind')}に spec（問い・答え・根拠の形・趣旨・パターン。"
                                                      "visual-patterns スキルで決める）を書いてください。"))
        nts = s.get("new_terms") or []
        for t in nts:
            if not (isinstance(t, dict) and _nonempty_str(t.get("term")) and _nonempty_str(t.get("definition"))):
                issues.append(Issue("GT095", "error", f"節 {sid} の new_terms は {{\"term\", \"definition\"}} の形にしてください。"))
            else:
                all_new_terms.add(t["term"])
        if len(nts) > limit + 2:
            issues.append(Issue("GT096", "error", f"節 {sid} で新しく導入する語が{len(nts)}個あります（読者の目安は{limit}個）。節を分けるか、語を減らしてください。"))
        elif len(nts) > limit:
            issues.append(Issue("GT096", "warn", f"節 {sid} で新しく導入する語が{len(nts)}個あります（読者の目安は{limit}個）。"))
        lc = s.get("length_chars")
        if not (isinstance(lc, int) and lc > 0):
            issues.append(Issue("GT097", "error", f"節 {sid} の length_chars（想定字数）を正の整数で書いてください。"))
        else:
            total += lc
    plans = json.dumps(data, ensure_ascii=False)
    for t in sorted(prof.unknown_terms):
        if t in plans and t not in all_new_terms:
            issues.append(Issue("GT098", "warn", f"読者が知らない語「{t}」を使う計画ですが、どの節の new_terms にもありません。"))
    target = data.get("target_length_chars")
    if isinstance(target, int) and target > 0 and total:
        if abs(total - target) / target > 0.3:
            issues.append(Issue("GT099", "warn", f"節の想定字数の合計（{total}字）が target_length_chars（{target}字）から30%以上ずれています。"))
    elif not (isinstance(target, int) and target > 0):
        issues.append(Issue("GT099", "error", "target_length_chars（文書全体の目標字数）を書いてください。"))
    if prof.time_budget_min and total:
        minutes = total / prof.limits["chars_per_minute"]
        if minutes > prof.time_budget_min * 1.2:
            issues.append(Issue("GT100", "warn", f"想定字数では読むのに約{minutes:.1f}分かかり、読者の時間（{prof.time_budget_min:g}分）を超えます。"))
    # 図表の spec を、visual-patterns のカタログの規則（手順2・5・6）で検査する
    issues += figure.check_detail(data, prof.level)
    return issues


def _norm_heading(s: str) -> str:
    return re.sub(r"\s+", "", jatext.strip_inline(s))


def gate_writing(ws: Workspace) -> list[Issue]:
    p = ws.path("draft.md")
    if not p.exists():
        return [Issue("GT000", "error", "draft.md がありません。")]
    text = p.read_text(encoding="utf-8")
    issues: list[Issue] = []
    structure = ws.read_json("08-structure.json") or {}
    heads = [(h.level, _norm_heading(h.text)) for h in mdparse.headings(mdparse.parse(text))]
    pos = 0
    for s in structure.get("sections") or []:
        want = _norm_heading(s.get("heading", ""))
        idx = next((i for i in range(pos, len(heads)) if heads[i][1] == want), None)
        if idx is None:
            if any(h[1] == want for h in heads):
                issues.append(Issue("GT110", "error", f"見出し「{s.get('heading')}」の順序が 08-structure.json と違います。"))
            else:
                issues.append(Issue("GT110", "error", f"見出し「{s.get('heading')}」（{s.get('id')}）が draft.md にありません。"
                                                      "構成を変えた場合は `cyrus back structure` で設計に戻してください。"))
            continue
        if heads[idx][0] != s.get("level"):
            issues.append(Issue("GT111", "warn", f"見出し「{s.get('heading')}」のレベルが設計（H{s.get('level')}）と違います（H{heads[idx][0]}）。"))
        pos = idx + 1
    if PLACEHOLDER_RE.search(text):
        issues.append(Issue("GT112", "error", "draft.md に TODO などの未記入箇所が残っています。"))
    # 文体が設計（08-structure.json の style）どおりか: 段落の文の過半数が、宣言した文体であること
    style = structure.get("style")
    if style in STYLES:
        counts = {"desumasu": 0, "plain": 0}
        for b in mdparse.parse(text):
            if b.kind in ("paragraph", "quote"):
                plain_text = jatext.strip_inline(b.text)
                if b.kind == "paragraph" and figure.CAPTION_RE.match(plain_text):
                    continue  # 図表のキャプションは答えの一文をそのまま書くので、文体の集計から外す（lint の JA006 と同じ扱い）
                for s in jatext.split_sentences(plain_text):
                    st = jatext.sentence_style(s)
                    if st in counts:
                        counts[st] += 1
        want = "desumasu" if style == "敬体" else "plain"
        other = "plain" if want == "desumasu" else "desumasu"
        if counts[want] + counts[other] >= 5 and counts[other] > counts[want]:
            issues.append(Issue("GT118", "error", f"文体が設計（{style}）と違います（です・ます {counts['desumasu']} 文、だ・である {counts['plain']} 文）。"
                                                  "本文の文体を設計に合わせるか、`cyrus back structure` で style を直してください。"))
    lint_issues, _ = lint.lint_text(text, build_profile(ws.read_json("03-reader.json")))
    for i in lint_issues:
        if i.rule in ("ST001", "ST003", "ST010") and i.severity == "error":
            issues.append(i)
    # 図表が設計（10-detail.json の spec）どおりか: キャプションに答えの一文、描き方、画像の有無
    issues += figure.check_draft(ws, text, ws.read_json("10-detail.json"))
    return issues


def _skim_score(skim: dict) -> float:
    secs = skim.get("sections") or []
    if not secs:
        return 0.0
    pts = {"yes": 1.0, "partial": 0.5, "no": 0.0}
    return sum(pts.get(s.get("recovered"), 0.0) for s in secs) / len(secs)


SKIM_THRESHOLD = 0.7


def _visual_tools_available() -> bool:
    """Chrome・Pillow・読み手のコマンドがそろっているか。読み手の設定に誤りがあれば ReaderConfigError。"""
    from . import visionreader, visual
    if not (visual.find_chrome() and visionreader.available()):
        return False
    try:
        import PIL  # noqa: F401
    except ImportError:
        return False
    return True


def _check_visual_test(ws: Workspace, vt: dict | None, sids: list, current_hash: str) -> list[Issue]:
    """画像での拾い読みテスト（読み手に読ませた結果を cyrus-alignment-judge が判定したもの）を検査する。"""
    from . import visionreader
    if not vt:
        return [Issue("GT140", "error", "visual_test（画像での拾い読みテスト）がありません。`cyrus vision` を実行し、"
                                        "cyrus-alignment-judge の判定を記録してください。")]
    if vt.get("skipped_reason"):
        try:
            usable = _visual_tools_available()
        except visionreader.ReaderConfigError as e:
            return [Issue("GT148", "error", f"読み手の設定に誤りがあります: {e}")]
        if usable:
            return [Issue("GT141", "error", "この環境では Chrome と読み手のコマンドが使えるので、画像での拾い読みテストは省略できません。")]
        return []
    rec = ws.path("skim/visual") / visionreader.RESULT_NAME
    try:
        run = json.loads(rec.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [Issue("GT142", "error", f"skim/visual/{visionreader.RESULT_NAME} がないか、読めません。"
                                        "`cyrus vision` で読み手に読ませてください。")]
    issues: list[Issue] = []
    if run.get("draft_hash") != current_hash or vt.get("draft_hash") != current_hash:
        issues.append(Issue("GT143", "error", "画像での拾い読みテストが、いまの draft.md で行われていません。"
                                              "原稿を直したら `cyrus vision` からやり直し、visual_test.draft_hash を更新してください。"))
    elif "assets_hash" in run and run["assets_hash"] != figure.assets_hash(ws, ws.path("draft.md").read_text(encoding="utf-8")):
        issues.append(Issue("GT143", "error", "画像での拾い読みテストのあとで、原稿が参照する画像ファイルが変わっています。`cyrus vision` からやり直してください。"))
    got = {s.get("id") for s in vt.get("sections") or []}
    for sid in sids:
        if sid not in got:
            issues.append(Issue("GT144", "error", f"visual_test.sections に節 {sid} の判定がありません。"))
    for s in vt.get("sections") or []:
        if s.get("recovered") not in ("yes", "partial", "no"):
            issues.append(Issue("GT144", "error", f"visual_test の節 {s.get('id')} の recovered は yes / partial / no にしてください。"))
    if vt.get("main_claim_recovered") is not True:
        issues.append(Issue("GT145", "error", "画像で拾い読みした読み手に、主張の中心（C0）が伝わっていません。"
                                              "冒頭の見出しと段落の最初の文、太字の使い方を見直してください。"))
    score = _skim_score(vt)
    if score < SKIM_THRESHOLD:
        issues.append(Issue("GT146", "error", f"画像での拾い読みテストの再現率が {score:.0%} です（基準 {SKIM_THRESHOLD:.0%}）。"
                                              "伝わらなかった節の見出し・段落の最初の文・太字を直し、再テストしてください。"))
    missed = ((run.get("result") or {}).get("visual_notes") or {}).get("missed_or_hidden") or []
    if missed and not _nonempty_str(vt.get("visual_notes_resolution")):
        issues.append(Issue("GT147", "warn", "読み手が「重要そうなのに目立たなかった」点を挙げています。"
                                             "どう対応したかを visual_test.visual_notes_resolution に書いてください。"))
    return issues


def gate_cogload(ws: Workspace) -> list[Issue]:
    data, issues = _load_json(ws, "12-cogload.json")
    draft = ws.path("draft.md")
    if not draft.exists():
        issues.append(Issue("GT000", "error", "draft.md がありません。"))
        return issues
    lint_issues, _ = lint.lint_text(draft.read_text(encoding="utf-8"), build_profile(ws.read_json("03-reader.json")))
    errs = [i for i in lint_issues if i.severity == "error"]
    if errs:
        issues.append(Issue("GT120", "error", f"draft.md に認知負荷のエラーが{len(errs)}件残っています（`cyrus lint` で確認）。"))
    if data is None:
        return issues
    structure = ws.read_json("08-structure.json") or {}
    sids = [s.get("id") for s in structure.get("sections") or []]
    skim_t = data.get("skim_test") or {}
    if not _nonempty_str(skim_t.get("reader_summary")):
        issues.append(Issue("GT121", "error", "skim_test.reader_summary（拾い読みした読者が再構成した要約）がありません。"))
    got = {s.get("id") for s in skim_t.get("sections") or []}
    for sid in sids:
        if sid not in got:
            issues.append(Issue("GT122", "error", f"skim_test.sections に節 {sid} の判定がありません。"))
    for s in skim_t.get("sections") or []:
        if s.get("recovered") not in ("yes", "partial", "no"):
            issues.append(Issue("GT123", "error", f"skim_test の節 {s.get('id')} の recovered は yes / partial / no にしてください。"))
    if skim_t.get("main_claim_recovered") is not True:
        issues.append(Issue("GT124", "error", "拾い読みで主張の中心（C0）が伝わっていません（main_claim_recovered が true ではない）。"
                                              "冒頭の要約・見出し・段落の最初の文を見直して、再テストしてください。"))
    current = skim.text_hash(draft.read_text(encoding="utf-8"))
    if skim_t.get("draft_hash") != current:
        issues.append(Issue("GT129", "error", "拾い読みテストが、いまの draft.md で行われていません（skim_test.draft_hash が一致しない）。"
                                              "原稿を直したら `cyrus skim` からテストをやり直し、表示された指紋を draft_hash に記録してください。"))
    score = _skim_score(skim_t)
    if score < SKIM_THRESHOLD:
        issues.append(Issue("GT125", "error", f"拾い読みテストの再現率が {score:.0%} です（基準 {SKIM_THRESHOLD:.0%}）。"
                                              "伝わらなかった節の見出しと段落の最初の文を直し、再テストしてください。"))
    issues += _check_visual_test(ws, data.get("visual_test"), sids, current)
    detail = ws.read_json("10-detail.json")
    draft_text = draft.read_text(encoding="utf-8")
    issues += figure.check_figure_test(ws, data.get("figure_test"), figure.planned(detail), current, draft_text, detail)
    review = data.get("persona_review") or {}
    if not isinstance(review.get("issues"), list):
        issues.append(Issue("GT126", "error", "persona_review.issues（ペルソナ読者が指摘した問題の一覧）がありません。"))
    else:
        for n, it in enumerate(review["issues"], 1):
            if not _nonempty_str(it.get("resolution")):
                issues.append(Issue("GT127", "error", f"persona_review の指摘 {n} に resolution（どう直したか、直さない理由）がありません。"))
    local = data.get("local_test")
    if local is not None and not isinstance(local.get("unclear_paragraphs", []), list):
        issues.append(Issue("GT128", "error", "local_test.unclear_paragraphs は配列にしてください。"))
    return issues


def gate_wording(ws: Workspace) -> list[Issue]:
    p = ws.path("final.md")
    if not p.exists():
        return [Issue("GT000", "error", "final.md がありません。draft.md を元に言葉遣いを直して final.md を作ってください。")]
    text = p.read_text(encoding="utf-8")
    prof = build_profile(ws.read_json("03-reader.json"))
    issues: list[Issue] = []
    lint_issues, _ = lint.lint_text(text, prof)
    errs = [i for i in lint_issues if i.severity == "error"]
    if errs:
        issues.append(Issue("GT130", "error", f"final.md に認知負荷のエラーが{len(errs)}件あります（`cyrus lint final.md`）。"))
    w_issues, _ = wording.check_wording(text, prof, wording.glossary_from_detail(ws.read_json("10-detail.json")))
    werrs = [i for i in w_issues if i.severity == "error"]
    if werrs:
        issues.append(Issue("GT131", "error", f"final.md に言葉遣いのエラーが{len(werrs)}件あります（`cyrus wording final.md`）。"))
    if PLACEHOLDER_RE.search(text):
        issues.append(Issue("GT132", "error", "final.md に TODO などの未記入箇所が残っています。"))
    # 推敲でキャプション（答えの一文）が書き換えられていないか、図表が設計どおりのままか
    issues += figure.check_draft(ws, text, ws.read_json("10-detail.json"), name="final.md")
    script = yomiyasu.find_check()
    if script is None:
        issues.append(Issue("GT133", "error", "yomiyasu が見つかりません。`apm install` で入れてください"
                                              "（場所は環境変数 CYRUS_YOMIYASU で yomiyasu_check.py を指定できます）。"))
    else:
        rc, status, first = yomiyasu.verify(script, p, ws.path("draft.md"))
        if rc != 0 and status == "no_record":
            issues.append(Issue("GT134", "error", "final.md に yomiyasu の検査の記録がありません（no_record）。"
                                                  "stages/13-wording.md の手順1で、yomiyasu で draft.md を推敲してください。"))
        elif rc != 0:
            reason = first.split("。")[0] + "。" if first else ""
            issues.append(Issue("GT134", "error", f"final.md が、yomiyasu で draft.md から推敲して検査した本文と合いません（{status}）。"
                                                  f"{reason}yomiyasu_check.py の run をやり直してから verify してください"
                                                  "（stages/13-wording.md の手順4）。"))
    return issues


GATES = {
    "intent": gate_intent,
    "context": gate_context,
    "reader": gate_reader,
    "analysis": gate_analysis,
    "claims": gate_claims,
    "facts": gate_facts,
    "logic": gate_logic,
    "structure": gate_structure,
    "storyline": gate_storyline,
    "detail": gate_detail,
    "writing": gate_writing,
    "cogload": gate_cogload,
    "wording": gate_wording,
}


def run_gate(ws: Workspace, key: str) -> list[Issue]:
    return GATES[key](ws)
