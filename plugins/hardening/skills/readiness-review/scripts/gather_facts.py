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
from rr_common import detect_stack, find_config, load_config  # noqa: E402


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


def gather(repo: Path, cfg: dict, week: int, area_name: str | None) -> dict:
    scan_cfg = cfg.get("scan") or {}
    sec_args = [str(HERE / "security_scan.py"), "--path", str(repo), "--json"]
    for p in scan_cfg.get("auth_patterns") or []:
        sec_args += ["--auth-pattern", p]
    for p in scan_cfg.get("service_key_patterns") or []:
        sec_args += ["--service-key-pattern", p]
    for d in scan_cfg.get("migrations_dirs") or []:
        sec_args += ["--migrations-dir", d]

    out: dict = {
        "repo_path": str(repo),
        "product": cfg.get("product") or {},
        "report_dir": str(Path(cfg.get("report_dir") or f"~/readiness-reports/{repo.name}").expanduser()),
        "stack": detect_stack(repo),
        "area": pick_area(cfg.get("review_areas") or [], week, area_name),
        "security_scan": run_json(sec_args),
        "completeness_scan": run_json([str(HERE / "completeness_scan.py"), "--path", str(repo), "--json"]),
    }

    gh_cfg = cfg.get("github") or {}
    gh_args = [str(HERE / "gh_facts.py"), "--path", str(repo), "--json", "--days", str(gh_cfg.get("days", 7))]
    if gh_cfg.get("repo"):
        gh_args += ["--repo", gh_cfg["repo"]]
    for l in gh_cfg.get("count_labels") or []:
        gh_args += ["--label", l]
    for n in (cfg.get("launch_blockers") or {}).get("issues") or []:
        gh_args += ["--blocker", str(n)]
    if cfg.get("risky_paths"):
        gh_args += ["--risky-paths", cfg["risky_paths"]]
    out["github"] = run_json(gh_args)
    out["launch_blockers_note"] = (cfg.get("launch_blockers") or {}).get("note")

    db = cfg.get("database") or {}
    if not db.get("url_env"):
        out["live_database"] = {"status": "NOT CONFIGURED", "reason": "no database.url_env in the config"}
    else:
        db_args = [str(HERE / "db_facts.py"), "--env-var", db["url_env"], "--json",
                   "--env-file", str(repo / db.get("env_file", ".env"))]
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
    args = ap.parse_args(argv)
    repo = Path(args.path).resolve()
    if not repo.is_dir():
        print(f"not a directory: {repo}", file=sys.stderr)
        return 2
    cfg_path = Path(args.config) if args.config else find_config(repo)
    cfg = load_config(cfg_path)
    res = gather(repo, cfg, args.week, args.area)
    res["config"] = str(cfg_path) if cfg_path else "none found: defaults used"
    # passed through untouched for the product walk; the scripts never act on them
    for k in ("product_walk", "test_account", "exercise"):
        res[k] = cfg.get(k) or {}
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
