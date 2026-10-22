"""The ux-designer agent keeps its review-only guardrails and stays free of research artifacts and private terms.
Run: python3 -m unittest discover -s scripts/tests"""
import importlib.util
import re
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("gen_codex_agents", PACK / "scripts" / "gen_codex_agents.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

AGENT = PACK / "agents" / "ux-designer.md"


def split(text):
    _, front, body = text.split("---\n", 2)
    meta = {}
    for line in front.splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')
    return meta, body


class UxDesigner(unittest.TestCase):
    def setUp(self):
        self.meta, self.body = split(AGENT.read_text())

    def test_frontmatter_blocks_edits_and_inherits_tools(self):
        self.assertEqual(self.meta["name"], "ux-designer")
        self.assertEqual(self.meta["model"], "inherit")
        self.assertEqual(self.meta["disallowedTools"], "Write, Edit, MultiEdit, NotebookEdit")
        for key in ("tools", "memory", "permissionMode"):
            self.assertNotIn(key, self.meta)

    def test_body_has_required_rules(self):
        low = self.body.lower()
        for phrase in ("consult", "review", "duplicate", "not verified", "never create", "review only", "decline", "even when asked directly"):
            self.assertIn(phrase, low)

    def test_body_has_no_research_artifacts_or_private_terms(self):
        sentences = re.split(r"(?<=[.!?])\s+|\n", self.body)
        for term in ("persona", "journey map", "wireframe", "mockup"):
            for s in sentences:
                if term in s.lower():
                    self.assertTrue(s.strip().startswith("Do not produce"), f"{term!r} outside a 'Do not produce' sentence: {s}")
        low = self.body.lower()
        for term in ("critforge", "stylus", "company os", "founder", "/users/"):
            self.assertNotIn(term, low)

    def test_codex_twin_exists(self):
        self.assertTrue((PACK / "codex-agents" / "ux-designer.toml").is_file())


FIXTURES = PACK / "scripts" / "tests" / "fixtures" / "ux-designer"
CASES = ("nav-item-removed", "hover-flyout-hides-feature", "label-renamed-one-place",
         "popover-clipped-mobile", "breakpoint-hides-entry", "clean-copy-fix")


class Fixtures(unittest.TestCase):
    def check_hunks(self, name, text):
        hunks = re.split(r"^(?=@@ )", text, flags=re.M)[1:]
        self.assertTrue(hunks, f"{name}: no hunks")
        for h in hunks:
            head, *lines = h.splitlines()
            m = re.fullmatch(r"@@ -\d+,(\d+) \+\d+,(\d+) @@.*", head)
            self.assertTrue(m, f"{name}: bad hunk header {head!r}")
            old = sum(1 for l in lines if l[:1] in (" ", "-"))
            new = sum(1 for l in lines if l[:1] in (" ", "+"))
            self.assertEqual((old, new), (int(m.group(1)), int(m.group(2))), f"{name}: hunk counts wrong in {head}")

    def test_fixtures_are_complete(self):
        for case in CASES:
            self.assertTrue((FIXTURES / case).is_dir(), f"missing case {case}")
        for d in sorted(p for p in FIXTURES.iterdir() if p.is_dir()):
            diff = d / "change.diff"
            exp = d / "expected.md"
            self.assertTrue(diff.is_file() and diff.read_text().strip(), f"{d.name}: change.diff empty")
            self.assertTrue(exp.is_file() and exp.read_text().strip(), f"{d.name}: expected.md empty")
            self.check_hunks(d.name, diff.read_text())
            m = re.fullmatch(r"FINDINGS: (\d+)", exp.read_text().splitlines()[0])
            self.assertTrue(m, f"{d.name}: first line must be 'FINDINGS: <n>'")
            if d.name == "clean-copy-fix":
                self.assertEqual(int(m.group(1)), 0)
            else:
                self.assertGreaterEqual(int(m.group(1)), 1)


if __name__ == "__main__":
    unittest.main()
