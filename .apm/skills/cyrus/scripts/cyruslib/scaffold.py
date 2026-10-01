"""成果物の雛形を作る。

前のステージの成果物から決まる部分（id の対応や Lean の骨組み）は決定論的に埋め、
判断が必要な部分は TODO として残す。TODO が残っている限りゲートは通らない。
"""

from __future__ import annotations

import json
import re

from .workspace import Workspace

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
                       "form": "TODO: capability（能力の文）か comparison（比較の文）", "premises": []},
        "claims": [
            {"id": "C1", "text": "TODO: C0 を支える主張", "type": "judgement",
             "form": "TODO: capability（能力の文）か comparison（比較の文）", "supports": "C0", "premises": ["F1"]}
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


def _doc(s: str) -> str:
    return s.replace("-/", "- /").replace("\n", " ").strip()


def lean_namespace(ws: Workspace) -> str:
    """slug から Lean の名前空間を作る（wiki-search → WikiSearch）。"""
    name = "".join(part[:1].upper() + part[1:] for part in re.split(r"[^A-Za-z0-9]+", ws.slug) if part)
    return name if name[:1].isalpha() else "Doc" + name


def _claims(ws: Workspace) -> list[dict]:
    claims = ws.read_json("05-claims.json") or {}
    main = dict(claims.get("main_claim") or {})
    main.setdefault("id", "C0")
    return [main] + list(claims.get("claims") or [])


WRITER_PROMISES = """## 書き方の約束（ガイド `stages/07-logic.md` の「Writer の約束」の要約）

- `def` は計算の手順だけに使う。現実についての判断は、宣言（中身を決めない `axiom`）と関係公理（型が命題の `axiom`）に分ける。
- 判断を、定理の引数、宣言の型、比較相手の定義、計算の def の docstring に置かない。
- 両方式の式に現れる量は、方式を引数に取る。「同じとみなす」なら【仮定】の関係公理にし、理由と向きを書く。
- 論証に必要な関係は、確信度が低くても省かない。要ファクトを付ける。
- 関係公理の型の最上位と ∀ の直下に ∧ を置かない（原子命題ごとに公理を分ける）。
- 関係公理の docstring の先頭に種類を書く: 【自明】（論拠）、【実験】（@support）、【経験則】（@support・@confidence・論拠・弱い点）、【仮定】（同上と「要ファクト:」）。
- 主張を示す定理に `@claim C…` を付ける。主張より強い定理は `@beyond C…`、比べる相手を確かめる定理は `@baseline`。
- 不利な結論も定理として導く。有利な向きの仮定を経由しない経路を選ぶ。
- 検査の警告を消すために、ラベルを変えたり、公理を省いたりしない。
- `@reviewer`・`@against`・`@restates` は Reviewer だけが付ける。
"""


def argument_template(ws: Workspace) -> str:
    ns = lean_namespace(ws)
    title = _doc(ws.load().get("title") or ws.slug)
    rows = "\n".join(f"| {c.get('id')} | {_doc(c.get('text', ''))} | TODO | TODO |" for c in _claims(ws))
    return f"""/-!
# 論証のモデル: {title}

設計書: `07-logic/model-plan.md`。主張: `05-claims.json`。事実: `06-facts.json`。

{WRITER_PROMISES}
## 主張と定理の対応

種類: [決定論] Prop の世界、[確率] 確率・期待値の比較、[件数] 件数の比較、[不利] 書き手の結論に不利な定理。

| 主張 | 主張の文 | 定理 | 種類 |
|---|---|---|---|
{rows}

## 設計書（model-plan.md）との違い

TODO: 設計書と違う書き方をしたところと、その理由。なければ「なし」。
-/

namespace {ns}

-- 公理で宣言した関数に依存する定義は実行できないので、すべて計算不能として扱う
noncomputable section

/-! ## §1 帰納型（定義） -/

/-! ## §2 宣言（中身を決めない型・関数・定数） -/

/-! ## §3 計算の def（手順だけ。判断を入れない） -/

/-! ## §4 関係公理 -/

/-! ## §5 主張の定理 -/

end

end {ns}
"""


def model_template(ws: Workspace) -> str:
    ns = lean_namespace(ws)
    return f"""/-!
# 証人: {_doc(ws.load().get("title") or ws.slug)}

`Argument.lean` のすべての `axiom` を、同じ名前・同じ型の具体的な `def` / `theorem` に差し替えた写し。公理系が無矛盾であることの証拠。
Writer が `Argument.lean` を書き終えてから作る。axiom 以外の行は、`Argument.lean` と同じ順で残す。
`instance`・`attribute`・`open`・`set_option` を足さない。証人の世界で、関係公理の結論が空回りしないようにする
（前提が実際に成り立つ例を持たせる）。

書き方: Argument.lean を写してから、axiom を1つずつ定義に差し替える。
-/

namespace {ns}

noncomputable section

end

end {ns}
"""


def model_plan_template(ws: Workspace) -> str:
    rows = "\n".join(f"| {c.get('id')} | {_doc(c.get('text', ''))} | TODO | TODO | TODO |" for c in _claims(ws))
    return f"""# 論証の設計書: {_doc(ws.load().get("title") or ws.slug)}

Logical Model Planner が書く。Lean Writer はこれに従って `Argument.lean` と `Model.lean` を書く。

## 1. 主張の形と論証の深さ

| 主張 | 主張の文 | 形（能力の文／比較の文） | 論証の世界（決定論／確率・件数） | 理由 |
|---|---|---|---|---|
{rows}

比較の文の主張があるときだけ、確率の世界（層・確率・「同じとみなす」判断）と失敗の台帳（`ledger.json`）を作る。

## 2. コンポーネント（宣言）

| 名前 | 型 | 何を表すか | 方式を引数に取るか |
|---|---|---|---|
| TODO | | | |

## 3. 関係公理（原子命題ごと）

命題は日常語で書く。式に近い書き方（例: 失われる時間 ≥ 費用）はよいが、Lean の構文は書かない（それは Writer の仕事）。

| 名前 | 種類 | 命題 | 支える事実 | 確信度の案 | 論拠 | 弱い点 | 要ファクト |
|---|---|---|---|---|---|---|---|
| TODO | 【自明】【実験】【経験則】【仮定】 | | F… | | | | |

## 4. 「同じとみなす」置き方

比較の文がなければ「比較なし」と書く。

| 公理 | 何を同じとみなすか | 理由 | どちらの方式に有利な向きか | 弱い点 |
|---|---|---|---|---|
| TODO | | | | |

## 5. 主張の項ごとの定理の計画

| 主張 | 項 | 定理の名前 | 使う判断（関係公理） | 種類 |
|---|---|---|---|---|
| TODO | | | | |

## 6. 比べる相手と、予想される不利な結論

TODO: 比べる相手（現実の相手にする）と、導くべき不利な結論。比較の文がなければ、比べる相手は「比較なし」とし、主張が成り立たない場合や条件（不利な結論）だけを書く。
"""


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
        "logic": [("07-logic/Argument.lean", lambda: argument_template(ws)),
                  ("07-logic/Model.lean", lambda: model_template(ws)),
                  ("07-logic/model-plan.md", lambda: model_plan_template(ws))],
        "structure": ("08-structure.json", lambda: _dump(structure_template(ws))),
        "storyline": ("09-storyline.json", lambda: _dump(storyline_template(ws))),
        "detail": ("10-detail.json", lambda: _dump(detail_template(ws))),
        "writing": ("draft.md", lambda: draft_template(ws)),
        "cogload": ("12-cogload.json", lambda: _dump(cogload_template())),
        "wording": ("final.md", lambda: ws.path("draft.md").read_text(encoding="utf-8") if ws.path("draft.md").exists() else ""),
    }
    entries = targets[key] if isinstance(targets[key], list) else [targets[key]]
    msgs = []
    for rel, make in entries:
        p = ws.path(rel)
        if p.exists() and not force:
            msgs.append(f"{rel} はすでにあります（上書きするなら --force）。")
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(make(), encoding="utf-8")
        msgs.append(f"{rel} を作りました。")
    return "\n".join(msgs)
