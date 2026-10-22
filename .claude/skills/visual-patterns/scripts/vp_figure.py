#!/usr/bin/env python3
"""visual-patterns の決定論的な部分: 図表の仕様の検査、候補の一覧、描画。

スキル本文（SKILL.md）が決める「問い・答え・根拠の形・趣旨・パターン」を figure spec（JSON）に書き、
このスクリプトで、カタログ（taxonomy.md の手順2・5・6）の規則に合っているかを機械的に確かめる。
描くのは Mermaid（本文に埋める）か Vega-Lite（ヘッドレス Chrome で PNG にする）。

標準ライブラリだけで動く。cyrus の CLI はこのファイルを import して同じ検査を完了条件に使う。

使い方:
    vp_figure.py candidates <趣旨の ID>        候補のパターンと切替条件、制約、描き方を一覧する
    vp_figure.py intents                       趣旨の一覧（カテゴリ・問い）
    vp_figure.py show <パターンの ID>           パターン文書を表示する
    vp_figure.py check <spec.json> [--reader-level novice|intermediate|expert] [--json]
    vp_figure.py render <入力> --out <PNG> [--width 760] [--scale 2]
        入力は Vega-Lite の JSON（.json / .vl.json）か Mermaid のテキスト（.mmd / .mermaid）
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
CATALOG_DIR = SKILL_DIR / "references" / "catalog"

FORMS = ("quantity", "items-attributes", "parts-relations", "conditions", "appearance")
FORM_JA = {"quantity": "量", "items-attributes": "項目×属性", "parts-relations": "段階・主体・部分とその関係",
           "conditions": "条件と結果", "appearance": "外観"}
# 手順2 の表: 根拠の形ごとに選べる趣旨（表の「趣旨のカテゴリ」列を、3.1 の趣旨 ID に展開したもの）
FORM_INTENTS = {
    "quantity": {"magnitude-comparison", "deviation", "ranking", "time-series-change", "part-to-whole",
                 "distribution", "geographic", "correlation", "flow"},
    "items-attributes": {"attribute-comparison", "positioning", "lookup"},
    "parts-relations": {"step-order", "branching", "schedule", "cycle", "flow", "parent-child", "membership",
                        "layering", "argumentation", "relationship", "causation", "dependency", "opposing-forces",
                        "chronology"},
    "conditions": {"conditional-outcome"},
    "appearance": {"appearance"},
}
STRUCTURE_FEATURES = {"branching", "merging", "cycle", "many-to-many", "nesting"}
HANDOFF_FEATURES = {"loss-per-handoff", "change-per-handoff"}
FEATURES = STRUCTURE_FEATURES | HANDOFF_FEATURES | {"relative-timing"}
COUNT_KEYS = ("values", "groups", "periods", "series", "items", "categories", "actors", "steps", "conditions",
              "levels", "nodes", "edges", "regions", "cells", "points")
PRECISIONS = ("overview", "exact")
READINGS = ("through", "lookup")
# 手順2 の目安に満たなくても図表にする判断（根拠を文章で書き出して確かめる）
BELOW_THRESHOLD_REASONS = {"repeated-pattern": "同じ文型の文が 3 つ以上並ぶ", "cross-reference": "読み手が前の文に戻って照合し直す"}
RENDERS = ("mermaid", "vega-lite", "markdown-table", "image")
FAMILY_FOR_KIND = {"table": {"table"}, "figure": {"chart", "diagram", "picture"}}
JOINERS = ("および", "ならびに", "とともに", "し、")
ANSWER_WARN, ANSWER_ERROR = 80, 120

# 描画に使うライブラリ（読み込むのはライブラリ本体だけで、図のデータは送らない）。
# オフラインでは VP_MERMAID_JS / VP_VEGA_JS（空白区切り）でローカルのファイルを指定する。cyrus の CYRUS_MERMAID_JS も使う（空なら CDN）。
MERMAID_SRC = (os.environ.get("VP_MERMAID_JS") or os.environ.get("CYRUS_MERMAID_JS")
               or "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js")
VEGA_SRCS = (os.environ.get("VP_VEGA_JS") or "https://cdn.jsdelivr.net/npm/vega@5 https://cdn.jsdelivr.net/npm/vega-lite@5 "
                                             "https://cdn.jsdelivr.net/npm/vega-embed@6").split()


@dataclass
class Issue:
    rule: str
    severity: str  # error / warn / info
    message: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------- カタログ


def load_index(path: Path | None = None) -> dict:
    p = path or DATA_DIR / "index.json"
    return json.loads(p.read_text(encoding="utf-8"))


def load_routes(path: Path | None = None) -> dict:
    p = path or DATA_DIR / "render-routes.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def allowed_renders(routes: dict, pattern: str) -> list[str]:
    r = routes.get(pattern) or {}
    out = [r.get("route")] + list(r.get("alt") or [])
    return [x for x in out if x and x != "none"]


def parse_range(s: str) -> tuple[float | None, float | None]:
    """scale の値（「2〜30」「〜30」「3〜」「1」「30 以上」「900 程度まで」「10〜数千」、括弧の注記付き）を下限と上限にする。

    「1行あたり 2〜5」「各層 1〜6」のような単位あたりの値は、図全体の数とは比べられないので (None, None)。
    """
    raw = str(s)
    t = re.sub(r"[（(].*?[）)]", "", raw).strip()
    m = re.match(r"^(\d+)$", t)
    if m:
        if "標準" in raw:  # 「100（10×10 が標準）」は目安であって上限・下限ではない
            return (None, None)
        n = float(m.group(1))
        return (n, n)
    m = re.match(r"^(\d+)\s*以上$", t)
    if m:
        return (float(m.group(1)), None)
    m = re.match(r"^(\d+)\s*程度まで$", t)
    if m:
        return (None, float(m.group(1)))
    m = re.match(r"^(\d+)?\s*[〜~\-–]\s*(\d+)?\s*(数[十百千万]+)?$", t)
    if not m or not (m.group(1) or m.group(2)):
        return (None, None)
    lo = float(m.group(1)) if m.group(1) else None
    hi = float(m.group(2)) if m.group(2) else None
    return (lo, hi)


_OPENERS, _CLOSERS = "「『（(【［[", "」』）)】］]"


def split_sentences(text: str) -> list[str]:
    """文に分ける。括弧・かぎ括弧の中の 。！？ では分けない（「〜ですか？」と確認する画面、など）。"""
    out: list[str] = []
    buf: list[str] = []
    depth = 0
    for ch in text.strip():
        buf.append(ch)
        if ch in _OPENERS:
            depth += 1
        elif ch in _CLOSERS and depth:
            depth -= 1
        elif ch in "。！？" and depth == 0:
            out.append("".join(buf).strip())
            buf = []
    tail = "".join(buf).strip()
    if tail:
        out.append(tail)
    return out


def _is(v, coll) -> bool:
    """列挙に含まれる文字列か（リストなどが来ても例外にしない）。"""
    return isinstance(v, str) and v in coll


def visible_length(text: str) -> int:
    return len(re.sub(r"\s", "", text))


# ---------------------------------------------------------------- 手順2: 根拠の形で表現を決める


def figure_warranted(evidence: dict) -> tuple[bool, str]:
    """手順2 の表に当たるか。(当たる, 理由)。"""
    if not isinstance(evidence, dict):
        return False, "根拠 evidence は {form, description, counts, features} のオブジェクトにする"
    form = evidence.get("form")
    counts = evidence.get("counts") if isinstance(evidence.get("counts"), dict) else {}
    c = {k: v for k, v in counts.items() if isinstance(v, int) and not isinstance(v, bool)}  # 整数だけ（Infinity や NaN を通さない）
    raw_feats = evidence.get("features")
    feats = {f for f in raw_feats if isinstance(f, str)} if isinstance(raw_feats, list) else set()
    if not isinstance(form, str):
        return False, f"根拠の形 form は {', '.join(FORMS)} のいずれかにする"
    if form == "quantity":
        if c.get("values", 0) >= 5:
            return True, f"答えが述べる値が {c['values']} 個（5 以上）"
        if c.get("groups", 0) >= 2 and c.get("periods", 0) >= 2 and evidence.get("difference_matters"):
            return True, f"{c['groups']} 区分 × {c['periods']} 時点・条件の増減・差で、差の大きさが精度に含まれる"
        return False, "値が 4 つ以下の比較・増減（2 区分 × 2 時点以上で差の大きさが要る場合を除く）は文章にする"
    if form == "items-attributes":
        if (c.get("items", 0) >= 2 and c.get("categories", 0) >= 3) or (c.get("items", 0) >= 5 and c.get("categories", 0) >= 2):
            return True, f"対象 {c.get('items', 0)} × 観点 {c.get('categories', 0)}"
        return False, "対象 2 以上 × 観点 3 以上、または対象 5 以上 × 観点 2 以上に満たないので文章にする"
    if form == "parts-relations":
        if feats & STRUCTURE_FEATURES:
            return True, "分岐・合流・循環・多対多・入れ子を含む（数によらない）"
        if "relative-timing" in feats:
            return True, "出来事の前後関係が答えで、期限や時点が別の出来事からの相対で決まる"
        if feats & HANDOFF_FEATURES:
            return True, "主体から主体へ渡るたびに減る・変わることが答え"
        actors, steps = c.get("actors", 0), c.get("steps", 0)
        if actors >= 2 and actors + steps >= 4:
            return True, f"主体・部分 {actors} と段階 {steps} を合わせて {actors + steps}（4 以上）"
        return False, "主体が一つで分岐のない段階、または主体・部分と段階を合わせて 3 つ以下の直線は文章（番号付きリスト）にする"
    if form == "conditions":
        if c.get("conditions", 0) >= 2:
            return True, f"条件が {c['conditions']} 個で、どの条件に当たるかで結果が分かれる"
        return False, "条件がすべて揃って結果が一つに決まる規則は文章にする"
    if form == "appearance":
        return True, "形状や見た目が答え"
    return False, f"根拠の形 form は {', '.join(FORMS)} のいずれかにする"


# ---------------------------------------------------------------- 検査


def check_spec(spec: dict, kind: str = "figure", index: dict | None = None, routes: dict | None = None,
               reader_level: str | None = None, chrome: bool | None = None) -> list[Issue]:
    """figure spec をカタログの規則に照らす。cyrus の完了条件と、このスクリプトの check の両方から使う。"""
    index = index or load_index()
    routes = routes if routes is not None else load_routes()
    issues: list[Issue] = []
    E = lambda r, m: issues.append(Issue(r, "error", m))  # noqa: E731
    W = lambda r, m: issues.append(Issue(r, "warn", m))  # noqa: E731

    if not isinstance(spec, dict) or not spec:
        return [Issue("VP001", "error", "spec（問い・答え・根拠・趣旨・パターン）を書いてください。")]
    for k in ("question", "answer", "drawing"):
        if not (isinstance(spec.get(k), str) and spec[k].strip()):
            E("VP002", f"spec.{k} を書いてください。")
    answer = spec.get("answer") if isinstance(spec.get("answer"), str) else ""
    if answer:
        n = visible_length(answer)
        if len(split_sentences(answer)) > 1:
            E("VP003", "spec.answer（読み手に持ち帰ってほしい主張）は一文にしてください。主張が複数なら主となる一つを答えにし、残りは組み合わせかキャプションに回します（手順1）。")
        if n > ANSWER_WARN:  # 字数はカタログの規則ではなく、キャプションとして読みやすい長さの目安（cyrus の文の長さの基準と同じ）
            W("VP003", f"spec.answer が {n} 字あります。キャプションになる一文なので、{ANSWER_WARN} 字以内が目安です（{ANSWER_ERROR} 字を超えると cyrus の lint でも長い文になります）。")
        for j in JOINERS:
            if j in answer:
                W("VP004", f"spec.answer に「{j}」があります。述語が二つなら主張が二つなので、主となる一つに絞ってください。")
                break

    ev = spec.get("evidence")
    ev_ok = isinstance(ev, dict)
    if not ev_ok:
        E("VP010", "spec.evidence は {form, description, counts, features} のオブジェクトにしてください。")
        ev = {}
    form = ev.get("form")
    if ev_ok and not _is(form, FORMS):
        E("VP010", f"spec.evidence.form は {', '.join(FORMS)} のいずれかにしてください。")
    if ev_ok and not (isinstance(ev.get("description"), str) and ev["description"].strip()):
        E("VP011", "spec.evidence.description（根拠を、数を添えて）を書いてください。")
    counts = ev.get("counts") or {}
    if not isinstance(counts, dict):
        E("VP012", "spec.evidence.counts は {軸: 整数} のオブジェクトにしてください。")
        counts = {}
    for k, v in counts.items():
        if k not in COUNT_KEYS:
            W("VP012", f"spec.evidence.counts の「{k}」は知らない軸です（使えるのは {', '.join(COUNT_KEYS)}）。")
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            E("VP012", f"spec.evidence.counts.{k} は 0 以上の整数にしてください。")
    feats = ev.get("features") or []
    if not isinstance(feats, list):
        E("VP013", f"spec.evidence.features は配列にしてください（使えるのは {', '.join(sorted(FEATURES))}）。")
        feats = []
    for f in feats:
        if not isinstance(f, str) or f not in FEATURES:
            E("VP013", f"spec.evidence.features の「{f}」は知らない特徴です（使えるのは {', '.join(sorted(FEATURES))}）。")
    if ev_ok and _is(form, FORMS):
        ok, why = figure_warranted(ev)
        if not ok:
            # 目安に満たなくても、根拠を文章で書き出して「同じ文型が 3 つ以上並ぶ」「読み手が前の文に戻って照合し直す」なら図表にする（手順2）。
            # その判断は書き手のもので、ここでは理由が記録されていることだけを確かめる。
            reason = ev.get("below_threshold_reason")
            if _is(reason, BELOW_THRESHOLD_REASONS):
                W("VP020", f"手順2 の目安（{why}）には満たないが、{BELOW_THRESHOLD_REASONS[reason]}ので図表にした、と記録されています。"
                           "根拠を文章で書き出して確かめた上での判断にしてください。")
            else:
                E("VP020", f"手順2 の目安では、この根拠は図表にしません: {why}。文章（箇条書き）で書くか、根拠の数を見直してください。"
                           "根拠を文章で書き出し、同じ文型が 3 つ以上並ぶ、または読み手が前の文に戻って照合し直すなら、"
                           "evidence.below_threshold_reason に repeated-pattern か cross-reference を書いて図表にできます。")

    if not _is(spec.get("precision"), PRECISIONS):
        E("VP014", f"spec.precision は {' / '.join(PRECISIONS)} にしてください。")
    if not _is(spec.get("reading"), READINGS):
        E("VP015", f"spec.reading は through（通読）/ lookup（参照）にしてください。")

    intents = index.get("intents") or {}
    patterns = index.get("patterns") or {}
    intent = spec.get("intent")
    pattern = spec.get("pattern")
    if not isinstance(intent, str) or intent not in intents:
        E("VP030", f"spec.intent「{intent}」は趣旨の一覧にありません（`vp_figure.py intents` で確かめてください）。")
    elif _is(form, FORM_INTENTS) and intent not in FORM_INTENTS[form]:
        E("VP031", f"根拠の形「{FORM_JA[form]}」から選べる趣旨は {', '.join(sorted(FORM_INTENTS[form]))} です（手順2・3）。"
                   f"「{intent}」は別の根拠の形から選びます。")
    if not isinstance(pattern, str) or pattern not in patterns:
        E("VP040", f"spec.pattern「{pattern}」はパターンの一覧にありません。")
    elif intent in intents:
        cands = [c["pattern"] for c in intents[intent]["candidates"]]
        if pattern not in cands:
            E("VP041", f"「{pattern}」は趣旨「{intents[intent]['name']}」の候補にありません（候補: {', '.join(cands)}）。"
                       "趣旨を選び直すか、候補から選んでください（手順5・6）。")
        elif cands and pattern != cands[0]:
            rej = spec.get("rejected") if isinstance(spec.get("rejected"), list) else []
            rejected = {r.get("pattern") for r in rej if isinstance(r, dict)}
            if cands[0] not in rejected:
                W("VP042", f"第一候補は「{cands[0]}」です。「{pattern}」に切り替える条件（when）に当たることを、"
                           f"spec.rejected に第一候補を退けた理由として書いてください（手順6）。")
    p = patterns.get(pattern) if isinstance(pattern, str) else None
    p = p or {}
    if p:
        if p.get("status") == "planned":
            E("VP043", f"「{pattern}」はまだ定義のないパターンです。")
        fams = FAMILY_FOR_KIND.get(kind, set())
        if fams and p.get("family") not in fams:
            E("VP044", f"kind「{kind}」のブロックに family「{p.get('family')}」のパターンは置けません"
                       f"（table は表のパターン、figure は chart・diagram・picture のパターン）。")
        for axis, rng in (p.get("scale") or {}).items():
            if axis in counts and isinstance(counts[axis], int):
                lo, hi = parse_range(rng)
                v = counts[axis]
                if (lo is not None and v < lo) or (hi is not None and v > hi):
                    W("VP050", f"「{pattern}」の規模の制約 {axis}: {rng} に対し、counts.{axis} が {v} です。"
                               "候補を切り替えるか、組み合わせ（手順7）を検討してください（手順5）。")
        if spec.get("precision") == "overview" and p.get("text_dependency") == "high":
            W("VP051", f"精度が overview なのに、「{pattern}」はテキスト依存度が high です。選択を見直してください（4.3）。")
        if spec.get("precision") == "exact" and p.get("precision") == "overview":
            E("VP053", f"正確な値を読ませる（precision: exact）のに、「{pattern}」は概観のパターン（precision: overview）です。"
                       "精度の制約で候補から外れます（手順5）。表など exact のパターンにするか、概観の図と正確な値の表に分けてください（手順7）。")
        if p.get("complexity") == "high" and reader_level == "novice":
            W("VP052", f"「{pattern}」は専門的な記法の知識が要ります（complexity: high）。読者は初心者なので、"
                       "凡例を付けるか、記法の知識が要らない候補に切り替えてください（3.3）。")
    it = spec.get("intent_type")
    if it and (not isinstance(it, str) or it not in (index.get("intent_types") or [])):
        E("VP060", f"spec.intent_type「{it}」は意図の型の一覧にありません。型は本書の側でしか増やしません。"
                   "型がなければ空にし、デザインの文法と作成時のルールに従って描きます（手順8）。")

    render = spec.get("render")
    if not _is(render, RENDERS):
        E("VP070", f"spec.render は {', '.join(RENDERS)} のいずれかにしてください。")
    elif p:
        allowed = allowed_renders(routes, pattern)
        if not allowed:
            E("VP071", f"「{pattern}」を描く手段がこのスキルにはありません。別の候補か組み合わせ（手順7）、表か文章（1.4）にしてください。")
        elif render not in allowed:
            E("VP074", f"「{pattern}」は {', '.join(allowed)} で描きます。spec.render を {render} から直してください。")
        caveat = ((routes.get(pattern) or {}).get("caveats") or {}).get(render)
        if caveat:
            W("VP073", f"「{pattern}」を {render} で描くときの注意: {caveat}")
        if render == "vega-lite" and chrome is False:
            E("VP072", "Vega-Lite の図は PNG にするのに Chrome が要りますが、この環境にはありません。"
                       "出力媒体の制約（3.3）として、Mermaid で描ける候補か表に切り替えてください。")
    return issues


# ---------------------------------------------------------------- 描画


def find_chrome() -> str | None:
    env = os.environ.get("CYRUS_CHROME") or os.environ.get("VP_CHROME")
    if env and Path(env).exists():
        return env
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        exe = shutil.which(name)
        if exe:
            return exe
    for cand in sorted((Path.home() / ".cache" / "ms-playwright").glob("chromium-*/chrome-linux*/chrome"), reverse=True):
        return str(cand)
    return None


class RenderError(RuntimeError):
    pass


MEASURE_JS = """
<script>
function vpDone(err, needSvg) {
  // フォントの読み込みで行の高さが変わるので、読み込みを待ってから測る
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
    const el = document.getElementById('fig');
    const r = el.getBoundingClientRect();
    const drawn = needSvg === false || el.querySelector('svg, canvas');
    const pre = document.createElement('pre');
    pre.id = 'vp-layout';
    pre.textContent = JSON.stringify({width: Math.ceil(r.width), height: Math.ceil(r.height),
      error: err ? String(err).slice(0, 300) : (drawn ? '' : 'no svg rendered')});
    document.body.appendChild(pre);
  });
}
</script>
"""
# ヘッドレス Chrome は、窓の高さが小さすぎると（およそ 130px 未満）何も描かないので、下限を置く
MIN_WINDOW_HEIGHT = 240
SAFETY = 24


def _mermaid_html(source: str) -> str:
    return ("<!doctype html><html lang=\"ja\"><head><meta charset=\"utf-8\"><style>"
            "body{margin:0;background:#fff;font-family:'Noto Sans CJK JP','Noto Sans JP',sans-serif}"
            "#fig{display:inline-block;padding:12px}pre.mermaid{margin:0}#fig svg{display:block}#vp-layout{display:none}"
            "</style></head><body>"
            f"<div id=\"fig\"><pre class=\"mermaid\">{html.escape(source)}</pre></div>"
            f"<script src=\"{html.escape(MERMAID_SRC)}\"></script>" + MEASURE_JS +
            "<script>mermaid.initialize({startOnLoad:false, theme:'neutral'});"
            "mermaid.run().then(function(){vpDone('')}, function(e){vpDone(e)});</script></body></html>")


def _generic_html(fragment: str) -> str:
    """HTML の断片（表など）をそのまま描く。表を画像にして逆読みさせるときに使う。"""
    return ("<!doctype html><html lang=\"ja\"><head><meta charset=\"utf-8\"><style>"
            "body{margin:0;background:#fff;font-family:'Noto Sans CJK JP','Noto Sans JP',sans-serif;font-size:15px;color:#1f2328}"
            "#fig{display:inline-block;padding:12px}#vp-layout{display:none}"
            "table{border-collapse:collapse}th,td{border:1px solid #d0d7de;padding:0.3em 0.6em;text-align:left;vertical-align:top}"
            "th{background:#f6f8fa}</style></head><body>"
            f"<div id=\"fig\">{fragment}</div>" + MEASURE_JS +
            "<script>window.addEventListener('load', function(){vpDone('', false)});</script></body></html>")


def _vega_html(spec: dict, width: int) -> str:
    scripts = "".join(f"<script src=\"{html.escape(s)}\"></script>" for s in VEGA_SRCS)
    spec = dict(spec)
    spec.setdefault("$schema", "https://vega.github.io/schema/vega-lite/v5.json")
    spec.setdefault("background", "white")
    cfg = spec.setdefault("config", {})
    cfg.setdefault("font", "Noto Sans CJK JP, Noto Sans JP, sans-serif")
    return ("<!doctype html><html lang=\"ja\"><head><meta charset=\"utf-8\"><style>"
            "body{margin:0;background:#fff}#fig{display:inline-block;padding:12px}#vp-layout{display:none}</style></head><body>"
            "<div id=\"fig\"></div>" + scripts + MEASURE_JS +
            "<script>vegaEmbed('#fig', " + json.dumps(spec, ensure_ascii=False) +
            ", {actions:false, renderer:'svg'}).then(function(){vpDone('')}, function(e){vpDone(e)});</script>"
            "</body></html>")


def _chrome(args: list[str], timeout: int = 90) -> subprocess.CompletedProcess:
    exe = find_chrome()
    if not exe:
        raise RenderError("Chrome / Chromium が見つかりません（環境変数 CYRUS_CHROME で場所を指定できます）。")
    with tempfile.TemporaryDirectory(prefix="vp-chrome-") as profile:
        base = [exe, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--no-first-run",
                "--disable-extensions", f"--user-data-dir={profile}"]
        return subprocess.run(base + args, capture_output=True, text=True, timeout=timeout)


def render(source: str | dict, out: Path, width: int = 760, scale: int = 2) -> dict:
    """Mermaid のテキストか Vega-Lite の仕様（または {"html": 断片}）を PNG にする。{width, height} を返す。"""
    if isinstance(source, dict) and "html" in source and len(source) == 1:
        page = _generic_html(source["html"])
    elif isinstance(source, dict):
        page = _vega_html(source, width)
    else:
        page = _mermaid_html(source)
    with tempfile.TemporaryDirectory(prefix="vp-render-") as td:
        p = Path(td) / "fig.html"
        p.write_text(page, encoding="utf-8")
        proc = _chrome([f"--window-size={width + 24},800", "--virtual-time-budget=15000", "--dump-dom", p.as_uri()])
        m = re.search(r'<pre id="vp-layout">(.*?)</pre>', proc.stdout, re.S)
        if not m:
            raise RenderError(f"Chrome から描画結果を取得できませんでした: {proc.stderr.strip()[:300]}")
        layout = json.loads(html.unescape(m.group(1)))
        if layout.get("error"):
            raise RenderError(f"図を描けませんでした: {layout['error']}")
        w, h = max(int(layout["width"]), 1), max(int(layout["height"]), 1)
        out.parent.mkdir(parents=True, exist_ok=True)
        win_w, win_h = w + SAFETY, max(h + SAFETY, MIN_WINDOW_HEIGHT)
        proc = _chrome([f"--window-size={win_w},{win_h}", f"--force-device-scale-factor={scale}",
                        "--virtual-time-budget=15000", f"--screenshot={out}", p.as_uri()])
        if not out.exists():
            raise RenderError(f"PNG を作れませんでした: {proc.stderr.strip()[:300]}")
    _crop_to_content(out, pad=12 * scale)
    return {"width": w, "height": h}


def _crop_to_content(png: Path, pad: int) -> None:
    """余白を切る（Pillow があるときだけ。なければ、窓の大きさのまま残す）。"""
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return
    im = Image.open(png).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).getbbox()
    if not box:
        return
    x0, y0, x1, y1 = box
    im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad))).save(png)


def load_source(path: Path) -> str | dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json" or path.name.endswith(".vl.json"):
        return json.loads(text)
    return text


# ---------------------------------------------------------------- CLI


def cmd_intents(index: dict) -> None:
    for iid, it in index["intents"].items():
        first = it["candidates"][0]["pattern"] if it["candidates"] else "-"
        print(f"{iid:24s} {it['category']}・{it['name']}（第一候補: {first}、定義: {it['family_doc']}）")


def cmd_candidates(index: dict, routes: dict, iid: str) -> None:
    it = index["intents"].get(iid)
    if not it:
        sys.exit(f"趣旨 {iid} はありません。`vp_figure.py intents` で一覧を見てください。")
    print(f"趣旨: {it['name']}（{it['category']}）— 定義は references/catalog/{it['family_doc']}")
    print("候補（読み手の認知コストが低い順。先頭が第一候補、2 番目以降は when に当たるときだけ）:")
    for i, c in enumerate(it["candidates"], 1):
        p = index["patterns"].get(c["pattern"]) or {}
        r = routes.get(c["pattern"]) or {}
        scale = "、".join(f"{k} {v}" for k, v in (p.get("scale") or {}).items()) or "-"
        route = r.get("route", "未定")
        if r.get("alt"):
            route += "（" + "・".join(r["alt"]) + " も可）"
        print(f"{i:2d}. {c['pattern']}（{p.get('name', '?')}）" + (f"  when: {c['when']}" if c.get("when") else ""))
        print(f"     精度 {p.get('precision', '?')}／記法 {p.get('complexity', '?')}／テキスト依存 {p.get('text_dependency', '?')}"
              f"／規模 {scale}／描き方 {route}" + (f"（{r['fidelity']}）" if r.get("fidelity") else ""))
        for a in p.get("avoid_when") or []:
            print(f"     避ける: {a}")
        for how, text in (r.get("caveats") or {}).items():
            print(f"     {how} の注意: {text}")
        if r.get("notes"):
            print(f"     描き方の補足: {r['notes']}")
        if p.get("path"):
            print(f"     文書: references/catalog/{p['path']}" + ("（意図の型と手段あり）" if p.get("has_intent_means") else ""))


def cmd_show(index: dict, pid: str) -> None:
    p = index["patterns"].get(pid)
    if not p or not p.get("path"):
        sys.exit(f"パターン {pid} の文書がありません。")
    print((CATALOG_DIR / p["path"]).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="vp_figure", description="visual-patterns: 図表の仕様の検査と描画")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("intents", help="趣旨の一覧")
    p = sub.add_parser("candidates", help="趣旨の候補パターンと制約")
    p.add_argument("intent")
    p = sub.add_parser("show", help="パターン文書を表示する")
    p.add_argument("pattern")
    p = sub.add_parser("check", help="figure spec を検査する")
    p.add_argument("spec", type=Path)
    p.add_argument("--kind", choices=["figure", "table"], default="figure")
    p.add_argument("--reader-level", choices=["novice", "intermediate", "expert"])
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("render", help="Mermaid か Vega-Lite を PNG にする")
    p.add_argument("source", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--width", type=int, default=760)
    p.add_argument("--scale", type=int, default=2)
    args = ap.parse_args(argv)

    index = load_index()
    routes = load_routes()
    if args.cmd == "intents":
        cmd_intents(index)
    elif args.cmd == "candidates":
        cmd_candidates(index, routes, args.intent)
    elif args.cmd == "show":
        cmd_show(index, args.pattern)
    elif args.cmd == "check":
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        if "spec" in spec and isinstance(spec["spec"], dict):  # 10-detail.json のブロックをそのまま渡してもよい
            args.kind = spec.get("kind", args.kind)
            spec = spec["spec"]
        issues = check_spec(spec, args.kind, index, routes, args.reader_level, chrome=find_chrome() is not None)
        if args.json:
            print(json.dumps([i.to_dict() for i in issues], ensure_ascii=False, indent=1))
        else:
            for i in issues:
                print(f"[{ {'error': 'エラー', 'warn': '警告', 'info': '参考'}[i.severity] }] {i.rule}: {i.message}")
            if not issues:
                print("問題ありません。")
        sys.exit(1 if any(i.severity == "error" for i in issues) else 0)
    elif args.cmd == "render":
        try:
            size = render(load_source(args.source), args.out, args.width, args.scale)
        except RenderError as e:
            sys.exit(str(e))
        print(f"{args.out}（{size['width']}×{size['height']}）")


# VP074（render の不一致）は、VP071（描く手段がない）と分けてある: 前者は spec.render を直すだけでよい。


if __name__ == "__main__":
    main()
