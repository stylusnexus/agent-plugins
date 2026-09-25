#!/usr/bin/env python3
"""gh_facts.py -- read-only GitHub and git facts for the readiness review.

Every call goes through an allowlist: `gh api` as GET only, `gh issue list`,
`gh run list`, and `git log` / `git remote get-url`. Anything else raises
before a process starts, so this script cannot file, comment, label, push,
or change a repository. A source that fails (missing permission, no network,
Dependabot not enabled) is reported "NOT VERIFIED: <reason>" and the rest
still run.

Usage:
  gh_facts.py --path <repo> [--repo owner/name] [--label L ...] [--blocker N ...]
              [--risky-paths REGEX] [--days 7] [--json]
Exit 0 = ran (individual sources may be NOT VERIFIED).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import date, timedelta

GH_READ = {("issue", "list"), ("run", "list")}
GIT_READ = {("log",), ("remote", "get-url")}
GH_WRITE_FLAGS = {"-f", "-F", "--field", "--raw-field", "--input"}


class NotReadOnly(ValueError):
    """A command outside the read-only allowlist was requested."""


def check_gh(args: list[str]) -> None:
    if not args:
        raise NotReadOnly("empty gh command")
    if args[0] == "api":
        if any(a.split("=", 1)[0] in GH_WRITE_FLAGS for a in args):
            raise NotReadOnly("gh api with body fields sends a POST")
        for i, a in enumerate(args):
            if a in ("-X", "--method"):
                method = args[i + 1] if i + 1 < len(args) else ""
            elif a.startswith("--method=") or (a.startswith("-X") and len(a) > 2):
                method = a.split("=", 1)[-1] if "=" in a else a[2:]
            else:
                continue
            if method.upper() != "GET":
                raise NotReadOnly(f"gh api method {method!r} is not GET")
        if any("method-override" in a.lower() for a in args):
            raise NotReadOnly("gh api with a method-override header")
        if any(a.lower().rstrip("/").split("?")[0].endswith("graphql") for a in args[1:]):
            raise NotReadOnly("gh api graphql can mutate; not allowed")
        return
    if tuple(args[:2]) not in GH_READ:
        raise NotReadOnly(f"gh {' '.join(args[:2])} is not a read-only command")


def check_git(args: list[str]) -> None:
    if args == ["remote"]:  # bare `git remote` only lists names
        return
    if tuple(args[:1]) not in GIT_READ and tuple(args[:2]) not in GIT_READ:
        raise NotReadOnly(f"git {' '.join(args[:2])} is not a read-only command")


def gh(args: list[str]) -> str:
    check_gh(args)
    r = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError((r.stderr.strip().splitlines() or ["gh failed"])[-1][:200])
    return r.stdout


def git(path: str, args: list[str]) -> str:
    check_git(args)
    r = subprocess.run(["git", "-C", path, *args], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError((r.stderr.strip().splitlines() or ["git failed"])[-1][:200])
    return r.stdout


def fact(fn):
    try:
        return fn()
    except FileNotFoundError as e:
        return f"NOT VERIFIED: {e.filename} is not installed"
    except Exception as e:  # permission, network, feature disabled: report, keep going
        return f"NOT VERIFIED: {e}"


def repo_from_remote(path: str) -> str:
    """owner/name from origin, else from the first remote that points at GitHub."""
    names = git(path, ["remote"]).split()
    for name in (["origin"] if "origin" in names else []) + [n for n in names if n != "origin"]:
        m = re.search(r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$", git(path, ["remote", "get-url", name]).strip())
        if m:
            return m.group(1)
    raise RuntimeError("no GitHub remote found; set github.repo in the config")


def ci(repo: str):
    runs = json.loads(gh(["run", "list", "-R", repo, "--limit", "40", "--json", "workflowName,conclusion,createdAt"]))
    by: dict[str, Counter] = {}
    latest: dict[str, str] = {}
    for r in runs:
        if r.get("conclusion") not in ("success", "failure"):
            continue
        w = r["workflowName"]
        by.setdefault(w, Counter())[r["conclusion"]] += 1
        latest.setdefault(w, f"{r['conclusion']} {r['createdAt'][:10]}")
    return {w: f"{c['success']}/{sum(c.values())} passed, latest {latest[w]}" for w, c in by.items()} or "no finished runs"


def dependabot(repo: str):
    out = gh(["api", f"repos/{repo}/dependabot/alerts?state=open&per_page=100", "--paginate",
              "--jq", ".[] | .security_advisory.severity"])
    return dict(Counter(x for x in out.split() if x)) or "no open alerts"


def label_counts(repo: str, labels: list[str]):
    return {l: len(json.loads(gh(["issue", "list", "-R", repo, "--state", "open", "--label", l,
                                  "--limit", "500", "--json", "number"]))) for l in labels}


def blockers(repo: str, numbers: list[int]):
    rows = []
    for n in numbers:
        i = json.loads(gh(["api", f"repos/{repo}/issues/{int(n)}"]))
        rows.append(f"#{i['number']} {i['state'].upper()} {i['title']}")
    return rows


def titles(repo: str, days: int = 90):
    since = (date.today() - timedelta(days=days)).isoformat()
    rows = json.loads(gh(["issue", "list", "-R", repo, "--state", "open", "--limit", "1500", "--json", "number,title"]))
    rows += json.loads(gh(["issue", "list", "-R", repo, "--state", "closed", "--search", f"closed:>={since}",
                           "--limit", "1500", "--json", "number,title"]))
    return [f"#{r['number']} {r['title']}" for r in rows]


def risky_changes(path: str, pattern: str, days: int):
    rx = re.compile(pattern)
    out = git(path, ["log", f"--since={days}.days", "--numstat", "--format="])
    changed: Counter = Counter()
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and rx.search(parts[2]):
            added = int(parts[0]) if parts[0].isdigit() else 0
            removed = int(parts[1]) if parts[1].isdigit() else 0
            changed[parts[2]] += added + removed
    return [f"{n} {f}" for f, n in changed.most_common(40)]


def gather(path: str, repo: str | None, labels, numbers, risky: str | None, days: int) -> dict:
    if not repo:
        repo = fact(lambda: repo_from_remote(path))
    out = {"repo": repo}
    if isinstance(repo, str) and repo.startswith("NOT VERIFIED"):
        for k in ("ci", "dependabot", "label_counts", "launch_blockers", "issue_titles"):
            out[k] = "NOT VERIFIED: no GitHub repository identified"
    else:
        out["ci"] = fact(lambda: ci(repo))
        out["dependabot"] = fact(lambda: dependabot(repo))
        out["label_counts"] = fact(lambda: label_counts(repo, labels)) if labels else "none configured"
        out["launch_blockers"] = fact(lambda: blockers(repo, numbers)) if numbers else "none configured"
        out["issue_titles"] = fact(lambda: titles(repo))
    out["risky_changes"] = fact(lambda: risky_changes(path, risky, days)) if risky else "no risky_paths configured"
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Read-only GitHub and git facts for the readiness review.")
    ap.add_argument("--path", required=True)
    ap.add_argument("--repo", help="owner/name (default: parsed from the origin remote)")
    ap.add_argument("--label", action="append", default=[], help="count open issues with this label")
    ap.add_argument("--blocker", action="append", type=int, default=[], help="launch-blocker issue number")
    ap.add_argument("--risky-paths", help="regex over changed file paths")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    res = gather(args.path, args.repo, args.label, args.blocker, args.risky_paths, args.days)
    print(json.dumps(res, indent=2) if args.json else "\n".join(f"{k}: {v}" for k, v in res.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
