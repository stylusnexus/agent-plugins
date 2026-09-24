import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('digest', Path(__file__).parents[1] / 'discovery_digest.py')
digest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(digest)

class DigestTests(unittest.TestCase):
    def parse(self, rows):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / 'input.jsonl'
            p.write_text('\n'.join(json.dumps(r) for r in rows))
            return digest.read_records(p)

    def test_provenance_and_safe_output(self):
        row = dict(id='E1', source_type='support_ticket', status='reported', summary='<script>x</script>|line\nbreak')
        report = digest.render(self.parse([row]))
        self.assertIn('missing source_ref, date, segment', report)
        self.assertNotIn('<script>', report)
        self.assertIn('&#124;', report)
        self.assertIn('| customer_interview | 0 |', report)

    def test_synthetic_cannot_masquerade_as_observation(self):
        row = dict(id='S1', source_type='synthetic_research', status='observation', summary='Simulated view')
        with self.assertRaisesRegex(ValueError, 'synthetic status'):
            self.parse([row])
        row['status'] = 'synthetic'
        self.assertIn('never customer evidence', digest.render(self.parse([row])))

    def test_duplicate_ids_invalid_date_and_unknown_source(self):
        row = dict(id='E1', source_type='survey', status='reported', summary='Response')
        with self.assertRaisesRegex(ValueError, 'duplicate id'):
            self.parse([row, row])
        with self.assertRaises(ValueError):
            self.parse([dict(row, date='2026-02-30')])
        with self.assertRaisesRegex(ValueError, 'unrecognized'):
            self.parse([dict(row, source_type='invented')])

if __name__ == '__main__':
    unittest.main()
