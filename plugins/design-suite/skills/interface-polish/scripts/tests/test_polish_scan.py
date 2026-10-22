import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "polish_scan.py"
spec = importlib.util.spec_from_file_location("polish_scan", SCRIPT)
polish_scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(polish_scan)


def scan_css(text, name="a.css"):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / name
        path.write_text(text)
        return polish_scan.scan_file(path)[0]


def rules(hits):
    return {h["rule"] for h in hits}


class RuleTests(unittest.TestCase):
    def test_flags_transition_all(self):
        self.assertIn("transition-all", rules(scan_css(".a { transition: all 200ms; }")))

    def test_flags_removed_outline_without_replacement(self):
        self.assertIn("outline-removed", rules(scan_css("button { outline: none; }")))

    def test_removed_outline_with_focus_visible_replacement_is_ok(self):
        css = "button { outline: none; }\nbutton:focus-visible { box-shadow: 0 0 0 2px blue; }"
        self.assertNotIn("outline-removed", rules(scan_css(css)))

    def test_flags_heavy_black_shadow(self):
        self.assertIn("heavy-black-shadow", rules(scan_css(".a { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5); }")))

    def test_light_black_shadow_is_ok(self):
        self.assertNotIn("heavy-black-shadow", rules(scan_css(".a { box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); }")))

    def test_ignore_marker_on_the_line_silences_it(self):
        self.assertEqual(scan_css(".a { transition: all 1s; } /* polish-scan-ignore */"), [])

    def test_ignore_marker_on_the_line_above_silences_it(self):
        self.assertEqual(scan_css("/* polish-scan-ignore */\n.a { transition: all 1s; }"), [])

    def test_clean_input_has_no_hits(self):
        self.assertEqual(scan_css(".a { transition: color 150ms; }\n.a:focus-visible { outline: 2px solid blue; }"), [])


class PathTests(unittest.TestCase):
    def test_skip_dirs_are_relative_to_the_given_path(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "node_modules").mkdir()
            (root / "node_modules" / "x.css").write_text("a { transition: all 1s; }")
            (root / "src").mkdir()
            (root / "src" / "y.css").write_text("a { color: red; }")
            names = [f.name for f in polish_scan.files_under([root])]
            self.assertEqual(names, ["y.css"])
            # Scanning inside a skipped directory by name still works: the skip list is relative.
            inside = [f.name for f in polish_scan.files_under([root / "node_modules"])]
            self.assertEqual(inside, ["x.css"])


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)

    def test_missing_path_exits_2(self):
        self.assertEqual(self.run_cli("/no/such/path/for/polish-scan").returncode, 2)

    def test_fail_on_hits_exits_1_and_clean_exits_0(self):
        with tempfile.TemporaryDirectory() as folder:
            bad = Path(folder) / "bad.css"
            bad.write_text("a { transition: all 1s; }")
            self.assertEqual(self.run_cli(str(bad), "--fail-on-hits").returncode, 1)
            good = Path(folder) / "good.css"
            good.write_text("a { color: red; }")
            self.assertEqual(self.run_cli(str(good), "--fail-on-hits").returncode, 0)


if __name__ == "__main__":
    unittest.main()
