"""koko（asuka1975/koko）の記録との照合。

ステージ13の推敲は koko スキルが受け持つ。koko は final.md を意味のまとまりに分け、まとまりごとに
koko-copy-editor に推敲させ、koko-proofreader に校正させ（書き手がしたことの受け身を能動に。判定モデルの値は見ない）、
判定モデルの値（P(Yes)。人が書いた文と判定する確率）で採点し直して、
記録（documents/<slug>/koko/record.json。本文のハッシュとまとまりごとの値・校正の有無・機械チェック）を残す。
ここでは `koko.py verify` で final.md がその本文のままかを確かめ、record.json から機械チェックの結果と
まとまりの状態を読む。頼るのは koko の references/interface.md にある取り決めだけ。
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from .workspace import SKILL_DIR, project_root

SCRIPT_REL = Path("koko") / "scripts" / "koko.py"
WORKDIR = "koko"  # documents/<slug>/koko/（計画・まとまり・報告・記録の置き場所）
# assemble が本文に使うファイル。koko のあとの直しはここに書く（校正後の本文があるのに revised.md を直すと、assemble が止まる）
BODY_FILES = "chunks/cNN.proofread.md（校正していないまとまりは cNN.revised.md）"
STATUS_RE = re.compile(r"^koko-check: (\S+)", re.M)
CHUNK_STATUSES = {"met": "達成", "not_met": "未達", "already_met": "推敲前から達成", "unrevised": "未推敲"}


def find_script() -> Path | None:
    env = os.environ.get("CYRUS_KOKO")
    if env:
        return Path(env) if Path(env).exists() else None
    # APM は依存の koko を cyrus と同じ skills/ に置く
    for cand in (SKILL_DIR.parent / SCRIPT_REL, project_root() / ".claude" / "skills" / SCRIPT_REL):
        if cand.exists():
            return cand
    return None


def uv_bin() -> str | None:
    """koko は `uv run <koko.py>` で動かす取り決め（採点サーバの環境も uv が持つ）。"""
    return os.environ.get("UV") or shutil.which("uv")


def verify(script: Path, workdir: Path, final: Path, timeout: int = 120) -> tuple[int, str, str]:
    """(終了コード, 状態, 1行目の説明) を返す。終了コード0なら final が記録した本文のまま。

    状態は ok / modified / no_record / missing_final / model_changed（koko の取り決め）。
    """
    cmd = [uv_bin() or "uv", "run", "--quiet", str(script), "verify", "--workdir", str(workdir), "--final", str(final)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(project_root()))
    except subprocess.TimeoutExpired:
        return 124, "timeout", f"koko の照合が {timeout} 秒で終わりませんでした。"
    except OSError as e:
        return 127, "error", f"koko を実行できませんでした: {e}"
    out = proc.stdout or ""
    m = STATUS_RE.search(out)
    lines = out.strip().splitlines()  # 1行目は koko-check: <状態>、2行目が説明
    detail = lines[1] if len(lines) > 1 else (lines[0] if lines else (proc.stderr or "").strip())
    return proc.returncode, (m.group(1) if m else "unknown"), detail


def read_record(workdir: Path) -> dict | None:
    """koko/record.json（koko-record-v1）。なければ、読めなければ None。"""
    p = workdir / "record.json"
    if not p.exists():
        return None
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return rec if isinstance(rec, dict) and isinstance(rec.get("chunks"), list) else None


def summarize(rec: dict) -> str:
    """記録の要約を一行にする（GT138 の参考）。"""
    s = rec.get("summary") or {}
    chunks = rec.get("chunks") or []
    n = {k: sum(1 for c in chunks if c.get("status") == k) for k in CHUNK_STATUSES}
    proofread = s.get("proofread") if isinstance(s.get("proofread"), int) else sum(1 for c in chunks if c.get("proofread"))
    def mean(v):
        return "—" if not isinstance(v, (int, float)) else f"{v:.2f}"
    return (f"まとまり {len(chunks)}（達成 {n['met']}・未達 {n['not_met']}・推敲前から達成 {n['already_met']}・未推敲 {n['unrevised']}、"
            f"校正 {proofread}）、平均 P(Yes) {mean(s.get('mean_before'))} → {mean(s.get('mean_after'))}（目標 {rec.get('target', '—')}）")
