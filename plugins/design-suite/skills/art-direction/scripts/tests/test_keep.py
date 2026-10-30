"""Helpers behind keep.mjs: key normalisation and --drop parsing.  Run: python3 -m unittest discover -s scripts/tests

These tests call the real functions in lib/kept.mjs through Node. They are skipped without Node.
They do not start Chrome.
"""
import functools
import http.server
import json
import os
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
KEPT = SCRIPTS / "lib" / "kept.mjs"
CLI = SCRIPTS / "keep.mjs"
CDP = SCRIPTS / "lib" / "cdp.mjs"
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

    def test_form_drop_matches_method_and_action(self):
        before = rec({"/": page([it("form", "POST /x")])})
        after = rec({"/": page([])})
        for spec in ("form:POST /x -- retired form here", "form:post /x -- retired form here"):
            r = compare(before, after, [spec])
            self.assertEqual(r["findings"], [], spec)
            self.assertEqual(r["unmatchedDrops"], [], spec)

    def test_form_drop_hint_round_trips(self):
        before = rec({"/": page([it("form", "POST /subscribe")])})
        after = rec({"/": page([])})
        hint = compare(before, after)["findings"][0]["drop"]
        self.assertEqual(hint, "form:POST /subscribe -- <reason>")
        r = compare(before, after, [hint.replace("<reason>", "retired form here")])
        self.assertEqual(r["findings"], [])
        self.assertEqual(r["unmatchedDrops"], [])

    def test_form_prefix_drop_covers_many(self):
        before = rec({"/": page([it("form", "POST /api/a"), it("form", "POST /api/b"), it("form", "GET /c")])})
        after = rec({"/": page([])})
        r = compare(before, after, ["form:POST /api/* -- api forms retired"])
        self.assertEqual([x["key"] for x in r["findings"]], ["GET /c"])
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


def find_chrome():
    if not NODE:
        return None
    result = subprocess.run(
        [NODE, "--input-type=module", "-e", f"import {{ findChrome }} from {CDP.as_uri()!r}; console.log(findChrome() || '');"],
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout.strip() or None


@unittest.skipUnless(NODE, "node is required")
class KeepSnapshot(unittest.TestCase):
    def test_snapshot_function_is_self_contained(self):
        # page.eval sends snapshot.toString() to the browser, so it may not use anything outside itself.
        code = (
            "import vm from 'node:vm';"
            "const doc = { querySelectorAll: () => [], getElementById: () => null, title: '', body: null };"
            "const ctx = { document: doc, URL, location: { href: 'http://localhost:3000/' } };"
            "const src = '(' + k.snapshot.toString() + ')(' + JSON.stringify('http://localhost:3000/') + ')';"
            "console.log(JSON.stringify(vm.runInNewContext(src, ctx)));"
        )
        out = json.loads(run_node(code))
        self.assertEqual(out, {"items": [], "skippedButtons": 0})


BEFORE = """<!doctype html><html><head><title>Home</title></head><body>
<nav>
  <a href="/pricing/">Pricing</a>
  <a href="/blog">Blog</a>
  <a href="mailto:hi@example.com">Email us</a>
  <a href="#features">Features</a>
</nav>
<h1>Welcome  home</h1>
<section id="features"><h2>Features</h2></section>
<form method="post" action="/subscribe"><input name="email" type="email"><button type="submit">Subscribe</button></form>
<form action="search"><input name="q"><input type="submit" value="Go"></form>
<form><input id="note"></form>
<button aria-label="Open menu" data-testid="menu" onclick="void 0">&#9776;</button>
<button><svg width="10" height="10"></svg></button>
</body></html>"""

AFTER_LOST = """<!doctype html><html><head><title>Home</title></head><body>
<nav>
  <a href="/pricing">Pricing</a>
  <a href="mailto:hi@example.com">Email us</a>
  <a href="#features">Features</a>
</nav>
<h1>Welcome home</h1>
<section id="features"><h2>Features</h2></section>
<form method="post" action="/subscribe"><button type="submit">Subscribe</button></form>
<form action="search"><input name="q"><input type="submit" value="Go"></form>
<form><input id="note"></form>
<button aria-label="Open menu" data-testid="menu" onclick="void 0">&#9776;</button>
<button><svg width="10" height="10"></svg></button>
</body></html>"""

BLANK = "<!doctype html><html><head><title>Blank</title></head><body></body></html>"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(directory):
    handler = functools.partial(QuietHandler, directory=str(directory))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


@unittest.skipUnless(NODE and find_chrome(), "node and a local Chrome are required")
class KeepCli(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="keep-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.out = self.tmp / "out"
        self.servers = []
        self.profiles = self.tmp / "profiles"
        self.profiles.mkdir()

    def site(self, name, html):
        directory = self.tmp / name
        directory.mkdir(exist_ok=True)
        (directory / "index.html").write_text(html, encoding="utf-8")
        server = serve(directory)
        self.servers.append(server)
        self.addCleanup(self._stop, server)
        return f"http://127.0.0.1:{server.server_address[1]}/"

    @staticmethod
    def _stop(server):
        server.shutdown()
        server.server_close()

    def keep(self, *args):
        # Chrome's throwaway profiles go under the test's own folder, so leftovers can be seen.
        env = {**os.environ, "TASTE_SKILL_TMP": str(self.profiles)}
        return subprocess.run(
            [NODE, str(CLI), *args], capture_output=True, text=True, timeout=120, env=env,
        )

    def record(self, url, *extra):
        return self.keep("record", url, "--out", str(self.out), *extra)

    def check(self, url, *extra):
        return self.keep("check", url, "--out", str(self.out), *extra)

    def test_record_then_check_identical_passes(self):
        url = self.site("before", BEFORE)
        rec = self.record(url)
        self.assertEqual(rec.returncode, 0, rec.stderr + rec.stdout)
        before = json.loads((self.out / "before.json").read_text())
        items = before["pages"]["/"]["items"]
        keys = {(i["kind"], i["key"]) for i in items}
        self.assertIn(("href", "/pricing"), keys)
        self.assertIn(("href", "mailto:hi@example.com"), keys)
        self.assertIn(("form", "POST /subscribe"), keys)
        self.assertIn(("form", "GET /search"), keys)
        self.assertIn(("field", "email"), keys)
        self.assertIn(("field", "note"), keys)
        self.assertIn(("button", "Subscribe"), keys)
        self.assertIn(("button", "Open menu"), keys)
        self.assertIn(("hook", "data-testid=menu"), keys)
        self.assertIn(("handler", "onclick button#☰"), keys)
        self.assertIn(("heading", "Welcome home"), keys)
        self.assertIn(("anchor", "features"), keys)
        self.assertEqual(before["pages"]["/"]["skippedButtons"], 1)
        self.assertIn("no accessible name", rec.stdout)
        res = self.check(url)
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertIn("Kept ", res.stdout)
        self.assertIn("Not checked: handlers attached by scripts (framework event handlers), logins, state after interaction.", res.stdout)
        self.assertIn("no accessible name", res.stdout)
        self.assertTrue((self.out / "after.json").exists())
        self.assertTrue((self.out / "report.json").exists())

    def test_check_after_removing_a_link_and_field_exits_1(self):
        self.assertEqual(self.record(self.site("before", BEFORE)).returncode, 0)
        res = self.check(self.site("after", AFTER_LOST))
        self.assertEqual(res.returncode, 1, res.stderr + res.stdout)
        self.assertIn("FAIL", res.stdout)
        self.assertIn("/blog", res.stdout)
        self.assertIn("email", res.stdout)
        self.assertIn('--drop "href:/blog -- <reason>"', res.stdout)
        self.assertIn("Not checked:", res.stdout)

    def test_check_on_different_port_matches_by_path(self):
        self.assertEqual(self.record(self.site("before", BEFORE)).returncode, 0)
        other = self.site("same", BEFORE)
        res = self.check(other)
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)

    def test_record_refuses_overwrite_without_force(self):
        url = self.site("before", BEFORE)
        self.assertEqual(self.record(url).returncode, 0)
        again = self.record(url)
        self.assertEqual(again.returncode, 2, again.stderr + again.stdout)
        self.assertIn("--force", again.stderr)
        self.assertEqual(self.record(url, "--force").returncode, 0)

    def test_check_without_record_exits_2(self):
        res = self.check(self.site("after", AFTER_LOST))
        self.assertEqual(res.returncode, 2, res.stderr + res.stdout)
        self.assertIn("before.json", res.stderr)

    def test_check_url_without_record_exits_2(self):
        self.assertEqual(self.record(self.site("before", BEFORE)).returncode, 0)
        other = self.site("other", BEFORE)
        res = self.check(other + "never-recorded")
        self.assertEqual(res.returncode, 2, res.stderr + res.stdout)

    def test_unreachable_url_exits_2(self):
        url = self.site("before", BEFORE)
        self.assertEqual(self.record(url).returncode, 0)
        dead = self.site("dead", BEFORE)
        server = self.servers[-1]
        self._stop(server)
        self.servers.remove(server)
        res = self.check(dead)
        self.assertEqual(res.returncode, 2, res.stderr + res.stdout)

    def test_drop_with_reason_turns_fail_into_pass(self):
        self.assertEqual(self.record(self.site("before", BEFORE)).returncode, 0)
        after = self.site("after", AFTER_LOST)
        res = self.check(
            after,
            "--drop", "href:/blog -- the blog moved to a subdomain",
            "--drop", "field:email -- signup moved into a dialog",
        )
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertIn("the blog moved to a subdomain", res.stdout)

    def test_unmatched_drop_fails(self):
        url = self.site("before", BEFORE)
        self.assertEqual(self.record(url).returncode, 0)
        res = self.check(url, "--drop", "href:/typo -- never existed on this page")
        self.assertEqual(res.returncode, 1, res.stderr + res.stdout)
        self.assertIn("/typo", res.stdout)

    def test_bad_drop_exits_2(self):
        url = self.site("before", BEFORE)
        self.assertEqual(self.record(url).returncode, 0)
        res = self.check(url, "--drop", "href:/blog -- short")
        self.assertEqual(res.returncode, 2, res.stderr + res.stdout)

    def test_blank_page_warns_nothing_recorded(self):
        url = self.site("blank", BLANK)
        rec = self.record(url)
        self.assertEqual(rec.returncode, 0, rec.stderr + rec.stdout)
        res = self.check(url)
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertIn("WARN", res.stdout)
        self.assertIn("nothing recorded", res.stdout)

    def test_no_chrome_profile_left_behind(self):
        url = self.site("before", BEFORE)
        self.assertEqual(self.record(url).returncode, 0)
        self.assertEqual(self.check(url).returncode, 0)
        self.assertEqual(list(self.profiles.iterdir()), [])

    def test_usage_errors_exit_2(self):
        self.assertEqual(self.keep().returncode, 2)
        self.assertEqual(self.keep("record").returncode, 2)
        self.assertEqual(self.keep("nope", "http://127.0.0.1:1/").returncode, 2)


if __name__ == "__main__":
    unittest.main()
