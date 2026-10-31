"""lint.mjs --allow waivers.  Run: python3 -m unittest discover -s scripts/tests

These tests run the real lint.mjs through Node on small fixture files in a temp folder. They are skipped
without Node. They do not start Chrome.
"""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
CLI = SCRIPTS / "lint.mjs"
NODE = shutil.which("node")

GRADIENT = '<div style="background: linear-gradient(red, blue)">x</div>\n'
NUMBERING = "<ul><li>01</li></ul>\n<h3>>01<</h3>\n<script>n.padStart(2, '0')</script>\n"
PLACEHOLDER = "<p>John Doe</p>\n"


@unittest.skipUnless(NODE, "node is required")
class LintWaivers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.dir = Path(self.tmp)

    def fixture(self, name, text):
        (self.dir / name).write_text(text, encoding="utf-8")

    def lint(self, *args):
        return subprocess.run(
            [NODE, str(CLI), *args], cwd=self.tmp, capture_output=True, text=True, timeout=30,
        )

    def test_gradient_fails_without_allow(self):
        self.fixture("a.html", GRADIENT)
        self.assertEqual(self.lint(".").returncode, 1)

    def test_allow_waives_fail_and_reports_it(self):
        self.fixture("a.html", GRADIENT)
        r = self.lint(".", "--allow", "gradient -- brand mark is a photo overlay")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("WAIVED", r.stdout)
        self.assertIn("[gradient] brand mark is a photo overlay  (1×)", r.stdout)
        self.assertIn("a.html:1", r.stdout)

    def test_json_carries_waived_and_drops_findings(self):
        self.fixture("a.html", GRADIENT)
        r = self.lint(".", "--json", "--allow", "gradient -- brand mark is a photo overlay")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["files"], 1)
        self.assertNotIn("gradient", [f["id"] for f in out["findings"]])
        w = out["waived"][0]
        self.assertEqual((w["id"], w["count"], w["reason"]), ("gradient", 1, "brand mark is a photo overlay"))
        self.assertEqual(len(w["findings"]), 1)

    def test_json_without_allow_has_empty_waived(self):
        self.fixture("a.html", GRADIENT)
        out = json.loads(self.lint(".", "--json").stdout)
        self.assertEqual(out["waived"], [])

    def test_short_reason_is_usage_error(self):
        self.fixture("a.html", GRADIENT)
        r = self.lint(".", "--allow", "gradient -- too short")
        self.assertEqual(r.returncode, 2)
        self.assertIn("10 characters", r.stderr)
        self.assertEqual(r.stdout, "")

    def test_missing_separator_is_usage_error(self):
        self.fixture("a.html", GRADIENT)
        r = self.lint(".", "--allow", "gradient because the brand mark is a photo")
        self.assertEqual(r.returncode, 2)
        self.assertIn('" -- "', r.stderr)

    def test_unknown_rule_lists_valid_ids(self):
        self.fixture("a.html", GRADIENT)
        r = self.lint(".", "--allow", "no-such-rule -- some long enough reason")
        self.assertEqual(r.returncode, 2)
        self.assertIn("no-such-rule", r.stderr)
        for rid in ("gradient", "numbering", "em-dash"):
            self.assertIn(rid, r.stderr)
        self.assertNotIn("placeholder-data", r.stderr)

    def test_allow_without_value_is_usage_error(self):
        self.fixture("a.html", GRADIENT)
        self.assertEqual(self.lint(".", "--allow").returncode, 2)

    def test_unused_waiver_is_a_note(self):
        self.fixture("a.html", "<p>hello</p>\n")
        r = self.lint(".", "--allow", "gradient -- brand mark is a photo overlay")
        self.assertEqual(r.returncode, 0)
        self.assertIn("[gradient] waiver matched nothing: brand mark is a photo overlay", r.stdout)

    def test_unused_waiver_in_json(self):
        self.fixture("a.html", "<p>hello</p>\n")
        out = json.loads(self.lint(".", "--json", "--allow", "gradient -- brand mark is a photo overlay").stdout)
        self.assertEqual(out["waived"], [{"id": "gradient", "reason": "brand mark is a photo overlay", "count": 0, "findings": []}])

    def test_numbering_waiver_covers_fail_and_warn(self):
        self.fixture("a.html", NUMBERING)
        before = json.loads(self.lint(".", "--json").stdout)
        levels = {f["level"] for f in before["findings"] if f["id"] == "numbering"}
        self.assertEqual(levels, {"FAIL", "WARN"})
        r = self.lint(".", "--json", "--allow", "numbering -- clock face and date labels")
        self.assertEqual(r.returncode, 0, r.stdout)
        out = json.loads(r.stdout)
        self.assertNotIn("numbering", [f["id"] for f in out["findings"]])
        self.assertEqual({f["level"] for f in out["waived"][0]["findings"]}, {"FAIL", "WARN"})

    def test_reason_with_separator_and_equals_is_kept_whole(self):
        self.fixture("a.html", GRADIENT)
        reason = "photo overlay -- see a=b in design notes"
        out = json.loads(self.lint(".", "--json", "--allow", f"gradient -- {reason}").stdout)
        self.assertEqual(out["waived"][0]["reason"], reason)

    def test_flag_value_is_not_a_path(self):
        self.fixture("a.html", GRADIENT)
        spec = "gradient -- brand mark is a photo overlay"
        before = self.lint(".", "--json", "--allow", spec)
        after = self.lint("--allow", spec, ".", "--json")
        self.assertNotEqual(before.returncode, 2, before.stderr)
        self.assertEqual(before.returncode, after.returncode)
        self.assertEqual(before.stdout, after.stdout)

    def test_app_only_id_needs_app_mode(self):
        self.fixture("a.html", PLACEHOLDER)
        spec = "placeholder-data -- seeded demo names stay"
        self.assertEqual(self.lint(".", "--allow", spec).returncode, 2)
        r = self.lint(".", "--app", "--allow", spec)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("[placeholder-data] seeded demo names stay  (1×)", r.stdout)

    def test_two_allows_both_apply(self):
        self.fixture("a.html", GRADIENT + "<p>unlock</p>\n<p>lorem ipsum</p>\n")
        r = self.lint(".", "--json", "--allow", "gradient -- brand mark is a photo overlay",
                      "--allow", "lorem -- quoting the font specimen")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual([w["id"] for w in json.loads(r.stdout)["waived"]], ["gradient", "lorem"])

    def test_overflow_line_after_six_locations(self):
        self.fixture("a.html", GRADIENT * 8)
        r = self.lint(".", "--allow", "gradient -- brand mark is a photo overlay")
        self.assertIn("(8×)", r.stdout)
        self.assertIn("… 2 more", r.stdout)


if __name__ == "__main__":
    unittest.main()
