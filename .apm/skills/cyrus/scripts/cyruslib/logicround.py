"""ステージ7の周の記録（`cyrus logic-round`）。

Planner・Writer・Reviewer の3役のループを、周ごとに `07-logic/rounds/NN/` へ写して残す。
2周目からの局所修正では、前の周との差分を宣言ごとに取り、差分の設計書（model-plan-delta.md）の行との対応表を作る。
打ち切りの判定（高の指摘が0で、どの主張の確信度も前の周から上がらなかった）も、ここで決定論的に行う。
"""

from __future__ import annotations

import difflib
import json
import re
import shutil
from pathlib import Path

from datetime import datetime

from . import leancheck, leansrc
from .issues import Issue
from .workspace import now

ROUND_FILES = [
    "model-plan.md", "model-plan-delta.md", "ledger.json", "Argument.lean", "Model.lean",
    "writer-note.md", "review.md", "report.json", "hints.json", "rejected.json", "diff.md", "diff.patch",
]
MAX_ROUNDS = 3
DELTA_TEMPLATE = """# 差分の設計書（{n}周目）

前の周の review.md の指摘に答える。`cyrus logic-round diff` は「## 変更」の表の行だけを、差分との対応表に使う。

## 変更

1行に1つの変更。対象の宣言・公理・定理の名前を `名前` の形で必ず挙げる。指摘の ID がない変更は、答える指摘の欄に「—（理由）」と書く。

| # | 変更 | 対象 | 答える指摘 |
|---|---|---|---|
| 1 | TODO | `名前` | TODO |

## 新しい公理・宣言の中身

（命題、種類、支える事実、確信度の案、論拠、弱い点、要ファクト）

## 定理の計画の変更

（定理ごとの、使う判断と種類の変更。なければ「なし」）

## 台帳の変更

（ledger.json の変更。比較の文がなければ「比較なし」）

## 採らない指摘

（指摘の ID と、採らない理由・送り先のステージ）

## ステージ6で確かめること

（手戻りの一覧に入る公理のうち、先に事実を集めるべきものと、その順）

## 証人の見通しの変更

（なければ「なし」）

## Writer への注

（docstring に写さない注意。Writer は review.md を読まないので、指摘のうち Writer が知るべきことはここに書く）
"""
VERDICT_RE = re.compile(
    r"^判定\s*[:：]\s*(?P<verdict>[^（(\n]+?)\s*[（(]\s*高\s*(?P<h>\d+)\s*[・,、/]\s*中\s*(?P<m>\d+)\s*[・,、/]\s*低\s*(?P<l>\d+)\s*[）)]"
)


def _logic(doc_dir: Path) -> Path:
    return doc_dir / "07-logic"


def rounds(doc_dir: Path) -> list[Path]:
    d = _logic(doc_dir) / "rounds"
    if not d.exists():
        return []
    return sorted((p for p in d.iterdir() if p.is_dir() and re.fullmatch(r"\d{2}", p.name)), key=lambda p: p.name)


def read_verdict(review: Path) -> dict | None:
    """review.md の1行目「判定: …（高 N・中 N・低 N）」を読む。"""
    if not review.exists():
        return None
    first = next((ln.strip().lstrip("#").strip() for ln in review.read_text(encoding="utf-8").split("\n") if ln.strip()), "")
    m = VERDICT_RE.match(first)
    if not m:
        return None
    return {"verdict": m.group("verdict").strip(), "high": int(m.group("h")), "mid": int(m.group("m")), "low": int(m.group("l"))}


def _loop_start(doc_dir: Path) -> str | None:
    """いまのループが始まった時刻（ステージ7からステージ5・6へ最後に戻った時刻）。"""
    try:
        history = json.loads((doc_dir / "state.json").read_text(encoding="utf-8")).get("history") or []
    except (OSError, json.JSONDecodeError):
        return None
    backs = [h.get("at") for h in history if h.get("event") == "back" and h.get("from") == "logic" and h.get("at")]
    return backs[-1] if backs else None


def _after(a: str | None, b: str | None) -> bool:
    if not a or not b:
        return True
    try:
        return datetime.fromisoformat(a) > datetime.fromisoformat(b)
    except ValueError:
        return True


def close(doc_dir: Path) -> tuple[list[Issue], dict]:
    """いまの周を rounds/NN/ に写し、打ち切りを判定する。"""
    logic = _logic(doc_dir)
    verdict = read_verdict(logic / "review.md")
    if verdict is None:
        return [Issue("LR001", "error", "07-logic/review.md の1行目に「判定: …（高 N・中 N・低 N）」がありません。"
                                        "Reviewer の監査が終わってから周を閉じてください。")], {}
    issues, report = leancheck.check(doc_dir)
    gate_errors = sum(1 for i in issues if i.severity == "error")
    past = rounds(doc_dir)
    n = len(past) + 1
    # 3周の上限は、ループごとに数える（手戻りでステージ5・6へ戻って帰ってきたら、新しいループ）
    start = _loop_start(doc_dir)
    in_loop = 1 + sum(1 for p in past if (p / "round.json").exists()
                      and _after(json.loads((p / "round.json").read_text(encoding="utf-8")).get("closed_at"), start))
    prev_claims = {}
    if past:
        prev = json.loads((past[-1] / "report.json").read_text(encoding="utf-8")) if (past[-1] / "report.json").exists() else {}
        prev_claims = {k: v.get("confidence") for k, v in (prev.get("claims") or {}).items()}
    cur_claims = {k: v.get("confidence") for k, v in (report.get("claims") or {}).items()}
    raised = [{"claim": k, "from": prev_claims[k], "to": v} for k, v in cur_claims.items()
              if k in prev_claims and v is not None and prev_claims[k] is not None and v > prev_claims[k] + 1e-9]
    stop = verdict["high"] == 0 and not raised and gate_errors == 0
    if stop:
        reason = "高の指摘が0で、どの主張の確信度も前の周から上がらなかった。ループを止める。" if past else \
            "高の指摘が0で、比べる前の周がない（上がった主張はない）。ループを止める。"
    else:
        why = []
        if gate_errors:
            why.append(f"門のエラーが {gate_errors} 件ある")
        if verdict["high"]:
            why.append(f"高の指摘が {verdict['high']} 件ある")
        if raised:
            why.append("確信度が上がった主張がある（" + "、".join(f"{r['claim']} {r['from']}→{r['to']}" for r in raised) + "）")
        reason = "、".join(why) + "。"
    escalate = not stop and in_loop >= MAX_ROUNDS
    if escalate:
        reason += f" {MAX_ROUNDS}周で収まらなかったので、残った指摘を日常語でユーザーに見せ、判断を仰ぐ。"
    elif not stop:
        reason += " 指摘を役に戻し、局所修正で次の周へ進む。"

    dest = logic / "rounds" / f"{n:02d}"
    dest.mkdir(parents=True, exist_ok=True)
    for name in ROUND_FILES:
        if (logic / name).exists():
            shutil.copyfile(logic / name, dest / name)
    summary = {"round": n, "loop_round": in_loop, "closed_at": now(), **verdict, "gate_errors": gate_errors, "claims": cur_claims, "raised": raised,
               "stop": stop, "escalate": escalate, "reason": reason,
               "rework": [r["axiom"] for r in report.get("rework") or []]}
    (dest / "round.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # 周をまたいで残さないもの（次の周で書き直す）
    for name in ("diff.md", "diff.patch", "model-plan-delta.md"):
        if (logic / name).exists():
            (logic / name).unlink()
    if not stop and not escalate:
        (logic / "model-plan-delta.md").write_text(DELTA_TEMPLATE.format(n=n + 1), encoding="utf-8")
    return [], summary


# ---------------------------------------------------------------- 差分と対応表


def _blocks(text: str) -> tuple[dict[str, tuple[str, str, str]], list[str]]:
    """宣言ごとの（原文（docstring を含む）, コードだけ, 印の行）と、どの宣言にも属さない行。"""
    src = leansrc.parse(text)
    lines = src.lines
    mlines = src.masked.split("\n")
    owned: set[int] = set()
    blocks: dict[str, tuple[str, str]] = {}
    for d in src.decls:
        code = "\n".join(ln.rstrip() for ln in mlines[d.line - 1:d.end_line]).strip()
        marks = "\n".join(ln.strip() for ln in d.doc.split("\n")
                          if re.match(r"\s*(@|要ファクト|【|\[不利\])", ln))
        blocks[d.full] = (src.block(d), re.sub(r"\s+", " ", code), marks)
        owned.update(range(d.doc_line - 1, d.end_line))
    rest = [f"{i + 1}\t{ln}" for i, ln in enumerate(lines) if i not in owned]
    return blocks, rest


def _design_rows(text: str) -> list[tuple[str, set[str]]]:
    """差分の設計書の「## 変更」の節（なければ全体）の、表の行と箇条書きの行。"""
    m = re.search(r"^##\s*変更\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if m:
        text = m.group(1)
    rows = []
    for line in text.split("\n"):
        s = line.strip()
        if re.match(r"^\|[\s:|-]+\|$", s):
            continue
        if s.startswith("|") or re.match(r"^([-*+]|\d+[.)])\s", s):
            names = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_'.]*)`", s))
            if names:
                rows.append((s, names))
    return rows


def diff(doc_dir: Path) -> tuple[list[Issue], dict]:
    logic = _logic(doc_dir)
    past = rounds(doc_dir)
    if not past:
        return [Issue("LR002", "error", "前の周の記録がありません。先に `cyrus logic-round close` で1周目を閉じてください。")], {}
    prev = past[-1]
    changes: list[dict] = []
    same_name: list[tuple[str, bool]] = []
    unified: list[str] = []
    other_lines = 0
    other_where: list[str] = []
    for fname in ("Argument.lean", "Model.lean"):
        old_p, new_p = prev / fname, logic / fname
        old_t = old_p.read_text(encoding="utf-8") if old_p.exists() else ""
        new_t = new_p.read_text(encoding="utf-8") if new_p.exists() else ""
        ob, orest = _blocks(old_t)
        nb, nrest = _blocks(new_t)
        for name in sorted(set(ob) | set(nb)):
            if name not in ob:
                kind = "追加"
            elif name not in nb:
                kind = "削除"
            elif ob[name][1] != nb[name][1]:
                kind = "変更"
            elif ob[name][2] != nb[name][2]:
                kind = "変更（印）"  # @confidence・@reviewer・@support・【】などの行
            elif ob[name][0] != nb[name][0]:
                kind = "変更（説明だけ）"
            else:
                continue
            changes.append({"file": fname, "name": name.rsplit(".", 1)[-1], "full": name, "change": kind})
            if fname == "Argument.lean" and kind == "変更" and name in nb and nb[name][1].startswith("axiom"):
                same_name.append((name.rsplit(".", 1)[-1], "@reviewer" in nb[name][2]))
        o_txt = [r.split("\t", 1)[1] for r in orest]
        n_txt = [r.split("\t", 1)[1] for r in nrest]
        sm = difflib.SequenceMatcher(a=o_txt, b=n_txt, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            other_lines += max(i2 - i1, j2 - j1)
            if j2 > j1:
                other_where.append(f"{fname} {nrest[j1].split(chr(9))[0]}〜{nrest[j2 - 1].split(chr(9))[0]}行目")
            else:
                other_where.append(f"{fname}（前の周の {orest[i1].split(chr(9))[0]}〜{orest[i2 - 1].split(chr(9))[0]}行目を削除）")
        unified += list(difflib.unified_diff(old_t.split("\n"), new_t.split("\n"), f"rounds/{prev.name}/{fname}", fname,
                                             lineterm="", n=2))
    plan = logic / "model-plan-delta.md"
    rows = _design_rows(plan.read_text(encoding="utf-8")) if plan.exists() else []
    changed_arg = {c["name"] for c in changes if c["file"] == "Argument.lean"}
    table = []
    mentioned: set[str] = set()
    for text, names in rows:
        hit = sorted(names & changed_arg)
        mentioned |= names
        table.append({"row": text, "names": sorted(names), "hit": hit})
    unplanned = sorted(changed_arg - mentioned)

    out = [f"# 差分と対応表（rounds/{prev.name} → いま）", "",
           "`cyrus logic-round diff` が機械で作った。Reviewer は、差分の設計書の行が当たっているか、設計書にない変更がないかを確かめる。", "",
           "## 変わった宣言", "",
           "変化の種類: 「変更」はコード（公理の型、定理の文と証明、def）が変わった。「変更（印）」は `@confidence`・`@reviewer`・`@support`・【】などの印の行だけが変わった"
           "（`@reviewer` の行が消えていないかを見る）。「変更（説明だけ）」は docstring の説明だけが変わった。", "",
           "| ファイル | 宣言 | 変化 |", "|---|---|---|"]
    out += [f"| {c['file']} | `{c['name']}` | {c['change']} |" for c in changes] or ["| — | — | 変化なし |"]
    out += ["", f"宣言の外（見出し・説明のコメントなど）で変わった行: {other_lines}"
            + (f"（{'、'.join(other_where[:12])}{' ほか' if len(other_where) > 12 else ''}）" if other_where else ""), "",
            "## 差分の設計書（model-plan-delta.md）の行と差分の対応", ""]
    if not plan.exists():
        out.append("model-plan-delta.md がありません。")
    else:
        out += ["| # | 設計書の行 | 挙げた名前 | 当たった変更 |", "|---|---|---|---|"]
        for i, r in enumerate(table, 1):
            row = r["row"].replace("|", "／")
            row = row if len(row) <= 60 else row[:60] + "…"
            out.append(f"| {i} | {row} | {', '.join('`' + n + '`' for n in r['names'])} | "
                       f"{', '.join('`' + n + '`' for n in r['hit']) or '**当たっていない**'} |")
    out += ["", "## 命題（型）が変わったのに名前が同じ公理", "",
            "命題を変えたら名前も変えて別の公理にする決まり。`@reviewer` が残っているものは、前の周の Reviewer の判断が、変わった命題には当てはまらない。", ""]
    out += [f"- `{n}`" + ("（`@reviewer` が残っている）" if rv else "") for n, rv in same_name] or ["なし"]
    out += ["", "## 設計書に名前の出ていない変更", ""]
    out += [f"- `{n}`" for n in unplanned] or ["なし"]
    out += ["", "## 差分の全文", "", f"行ごとの差分は `07-logic/diff.patch` にある（{len(unified)} 行）。", ""]
    (logic / "diff.md").write_text("\n".join(out), encoding="utf-8")
    (logic / "diff.patch").write_text("\n".join(unified) + "\n", encoding="utf-8")
    summary = {"previous": prev.name, "changes": changes, "same_name_changed": [n for n, _ in same_name],
               "stale_reviewer": [n for n, rv in same_name if rv], "rows": len(table),
               "rows_without_hit": sum(1 for r in table if not r["hit"]), "unplanned": unplanned,
               "other_lines": other_lines, "diff_lines": len(unified)}
    return [], summary
