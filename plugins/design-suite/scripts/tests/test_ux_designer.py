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
        for phrase in ("consult", "review", "duplicate", "not verified", "never create", "review only"):
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


if __name__ == "__main__":
    unittest.main()
