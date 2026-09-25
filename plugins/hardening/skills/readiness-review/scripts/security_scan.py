#!/usr/bin/env python3
"""security_scan.py -- cheap whole-repo security and architecture pattern checks.

Read-only. Every hit is a LEAD for the reviewer to triage, not a verdict:
a helper can wrap an auth check, and some routes are public on purpose.

Supported stacks: Next.js (app and pages routers) and TypeScript/JavaScript
generally; Python with FastAPI, Flask, or Starlette-style decorators. Anything
else degrades: the checks that can't apply are listed under "not_checked".

Usage:
  security_scan.py --path <repo> [--auth-pattern REGEX ...] [--service-key-pattern REGEX ...]
                   [--migrations-dir DIR ...] [--json]
Exit 0 = the scan ran; 2 = bad arguments.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rr_common import JS_CODE, PY_CODE, TEMPLATES, detect_stack, inside, read, walk  # noqa: E402

JS_AUTH = (r"requireAuth|requireUser|requireAdmin|require[A-Z]\w*Admin|withAuth|withApiAuth|getAuthenticatedUser"
           r"|auth\.getUser|getUser\(|getServerSession|getSession|currentUser\(|\bauth\(\)|getToken\(|jwtVerify"
           r"|verifyToken|verifySignature|constructEvent|CRON_SECRET|verifyCron|requireApiKey|validateRequest")
PY_AUTH = (r"Depends\(\s*\w*(auth|user|current|token|verify|require|admin|api_key)\w*|Security\(|login_required"
           r"|permission_required|get_current_\w+|verify_\w*token|HTTPBearer|OAuth2PasswordBearer|APIKeyHeader"
           r"|require_\w+|authenticate\(|jwt\.decode")
SERVICE = r"SERVICE_ROLE|service_role|createAdminClient|supabaseAdmin|createServiceClient|sk_live_|PRIVATE_KEY|SECRET_KEY"
PUBLIC_SECRET = re.compile(r"\b(?:NEXT_PUBLIC|VITE|REACT_APP|EXPO_PUBLIC|PUBLIC)_[A-Z0-9_]*(?:SECRET|SERVICE|PRIVATE|PASSWORD)[A-Z0-9_]*")
RAW_HTML_JS = re.compile(r"dangerouslySetInnerHTML|\bv-html\b|\{@html\b|\.innerHTML\s*=")
RAW_HTML_PY = re.compile(r"mark_safe\(|Markup\(|autoescape\s*=\s*False")
RAW_HTML_TPL = re.compile(r"\|\s*safe\b|\{%\s*autoescape\s+false")
EXEC_JS = re.compile(r"(?<![\w.])eval\(|new Function\(|child_process|execSync\(`")
EXEC_PY = re.compile(r"(?<![\w.])(eval|exec)\(|pickle\.loads?\(|yaml\.load\((?![^)]*Loader)|shell\s*=\s*True|os\.system\(")
SQL_JS = re.compile(r"\.(query|execute)\(\s*`[^`]*\$\{|\$(queryRawUnsafe|executeRawUnsafe)\(|sql\.raw\(|\.raw\(\s*`[^`]*\$\{")
SQL_PY = re.compile(r"\.(execute|executemany|raw)\(\s*(f[\"']|[\"'][^\"']*[\"']\s*(%|\+|\.format))|text\(\s*f[\"']")
PY_ROUTE = re.compile(r"^[ \t]*@\s*\w+(?:\.\w+)*\.(get|post|put|patch|delete|route|api_route|websocket)\(", re.M)
PY_ROUTER_DEPS = re.compile(r"(APIRouter|FastAPI|include_router)\([^)]*dependencies\s*=", re.S)

NAME = r'(?:"?(\w+)"?\.)?"?(\w+)"?'
RLS_EVENTS = re.compile(
    r"create\s+table\s+(?:if\s+not\s+exists\s+)?(?P<create>" + NAME + r")"
    r"|drop\s+table\s+(?:if\s+exists\s+)?(?P<drop>" + NAME + r")"
    r"|alter\s+table\s+(?:if\s+exists\s+)?(?:only\s+)?(?P<alter>" + NAME + r")\s+(?P<mode>enable|disable)\s+row\s+level\s+security",
    re.I)
DEFAULT_MIGRATION_DIRS = ("supabase/migrations", "migrations", "db/migrations", "database/migrations", "prisma/migrations")


def _split(name: str):
    """'"public"."foo"' -> ('public', 'foo'); 'foo' -> (None, 'foo')."""
    parts = [x.strip('"') for x in name.split(".")]
    return (parts[0], parts[1]) if len(parts) == 2 else (None, parts[0])


def is_next_route(rel: str) -> bool:
    name = rel.rsplit("/", 1)[-1]
    if name.split(".")[0] == "route" and ("/app/" in "/" + rel):
        return True
    return "/pages/api/" in "/" + rel


def python_routes(text: str, auth: re.Pattern) -> list[tuple[int, bool]]:
    """(line, has_auth) for each decorated route: decorators + signature + the first 40 body lines."""
    lines = text.splitlines()
    file_level = bool(PY_ROUTER_DEPS.search(text) and auth.search(text))
    out = []
    for m in PY_ROUTE.finditer(text):
        start = text.count("\n", 0, m.start())
        window = []
        seen_def = False
        indent = len(lines[start]) - len(lines[start].lstrip())
        for line in lines[start:start + 45]:
            stripped = line.lstrip()
            # after this route's own def, the next decorator/def/class at its indent is someone else's code
            if seen_def and stripped.startswith(("@", "def ", "async def ", "class ")) \
                    and len(line) - len(stripped) <= indent:
                break
            seen_def = seen_def or stripped.startswith(("def ", "async def "))
            window.append(line)
        out.append((start + 1, file_level or bool(auth.search("\n".join(window)))))
    return out


def rls_replay(root: Path, dirs) -> dict | None:
    """Replay SQL migrations in path order. None when there are no SQL migrations."""
    files = []
    for d in dirs:
        base = inside(root, d)  # a dir that escapes the repo is ignored
        if base and base.is_dir():
            files += sorted(base.rglob("*.sql"))
    if not files:
        return None
    tables, rls = set(), set()
    for p in files:
        for m in RLS_EVENTS.finditer(read(p)):
            kind = next(k for k in ("create", "drop", "alter") if m.group(k))
            schema, table = [g.lower() if g else g for g in _split(m.group(kind))]
            if schema not in (None, "public"):
                continue
            if kind == "create":
                tables.add(table)
            elif kind == "drop":
                tables.discard(table)
                rls.discard(table)
            elif m.group("mode").lower() == "enable":
                rls.add(table)
            else:
                rls.discard(table)
    return {"migration_files": len(files), "public_tables_in_migrations": sorted(tables),
            "tables_without_rls_in_migrations": sorted(tables - rls)}


def scan(root: Path, auth_extra=(), service_extra=(), migration_dirs=None) -> dict:
    stack = detect_stack(root)
    rel = lambda p: str(p.relative_to(root))
    js_auth = re.compile("|".join([JS_AUTH, *auth_extra]))
    py_auth = re.compile("|".join([PY_AUTH, *auth_extra]))
    service = re.compile("|".join([SERVICE, *service_extra]))

    out = {"stack": stack, "routes_total": 0, "routes_without_auth_pattern": [],
           "secret_keys_in_client_files": [], "raw_html_injection": [], "public_env_secret_names": [],
           "dynamic_code_execution": [], "sql_built_from_strings": [], "largest_files": [],
           "checked": [], "not_checked": []}
    sizes = []

    js_files = list(walk(root, JS_CODE))
    for p in js_files:
        t, r = read(p), rel(p)
        if is_next_route(r):
            out["routes_total"] += 1
            if not js_auth.search(t):
                out["routes_without_auth_pattern"].append(r)
        head = t[:300]
        if ("'use client'" in head or '"use client"' in head) and service.search(t):
            out["secret_keys_in_client_files"].append(r)
        if RAW_HTML_JS.search(t):
            out["raw_html_injection"].append(r)
        for m in sorted({x.group(0) for x in PUBLIC_SECRET.finditer(t)}):
            out["public_env_secret_names"].append(f"{r}: {m}")
        if EXEC_JS.search(t):
            out["dynamic_code_execution"].append(r)
        if SQL_JS.search(t):
            out["sql_built_from_strings"].append(r)
        sizes.append((t.count("\n") + 1, r))

    for p in walk(root, PY_CODE):
        t, r = read(p), rel(p)
        for line, ok in python_routes(t, py_auth):
            out["routes_total"] += 1
            if not ok:
                out["routes_without_auth_pattern"].append(f"{r}:{line}")
        if RAW_HTML_PY.search(t):
            out["raw_html_injection"].append(r)
        if EXEC_PY.search(t):
            out["dynamic_code_execution"].append(r)
        if SQL_PY.search(t):
            out["sql_built_from_strings"].append(r)
        sizes.append((t.count("\n") + 1, r))

    for p in walk(root, TEMPLATES):
        if RAW_HTML_TPL.search(read(p)):
            out["raw_html_injection"].append(rel(p))

    mw = [rel(p) for p in root.glob("*middleware.*") if p.suffix in JS_CODE] + \
         [rel(p) for p in root.glob("src/middleware.*") if p.suffix in JS_CODE]
    out["nextjs_middleware"] = sorted(mw)
    out["largest_files"] = [{"file": f, "lines": n} for n, f in sorted(sizes, reverse=True)[:15]]
    for k in ("routes_without_auth_pattern", "secret_keys_in_client_files", "raw_html_injection",
              "public_env_secret_names", "dynamic_code_execution", "sql_built_from_strings"):
        out[k] = sorted(set(out[k]))

    rls = rls_replay(root, migration_dirs or DEFAULT_MIGRATION_DIRS)
    if rls:
        out.update(rls)
        out["checked"].append("row-level security replayed from SQL migrations")
    else:
        out["not_checked"].append("row-level security in migrations: no SQL migration files found")

    if stack["nextjs"]:
        out["checked"].append("Next.js route handlers (app/ route.* and pages/api) for an auth call")
    elif stack["node"]:
        out["not_checked"].append("route auth for non-Next.js Node servers (Express, Fastify, ...): routes are not detected")
    if stack["python"]:
        out["checked"].append("Python decorator routes (FastAPI, Flask, Starlette style) for an auth dependency")
        if stack["django"]:
            out["not_checked"].append("Django URLconf views: routes are not detected")
    if not (stack["node"] or stack["python"]):
        out["not_checked"].append("no supported stack detected (Next.js/TypeScript or Python): only generic checks ran")
    out["checked"] += ["secret keys in client components", "raw HTML injection", "public env vars named like secrets",
                       "dynamic code execution", "SQL built from strings", "largest files"]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Whole-repo security and architecture pattern checks (leads, not verdicts).")
    ap.add_argument("--path", required=True, help="repository root")
    ap.add_argument("--auth-pattern", action="append", default=[], help="extra regex that counts as an auth check")
    ap.add_argument("--service-key-pattern", action="append", default=[], help="extra regex for a server-only secret")
    ap.add_argument("--migrations-dir", action="append", default=[], help="SQL migrations directory (repeatable)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    root = Path(args.path)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    res = scan(root, args.auth_pattern, args.service_key_pattern, args.migrations_dir or None)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        for k, v in res.items():
            if k != "stack":
                print(f"{k}: {v if isinstance(v, int) else len(v)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
