"""Lean 4 による論証構造の検証と、主張ごとの「確からしさ」の計算。

約束ごと（Logical Structure Design のガイドと同じ）:
  - 命題:     axiom P_<ID> : Prop          （ID は F1, C1 など）
  - 事実:     axiom fact_<Fの ID> : P_<Fの ID>         確からしさは 06-facts.json から決まる
  - 推論規則: axiom rule_<名前> : 前提 → 結論       docstring に @confidence <0〜1> を書く
  - 仮定:     axiom assume_<名前> : ...              docstring に @confidence <0〜1> を書く
  - 主張:     theorem claim_<Cの ID> : P_<Cの ID> := ...

主張の確からしさは、可能性論理（possibilistic logic）の考え方で求める。
  - 1つの導出の確からしさ = その定理が依存する公理（#print axioms で取得）の確からしさの最小値
    （鎖の強さは最も弱い輪で決まる）
  - 独立した導出（claim_<ID>_via_<名前>）が複数あれば、その最大値
参考値として、依存する公理の確からしさの積（独立を仮定した同時確率）も出す。
あいまいなものを公理として置き、事実に基づいて帰納的に確からしさを積み上げる考え方である。
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .issues import Issue

STATUS_CONFIDENCE = {
    "verified": 0.95,
    "partially_verified": 0.75,
    "user_asserted": 0.6,
    "unverified": 0.4,
    "refuted": 0.0,
}

HEDGES = [
    (0.85, "assert", "言い切る（〜です／〜である）"),
    (0.6, "moderate", "根拠を添えて控えめに言う（〜と考えられます／〜の傾向があります）"),
    (0.4, "tentative", "可能性として述べる（〜の可能性があります）"),
    (0.0, "hypothesis", "主張ではなく仮説・未確認事項として明示する"),
]

AXIOM_RE = re.compile(
    r"(?:/--(?P<doc>(?:(?!-/).)*)-/\s*)?(?:(?:private|protected|noncomputable)\s+)*axiom\s+(?P<name>[A-Za-z_][A-Za-z0-9_'.]*)\s*:\s*(?P<type>[^\n]*(?:\n[ \t]+\S[^\n]*)*)",
    re.DOTALL,
)
THEOREM_RE = re.compile(r"(?:theorem|lemma)\s+(claim_[A-Za-z0-9_]+)")
CONF_RE = re.compile(r"@confidence\s+([0-9]*\.?[0-9]+)")
DEPENDS_RE = re.compile(r"'([^']+)' depends on axioms: \[(.*?)\]", re.DOTALL)
NODEPS_RE = re.compile(r"'([^']+)' does not depend on any axioms")
ERROR_RE = re.compile(r"^.*?:(\d+):(\d+): error:?(.*)$", re.MULTILINE)


def find_lean() -> str | None:
    exe = shutil.which("lean")
    if exe:
        return exe
    cand = Path.home() / ".elan" / "bin" / "lean"
    return str(cand) if cand.exists() else None


def hedge_for(conf: float) -> dict:
    for threshold, key, text in HEDGES:
        if conf >= threshold:
            return {"level": key, "guidance": text}
    return {"level": "hypothesis", "guidance": HEDGES[-1][2]}


def fact_confidence(fact: dict) -> float:
    base = STATUS_CONFIDENCE.get(fact.get("status", "unverified"), 0.4)
    if isinstance(fact.get("confidence"), (int, float)):
        # 明示された値は、状態から決まる上限を超えられない
        return max(0.0, min(float(fact["confidence"]), base if base > 0 else 0.0))
    return base


def parse_axioms(src: str) -> list[dict]:
    out = []
    for m in AXIOM_RE.finditer(src):
        doc = (m.group("doc") or "").strip()
        typ = re.sub(r"\s+", " ", m.group("type")).strip()
        typ = re.sub(r"\s*--.*$", "", typ)
        conf = CONF_RE.search(doc)
        out.append({
            "name": m.group("name"),
            "type": typ,
            "doc": doc,
            "confidence": float(conf.group(1)) if conf else None,
            "line": src[: m.start("name")].count("\n") + 1,
        })
    return out


def run_lean(lean_file: Path, theorems: list[str], timeout: int = 180) -> tuple[int, str]:
    lean = find_lean()
    if not lean:
        return 127, "lean が見つかりません。elan で Lean 4 をインストールしてください（https://lean-lang.org/install/）。"
    src = lean_file.read_text(encoding="utf-8")
    probe = src.rstrip() + "\n\n" + "\n".join(f"#print axioms {t}" for t in theorems) + "\n"
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / lean_file.name
        tmp.write_text(probe, encoding="utf-8")
        try:
            proc = subprocess.run([lean, str(tmp)], capture_output=True, text=True, timeout=timeout,
                                  cwd=str(lean_file.parent), env=os.environ.copy())
        except subprocess.TimeoutExpired:
            return 124, f"Lean の検査が {timeout} 秒でタイムアウトしました。"
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.replace(str(tmp), lean_file.name)


def check(doc_dir: Path, write_report: bool = True) -> tuple[list[Issue], dict]:
    issues: list[Issue] = []
    lean_file = doc_dir / "07-logic" / "Argument.lean"
    claims_path = doc_dir / "05-claims.json"
    facts_path = doc_dir / "06-facts.json"
    if not lean_file.exists():
        return [Issue("LG000", "error", "07-logic/Argument.lean がありません。`cyrus scaffold logic` で雛形を作ってください。")], {}
    try:
        claims = json.loads(claims_path.read_text(encoding="utf-8"))
        facts_doc = json.loads(facts_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [Issue("LG000", "error", f"05-claims.json / 06-facts.json を読めません: {e}")], {}

    claim_ids = [claims.get("main_claim", {}).get("id", "C0")] + [c["id"] for c in claims.get("claims", []) if "id" in c]
    facts = {f["id"]: f for f in facts_doc.get("facts", []) if "id" in f}
    src = lean_file.read_text(encoding="utf-8")

    if re.search(r"\bsorry\b", re.sub(r"--[^\n]*|/-.*?-/", "", src, flags=re.DOTALL)):
        issues.append(Issue("LG001", "error", "sorry が残っています。証明を完成させるか、足りない前提を assume_ 公理として明示してください。"))

    axioms = parse_axioms(src)
    ax_by_name = {a["name"]: a for a in axioms}
    confidences: dict[str, float] = {}
    for a in axioms:
        name, typ = a["name"], a["type"]
        if typ == "Prop":
            continue
        if re.fullmatch(r"\(?\s*P_C[A-Za-z0-9_]*\s*\)?", typ):
            issues.append(Issue("LG002", "error", f"公理 {name} が主張の命題（{typ}）を直接仮定しています。主張は theorem として導いてください。", a["line"]))
        if name.startswith("fact_"):
            fid = name[len("fact_"):]
            if fid not in facts:
                issues.append(Issue("LG003", "error", f"{name} に対応する事実 {fid} が 06-facts.json にありません。", a["line"]))
                confidences[name] = 0.0
            else:
                c = fact_confidence(facts[fid])
                if facts[fid].get("status") == "refuted":
                    issues.append(Issue("LG004", "error", f"事実 {fid} は反証されています（refuted）。この事実を公理にしてはいけません。", a["line"]))
                confidences[name] = c
        elif name.startswith(("rule_", "assume_")):
            if a["confidence"] is None:
                issues.append(Issue("LG005", "error", f"{name} に確からしさがありません。docstring に `@confidence 0.8` のように書き、理由も添えてください。", a["line"]))
                confidences[name] = 0.0
            elif not 0 <= a["confidence"] <= 1:
                issues.append(Issue("LG005", "error", f"{name} の確からしさ {a['confidence']} は 0〜1 の範囲外です。", a["line"]))
                confidences[name] = 0.0
            else:
                confidences[name] = a["confidence"]
                if len(CONF_RE.sub("", a["doc"]).strip()) < 4:
                    issues.append(Issue("LG006", "warn", f"{name} の docstring に、その推論が成り立つ理由（論拠）を書いてください。", a["line"]))
        else:
            issues.append(Issue("LG007", "error", f"公理 {name} の名前が約束ごとに合いません。fact_ / rule_ / assume_ のいずれかで始めてください。", a["line"]))

    theorems = THEOREM_RE.findall(src)
    derivations: dict[str, list[str]] = {cid: [] for cid in claim_ids}
    for t in theorems:
        m = re.fullmatch(r"claim_(C\d+)(?:_via_[A-Za-z0-9_]+)?", t)
        if m and m.group(1) in derivations:
            derivations[m.group(1)].append(t)
    for cid in claim_ids:
        if not derivations[cid]:
            issues.append(Issue("LG008", "error", f"主張 {cid} を導く theorem claim_{cid}（または claim_{cid}_via_…）がありません。"))

    code, out = run_lean(lean_file, theorems)
    for m in ERROR_RE.finditer(out):
        issues.append(Issue("LG009", "error", f"Lean のエラー: {m.group(3).strip()}", int(m.group(1))))
    if code != 0 and not ERROR_RE.search(out):
        issues.append(Issue("LG009", "error", f"Lean の実行に失敗しました（終了コード {code}）: {out.strip()[:300]}"))

    deps: dict[str, list[str]] = {}
    for m in DEPENDS_RE.finditer(out):
        deps[m.group(1).split(".")[-1]] = [x.strip().split(".")[-1] for x in m.group(2).split(",") if x.strip()]
    for m in NODEPS_RE.finditer(out):
        deps[m.group(1).split(".")[-1]] = []

    claim_text = {claims.get("main_claim", {}).get("id", "C0"): claims.get("main_claim", {}).get("text", "")}
    claim_text.update({c["id"]: c.get("text", "") for c in claims.get("claims", []) if "id" in c})
    results = {}
    used_facts: set[str] = set()
    for cid in claim_ids:
        derivs = []
        for t in derivations[cid]:
            if t not in deps:
                continue
            used = [d for d in deps[t] if d in ax_by_name and ax_by_name[d]["type"] != "Prop"]
            if "sorryAx" in deps[t]:
                issues.append(Issue("LG001", "error", f"{t} が sorry に依存しています。"))
            # 連言は最も弱い根拠で決まる（可能性論理の必然性の度合い）。積は独立を仮定した参考値。
            nec = min((confidences.get(d, 0.0) for d in used), default=1.0)
            joint = 1.0
            for d in used:
                joint *= confidences.get(d, 0.0)
            if "sorryAx" in deps[t]:
                nec = joint = 0.0
            weakest = min(used, key=lambda d: confidences.get(d, 0.0)) if used else None
            used_facts.update(d[len("fact_"):] for d in used if d.startswith("fact_"))
            derivs.append({"theorem": t, "confidence": nec, "joint": joint, "depends_on": used, "weakest": weakest})
        if not derivs:
            continue
        # 独立した導出が複数あれば、最も強い導出を採る（選言は最大値）
        best = max(derivs, key=lambda d: (d["confidence"], d["joint"]))
        if len(derivs) > 1:
            fact_sets = [set(x for x in d["depends_on"] if x.startswith("fact_")) for d in derivs]
            shared = set.intersection(*fact_sets) if fact_sets else set()
            if shared:
                issues.append(Issue("LG013", "info", f"{cid} の複数の導出が同じ事実（{', '.join(sorted(shared))}）に依存しています。独立した根拠とは言えません。"))
        conf = best["confidence"]
        used = best["depends_on"]
        weakest = best["weakest"]
        results[cid] = {
            "text": claim_text.get(cid, ""),
            "confidence": round(conf, 3),
            "joint_probability": round(best["joint"], 3),
            "derivations": [{"theorem": d["theorem"], "confidence": round(d["confidence"], 3)} for d in derivs],
            "depends_on": used,
            "weakest_link": weakest,
            "weakest_confidence": round(confidences.get(weakest, 0.0), 3) if weakest else None,
            "hedge": hedge_for(conf),
        }
        if best["joint"] < 0.3 and conf >= 0.4:
            issues.append(Issue("LG014", "info", f"{cid} は不確かな前提が積み重なっています（すべてが同時に成り立つ確率の目安 {best['joint']:.2f}）。"
                                                  "本文では前提の数を減らすか、条件つきで述べることを検討してください。"))
        if not used:
            issues.append(Issue("LG010", "warn", f"{best['theorem']} がどの事実にも規則にも依存していません。論証になっているか確認してください。"))

    main_id = claim_ids[0]
    if main_id in results and results[main_id]["confidence"] < 0.4:
        issues.append(Issue("LG011", "warn",
                            f"主張の中心（{main_id}）の確からしさが {results[main_id]['confidence']} と低いです。"
                            "根拠を補強するか、主張を弱めることをユーザーと相談してください。"))
    for fid in facts:
        if fid not in used_facts and facts[fid].get("status") != "refuted":
            issues.append(Issue("LG012", "info", f"事実 {fid} はどの主張の論証にも使われていません。本文に載せる必要があるか検討してください。"))

    report = {
        "claims": results,
        "axioms": {k: round(v, 3) for k, v in confidences.items()},
        "lean_exit_code": code,
        "lean_output": out.strip()[-2000:],
    }
    if write_report:
        (doc_dir / "07-logic" / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return issues, report
