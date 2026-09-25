import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import completeness_scan  # noqa: E402
import db_facts  # noqa: E402
import findings  # noqa: E402
import gather_facts  # noqa: E402
import rr_common  # noqa: E402
import gh_facts  # noqa: E402
import make_review_copy  # noqa: E402
import security_scan  # noqa: E402
import write_report  # noqa: E402
from redaction import redact  # noqa: E402


class RedactionTests(unittest.TestCase):
    def test_known_secret_shapes_are_scrubbed(self):
        samples = {
            # assembled at runtime so secret scanners don't flag this file
            "anthropic_key": "sk-" + "ant-api03-abcdefghijklmnop",
            "openai_key": "sk-" + "proj-abcdefghijklmnopqrstuvwx",
            "github_token": "gh" + "p_abcdefghijklmnopqrstuvwxyz0123",
            "stripe_key": "sk_" + "live_abcdefghijklmnop1234",
            "aws_access_key": "AK" + "IAABCDEFGHIJKLMNOP",
            "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoic2VydmljZSJ9.c2lnbmF0dXJlc2ln",
            "bearer_token": "Bearer abcdefghijklmnopqrstuvwx",
        }
        for cls, secret in samples.items():
            out, found = redact(f"value={secret} end")
            self.assertNotIn(secret, out, cls)
            self.assertIn(cls, found)

    def test_connection_string_password_removed_host_kept(self):
        out, found = redact("postgresql://reader:hunter2secret@db.example.com:5432/app")
        self.assertNotIn("hunter2secret", out)
        self.assertIn("db.example.com", out)
        self.assertIn("url_password", found)

    def test_redacting_twice_changes_nothing(self):
        once, _ = redact("postgresql://reader:hunter2secret@db.example.com/app and " + "sk-" + "ant-api03-abcdefghijklmnop")
        self.assertEqual(redact(once), (once, []))

    def test_private_key_block(self):
        pem = "-----BEGIN RSA PRIVATE KEY-----\nMIIabc\n-----END RSA PRIVATE KEY-----"
        out, _ = redact(f"x {pem} y")
        self.assertNotIn("MIIabc", out)

    def test_plain_text_untouched(self):
        text = "## Security\n- high, src/app/api/route.ts:14, missing auth"
        self.assertEqual(redact(text), (text, []))


class FakeCursor:
    def __init__(self, read_only="on"):
        self.statements = []
        self.read_only = read_only
        self._last = None

    def execute(self, sql, params=None):
        self.statements.append(sql.strip())
        self._last = sql

    def fetchone(self):
        return (self.read_only,) if "SHOW transaction_read_only" in self._last else None

    def fetchall(self):
        if "pg_roles where rolname = any" in self._last:
            return [("anon",)]
        if "rolsuper" in self._last:
            return [(False, 0)]
        if "relrowsecurity\nfrom" in self._last:
            return [("public.notes", True), ("public.logs", False)]
        return []


class FakeConn:
    def __init__(self, cur):
        self.cur = cur
        self.autocommit = False

    def cursor(self):
        return self.cur


class DbGuardTests(unittest.TestCase):
    def test_session_is_read_only_before_any_catalog_query(self):
        cur = FakeCursor()
        res = db_facts.collect(FakeConn(cur), ["public"], ["anon"], ["notes", "logs", "gone"])
        first = cur.statements[:4]
        self.assertEqual(first[0], "SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY")
        self.assertEqual(first[1], "SET default_transaction_read_only = on")
        self.assertTrue(first[2].startswith("SET statement_timeout"))
        self.assertEqual(first[3], "SHOW transaction_read_only")
        for sql in cur.statements[4:]:
            self.assertTrue(sql.lower().startswith("select"), sql)
        self.assertEqual(res["tables_without_rls"], ["public.logs"])
        self.assertEqual(res["drift_in_migrations_not_live"], ["public.gone"])

    def test_refuses_to_query_when_server_does_not_confirm_read_only(self):
        cur = FakeCursor(read_only="off")
        with self.assertRaises(db_facts.GuardError):
            db_facts.collect(FakeConn(cur), ["public"], [])
        self.assertFalse(any(s.lower().startswith("select") for s in cur.statements))

    def test_every_shipped_query_is_catalog_only(self):
        for name in ("ROLES_SQL", "CREDENTIAL_SQL", "TABLES_SQL", "ROLE_WRITABLE_SQL", "POLICIES_SQL",
                     "SECDEF_SQL", "VIEWS_SQL"):
            db_facts.assert_catalog_only(getattr(db_facts, name))

    def test_catalog_guard_rejects_rows_and_writes(self):
        for sql in ("select * from users", "select email from public.profiles",
                    "update pg_catalog.pg_class set relname = 'x'", "delete from pg_policies",
                    "select 1; drop table notes", "insert into pg_class values (1)",
                    "select * from pg_class c join accounts a on true",
                    "select * from pg_catalog.pg_class c, users u",
                    "select pg_read_file('/etc/passwd')", "select dblink('host=x', 'select 1')",
                    "select set_config('default_transaction_read_only', 'off', false)",
                    "select query_to_xml('select * from users', true, true, '')"):
            with self.assertRaises(db_facts.GuardError, msg=sql):
                db_facts.assert_catalog_only(sql)

    def test_url_is_never_printed(self):
        url = "postgresql://reader:s3cretpw@db.example.com/app"
        with tempfile.TemporaryDirectory() as d:
            env = Path(d) / ".env"
            env.write_text(f"OTHER=1\nDB_RO='{url}'\n")
            with mock.patch.object(db_facts, "connect", side_effect=RuntimeError(f"could not connect to {url}")), \
                    mock.patch.dict(os.environ, {}, clear=True), \
                    mock.patch("sys.stdout", new_callable=io.StringIO) as out:
                rc = db_facts.main(["--env-var", "DB_RO", "--env-file", str(env), "--json"])
            self.assertEqual(rc, 5)
            self.assertNotIn("s3cretpw", out.getvalue())
            self.assertNotIn(url, out.getvalue())
            self.assertIn("NOT VERIFIED", out.getvalue())

    def test_not_configured_and_unsupported(self):
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(db_facts.main(["--env-var", "NOPE", "--json"]), 3)
        with mock.patch.dict(os.environ, {"DB": "mysql://u:p@h/db"}, clear=True), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as out:
            self.assertEqual(db_facts.main(["--env-var", "DB", "--json"]), 4)
            self.assertIn("not supported", out.getvalue())
            self.assertNotIn("u:p", out.getvalue())


class GhAllowlistTests(unittest.TestCase):
    def test_reads_allowed(self):
        gh_facts.check_gh(["api", "repos/o/r/dependabot/alerts?state=open", "--paginate"])
        gh_facts.check_gh(["api", "-X", "GET", "repos/o/r/issues/1"])
        gh_facts.check_gh(["issue", "list", "-R", "o/r"])
        gh_facts.check_gh(["run", "list", "-R", "o/r"])
        gh_facts.check_git(["log", "--since=7.days"])
        gh_facts.check_git(["remote"])

    def test_writes_refused(self):
        for args in (["issue", "create", "--title", "x"], ["issue", "comment", "1"], ["pr", "merge", "1"],
                     ["api", "-X", "POST", "repos/o/r/issues"], ["api", "--method=PATCH", "repos/o/r"],
                     ["api", "repos/o/r/issues", "-f", "title=x"], ["api", "repos/o/r/labels", "--input", "x.json"],
                     ["api", "graphql", "-F", "query=mutation{}"], ["label", "create", "x"],
                     ["api", "-XPOST", "repos/o/r/issues"], ["api", "-H", "X-HTTP-Method-Override: POST", "repos/o/r"],
                     ["api", "--method", "GET", "graphql"], ["api", "-X", "GET", "graphql", "--paginate"],
                     ["api", "--paginate", "/graphql"]):
            with self.assertRaises(gh_facts.NotReadOnly, msg=args):
                gh_facts.check_gh(args)
        for args in (["push"], ["commit", "-m", "x"], ["checkout", "main"], ["remote", "add", "x", "y"]):
            with self.assertRaises(gh_facts.NotReadOnly):
                gh_facts.check_git(args)


class OperatorOwnsPathsTests(unittest.TestCase):
    """The reviewed repo's config must not choose where we write, what we read, or which DB we reach."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, ignore_errors=True))
        self.repo = self.tmp / "repo"
        (self.repo / "sub").mkdir(parents=True)
        (self.tmp / "outside").mkdir()
        (self.repo / "escape").symlink_to(self.tmp / "outside")

    def test_inside_rejects_absolute_parent_and_symlink_escape(self):
        self.assertIsNotNone(rr_common.inside(self.repo, "sub"))
        for bad in ("/etc", "../outside", "sub/../../outside", "escape", ""):
            self.assertIsNone(rr_common.inside(self.repo, bad), bad)

    def test_report_dir_ignores_config_and_refuses_repo_and_symlinks(self):
        with mock.patch.dict(os.environ, {"HOME": str(self.tmp)}, clear=False):
            os.environ.pop("READINESS_REPORT_DIR", None)
            d = gather_facts.report_dir(self.repo, None)
        self.assertEqual(d, self.tmp / ".readiness-review" / "reports" / "repo")
        with self.assertRaises(SystemExit):
            gather_facts.report_dir(self.repo, str(self.repo / "reports"))
        with self.assertRaises(SystemExit):
            gather_facts.report_dir(self.repo, str(self.repo / "escape" / "r"))
        res = gather_facts.gather(self.repo, {"report_dir": "/tmp/evil"}, 1, None)
        self.assertNotIn("report_dir", res)
        self.assertTrue(any(x.startswith("report_dir") for x in res["config_values_ignored"]))

    def test_config_paths_and_db_env_stay_inside_repo(self):
        cfg = {"scan": {"migrations_dirs": ["../outside", "sub"]},
               "database": {"url_env": "OPERATOR_PROD_URL", "env_file": "../outside/.env"},
               "review_areas": [{"name": "a", "paths": ["src", "/etc", "../x"], "focus": "f"}]}
        res = gather_facts.gather(self.repo, cfg, 0, None)
        self.assertEqual(res["live_database"]["status"], "NOT VERIFIED")
        self.assertIn("scan.migrations_dirs '../outside': outside the repo", res["config_values_ignored"])
        self.assertEqual(res["area"]["paths"], ["src"])
        self.assertEqual(res["area"]["paths_dropped_unsafe"], 2)

    def test_repo_named_variable_is_not_read_from_operator_environment(self):
        (self.repo / ".env").write_text("")
        with mock.patch.dict(os.environ, {"OPERATOR_PROD_URL": "postgresql://u:p@prod/db"}):
            self.assertIsNone(db_facts.load_env_value("OPERATOR_PROD_URL", str(self.repo / ".env"), file_only=True))
            self.assertIsNotNone(db_facts.load_env_value("OPERATOR_PROD_URL", str(self.repo / ".env")))

    def test_write_report_refuses_symlink_and_forbidden_trees(self):
        with self.assertRaises(SystemExit):
            write_report.check_out_dir(self.repo / "escape" / "r", [])
        with self.assertRaises(SystemExit):
            write_report.check_out_dir(self.repo / "sub" / "r", [str(self.repo)])
        write_report.check_out_dir(self.tmp / "outside" / "r", [str(self.repo)])


class ReportWriteTests(unittest.TestCase):
    def test_never_overwrites_and_redacts(self):
        with tempfile.TemporaryDirectory() as d:
            a = write_report.write_new(Path(d), "2026-01-01-x-readiness", "first")
            b = write_report.write_new(Path(d), "2026-01-01-x-readiness", "second")
            self.assertNotEqual(a, b)
            self.assertEqual(a.read_text(), "first")
            self.assertTrue(b.name.endswith("-2.md"))
            with mock.patch("sys.stdin", io.StringIO("key sk-" + "ant-api03-abcdefghijklmnop")), \
                    mock.patch("sys.stdout", new_callable=io.StringIO) as out, \
                    mock.patch("sys.stderr", new_callable=io.StringIO):
                write_report.main(["--out-dir", d, "--slug", "X", "--date", "2026-01-01"])
            written = Path(out.getvalue().strip())
            self.assertTrue(written.name.endswith("-3.md"))
            self.assertNotIn("sk-ant-api03", written.read_text())


class ReviewCopyTests(unittest.TestCase):
    def test_copy_drops_git_env_and_symlinks(self):
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as outside:
            s = Path(src)
            (s / ".git").mkdir()
            (s / ".git" / "config").write_text("x")
            (s / ".env").write_text("SECRET=1")
            (s / ".env.local").write_text("SECRET=2")
            (s / "app").mkdir()
            (s / "app" / ".env.production").write_text("SECRET=3")
            (s / "app" / "page.tsx").write_text("ok")
            (s / "node_modules").mkdir()
            (s / "node_modules" / "x.js").write_text("x")
            secret = Path(outside) / "secret.txt"
            secret.write_text("SECRET=4")
            (s / "link.txt").symlink_to(secret)
            with tempfile.TemporaryDirectory() as dest:
                make_review_copy.copy(s, Path(dest))
                self.assertEqual(make_review_copy.leftovers(Path(dest)), [])
                names = {str(p.relative_to(dest)) for p in Path(dest).rglob("*")}
                self.assertIn("app/page.tsx", names)
                for gone in (".git", ".env", ".env.local", "app/.env.production", "node_modules", "link.txt"):
                    self.assertNotIn(gone, names)


FAKE_KEY = "sk-" + "ant-api03-abcdefghijklmnop"
REPORT = """## Verdict
at risk

## Findings to file
```json
[{"title": "fix(api): export route has no auth", "kind": "security", "severity": "high",
  "files": ["src/app/api/export/route.ts:14"], "body": "token FAKE_KEY leaked", "known": null},
 {"title": "fix(ui): send button hidden on phones", "kind": "usability", "severity": "medium", "files": [], "known": 42},
 {"title": "fix(db): notes table has no RLS", "kind": "database", "severity": "critical", "files": []},
 {"severity": "bogus"}]
```
""".replace("FAKE_KEY", FAKE_KEY)


class FindingsTests(unittest.TestCase):
    def test_annotates_without_filing_or_dropping(self):
        found, err, start = findings.parse(REPORT)
        self.assertEqual(len(found), 3)
        self.assertIn("1 malformed", err)
        titles = {findings.normalize("Notes table has no RLS"): 7}
        with mock.patch.object(findings, "gh", side_effect=AssertionError("no gh without --repo")):
            out = findings.annotate(found, titles, None)
        notes = {f["title"]: f["looks_like"] for f in out}
        self.assertEqual(notes["fix(db): notes table has no RLS"], "looks like existing #7 (same title)")
        self.assertEqual(notes["fix(ui): send button hidden on phones"], "known #42")
        self.assertIsNone(notes["fix(api): export route has no auth"])
        text = findings.render(out, err, "2026-01-01")
        self.assertIn("Nothing was filed", text)
        self.assertNotIn("sk-ant-api03", text)
        self.assertIn("readiness-review-fp:", text)
        data = json.loads(text.split("```json", 1)[1].split("```", 1)[0])
        self.assertEqual(len(data), 3)

    def test_missing_block_is_reported(self):
        found, err, start = findings.parse("## Verdict\nok\n")
        self.assertEqual((found, start), ([], -1))
        self.assertIn("no '## Findings to file'", err)


class ScannerTests(unittest.TestCase):
    def repo(self, files: dict) -> Path:
        d = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        for rel, text in files.items():
            p = d / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        return d

    def test_nextjs_routes_and_client_secrets(self):
        root = self.repo({
            "package.json": '{"dependencies": {"next": "15"}}',
            "src/app/api/open/route.ts": "export async function GET() { return Response.json({}) }",
            "src/app/api/safe/route.ts": "export async function GET() { const u = await requireAuth(); }",
            "src/app/api/custom/route.ts": "export async function GET() { await requireMember(req) }",
            "src/components/Admin.tsx": "'use client'\nconst k = process.env.SUPABASE_SERVICE_ROLE_KEY",
            "supabase/migrations/001.sql": "create table public.notes (id int);\ncreate table logs (id int);\n"
                                           "alter table notes enable row level security;",
        })
        res = security_scan.scan(root, auth_extra=[r"requireMember\("])
        self.assertEqual(res["routes_total"], 3)
        self.assertEqual(res["routes_without_auth_pattern"], ["src/app/api/open/route.ts"])
        self.assertEqual(res["secret_keys_in_client_files"], ["src/components/Admin.tsx"])
        self.assertEqual(res["tables_without_rls_in_migrations"], ["logs"])

    def test_fastapi_routes(self):
        root = self.repo({
            "pyproject.toml": 'dependencies = ["fastapi"]',
            "app/main.py": (
                "@app.get('/open')\ndef open_():\n    return {}\n\n"
                "@app.get('/me')\ndef me(user = Depends(get_current_user)):\n    return user\n\n"
                "@router.post('/items')\nasync def create(item: Item):\n    db.execute(f\"insert {item}\")\n"),
        })
        res = security_scan.scan(root)
        self.assertEqual(res["routes_total"], 3)
        self.assertEqual(res["routes_without_auth_pattern"], ["app/main.py:1", "app/main.py:9"])
        self.assertEqual(res["sql_built_from_strings"], ["app/main.py"])

    def test_completeness_leads_skip_tests(self):
        root = self.repo({
            "package.json": "{}",
            "src/app/api/beta/route.ts": "return NextResponse.json({}, { status: 501 })",
            "src/components/Card.tsx": "<img src='a.png' /> Coming soon // TODO",
            "src/components/Card.test.tsx": "<img src='a.png' />",
            "svc/jobs.py": "def run():\n    raise NotImplementedError\n",
        })
        res = completeness_scan.scan(root)
        self.assertEqual(res["not_implemented_routes"], ["src/app/api/beta/route.ts"])
        self.assertEqual(res["images_without_alt"], ["src/components/Card.tsx"])
        self.assertEqual(res["coming_soon"], ["src/components/Card.tsx"])
        self.assertEqual(res["not_implemented_errors"], ["svc/jobs.py"])
        self.assertEqual(res["todo_total"], 1)


if __name__ == "__main__":
    unittest.main()
