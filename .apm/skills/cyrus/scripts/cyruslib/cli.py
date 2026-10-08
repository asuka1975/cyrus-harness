"""cyrus コマンドラインインターフェース。"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import gates, lint, leancheck, logicround, scaffold, skim, wording
from .issues import count, format_issues
from .reader import build_profile, load_profile
from .workspace import (PHASE_JA, STAGE_KEYS, STAGES, Workspace, documents_dir, list_workspaces,
                        now, set_current, stage)


def _ws(args) -> Workspace:
    if getattr(args, "doc", None):
        ws = Workspace(args.doc)
        if not ws.state_path.exists():
            sys.exit(f"ドキュメント {args.doc} が見つかりません。")
        return ws
    ws = Workspace.current()
    if ws is None:
        sys.exit("進行中のドキュメントがありません。`cyrus new <slug> --title <タイトル>` で始めてください。")
    return ws


def _progress(state: dict) -> str:
    key = state["stage"]
    if key == "done":
        return "完了"
    idx = STAGE_KEYS.index(key)
    st = STAGES[idx]
    in_phase = [s for s in STAGES if s.phase == st.phase]
    pos = in_phase.index(st) + 1
    return f"{PHASE_JA[st.phase]} {pos}/{len(in_phase)}「{st.title_ja}」（{st.name}）・全体 {idx + 1}/{len(STAGES)}"


def cmd_new(args):
    try:
        ws = Workspace.create(args.slug, args.title or "")
    except (ValueError, FileExistsError) as e:
        sys.exit(str(e))
    print(f"ドキュメント「{args.title or args.slug}」を {ws.dir} に作りました。")
    print(scaffold.scaffold(ws, "intent"))
    _print_next(ws)


def cmd_use(args):
    ws = Workspace(args.slug)
    if not ws.state_path.exists():
        sys.exit(f"ドキュメント {args.slug} が見つかりません。")
    set_current(args.slug)
    print(f"{args.slug} に切り替えました。")
    _print_next(ws)


def cmd_list(args):
    cur = Workspace.current()
    items = list_workspaces()
    if not items:
        print("ドキュメントはまだありません。")
    for ws in items:
        st = ws.load()
        mark = "*" if cur and cur.slug == ws.slug else " "
        print(f"{mark} {ws.slug}  {st.get('title', '')}  — {_progress(st)}")


def cmd_status(args):
    ws = _ws(args)
    st = ws.load()
    if args.json:
        print(json.dumps({"slug": ws.slug, "dir": str(ws.dir), **st}, ensure_ascii=False, indent=2))
        return
    print(f"ドキュメント: {st.get('title') or ws.slug}（{ws.slug}）")
    print(f"場所: {ws.dir}")
    print(f"進捗: {_progress(st)}")
    done = {h["stage"] for h in st.get("history", []) if h.get("event") == "advance"}
    for s in STAGES:
        mark = "✓" if s.key in done and STAGE_KEYS.index(s.key) < (STAGE_KEYS.index(st["stage"]) if st["stage"] != "done" else 99) else (
            "▶" if s.key == st["stage"] else " ")
        print(f"  {mark} {STAGE_KEYS.index(s.key) + 1:2d}. [{PHASE_JA[s.phase]}] {s.title_ja}（{s.name}） → {s.artifact}")


def _print_next(ws: Workspace):
    st = ws.load()
    if st["stage"] == "done":
        print(f"すべてのステージが完了しています。完成版: {ws.path('final.md')}")
        return
    s = stage(st["stage"])
    print(f"\n現在のステージ: {_progress(st)}")
    print(f"ガイド: {s.guide}")
    print(f"成果物: {ws.path(s.artifact)}")
    if s.confirm:
        print("このステージを終えるにはユーザーの承認が必要です（`cyrus advance --confirmed \"承認の要旨\"`）。")


def cmd_next(args):
    ws = _ws(args)
    _print_next(ws)
    st = ws.load()
    if st["stage"] != "done":
        issues = gates.run_gate(ws, st["stage"])
        c = count(issues)
        print(f"完了条件の状態: エラー {c['error']} 件・警告 {c['warn']} 件（詳細は `cyrus check`）")


def cmd_check(args):
    ws = _ws(args)
    key = args.stage or ws.load()["stage"]
    if key == "done":
        print("すべて完了しています。")
        return
    issues = gates.run_gate(ws, key)
    c = count(issues)
    if args.json:
        print(json.dumps({"stage": key, "counts": c, "issues": [i.to_dict() for i in issues]}, ensure_ascii=False, indent=2))
    else:
        print(f"ステージ {key} の完了条件: エラー {c['error']} 件・警告 {c['warn']} 件・参考 {c['info']} 件")
        if issues:
            print(format_issues(issues))
        if not c["error"]:
            print("→ 完了条件を満たしています。" + ("ユーザーの承認を得てから `cyrus advance --confirmed \"…\"`。" if stage(key).confirm else "`cyrus advance` で次へ進めます。"))
    sys.exit(1 if c["error"] else 0)


def cmd_advance(args):
    ws = _ws(args)
    st = ws.load()
    key = st["stage"]
    if key == "done":
        print("すべて完了しています。")
        return
    s = stage(key)
    issues = gates.run_gate(ws, key)
    c = count(issues)
    if c["error"]:
        print(f"完了条件を満たしていないため進めません（エラー {c['error']} 件）。")
        print(format_issues(issues, min_severity="error"))
        sys.exit(1)
    if s.confirm and not args.confirmed:
        print("このステージはユーザーの承認が必要です。成果物の要点をユーザーに見せて承認をもらい、"
              "`cyrus advance --confirmed \"承認の要旨\"` を実行してください。")
        sys.exit(2)
    if c["warn"] and not args.accept_warnings:
        print(f"警告が {c['warn']} 件あります。直すか、問題ないと判断したら `--accept-warnings` を付けてください。")
        print(format_issues(issues, min_severity="warn"))
        sys.exit(3)
    idx = STAGE_KEYS.index(key)
    nxt = STAGE_KEYS[idx + 1] if idx + 1 < len(STAGE_KEYS) else "done"
    entry = {"event": "advance", "stage": key, "at": now(), "warnings": c["warn"]}
    if args.confirmed and s.confirm:
        entry["confirmed"] = args.confirmed
        st.setdefault("confirmations", {})[key] = {"note": args.confirmed, "at": now()}
    st.setdefault("history", []).append(entry)
    # 書き上げた直後の原稿を残しておく（Refinement での変化を比べられるように）
    if key == "writing" and ws.path("draft.md").exists():
        shutil.copyfile(ws.path("draft.md"), ws.path("draft.v1.md"))
    st["stage"] = nxt
    ws.save(st)
    print(f"ステージ「{s.title_ja}」を完了しました。")
    if nxt != "done":
        msg = scaffold.scaffold(ws, nxt)
        print(msg)
    _print_next(ws)


def cmd_back(args):
    ws = _ws(args)
    st = ws.load()
    target = args.stage
    if target not in STAGE_KEYS:
        sys.exit(f"未知のステージです: {target}")
    cur = st["stage"]
    if cur != "done" and STAGE_KEYS.index(target) > STAGE_KEYS.index(cur):
        sys.exit("先のステージには戻れません。")
    st.setdefault("history", []).append({"event": "back", "from": cur, "stage": target, "at": now(), "reason": args.reason or ""})
    st["stage"] = target
    # 戻った先より後の承認は無効にする
    for k in list(st.get("confirmations", {})):
        if STAGE_KEYS.index(k) >= STAGE_KEYS.index(target):
            del st["confirmations"][k]
    ws.save(st)
    print(f"ステージ「{stage(target).title_ja}」に戻りました。後続の成果物は残してあります。前の成果物との整合を保つよう更新してください。")
    _print_next(ws)


def cmd_scaffold(args):
    ws = _ws(args)
    key = args.stage or ws.load()["stage"]
    print(scaffold.scaffold(ws, key, force=args.force))


def _resolve_file(ws: Workspace | None, name: str) -> Path:
    p = Path(name)
    if p.exists():
        return p
    if ws and ws.path(name).exists():
        return ws.path(name)
    sys.exit(f"{name} が見つかりません。")


def _profile_for(args, ws: Workspace | None):
    if getattr(args, "reader", None):
        return load_profile(Path(args.reader))
    if ws:
        return build_profile(ws.read_json("03-reader.json"))
    return build_profile(None)


def cmd_lint(args):
    ws = Workspace.current() if not args.doc else Workspace(args.doc)
    path = _resolve_file(ws, args.file)
    prof = _profile_for(args, ws)
    issues, metrics = lint.lint_text(path.read_text(encoding="utf-8"), prof)
    c = count(issues)
    if args.json:
        print(json.dumps({"file": str(path), "metrics": metrics, "counts": c, "issues": [i.to_dict() for i in issues]},
                         ensure_ascii=False, indent=2))
    else:
        print(f"{path}: エラー {c['error']} 件・警告 {c['warn']} 件・参考 {c['info']} 件（読者プロファイル: {prof.level}）")
        print("指標: " + "、".join(f"{k}={v}" for k, v in metrics.items() if k != "styles"))
        if issues:
            print(format_issues(issues, str(path.name), limit=args.limit, min_severity=args.min_severity))
    sys.exit(1 if c["error"] else 0)


def cmd_wording(args):
    ws = Workspace.current() if not args.doc else Workspace(args.doc)
    path = _resolve_file(ws, args.file)
    prof = _profile_for(args, ws)
    glossary = wording.glossary_from_detail(ws.read_json("10-detail.json")) if ws else {}
    issues, summary = wording.check_wording(path.read_text(encoding="utf-8"), prof, glossary)
    c = count(issues)
    if args.json:
        print(json.dumps({"file": str(path), "summary": summary, "counts": c, "issues": [i.to_dict() for i in issues]},
                         ensure_ascii=False, indent=2))
    else:
        print(f"{path}: エラー {c['error']} 件・警告 {c['warn']} 件・参考 {c['info']} 件")
        if issues:
            print(format_issues(issues, str(path.name), limit=args.limit, min_severity=args.min_severity))
    sys.exit(1 if c["error"] else 0)


def cmd_skim(args):
    ws = _ws(args) if not args.file_only else None
    src = _resolve_file(ws, args.file)
    text = src.read_text(encoding="utf-8")
    out_dir = (ws.path("skim") if ws else src.parent / "skim")
    out_dir.mkdir(parents=True, exist_ok=True)
    modes = list(skim.VIEWS) if args.mode == "all" else [args.mode]
    for m in modes:
        p = out_dir / f"{m}.md"
        p.write_text(skim.VIEWS[m](text), encoding="utf-8")
        print(f"{m}: {p}")
    h = skim.text_hash(text)
    (out_dir / "meta.json").write_text(json.dumps({"source": src.name, "draft_hash": h}, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"原稿の指紋: {h}（12-cogload.json の skim_test.draft_hash に記録してください）")


def cmd_vision(args):
    from . import visionreader, visual
    cfg = None
    if args.show_command or not args.no_reader:
        try:
            cfg = visionreader.load_config()
        except visionreader.ReaderConfigError as e:
            sys.exit(f"読み手の設定に誤りがあります: {e}")
    if args.show_command:
        print("\n".join(visionreader.describe(cfg, args.model)))
        return
    ws = _ws(args)
    src = _resolve_file(ws, args.file)
    text = src.read_text(encoding="utf-8")
    reader = ws.read_json("03-reader.json")
    media = args.media or ((reader or {}).get("reading_context") or {}).get("medium") or "screen"
    out_dir = ws.path("skim") / "visual"
    try:
        res = visual.render(text, out_dir, media=media, keep_sharp=args.keep_sharp)
    except visual.VisualUnavailable as e:
        sys.exit(f"画像化できません: {e}")
    h = skim.text_hash(text)
    print(f"画像: {len(res.pages)}画面（{media}）、注視点 {res.fixations} か所 → {out_dir}")
    print(f"原稿の指紋: {h}")
    if args.no_reader:
        return
    model = args.model or cfg.model
    print(f"{cfg.name}" + (f"（{model}）" if model else "") + " に読ませています…")
    try:
        out = visionreader.run(res.pages, res.overview, reader, model=args.model, cfg=cfg)
    except visionreader.ReaderUnavailable as e:
        sys.exit(f"{cfg.name} に読ませられませんでした: {e}")
    out = {"source": src.name, "draft_hash": h, "media": media, **out}
    dest = out_dir / visionreader.RESULT_NAME
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    r = out["result"]
    print(f"\n結果: {dest}（{out['duration_seconds']}秒）")
    print(f"要約: {r.get('reader_summary', '')}")
    print(f"いちばん伝えたいこと: {r.get('main_point', '')}")
    print(f"求められている行動: {r.get('requested_action', '')}")
    for sec in r.get("sections", []):
        print(f"  - {sec.get('heading')}: {sec.get('understood')}（{sec.get('confidence')}）")
    notes = r.get("visual_notes") or {}
    for key, label in (("missed_or_hidden", "目立たなかった重要な点"), ("layout_issues", "見た目の構造の問題")):
        for x in notes.get(key, []):
            print(f"  [{label}] {x}")
    print("\n次に cyrus-alignment-judge で 09-storyline.json と照合し、12-cogload.json の visual_test に記録してください。")


def _names(names: list[str], limit: int = 5) -> str:
    return "、".join(names[:limit]) + (f" ほか {len(names) - limit} 個" if len(names) > limit else "")


def cmd_lean(args):
    ws = _ws(args)
    issues, report = leancheck.check(ws.dir)
    c = count(issues)
    if report.get("counts"):
        k = report["counts"]
        a = report["atoms"]
        print(f"公理 {k['axioms']}（宣言 {k['declarations']}・関係公理 {k['relational']}）、"
              f"原子命題 {a['total']}（自明でないもの {a['non_trivial']}。主張の定理が使う {a['used_by_claims']}、"
              f"@beyond・@baseline だけが使う {a['side_only']}、使われない {a['unused']}）")
    if report.get("claims"):
        print("主張ごとの確信度（主張の定理が依存する関係公理の確信度の最小値）:")
        for cid, r in report["claims"].items():
            print(f"  {cid}: {r['confidence']:.2f}  → {r['hedge']['guidance']}"
                  + (f"  ／最も弱い公理: {_names(r.get('weakest_links') or [r['weakest_link']])}（{r['weakest_confidence']}）"
                     if r.get("weakest_link") else ""))
    if report.get("weak_premises"):
        print("確信度を左右する弱い前提（ステージの終わりに、日常語でユーザーに見せる）:")
        for w in report["weak_premises"]:
            print(f"  {w['axiom']}（【{w['kind']}】{w['confidence']}、主張 {', '.join(w['claims'])}）: {w['statement'][:60]}")
    if report.get("rework"):
        print(f"手戻りの一覧（ステージ6で証拠を集める公理。確信度 {leancheck.REWORK_THRESHOLD} 未満か @against 付き）:")
        for r in report["rework"]:
            why = "・".join({"low_confidence": "確信度が低い", "against": "反対の証拠"}[x] for x in r["reasons"])
            print(f"  {r['axiom']}（{r['confidence']}、{why}）→ 主張 {', '.join(r['claims']) or 'なし'}")
    print(f"Lean 検査: エラー {c['error']} 件・警告 {c['warn']} 件・参考 {c['info']} 件")
    if issues:
        print(format_issues(issues, "Argument.lean"))
    sys.exit(1 if c["error"] else 0)


def cmd_logic_round(args):
    ws = _ws(args)
    if args.action == "close":
        issues, s = logicround.close(ws.dir)
        if issues:
            print(format_issues(issues))
            sys.exit(1)
        print(f"{s['round']}周目（このループの {s['loop_round']} 周目）を閉じました（07-logic/rounds/{s['round']:02d}/）。判定: {s['verdict']}"
              f"（高 {s['high']}・中 {s['mid']}・低 {s['low']}）、門のエラー {s['gate_errors']} 件")
        print("主張の確信度: " + "、".join(f"{k} {v}" for k, v in s["claims"].items()))
        if s["rework"]:
            print("手戻りの一覧: " + "、".join(s["rework"]))
        print(("→ 打ち切り: " if s["stop"] else "→ 続ける: ") + s["reason"])
        sys.exit(0 if s["stop"] else (3 if s["escalate"] else 2))
    issues, s = logicround.diff(ws.dir)
    if issues:
        print(format_issues(issues))
        sys.exit(1)
    print(f"07-logic/diff.md を作りました（rounds/{s['previous']} との差分）。変わった宣言 {len(s['changes'])} 個、"
          f"設計書の行 {s['rows']}（当たっていない行 {s['rows_without_hit']}）、設計書にない変更 {len(s['unplanned'])} 個。")


def cmd_hook(args):
    from . import hooks
    sys.exit(hooks.run(args.event))


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="cyrus", description="インタビュー型ドキュメント執筆ハーネス")
    ap.add_argument("--doc", help="対象のドキュメント（slug）。省略時は進行中のもの")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="新しいドキュメントを始める")
    p.add_argument("slug")
    p.add_argument("--title", default="")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("use", help="進行中のドキュメントを切り替える")
    p.add_argument("slug")
    p.set_defaults(func=cmd_use)

    sub.add_parser("list", help="ドキュメントの一覧").set_defaults(func=cmd_list)

    p = sub.add_parser("status", help="進捗を表示する")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)

    sub.add_parser("next", help="現在のステージとガイドを表示する").set_defaults(func=cmd_next)

    p = sub.add_parser("check", help="ステージの完了条件を検査する")
    p.add_argument("stage", nargs="?")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("advance", help="完了条件を満たしていれば次のステージへ進む")
    p.add_argument("--confirmed", help="ユーザーの承認の要旨（承認が必要なステージで必須）")
    p.add_argument("--accept-warnings", action="store_true", help="警告を確認したうえで進む")
    p.set_defaults(func=cmd_advance)

    p = sub.add_parser("back", help="前のステージに戻る")
    p.add_argument("stage", choices=STAGE_KEYS)
    p.add_argument("--reason", default="")
    p.set_defaults(func=cmd_back)

    p = sub.add_parser("scaffold", help="成果物の雛形を作る")
    p.add_argument("stage", nargs="?", choices=STAGE_KEYS)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_scaffold)

    for name, func, helptext in (("lint", cmd_lint, "認知負荷を検査する"), ("wording", cmd_wording, "言葉遣いを検査する")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("file", nargs="?", default="draft.md")
        p.add_argument("--reader", help="読者ペルソナの JSON（省略時は進行中ドキュメントの 03-reader.json）")
        p.add_argument("--json", action="store_true")
        p.add_argument("--limit", type=int, default=60)
        p.add_argument("--min-severity", choices=["error", "warn", "info"], default="info")
        p.set_defaults(func=func)

    p = sub.add_parser("skim", help="拾い読み（周辺視野）ビューを作る")
    p.add_argument("file", nargs="?", default="draft.md")
    p.add_argument("--mode", choices=["all", *skim.VIEWS], default="all")
    p.add_argument("--file-only", action="store_true", help="ドキュメントに紐づけず、ファイルの隣に出力する")
    p.set_defaults(func=cmd_skim)

    p = sub.add_parser("vision", help="原稿を画像にして周辺視野を模してぼかし、読み手（既定は agy 経由の Gemini）に読ませる")
    p.add_argument("file", nargs="?", default="draft.md")
    p.add_argument("--media", choices=["screen", "mobile", "print", "slide"], help="省略時は 03-reader.json の reading_context.medium")
    p.add_argument("--model", help="読み手に渡すモデル名（既定は cyrus.config.json の vision.reader.model。"
                                   "設定ファイルがなければ環境変数 CYRUS_AGY_MODEL か gemini-3.8-flash-medium）")
    p.add_argument("--no-reader", action="store_true", help="画像を作るだけで読み手には読ませない")
    p.add_argument("--keep-sharp", action="store_true", help="ぼかす前の画像（sharp.png）も残す")
    p.add_argument("--show-command", action="store_true",
                   help="読み手を起動せず、cyrus.config.json から組み立てたコマンドと環境変数を表示する")
    p.set_defaults(func=cmd_vision)

    p = sub.add_parser("logic-round", help="ステージ7の周を記録する（close: いまの周を写して打ち切りを判定 / diff: 前の周との差分と対応表）")
    p.add_argument("action", choices=["close", "diff"])
    p.set_defaults(func=cmd_logic_round)

    sub.add_parser("lean", help="論証のモデルを検査し（門）、主張ごとの確信度と手戻りの一覧を出す").set_defaults(func=cmd_lean)

    p = sub.add_parser("hook", help="Claude Code のフックから呼ばれる")
    p.add_argument("event", choices=["post-edit", "session-start"])
    p.set_defaults(func=cmd_hook)

    args = ap.parse_args(argv)
    args.func(args)
