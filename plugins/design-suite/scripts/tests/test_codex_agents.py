"""Every Claude agent in agents/ has a Codex twin in codex-agents/, and the twins are current.
Run: python3 -m unittest discover -s scripts/tests"""
import importlib.util
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("gen_codex_agents", PACK / "scripts" / "gen_codex_agents.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

try:
    import tomllib
except ImportError:  # Python < 3.11
    tomllib = None


class CodexAgents(unittest.TestCase):
    def test_every_claude_agent_has_a_current_codex_twin(self):
        want = gen.expected(PACK)
        self.assertTrue(want, "no Claude agents found")
        for stem, text in want.items():
            target = PACK / "codex-agents" / f"{stem}.toml"
            self.assertTrue(target.is_file(), f"missing {target.name}")
            self.assertEqual(target.read_text(), text, f"{target.name} is stale: run scripts/gen_codex_agents.py")

    def test_no_codex_agent_without_a_claude_twin(self):
        claude = {p.stem for p in (PACK / "agents").glob("*.md")}
        codex = {p.stem for p in (PACK / "codex-agents").glob("*.toml")}
        self.assertEqual(codex - claude, set())

    @unittest.skipUnless(tomllib, "needs Python 3.11+ for tomllib")
    def test_files_parse_and_carry_exactly_three_keys(self):
        for path in sorted((PACK / "codex-agents").glob("*.toml")):
            data = tomllib.loads(path.read_text())
            self.assertEqual(sorted(data), ["description", "developer_instructions", "name"], path.name)
            self.assertEqual(data["name"], path.stem)
            self.assertTrue(data["description"] and data["developer_instructions"], path.name)

    def test_generator_check_flag_passes(self):
        import subprocess, sys
        r = subprocess.run([sys.executable, str(PACK / "scripts" / "gen_codex_agents.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
