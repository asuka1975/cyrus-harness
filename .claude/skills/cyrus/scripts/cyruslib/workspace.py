"""ステージの定義と、ドキュメントごとの作業状態（state.json）の管理。"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent.parent


@dataclass(frozen=True)
class Stage:
    key: str
    phase: str
    name: str
    title_ja: str
    artifact: str
    confirm: bool = False  # 次へ進む前にユーザーの承認が必要か

    @property
    def guide(self) -> Path:
        return SKILL_DIR / "stages" / f"{STAGE_KEYS.index(self.key) + 1:02d}-{self.key}.md"


STAGES: list[Stage] = [
    Stage("intent", "Interview", "Intent Capture", "目的をつかむ", "01-intent.md", confirm=True),
    Stage("context", "Interview", "Context Sharing", "背景を共有してもらう", "02-context/sources.md"),
    Stage("reader", "Interview", "Target Reader", "読者を描く", "03-reader.json", confirm=True),
    Stage("analysis", "Interview", "Context Analysis", "伝えるべき情報を選ぶ", "04-analysis.md"),
    Stage("claims", "Interview", "Claim Analysis", "主張を組み立てる", "05-claims.json", confirm=True),
    Stage("facts", "Interview", "Fact Verification", "事実を確かめる", "06-facts.json"),
    Stage("logic", "Construction", "Logical Structure Design", "論理を検証する", "07-logic/Argument.lean"),
    Stage("structure", "Construction", "Document Structure Design", "文書の骨組みを決める", "08-structure.json"),
    Stage("storyline", "Construction", "Storyline Design", "話の流れを決める", "09-storyline.json", confirm=True),
    Stage("detail", "Construction", "Document Detail Design", "見せ方を決める", "10-detail.json"),
    Stage("writing", "Construction", "Document Writing", "書く", "draft.md"),
    Stage("cogload", "Refinement", "Cognitive Load Check", "認知負荷を下げる", "12-cogload.json"),
    Stage("wording", "Refinement", "Wording Check", "言葉を読者に合わせる", "final.md", confirm=True),
]
STAGE_KEYS = [s.key for s in STAGES]
PHASE_JA = {"Interview": "インタビュー", "Construction": "組み立て", "Refinement": "仕上げ"}


def stage(key: str) -> Stage:
    for s in STAGES:
        if s.key == key:
            return s
    raise KeyError(f"未知のステージです: {key}（{', '.join(STAGE_KEYS)}）")


def project_root() -> Path:
    for env in ("CYRUS_ROOT", "CLAUDE_PROJECT_DIR"):
        v = os.environ.get(env)
        if v:
            return Path(v)
    return Path.cwd()


def documents_dir() -> Path:
    return project_root() / os.environ.get("CYRUS_DOCS_DIR", "documents")


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-]{0,63}$")


class Workspace:
    def __init__(self, slug: str):
        self.slug = slug
        self.dir = documents_dir() / slug
        self.state_path = self.dir / "state.json"

    # ---- 作成・読み込み ----
    @classmethod
    def create(cls, slug: str, title: str = "") -> "Workspace":
        if not SLUG_RE.match(slug):
            raise ValueError("slug は英小文字・数字・ハイフンで、64文字以内にしてください（例: wiki-search-proposal）。")
        ws = cls(slug)
        if ws.state_path.exists():
            raise FileExistsError(f"{ws.dir} はすでにあります。`cyrus use {slug}` で切り替えてください。")
        (ws.dir / "02-context").mkdir(parents=True, exist_ok=True)
        (ws.dir / "07-logic").mkdir(parents=True, exist_ok=True)
        ws.save({
            "slug": slug,
            "title": title,
            "stage": STAGES[0].key,
            "created_at": now(),
            "updated_at": now(),
            "history": [],
            "confirmations": {},
        })
        set_current(slug)
        return ws

    @classmethod
    def current(cls) -> "Workspace | None":
        slug = get_current()
        if not slug:
            return None
        ws = cls(slug)
        return ws if ws.state_path.exists() else None

    def load(self) -> dict:
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def save(self, state: dict) -> None:
        state["updated_at"] = now()
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- 便利関数 ----
    def path(self, rel: str) -> Path:
        return self.dir / rel

    def read_json(self, rel: str) -> dict | None:
        p = self.path(rel)
        if not p.exists():
            return None
        return json.loads(p.read_text(encoding="utf-8"))

    def stage(self) -> Stage:
        return stage(self.load()["stage"])

    def is_done(self) -> bool:
        return self.load().get("stage") == "done"


def _current_file() -> Path:
    return documents_dir() / ".current"


def get_current() -> str | None:
    p = _current_file()
    if p.exists():
        v = p.read_text(encoding="utf-8").strip()
        return v or None
    return None


def set_current(slug: str) -> None:
    p = _current_file()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(slug + "\n", encoding="utf-8")


def list_workspaces() -> list[Workspace]:
    d = documents_dir()
    if not d.exists():
        return []
    return [Workspace(p.name) for p in sorted(d.iterdir()) if (p / "state.json").exists()]


def artifact_owner(path: Path) -> tuple[Workspace, Stage | None, str] | None:
    """ファイルパスから、どのワークスペースのどの成果物かを判定する。"""
    try:
        rel = path.resolve().relative_to(documents_dir().resolve())
    except (ValueError, OSError):
        return None
    parts = rel.parts
    if len(parts) < 2:
        return None
    ws = Workspace(parts[0])
    if not ws.state_path.exists():
        return None
    inner = "/".join(parts[1:])
    for s in STAGES:
        if s.artifact == inner:
            return ws, s, inner
    return ws, None, inner
