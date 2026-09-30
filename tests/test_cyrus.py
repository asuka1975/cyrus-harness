"""cyrus ハーネスのテスト。

実行: python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
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

from cyruslib import agyreader, jatext, leancheck, lint, skim, visual, wording  # noqa: E402
from cyruslib.reader import build_profile  # noqa: E402

HAS_LEAN = leancheck.find_lean() is not None
try:
    import PIL  # noqa: F401
    HAS_VISUAL = visual.find_chrome() is not None
except ImportError:
    HAS_VISUAL = False
FAKE_AGY = Path(__file__).resolve().parent / "fakes" / "fake_agy.py"

# ステージの成果物のほかに、完了条件の検査で参照されるファイル
EXTRA_FILES = {"cogload": ["skim/visual/gemini-reader.json"]}

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
class LeanTest(CliCase):
    def setUp(self):
        super().setUp()
        self.run_cli("new", "wiki-search", "--title", "テスト")
        self.advance_through("logic")

    def test_scaffold_compiles_but_needs_confidence(self):
        r = self.run_cli("lean")
        self.assertEqual(r.returncode, 1)
        self.assertIn("LG005", r.stdout)
        self.assertNotIn("LG009", r.stdout)  # 雛形そのものは Lean として正しい

    def test_fixture_confidence(self):
        self.put("07-logic/Argument.lean")
        r = self.run_cli("lean")
        self.assertEqual(r.returncode, 0, r.stdout)
        report = json.loads((self.doc / "07-logic" / "report.json").read_text(encoding="utf-8"))
        self.assertAlmostEqual(report["claims"]["C2"]["confidence"], 0.7)  # 仮定 0.7 が最弱
        self.assertEqual(report["claims"]["C0"]["weakest_link"], "fact_F4")
        self.assertEqual(report["claims"]["C0"]["hedge"]["level"], "moderate")

    def _write(self, extra: str, replace: tuple[str, str] | None = None):
        src = (FIXTURE / "07-logic" / "Argument.lean").read_text(encoding="utf-8")
        if replace:
            src = src.replace(*replace)
        (self.doc / "07-logic" / "Argument.lean").write_text(src + extra, encoding="utf-8")

    def test_claim_as_axiom_forbidden(self):
        self._write("\n/-- @confidence 0.9 ずる -/\naxiom rule_cheat : P_C0\n")
        self.assertIn("LG002", self.run_cli("lean").stdout)

    def test_sorry_detected(self):
        self._write("", ("theorem claim_C3 : P_C3 := rule_C3 ⟨fact_F4, fact_F1⟩", "theorem claim_C3 : P_C3 := sorry"))
        r = self.run_cli("lean")
        self.assertEqual(r.returncode, 1)
        self.assertIn("LG001", r.stdout)

    def test_type_error_reported(self):
        self._write("", ("rule_C1 ⟨fact_F1, fact_F2⟩", "rule_C1 ⟨fact_F2, fact_F1⟩"))
        self.assertIn("LG009", self.run_cli("lean").stdout)

    def test_independent_derivation_raises_confidence(self):
        extra = ("\n/-- @confidence 0.9 当日の記事が見つからない問題は、他部署でも同じ置き換えで解消した -/\n"
                 "axiom rule_C3_alt : P_C1 ∧ P_C2 → P_C3\n"
                 "theorem claim_C3_via_experience : P_C3 := rule_C3_alt ⟨claim_C1, claim_C2⟩\n")
        self._write(extra)
        self.assertEqual(self.run_cli("lean").returncode, 0)
        report = json.loads((self.doc / "07-logic" / "report.json").read_text(encoding="utf-8"))
        self.assertAlmostEqual(report["claims"]["C3"]["confidence"], 0.7)
        self.assertEqual(len(report["claims"]["C3"]["derivations"]), 2)


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
