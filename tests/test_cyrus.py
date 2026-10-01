"""cyrus ハーネスのテスト。

実行: python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import re
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".apm" / "skills" / "cyrus" / "scripts"
CLI = SCRIPTS / "cyrus.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "wiki-search"
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True  # .apm/ に __pycache__ を作らない（apm install がそれを .claude/ に写してしまうため）

from cyruslib import agyreader, jatext, leancheck, leansrc, lint, logicround, skim, visual, wording  # noqa: E402
from cyruslib.reader import build_profile  # noqa: E402

HAS_LEAN = leancheck.find_lean() is not None
try:
    import PIL  # noqa: F401
    HAS_VISUAL = visual.find_chrome() is not None
except ImportError:
    HAS_VISUAL = False
FAKE_AGY = Path(__file__).resolve().parent / "fakes" / "fake_agy.py"

MINI = Path(__file__).resolve().parent / "fixtures" / "logic-mini"
PRIVATE = Path(__file__).resolve().parent / "fixtures" / "private-subject"  # 公開しない題材（.gitignore）

# ステージの成果物のほかに、完了条件の検査で参照されるファイル
EXTRA_FILES = {"logic": ["07-logic/Model.lean"], "cogload": ["skim/visual/gemini-reader.json"]}

STAGE_FILES = [
    ("intent", "01-intent.md"),
    ("context", "02-context/sources.md"),
    ("reader", "03-reader.json"),
    ("analysis", "04-analysis.md"),
    ("claims", "05-claims.json"),
    ("facts", "06-facts.json"),
    ("logic", "07-logic/Argument.lean"),
    ("structure", "08-structure.json"),
    ("storyline", "09-storyline.json"),
    ("detail", "10-detail.json"),
    ("writing", "draft.md"),
    ("cogload", "12-cogload.json"),
    ("wording", "final.md"),
]


def rules(issues):
    return {i.rule for i in issues}


class JaTextTest(unittest.TestCase):
    def test_split_keeps_quotes(self):
        s = jatext.split_sentences("彼は「行く。」と言った。次の文です。")
        self.assertEqual(s, ["彼は「行く。」と言った。", "次の文です。"])

    def test_sentence_style(self):
        self.assertEqual(jatext.sentence_style("これはペンです。"), "desumasu")
        self.assertEqual(jatext.sentence_style("これはペンである。"), "plain")
        self.assertEqual(jatext.sentence_style("検索が遅い。"), "plain")
        self.assertEqual(jatext.sentence_style("そうですね。"), "desumasu")
        self.assertEqual(jatext.sentence_style("結果の一覧。"), "neutral")

    def test_pickup_drops_hiragana(self):
        self.assertEqual(jatext.pickup("社内の検索はとても遅いです"), "社内 検索 遅")


class LintTest(unittest.TestCase):
    def lint(self, text, reader=None):
        return lint.lint_text(text, build_profile(reader))[0]

    def test_long_sentence(self):
        text = "# t\n\n" + "あ" * 50 + "、" + "い" * 80 + "です。\n"
        self.assertIn("JA001", rules([i for i in self.lint(text) if i.severity == "error"]))

    def test_threshold_depends_on_reader(self):
        text = "# t\n\n" + "検索" * 32 + "です。\n"  # 67字
        novice = self.lint(text, {"knowledge_level": "novice"})
        expert = self.lint(text, {"knowledge_level": "expert"})
        self.assertIn("JA001", rules(novice))
        self.assertNotIn("JA001", rules(expert))

    def test_mixed_style(self):
        text = "# t\n\n速いです。遅い。重い。軽いです。\n"
        self.assertIn("JA006", rules(self.lint(text)))

    def test_heading_skip(self):
        self.assertIn("ST001", rules(self.lint("# t\n\n## a\n\n#### b\n\n本文です。\n")))

    def test_figure_reference(self):
        issues = self.lint("# t\n\n図2を見てください。\n")
        self.assertIn("ST010", rules([i for i in issues if i.severity == "error"]))
        ok = self.lint("# t\n\n図1のとおりです。\n\n図1: 流れ\n")
        self.assertNotIn("ST010", rules(ok))

    def test_caption_not_counted_as_style(self):
        text = "# t\n\n図1のとおりです。流れを示します。手順は3つです。\n\n図1: 取り込みまでの流れ\n"
        self.assertNotIn("JA006", rules(self.lint(text)))

    def test_double_negative(self):
        self.assertIn("JA008", rules(self.lint("# t\n\n使えないわけではありません。\n")))

    def test_new_term_density(self):
        text = "# t\n\n## 用語\n\nアルファベット、ブラボー、チャーリー、デルタフォース、エコーチェンバーを使います。\n"
        self.assertIn("ST011", rules(self.lint(text, {"knowledge_level": "novice"})))

    def test_fixture_final_is_clean(self):
        reader = json.loads((FIXTURE / "03-reader.json").read_text(encoding="utf-8"))
        issues = self.lint((FIXTURE / "final.md").read_text(encoding="utf-8"), reader)
        self.assertEqual([i for i in issues if i.severity == "error"], [])


class WordingTest(unittest.TestCase):
    reader = {"knowledge_level": "novice", "known_terms": [], "unknown_terms": ["インデックス"],
              "avoid_terms": [{"term": "Elasticsearch", "replace": "いまの検索の仕組み"}]}

    def check(self, text):
        return wording.check_wording(text, build_profile(self.reader))[0]

    def test_undefined_unknown_term(self):
        self.assertIn("WD002", rules(self.check("# t\n\nインデックスを作ります。\n")))

    def test_defined_unknown_term(self):
        issues = self.check("# t\n\nインデックス（検索用の索引）を作ります。インデックスは毎晩更新します。\n")
        self.assertNotIn("WD002", rules(issues))
        self.assertNotIn("WD003", rules(issues))

    def test_definition_after_first_use(self):
        text = "# t\n\nインデックスを作ります。\n\nインデックスとは、検索用の索引のことです。\n"
        self.assertIn("WD003", rules(self.check(text)))

    def test_avoid_term(self):
        self.assertIn("WD001", rules(self.check("# t\n\nElasticsearchは遅いです。\n")))

    def test_ascii_term_matches_whole_word(self):
        prof = build_profile({"avoid_terms": [{"term": "PR", "replace": "プルリクエスト"}]})
        self.assertNotIn("WD001", rules(wording.check_wording("# t\n\nprefix を付けます。\n", prof)[0]))
        self.assertIn("WD001", rules(wording.check_wording("# t\n\nPRを出します。\n", prof)[0]))

    def test_hard_expression_and_variants(self):
        issues = self.check("# t\n\n状況に鑑みて判断します。サーバーとサーバを比べます。\n")
        self.assertIn("WD005", rules(issues))
        self.assertIn("WD007", rules(issues))


class SkimTest(unittest.TestCase):
    def test_views(self):
        text = (FIXTURE / "final.md").read_text(encoding="utf-8")
        outline = skim.outline_view(text)
        self.assertIn("## お願いしたいこと", outline)
        self.assertNotIn("理由は、", outline)  # 段落の2文目以降は出さない
        self.assertIn("焦点 1", skim.local_view(text))
        self.assertNotIn("を", skim.pickup_view(text).replace("#", ""))


class CliCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="cyrus-test-"))
        self.env = dict(os.environ, CYRUS_ROOT=str(self.tmp))
        self.env.pop("CLAUDE_PROJECT_DIR", None)
        self.doc = self.tmp / "documents" / "wiki-search"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *args, stdin=None):
        return subprocess.run([sys.executable, str(CLI), *args], capture_output=True, text=True,
                              env=self.env, input=stdin, timeout=300)

    def put(self, rel):
        dst = self.doc / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURE / rel, dst)

    def advance_through(self, upto: str):
        for key, rel in STAGE_FILES:
            if key == upto:
                return
            self.put(rel)
            for extra in EXTRA_FILES.get(key, []):
                self.put(extra)
            r = self.run_cli("advance", "--confirmed", "テスト", "--accept-warnings")
            self.assertEqual(r.returncode, 0, f"{key}: {r.stdout}{r.stderr}")


class GateTest(CliCase):
    def setUp(self):
        super().setUp()
        self.assertEqual(self.run_cli("new", "wiki-search", "--title", "テスト").returncode, 0)

    def test_scaffold_blocks_advance(self):
        r = self.run_cli("advance", "--confirmed", "x")
        self.assertEqual(r.returncode, 1)
        self.assertIn("GT002", r.stdout)

    def test_confirmation_required(self):
        self.put("01-intent.md")
        r = self.run_cli("advance")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(json.loads((self.doc / "state.json").read_text())["stage"], "intent")

    def test_claim_cycle_detected(self):
        self.advance_through("claims")
        data = json.loads((FIXTURE / "05-claims.json").read_text(encoding="utf-8"))
        data["claims"][0]["premises"].append("C3")
        data["claims"][2]["premises"].append("C1")
        data["claims"][2]["supports"] = "C1"
        data["claims"][0]["supports"] = "C3"
        (self.doc / "05-claims.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        r = self.run_cli("check")
        self.assertIn("GT038", r.stdout)

    def test_claim_form_required(self):
        self.advance_through("claims")
        data = json.loads((FIXTURE / "05-claims.json").read_text(encoding="utf-8"))
        del data["main_claim"]["form"]
        data["claims"][0]["form"] = "比べる"
        (self.doc / "05-claims.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertEqual(out.count("GT042"), 2)

    def test_rework_fact_with_axioms_is_not_warned(self):
        self.advance_through("facts")
        data = json.loads((FIXTURE / "06-facts.json").read_text(encoding="utf-8"))
        data["facts"].append({"id": "F5", "statement": "本番の記事数で計測しても5秒以内に検索に出た", "status": "verified",
                              "method": "execution", "sources": [], "evidence": "本番相当の3万件で計測", "notes": "",
                              "axioms": ["prodDelay_le_test"]})
        data["facts"].append({"id": "F6", "statement": "どの公理のためでもない事実", "status": "verified", "method": "execution",
                              "sources": [], "evidence": "x", "notes": ""})
        (self.doc / "06-facts.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertNotIn("事実 F5 は 05-claims.json にありません", out)
        self.assertIn("事実 F6 は 05-claims.json にありません", out)

    def test_rework_coverage_after_back_from_logic(self):
        self.advance_through("logic")
        for rel in ("07-logic/Argument.lean", "07-logic/Model.lean"):
            self.put(rel)
        self.run_cli("lean")  # ステージ7の report.json（手戻りの一覧）を作る
        self.assertEqual(self.run_cli("back", "facts", "--reason", "ステージ7の手戻り").returncode, 0)
        report = json.loads((self.doc / "07-logic" / "report.json").read_text(encoding="utf-8"))
        rework = [r["axiom"] for r in report["rework"]]
        self.assertTrue(rework)
        out = self.run_cli("check").stdout
        self.assertIn("GT058", out)
        data = json.loads((self.doc / "06-facts.json").read_text(encoding="utf-8"))
        data["facts"].append({"id": "F5", "statement": "部会までに確かめられなかった", "status": "unverified",
                              "method": "user", "sources": [], "notes": "情報システム部の返事が期限に間に合わなかった",
                              "axioms": rework[1:]})
        (self.doc / "07-logic" / "rejected.json").write_text(json.dumps(
            {"rejected": [{"axiom": rework[0], "reason": "誤り", "facts": ["F5"], "rejected_at": "2026-10-01"}]},
            ensure_ascii=False), encoding="utf-8")
        data["facts"].append({"id": "F6", "statement": "x", "status": "verified", "method": "execution", "sources": [],
                              "evidence": "x", "notes": "", "axioms": ["no_such_axiom"]})
        (self.doc / "06-facts.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertNotIn("GT058", out)
        self.assertIn("GT059", out)

    def test_refuted_fact_in_premises(self):
        self.advance_through("facts")
        data = json.loads((FIXTURE / "06-facts.json").read_text(encoding="utf-8"))
        data["facts"][1]["status"] = "refuted"
        (self.doc / "06-facts.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        r = self.run_cli("check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("GT055", r.stdout)

    def test_storyline_order(self):
        self.advance_through("storyline")
        data = json.loads((FIXTURE / "09-storyline.json").read_text(encoding="utf-8"))
        data["sections"][1], data["sections"][2] = data["sections"][2], data["sections"][1]
        (self.doc / "09-storyline.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT083", self.run_cli("check").stdout)

    def test_skim_score_threshold(self):
        self.advance_through("cogload")
        data = json.loads((FIXTURE / "12-cogload.json").read_text(encoding="utf-8"))
        for s in data["skim_test"]["sections"][1:]:
            s["recovered"] = "no"
        (self.doc / "12-cogload.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT125", self.run_cli("check").stdout)

    def test_visual_test_required_and_tied_to_draft(self):
        self.advance_through("cogload")
        self.put("12-cogload.json")
        self.put("skim/visual/gemini-reader.json")
        self.assertEqual(self.run_cli("check").returncode, 0)
        data = json.loads((FIXTURE / "12-cogload.json").read_text(encoding="utf-8"))
        del data["visual_test"]
        (self.doc / "12-cogload.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT140", self.run_cli("check").stdout)
        self.put("12-cogload.json")
        (self.doc / "skim" / "visual" / "gemini-reader.json").unlink()
        self.assertIn("GT142", self.run_cli("check").stdout)

    def test_skim_test_must_match_current_draft(self):
        self.advance_through("cogload")
        self.put("12-cogload.json")
        self.put("skim/visual/gemini-reader.json")
        self.assertEqual(self.run_cli("check").returncode, 0)
        with open(self.doc / "draft.md", "a", encoding="utf-8") as f:
            f.write("\n追記した段落です。\n")
        out = self.run_cli("check").stdout
        self.assertIn("GT129", out)
        self.assertIn("GT143", out)
        r = self.run_cli("skim")
        self.assertIn("原稿の指紋", r.stdout)
        self.assertTrue((self.doc / "skim" / "meta.json").exists())

    def test_back_clears_later_confirmations(self):
        self.advance_through("analysis")
        r = self.run_cli("back", "reader", "--reason", "読者を見直す")
        self.assertEqual(r.returncode, 0)
        st = json.loads((self.doc / "state.json").read_text())
        self.assertEqual(st["stage"], "reader")
        self.assertIn("intent", st["confirmations"])
        self.assertNotIn("reader", st["confirmations"])

    def test_post_edit_hook_reports_errors(self):
        self.advance_through("writing")
        bad = "# t\n\n## a\n\n#### b\n\n" + "とても長い文" * 30 + "です。\n"
        (self.doc / "draft.md").write_text(bad, encoding="utf-8")
        payload = json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(self.doc / "draft.md")}})
        r = self.run_cli("hook", "post-edit", stdin=payload)
        self.assertEqual(r.returncode, 2)
        self.assertIn("ST001", r.stderr)
        outside = json.dumps({"tool_input": {"file_path": str(self.tmp / "other.md")}})
        self.assertEqual(self.run_cli("hook", "post-edit", stdin=outside).returncode, 0)

    def test_session_start_hook(self):
        r = self.run_cli("hook", "session-start")
        self.assertIn("wiki-search", r.stdout)


class VisualHtmlTest(unittest.TestCase):
    def test_fixations_marked(self):
        md = ("# 題\n\n## 節\n\n最初の文です。次の文です。\n\n1. 一つ目の手順を行う\n2. 二つ目\n\n"
              "> 注意の最初の文です。続きです。\n\n```sh\ngit pull\ngit push\n```\n\n図1: 流れ\n\n**太字**です。\n")
        h = visual.markdown_to_html(md)
        self.assertIn('<span data-fx="heading">節</span>', h)
        self.assertIn('<span data-fx="first">最初の文です。</span>次の文です。', h)
        self.assertIn("<ol>", h)
        self.assertIn('<span data-fx="first">注意の最初の文です。</span>', h)
        self.assertIn('<span data-fx="code-head">git pull</span>', h)
        self.assertIn('<span data-fx="caption">図1: 流れ</span>', h)
        self.assertIn('<strong data-fx="bold">太字</strong>', h)
        self.assertNotIn("mermaid.min.js", h)  # 図がなければ外部のライブラリを読まない

    def test_prompt_has_no_paths(self):
        p = agyreader.build_prompt({"persona": {"role": "部長"}, "knowledge_level": "novice"}, ["page-01.png"], True, False)
        self.assertIn("部長", p)
        self.assertNotIn("/", p.replace("／", ""))


@unittest.skipUnless(HAS_VISUAL, "Chrome か Pillow がないため画像のテストを省略")
class VisionTest(CliCase):
    def test_render_and_fake_gemini(self):
        self.env["CYRUS_AGY"] = str(FAKE_AGY)
        log = self.tmp / "agy.json"
        self.env["FAKE_AGY_LOG"] = str(log)
        self.env["CYRUS_MERMAID_JS"] = ""  # テストではネットワークを使わない
        self.run_cli("new", "wiki-search", "--title", "テスト")
        self.advance_through("cogload")
        r = self.run_cli("vision")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        called = json.loads(log.read_text(encoding="utf-8"))
        self.assertEqual(called["problems"], [])
        self.assertIn("overview.png", called["files"])
        out = json.loads((self.doc / "skim" / "visual" / "gemini-reader.json").read_text(encoding="utf-8"))
        self.assertEqual(out["draft_hash"], skim.text_hash((self.doc / "draft.md").read_text(encoding="utf-8")))
        self.assertEqual(out["result"]["requested_action"], "予算の承認")
        self.assertTrue((self.doc / "skim" / "visual" / "page-01.png").exists())

    def test_foveation_blurs_outside_fixations(self):
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (200, 100), "white")
        d = ImageDraw.Draw(img)
        for x in range(0, 200, 4):
            d.line([(x, 0), (x, 100)], fill="black")
        out = visual.foveate(img, [[10, 10, 30, 16]], 16)
        sharp = out.crop((15, 12, 35, 24)).convert("L").getextrema()
        far = out.crop((150, 70, 190, 95)).convert("L").getextrema()
        self.assertGreater(sharp[1] - sharp[0], 200)  # 注視点は縞がくっきり残る
        self.assertLess(far[1] - far[0], 80)           # 周辺は縞が溶けて灰色になる


@unittest.skipUnless(HAS_LEAN, "lean が見つからないため Lean のテストを省略")
class WikiSearchLogicTest(CliCase):
    """fixtures/wiki-search の論証（3役で書いた新形式）が門を通ること。"""

    def test_fixture_passes_gates(self):
        self.run_cli("new", "wiki-search", "--title", "テスト")
        self.advance_through("logic")
        for rel in ("07-logic/Argument.lean", "07-logic/Model.lean"):
            self.put(rel)
        r = self.run_cli("check", "logic")
        self.assertEqual(r.returncode, 0, r.stdout)
        report = json.loads((self.doc / "07-logic" / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(set(report["claims"]), {"C0", "C1", "C2", "C3"})
        self.assertNotIn("rule_", (FIXTURE / "07-logic" / "Argument.lean").read_text(encoding="utf-8"))
        self.assertTrue(report["rework"])  # 証拠のない【仮定】が手戻りの一覧に出る


class LeanSourceTest(unittest.TestCase):
    def test_parse_and_marks(self):
        src = leansrc.parse((MINI / "07-logic" / "Argument.lean").read_text(encoding="utf-8"))
        axioms = {d.name: d for d in src.by_kw("axiom")}
        self.assertEqual(axioms["passes"].full, "Mini.passes")
        self.assertEqual(leansrc.type_text(axioms["passes_consistent"]), "∀ s : Spec, passes s → ¬ contradictory s")
        mk = leansrc.axiom_marks(axioms["doc_miss_pos"].doc)
        self.assertEqual((mk.kind, mk.support, mk.confidence, mk.weak_point_facts), ("経験則", ["F2"], [0.8], ["F3"]))
        mk = leansrc.axiom_marks(axioms["lean_le_doc"].doc)
        self.assertEqual((mk.kind, mk.support, mk.needs_fact), ("仮定", [], True))
        tm = leansrc.theorem_marks("@beyond C0 強い版")
        self.assertEqual((tm.claims, tm.beyond), ([], ["C0"]))

    def test_comment_masking_and_binders(self):
        text = "/-- 説明 -/\naxiom f (x : Nat) {y : Nat} : x ≤ y -- 行末のコメント\n/- axiom g : True -/\n"
        src = leansrc.parse(text)
        self.assertEqual([d.name for d in src.by_kw("axiom")], ["f"])
        self.assertEqual(leansrc.type_text(src.decls[0]), "∀ (x : Nat) {y : Nat}, x ≤ y")
        self.assertEqual(src.decls[0].doc, "説明")

    def test_marks_only_at_line_start(self):
        mk = leansrc.axiom_marks("【仮定】F3 は @support に足せる（文中の語）\n@support なし（F3 は別の話）\n@confidence 0.5\n要ファクト: x")
        self.assertEqual((mk.support, mk.confidence), ([], [0.5]))
        tm = leansrc.theorem_marks("[不利] この定理は @claim C1 を弱める（文中の語）")
        self.assertEqual(tm.claims, [])

    def test_reviewer_and_branch_ids(self):
        mk = leansrc.axiom_marks("【経験則】\n@support F26a, F3\n@against F41\n@confidence 0.05\n"
                                 "@reviewer 0.3 ← 0.6 理由: 1周目\n@reviewer 0.05 ← 0.3 理由: F26a は述べていない")
        self.assertEqual((mk.support, mk.against), (["F3", "F26a"], ["F41"]))
        self.assertEqual([(r.value, r.original) for r in mk.reviewer], [(0.3, 0.6), (0.05, 0.3)])


@unittest.skipUnless(HAS_LEAN, "lean が見つからないため Lean のテストを省略")
class LogicGateTest(unittest.TestCase):
    """小さな論証（fixtures/logic-mini）を1か所ずつ壊して、門が止まることを確かめる。"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="cyrus-logic-"))
        shutil.copytree(MINI, self.tmp, dirs_exist_ok=True)
        self.arg = self.tmp / "07-logic" / "Argument.lean"
        self.model = self.tmp / "07-logic" / "Model.lean"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def edit(self, path: Path, old: str, new: str):
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def check(self):
        issues, report = leancheck.check(self.tmp)
        return issues, report

    def errors(self, issues):
        return [i for i in issues if i.severity == "error"]

    def test_mini_passes_all_gates(self):
        issues, report = self.check()
        self.assertEqual(self.errors(issues), [], "\n".join(i.format() for i in issues))
        self.assertEqual({k: v["confidence"] for k, v in report["claims"].items()}, {"C0": 0.05, "C1": 0.95, "C2": 0.75})
        self.assertEqual(report["axioms"]["lean_le_doc"]["confidence"], 0.05)   # @support のない【仮定】は案によらず 0.05
        self.assertEqual(report["axioms"]["doc_miss_pos"]["confidence"], 0.75)  # 案 0.8 と partially_verified 0.75 の小さいほう
        self.assertEqual(report["axioms"]["lean_miss_pos"]["confidence"], 0.05) # unverified の事実は 0.05
        self.assertEqual([r["axiom"] for r in report["rework"]], ["lean_le_doc", "lean_miss_pos"])
        self.assertEqual(report["witness"]["type_checked"], 8)
        self.assertEqual(report["atoms"]["side_only"], 1)  # lean_miss_pos は @beyond の定理だけが使う
        hints = json.loads((self.tmp / "07-logic" / "hints.json").read_text(encoding="utf-8"))["hints"]
        self.assertIn(("proof_is_axiom", "claim_C0_not_worse"), {(h["kind"], h["target"]) for h in hints})
        self.assertNotIn("hints", report)

    def test_empty_inductive(self):
        for p in (self.arg, self.model):
            self.edit(p, "/-- 仕様。 -/", "/-- 空の型。 -/\ninductive Nothing : Type\n\n/-- 仕様。 -/")
        self.assertIn("LG010", rules(self.errors(self.check()[0])))

    def test_conjoined_axiom(self):
        for p, body in ((self.arg, "axiom lean_miss_pos : 0 < missCount .lean"),
                        (self.model, "theorem lean_miss_pos : 0 < missCount .lean := by decide")):
            self.edit(p, body, body.replace("0 < missCount .lean", "0 < missCount .lean ∧ 0 < missCount .document"))
        errs = self.errors(self.check()[0])
        self.assertIn("LG007", rules(errs))

    def test_conjunction_under_implication_is_one_atom(self):
        extra = "\n/-- 【自明】通る仕様は通る。 -/\naxiom pass_pass : ∀ s : Spec, passes s → passes s ∧ passes s\n"
        self.edit(self.arg, "\n/-- @claim C1", extra + "\n/-- @claim C1")
        self.edit(self.model, "\n/-- @claim C1", extra.replace("axiom pass_pass : ∀ s : Spec, passes s → passes s ∧ passes s",
                                                          "theorem pass_pass : ∀ s : Spec, passes s → passes s ∧ passes s :=\n  fun _ h => ⟨h, h⟩") + "\n/-- @claim C1")
        issues, report = self.check()
        self.assertEqual(self.errors(issues), [], "\n".join(i.format() for i in issues))
        self.assertEqual(report["axioms"]["pass_pass"]["atoms"], 1)

    def test_reviewer_must_match_confidence(self):
        self.edit(self.arg, "@confidence 0.8\n", "@confidence 0.8\n@reviewer 0.3 ← 0.8 理由: F2 は1件だけ\n")
        self.assertIn("LG008", rules(self.errors(self.check()[0])))
        self.edit(self.arg, "@confidence 0.8\n", "@confidence 0.3\n")
        issues, report = self.check()
        self.assertEqual(self.errors(issues), [])  # Reviewer が docstring を書き換えても、証人は直さなくてよい
        self.assertEqual(report["axioms"]["doc_miss_pos"]["confidence"], 0.3)
        self.assertEqual(report["claims"]["C2"]["confidence"], 0.3)

    def test_reviewer_lines_chain(self):
        self.edit(self.arg, "@confidence 0.8\n", "@confidence 0.05\n@reviewer 0.3 ← 0.8 理由: 1周目\n@reviewer 0.05 ← 0.3 理由: 2周目\n")
        issues, report = self.check()
        self.assertEqual(self.errors(issues), [])
        self.assertEqual(report["axioms"]["doc_miss_pos"]["confidence"], 0.05)
        self.edit(self.arg, "@reviewer 0.05 ← 0.3", "@reviewer 0.05 ← 0.9")
        self.assertIn("LG008", rules(self.errors(self.check()[0])))

    def test_indented_declaration_is_rejected(self):
        self.edit(self.arg, "axiom lean_miss_pos : 0 < missCount .lean", "  axiom lean_miss_pos : 0 < missCount .lean")
        self.assertIn("LG012", rules(self.errors(self.check()[0])))

    def test_without_namespace(self):
        for p in (self.arg, self.model):
            self.edit(p, "namespace Mini\n", "")
            self.edit(p, "end Mini\n", "")
        issues, report = self.check()
        self.assertEqual(self.errors(issues), [], "\n".join(i.format() for i in issues))
        self.assertEqual(report["claims"]["C1"]["confidence"], 0.95)

    def test_reviewer_cannot_raise(self):
        self.edit(self.arg, "@confidence 0.8\n", "@confidence 0.9\n@reviewer 0.9 ← 0.8 理由: 上げたい\n")
        self.assertIn("LG008", rules(self.errors(self.check()[0])))

    def test_rejected_axiom_reappears(self):
        (self.tmp / "07-logic" / "rejected.json").write_text(json.dumps(
            {"rejected": [{"axiom": "lean_miss_pos", "reason": "誤り", "facts": ["F3"], "rejected_at": "2026-10-01"}]},
            ensure_ascii=False), encoding="utf-8")
        self.assertIn("LG009", rules(self.errors(self.check()[0])))

    def test_witness_type_mismatch(self):
        self.edit(self.model, "theorem lean_le_doc : missCount .lean ≤ missCount .document := by decide",
                  "theorem lean_le_doc : missCount .lean ≤ missCount .lean := Nat.le_refl _")
        self.assertIn("LG024", rules(self.errors(self.check()[0])))

    def test_witness_added_instance(self):
        self.edit(self.model, "def passes", "instance : Inhabited Spec := ⟨true⟩\n\ndef passes")
        self.assertIn("LG023", rules(self.errors(self.check()[0])))

    def test_witness_leftover_axiom_and_sorry(self):
        self.edit(self.model, "theorem lean_miss_pos : 0 < missCount .lean := by decide", "axiom lean_miss_pos : 0 < missCount .lean")
        self.assertIn("LG021", rules(self.errors(self.check()[0])))
        self.edit(self.model, "axiom lean_miss_pos : 0 < missCount .lean", "theorem lean_miss_pos : 0 < missCount .lean := sorry")
        errs = rules(self.errors(self.check()[0]))
        self.assertIn("LG001", errs)
        self.assertIn("LG026", errs)

    def test_witness_must_only_replace_axioms(self):
        self.edit(self.model, "theorem claim_C2_doc_miss : 0 < missCount .document :=\n  doc_miss_pos",
                  "theorem claim_C2_doc_miss : 0 < missCount .document := by decide")
        self.assertIn("LG022", rules(self.errors(self.check()[0])))

    def test_unknown_fact_id(self):
        self.edit(self.arg, "@support F2", "@support F2, F9")
        self.assertIn("LG004", rules(self.errors(self.check()[0])))
        self.edit(self.arg, "@support F2, F9", "@support F2\n@against F10")
        self.assertIn("LG004", rules(self.errors(self.check()[0])))

    def test_against_goes_to_rework(self):
        self.edit(self.arg, "@support F2\n", "@support F2\n@against F3\n")
        issues, report = self.check()
        self.assertEqual(self.errors(issues), [])
        rw = {r["axiom"]: r for r in report["rework"]}
        self.assertEqual(rw["doc_miss_pos"]["reasons"], ["against"])
        self.assertEqual(rw["doc_miss_pos"]["claims"], ["C2"])

    def test_form_of_relational_axioms(self):
        self.edit(self.arg, "要ファクト: 両方式で、伝え間違えた要件の数を数える。", "")
        self.edit(self.arg, "【実験】関門を通った", "関門を通った")
        self.edit(self.arg, "@support F3\n@confidence 0.9\n", "@support F3\n")
        errs = rules(self.errors(self.check()[0]))
        self.assertTrue({"LG003", "LG005", "LG006"} <= errs, errs)

    def test_banned_constructs_and_claim_coverage(self):
        self.edit(self.arg, "theorem claim_C0_not_worse : missCount .lean ≤ missCount .document :=\n  lean_le_doc",
                  "theorem claim_C0_not_worse : missCount .lean ≤ missCount .document := by\n  sorry")
        self.edit(self.arg, "/-- @claim C2 [件数]", "/-- [件数]")
        issues, report = self.check()
        errs = rules(self.errors(issues))
        self.assertIn("LG001", errs)
        self.assertIn("LG011", errs)
        self.assertEqual(report["claims"]["C0"]["confidence"], 0.0)  # 門でエラーでも値は出す
        self.edit(self.arg, "by\n  sorry", "by\n  native_decide")
        self.assertIn("LG001", rules(self.errors(self.check()[0])))

    def test_weak_premises(self):
        issues, report = self.check()
        weak = {w["axiom"]: w for w in report["weak_premises"]}
        self.assertEqual(set(weak), {"lean_le_doc", "doc_miss_pos"})  # C1（0.95）は言い切れるので出さない
        self.assertEqual(weak["lean_le_doc"]["claims"], ["C0"])
        self.assertIn("Lean 方式の伝え間違いは", weak["lean_le_doc"]["statement"])
        self.assertIn("数える", weak["lean_le_doc"]["needs_fact"])
        self.assertEqual(report["weak_premises"][0]["axiom"], "lean_le_doc")  # 確信度の低いほうが先

    def test_ledger_empty_side_is_a_hint(self):
        (self.tmp / "07-logic" / "ledger.json").write_text(json.dumps({
            "methods": ["lean", "document"],
            "rows": [{"layer": "決める", "failure": "取り違え", "quantity": "missCount",
                      "cells": {"lean": {"what": "関門の外で取り違える", "axioms": ["lean_miss_pos"]}},
                      "comparison": "Lean ≤ doc", "theorems": ["claim_C0_not_worse"]}]}, ensure_ascii=False), encoding="utf-8")
        issues, report = self.check()
        self.assertEqual(self.errors(issues), [])
        hints = json.loads((self.tmp / "07-logic" / "hints.json").read_text(encoding="utf-8"))["hints"]
        h = [x for x in hints if x["kind"] == "ledger_empty_side"]
        self.assertEqual(h[0]["detail"]["empty_methods"], ["document"])
        (self.tmp / "07-logic" / "ledger.json").write_text("{\"rows\": 1}", encoding="utf-8")
        self.assertIn("LG031", rules(self.check()[0]))

    def test_compile_error(self):
        self.edit(self.arg, "fun s h => passes_consistent s h", "fun s h => passes_consistent h s")
        issues, report = self.check()
        self.assertIn("LG002", rules(self.errors(issues)))
        self.assertIn("C2", report["claims"])  # エラーがあっても計算できるものは出す


@unittest.skipUnless(HAS_LEAN, "lean が見つからないため Lean のテストを省略")
class LogicScaffoldTest(CliCase):
    def test_scaffold_makes_three_files_without_rule(self):
        self.assertEqual(self.run_cli("new", "wiki-search", "--title", "テスト").returncode, 0)
        for rel in ("05-claims.json", "06-facts.json"):
            self.put(rel)
        r = self.run_cli("scaffold", "logic")
        self.assertIn("model-plan.md を作りました", r.stdout)
        arg = (self.doc / "07-logic" / "Argument.lean").read_text(encoding="utf-8")
        self.assertIn("namespace WikiSearch", arg)
        self.assertNotIn("rule_", arg)
        self.assertTrue((self.doc / "07-logic" / "Model.lean").exists())
        r = self.run_cli("check", "logic")
        self.assertEqual(r.returncode, 1)
        self.assertIn("LG011", r.stdout)       # 主張の定理がまだない
        self.assertNotIn("LG002", r.stdout)    # 雛形そのものはコンパイルできる


@unittest.skipUnless(HAS_LEAN, "lean が見つからないため Lean のテストを省略")
class LogicRoundTest(CliCase):
    def setUp(self):
        super().setUp()
        self.run_cli("new", "mini", "--title", "小さな論証")
        self.doc = self.tmp / "documents" / "mini"
        shutil.copytree(MINI, self.doc, dirs_exist_ok=True)
        self.logic = self.doc / "07-logic"

    def review(self, first_line: str):
        (self.logic / "review.md").write_text(first_line + "\n\n## 指摘\n", encoding="utf-8")

    def test_rounds_diff_and_stop(self):
        r = self.run_cli("logic-round", "close")
        self.assertEqual(r.returncode, 1)
        self.assertIn("LR001", r.stdout)  # review.md がない
        self.review("判定: 条件付き合格（高 1・中 0・低 2）")
        r = self.run_cli("logic-round", "close")
        self.assertEqual(r.returncode, 2, r.stdout)  # 続ける
        rd = json.loads((self.logic / "rounds" / "01" / "round.json").read_text(encoding="utf-8"))
        self.assertEqual((rd["high"], rd["stop"]), (1, False))
        self.assertTrue((self.logic / "rounds" / "01" / "Argument.lean").exists())

        # 2周目: Reviewer が doc_miss_pos を下げ、差分の設計書に1行
        arg = self.logic / "Argument.lean"
        arg.write_text(arg.read_text(encoding="utf-8").replace(
            "@confidence 0.8\n", "@confidence 0.3\n@reviewer 0.3 ← 0.8 理由: F2 は1チームだけ\n"), encoding="utf-8")
        (self.logic / "model-plan-delta.md").write_text(
            "# 差分の設計書\n\n| # | 変更 |\n|---|---|\n| 1 | `doc_miss_pos` の論拠を直す |\n| 2 | `lean_le_doc` を分ける |\n",
            encoding="utf-8")
        r = self.run_cli("logic-round", "diff")
        self.assertEqual(r.returncode, 0, r.stdout)
        d = (self.logic / "diff.md").read_text(encoding="utf-8")
        self.assertIn("| Argument.lean | `doc_miss_pos` | 変更（印） |", d)
        self.assertIn("**当たっていない**", d)  # 2行目は変更がない
        self.review("判定: 合格（高 0・中 0・低 1）")
        r = self.run_cli("logic-round", "close")
        self.assertEqual(r.returncode, 0, r.stdout)  # 高0・上がった主張なし → 止める
        self.assertIn("打ち切り", r.stdout)
        self.assertTrue((self.logic / "rounds" / "02" / "diff.md").exists())
        self.assertTrue((self.logic / "rounds" / "02" / "diff.patch").exists())
        self.assertFalse((self.logic / "diff.md").exists())

    def test_diff_flags_changed_axiom_keeping_reviewer(self):
        self.review("判定: 条件付き合格（高 1・中 0・低 0）")
        arg = self.logic / "Argument.lean"
        arg.write_text(arg.read_text(encoding="utf-8").replace(
            "@confidence 0.8\n", "@confidence 0.3\n@reviewer 0.3 ← 0.8 理由: F2 は1チームだけ\n"), encoding="utf-8")
        self.run_cli("logic-round", "close")
        self.assertIn("## 変更", (self.logic / "model-plan-delta.md").read_text(encoding="utf-8"))  # 次の周の雛形
        for p in (arg, self.logic / "Model.lean"):
            p.write_text(p.read_text(encoding="utf-8").replace("0 < missCount .document", "1 ≤ missCount .document"), encoding="utf-8")
        self.assertEqual(self.run_cli("logic-round", "diff").returncode, 0)
        d = (self.logic / "diff.md").read_text(encoding="utf-8")
        section = d.split("命題（型）が変わったのに名前が同じ公理")[1].split("## ")[0]
        self.assertIn("`doc_miss_pos`（`@reviewer` が残っている）", section)
        self.assertTrue((self.logic / "diff.patch").exists())

    def test_round_cap_resets_after_rework(self):
        self.review("判定: 差し戻し（高 1・中 0・低 0）")
        for _ in range(3):
            r = self.run_cli("logic-round", "close")
        self.assertEqual(r.returncode, 3)  # 3周で収まらない
        st = json.loads((self.doc / "state.json").read_text(encoding="utf-8"))
        st["stage"] = "logic"
        (self.doc / "state.json").write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(self.run_cli("back", "facts", "--reason", "ステージ7の手戻り").returncode, 0)
        st = json.loads((self.doc / "state.json").read_text(encoding="utf-8"))
        st["stage"] = "logic"  # ステージ6を終えて戻ってきた
        (self.doc / "state.json").write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
        r = self.run_cli("logic-round", "close")
        self.assertEqual(r.returncode, 2, r.stdout)  # 新しいループの1周目なので、ユーザーに見せる段階ではない
        self.assertIn("このループの 1 周目", r.stdout)

    def test_raised_claim_continues_and_escalates(self):
        self.review("判定: 条件付き合格（高 0・中 1・低 0）")
        arg = self.logic / "Argument.lean"
        original = arg.read_text(encoding="utf-8")
        arg.write_text(original.replace("@confidence 0.8\n", "@confidence 0.5\n"), encoding="utf-8")
        self.run_cli("logic-round", "close")        # 1周目: C2 = 0.5
        arg.write_text(original, encoding="utf-8")   # 2周目: C2 = 0.75（上がった）
        r = self.run_cli("logic-round", "close")
        self.assertEqual(r.returncode, 2)
        self.assertIn("C2 0.5→0.75", r.stdout)
        arg.write_text(original.replace("@support F2\n", "@support F1\n"), encoding="utf-8")  # 3周目: C2 = 0.8（また上がる）
        r = self.run_cli("logic-round", "close")
        self.assertEqual(r.returncode, 3)            # 3周で収まらない → ユーザーに見せる
        self.assertIn("ユーザー", r.stdout)


class HarnessConsistencyTest(unittest.TestCase):
    """ガイド・エージェント定義・CLI の約束（印とファイル名）が食い違っていないこと。"""
    APM = ROOT / ".apm"
    MARKS = ["@support", "@confidence", "@against", "@reviewer", "@restates", "@claim", "@beyond", "@baseline", "要ファクト"]
    FILES = ["model-plan.md", "model-plan-delta.md", "ledger.json", "Argument.lean", "Model.lean", "writer-note.md",
             "review.md", "report.json", "hints.json", "rejected.json", "diff.md"]

    def read(self, rel):
        return (self.APM / rel).read_text(encoding="utf-8")

    def test_guide_covers_marks_and_files(self):
        guide = self.read("skills/cyrus/stages/07-logic.md")
        for m in self.MARKS + self.FILES:
            self.assertIn(m, guide, m)
        self.assertNotIn("命題論理（∧, ∨, →, ¬）で十分", guide)
        for f in logicround.ROUND_FILES:
            self.assertIn(f, guide, f)

    def test_agents_exist_and_follow_roles(self):
        planner = self.read("agents/cyrus-logic-planner.agent.md")
        writer = self.read("agents/cyrus-lean-writer.agent.md")
        reviewer = self.read("agents/cyrus-logic-reviewer.agent.md")
        self.assertFalse((self.APM / "agents" / "cyrus-logic-critic.agent.md").exists())
        for m in ("@reviewer", "@against", "@restates", "hints.json", "review.md", "判定:"):
            self.assertIn(m, reviewer, m)
        for m in ("@claim", "@beyond", "@baseline", "writer-note.md", "Model.lean", "hints.json"):
            self.assertIn(m, writer, m)
        self.assertIn("読まないでください", writer)  # hints.json を Writer に見せない
        for m in ("model-plan.md", "model-plan-delta.md", "ledger.json"):
            self.assertIn(m, planner, m)
        skill = self.read("skills/cyrus/SKILL.md")
        for name in ("cyrus-logic-planner", "cyrus-lean-writer", "cyrus-logic-reviewer"):
            self.assertIn(name, skill)
            self.assertIn(name, self.read("skills/cyrus/stages/07-logic.md"))

    def test_verdict_format_matches_cli(self):
        reviewer = self.read("agents/cyrus-logic-reviewer.agent.md")
        line = re.search(r"^判定: .*$", reviewer, re.M).group(0)
        self.assertIsNotNone(logicround.VERDICT_RE.match(line))
        guide = self.read("skills/cyrus/stages/07-logic.md")
        self.assertIn("判定: 合格／条件付き合格／差し戻し（高 N・中 N・低 N）", guide)

    def test_no_old_format_left(self):
        for p in self.APM.rglob("*"):
            if p.is_file() and p.suffix in (".md", ".py", ".json"):
                t = p.read_text(encoding="utf-8")
                self.assertNotIn("cyrus-logic-critic", t, p)
                self.assertIsNone(re.search(r"\baxiom rule_|\bfact_F\d|claim_\w+_via_", t), p)

    def test_owner_principles_are_verbatim(self):
        text = self.read("skills/cyrus/references/owner-principles.md")
        self.assertIn("## 1. オーナーの原則（原文）", text)
        self.assertIn("「ちなみにconfidenceは単に「確信度」という意味だと思うので", text)
        self.assertIn("根拠にしてよい資料の範囲", text)


@unittest.skipUnless(HAS_LEAN, "lean が見つからないため Lean のテストを省略")
@unittest.skipUnless((PRIVATE / "expected.json").exists(),
                     "非公開の題材 tests/fixtures/private-subject/ がないため省略（公開リポジトリには含めない）")
class PrivateSubjectTest(CliCase):
    """非公開の題材（大きな論証）で、検査の値が expected.json の期待値と一致すること。"""

    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads((PRIVATE / "expected.json").read_text(encoding="utf-8"))
        cls.dir = Path(tempfile.mkdtemp(prefix="cyrus-subject-"))
        shutil.copytree(PRIVATE, cls.dir, dirs_exist_ok=True)
        cls.issues, cls.report = leancheck.check(cls.dir)
        cls.hints = json.loads((cls.dir / "07-logic" / "hints.json").read_text(encoding="utf-8"))["hints"]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def test_gate_errors(self):
        errs = [i for i in self.issues if i.severity == "error"]
        self.assertEqual(sorted(rules(errs)), self.expected["error_rules"], "\n".join(i.format() for i in errs[:5]))
        conj = [i.message.split(" ")[1] for i in errs if i.rule == "LG007"]
        c = self.expected["conjoined"]
        self.assertEqual(len(conj), c["count"])
        self.assertEqual(sum(1 for n in conj if n.endswith(c["suffix"])), c["suffix_count"])

    def test_witness_and_counts(self):
        w = self.report["witness"]
        self.assertTrue(w["compiled"])
        self.assertEqual((w["missing_lines"], w["nonstd"], w["type_checked"]), (0, {}, self.expected["witness_type_checked"]))
        self.assertEqual({k: self.report["counts"][k] for k in self.expected["counts"]}, self.expected["counts"])
        self.assertEqual(self.report["atoms"]["non_trivial"], self.expected["atoms_non_trivial"])

    def test_claim_confidences(self):
        self.assertEqual({k: v["confidence"] for k, v in self.report["claims"].items()}, self.expected["claims"])

    def test_rework_list(self):
        self.assertEqual(sorted(r["axiom"] for r in self.report["rework"]), self.expected["rework"])

    def test_hints_only_in_hints_json(self):
        for e in self.expected["proof_is_axiom"]:
            h = [x for x in self.hints if x["kind"] == "proof_is_axiom" and x["target"] == e["theorem"]]
            self.assertEqual(h[0]["detail"]["axiom"], e["axiom"])
            self.assertNotIn(e["theorem"], " ".join(i.message for i in self.issues))
        self.assertNotIn("hints", self.report)

    def test_cli_check_logic(self):
        self.assertEqual(self.run_cli("new", "subject", "--title", "題材").returncode, 0)
        shutil.copytree(PRIVATE, self.tmp / "documents" / "subject", dirs_exist_ok=True)
        r = self.run_cli("check", "logic")
        self.assertEqual(r.returncode, 1)
        for rule in self.expected["error_rules"]:
            self.assertIn(rule, r.stdout)
        r = self.run_cli("lean")
        main = next(iter(self.expected["claims"]))
        self.assertIn(f"{main}: {self.expected['claims'][main]:.2f}", r.stdout)
        self.assertIn("手戻りの一覧", r.stdout)


@unittest.skipUnless(HAS_LEAN, "lean が見つからないため全ステージのテストを省略")
class EndToEndTest(CliCase):
    def test_all_stages(self):
        self.assertEqual(self.run_cli("new", "wiki-search", "--title", "社内Wiki検索の刷新提案").returncode, 0)
        for key, rel in STAGE_FILES:
            st = json.loads((self.doc / "state.json").read_text())
            self.assertEqual(st["stage"], key)
            self.assertTrue((self.doc / rel).exists(), f"{rel} の雛形が作られていない")
            self.put(rel)
            for extra in EXTRA_FILES.get(key, []):
                self.put(extra)
            r = self.run_cli("check")
            self.assertEqual(r.returncode, 0, f"{key}: {r.stdout}")
            r = self.run_cli("advance", "--confirmed", "テスト承認", "--accept-warnings")
            self.assertEqual(r.returncode, 0, f"{key}: {r.stdout}")
        st = json.loads((self.doc / "state.json").read_text())
        self.assertEqual(st["stage"], "done")
        self.assertEqual(set(st["confirmations"]), {"intent", "reader", "claims", "storyline", "wording"})
        self.assertTrue((self.doc / "draft.v1.md").exists())


if __name__ == "__main__":
    unittest.main()
