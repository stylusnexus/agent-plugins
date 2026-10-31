"""The direction-reviewer agent stays read-only, page-only and isolated from the builder, and is free of private terms.
Run: python3 -m unittest discover -s scripts/tests"""
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
AGENT = PACK / "agents" / "direction-reviewer.md"
AD = PACK / "skills" / "art-direction"


def split(text):
    _, front, body = text.split("---\n", 2)
    meta = {}
    for line in front.splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')
    return meta, body


class DirectionReviewer(unittest.TestCase):
    def setUp(self):
        self.meta, self.body = split(AGENT.read_text())

    def test_frontmatter_is_an_allowlist(self):
        self.assertEqual(self.meta["name"], "direction-reviewer")
        self.assertEqual(self.meta["model"], "inherit")
        self.assertEqual(self.meta["tools"], "Read")
        for key in ("disallowedTools", "memory", "permissionMode"):
            self.assertNotIn(key, self.meta)

    def test_body_has_required_rules(self):
        low = self.body.lower()
        for phrase in ("kind: page", "app screens not covered in v1", "no problems seen", "unable to verify",
                       "taste notes", "at most 7", "read only the review folder", "claim.md", "five-second",
                       "blocks", "weakens", "old page did better", "not shown", "do not read source", "hero", "finish"):
            self.assertIn(phrase, low)

    def test_body_has_no_private_terms(self):
        low = self.body.lower()
        for term in ("critforge", "stylus", "company os", "founder", "/users/", "/applications/", "~/"):
            self.assertNotIn(term, low)

    def test_codex_twin_exists(self):
        self.assertTrue((PACK / "codex-agents" / "direction-reviewer.toml").is_file())


class ReviewWiring(unittest.TestCase):
    def test_skill_points_at_reviewer_and_packet_reference(self):
        text = (AD / "SKILL.md").read_text()
        self.assertIn("direction-reviewer", text)
        self.assertIn("references/review.md", text)

    def test_review_reference_has_packet_contract(self):
        ref = AD / "references" / "review.md"
        self.assertTrue(ref.is_file())
        text = ref.read_text()
        for phrase in ("kind: page", "claim.md", "replies.md", ".taste-skill/review/", "fix first", "disputed",
                       "withheld", "inspect.mjs"):
            self.assertIn(phrase, text)

    def test_app_screens_are_not_wired(self):
        self.assertNotIn("direction-reviewer", (AD / "references" / "app-screens.md").read_text())


if __name__ == "__main__":
    unittest.main()
