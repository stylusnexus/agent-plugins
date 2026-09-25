#!/usr/bin/env python3
"""write_report.py -- redact secrets, then write the report without ever overwriting one.

Reads the finished report on stdin, scrubs known secret shapes, and creates
<out-dir>/<date>-<slug>-readiness.md. If that name exists, it tries -2, -3,
... Creation is exclusive (O_EXCL), so an earlier report is never replaced,
even by a run racing this one. Prints the path written and the secret
classes that were redacted.

Usage: write_report.py --out-dir DIR --slug NAME [--date YYYY-MM-DD] < report.md
Exit 0 = written.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from redaction import redact  # noqa: E402


def write_new(out_dir: Path, stem: str, text: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 1
    while True:
        p = out_dir / (f"{stem}.md" if n == 1 else f"{stem}-{n}.md")
        try:
            fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            n += 1
            continue
        with os.fdopen(fd, "w") as fh:
            fh.write(text)
        return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Redact and write a readiness report; never overwrites.")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--slug", required=True, help="short name for the product or repo")
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args(argv)
    slug = re.sub(r"[^a-z0-9-]+", "-", args.slug.lower()).strip("-") or "repo"
    text, classes = redact(sys.stdin.read())
    p = write_new(Path(args.out_dir).expanduser(), f"{args.date}-{slug}-readiness", text)
    print(p)
    if classes:
        print(f"redacted before writing: {', '.join(classes)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
