"""Read-only package checks and isolated local tool contract tests."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ToolTests(unittest.TestCase):
    def run_tool(self, script, *args, cwd=None):
        return subprocess.run(
            [sys.executable, '-B', str(script), *args], cwd=cwd,
            capture_output=True, text=True, check=False,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
        )

    def test_metrics_relocated_skill_works_from_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            skill = Path(folder) / 'copied-skill'
            shutil.copytree(ROOT / 'skills/pm-objectives', skill)
            result = self.run_tool(skill / 'scripts/metrics_lookup.py',
                                   '--category', 'aCtIvAtIoN', '--json', cwd=folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            records = json.loads(result.stdout)
            self.assertEqual(len(records), 7)
            self.assertEqual({row['category'] for row in records}, {'Activation'})
            self.assertEqual(len({row['id'] for row in records}), 7)

    def test_metrics_search_and_empty_results(self):
        script = ROOT / 'skills/pm-objectives/scripts/metrics_lookup.py'
        result = self.run_tool(script, 'lifetime', '--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        records = json.loads(result.stdout)
        self.assertTrue(any('Lifetime Value' in row['name'] for row in records))
        result = self.run_tool(script, '--category', 'No such category', '--json')
        self.assertEqual(json.loads(result.stdout), [])
        result = self.run_tool(script, 'not-a-metric-123')
        self.assertIn('No matching metrics', result.stdout)

    def test_digest_cli_rejects_invalid_input_without_mutation(self):
        script = ROOT / 'skills/pm-discovery/scripts/discovery_digest.py'
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'bad.jsonl'
            source.write_text('{not json}\n', encoding='utf-8')
            before = source.read_bytes()
            result = self.run_tool(script, str(source), cwd=folder)
            self.assertEqual(result.returncode, 2)
            self.assertIn('line 1', result.stderr)
            self.assertEqual(result.stdout, '')
            self.assertEqual(source.read_bytes(), before)
            self.assertEqual(list(Path(folder).iterdir()), [source])

    def test_digest_cli_complete_evidence(self):
        script = ROOT / 'skills/pm-discovery/scripts/discovery_digest.py'
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'evidence.jsonl'
            row = dict(id='E1', source_type='observation', status='observation',
                       summary='An observed task', source_ref='notes.md#E1',
                       date='2026-09-18', segment='pilot')
            source.write_text(json.dumps(row) + '\n', encoding='utf-8')
            result = self.run_tool(script, str(source), cwd=folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('| observation | 1 |', result.stdout)
            self.assertIn('No missing-provenance flags', result.stdout)
            self.assertIn('not unique people, prevalence or validation', result.stdout)


class PackageTests(unittest.TestCase):
    def test_exactly_fourteen_discoverable_skills_and_manifests(self):
        skills = list((ROOT / 'skills').rglob('SKILL.md'))
        self.assertEqual(len(skills), 14)
        for file in skills:
            text = file.read_text(encoding='utf-8')
            self.assertTrue(text.startswith('---\n'), file)
            self.assertIn('name: ' + file.parent.name + '\n', text)
            self.assertIn('description:', text)
            self.assertIn('project-local version', text)
        for host in ('.claude-plugin', '.codex-plugin'):
            data = json.loads((ROOT / host / 'plugin.json').read_text())
            self.assertEqual(data['name'], 'product-management')
            self.assertEqual(data['version'], '1.0.0')
            self.assertEqual(data['author']['name'], 'Stylus Nexus')
            self.assertEqual(data['license'], 'MIT AND CC-BY-SA-4.0')

    def test_relative_markdown_links_resolve_inside_plugin(self):
        for file in ROOT.rglob('*.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', file.read_text()):
                if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                resolved = (file.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT), (file, target))
                self.assertTrue(resolved.exists(), (file, target))

    def test_no_private_records_or_research_archives(self):
        # File format does not establish provenance. Original deliverables and
        # permitted adaptations may include PDFs, slides, sheets, and images.
        for file in ROOT.rglob('*'):
            self.assertNotEqual(file.suffix.lower(), '.pyc', file)
            self.assertNotIn(file.name, {'user-supplied', 'ProductCompass-Export',
                                        'backups', '__pycache__', 'verification'}, file)
            if file.suffix in {'.md', '.html', '.json'}:
                text = file.read_text(encoding='utf-8')
                for marker in ('/Users/', '/Applications/', 'resources/user-supplied',
                               'resources/ProductCompass-Export', 'text-extracted',
                               'scripts/import_assets.py'):
                    self.assertNotIn(marker, text, file)

    def test_offline_templates_and_attribution(self):
        for file in (ROOT / 'skills').rglob('*.html'):
            text = file.read_text(encoding='utf-8')
            self.assertIsNone(re.search(r'<(?:script|img|link)\b[^>]*(?:src|href)=[\"\']https?://', text), file)
            self.assertNotRegex(text, r'\b(?:fetch|XMLHttpRequest)\s*\(')
        for path in ('pm-canvas/templates/product-strategy-canvas.md',
                     'pm-value-proposition/templates/value-proposition.md'):
            self.assertIn('CC BY-SA 4.0', (ROOT / 'skills' / path).read_text())


if __name__ == '__main__':
    unittest.main()
