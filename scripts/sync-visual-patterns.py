#!/usr/bin/env python3
"""図表パターンのカタログ（visual-patterns）を、スキル visual-patterns に写す。

写すのは、選んで描くのに要るものだけ: taxonomy.md・index.yaml・表現形式ごとの分類文書・パターン文書。
開発の記録（fixtures/・adr/・development.md）は写さない（本体は記録を引かない、という本書自身の決まりに合わせる）。

あわせて、cyrus の CLI が標準ライブラリだけで読めるように、index.yaml とパターン文書の frontmatter を
data/index.json にまとめる。描き方の対応（data/render-routes.json）は手で保守し、ここでは触らない。

使い方（開発時だけ。PyYAML が要る）:
    python3 scripts/sync-visual-patterns.py [--source <カタログのディレクトリ>] [--check]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / ".apm" / "skills" / "visual-patterns"
DEFAULT_SOURCE = Path.home() / "work" / "ai-agent" / "visual-patterns"
FAMILIES = ("chart", "diagram", "table", "picture")
COPY_TOP = ("taxonomy.md", "index.yaml")

try:
    import yaml  # PyYAML。開発時にだけ使う（配布するスキルと CLI は標準ライブラリだけで動く）
except ImportError:  # pragma: no cover
    sys.exit("PyYAML が要ります: pip install pyyaml")


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def intents_table(taxonomy: str) -> dict[str, dict]:
    """3.1「趣旨の一覧」の表から、趣旨の名前・カテゴリ・定義のある分類文書を取る。"""
    out: dict[str, dict] = {}
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`([a-z0-9-]+)`\s*\|\s*`([^`]+)`\s*\|\s*$", taxonomy, re.M):
        category, name, iid, doc = m.groups()
        if category in ("カテゴリ", "---"):
            continue
        out[iid] = {"name": name, "category": category, "family_doc": doc}
    return out


def intent_types(taxonomy: str) -> list[str]:
    """6.3「意図の型の一覧」の表から、型の名前を取る（型は本書の側でしか増やさない）。"""
    sec = taxonomy.split("#### 意図の型の一覧", 1)
    if len(sec) < 2:
        return []
    body = sec[1].split("####", 1)[0]
    names = []
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", body, re.M):
        if m.group(1) in ("意図の型", "---") or set(m.group(1)) <= set("-: "):
            continue
        names.append(m.group(1))
    return names


def has_rows(pattern_md: str) -> bool:
    """「意図の型と手段」の表にデータ行があるか。"""
    sec = pattern_md.split("## 意図の型と手段", 1)
    if len(sec) < 2:
        return False
    body = sec[1].split("\n## ", 1)[0]
    rows = [l for l in body.splitlines() if l.startswith("|")]
    return len(rows) > 2


def copied_files(src: Path) -> list[str]:
    """写す対象（元からの相対パス）。"""
    rel = list(COPY_TOP)
    for fam in FAMILIES:
        rel += sorted(f"{fam}/{f.name}" for f in (src / fam).glob("*.md"))
    return rel


def source_info(src: Path) -> dict:
    info = {"name": src.name, "synced_at": dt.date.today().isoformat()}
    try:
        info["commit"] = subprocess.run(["git", "-C", str(src), "rev-parse", "--short", "HEAD"],
                                        capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(src), "status", "--porcelain", "--untracked-files=no"],
                               capture_output=True, text=True, check=True).stdout.strip()
        info["dirty"] = bool(dirty)
    except (OSError, subprocess.CalledProcessError):
        pass
    return info


def build_index(src: Path, catalog: Path) -> dict:
    taxonomy = (src / "taxonomy.md").read_text(encoding="utf-8")
    idx = yaml.safe_load((src / "index.yaml").read_text(encoding="utf-8"))
    names = intents_table(taxonomy)
    intents = {}
    for iid, spec in (idx.get("intents") or {}).items():
        meta = names.get(iid, {})
        intents[iid] = {
            "name": meta.get("name", iid),
            "category": meta.get("category", ""),
            "family_doc": meta.get("family_doc", ""),
            "candidates": [{"pattern": c["pattern"], "when": c.get("when", "")} for c in spec.get("candidates", [])],
        }
    patterns = {}
    for p in idx.get("patterns") or []:
        pid = p["id"]
        entry = {"name": p.get("name", pid), "layer": p.get("layer", "primitive"), "family": p.get("family", ""),
                 "path": p.get("path", ""), "status": p.get("status", "available")}
        if p.get("path"):
            md = (src / p["path"]).read_text(encoding="utf-8")
            fm = frontmatter(md)
            info = fm.get("information_structure") or {}
            entry.update({
                "name": fm.get("name", entry["name"]),
                "aliases": fm.get("aliases") or [],
                "primary_intent": fm.get("primary_intent", ""),
                "secondary_intents": fm.get("secondary_intents") or [],
                "shape": info.get("shape", ""),
                "attributes": info.get("attributes") or [],
                "scale": {k: str(v) for k, v in (fm.get("scale") or {}).items()},
                "precision": fm.get("precision", ""),
                "complexity": fm.get("complexity", ""),
                "visual_encoding": {k: str(v) for k, v in (fm.get("visual_encoding") or {}).items()},
                "text_dependency": fm.get("text_dependency", ""),
                "abstraction": fm.get("abstraction", ""),
                "best_for": fm.get("best_for") or [],
                "avoid_when": fm.get("avoid_when") or [],
                "alternatives": fm.get("alternatives") or [],
                "has_intent_means": has_rows(md),
            })
        patterns[pid] = entry
    return {
        "source": source_info(src),
        "intents": intents,
        "patterns": patterns,
        "intent_types": intent_types(taxonomy),
    }


def sync(src: Path, check: bool) -> int:
    if not (src / "taxonomy.md").exists():
        sys.exit(f"{src} にカタログ（taxonomy.md）がありません。--source で場所を指定してください。")
    catalog = DEST / "references" / "catalog"
    index = build_index(src, catalog)
    if check:
        cur = DEST / "data" / "index.json"
        old = json.loads(cur.read_text(encoding="utf-8")) if cur.exists() else {}
        same = {k: v for k, v in old.items() if k != "source"} == {k: v for k, v in index.items() if k != "source"}
        stale = [r for r in copied_files(src) if not (catalog / r).exists() or (catalog / r).read_bytes() != (src / r).read_bytes()]
        extra = [f"{fam}/{p.name}" for fam in FAMILIES for p in (catalog / fam).glob("*.md") if not (src / fam / p.name).exists()]
        print("index.json は最新です。" if same else "index.json がカタログと違います。sync を実行してください。")
        if stale or extra:
            print("カタログの写しが元と違います: " + ", ".join(stale + [f"{x}（元にない）" for x in extra]))
        return 0 if same and not stale and not extra else 1
    # 写す（古いファイルは消す）
    for fam in FAMILIES:
        d = catalog / fam
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        for f in sorted((src / fam).glob("*.md")):
            shutil.copyfile(f, d / f.name)
    for name in COPY_TOP:
        shutil.copyfile(src / name, catalog / name)
    (DEST / "data").mkdir(parents=True, exist_ok=True)
    (DEST / "data" / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # 描き方の対応に抜けがないか知らせる（ここでは直さない）
    routes_path = DEST / "data" / "render-routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8")) if routes_path.exists() else {}
    missing = [pid for pid, p in index["patterns"].items() if p.get("status") != "planned" and pid not in routes]
    n_files = sum(1 for fam in FAMILIES for _ in (catalog / fam).glob("*.md"))
    print(f"カタログを写しました: {n_files} ファイル、趣旨 {len(index['intents'])}、パターン {len(index['patterns'])}"
          f"（元: {index['source'].get('commit', '?')}{' +未コミットの変更' if index['source'].get('dirty') else ''}）")
    if missing:
        print(f"render-routes.json にないパターン: {', '.join(missing)}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help=f"カタログのディレクトリ（既定: {DEFAULT_SOURCE}）")
    ap.add_argument("--check", action="store_true", help="写さずに、index.json と写したカタログが元と合っているかだけ確かめる")
    args = ap.parse_args()
    sys.exit(sync(args.source.expanduser().resolve(), args.check))


if __name__ == "__main__":
    main()
