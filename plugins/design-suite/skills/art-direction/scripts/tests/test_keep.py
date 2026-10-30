"""Helpers behind keep.mjs: key normalisation and --drop parsing.  Run: python3 -m unittest discover -s scripts/tests

These tests call the real functions in lib/kept.mjs through Node. They are skipped without Node.
They do not start Chrome.
"""
import shutil
import subprocess
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
KEPT = SCRIPTS / "lib" / "kept.mjs"
NODE = shutil.which("node")


def run_node(code: str) -> str:
    prelude = f"import * as k from {KEPT.as_uri()!r};\n"
    result = subprocess.run(
        [NODE, "--input-type=module", "-e", prelude + code],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


@unittest.skipUnless(NODE, "node is required")
class KeptHelpers(unittest.TestCase):
    def test_norm_text_collapses_whitespace_and_nfc(self):
        out = run_node(r"console.log(JSON.stringify(k.normText('  Café \n\t  menu  ')))")
        self.assertEqual(out, '"Café menu"')

    def test_norm_path_same_origin_ignores_port_and_trailing_slash(self):
        out = run_node("console.log(k.normPath('http://localhost:4000/pricing/', 'http://localhost:3000/'))")
        self.assertEqual(out, "/pricing")

    def test_norm_path_keeps_search_and_hash(self):
        out = run_node("console.log(k.normPath('/a/b/?x=1#top', 'http://localhost:3000/'))")
        self.assertEqual(out, "/a/b?x=1#top")

    def test_norm_path_keeps_mailto_and_cross_origin_whole(self):
        out = run_node(
            "console.log(k.normPath('mailto:hi@example.com', 'http://localhost:3000/'));"
            "console.log(k.normPath('https://other.example/x/', 'http://localhost:3000/'));"
        )
        self.assertEqual(out.splitlines(), ["mailto:hi@example.com", "https://other.example/x/"])

    def test_norm_path_root_stays_slash(self):
        out = run_node("console.log(k.normPath('http://localhost:3000/', 'http://localhost:3000/'))")
        self.assertEqual(out, "/")

    def test_is_unstable_id(self):
        out = run_node(
            "console.log(JSON.stringify([':r1:', 'radix-:r2:-trigger', 'a3f09b1c7d', 'headlessui-menu-1',"
            " 'react-aria123', 'email', 'user_name'].map(k.isUnstableId)))"
        )
        self.assertEqual(out, "[true,true,true,true,true,false,false]")

    def test_parse_drop_splits_on_first_separator(self):
        out = run_node("console.log(JSON.stringify(k.parseDrop('href:/search?q=a=b -- retiring search')))")
        self.assertIn('"kind":"href"', out)
        self.assertIn('"value":"/search?q=a=b"', out)
        self.assertIn('"prefix":false', out)
        self.assertIn('"reason":"retiring search"', out)

    def test_parse_drop_rejects_short_reason(self):
        out = run_node("try { k.parseDrop('href:/x -- short'); console.log('no throw'); } catch (e) { console.log(e.message); }")
        self.assertTrue(out.startswith("usage:"), out)

    def test_parse_drop_rejects_unknown_kind(self):
        out = run_node("try { k.parseDrop('nope:/x -- long enough reason'); console.log('no throw'); } catch (e) { console.log(e.message); }")
        self.assertTrue(out.startswith("usage:"), out)

    def test_parse_drop_rejects_missing_separator(self):
        out = run_node("try { k.parseDrop('href:/x'); console.log('no throw'); } catch (e) { console.log(e.message); }")
        self.assertTrue(out.startswith("usage:"), out)

    def test_parse_drop_wildcard_sets_prefix(self):
        out = run_node("console.log(JSON.stringify(k.parseDrop('href:/blog/* -- retiring the blog')))")
        self.assertIn('"value":"/blog/"', out)
        self.assertIn('"prefix":true', out)

    def test_matches_drop_prefix_and_exact(self):
        out = run_node(
            "const p = k.parseDrop('href:/blog/* -- retiring the blog');"
            "const e = k.parseDrop('href:/blog -- retiring the blog');"
            "console.log(JSON.stringify(["
            "k.matchesDrop(p, {kind:'href', key:'href:/blog/post-1'}),"
            "k.matchesDrop(p, {kind:'form', key:'href:/blog/post-1'}),"
            "k.matchesDrop(e, {kind:'href', key:'href:/blog'}),"
            "k.matchesDrop(e, {kind:'href', key:'href:/blog/post-1'})]))"
        )
        self.assertEqual(out, "[true,false,true,false]")


if __name__ == "__main__":
    unittest.main()
