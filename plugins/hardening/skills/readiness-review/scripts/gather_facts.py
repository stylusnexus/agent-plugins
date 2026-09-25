#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml>=6", "psycopg[binary]>=3.1"]
# ///
"""gather_facts.py -- run every read-only fact source and print one JSON bundle.

Reads the target repo's .readiness-review.yaml (every section optional),
picks this run's deep-read area, and runs, each as its own subprocess:
security_scan, completeness_scan, gh_facts, and -- only when the config
names a database variable -- db_facts. The database connection string is
loaded inside db_facts' own process from the repo's local .env and never
reaches this bundle. A source that fails is recorded as "NOT VERIFIED" and
the rest still run. Nothing is written to the target repo.

Usage: uv run gather_facts.py --path <repo> [--config FILE] [--week N] [--area NAME]
Exit 0 = ran; 2 = bad arguments.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gh_facts import repo_from_remote  # noqa: E402
from rr_common import detect_stack, find_config, inside, load_config, regex_problem, symlinked_component  # noqa: E402


def report_dir(repo: Path, flag: str | None) -> Path:
    """Where the report goes. Chosen by the OPERATOR (flag, then READINESS_REPORT_DIR, then a fixed
    folder in their home), never by the reviewed repo. Refused if it is inside the repo or reached
    through a symlink."""
    raw = flag or os.environ.get("READINESS_REPORT_DIR") or f"~/.readiness-review/reports/{repo.name}"
    d = Path(os.path.abspath(Path(raw).expanduser()))
    link = symlinked_component(d)
    if link:
        raise SystemExit(f"refusing report dir {d}: {link} is a symlink")
    if d.resolve() == repo or repo in d.resolve().parents:
        raise SystemExit(f"refusing report dir {d}: it is inside the reviewed repo")
    return d


def safe_area(area: dict | None) -> dict | None:
    """Drop area paths that are absolute or climb out of the repo: the reviewer reads only its copy."""
    if not area:
        return area
    paths = [x for x in area.get("paths") or [] if isinstance(x, str) and not Path(x).is_absolute()
             and ".." not in Path(x).parts]
    dropped = len(area.get("paths") or []) - len(paths)
    return {**area, "paths": paths, **({"paths_dropped_unsafe": dropped} if dropped else {})}


def pick_area(areas: list, week: int, name: str | None = None) -> dict | None:
    """This run's area: by name if given, else ISO week mod the number of areas."""
    if not areas:
        return None
    if name:
        for i, a in enumerate(areas):
            if a.get("name", "").lower() == name.lower():
                return {"index": i, "of": len(areas), **a}
        raise SystemExit(f"no review area named {name!r}")
    i = week % len(areas)
    return {"week": week, "index": i, "of": len(areas), **areas[i]}


def run_json(args: list[str], env=None) -> dict | str:
    try:
        r = subprocess.run([sys.executable, *args], capture_output=True, text=True, timeout=600, env=env)
    except subprocess.TimeoutExpired:
        return f"NOT VERIFIED: {Path(args[0]).name} timed out"
    try:
        return json.loads(r.stdout)
    except ValueError:
        tail = (r.stderr.strip().splitlines() or ["no output"])[-1][:200]
        return f"NOT VERIFIED: {Path(args[0]).name} exited {r.returncode} ({tail})"


def github_repo(repo: Path, cfg_repo, flag: str | None, ignored: list) -> str | None:
    """The operator's --github-repo, else the checkout's own GitHub remote. A config value that
    names anything else is ignored: the reviewed repo must not aim the reads at another repo."""
    if flag:
        return flag
    try:
        own = repo_from_remote(str(repo))
    except Exception:
        own = None
    if cfg_repo and (not own or str(cfg_repo).lower() != own.lower()):
        ignored.append(f"github.repo {cfg_repo!r}: not this checkout's own GitHub remote (use --github-repo)")
    return own


def safe_patterns(values, key: str, ignored: list) -> list[str]:
    out = []
    for v in values or []:
        why = regex_problem(v)
        if why:
            ignored.append(f"{key} {str(v)[:60]!r}: {why}")
        else:
            out.append(v)
    return out


def gather(repo: Path, cfg: dict, week: int, area_name: str | None, db_env_var: str | None = None,
           github_repo_flag: str | None = None) -> dict:
    scan_cfg = cfg.get("scan") or {}
    ignored = []
    sec_args = [str(HERE / "security_scan.py"), "--path", str(repo), "--json"]
    for p in safe_patterns(scan_cfg.get("auth_patterns"), "scan.auth_patterns", ignored):
        sec_args += ["--auth-pattern", p]
    for p in safe_patterns(scan_cfg.get("service_key_patterns"), "scan.service_key_patterns", ignored):
        sec_args += ["--service-key-pattern", p]
    if "report_dir" in cfg:
        ignored.append("report_dir: the report location is the operator's choice (--report-dir), not the repo's")
    for d in scan_cfg.get("migrations_dirs") or []:
        if inside(repo, d):
            sec_args += ["--migrations-dir", d]
        else:
            ignored.append(f"scan.migrations_dirs {d!r}: outside the repo")

    out: dict = {
        "repo_path": str(repo),
        "product": cfg.get("product") or {},
        "stack": detect_stack(repo),
        "area": safe_area(pick_area(cfg.get("review_areas") or [], week, area_name)),
        "security_scan": run_json(sec_args),
        "completeness_scan": run_json([str(HERE / "completeness_scan.py"), "--path", str(repo), "--json"]),
    }

    gh_cfg = cfg.get("github") or {}
    gh_args = [str(HERE / "gh_facts.py"), "--path", str(repo), "--json", "--days", str(gh_cfg.get("days", 7))]
    gh_repo = github_repo(repo, gh_cfg.get("repo"), github_repo_flag, ignored)
    if gh_repo:
        gh_args += ["--repo", gh_repo]
    for l in gh_cfg.get("count_labels") or []:
        gh_args += ["--label", l]
    for n in (cfg.get("launch_blockers") or {}).get("issues") or []:
        gh_args += ["--blocker", str(n)]
    risky = safe_patterns([cfg["risky_paths"]] if cfg.get("risky_paths") else [], "risky_paths", ignored)
    if risky:
        gh_args += ["--risky-paths", risky[0]]
    out["github"] = run_json(gh_args)
    out["launch_blockers_note"] = (cfg.get("launch_blockers") or {}).get("note")

    # The repo config may name a variable, but it is looked up ONLY in the repo's own .env file
    # (inside the repo, no symlink escape), never in the operator's environment -- otherwise a
    # reviewed repo could point this at any database the operator has credentials for. The
    # operator widens that with --db-env-var.
    db = cfg.get("database") or {}
    env_file = inside(repo, db.get("env_file", ".env"))
    if not (db_env_var or db.get("url_env")):
        out["live_database"] = {"status": "NOT CONFIGURED", "reason": "no database.url_env in the config"}
    elif not db_env_var and not env_file:
        out["live_database"] = {"status": "NOT VERIFIED", "reason": "database.env_file is outside the repo; ignored"}
    else:
        db_args = [str(HERE / "db_facts.py"), "--env-var", db_env_var or db["url_env"], "--json"]
        if env_file:
            db_args += ["--env-file", str(env_file)]
        if not db_env_var:
            db_args += ["--env-file-only"]
        for s in db.get("schemas") or []:
            db_args += ["--schema", s]
        for r in db.get("public_roles") or []:
            db_args += ["--public-role", r]
        sec = out["security_scan"]
        with tempfile.TemporaryDirectory() as tmp:
            if isinstance(sec, dict) and "public_tables_in_migrations" in sec:
                mt = Path(tmp) / "migration-tables.json"
                mt.write_text(json.dumps(sec["public_tables_in_migrations"]))
                db_args += ["--migration-tables", str(mt)]
            out["live_database"] = run_json(db_args, env=dict(os.environ))

    out["config_values_ignored"] = ignored
    sec = out["security_scan"]
    if isinstance(sec, dict) and sec.get("routes_total") == 0 and (out["stack"]["nextjs"] or out["stack"]["fastapi"]
                                                                    or out["stack"]["flask"]):
        out["warning"] = ("a web stack was detected but the scan found 0 routes: the checkout may be empty, "
                          "or routes live somewhere the scanner doesn't look. Check before trusting 'no findings'.")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Gather every read-only fact for a readiness review as one JSON bundle.")
    ap.add_argument("--path", required=True, help="the target repository (read-only)")
    ap.add_argument("--config", help="config file (default: .readiness-review.yaml in the repo)")
    ap.add_argument("--week", type=int, default=date.today().isocalendar()[1])
    ap.add_argument("--area", help="review this area by name instead of the week's rotation")
    ap.add_argument("--report-dir", help="where the report goes (default: $READINESS_REPORT_DIR, "
                                         "else ~/.readiness-review/reports/<repo>); never taken from the repo")
    ap.add_argument("--github-repo", help="owner/name to read, overriding the checkout's own GitHub remote")
    ap.add_argument("--db-env-var", help="operator's choice of variable holding a read-only connection string; "
                                         "looked up in the environment, then the repo's .env")
    args = ap.parse_args(argv)
    repo = Path(args.path).resolve()
    if not repo.is_dir():
        print(f"not a directory: {repo}", file=sys.stderr)
        return 2
    cfg_path = Path(args.config) if args.config else find_config(repo)
    cfg = load_config(cfg_path)
    out_dir = report_dir(repo, args.report_dir)
    res = gather(repo, cfg, args.week, args.area, args.db_env_var, args.github_repo)
    res["report_dir"] = str(out_dir)
    res["config"] = str(cfg_path) if cfg_path else "none found: defaults used"
    # passed through untouched for the product walk; the scripts never act on them
    for k in ("product_walk", "test_account", "exercise"):
        res[k] = cfg.get(k) or {}
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
