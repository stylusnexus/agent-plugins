import importlib.util
import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('signals', Path(__file__).parents[1] / 'static_signals.py')
signals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(signals)

SHELL = """<!doctype html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="description" content="Track watering for large plant collections.">
<title>Plant Ledger</title>
<script type="module" src="/assets/app.js"></script></head>
<body><div id="root"></div></body></html>"""

RENDERED = """<!doctype html>
<html lang="en"><head>
<title>Plant Ledger - Watering schedules for plant collectors</title>
<meta name="description" content="Keep a 40-plant collection on schedule, room by room.">
<meta property="og:title" content="Plant Ledger">
<meta property="og:image" content="https://plantledger.example/card.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://plantledger.example/">
<script type="application/ld+json">{"@type": "SoftwareApplication"}</script>
</head><body>
<h1>Never lose a plant to a missed watering. <span>Even when you travel.</span></h1>
<p>Plant Ledger schedules watering room by room and shifts the plan with the season, so a collection of forty plants stays alive while you are away. Add a room, add a plant, and the calendar does the rest. Collectors use it to replace the repeating phone reminders that fire on the wrong day.</p>
<video src="/demo.mp4" muted autoplay><track kind="captions" src="/demo.vtt"></video>
<noscript>Turn on JavaScript to use the app.</noscript>
</body></html>"""


class AnalyseTests(unittest.TestCase):
    def test_script_only_page_is_flagged_as_a_js_shell(self):
        result = signals.analyse(SHELL, 'https://plantledger.example/', 200)
        self.assertTrue(result['js_shell'])
        self.assertIsNotNone(result['js_shell_note'])
        self.assertEqual(result['title'], 'Plant Ledger')
        self.assertEqual(result['meta_description'], 'Track watering for large plant collections.')
        self.assertEqual(result['h1'], [])
        self.assertEqual(result['open_graph'], {})
        self.assertEqual(result['json_ld_blocks'], 0)

    def test_server_rendered_page_is_not_a_shell(self):
        result = signals.analyse(RENDERED, 'https://plantledger.example/', 200)
        self.assertFalse(result['js_shell'])
        self.assertIsNone(result['js_shell_note'])
        self.assertGreater(result['visible_text_chars'], 200)
        self.assertEqual(result['h1'], ['Never lose a plant to a missed watering. Even when you travel.'])
        self.assertEqual(result['open_graph']['title'], 'Plant Ledger')
        self.assertEqual(result['twitter_card']['card'], 'summary_large_image')
        self.assertEqual(result['canonical'], 'https://plantledger.example/')
        self.assertEqual(result['json_ld_blocks'], 1)
        self.assertEqual(result['lang'], 'en')

    def test_title_and_scripts_do_not_count_as_visible_text(self):
        result = signals.analyse(SHELL)
        self.assertEqual(result['visible_text_chars'], 0)

    def test_noscript_text_is_counted_separately(self):
        result = signals.analyse(RENDERED)
        self.assertGreater(result['noscript_text_chars'], 0)

    def test_muted_video_and_caption_tracks_are_reported(self):
        result = signals.analyse(RENDERED)
        self.assertEqual(len(result['videos']), 1)
        self.assertTrue(result['videos'][0]['muted'])
        self.assertFalse(result['videos'][0]['controls'])
        self.assertEqual(result['caption_tracks'], 1)

    def test_unclosed_head_does_not_hide_the_body(self):
        html = '<html><head><title>T</title><body><h1>Hello there</h1><p>' + 'word ' * 60 + '</p></body></html>'
        result = signals.analyse(html)
        self.assertFalse(result['js_shell'])
        self.assertEqual(result['h1'], ['Hello there'])

    def test_domain_label_flags_digits_and_hyphens(self):
        self.assertTrue(signals.analyse(SHELL, 'https://www.plant-ledger.example/')['domain']['has_digits_or_hyphens'])
        plain = signals.analyse(SHELL, 'https://www.plantledger.example/')['domain']
        self.assertFalse(plain['has_digits_or_hyphens'])
        self.assertEqual(plain['name_label'], 'plantledger')


class CommandLineTests(unittest.TestCase):
    def run_main(self, argv):
        out = io.StringIO()
        with redirect_stdout(out):
            code = signals.main(argv)
        return code, json.loads(out.getvalue())

    def test_reads_a_saved_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'page.html'
            path.write_text(RENDERED)
            code, report = self.run_main(['--file', str(path)])
        self.assertEqual(code, 0)
        self.assertEqual(report['json_ld_blocks'], 1)

    def test_refuses_non_http_urls(self):
        for url in ('file:///etc/passwd', 'ftp://example.com/', 'javascript:alert(1)'):
            code, report = self.run_main([url])
            self.assertEqual(code, 1)
            self.assertIn('http', report['error'])

    def test_missing_file_is_a_reported_error(self):
        code, report = self.run_main(['--file', '/nonexistent/page.html'])
        self.assertEqual(code, 1)
        self.assertIn('error', report)

    def test_needs_exactly_one_source(self):
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            signals.main([])


if __name__ == '__main__':
    unittest.main()
