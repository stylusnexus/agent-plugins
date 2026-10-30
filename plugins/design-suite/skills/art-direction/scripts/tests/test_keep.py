"""Helpers behind keep.mjs: key normalisation and --drop parsing.  Run: python3 -m unittest discover -s scripts/tests

These tests call the real functions in lib/kept.mjs through Node. They are skipped without Node.
They do not start Chrome.
"""
import json
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


def page(items, final="/", status=200):
    return {"finalPath": final, "status": status, "skippedButtons": 0, "items": items}


def rec(pages):
    return {"version": 1, "width": 1280, "at": "2026-10-30T00:00:00Z", "pages": pages}


def it(kind, key, label=None, visible=True):
    d = {"kind": kind, "key": key, "visible": visible}
    if label is not None:
        d["label"] = label
    return d


def compare(before, after, drops=()):
    code = (
        f"const d = {json.dumps(list(drops))}.map(k.parseDrop);"
        f"console.log(JSON.stringify(k.compare({json.dumps(before)}, {json.dumps(after)}, d)));"
    )
    return json.loads(run_node(code))


@unittest.skipUnless(NODE, "node is required")
class KeptCompare(unittest.TestCase):
    def test_reorder_and_additions_pass(self):
        before = rec({"/": page([it("href", "/a"), it("href", "/b")])})
        after = rec({"/": page([it("href", "/new"), it("href", "/b"), it("href", "/a")])})
        self.assertEqual(compare(before, after)["findings"], [])

    def test_lost_link_fails_with_drop_hint(self):
        before = rec({"/": page([it("href", "/blog"), it("href", "/a")])})
        after = rec({"/": page([it("href", "/a")])})
        f = compare(before, after)["findings"]
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["level"], "FAIL")
        self.assertEqual(f[0]["kind"], "href")
        self.assertEqual(f[0]["key"], "/blog")
        self.assertEqual(f[0]["page"], "/")
        self.assertEqual(f[0]["drop"], "href:/blog -- <reason>")

    def test_changed_href_is_one_fail_with_both_values(self):
        before = rec({"/": page([it("href", "/pricing", "Pricing")])})
        after = rec({"/": page([it("href", "/plans", "Pricing")])})
        f = compare(before, after)["findings"]
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["level"], "FAIL")
        self.assertIn("changed", f[0]["message"])
        self.assertIn("/pricing", f[0]["message"])
        self.assertIn("/plans", f[0]["message"])

    def test_lost_field_and_hook_fail(self):
        before = rec({"/": page([it("field", "email"), it("hook", "data-testid=cta")])})
        after = rec({"/": page([])})
        f = compare(before, after)["findings"]
        self.assertEqual(sorted((x["kind"], x["level"]) for x in f), [("field", "FAIL"), ("hook", "FAIL")])

    def test_lost_heading_is_warn(self):
        before = rec({"/": page([it("heading", "Welcome")])})
        after = rec({"/": page([])})
        f = compare(before, after)["findings"]
        self.assertEqual([(x["kind"], x["level"]) for x in f], [("heading", "WARN")])

    def test_visible_to_hidden_is_warn_not_fail(self):
        before = rec({"/": page([it("button", "Menu", visible=True)])})
        after = rec({"/": page([it("button", "Menu", visible=False)])})
        f = compare(before, after)["findings"]
        self.assertEqual([(x["kind"], x["level"]) for x in f], [("button", "WARN")])

    def test_hidden_item_missing_after_still_fails(self):
        before = rec({"/": page([it("button", "Menu", visible=False)])})
        after = rec({"/": page([])})
        f = compare(before, after)["findings"]
        self.assertEqual([(x["kind"], x["level"]) for x in f], [("button", "FAIL")])

    def test_missing_page_fails_and_can_be_dropped(self):
        before = rec({"/": page([it("href", "/a")]), "/pricing": page([it("href", "/b")])})
        after = rec({"/": page([it("href", "/a")])})
        f = compare(before, after)["findings"]
        self.assertEqual([(x["level"], x["kind"], x["key"]) for x in f], [("FAIL", "page", "/pricing")])
        r = compare(before, after, ["page:/pricing -- folded into home"])
        self.assertEqual(r["findings"], [])
        self.assertEqual(r["dropped"][0]["kind"], "page")
        self.assertEqual(r["dropped"][0]["reason"], "folded into home")

    def test_status_404_fails_page(self):
        before = rec({"/x": page([it("href", "/a")], final="/x")})
        after = rec({"/x": page([], final="/x", status=404)})
        f = compare(before, after)["findings"]
        self.assertEqual([(x["level"], x["kind"], x["page"]) for x in f], [("FAIL", "page", "/x")])

    def test_redirect_to_other_path_warns(self):
        before = rec({"/x": page([it("href", "/a")], final="/x")})
        after = rec({"/x": page([it("href", "/a")], final="/y")})
        f = compare(before, after)["findings"]
        self.assertEqual([(x["level"], x["kind"]) for x in f], [("WARN", "page")])

    def test_empty_record_warns_nothing_recorded(self):
        before = rec({"/": page([])})
        after = rec({"/": page([it("href", "/a")])})
        f = compare(before, after)["findings"]
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["level"], "WARN")
        self.assertIn("nothing recorded", f[0]["message"])

    def test_no_pages_at_all_warns_nothing_recorded(self):
        f = compare(rec({}), rec({}))["findings"]
        self.assertEqual(len(f), 1)
        self.assertIn("nothing recorded", f[0]["message"])

    def test_prefix_drop_covers_many(self):
        before = rec({"/": page([it("href", "/blog/a"), it("href", "/blog/b"), it("href", "/c")])})
        after = rec({"/": page([])})
        r = compare(before, after, ["href:/blog/* -- retiring the blog"])
        self.assertEqual([x["key"] for x in r["findings"]], ["/c"])
        self.assertEqual(len(r["dropped"]), 2)

    def test_drop_values_are_normalised_like_keys(self):
        before = rec({"/": page([it("button", "Sign up"), it("href", "/pricing")])})
        after = rec({"/": page([])})
        r = compare(before, after, ["button:Sign  up -- moved into the menu", "href:/pricing/ -- plans page retired"])
        self.assertEqual(r["findings"], [])
        self.assertEqual(r["unmatchedDrops"], [])
        self.assertEqual(len(r["dropped"]), 2)

    def test_unmatched_drop_is_reported(self):
        before = rec({"/": page([it("href", "/a")])})
        after = rec({"/": page([it("href", "/a")])})
        r = compare(before, after, ["href:/typo -- never existed here"])
        self.assertEqual(r["unmatchedDrops"], ["href:/typo -- never existed here"])

    def test_counts_shape(self):
        before = rec({"/": page([it("href", "/a"), it("href", "/b"), it("href", "/c"), it("field", "email")])})
        after = rec({"/": page([it("href", "/a"), it("field", "email")])})
        r = compare(before, after, ["href:/c -- removed on purpose"])
        self.assertEqual(r["counts"], {"href": {"kept": 1, "total": 3}, "field": {"kept": 1, "total": 1}})


if __name__ == "__main__":
    unittest.main()
