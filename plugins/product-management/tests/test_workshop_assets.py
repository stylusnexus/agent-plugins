"""Validate distributed workshop artifacts without optional authoring libraries."""
import csv
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile


ASSETS = Path(__file__).resolve().parents[1] / 'skills/pm-visuals/assets'
SLUGS = ('pareto-analysis', 'five-forces', 'outcome-roadmap', 'value-curve',
         'assumption-map', 'customer-journey', 'strategy-canvas',
         'value-proposition')


class WorkshopAssetsTests(unittest.TestCase):
    def test_manifest_and_pareto_data_match_distributed_assets(self):
        manifest = json.loads((ASSETS / 'manifest.json').read_text())
        self.assertEqual([row['id'] for row in manifest['assets']], list(SLUGS))
        for index, row in enumerate(manifest['assets']):
            self.assertEqual(row['combined_page'], index + 1)
            self.assertEqual(row['license'], 'CC-BY-SA-4.0' if index >= 6 else 'MIT')
            for output in row['outputs']:
                self.assertTrue((ASSETS / output).is_file(), output)
        with (ASSETS / 'pareto-fictional-data.csv').open(newline='') as source:
            rows = list(csv.DictReader(source))
        counts = sorted((float(row['count']) for row in rows), reverse=True)
        total, cumulative = sum(counts), 0
        text = ' '.join(ET.parse(ASSETS / 'pareto-analysis.svg').getroot().itertext())
        self.assertIn('Fictional', text)
        for count in counts:
            cumulative += count
            self.assertIn(f'{100 * cumulative / total:g}%', text)

    def test_individual_vectors_and_printable_pages_exist(self):
        for slug in SLUGS:
            with self.subTest(asset=slug):
                root = ET.parse(ASSETS / (slug + '.svg')).getroot()
                self.assertEqual(root.tag, '{http://www.w3.org/2000/svg}svg')
                self.assertTrue(root.get('viewBox'))
                self.assertFalse(root.findall('.//{http://www.w3.org/2000/svg}image'))
                content = (ASSETS / (slug + '.pdf')).read_bytes()
                self.assertTrue(content.startswith(b'%PDF-'))
                self.assertEqual(len(re.findall(rb'/Type\s*/Page\b', content)), 1)

    def test_combined_deck_has_eight_editable_slides(self):
        with ZipFile(ASSETS / 'workshop-toolkit.pptx') as deck:
            slides = sorted(name for name in deck.namelist()
                            if re.fullmatch(r'ppt/slides/slide\d+\.xml', name))
            self.assertEqual(len(slides), 8)
            for name in slides:
                root = ET.fromstring(deck.read(name))
                ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
                self.assertGreater(len(root.findall('.//a:t', ns)), 5, name)
                self.assertGreater(len(root.findall('.//p:sp', ns)), 5, name)
                self.assertFalse(root.findall('.//p:pic', ns), name)
        content = (ASSETS / 'workshop-toolkit.pdf').read_bytes()
        self.assertEqual(len(re.findall(rb'/Type\s*/Page\b', content)), 8)

    def test_adaptation_credits_travel_with_editable_assets(self):
        for slug in ('strategy-canvas', 'value-proposition'):
            text = ' '.join(ET.parse(ASSETS / (slug + '.svg')).getroot().itertext())
            self.assertIn('CC BY-SA', text)
            self.assertIn('Product Compass', text)
            if slug == 'value-proposition':
                self.assertIn('Behind Product Lines', text)
        with ZipFile(ASSETS / 'workshop-toolkit.pptx') as deck:
            for slide in (7, 8):
                root = ET.fromstring(deck.read(f'ppt/slides/slide{slide}.xml'))
                text = ' '.join(root.itertext())
                self.assertIn('CC BY-SA', text)
                self.assertIn('Product Compass', text)


if __name__ == '__main__':
    unittest.main()
