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
                       "blocks", "weakens", "old page did better", "not shown", "do not read source", "hero", "finish",
                       "files.md", "laws.md", "scope: re-review", "fix first", "earlier-findings.md"):
            self.assertIn(phrase, low)

    def test_reads_manifest_first_then_in_order(self):
        low = self.body.lower()
        work = low[low.index("## order of work"):]
        pos = [work.index(x) for x in ("files.md", "screenshot", "five-second", "claim.md", "packet.md", "laws.md")]
        self.assertEqual(pos, sorted(pos))
        order = work[work.index("1. read `files.md`"):work.index("re-review:")]
        steps = [order.index(x) for x in ("1. read `files.md`", "2. then read `claim.md`", "3. judge")]
        self.assertEqual(steps, sorted(steps))
        self.assertLess(order.index("`claim.md`"), order.index("`packet.md`"))
        self.assertLess(order.index("`packet.md`"), order.index("`laws.md`"))
        self.assertLess(order.index("`laws.md`"), order.index("`earlier-findings.md`"))
        self.assertIn("`files.md` is missing, say so and stop", low)

    def test_earlier_findings_read_in_finish_and_re_review(self):
        low = self.body.lower()
        self.assertIn("finish mode and any re-review also hold `earlier-findings.md`", low)
        self.assertNotIn("finish mode also holds", low)

    def test_no_private_terms_in_whole_file(self):
        low = AGENT.read_text().lower()
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
                       "withheld", "inspect.mjs", "files.md", "laws.md", "earlier-findings.md", "before-",
                       "scope: re-review", "#153"):
            self.assertIn(phrase, text)
        self.assertIn("saves its reply as `.taste-skill/review/<n>/findings.md`", text)
        self.assertIn("findings.md", text.replace("earlier-findings.md", ""))

    def test_checkpoints_sit_between_the_right_steps(self):
        text = (AD / "SKILL.md").read_text()
        idx = {n: text.index(f"### {n}. ") for n in (6, 7, 8, 9, 10)}
        hero = text.index("**Hero checkpoint (pages only):**")
        finish = text.index("**Finish checkpoint (pages only).**")
        self.assertTrue(idx[6] < hero < idx[7])
        self.assertTrue(idx[8] < finish < idx[9])
        checklist = [l for l in text[idx[10]:].splitlines() if l.startswith("- Pages:")]
        self.assertEqual(len(checklist), 1)
        self.assertIn("replies.md", checklist[0])

    def test_app_screens_are_not_wired(self):
        self.assertNotIn("direction-reviewer", (AD / "references" / "app-screens.md").read_text())


if __name__ == "__main__":
    unittest.main()
