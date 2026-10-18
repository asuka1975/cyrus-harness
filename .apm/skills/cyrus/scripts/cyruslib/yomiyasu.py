"""yomiyasu（nanaism/yomiyasu）の検査の記録との照合。

ステージ13の推敲は yomiyasu スキルが受け持つ。yomiyasu は推敲した最終稿に lint と diff をかけ、
その記録（最終稿のハッシュ）を残す。ここでは `yomiyasu_check.py verify` で、final.md が
draft.md から推敲して検査したときの本文のままかを確かめる。
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from .workspace import SKILL_DIR, project_root

CHECK_REL = Path("yomiyasu") / "scripts" / "yomiyasu_check.py"
STATUS_RE = re.compile(r"^yomiyasu-check: (\S+)", re.M)


def find_check() -> Path | None:
    env = os.environ.get("CYRUS_YOMIYASU")
    if env:
        return Path(env) if Path(env).exists() else None
    # APM は依存の yomiyasu を cyrus と同じ skills/ に置く
    for cand in (SKILL_DIR.parent / CHECK_REL, project_root() / ".claude" / "skills" / CHECK_REL):
        if cand.exists():
            return cand
    return None


def verify(script: Path, final: Path, source: Path, timeout: int = 120) -> tuple[int, str, str]:
    """(終了コード, 状態, 1行目の説明) を返す。終了コード0なら記録と合った。

    状態フォルダは yomiyasu と同じ決め方（作業ディレクトリから上の git の最上位の .yomiyasu/）にするため、
    プロジェクトのルートで動かす。
    """
    try:
        proc = subprocess.run([sys.executable, str(script), "verify", "--final", str(final), "--source", str(source)],
                              capture_output=True, text=True, timeout=timeout, cwd=str(project_root()))
    except subprocess.TimeoutExpired:
        return 124, "timeout", f"yomiyasu の照合が {timeout} 秒で終わりませんでした。"
    out = proc.stdout or ""
    m = STATUS_RE.search(out)
    first = (out.strip().splitlines() or [(proc.stderr or "").strip()])[0]
    return proc.returncode, (m.group(1) if m else "unknown"), first
