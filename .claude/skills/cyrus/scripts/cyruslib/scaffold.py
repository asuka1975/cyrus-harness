"""成果物の雛形を作る。

前のステージの成果物から決まる部分（id の対応や Lean の骨組み）は決定論的に埋め、
判断が必要な部分は TODO として残す。TODO が残っている限りゲートは通らない。
"""

from __future__ import annotations

import json
import re

from .workspace import Workspace
from . import leancheck

INTENT_MD = """# 目的のメモ

## 目的
TODO: この文書で何を実現したいか（例: 来期の予算で検索基盤の刷新を承認してもらう）

## 読者
TODO: 誰に向けた文書か（詳しくは Target Reader で描く）

## 伝えたいこと
TODO: 100字以内の1文で。これが文書全体の軸になる

## 読後の行動
TODO: 読み終えた読者に何をしてほしいか・何ができるようになってほしいか

## 種類と形式
TODO: 提案書・手順書・解説・報告など。Markdown か、スライドか、分量の目安

## 制約
TODO: 締め切り、字数、使ってはいけない情報、社内ルールなど。なければ「特になし」
"""

SOURCES_MD = """# 背景と素材

## 提供された素材
TODO: ユーザーから受け取ったファイル・URL・メモの一覧（- 名前: 場所・要点）

## 聞き取りメモ
TODO: 発端となった出来事、関係者、経緯、数字、ユーザーの考え

## 未確認の点
TODO: まだわかっていないこと・後で確かめること。なければ「なし」
"""

ANALYSIS_MD = """# 情報の分析

## 素材の要点
TODO: 素材ごとに、この文書に関係する要点

## 読者に必要な情報
TODO: 読者の疑問（03-reader.json の questions）に答えるために必要な情報

## 載せない情報
TODO: 正しいが、この読者・この目的には不要な情報と、その理由

## 不足している情報
TODO: 主張を支えるのに足りない情報。Fact Verification で調べるか、ユーザーに聞く

## 論点
TODO: 読者が疑問に思いそうな点・反論されそうな点
"""


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def reader_template() -> dict:
    return {
        "persona": {"name": "TODO: 呼び名（例: 情シスの田中さん）", "role": "TODO: 立場・職種",
                    "background": "TODO: 経験・前提知識・関心ごと"},
        "knowledge_level": "intermediate",
        "known_terms": [],
        "unknown_terms": [],
        "avoid_terms": [],
        "reading_context": {"medium": "screen", "reading_mode": "careful", "time_budget_min": 10},
        "motivation": "TODO: 読者がこの文書を読む理由",
        "questions": ["TODO: 読者が読む前に抱いている疑問"],
        "success_criteria": ["TODO: 読後に読者が〜できる"],
    }


def claims_template() -> dict:
    return {
        "main_claim": {"id": "C0", "text": "TODO: 文書全体で最も伝えたい主張（01-intent.md の「伝えたいこと」を精密にしたもの）",
                       "premises": []},
        "claims": [
            {"id": "C1", "text": "TODO: C0 を支える主張", "type": "judgement", "supports": "C0", "premises": ["F1"]}
        ],
        "facts": [
            {"id": "F1", "statement": "TODO: 主張の根拠になる事実（検証できる形で）", "source_hint": "TODO: どこで確かめられそうか"}
        ],
    }


def facts_template(ws: Workspace) -> dict:
    claims = ws.read_json("05-claims.json") or {}
    return {
        "facts": [
            {"id": f.get("id"), "statement": f.get("statement", ""), "status": "unverified", "method": "web",
             "sources": [], "evidence": "", "notes": "TODO: 検証の結果"}
            for f in claims.get("facts") or []
        ]
    }


def _ident(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", s)


def _doc(s: str) -> str:
    return s.replace("-/", "- /").replace("\n", " ").strip()


def lean_template(ws: Workspace) -> str:
    claims = ws.read_json("05-claims.json") or {}
    facts_doc = ws.read_json("06-facts.json") or {}
    status = {f.get("id"): f for f in facts_doc.get("facts") or []}
    main = dict(claims.get("main_claim") or {})
    main.setdefault("id", "C0")
    all_claims = [main] + list(claims.get("claims") or [])
    facts = claims.get("facts") or []
    by_id = {c["id"]: c for c in all_claims}

    # 主張の前提: premises に加えて、supports で自分を支えている下位の主張も前提にする
    premises: dict[str, list[str]] = {c["id"]: list(c.get("premises") or []) for c in all_claims}
    for c in all_claims[1:]:
        sup = c.get("supports")
        if sup in premises and c["id"] not in premises[sup]:
            premises[sup].append(c["id"])

    # 依存順に並べる（前提になる主張を先に証明する）
    order: list[str] = []
    seen: set[str] = set()

    def visit(cid: str, stack: tuple = ()) -> None:
        if cid in seen or cid in stack:
            return
        for p in premises.get(cid, []):
            if p in by_id:
                visit(p, stack + (cid,))
        seen.add(cid)
        order.append(cid)

    for c in all_claims:
        visit(c["id"])

    title = (ws.load().get("title") or ws.slug)
    L = [
        "/-!",
        f"# 論証構造: {_doc(title)}",
        "",
        "cyrus が 05-claims.json と 06-facts.json から作った雛形です。",
        "- 事実（fact_）の確からしさは 06-facts.json の status から自動で決まります。",
        "- 推論規則（rule_）には `@confidence 0〜1` と、その推論が成り立つ理由を書いてください。",
        "- 隠れた前提に気づいたら assume_ 公理として明示し、確からしさを付けてください。",
        "- 主張（P_C…）そのものを公理にしてはいけません。theorem claim_… として導きます。",
        "-/",
        "",
        "-- ========== 命題 ==========",
    ]
    for f in facts:
        L.append(f"/-- {f['id']}: {_doc(f.get('statement', ''))} -/")
        L.append(f"axiom P_{_ident(f['id'])} : Prop")
    for c in all_claims:
        L.append(f"/-- {c['id']}: {_doc(c.get('text', ''))} -/")
        L.append(f"axiom P_{_ident(c['id'])} : Prop")
    L += ["", "-- ========== 事実（Fact Verification の結果） =========="]
    for f in facts:
        st = status.get(f["id"], {}).get("status", "unverified")
        if st == "refuted":
            L.append(f"-- {f['id']} は反証されたため公理にしない（status=refuted）")
            continue
        conf = leancheck.fact_confidence(status.get(f["id"], {"status": st}))
        L.append(f"/-- @fact {f['id']} status={st} confidence={conf} -/")
        L.append(f"axiom fact_{_ident(f['id'])} : P_{_ident(f['id'])}")
    L += ["", "-- ========== 推論規則と主張 =========="]
    for cid in order:
        prem = [p for p in premises.get(cid, []) if p in by_id or p in {f['id'] for f in facts}]
        if not prem:
            L.append(f"-- {cid}: 前提がありません。05-claims.json の premises を見直してください。")
            L.append(f"theorem claim_{_ident(cid)} : P_{_ident(cid)} := sorry")
            L.append("")
            continue
        ante = " ∧ ".join(f"P_{_ident(p)}" for p in prem)
        proofs = []
        for p in prem:
            proofs.append(f"claim_{_ident(p)}" if p in by_id else f"fact_{_ident(p)}")
        arg = proofs[0] if len(proofs) == 1 else "⟨" + ", ".join(proofs) + "⟩"
        L.append(f"/-- @confidence TODO {cid} を導く論拠: TODO（なぜ前提から結論が言えるのか） -/")
        L.append(f"axiom rule_{_ident(cid)} : {ante} → P_{_ident(cid)}")
        L.append(f"theorem claim_{_ident(cid)} : P_{_ident(cid)} := rule_{_ident(cid)} {arg}")
        L.append("")
    return "\n".join(L).rstrip() + "\n"


def structure_template(ws: Workspace) -> dict:
    return {
        "title": (ws.load().get("title") or "TODO: 文書のタイトル"),
        "doc_type": "TODO: 提案書／手順書／解説／報告 など",
        "format": "markdown",
        "conclusion_first": True,
        "sections": [
            {"id": "S1", "heading": "TODO: 見出し", "level": 2, "purpose": "TODO: この節の役割",
             "reader_question": "TODO: この節が答える読者の疑問", "claims": ["C0"]}
        ],
    }


def storyline_template(ws: Workspace) -> dict:
    structure = ws.read_json("08-structure.json") or {}
    return {
        "pattern": "TODO: 例 結論→理由→具体例→行動（PREP）／状況→問題→解決（SCQA）など",
        "summary": "TODO: 文書全体を一文で",
        "sections": [
            {"id": s.get("id"), "heading": s.get("heading"), "message": "TODO: この節で読者が持ち帰る一文",
             "bridge": "" if i == 0 else "TODO: 前の節からのつなぎ"}
            for i, s in enumerate(structure.get("sections") or [])
        ],
    }


def detail_template(ws: Workspace) -> dict:
    structure = ws.read_json("08-structure.json") or {}
    return {
        "target_length_chars": 0,
        "sections": [
            {"id": s.get("id"), "heading": s.get("heading"),
             "blocks": [{"kind": "prose", "plan": "TODO: 何をどう見せるか", "why": ""}],
             "new_terms": [], "length_chars": 0}
            for s in structure.get("sections") or []
        ],
    }


def draft_template(ws: Workspace) -> str:
    structure = ws.read_json("08-structure.json") or {}
    story = {s.get("id"): s for s in (ws.read_json("09-storyline.json") or {}).get("sections") or []}
    L = [f"# {structure.get('title', ws.slug)}", ""]
    for s in structure.get("sections") or []:
        L.append(f"{'#' * int(s.get('level', 2))} {s.get('heading', '')}")
        L.append("")
        msg = story.get(s.get("id"), {}).get("message", "")
        L.append(f"<!-- TODO {s.get('id')}: {msg} -->")
        L.append("")
    return "\n".join(L)


def cogload_template() -> dict:
    return {
        "metrics_before": {},
        "metrics_after": {},
        "skim_test": {
            "draft_hash": "",
            "reader_summary": "",
            "main_claim_recovered": False,
            "sections": [],
        },
        "visual_test": {
            "draft_hash": "",
            "reader_model": "",
            "main_claim_recovered": False,
            "sections": [],
            "visual_notes_resolution": "",
        },
        "local_test": {"unclear_paragraphs": []},
        "persona_review": {"issues": []},
        "changes": [],
    }


def scaffold(ws: Workspace, key: str, force: bool = False) -> str:
    targets = {
        "intent": ("01-intent.md", lambda: INTENT_MD),
        "context": ("02-context/sources.md", lambda: SOURCES_MD),
        "reader": ("03-reader.json", lambda: _dump(reader_template())),
        "analysis": ("04-analysis.md", lambda: ANALYSIS_MD),
        "claims": ("05-claims.json", lambda: _dump(claims_template())),
        "facts": ("06-facts.json", lambda: _dump(facts_template(ws))),
        "logic": ("07-logic/Argument.lean", lambda: lean_template(ws)),
        "structure": ("08-structure.json", lambda: _dump(structure_template(ws))),
        "storyline": ("09-storyline.json", lambda: _dump(storyline_template(ws))),
        "detail": ("10-detail.json", lambda: _dump(detail_template(ws))),
        "writing": ("draft.md", lambda: draft_template(ws)),
        "cogload": ("12-cogload.json", lambda: _dump(cogload_template())),
        "wording": ("final.md", lambda: ws.path("draft.md").read_text(encoding="utf-8") if ws.path("draft.md").exists() else ""),
    }
    rel, make = targets[key]
    p = ws.path(rel)
    if p.exists() and not force:
        return f"{rel} はすでにあります（上書きするなら --force）。"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(make(), encoding="utf-8")
    return f"{rel} を作りました。"
