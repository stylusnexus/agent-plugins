#!/usr/bin/env python3
"""findings.py -- turn the reviewer's findings into a ready-to-file list. Files nothing.

Reads the draft report on stdin, takes the JSON list under "## Findings to
file", and rewrites that section as a severity-ordered Markdown list plus a
clean JSON block a person can file from. Each finding is annotated, never
dropped:
  - "known #N"               the reviewer said it duplicates #N
  - "looks like existing #N" its normalized title matches an existing issue
                             (open or closed in the last 90 days), or its
                             fingerprint already appears in an issue body
Titles and bodies are scrubbed of secrets. Every body carries a fingerprint
comment, so once a person files it, the next run recognizes it.

The only GitHub call is the optional fingerprint search (`gh issue list
--search`), through the same read-only allowlist as gh_facts.py.

Usage: findings.py --titles FILE [--repo owner/name] [--date YYYY-MM-DD] < draft.md > report.md
Exit 0 = ran (a missing or malformed findings block is reported in the section).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gh_facts import gh  # noqa: E402  (read-only allowlisted gh)
from redaction import redact  # noqa: E402

SEVERITIES = ["critical", "high", "medium", "low"]
KINDS = {"security", "architecture", "database", "incomplete", "accessibility", "usability", "finish"}
SECTION = re.compile(r"^## Findings to file\s*$", re.M)
BLOCK = re.compile(r"```json\s*(.*?)\s*```", re.S)


def normalize(title: str) -> str:
    t = re.sub(r"^\w+(\([^)]*\))?!?:\s*", "", title.lower())  # drop "fix(area): "
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def fingerprint(f: dict) -> str:
    first = (f.get("files") or [""])[0].split(":")[0]
    return hashlib.sha256(f"{normalize(f['title'])}|{first}".encode()).hexdigest()[:12]


def parse(report: str) -> tuple[list[dict], str | None, int]:
    """(findings, error, section_start). section_start is -1 when the heading is missing."""
    m = SECTION.search(report)
    if not m:
        return [], "the report has no '## Findings to file' section", -1
    b = BLOCK.search(report, m.end())
    if not b:
        return [], "no JSON block under '## Findings to file'", m.start()
    try:
        data = json.loads(b.group(1))
    except ValueError as e:
        return [], f"findings JSON unreadable ({e})", m.start()
    if not isinstance(data, list):
        return [], "findings JSON is not a list", m.start()
    ok = [f for f in data if isinstance(f, dict) and isinstance(f.get("title"), str) and f["title"].strip()
          and f.get("severity") in SEVERITIES]
    skipped = len(data) - len(ok)
    return ok, (f"{skipped} malformed finding(s) dropped (no title or unknown severity)" if skipped else None), m.start()


def load_titles(path: str) -> dict[str, int]:
    """normalized title -> issue number, from a JSON list or plain lines of '#N title'."""
    text = Path(path).read_text()
    try:
        rows = json.loads(text)
        rows = rows if isinstance(rows, list) else []
    except ValueError:
        rows = text.splitlines()
    out = {}
    for r in rows:
        m = re.match(r"#(\d+)\s+(.*)", str(r).strip())
        if m:
            out.setdefault(normalize(m.group(2)), int(m.group(1)))
    return out


def annotate(findings: list[dict], titles: dict[str, int], repo: str | None) -> list[dict]:
    out = []
    for f in findings:
        f = dict(f)
        f["fingerprint"] = fingerprint(f)
        note = None
        if f.get("known"):
            note = f"known #{f['known']}"
        elif normalize(f["title"]) in titles:
            note = f"looks like existing #{titles[normalize(f['title'])]} (same title)"
        elif repo:
            try:
                hit = gh(["issue", "list", "-R", repo, "--state", "all", "--search", f"{f['fingerprint']} in:body",
                          "--json", "number", "--jq", ".[0].number // empty"]).strip()
                if hit:
                    note = f"looks like existing #{hit} (same fingerprint)"
            except Exception as e:
                f["fingerprint_check"] = f"not checked: {e}"
        f["looks_like"] = note
        out.append(f)
    out.sort(key=lambda f: (f["looks_like"] is not None, SEVERITIES.index(f["severity"])))
    return out


def render(findings: list[dict], note: str | None, run_date: str) -> str:
    lines = ["## Findings to file", "",
             "Nothing was filed. This review only read. File the ones you agree with yourself; "
             "each body ends with a fingerprint so the next run recognizes it.", ""]
    if note:
        lines += [f"> {note}", ""]
    if not findings:
        lines.append("No findings.")
        return "\n".join(lines) + "\n"
    clean = []
    for i, f in enumerate(findings, 1):
        title = redact(f["title"][:200])[0]
        files = ", ".join(str(x) for x in (f.get("files") or []))
        body = redact(f"{f.get('body', '')}\n\nFiles: {files}\n\nFound by readiness-review, {run_date}.\n"
                      f"<!-- readiness-review-fp: {f['fingerprint']} -->")[0]
        tag = f" -- {f['looks_like']}" if f["looks_like"] else ""
        lines.append(f"{i}. **{f['severity']}** ({f.get('kind', 'unspecified')}) {title}{tag}")
        clean.append({"title": title, "kind": f.get("kind"), "severity": f["severity"], "files": f.get("files") or [],
                      "body": body, "looks_like": f["looks_like"], "fingerprint": f["fingerprint"]})
    lines += ["", "```json", json.dumps(clean, indent=2), "```"]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Annotate and render the findings list. Files nothing.")
    ap.add_argument("--titles", required=True, help="existing issue titles: JSON list or lines of '#N title'")
    ap.add_argument("--repo", help="owner/name, to also search issue bodies for each fingerprint (read-only)")
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args(argv)
    report = sys.stdin.read()
    findings, err, start = parse(report)
    section = render(annotate(findings, load_titles(args.titles), args.repo), err, args.date)
    if start < 0:
        sys.stdout.write(report.rstrip() + "\n\n" + section)
    else:
        sys.stdout.write(report[:start] + section)
    return 0


if __name__ == "__main__":
    sys.exit(main())
