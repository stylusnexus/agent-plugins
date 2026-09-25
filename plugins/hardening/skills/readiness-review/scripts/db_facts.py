#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["psycopg[binary]>=3.1"]
# ///
"""db_facts.py -- read-only facts about a LIVE Postgres database's structure.

Reads only the system catalog (pg_catalog, information_schema) -- never a
table row -- in a session forced read-only with a short statement timeout,
and refuses to run any query unless the server confirms the session is
read-only. Postgres and Supabase are supported; any other database is
reported "not supported, skipped".

The connection string never appears on the command line, in output, or in
the reviewer's environment: it is read from the named variable, looked up
first in this process's environment and then in --env-file (the target
repo's own local .env), inside this subprocess only. Use a read-only role;
the output says whether the credential could write.

Usage:
  db_facts.py --env-var NAME [--env-file PATH] [--schema public ...]
              [--public-role anon ...] [--migration-tables FILE] [--json]
Exit 0 = ran; 3 = not configured (variable missing); 4 = not a supported
database; 5 = not verified (driver missing, connection or guard failure).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from redaction import redact  # noqa: E402

STATEMENT_TIMEOUT = "15s"
GUARD = (
    "SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY",
    "SET default_transaction_read_only = on",
    f"SET statement_timeout = '{STATEMENT_TIMEOUT}'",
)

ROLES_SQL = "select rolname from pg_catalog.pg_roles where rolname = any(%s)"
CREDENTIAL_SQL = """
select r.rolsuper,
       (select count(*) from pg_catalog.pg_class c join pg_catalog.pg_namespace n on n.oid = c.relnamespace
         where n.nspname = any(%s) and c.relkind in ('r', 'p')
           and has_table_privilege(current_user, c.oid, 'INSERT,UPDATE,DELETE,TRUNCATE'))
from pg_catalog.pg_roles r where r.rolname = current_user
"""
TABLES_SQL = """
select n.nspname || '.' || c.relname, c.relrowsecurity
from pg_catalog.pg_class c join pg_catalog.pg_namespace n on n.oid = c.relnamespace
where n.nspname = any(%s) and c.relkind in ('r', 'p')
"""
ROLE_WRITABLE_SQL = """
select n.nspname || '.' || c.relname
from pg_catalog.pg_class c join pg_catalog.pg_namespace n on n.oid = c.relnamespace
where n.nspname = any(%s) and c.relkind in ('r', 'p') and not c.relrowsecurity
  and has_table_privilege(%s, c.oid, 'INSERT,UPDATE,DELETE')
"""
POLICIES_SQL = """
select schemaname || '.' || tablename, cmd, with_check is not null
from pg_catalog.pg_policies where schemaname = any(%s)
"""
SECDEF_SQL = """
select n.nspname || '.' || p.proname
from pg_catalog.pg_proc p join pg_catalog.pg_namespace n on n.oid = p.pronamespace
where n.nspname = any(%s) and p.prosecdef
  and not exists (select 1 from unnest(coalesce(p.proconfig, '{}')) cfg where cfg like 'search_path=%%')
"""
VIEWS_SQL = """
select n.nspname || '.' || c.relname
from pg_catalog.pg_class c join pg_catalog.pg_namespace n on n.oid = c.relnamespace
where n.nspname = any(%s) and c.relkind = 'v'
  and not coalesce('security_invoker=true' = any(c.reloptions), false)
  and not coalesce('security_invoker=on' = any(c.reloptions), false)
"""

FORBIDDEN = re.compile(r"\b(insert|update|delete|truncate|drop|alter|create|grant|revoke|copy|merge|call|do|"
                       r"vacuum|analyze|lock|set|reset|refresh|comment|execute|prepare|listen|notify|into)\b")
# functions that read files, reach the network, change settings, or run a query given as text
UNSAFE_FN = re.compile(r"\b(pg_read_\w*|pg_ls_\w*|pg_stat_file|lo_\w+|dblink\w*|set_config|pg_terminate_backend|"
                       r"pg_cancel_backend|pg_sleep\w*|pg_reload_conf|pg_rotate_logfile|\w+_to_xml\w*|"
                       r"query_to_\w+|pg_advisory\w*|nextval|setval)\s*\(")
SOURCE = re.compile(r"\b(?:from|join)\s+([\w.]+)")
FROM_END = re.compile(r"\b(where|join|group|order|limit|on|union|having)\b")


def from_list_extras(body: str) -> list[str]:
    """Relations after the first in each comma-separated FROM list (commas inside parentheses ignored)."""
    out = []
    for m in re.finditer(r"\bfrom\s+", body):
        depth, item, items = 0, "", []
        i = m.end()
        while i < len(body):
            ch = body[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                if depth == 0:
                    break
                depth -= 1
            elif depth == 0 and (ch == ";" or FROM_END.match(body, i) and body[i - 1] in " \n\t"):
                break
            if ch == "," and depth == 0:
                items.append(item)
                item = ""
            else:
                item += ch
            i += 1
        items.append(item)
        out += [x.split()[0] for x in items[1:] if x.split()]
    return out
CATALOG = re.compile(r"^(pg_catalog\.|information_schema\.|pg_[a-z_]+$|unnest$)")


class GuardError(RuntimeError):
    """The session could not be proven read-only, or a query was not catalog-only."""


def assert_catalog_only(sql: str) -> None:
    """Reject anything but a SELECT over the system catalog. String literals are ignored."""
    body = re.sub(r"'(?:[^']|'')*'", "''", sql).lower()
    body = re.sub(r"--[^\n]*", " ", body)
    if not body.strip().startswith("select"):
        raise GuardError("only SELECT statements are allowed")
    bad = FORBIDDEN.search(body)
    if bad:
        raise GuardError(f"forbidden keyword in catalog query: {bad.group(1)}")
    bad = UNSAFE_FN.search(body)
    if bad:
        raise GuardError(f"function not allowed in a catalog query: {bad.group(1)}")
    for src in SOURCE.findall(body) + from_list_extras(body):
        if not CATALOG.match(src):
            raise GuardError(f"query reads a non-catalog relation: {src}")


def enforce_read_only(cur) -> None:
    """Force the session read-only, then prove it before anything else runs."""
    for stmt in GUARD:
        cur.execute(stmt)
    cur.execute("SHOW transaction_read_only")
    row = cur.fetchone()
    if not row or str(row[0]).lower() != "on":
        raise GuardError("server did not confirm a read-only session; no catalog query was run")


def query(cur, sql: str, params=()):
    assert_catalog_only(sql)
    cur.execute(sql, params)
    return cur.fetchall()


def collect(conn, schemas: list[str], public_roles: list[str], migration_tables=None) -> dict:
    """Run the guard, then the catalog queries. Takes any DB-API connection (mockable)."""
    conn.autocommit = True  # each statement its own transaction, all read-only by session default
    cur = conn.cursor()
    enforce_read_only(cur)
    roles = [r[0] for r in query(cur, ROLES_SQL, (public_roles,))]
    cred = query(cur, CREDENTIAL_SQL, (schemas,))
    tables = query(cur, TABLES_SQL, (schemas,))
    writable = {}
    for role in roles:
        writable[role] = sorted(r[0] for r in query(cur, ROLE_WRITABLE_SQL, (schemas, role)))
    policies = query(cur, POLICIES_SQL, (schemas,))
    secdef = query(cur, SECDEF_SQL, (schemas,))
    views = query(cur, VIEWS_SQL, (schemas,))
    return summarize(tables, policies, secdef, views, writable, cred[0] if cred else None,
                     [r for r in public_roles if r not in roles], migration_tables)


def summarize(tables, policies, secdef, views, writable, cred, missing_roles, migration_tables=None) -> dict:
    by_table: dict[str, list] = {}
    for t, cmd, with_check in policies:
        by_table.setdefault(t, []).append((cmd, with_check))
    out = {
        "status": "ok",
        "tables": len(tables),
        "tables_without_rls": sorted(t for t, rls in tables if not rls),
        "rls_on_but_no_policies": sorted(t for t, rls in tables if rls and t not in by_table),
        "update_policies_without_with_check": sorted(
            {t for t, ps in by_table.items() for cmd, wc in ps if cmd in ("UPDATE", "ALL") and not wc}),
        "security_definer_functions_without_search_path": sorted(r[0] for r in secdef),
        "views_without_security_invoker": sorted(r[0] for r in views),
        "writable_without_rls_by_public_role": writable,
        "public_roles_not_present": missing_roles,
    }
    if cred is not None:
        out["credential_is_superuser"] = bool(cred[0])
        out["credential_can_write_tables"] = int(cred[1])
    if migration_tables is not None:
        live = {t for t, _ in tables}
        mig = {t if "." in t else f"public.{t}" for t in migration_tables}
        out["drift_live_not_in_migrations"] = sorted(live - mig)
        out["drift_in_migrations_not_live"] = sorted(mig - live)
    return out


def load_env_value(name: str, env_file: str | None, file_only: bool = False) -> str | None:
    """The variable from the environment (unless file_only), else from a KEY=VALUE .env file."""
    if not file_only and os.environ.get(name):
        return os.environ[name]
    if not env_file or not Path(env_file).is_file():
        return None
    for line in Path(env_file).read_text(errors="replace").splitlines():
        m = re.match(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if m and m.group(1) == name:
            v = m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
                v = v[1:-1]
            return v or None
    return None


def connect(url: str):
    options = f"-c default_transaction_read_only=on -c statement_timeout={STATEMENT_TIMEOUT}"
    try:
        import psycopg
        return psycopg.connect(url, connect_timeout=15, options=options)
    except ImportError:
        import psycopg2  # fall back to the older driver when that's what's installed
        return psycopg2.connect(url, connect_timeout=15, options=options)


def _emit(res: dict, as_json: bool) -> None:
    print(json.dumps(res, indent=2) if as_json else "\n".join(f"{k}: {v}" for k, v in res.items()))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Read-only catalog facts about a live Postgres database (no table rows).")
    ap.add_argument("--env-var", required=True, help="name of the variable holding the connection string")
    ap.add_argument("--env-file", help="the target repo's local .env file to look the variable up in")
    ap.add_argument("--env-file-only", action="store_true",
                    help="ignore the process environment (used when the variable name came from the repo's config)")
    ap.add_argument("--schema", action="append", default=[])
    ap.add_argument("--public-role", action="append", default=[], help="role the public/anonymous key maps to (e.g. anon)")
    ap.add_argument("--migration-tables", help="JSON file: tables the migrations create (schema-less names = public)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    url = load_env_value(args.env_var, args.env_file, args.env_file_only)
    if not url:
        _emit({"status": "NOT CONFIGURED", "reason": f"{args.env_var} is not set in the environment or the .env file"}, args.json)
        return 3
    if not re.match(r"postgres(ql)?://", url):
        scheme = url.split(":", 1)[0][:20]
        _emit({"status": "not supported, skipped", "reason": f"only Postgres is supported; this is {scheme!r}"}, args.json)
        return 4
    schemas = args.schema or ["public"]
    mig = json.loads(Path(args.migration_tables).read_text()) if args.migration_tables else None
    try:
        conn = connect(url)
        try:
            res = collect(conn, schemas, args.public_role, mig)
        finally:
            conn.close()
    except ImportError:
        _emit({"status": "NOT VERIFIED", "reason": "no Postgres driver (install psycopg, or run with uv)"}, args.json)
        return 5
    except Exception as e:  # connection refused, auth failure, guard failure: report, never the URL
        msg = redact(str(e).replace(url, "[connection string]"))[0].splitlines()[0][:300] if str(e) else type(e).__name__
        _emit({"status": "NOT VERIFIED", "reason": f"{type(e).__name__}: {msg}"}, args.json)
        return 5
    _emit(res, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
