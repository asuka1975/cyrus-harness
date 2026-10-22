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
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".apm" / "skills" / "cyrus" / "scripts"
CLI = SCRIPTS / "cyrus.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "wiki-search"
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True  # .apm/ に __pycache__ を作らない（apm install がそれを .claude/ に写してしまうため）

from cyruslib import jatext, leancheck, leansrc, lint, logicround, skim, visionreader, visual, wording  # noqa: E402
from cyruslib.reader import build_profile  # noqa: E402

HAS_LEAN = leancheck.find_lean() is not None
try:
    import PIL  # noqa: F401
    HAS_VISUAL = visual.find_chrome() is not None
except ImportError:
    HAS_VISUAL = False
YOMIYASU_CHECK = ROOT / ".claude" / "skills" / "yomiyasu" / "scripts" / "yomiyasu_check.py"  # apm install で入る依存
HAS_YOMIYASU = YOMIYASU_CHECK.exists()
CONSTRUCTIVISM = ROOT / ".claude" / "skills" / "constructivism"  # apm install で入る依存（ゲートは SKILL.md の有無だけを見る）
HAS_CONSTRUCTIVISM = (CONSTRUCTIVISM / "SKILL.md").exists()
VISUAL_PATTERNS = ROOT / ".apm" / "skills" / "visual-patterns"  # このパッケージのスキル（元を直接使う）
FAKE_AGY = Path(__file__).resolve().parent / "fakes" / "fake_agy.py"
FAKE_CLAUDE = Path(__file__).resolve().parent / "fakes" / "fake_claude.py"

MINI = Path(__file__).resolve().parent / "fixtures" / "logic-mini"
PRIVATE = Path(__file__).resolve().parent / "fixtures" / "private-subject"  # 公開しない題材（.gitignore）

# ステージの成果物のほかに、完了条件の検査で参照されるファイル
EXTRA_FILES = {"logic": ["07-logic/Model.lean"], "structure": ["08-structure.md"],
               "cogload": ["skim/visual/reader-result.json", "skim/figures/reader-result.json"]}

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
        self.assertEqual(jatext.sentence_style("索引を作り直します（図1）。"), "desumasu")  # 末尾の括弧の参照を外して判定する
        self.assertEqual(jatext.sentence_style("不満は解消しない（表1）。"), "plain")

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

    def test_kana_and_variants(self):
        issues = self.check("# t\n\n既に判断しました。サーバーとサーバを比べます。\n")
        self.assertIn("WD005", rules(issues))
        self.assertIn("WD007", rules(issues))

    def test_rewriting_is_left_to_yomiyasu(self):
        # 硬い漢語・冗長な表現・補助動詞の推敲は yomiyasu に任せ、辞書では拾わない
        issues = self.check("# t\n\n状況に鑑みて、確認することができます。確認を行って下さい。\n")
        self.assertNotIn("WD005", rules(issues))
        self.assertNotIn("WD006", rules(issues))


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
        constructivism = CONSTRUCTIVISM
        if not HAS_CONSTRUCTIVISM:  # 入っていなくても他のステージの検査を試せるよう、場所だけの代役を置く
            constructivism = self.tmp / "constructivism"
            constructivism.mkdir()
            (constructivism / "SKILL.md").write_text("stub\n", encoding="utf-8")
        self.env = dict(os.environ, CYRUS_ROOT=str(self.tmp), CYRUS_YOMIYASU=str(YOMIYASU_CHECK),
                        CYRUS_CONSTRUCTIVISM=str(constructivism), CYRUS_VISUAL_PATTERNS=str(VISUAL_PATTERNS))
        for k in ("CLAUDE_PROJECT_DIR", "CYRUS_CONFIG", "CYRUS_DOCS_DIR", "CYRUS_AGY", "CYRUS_AGY_MODEL"):  # 開発者の環境を持ち込まない
            self.env.pop(k, None)
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

    def yomiyasu_run(self):
        """ステージ13の推敲のあとに yomiyasu が残す検査の記録を、draft.md と final.md で作る。"""
        r = subprocess.run([sys.executable, str(YOMIYASU_CHECK), "run", "--source", str(self.doc / "draft.md"),
                            "--final", str(self.doc / "final.md")], capture_output=True, text=True, cwd=str(self.tmp),
                           timeout=300)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

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

    def put_cogload(self):
        for rel in ("12-cogload.json", *EXTRA_FILES["cogload"]):
            self.put(rel)

    def test_visual_test_required_and_tied_to_draft(self):
        self.advance_through("cogload")
        self.put_cogload()
        self.assertEqual(self.run_cli("check").returncode, 0)
        data = json.loads((FIXTURE / "12-cogload.json").read_text(encoding="utf-8"))
        del data["visual_test"]
        (self.doc / "12-cogload.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT140", self.run_cli("check").stdout)
        self.put("12-cogload.json")
        (self.doc / "skim" / "visual" / "reader-result.json").unlink()
        self.assertIn("GT142", self.run_cli("check").stdout)

    def test_visual_test_skip_follows_reader_config(self):
        self.advance_through("cogload")
        self.put_cogload()
        data = json.loads((FIXTURE / "12-cogload.json").read_text(encoding="utf-8"))
        data["visual_test"] = {"skipped_reason": "読み手のコマンドがない"}
        data["figure_test"] = {"skipped_reason": "読み手のコマンドがない"}
        (self.doc / "12-cogload.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        config = self.tmp / "cyrus.config.json"
        config.write_text(json.dumps({"vision": {"reader": {"command": ["cyrus-no-such-reader"]}}}), encoding="utf-8")
        r = self.run_cli("check")
        self.assertEqual(r.returncode, 0, r.stdout)  # 読み手のコマンドがなければ省略できる
        config.write_text("{", encoding="utf-8")
        self.assertIn("GT148", self.run_cli("check").stdout)  # 設定の誤りで省略をすり抜けない
        if HAS_VISUAL:
            config.write_text(json.dumps({"vision": {"reader": {"command": [sys.executable]}}}), encoding="utf-8")
            self.assertIn("GT141", self.run_cli("check").stdout)

    def test_skim_test_must_match_current_draft(self):
        self.advance_through("cogload")
        self.put_cogload()
        self.assertEqual(self.run_cli("check").returncode, 0)
        with open(self.doc / "draft.md", "a", encoding="utf-8") as f:
            f.write("\n追記した段落です。\n")
        out = self.run_cli("check").stdout
        self.assertIn("GT129", out)
        self.assertIn("GT143", out)
        self.assertIn("GT153", out)  # 図表の逆読みも、いまの原稿で行われている必要がある
        r = self.run_cli("skim")
        self.assertIn("原稿の指紋", r.stdout)
        self.assertTrue((self.doc / "skim" / "meta.json").exists())

    @unittest.skipUnless(HAS_YOMIYASU, "yomiyasu が入っていない（apm install）")
    def test_wording_requires_yomiyasu_record(self):
        self.advance_through("wording")
        self.put("final.md")
        self.assertIn("GT134", self.run_cli("check").stdout)  # yomiyasu の検査の記録がない
        self.yomiyasu_run()
        r = self.run_cli("check")
        self.assertNotIn("GT134", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)
        with open(self.doc / "final.md", "a", encoding="utf-8") as f:
            f.write("\n検査のあとで足した段落です。\n")
        out = self.run_cli("check").stdout
        self.assertIn("GT134", out)  # 検査したあとで本文が変わった
        self.assertIn("final_changed", out)

    def test_wording_without_yomiyasu(self):
        self.advance_through("wording")
        self.put("final.md")
        self.env["CYRUS_YOMIYASU"] = str(self.tmp / "no-such" / "yomiyasu_check.py")
        self.assertIn("GT133", self.run_cli("check").stdout)

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

    # ---- constructivism（ステージ8）と、その入力になる読者・主張の項目 ----

    def test_reader_purpose_and_claim_kind_required(self):
        self.advance_through("reader")
        data = json.loads((FIXTURE / "03-reader.json").read_text(encoding="utf-8"))
        data["purpose"] = "読む"
        (self.doc / "03-reader.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT029", self.run_cli("check").stdout)
        data["purpose"] = "decide"
        data["audience_scope"] = "社外"
        (self.doc / "03-reader.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("audience_scope", self.run_cli("check").stdout)
        data["audience_scope"] = "external"
        data["reading_context"]["reading_mode"] = "headline"  # 冒頭だけ読む決裁者
        data["reading_context"]["medium"] = "mail"
        (self.doc / "03-reader.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(self.run_cli("check").returncode, 0)
        self.assertEqual(self.run_cli("advance", "--confirmed", "x", "--accept-warnings").returncode, 0)
        self.put("04-analysis.md")
        self.assertEqual(self.run_cli("advance", "--accept-warnings").returncode, 0)
        data = json.loads((FIXTURE / "05-claims.json").read_text(encoding="utf-8"))
        del data["main_claim"]["message_kind"]
        (self.doc / "05-claims.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT043", self.run_cli("check").stdout)

    def test_structure_requires_constructivism_output(self):
        self.advance_through("structure")
        r = self.run_cli("scaffold", "structure", "--force")
        self.assertIn("08-structure.md を作りました", r.stdout)
        self.put("08-structure.json")
        self.assertIn("GT002", self.run_cli("check").stdout)  # 雛形の 08-structure.md は TODO のまま
        self.put("08-structure.md")
        self.assertEqual(self.run_cli("check").returncode, 0, self.run_cli("check").stdout)
        md = (self.doc / "08-structure.md").read_text(encoding="utf-8")
        (self.doc / "08-structure.md").write_text(md.replace("3. 置き換えで変わること（", "3. 置き換えると何が変わるか（"), encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertIn("GT073", out)  # 骨子の見出しが節にない
        self.assertIn("置き換えると何が変わるか", out)
        self.put("08-structure.md")
        data = json.loads((FIXTURE / "08-structure.json").read_text(encoding="utf-8"))
        data["sections"][1], data["sections"][2] = data["sections"][2], data["sections"][1]  # 骨子と順が違う
        (self.doc / "08-structure.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("骨子の順と違います", self.run_cli("check").stdout)
        data = json.loads((FIXTURE / "08-structure.json").read_text(encoding="utf-8"))
        data["style"] = "常体"  # 構成選択結果の文体（敬体）と違う
        (self.doc / "08-structure.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("constructivism の文体「敬体」", self.run_cli("check").stdout)
        data = json.loads((FIXTURE / "08-structure.json").read_text(encoding="utf-8"))
        data["style"] = "です・ます"
        del data["genre"]
        (self.doc / "08-structure.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(self.run_cli("check").stdout.count("GT074"), 2)
        self.put("08-structure.json")
        self.env["CYRUS_CONSTRUCTIVISM"] = str(self.tmp / "no-such")
        self.assertIn("GT071", self.run_cli("check").stdout)

    def test_storyline_pattern_follows_form_and_draft_follows_style(self):
        self.advance_through("storyline")
        data = json.loads((FIXTURE / "09-storyline.json").read_text(encoding="utf-8"))
        data["pattern"] = "SCQA"
        (self.doc / "09-storyline.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertIn("GT088", out)
        self.assertNotIn("[エラー]", out)
        self.put("09-storyline.json")
        self.assertEqual(self.run_cli("advance", "--confirmed", "x", "--accept-warnings").returncode, 0)
        self.put("10-detail.json")
        self.assertEqual(self.run_cli("advance", "--accept-warnings").returncode, 0)
        self.put("draft.md")
        st = json.loads((self.doc / "08-structure.json").read_text(encoding="utf-8"))
        st["style"] = "常体"
        (self.doc / "08-structure.json").write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT118", self.run_cli("check").stdout)  # 本文は敬体なのに設計は常体

    # ---- 図表（visual-patterns）: 設計・原稿・逆読み ----

    def test_detail_figure_spec_is_checked(self):
        self.advance_through("detail")
        data = json.loads((FIXTURE / "10-detail.json").read_text(encoding="utf-8"))
        fig = data["sections"][2]["blocks"][1]
        del fig["spec"]
        (self.doc / "10-detail.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT094", self.run_cli("check").stdout)
        data = json.loads((FIXTURE / "10-detail.json").read_text(encoding="utf-8"))
        fig = data["sections"][2]["blocks"][1]
        fig["spec"]["evidence"] = {"form": "quantity", "description": "値が2つ", "counts": {"values": 2}}
        (self.doc / "10-detail.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertIn("VP020", out)  # 手順2 の目安では文章
        self.assertIn("VP031", out)  # 量の根拠から実行順は選べない
        data = json.loads((FIXTURE / "10-detail.json").read_text(encoding="utf-8"))
        data["sections"][2]["blocks"][1]["spec"]["pattern"] = "flowchart"
        (self.doc / "10-detail.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("VP041", self.run_cli("check").stdout)  # 実行順の候補にない
        self.env["CYRUS_VISUAL_PATTERNS"] = str(self.tmp / "no-such")
        self.assertIn("GT101", self.run_cli("check").stdout)

    def test_draft_figures_must_match_plan(self):
        self.advance_through("writing")
        self.put("draft.md")
        self.assertEqual(self.run_cli("check").returncode, 0, self.run_cli("check").stdout)
        text = (FIXTURE / "draft.md").read_text(encoding="utf-8")
        (self.doc / "draft.md").write_text(text.replace("図1: 記事は保存のたびに", "図1: 仕組み。記事は保存のたびに").replace(
            "図1: 仕組み。記事は保存のたびに索引が作り直され、数秒で検索に出る。", "図1: 仕組み"), encoding="utf-8")
        self.assertIn("GT114", self.run_cli("check").stdout)  # キャプションに答えがない
        (self.doc / "draft.md").write_text(text + "\n| a | b |\n| --- | --- |\n| 1 | 2 |\n\n表1: 設計にない表\n", encoding="utf-8")
        self.assertIn("GT117", self.run_cli("check").stdout)  # 設計にない図表
        (self.doc / "draft.md").write_text(text.replace("```mermaid", "```text"), encoding="utf-8")
        self.assertIn("GT115", self.run_cli("check").stdout)  # Mermaid で描く設計なのにコードブロックがない
        (self.doc / "draft.md").write_text(text.replace("図1", "図9"), encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertIn("GT113", out)
        self.assertIn("GT117", out)
        # キャプションのない Mermaid の図、同じ番号のキャプション
        (self.doc / "draft.md").write_text(text + "\n```mermaid\nflowchart LR\n X-->Y\n```\n", encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertIn("キャプションのない Mermaid", out)
        (self.doc / "draft.md").write_text(text + "\n```mermaid\nflowchart LR\n X-->Y\n```\n\n図1: 別の図。\n", encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertIn("図1のキャプションが 2 つ", out)
        # 小数点は照合で落とさない
        (self.doc / "draft.md").write_text(text.replace("5秒以内", "0.5秒以内"), encoding="utf-8")
        self.assertIn("GT114", self.run_cli("check").stdout)
        # style を list にしても落ちない
        st = json.loads((self.doc / "08-structure.json").read_text(encoding="utf-8"))
        st["style"] = ["敬体"]
        (self.doc / "08-structure.json").write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
        r = self.run_cli("check", "structure")
        self.assertIn("GT074", r.stdout)
        self.assertNotIn("Traceback", r.stdout + r.stderr)

    def test_figure_test_required_and_judged(self):
        self.advance_through("cogload")
        self.put_cogload()
        self.assertEqual(self.run_cli("check").returncode, 0)
        data = json.loads((FIXTURE / "12-cogload.json").read_text(encoding="utf-8"))
        data["figure_test"]["figures"][0]["verdict"] = "misread"
        (self.doc / "12-cogload.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT155", self.run_cli("check").stdout)
        rec0 = self.doc / "skim" / "figures" / "reader-result.json"
        run0 = json.loads(rec0.read_text(encoding="utf-8"))
        run0["figures"][0]["prefers_text"] = "yes"  # 読み手が「文章のほうがよい」と答えた
        rec0.write_text(json.dumps(run0, ensure_ascii=False), encoding="utf-8")
        data["figure_test"]["figures"][0].update(verdict="match", prefers_text="yes", note="読み手は値が少ないと答えた")
        (self.doc / "12-cogload.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertIn("GT157", out)  # 削除の問い（判定者の note があっても、書き手の keep_reason がなければ出る）
        self.assertNotIn("[エラー]", out)
        data["figure_test"]["figures"][0]["keep_reason"] = "三者の順序は文章だと戻り読みが要る"
        (self.doc / "12-cogload.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertNotIn("GT157", self.run_cli("check").stdout)
        self.put("skim/figures/reader-result.json")
        del data["figure_test"]
        (self.doc / "12-cogload.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT150", self.run_cli("check").stdout)
        self.put("12-cogload.json")
        rec = self.doc / "skim" / "figures" / "reader-result.json"
        run = json.loads(rec.read_text(encoding="utf-8"))
        run["figures"] = []  # 読み手の回答が空
        rec.write_text(json.dumps(run, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT152", self.run_cli("check").stdout)
        self.put("skim/figures/reader-result.json")
        run = json.loads(rec.read_text(encoding="utf-8"))
        run["figures"][0]["prefers_text"] = "yes"  # 判定の prefers_text（no）が読み手の答えと違う
        rec.write_text(json.dumps(run, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT154", self.run_cli("check").stdout)
        self.put("skim/figures/reader-result.json")
        det = json.loads((self.doc / "10-detail.json").read_text(encoding="utf-8"))
        det["sections"][2]["blocks"][1]["spec"]["answer"] = "別の答えに差し替えた。"  # 逆読みのあとで設計の答えを変える
        (self.doc / "10-detail.json").write_text(json.dumps(det, ensure_ascii=False), encoding="utf-8")
        self.assertIn("GT153", self.run_cli("check").stdout)
        self.put("10-detail.json")
        rec.unlink()
        self.assertIn("GT152", self.run_cli("check").stdout)

    def test_enum_fields_with_wrong_types_report_instead_of_crashing(self):
        self.advance_through("reader")
        data = json.loads((FIXTURE / "03-reader.json").read_text(encoding="utf-8"))
        data["purpose"] = ["decide"]
        data["audience_scope"] = ["internal"]
        data["reading_context"]["medium"] = ["screen"]
        (self.doc / "03-reader.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        out = self.run_cli("check").stdout
        self.assertIn("GT029", out)
        self.assertIn("GT026", out)
        self.assertNotIn("Traceback", out)
        self.put("03-reader.json")
        self.assertEqual(self.run_cli("advance", "--confirmed", "x", "--accept-warnings").returncode, 0)
        self.put("04-analysis.md")
        self.assertEqual(self.run_cli("advance", "--accept-warnings").returncode, 0)
        data = json.loads((FIXTURE / "05-claims.json").read_text(encoding="utf-8"))
        data["main_claim"]["message_kind"] = ["proposal"]
        (self.doc / "05-claims.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        r = self.run_cli("check")
        self.assertIn("GT043", r.stdout)
        self.assertNotIn("Traceback", r.stdout + r.stderr)

    def test_cogload_scaffold_has_figure_test(self):
        self.advance_through("cogload")
        data = json.loads((self.doc / "12-cogload.json").read_text(encoding="utf-8"))
        self.assertEqual([f["label"] for f in data["figure_test"]["figures"]], ["図1"])


class FigureParseTest(unittest.TestCase):
    """原稿の図表とキャプションの読み取り、constructivism の骨子の読み取り。"""

    def test_caption_requires_separator(self):
        from cyruslib import figure
        self.assertIsNone(figure.CAPTION_RE.match("表 1 に費用を示します。"))   # 参照の文はキャプションではない
        self.assertIsNone(figure.CAPTION_RE.match("図1 を見てください。"))
        self.assertTrue(figure.CAPTION_RE.match("図１．答えの一文。"))
        self.assertTrue(figure.CAPTION_RE.match("表1: 答え"))

    def test_caption_above_figure_does_not_steal_next_block(self):
        from cyruslib import figure
        text = ("# t\n\n## a\n\n図1: 一つ目。\n\n```mermaid\nflowchart LR\n A-->B\n```\n\n図2: 二つ目。\n\n```mermaid\nflowchart LR\n C-->D\n```\n\n"
                "図 1 のとおりです。\n\n![図3: 三つ目](figures/fig-03.png)\n")
        found = figure.draft_figures(text)
        self.assertEqual([(f.label, f.source) for f in found], [("図1", "mermaid"), ("図2", "mermaid"), ("図3", "image")])
        self.assertIn("C-->D", found[1].src)
        self.assertEqual(found[2].src, "figures/fig-03.png")

    def test_norm_keeps_decimal_points_and_image_titles_are_parsed(self):
        from cyruslib import figure, mdparse
        self.assertNotEqual(figure._norm("差は1.5%である。"), figure._norm("差は15%である。"))
        self.assertEqual(figure._norm("答え（補足）。"), figure._norm("答え補足"))
        self.assertEqual(figure._norm("1,200 時間"), "1,200時間")
        blocks = mdparse.parse('# t\n\n![図1](figures/a.png "説明")\n\n![図2](<figures/b c.png>)\n')
        self.assertEqual([b.src for b in blocks if b.kind == "image"], ["figures/a.png", "figures/b c.png"])

    def test_outline_headings_tolerate_indent_and_nested_items(self):
        from cyruslib import gates
        md = ("## 構成選択結果\n- 文体：常体 標題案：x\n\n## 骨子\n   1. 件名（役割：対象＋行為（SCQA の S と C）／目安：1行）\n"
              "   2. 目的（役割：y）\n      - 入れる要素：3.1 キャッシュ、3.2 並列化\n   10. 添付資料（役割：z）\n\n## 構成チェック\n- [x] a\n")
        self.assertEqual(gates.outline_headings(md), ["件名", "目的", "添付資料"])
        self.assertEqual(gates.selection_style(md), "常体")


class FigureReadTest(CliCase):
    """図表だけを切り出して読み手に読ませる（PNG の図なら Chrome も網も要らない）。"""

    def setUp(self):
        super().setUp()
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow がない")
        self.run_cli("new", "demo", "--title", "demo")
        self.doc = self.tmp / "documents" / "demo"
        (self.doc / "figures").mkdir()
        Image.new("RGB", (120, 60), "white").save(self.doc / "figures" / "fig-01.png")
        (self.doc / "03-reader.json").write_text(json.dumps({"knowledge_level": "novice", "persona": {"role": "部長"}}), encoding="utf-8")
        spec = {"question": "どの区分が最も伸びたか", "answer": "B だけが五年前より増えた。", "reading": "lookup", "precision": "overview",
                "evidence": {"form": "quantity", "description": "3 区分 × 2 時点", "counts": {"values": 6, "groups": 3, "periods": 2}, "difference_matters": True},
                "intent": "time-series-change", "pattern": "bar-chart", "drawing": "B だけ色", "render": "vega-lite"}
        (self.doc / "10-detail.json").write_text(json.dumps({"target_length_chars": 100, "sections": [
            {"id": "S1", "heading": "伸び", "blocks": [{"kind": "figure", "plan": "x", "spec": spec}], "new_terms": [], "length_chars": 100}]},
            ensure_ascii=False), encoding="utf-8")
        (self.doc / "draft.md").write_text("# t\n\n## 伸び\n\n図1を見てください。\n\n![図1](figures/fig-01.png)\n\n図1: B だけが五年前より増えた。\n",
                                           encoding="utf-8")

    def test_read_with_fake_agy(self):
        self.env["CYRUS_AGY"] = str(FAKE_AGY)
        log = self.tmp / "agy.json"
        self.env["FAKE_AGY_LOG"] = str(log)
        r = self.run_cli("figure", "read")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        called = json.loads(log.read_text(encoding="utf-8"))
        self.assertEqual(called["problems"], [])
        self.assertEqual(called["files"], ["fig-01.png"])
        prompt = called["args"][called["args"].index("-p") + 1]
        self.assertIn("どの区分が最も伸びたか", prompt)       # 参照の図表には問いを先に示す
        self.assertNotIn("五年前より増えた", prompt)            # 答えは渡さない
        out = json.loads((self.doc / "skim" / "figures" / "reader-result.json").read_text(encoding="utf-8"))
        self.assertEqual(out["draft_hash"], skim.text_hash((self.doc / "draft.md").read_text(encoding="utf-8")))
        self.assertEqual(out["figures"][0]["label"], "図1")
        self.assertEqual(out["figures"][0]["prefers_text"], "no")

    def test_check_reports_missing_png(self):
        (self.doc / "figures" / "fig-01.png").unlink()
        out = self.run_cli("figure", "check").stdout
        self.assertIn("GT116", out)

    def test_swapped_png_invalidates_reading(self):
        """本文を変えずに PNG を差し替えても、逆読みの記録は失効する。"""
        from PIL import Image
        from cyruslib import figure
        from cyruslib.workspace import Workspace
        with mock.patch.dict(os.environ, {"CYRUS_ROOT": str(self.tmp), "CYRUS_VISUAL_PATTERNS": str(VISUAL_PATTERNS)}):
            ws = Workspace("demo")
            text = (self.doc / "draft.md").read_text(encoding="utf-8")
            detail = ws.read_json("10-detail.json")
            before = figure.figures_hash(ws, text, detail)
            self.assertEqual(figure.figures_hash(ws, text, detail), before)
            Image.new("RGB", (120, 60), "black").save(self.doc / "figures" / "fig-01.png")
            self.assertNotEqual(figure.figures_hash(ws, text, detail), before)
            # 記録の指紋が古ければ GT153
            rec = self.doc / "skim" / "figures" / "reader-result.json"
            rec.parent.mkdir(parents=True, exist_ok=True)
            h = skim.text_hash(text)
            rec.write_text(json.dumps({"draft_hash": h, "figures_hash": before,
                                       "figures": [{"label": "図1", "claim": "B が増えた", "prefers_text": "no"}]}), encoding="utf-8")
            ft = {"draft_hash": h, "figures": [{"label": "図1", "verdict": "match", "note": "", "prefers_text": "no"}]}
            self.assertIn("GT153", rules(figure.check_figure_test(ws, ft, figure.planned(detail), h, text, detail)))
            rec.write_text(json.dumps({"draft_hash": h, "figures_hash": figure.figures_hash(ws, text, detail),
                                       "figures": [{"label": "図1", "claim": "B が増えた", "prefers_text": "no"}]}), encoding="utf-8")
            self.assertEqual(rules(figure.check_figure_test(ws, ft, figure.planned(detail), h, text, detail)), set())

    def test_many_figures_are_read_in_batches(self):
        """読み手に一度に渡せる枚数を超えても、全部の図表に回答が付く。"""
        from PIL import Image
        spec = json.loads((self.doc / "10-detail.json").read_text(encoding="utf-8"))["sections"][0]["blocks"][0]["spec"]
        blocks, md = [], ["# t", "", "## 伸び", ""]
        for n in range(1, 14):
            Image.new("RGB", (60, 40), "white").save(self.doc / "figures" / f"fig-{n:02d}.png")
            s = dict(spec, answer=f"{n} 番目の答え。")
            blocks.append({"kind": "figure", "plan": "x", "spec": s})
            md += [f"図{n}を見てください。", "", f"![図{n}](figures/fig-{n:02d}.png)", "", f"図{n}: {n} 番目の答え。", ""]
        (self.doc / "10-detail.json").write_text(json.dumps({"target_length_chars": 100, "sections": [
            {"id": "S1", "heading": "伸び", "blocks": blocks, "new_terms": [], "length_chars": 100}]}, ensure_ascii=False), encoding="utf-8")
        (self.doc / "draft.md").write_text("\n".join(md), encoding="utf-8")
        self.env["CYRUS_AGY"] = str(FAKE_AGY)
        r = self.run_cli("figure", "read")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = json.loads((self.doc / "skim" / "figures" / "reader-result.json").read_text(encoding="utf-8"))
        self.assertEqual(out["batches"], 2)
        self.assertEqual(len(out["figures"]), 13)
        self.assertTrue(all(x["claim"] for x in out["figures"]))


class VisualPatternsTest(unittest.TestCase):
    """visual-patterns スキルの決定論的な部分（vp_figure.py）。"""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(VISUAL_PATTERNS / "scripts"))
        import vp_figure
        cls.vp = vp_figure
        cls.index = vp_figure.load_index()
        cls.routes = vp_figure.load_routes()
        cls.good = {"question": "書いた記事はどうやって検索に出るのか", "answer": "記事は保存のたびに索引が作り直され、数秒で検索に出る。",
                    "evidence": {"form": "parts-relations", "description": "主体 3、受け渡し 3", "counts": {"actors": 3, "steps": 3}},
                    "precision": "overview", "reading": "through", "intent": "step-order", "pattern": "sequence-diagram",
                    "drawing": "数秒の注釈", "render": "mermaid"}

    def warranted(self, **ev):
        return self.vp.figure_warranted(ev)[0]

    def test_step2_thresholds(self):
        self.assertFalse(self.warranted(form="quantity", counts={"values": 4}))
        self.assertTrue(self.warranted(form="quantity", counts={"values": 5}))
        self.assertFalse(self.warranted(form="quantity", counts={"groups": 2, "periods": 2}))
        self.assertTrue(self.warranted(form="quantity", counts={"groups": 2, "periods": 2}, difference_matters=True))
        self.assertFalse(self.warranted(form="items-attributes", counts={"items": 2, "categories": 2}))
        self.assertTrue(self.warranted(form="items-attributes", counts={"items": 2, "categories": 3}))
        self.assertTrue(self.warranted(form="items-attributes", counts={"items": 5, "categories": 2}))
        self.assertFalse(self.warranted(form="parts-relations", counts={"actors": 1, "steps": 5}))   # 一主体の直線
        self.assertFalse(self.warranted(form="parts-relations", counts={"actors": 2, "steps": 1}))   # 合わせて 3 つ
        self.assertTrue(self.warranted(form="parts-relations", counts={"actors": 2, "steps": 2}))
        self.assertTrue(self.warranted(form="parts-relations", counts={"actors": 1, "steps": 2}, features=["branching"]))
        self.assertTrue(self.warranted(form="parts-relations", counts={}, features=["loss-per-handoff"]))
        self.assertFalse(self.warranted(form="conditions", counts={"conditions": 1}))
        self.assertTrue(self.warranted(form="conditions", counts={"conditions": 2}))
        self.assertTrue(self.warranted(form="appearance"))

    def test_parse_range(self):
        self.assertEqual(self.vp.parse_range("2〜30"), (2, 30))
        self.assertEqual(self.vp.parse_range("〜30"), (None, 30))
        self.assertEqual(self.vp.parse_range("2〜20（線の本数）"), (2, 20))
        self.assertEqual(self.vp.parse_range("ふつう"), (None, None))

    def errors(self, spec, kind="figure", level="intermediate", chrome=True):
        return rules([i for i in self.vp.check_spec(spec, kind, self.index, self.routes, level, chrome) if i.severity == "error"])

    def test_check_spec(self):
        self.assertEqual(self.errors(self.good), set())
        self.assertIn("VP041", self.errors(dict(self.good, pattern="flowchart")))
        self.assertIn("VP044", self.errors(self.good, kind="table"))
        self.assertIn("VP060", self.errors(dict(self.good, intent_type="ない型")))
        self.assertIn("VP074", self.errors(dict(self.good, render="vega-lite")))  # 描ける手段と render の不一致
        self.assertIn("VP003", self.errors(dict(self.good, answer="一文目。二文目。")))
        q = dict(self.good, evidence={"form": "quantity", "description": "x", "counts": {"values": 3}})
        self.assertEqual({"VP020", "VP031"}, self.errors(q) & {"VP020", "VP031"})
        bar = {"question": "どれが多いか", "answer": "A が最も多い。", "precision": "overview", "reading": "through",
               "evidence": {"form": "quantity", "description": "5 項目の件数", "counts": {"values": 5, "items": 5}},
               "intent": "magnitude-comparison", "pattern": "bar-chart", "drawing": "A だけ色", "render": "vega-lite"}
        self.assertEqual(self.errors(bar), set())
        self.assertIn("VP072", self.errors(bar, chrome=False))  # Chrome がなければ Vega-Lite は PNG にできない
        warns = rules([i for i in self.vp.check_spec(dict(bar, answer="A が増加し、B は減った。"), "figure", self.index, self.routes)
                       if i.severity == "warn"])
        self.assertIn("VP004", warns)  # 述語が二つ
        warns = rules([i for i in self.vp.check_spec(self.good, "figure", self.index, self.routes, "novice") if i.severity == "warn"])
        self.assertIn("VP052", warns)  # 専門的な記法 × 初心者
        self.assertIn("VP053", self.errors(dict(bar, precision="exact")))  # 正確な値 × 概観のパターン
        # 目安に満たなくても、照合し直す必要があると判断したなら図表にできる（警告に下がる）
        few = dict(bar, evidence={"form": "quantity", "description": "4 項目", "counts": {"values": 4, "items": 4}})
        self.assertIn("VP020", self.errors(few))
        few["evidence"]["below_threshold_reason"] = "cross-reference"
        self.assertNotIn("VP020", self.errors(few))
        self.assertIn("VP020", rules([i for i in self.vp.check_spec(few, "figure", self.index, self.routes) if i.severity == "warn"]))
        # 引用の中の「？」では文を分けない
        quoted = dict(self.good, answer="「この操作でよいですか？」と確認する画面が表示される。")
        self.assertNotIn("VP003", self.errors(quoted))
        self.assertEqual(self.vp.split_sentences("A。「B？」とC。"), ["A。", "「B？」とC。"])
        # リストなどの型違いは診断になる
        self.assertIn("VP010", self.errors(dict(self.good, evidence={"form": [], "description": "x"})))
        self.assertIn("VP014", self.errors(dict(self.good, precision=["exact"])))
        sankey = dict(bar, evidence={"form": "quantity", "description": "経路ごとの量", "counts": {"values": 6}},
                      intent="flow", pattern="sankey", render="mermaid")
        issues = self.vp.check_spec(sankey, "figure", self.index, self.routes)
        self.assertFalse([i for i in issues if i.severity == "error"], issues)
        self.assertIn("ASCII", next(i.message for i in issues if i.rule == "VP073"))  # 描き方ごとの注意

    def test_index_matches_catalog(self):
        for iid, it in self.index["intents"].items():
            self.assertTrue(it["category"], iid)
            for c in it["candidates"]:
                self.assertIn(c["pattern"], self.index["patterns"], f"{iid}: {c['pattern']}")
        for pid, p in self.index["patterns"].items():
            if p.get("status") == "planned":
                continue
            self.assertTrue((VISUAL_PATTERNS / "references" / "catalog" / p["path"]).exists(), pid)
            self.assertIn(p["primary_intent"], self.index["intents"], pid)
        self.assertIn("入れ替わり", self.index["intent_types"])

    def test_cli_candidates(self):
        r = subprocess.run([sys.executable, str(VISUAL_PATTERNS / "scripts" / "vp_figure.py"), "candidates", "step-order"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("sequence-diagram", r.stdout)
        self.assertIn("when:", r.stdout)


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
        p = visionreader.build_prompt({"persona": {"role": "部長"}, "knowledge_level": "novice"}, ["page-01.png"], True, False)
        self.assertIn("部長", p)
        self.assertNotIn("/", p.replace("／", ""))


class VisionReaderConfigTest(unittest.TestCase):
    """読み手のコマンドを cyrus.config.json で変えられること（Chrome がなくても試せる部分）。"""

    RESULT = {
        "reader_summary": "要約", "main_point": "要点", "requested_action": "不明", "sections": [],
        "confusing_points": [], "visual_notes": {"stood_out": [], "missed_or_hidden": [], "layout_issues": []},
    }

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="cyrus-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        patcher = mock.patch.dict(os.environ, {"CYRUS_ROOT": str(self.tmp)})
        patcher.start()
        self.addCleanup(patcher.stop)
        for k in ("CYRUS_CONFIG", "CYRUS_AGY", "CYRUS_AGY_MODEL", "CLAUDE_PROJECT_DIR"):
            os.environ.pop(k, None)

    def write_config(self, reader):
        (self.tmp / "cyrus.config.json").write_text(json.dumps({"vision": {"reader": reader}}, ensure_ascii=False),
                                                     encoding="utf-8")

    def pages(self):
        d = self.tmp / "images"
        d.mkdir()
        for name in ("page-01.png", "page-02.png"):
            (d / name).write_bytes(b"\x89PNG\r\n\x1a\n")
        return sorted(d.iterdir())

    def test_default_is_agy(self):
        cfg = visionreader.load_config()
        self.assertIsNone(cfg.source)
        self.assertEqual(cfg.command[0], "agy")
        self.assertEqual(cfg.command[cfg.command.index("--mode") + 1], "plan")
        self.assertEqual(cfg.model, visionreader.DEFAULT_MODEL)

    def test_without_command_keeps_agy(self):
        self.write_config({"model": "gemini-x", "env": {"HTTPS_PROXY": "http://proxy:8080"}})
        cfg = visionreader.load_config()
        self.assertEqual(cfg.command[0], "agy")
        self.assertEqual((cfg.model, cfg.env), ("gemini-x", {"HTTPS_PROXY": "http://proxy:8080"}))

    def test_command_and_env_from_config(self):
        log = self.tmp / "reader.json"
        os.environ["CYRUS_TEST_HOME"] = "/home/someone"
        os.environ["FAKE_READER_DROP"] = "外から来た値"
        self.write_config({
            "name": "偽の Claude Code",
            "command": [sys.executable, str(FAKE_CLAUDE), "-p", "--output-format", "json", "--permission-mode", "plan"],
            "env": {"FAKE_READER_LOG": str(log), "FAKE_READER_TOKEN": "${CYRUS_TEST_HOME}/token",
                    "FAKE_READER_DROP": None},
        })
        out = visionreader.run(self.pages(), None, {"persona": {"role": "部長"}})
        called = json.loads(log.read_text(encoding="utf-8"))
        self.assertEqual(called["problems"], [])
        self.assertEqual(called["env"], {"FAKE_READER_TOKEN": "/home/someone/token", "FAKE_READER_DROP": None})
        self.assertIn("JSON スキーマ", called["prompt"])  # スキーマを渡さないコマンドには、回答の形をプロンプトで伝える
        self.assertEqual((out["reader"], out["model"]), ("偽の Claude Code", None))
        self.assertEqual(out["result"]["requested_action"], "予算の承認")
        self.assertEqual(out["meta"]["usage"], {"output_tokens": 1})

    def test_placeholders_and_model_override(self):
        log = self.tmp / "reader.json"
        self.write_config({
            "command": [sys.executable, str(FAKE_CLAUDE), "-p", "--json-schema", "{schema}", "--model", "{model}",
                        "--permission-mode", "plan"],
            "model": "sonnet",
            "env": {"FAKE_READER_LOG": str(log)},
        })
        out = visionreader.run(self.pages(), None, None, model="opus")
        args = json.loads(log.read_text(encoding="utf-8"))["args"]
        self.assertEqual(args[args.index("--model") + 1], "opus")  # --model が設定ファイルより優先
        self.assertEqual(json.loads(args[args.index("--json-schema") + 1]), visionreader.SCHEMA)
        self.assertEqual(out["model"], "opus")

    def test_bad_config(self):
        for reader, word in (
            ({"command": "claude -p"}, "command"),
            ({"command": ["claude", "{promt}"]}, "{promt}"),
            ({"enviroment": {}}, "enviroment"),
            ({"env": {"A": 1}}, "env"),
            ({"timeout": "60"}, "timeout"),
        ):
            with self.subTest(reader=reader):
                self.write_config(reader)
                with self.assertRaises(visionreader.ReaderConfigError) as cm:
                    visionreader.load_config()
                self.assertIn(word, str(cm.exception))
        (self.tmp / "cyrus.config.json").write_text("{", encoding="utf-8")
        self.assertRaises(visionreader.ReaderConfigError, visionreader.load_config)
        os.environ["CYRUS_CONFIG"] = str(self.tmp / "missing.json")
        self.assertRaises(visionreader.ReaderConfigError, visionreader.load_config)

    def test_model_required_by_placeholder(self):
        self.write_config({"command": ["claude", "--model", "{model}"]})
        cfg = visionreader.load_config()
        self.assertIsNone(cfg.model)
        with self.assertRaises(visionreader.ReaderConfigError):
            visionreader.build_command(cfg, {"model": ""})

    def test_parse_output_shapes(self):
        result = self.RESULT
        text = json.dumps(result, ensure_ascii=False)
        cases = {
            "agy": json.dumps({"status": "SUCCESS", "structured_output": result}),
            "agy の文字列の回答": json.dumps({"status": "SUCCESS", "response": text}),
            "Claude Code の文章の回答": json.dumps({"type": "result", "result": "読みました。\n```json\n" + text + "\n```"}),
            "回答の JSON だけ": text,
            "文章だけ": "前置きです。\n```json\n" + text + "\n```\n",
            "ログのあとの JSON の行": "読み込み中…\n" + json.dumps({"structured_output": result}),
        }
        for label, stdout in cases.items():
            with self.subTest(label):
                self.assertEqual(visionreader.parse_output(stdout)[0], result)
        with self.assertRaises(visionreader.ReaderUnavailable):
            visionreader.parse_output(json.dumps({"type": "result", "result": "画像を開けませんでした。"}))
        with self.assertRaises(visionreader.ReaderUnavailable):
            visionreader._validate({"reader_summary": "要約"})


class VisionConfigCliTest(CliCase):
    def test_show_command(self):
        (self.tmp / "cyrus.config.json").write_text(json.dumps({"vision": {"reader": {
            "name": "Claude Code", "command": ["claude", "-p", "--model", "{model}"], "model": "sonnet",
            "env": {"SECRET_TOKEN": "秘密の値", "CLAUDECODE": None}}}}, ensure_ascii=False), encoding="utf-8")
        r = self.run_cli("vision", "--show-command")
        self.assertEqual(r.returncode, 0, r.stderr)
        for word in ("Claude Code", "--model sonnet", "標準入力", "SECRET_TOKEN", "CLAUDECODE"):
            self.assertIn(word, r.stdout)
        self.assertNotIn("秘密の値", r.stdout)  # 環境変数の値は表示しない

    def test_bad_config_is_reported(self):
        (self.tmp / "cyrus.config.json").write_text('{"vision": {"reader": {"command": []}}}', encoding="utf-8")
        r = self.run_cli("vision", "--show-command")
        self.assertEqual(r.returncode, 1)
        self.assertIn("vision.reader.command", r.stderr)


@unittest.skipUnless(HAS_VISUAL, "Chrome か Pillow がないため画像のテストを省略")
class VisionTest(CliCase):
    def test_render_and_default_agy_reader(self):
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
        out = json.loads((self.doc / "skim" / "visual" / "reader-result.json").read_text(encoding="utf-8"))
        self.assertEqual(out["draft_hash"], skim.text_hash((self.doc / "draft.md").read_text(encoding="utf-8")))
        self.assertEqual(out["result"]["requested_action"], "予算の承認")
        self.assertEqual(out["reader"], "Gemini（agy）")
        self.assertTrue((self.doc / "skim" / "visual" / "page-01.png").exists())

    def test_render_and_configured_reader(self):
        log = self.tmp / "reader.json"
        self.env["CYRUS_MERMAID_JS"] = ""
        (self.tmp / "cyrus.config.json").write_text(json.dumps({"vision": {"reader": {
            "name": "偽の Claude Code",
            "command": [sys.executable, str(FAKE_CLAUDE), "-p", "--output-format", "json",
                        "--json-schema", "{schema}", "--permission-mode", "plan"],
            "env": {"FAKE_READER_LOG": str(log)}}}}, ensure_ascii=False), encoding="utf-8")
        self.run_cli("new", "wiki-search", "--title", "テスト")
        self.advance_through("cogload")
        r = self.run_cli("vision")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("偽の Claude Code に読ませています", r.stdout)
        called = json.loads(log.read_text(encoding="utf-8"))
        self.assertEqual(called["problems"], [])
        self.assertIn("overview.png", called["files"])
        out = json.loads((self.doc / "skim" / "visual" / "reader-result.json").read_text(encoding="utf-8"))
        self.assertEqual(out["reader"], "偽の Claude Code")
        self.assertEqual(out["result"]["visual_notes"]["missed_or_hidden"], ["費用と効果の節の約6000万円"])

    def test_figure_render_vega_lite_to_png(self):
        """figures/*.vl.json を Chrome で PNG にし、原稿の画像として扱えること（ライブラリは CDN から読むので網が要る）。"""
        import urllib.request
        try:
            urllib.request.urlopen("https://cdn.jsdelivr.net/npm/vega-embed@6", timeout=5).close()
        except Exception:
            self.skipTest("CDN（jsdelivr）に届かない")
        self.run_cli("new", "demo", "--title", "demo")
        self.doc = self.tmp / "documents" / "demo"
        (self.doc / "figures").mkdir()
        (self.doc / "figures" / "fig-01.vl.json").write_text(json.dumps({
            "data": {"values": [{"k": "A", "v": 5}, {"k": "B", "v": 3}]}, "mark": "bar",
            "encoding": {"x": {"field": "k", "type": "nominal"}, "y": {"field": "v", "type": "quantitative"}}}), encoding="utf-8")
        r = self.run_cli("figure", "render")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        png = self.doc / "figures" / "fig-01.png"
        self.assertTrue(png.exists())
        from PIL import Image
        im = Image.open(png).convert("L")
        self.assertLess(min(im.getdata()), 200)  # 何か描かれている
        html_ = visual.markdown_to_html("# t\n\n![図1](figures/fig-01.png)\n\n図1: A が多い。\n", base_dir=self.doc)
        self.assertIn('<img src="file://', html_)  # 画像のある原稿は、そのまま画面に描く

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

    def test_structure_and_figure_guides(self):
        for m in ("constructivism", "08-structure.md", "genre", "form", "style", "purpose", "message_kind"):
            self.assertIn(m, self.read("skills/cyrus/stages/08-structure.md"), m)
        for m in ("visual-patterns", "spec", "VP020", "answer", "evidence"):
            self.assertIn(m, self.read("skills/cyrus/stages/10-detail.md"), m)
        for m in ("cyrus figure check", "cyrus figure render", "figures/fig-NN.vl.json", "キャプション"):
            self.assertIn(m, self.read("skills/cyrus/stages/11-writing.md"), m)
        for m in ("cyrus figure read", "figure_test", "match / partial / mismatch / misread"):
            self.assertIn(m, self.read("skills/cyrus/stages/12-cogload.md"), m)
        self.assertIn("genre", self.read("skills/cyrus/stages/13-wording.md"))
        self.assertIn("purpose", self.read("skills/cyrus/stages/03-reader.md"))
        self.assertIn("message_kind", self.read("skills/cyrus/stages/05-claims.md"))
        skill = self.read("skills/cyrus/SKILL.md")
        for m in ("constructivism", "visual-patterns", "figure check"):
            self.assertIn(m, skill, m)
        judge = self.read("agents/cyrus-alignment-judge.agent.md")
        for m in ("misread", "figure_test", "spec.answer"):
            self.assertIn(m, judge, m)
        vp = self.read("skills/visual-patterns/SKILL.md")
        self.assertTrue(vp.startswith("---\nname: visual-patterns\n"))
        for m in ("手順2", "evidence", "scripts/vp_figure.py", "references/catalog/taxonomy.md"):
            self.assertIn(m, vp, m)

    def test_render_routes_cover_catalog(self):
        index = json.loads(self.read("skills/visual-patterns/data/index.json"))
        routes = json.loads(self.read("skills/visual-patterns/data/render-routes.json"))
        render_md = self.read("skills/visual-patterns/references/render.md")
        for pid, p in index["patterns"].items():
            if p.get("status") == "planned":
                continue
            self.assertIn(pid, routes, f"{pid} の描き方が render-routes.json にない")
            r = routes[pid]
            self.assertIn(r["route"], ("mermaid", "vega-lite", "markdown-table", "image", "none"), pid)
            self.assertIn(r["fidelity"], ("full", "approximate", "unavailable"), pid)
            for how in r.get("caveats") or {}:
                self.assertIn(how, [r["route"]] + list(r.get("alt") or []), f"{pid}: 使わない描き方 {how} の注意")
            self.assertEqual(render_md.count(f"\n### {pid}（"), 1, f"{pid} の描き方が render.md にない（または重複）")
            if r["route"] != "none":
                self.assertRegex(render_md, rf"### {re.escape(pid)}（[^\n]*\n- 描き方: ", pid)

    def test_catalog_snapshot_in_sync(self):
        src = Path(os.environ.get("VISUAL_PATTERNS_DIR", Path.home() / "work" / "ai-agent" / "visual-patterns"))
        if not (src / "taxonomy.md").exists():
            self.skipTest("図表パターンのカタログの元が手元にない")
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("PyYAML がない")
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "sync-visual-patterns.py"), "--source", str(src), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


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


@unittest.skipUnless(HAS_LEAN and HAS_YOMIYASU, "lean か yomiyasu が見つからないため全ステージのテストを省略")
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
            if key == "wording":
                self.yomiyasu_run()
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
