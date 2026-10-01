"""ステージ7（論理を検証する）の決定論の検査と、主張ごとの確信度の計算。

論証は、コンポーネントの宣言・関係公理・定理によるモデルとして `07-logic/Argument.lean` に書き、
すべての公理を具体的な定義に差し替えた証人を `07-logic/Model.lean` に書く。

この検査の役割は、形と存在を確かめる「門」と、確信度の計算だけ。中身の良し悪し（証拠が意味の上で公理を支えるか、
公理が結論の言い換えか、比べ方が公平か）は Lean Logic Reviewer が判断する。
中身を数で近似するもの（証明が公理の名前だけの定理など）は門にせず、手がかりとして `07-logic/hints.json` に出し、
Reviewer にだけ渡す（report.json と警告には出さない）。

Lean への問い合わせは次の3回にまとめる。
  1. Argument.lean をそのまま検査する（門のコンパイル）。末尾に、印の付いた定理の `#print axioms` を完全な名前で足す。
  2. 先頭に `import Lean` を足した写しで、メタプログラムを走らせる。公理の型が命題か、原子命題の数、
     定理の証明が公理の名前だけか、空の inductive、方式を取らない宣言を調べる。
  3. Model.lean（証人）に、元の公理の型との一致（`example : 元の型 := @名前`）と `#print axioms` を足して検査する。

確信度の方針（オーナーの原則11）:
  - 【自明】= 1。【実験】= 支える事実の status の値の最小値。
  - 【経験則】【仮定】は、`@support` がなければ 0.05。あれば `@confidence`（書き手の案）と支える事実の値の小さいほう。
  - どの種類でも、`@confidence`（Reviewer が書き換えたものを含む）があれば、それとの小さいほう。
  - 定理の値 = `#print axioms` に出る関係公理の値の最小値。主張の値 = その主張の `@claim` 定理の値の最小値。
    `@beyond`・`@baseline` の定理は、公理の使用には数えるが、主張の値には入れない。
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

from . import leansrc
from .issues import Issue

STATUS_CONFIDENCE = {
    "verified": 0.95,
    "partially_verified": 0.75,
    "user_asserted": 0.6,
    "unverified": 0.05,
    "refuted": 0.0,
}
NO_EVIDENCE = 0.05          # 証拠のない公理の確信度（0 は「確実に誤り」を表すので使わない）
REWORK_THRESHOLD = 0.4      # これ未満の公理は、ステージ6に戻して証拠を集める
STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EPS = 1e-9

HEDGES = [
    (0.85, "assert", "言い切る（〜です／〜である）"),
    (0.6, "moderate", "根拠を添えて控えめに言う（〜と考えられます／〜の傾向があります）"),
    (0.4, "tentative", "可能性として述べる（〜の可能性があります）"),
    (0.0, "hypothesis", "主張ではなく仮説・未確認事項として明示する"),
]

WITNESS_FORBIDDEN_ADDITIONS = ("instance", "attribute", "open", "set_option")
DRAFT_MARK_RE = re.compile(r"TODO|TBD|FIXME|XXX|書きかけ|から埋める|後で埋める|あとで埋める")


def find_lean() -> str | None:
    exe = shutil.which("lean")
    if exe:
        return exe
    cand = Path.home() / ".elan" / "bin" / "lean"
    return str(cand) if cand.exists() else None


def hedge_for(conf: float) -> dict:
    for threshold, key, text in HEDGES:
        if conf >= threshold - EPS:
            return {"level": key, "guidance": text}
    return {"level": "hypothesis", "guidance": HEDGES[-1][2]}


def fact_confidence(fact: dict) -> float:
    """事実1つの確信度（status から決まる）。"""
    return STATUS_CONFIDENCE.get(fact.get("status", "unverified"), NO_EVIDENCE)


# ---------------------------------------------------------------- Lean の実行


def _run_lean(text: str, cwd: Path, timeout: int = 600) -> tuple[int, str]:
    lean = find_lean()
    if not lean:
        return 127, "lean が見つかりません。elan で Lean 4 をインストールしてください（https://lean-lang.org/install/）。"
    with tempfile.TemporaryDirectory(prefix="cyrus-lean-") as td:
        f = Path(td) / "Probe.lean"
        f.write_text(text, encoding="utf-8")
        try:
            proc = subprocess.run([lean, str(f)], capture_output=True, text=True, timeout=timeout, cwd=str(cwd),
                                  env=os.environ.copy())
        except subprocess.TimeoutExpired:
            return 124, f"Lean の検査が {timeout} 秒でタイムアウトしました。"
        return proc.returncode, ((proc.stdout or "") + (proc.stderr or "")).replace(str(f), "Probe.lean")


ERROR_RE = re.compile(r"^Probe\.lean:(\d+):(\d+): error(?:\([^)]*\))?:?\s*(.*)$", re.M)
DEPENDS_RE = re.compile(r"'([^']+)' depends on axioms: \[(.*?)\]", re.S)
NODEPS_RE = re.compile(r"'([^']+)' does not depend on any axioms")


def _errors(out: str) -> list[tuple[int, str]]:
    return [(int(m.group(1)), m.group(3).strip()) for m in ERROR_RE.finditer(out)]


def _deps(out: str) -> dict[str, list[str]]:
    deps: dict[str, list[str]] = {}
    for m in DEPENDS_RE.finditer(out):
        deps[m.group(1)] = [x.strip() for x in m.group(2).replace("\n", " ").split(",") if x.strip()]
    for m in NODEPS_RE.finditer(out):
        deps[m.group(1)] = []
    return deps


def _insert_before_trailing_ends(text: str, probe: str) -> tuple[str, int]:
    """ファイル末尾の `end …`・`#print`・空行の並びの前に probe を差し込む（名前空間と open の中で検査するため）。

    戻り値は、差し込んだ文字列と、probe の最初の行の行番号（1始まり）。
    """
    lines = text.rstrip("\n").split("\n")
    k = len(lines)
    while k > 0 and (not lines[k - 1].strip() or lines[k - 1].startswith("#print")
                     or re.match(r"^end\b", lines[k - 1])):
        k -= 1
    head = lines[:k]
    return "\n".join(head + [""] + probe.split("\n") + [""] + lines[k:]) + "\n", len(head) + 2


META_PROGRAM = r'''
open Lean Meta in
partial def cyrusAtoms (e : Expr) : MetaM Nat := do
  match e with
  | .mdata _ b => cyrusAtoms b
  | .app (.app (.const ``And _) a) b => return (← cyrusAtoms a) + (← cyrusAtoms b)
  | .forallE n d b bi =>
    if (← isProp d) then return 1
    else withLocalDecl n bi d fun x => cyrusAtoms (b.instantiate1 x)
  | _ => return 1

open Lean Meta in
def cyrusMentions (e : Expr) (method : Name) (ctors : List Name) : Bool :=
  e.getUsedConstants.contains method || (ctors.filter (fun c => e.getUsedConstants.contains c)).length ≥ 2

open Lean Meta in
#eval show MetaM Unit from do
  let env ← getEnv
  let axioms : List String := [%(axioms)s]
  let theorems : List String := [%(theorems)s]
  let inductives : List String := [%(inductives)s]
  let method : Name := (%(method)s : String).toName
  let ctors : List Name := match env.find? method with
    | some (.inductInfo i) => i.ctors
    | _ => []
  let mut decls : List Name := []
  for s in axioms do
    let n := s.toName
    match env.find? n with
    | none => IO.println s!"CYRUS_MISSING\t{s}"
    | some ci =>
      let prop ← isProp ci.type
      let atoms ← if prop then cyrusAtoms ci.type else pure 0
      let usesM := ci.type.getUsedConstants.contains method
      if !prop then decls := n :: decls
      IO.println s!"CYRUS_AX\t{s}\t{if prop then 1 else 0}\t{atoms}\t{if usesM then 1 else 0}"
  for s in theorems do
    let n := s.toName
    match env.find? n with
    | some (.thmInfo t) =>
      let v := t.value.consumeMData.eta
      let head := match v with
        | .const c _ => c.toString
        | _ => "-"
      IO.println s!"CYRUS_THM\t{s}\t{head}"
    | _ => IO.println s!"CYRUS_MISSING\t{s}"
  for s in inductives do
    match env.find? s.toName with
    | some (.inductInfo i) => IO.println s!"CYRUS_IND\t{s}\t{i.ctors.length}"
    | _ => pure ()
  if !ctors.isEmpty then
    for s in axioms ++ theorems do
      match env.find? s.toName with
      | none => pure ()
      | some ci =>
        if (← isProp ci.type) && cyrusMentions ci.type method ctors then
          for c in ci.type.getUsedConstants do
            if decls.contains c then
              match env.find? c with
              | some dci =>
                if !(dci.type.getUsedConstants.contains method) then
                  IO.println s!"CYRUS_BOTH\t{c}\t{s}"
              | none => pure ()
'''


def _lean_str_list(names: list[str]) -> str:
    return ", ".join(json.dumps(n, ensure_ascii=False) for n in names)


# ---------------------------------------------------------------- 本体


def _load_json(path: Path) -> tuple[dict | None, str | None]:
    if not path.exists():
        return None, None
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, str(e)


def _banned(src: leansrc.Source, fname: str) -> list[Issue]:
    issues = []
    # 字下げした宣言は読まない（検査を素通りしないよう、公理と定理は字下げせずに書かせる）
    for m in re.finditer(r"^[ \t]+(?:(?:private|protected)\s+)?(axiom|theorem)\b", src.masked, re.M):
        line = src.masked.count("\n", 0, m.start()) + 1
        issues.append(Issue("LG012", "error", f"{fname} の {m.group(1)} が字下げされています。検査が読めないので、行頭から書いてください。", line))
    for pat, msg in ((r"\bsorry\b|\badmit\b", "sorry（admit）"), (r"\bnative_decide\b", "native_decide"),
                     (r"^import\s+Mathlib", "Mathlib の import")):
        m = re.search(pat, src.masked, re.M)
        if m:
            line = src.masked.count("\n", 0, m.start()) + 1
            issues.append(Issue("LG001", "error", f"{fname} に {msg} があります。使えません。", line))
    return issues


def _witness_command_counts(src: leansrc.Source) -> Counter:
    c: Counter = Counter()
    for ml in src.masked.split("\n"):
        s = ml.strip()
        s = re.sub(r"^(?:@\[[^\]]*\]\s*)+", "", s)
        s = re.sub(r"^(?:(?:private|protected|local|scoped|noncomputable)\s+)+", "", s)
        if re.match(r"deriving\s+instance\b", s):
            c["instance"] += 1
            continue
        m = re.match(r"(instance|attribute|open|set_option)\b", s)
        if m:
            c[m.group(1)] += 1
    return c


def _axiom_line_set(src: leansrc.Source) -> set[int]:
    """公理の宣言の行（0始まり）。証人ではここが定義に差し替わる。"""
    out: set[int] = set()
    for d in src.by_kw("axiom"):
        out.update(range(d.line - 1, d.end_line))
    return out


def check_witness(arg: leansrc.Source, arg_axioms: list[leansrc.Decl], model_path: Path,
                  names_to_print: list[str]) -> tuple[list[Issue], dict]:
    """証人（Model.lean）で、公理系が無矛盾であることを確かめる。"""
    issues: list[Issue] = []
    info: dict = {"exists": model_path.exists()}
    if not model_path.exists():
        return [Issue("LG020", "error", "証人 07-logic/Model.lean がありません。すべての axiom を同じ名前・同じ型の定義に差し替えた写しを置いてください。")], info
    text = model_path.read_text(encoding="utf-8")
    model = leansrc.parse(text)
    issues += _banned(model, "Model.lean")
    leftover = model.by_kw("axiom")
    for d in leftover:
        issues.append(Issue("LG021", "error", f"証人に axiom {d.name} が残っています。定義か定理に差し替えてください。", d.line))

    # 置き換えだけであること: 元の axiom 以外のコードの行が、同じ順で残っている。
    # コメントと docstring は比べない（Reviewer が Argument.lean の @confidence を書き換えても、証人を直さずに済むように）。
    ax_lines = _axiom_line_set(arg)
    arg_lines = [ln.rstrip() for ln in arg.masked.split("\n")]
    kept = [arg_lines[k] for k in range(arg.namespace_lines, len(arg_lines)) if k not in ax_lines]
    model_lines = [ln.rstrip() for ln in model.masked.split("\n")][model.namespace_lines:]
    it = iter(model_lines)
    missing = [ln for ln in kept if ln.strip() and not any(ln == x for x in it)]
    if missing:
        issues.append(Issue("LG022", "error", f"証人で、元の axiom 以外の行のうち {len(missing)} 行が同じ順で残っていません。"
                                              "証人は axiom を定義に差し替えただけの写しにしてください。", None, missing[0][:60]))
    info["missing_lines"] = len(missing)

    # 足してはいけない命令
    ca, cm = _witness_command_counts(arg), _witness_command_counts(model)
    for kw in WITNESS_FORBIDDEN_ADDITIONS:
        if cm[kw] > ca[kw]:
            issues.append(Issue("LG023", "error", f"証人に {kw} が {cm[kw] - ca[kw]} 個足されています。証人で足してはいけません"
                                                  "（公理系の外で性質を持ち込めるため）。"))

    # 型の一致と、依存する公理
    probe_lines = []
    for d in arg_axioms:
        probe_lines.append(f"example : {leansrc.type_text(d)} := @_root_.{d.full}")
    probe_lines += [f"#print axioms _root_.{n}" for n in names_to_print]
    full, first = _insert_before_trailing_ends(text, "\n".join(probe_lines))
    code, out = _run_lean(full, model_path.parent)
    n_ex = len(arg_axioms)
    compile_errors = []
    for ln, msg in _errors(out):
        if first <= ln < first + n_ex:
            d = arg_axioms[ln - first]
            issues.append(Issue("LG024", "error", f"証人の {d.name} の型が、Argument.lean の公理の型と一致しないか、定義がありません: {msg[:160]}",
                                d.line))
        elif ln < first:
            compile_errors.append((ln, msg))
    if compile_errors:
        ln, msg = compile_errors[0]
        issues.append(Issue("LG025", "error", f"証人がコンパイルできません（{len(compile_errors)} 件）: {msg[:160]}", ln))
    if code == 127 or code == 124:
        issues.append(Issue("LG025", "error", out.strip()[:200]))
    nonstd = {}
    for name, ds in _deps(out).items():
        bad = sorted(set(ds) - STD_AXIOMS)
        if bad:
            nonstd[name] = bad
    for name, bad in list(nonstd.items())[:10]:
        issues.append(Issue("LG026", "error", f"証人の {name} が、Lean 標準の公理以外（{', '.join(bad)}）に依存しています。"))
    info.update({"compiled": not compile_errors, "nonstd": nonstd, "type_checked": n_ex})
    return issues, info


def check(doc_dir: Path, write_report: bool = True) -> tuple[list[Issue], dict]:
    logic = doc_dir / "07-logic"
    arg_path, model_path = logic / "Argument.lean", logic / "Model.lean"
    if not arg_path.exists():
        return [Issue("LG000", "error", "07-logic/Argument.lean がありません。")], {}
    issues: list[Issue] = []

    claims_doc, err = _load_json(doc_dir / "05-claims.json")
    if claims_doc is None:
        return [Issue("LG000", "error", f"05-claims.json を読めません: {err or 'ありません'}")], {}
    facts_doc, err = _load_json(doc_dir / "06-facts.json")
    if facts_doc is None:
        return [Issue("LG000", "error", f"06-facts.json を読めません: {err or 'ありません'}")], {}
    facts = {f.get("id"): f for f in facts_doc.get("facts") or [] if f.get("id")}
    main = claims_doc.get("main_claim") or {}
    claim_list = [dict(main, id=main.get("id", "C0"))] + list(claims_doc.get("claims") or [])
    claim_ids = [c["id"] for c in claim_list if c.get("id")]
    claim_text = {c["id"]: c.get("text", "") for c in claim_list if c.get("id")}
    rejected_doc, rej_err = _load_json(logic / "rejected.json")
    if rej_err:
        issues.append(Issue("LG030", "error", f"07-logic/rejected.json を読めません: {rej_err}"))
    ledger_doc, led_err = _load_json(logic / "ledger.json")
    if led_err or (ledger_doc is not None and not (isinstance(ledger_doc, dict) and isinstance(ledger_doc.get("rows"), list)
                                                     and isinstance(ledger_doc.get("methods"), list))):
        issues.append(Issue("LG031", "warn", "07-logic/ledger.json（失敗の台帳）を読めません。"
                                             "{\"methods\": [...], \"rows\": [...]} の形にしてください。" + (f" {led_err}" if led_err else "")))

    text = arg_path.read_text(encoding="utf-8")
    src = leansrc.parse(text)
    n_lines = text.count("\n") + 1
    issues += _banned(src, "Argument.lean")

    axioms = src.by_kw("axiom")
    theorems = src.by_kw("theorem", "lemma")
    tmarks = {t.full: leansrc.theorem_marks(t.doc) for t in theorems}
    tagged = [t for t in theorems if tmarks[t.full].claims or tmarks[t.full].beyond or tmarks[t.full].baseline]

    # ---- 1回目: そのままコンパイルし、印の付いた定理の依存公理を完全な名前で問い合わせる
    probe = "\n".join(f"#print axioms _root_.{t.full}" for t in theorems)
    code, out = _run_lean(text.rstrip("\n") + "\n\n" + probe + "\n", arg_path.parent)
    compile_errors = [(ln, msg) for ln, msg in _errors(out) if ln <= n_lines]
    for ln, msg in compile_errors[:20]:
        issues.append(Issue("LG002", "error", f"Lean のエラー: {msg[:200]}", ln))
    if len(compile_errors) > 20:
        issues.append(Issue("LG002", "error", f"Lean のエラーがほかに {len(compile_errors) - 20} 件あります。"))
    if code in (124, 127):
        issues.append(Issue("LG002", "error", out.strip()[:300]))
    deps = _deps(out)

    # ---- 2回目: メタプログラムで型を調べる
    method = next((d.full for d in src.by_kw("inductive") if d.short == "Method"), "")
    meta = META_PROGRAM % {
        "axioms": _lean_str_list([a.full for a in axioms]),
        "theorems": _lean_str_list([t.full for t in theorems]),
        "inductives": _lean_str_list([d.full for d in src.by_kw("inductive")]),
        "method": json.dumps(method),
    }
    _, mout = _run_lean("import Lean\n" + text.rstrip("\n") + "\n\n" + meta + "\n", arg_path.parent)
    ax_info: dict[str, dict] = {}
    thm_head: dict[str, str] = {}
    both: dict[str, list[str]] = {}
    for line in mout.splitlines():
        parts = line.split("\t")
        if parts[0] == "CYRUS_AX" and len(parts) == 5:
            ax_info[parts[1]] = {"prop": parts[2] == "1", "atoms": int(parts[3]), "uses_method": parts[4] == "1"}
        elif parts[0] == "CYRUS_THM" and len(parts) == 3:
            thm_head[parts[1]] = parts[2]
        elif parts[0] == "CYRUS_IND" and len(parts) == 3 and parts[2] == "0":
            d = next((x for x in src.by_kw("inductive") if x.full == parts[1]), None)
            issues.append(Issue("LG010", "error", f"inductive {parts[1].rsplit('.', 1)[-1]} にコンストラクタがありません（空の型）。"
                                                  "中身を決めない型は `axiom T : Type` で宣言してください。", d.line if d else None))
        elif parts[0] == "CYRUS_BOTH" and len(parts) == 3:
            both.setdefault(parts[1], []).append(parts[2])
    if axioms and not ax_info and not compile_errors:
        issues.append(Issue("LG002", "error", f"Lean に公理の型を問い合わせられませんでした: {mout.strip()[-300:]}"))

    relational = [a for a in axioms if ax_info.get(a.full, {}).get("prop")]
    declarations = [a for a in axioms if a.full in ax_info and not ax_info[a.full]["prop"]]
    rel_by_full = {a.full: a for a in relational}
    rel_by_short = {a.name: a.full for a in relational}

    # ---- 関係公理の形と確信度
    ax_report: dict[str, dict] = {}
    conf: dict[str, float] = {}
    for a in relational:
        mk = leansrc.axiom_marks(a.doc)
        where = a.name
        atoms = ax_info[a.full]["atoms"]
        if not mk.kind:
            issues.append(Issue("LG003", "error", f"関係公理 {where} に種類（【自明】【実験】【経験則】【仮定】）がありません。", a.line))
        unknown = [f for f in mk.support + mk.against if f not in facts]
        if unknown:
            issues.append(Issue("LG004", "error", f"{where} の @support / @against の事実 {', '.join(unknown)} が 06-facts.json にありません。", a.line))
        if mk.kind == "仮定" and not mk.needs_fact:
            issues.append(Issue("LG005", "error", f"【仮定】{where} に「要ファクト:」がありません（これから集める事実を書きます）。", a.line))
        if mk.kind in ("経験則", "仮定") and not mk.confidence:
            issues.append(Issue("LG006", "error", f"【{mk.kind}】{where} に @confidence（書き手の案）がありません。", a.line))
        if mk.kind == "実験" and not mk.support:
            issues.append(Issue("LG006", "error", f"【実験】{where} に @support がありません。", a.line))
        if atoms > 1:
            issues.append(Issue("LG007", "error", f"関係公理 {where} は、原子命題 {atoms} 個を ∧ で1つにまとめています。"
                                                  "型の最上位と ∀ の直下に ∧ を置かず、原子ごとに公理を分けてください。", a.line))
        if len(mk.confidence) > 1:
            issues.append(Issue("LG008", "error", f"{where} に @confidence が {len(mk.confidence)} 個あります。1つにしてください。", a.line))
        if mk.reviewer:
            bad = [r.raw for r in mk.reviewer if r.value is None or r.original is None]
            for raw in bad:
                issues.append(Issue("LG008", "error", f"{where} の @reviewer の行を読めません（`@reviewer <値> ← <元の案> 理由: …`）。", a.line, raw[:60]))
            ok = [r for r in mk.reviewer if r.value is not None and r.original is not None]
            for prev, r in zip(ok, ok[1:]):
                if abs(r.original - prev.value) > EPS:
                    issues.append(Issue("LG008", "error", f"{where} の @reviewer の元の案 {r.original:g} が、前の @reviewer の値 {prev.value:g} と一致しません。", a.line))
            for r in ok:
                if r.value > r.original + EPS:
                    issues.append(Issue("LG008", "error", f"{where} の @reviewer の値 {r.value:g} が元の案 {r.original:g} より高くなっています。"
                                                          "Reviewer は確信度を下げるだけです。", a.line))
            if ok and (not mk.confidence or abs(mk.confidence[-1] - ok[-1].value) > EPS):
                issues.append(Issue("LG008", "error", f"{where} の @confidence が、最後の @reviewer の値 {ok[-1].value:g} と一致しません。", a.line))

        sup_vals = [fact_confidence(facts[f]) for f in mk.support if f in facts]
        if mk.kind == "自明":
            base = 1.0
        elif mk.kind == "実験":
            base = min(sup_vals) if sup_vals else NO_EVIDENCE
        elif mk.kind in ("経験則", "仮定"):
            if not sup_vals:
                base = NO_EVIDENCE
            else:
                base = min(sup_vals + ([mk.confidence[-1]] if mk.confidence else [NO_EVIDENCE]))
        else:
            base = NO_EVIDENCE
        value = min(base, mk.confidence[-1]) if mk.confidence else base
        conf[a.full] = value
        ax_report[a.name] = {
            "full_name": a.full, "line": a.line, "kind": mk.kind, "support": mk.support, "against": mk.against,
            "proposal": mk.confidence[-1] if mk.confidence else None,
            "reviewer": [{"value": r.value, "original": r.original, "reason": r.reason} for r in mk.reviewer],
            "confidence": round(value, 3), "atoms": atoms,
        }

    # ---- 棄却した公理の再出現
    if rejected_doc:
        rejected = {r.get("axiom") for r in rejected_doc.get("rejected") or [] if isinstance(r, dict)}
        for a in axioms:
            if a.name in rejected or a.short in rejected:
                issues.append(Issue("LG009", "error", f"棄却した公理 {a.name} が、また現れています（07-logic/rejected.json）。", a.line))

    # ---- 主張と定理
    known_claims = set(claim_ids)
    for t in tagged:
        for cid in tmarks[t.full].claims + [c for c in tmarks[t.full].beyond if c != "*"]:
            if cid not in known_claims:
                issues.append(Issue("LG011", "error", f"定理 {t.name} の印が、05-claims.json にない主張 {cid} を指しています。", t.line))
    for cid in claim_ids:
        if not any(cid in tmarks[t.full].claims for t in theorems):
            issues.append(Issue("LG011", "error", f"主張 {cid} に `@claim {cid}` の付いた定理がありません。"))

    thm_report: dict[str, dict] = {}
    used_by_claims: set[str] = set()
    used_by_side: set[str] = set()
    for t in tagged:
        mk = tmarks[t.full]
        ds = deps.get(t.full)
        if ds is None:
            thm_report[t.name] = {"full_name": t.full, "line": t.line, "claims": mk.claims, "beyond": mk.beyond,
                                  "baseline": mk.baseline, "confidence": None, "depends_on": []}
            continue
        if "sorryAx" in ds:
            issues.append(Issue("LG001", "error", f"定理 {t.name} が sorry に依存しています。", t.line))
        rel = [d for d in ds if d in rel_by_full]
        value = 0.0 if "sorryAx" in ds else min((conf[d] for d in rel), default=1.0)
        weakest = sorted(rel, key=lambda d: conf[d])[:3]
        (used_by_claims if mk.claims else used_by_side).update(rel)
        thm_report[t.name] = {
            "full_name": t.full, "line": t.line, "claims": mk.claims, "beyond": mk.beyond, "baseline": mk.baseline,
            "confidence": round(value, 3),
            "depends_on": [rel_by_full[d].name for d in rel],
            "weakest": [{"axiom": rel_by_full[d].name, "confidence": round(conf[d], 3)} for d in weakest],
        }

    # 印のない定理（不利な結論・補題）も、値と依存する公理を出す（主張の値と公理の使用には数えない）
    other_report: dict[str, dict] = {}
    for t in theorems:
        if t in tagged or t.full not in deps:
            continue
        ds = deps[t.full]
        rel = [d for d in ds if d in rel_by_full]
        other_report[t.name] = {
            "full_name": t.full, "line": t.line, "unfavorable": t.doc.lstrip().startswith("[不利]"),
            "confidence": round(0.0 if "sorryAx" in ds else min((conf[d] for d in rel), default=1.0), 3),
            "depends_on": [rel_by_full[d].name for d in rel],
        }

    claims_report: dict[str, dict] = {}
    for cid in claim_ids:
        ts = [n for n, r in thm_report.items() if cid in r["claims"] and r["confidence"] is not None]
        if not ts:
            continue
        value = min(thm_report[n]["confidence"] for n in ts)
        used = sorted({d for n in ts for d in deps.get(thm_report[n]["full_name"], []) if d in rel_by_full})
        nontriv = [d for d in used if ax_report[rel_by_full[d].name]["kind"] != "自明"]
        decisive = [d for d in nontriv if abs(conf[d] - value) <= EPS]
        weakest = min(used, key=lambda d: conf[d]) if used else None
        claims_report[cid] = {
            "text": claim_text.get(cid, ""),
            "confidence": round(value, 3),
            "theorems": ts,
            "weakest_link": rel_by_full[weakest].name if weakest else None,
            "weakest_confidence": round(conf[weakest], 3) if weakest else None,
            "weakest_links": sorted(rel_by_full[d].name for d in used if weakest and abs(conf[d] - conf[weakest]) <= EPS),
            "decisive_atoms": sum(ax_info[d]["atoms"] for d in decisive),
            "path_atoms": sum(ax_info[d]["atoms"] for d in nontriv if d not in decisive),
            "decisive_axioms": [rel_by_full[d].name for d in decisive],
            "hedge": hedge_for(value),
        }

    # ---- 確信度を左右する弱い前提（ステージの終わりに、日常語でユーザーに見せる。5つまで）
    deciding: dict[str, list[str]] = {}
    for cid, c in claims_report.items():
        if c["confidence"] >= HEDGES[0][0] - EPS:
            continue
        for name in c["weakest_links"]:
            if ax_report[name]["kind"] != "自明":
                deciding.setdefault(name, []).append(cid)
    kind_rank = {"仮定": 0, "経験則": 1, "実験": 2}
    main_id = claim_ids[0] if claim_ids else "C0"
    # 主張の中心（C0）の値を決めるものを先に、次に効く主張の数、確信度の低さの順
    ranked = sorted(deciding, key=lambda n: (main_id not in deciding[n], -len(deciding[n]), ax_report[n]["confidence"],
                                             kind_rank.get(ax_report[n]["kind"], 3), n))
    weak_premises = []
    for name in ranked[:5]:
        a = next(x for x in relational if x.name == name)
        first = next((ln.strip() for ln in a.doc.split("\n") if ln.strip()), "")
        statement = re.sub(r"^【[^】]*】\s*", "", first)
        need = re.search(r"要ファクト\s*[:：]\s*([^\n]*)", a.doc)
        weak_premises.append({"axiom": name, "kind": ax_report[name]["kind"], "confidence": ax_report[name]["confidence"],
                              "claims": deciding[name], "statement": statement,
                              "needs_fact": need.group(1).strip() if need else ""})

    # ---- 原子命題の数（数えて報告するだけ）
    def atoms_of(names) -> int:
        return sum(ax_info[n]["atoms"] for n in names)
    rel_names = [a.full for a in relational]
    nontrivial = [n for n in rel_names if ax_report[rel_by_full[n].name]["kind"] != "自明"]
    atoms = {
        "total": atoms_of(rel_names),
        "non_trivial": atoms_of(nontrivial),
        "by_kind": {k: atoms_of([n for n in rel_names if ax_report[rel_by_full[n].name]["kind"] == k]) for k in leansrc.KINDS},
        "used_by_claims": atoms_of(used_by_claims),
        "side_only": atoms_of(used_by_side - used_by_claims),
        "unused": atoms_of(set(rel_names) - used_by_claims - used_by_side),
    }

    # ---- 手戻りの一覧（ステージ6へ戻して証拠を集める公理）
    rework = []
    for a in relational:
        r = ax_report[a.name]
        reasons = []
        if r["confidence"] < REWORK_THRESHOLD - EPS:
            reasons.append("low_confidence")
        if r["against"]:
            reasons.append("against")
        if not reasons:
            continue
        users = sorted({cid for n, t in thm_report.items() if a.name in t["depends_on"] for cid in t["claims"]})
        side = sorted(n for n, t in thm_report.items() if a.name in t["depends_on"] and not t["claims"])
        others = sorted(n for n, t in other_report.items() if a.name in t["depends_on"])
        rework.append({"axiom": a.name, "line": a.line, "kind": r["kind"], "confidence": r["confidence"],
                       "reasons": reasons, "support": r["support"], "against": r["against"],
                       "claims": users, "side_theorems": side, "other_theorems": others})

    # ---- 証人
    w_issues, witness = check_witness(src, [a for a in axioms if a.full in ax_info] or axioms, model_path,
                                      [a.full for a in axioms] + [t.full for t in tagged])
    issues += w_issues

    # ---- 手がかり（Reviewer にだけ渡す。report.json と警告には出さない）
    used_by_others = {rel_by_full_name for t in other_report.values() for rel_by_full_name in
                      (rel_by_short[n] for n in t["depends_on"] if n in rel_by_short)}
    unfavorable = {t.full for t in theorems if t.doc.lstrip().startswith("[不利]")}
    used_by_non_unfavorable = {rel_by_short[n] for name, t in other_report.items() if t["full_name"] not in unfavorable
                               for n in t["depends_on"] if n in rel_by_short}
    hints = build_hints(src, axioms, relational, theorems, tmarks, thm_head, thm_report, ax_report, ax_info,
                        used_by_claims | used_by_side, both, facts, logic, used_by_others, used_by_non_unfavorable)

    report = {
        "claims": claims_report,
        "theorems": thm_report,
        "other_theorems": other_report,
        "axioms": ax_report,
        "counts": {"axioms": len(axioms), "declarations": len(declarations), "relational": len(relational),
                   "by_kind": dict(Counter(ax_report[a.name]["kind"] or "（なし）" for a in relational)),
                   "claim_theorems": sum(1 for t in thm_report.values() if t["claims"]),
                   "side_theorems": sum(1 for t in thm_report.values() if not t["claims"])},
        "atoms": atoms,
        "rework": rework,
        "weak_premises": weak_premises,
        "witness": witness,
        "gate_errors": sum(1 for i in issues if i.severity == "error"),
        "lean_exit_code": code,
    }
    if write_report:
        logic.mkdir(parents=True, exist_ok=True)
        (logic / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (logic / "hints.json").write_text(json.dumps({"hints": hints}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return issues, report


# ---------------------------------------------------------------- 手がかり


def _design_tables(text: str) -> list[list[str]]:
    rows = []
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("|") and s.endswith("|") and not re.match(r"^\|[\s:|-]+\|$", s):
            rows.append([c.strip() for c in s.strip("|").split("|")])
    return rows


def build_hints(src, axioms, relational, theorems, tmarks, thm_head, thm_report, ax_report, ax_info,
                used, both, facts, logic: Path, used_by_others: set | None = None,
                used_by_non_unfavorable: set | None = None) -> list[dict]:
    hints: list[dict] = []
    ax_short = {a.full: a.name for a in axioms}
    rel_full = {a.full for a in relational}

    # 証明が公理の名前だけの定理（公理の言い換えの候補）
    for t in theorems:
        head = thm_head.get(t.full, "-")
        if head in ax_short:
            ack = ax_short[head] in tmarks[t.full].restates or head in tmarks[t.full].restates
            hints.append({"kind": "proof_is_axiom", "target": t.name, "line": t.line,
                          "detail": {"axiom": ax_short[head], "restates_acknowledged": ack}})

    # 依存する非自明の原子が1つだけの主張の定理
    for name, r in thm_report.items():
        if not r["claims"] or r["confidence"] is None:
            continue
        nontriv = [d for d in r["depends_on"] if ax_report[d]["kind"] != "自明"]
        n_atoms = sum(ax_report[d]["atoms"] for d in nontriv)
        if n_atoms == 1:
            full = r["full_name"]
            ack = nontriv[0] in tmarks.get(full, leansrc.TheoremMarks([], [], False, [])).restates
            hints.append({"kind": "single_atom_claim", "target": name, "line": r["line"],
                          "detail": {"axiom": nontriv[0], "claims": r["claims"], "restates_acknowledged": ack}})

    # どの主張の定理にも使われない公理（印のない定理だけが使うものと、どこでも使われないものを分ける）
    for a in relational:
        if a.full not in used:
            if a.full not in (used_by_others or set()):
                kind = "unused_axiom"
            elif a.full in (used_by_non_unfavorable or set()):
                kind = "used_only_by_unmarked_theorems"
            else:
                kind = "used_only_by_unfavorable_theorems"  # [不利] の定理だけが使う（設計どおりのことが多い）
            hints.append({"kind": kind, "target": a.name, "line": a.line, "detail": {"kind": ax_report[a.name]["kind"]}})

    # 両方式の式に現れるのに、方式を引数に取らない宣言
    for decl, where in both.items():
        hints.append({"kind": "method_free_decl", "target": ax_short.get(decl, decl),
                      "line": next((a.line for a in axioms if a.full == decl), None),
                      "detail": {"appears_in": sorted({ax_short.get(w, w.rsplit('.', 1)[-1]) for w in where})[:8]}})

    # 「弱い点」に出る事実のうち、@support にないもの
    for a in relational:
        mk = leansrc.axiom_marks(a.doc)
        extra = [f for f in mk.weak_point_facts if f not in mk.support and f not in mk.against]
        if extra:
            hints.append({"kind": "weak_point_fact_not_supported", "target": a.name, "line": a.line, "detail": {"facts": extra}})

    # 分けた事実の親番号の残り（F35a があるのに F35 を使っている）
    split_parents = {re.match(r"(F\d+)", f).group(1) for f in facts if re.match(r"F\d+[a-z]$", f)}
    for a in relational:
        mk = leansrc.axiom_marks(a.doc)
        parents = sorted(set(f for f in mk.support + mk.against + mk.weak_point_facts if f in split_parents),
                         key=leansrc.fact_sort_key)
        if parents:
            hints.append({"kind": "split_fact_parent", "target": a.name, "line": a.line, "detail": {"facts": parents}})

    # 失敗の台帳（ledger.json）で、片方の方式の欄が空いている量
    ledger, _ = _load_json(logic / "ledger.json")
    if isinstance(ledger, dict) and isinstance(ledger.get("rows"), list) and isinstance(ledger.get("methods"), list):
        methods = ledger["methods"]
        for i, row in enumerate(ledger["rows"]):
            if not isinstance(row, dict):
                continue
            cells = row.get("cells") or {}
            empty = [m for m in methods
                     if not isinstance(cells.get(m), dict)
                     or not (str(cells[m].get("what") or "").strip() or cells[m].get("axioms"))]
            if empty:
                hints.append({"kind": "ledger_empty_side", "target": row.get("quantity") or f"rows[{i}]", "line": None,
                              "detail": {"layer": row.get("layer"), "empty_methods": empty}})

    # 書きかけの印（論証と設計書）
    texts = [("Argument.lean", src.text)] + [(n, (logic / n).read_text(encoding="utf-8"))
                                             for n in ("model-plan.md", "model-plan-delta.md", "Model.lean") if (logic / n).exists()]
    for fname, text in texts:
        for i, line in enumerate(text.split("\n"), 1):
            m = DRAFT_MARK_RE.search(line)
            if m:
                hints.append({"kind": "draft_mark", "target": fname, "line": i, "detail": {"text": line.strip()[:80]}})

    # 設計書（model-plan.md）と Argument.lean の冒頭の表の値と、計算した値の食い違い
    thm_names = set(thm_report)
    for fname, text in (("Argument.lean", src.text), ("model-plan.md", (logic / "model-plan.md").read_text(encoding="utf-8")
                                                      if (logic / "model-plan.md").exists() else "")):
        for row in _design_tables(text):
            names = [n for n in re.findall(r"`([A-Za-z_][A-Za-z0-9_'.]*)`", " ".join(row)) if n in thm_names]
            nums = re.findall(r"(?<![\w.])(0(?:\.\d+)?|1(?:\.0+)?)(?![\w.])", row[-1]) if row else []
            if not names or not nums or (len(nums) != len(names) and len(nums) != 1):
                continue
            if len(nums) == len(names):
                groups = [([n], v) for n, v in zip(names, nums)]
            else:  # 値が1つで定理が複数なら、その最小値と比べる
                groups = [(names, nums[0])]
            for ns, v in groups:
                vals = [thm_report[n]["confidence"] for n in ns if thm_report[n]["confidence"] is not None]
                if vals and abs(float(v) - min(vals)) > 1e-6:
                    hints.append({"kind": "design_value_mismatch", "target": ns[0], "line": thm_report[ns[0]]["line"],
                                  "detail": {"file": fname, "theorems": ns, "design": float(v), "computed": min(vals)}})
    return hints
