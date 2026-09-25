#!/usr/bin/env python3
"""make_review_copy.py -- a throwaway copy of the repo for the reviewer to read.

Copies the repository's own files (what `git ls-files` lists: tracked plus
untracked-but-not-ignored) into a new temporary directory, WITHOUT .git,
without any .env* file, without dependency and build directories, and
without symlinks (a link could point back at a secret outside the copy). Then walks
the copy and refuses to hand it over if any .env* file or .git survived.
Prints the copy's path. The original repo is only read.

Usage: make_review_copy.py --path <repo>
Exit 0 = copy ready (path on stdout); 1 = verification failed (copy deleted).
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rr_common import SKIP_DIRS, repo_files  # noqa: E402


def excluded(name: str) -> bool:
    return name == ".git" or name.startswith(".env") or name in SKIP_DIRS


def copy(src: Path, dest: Path) -> None:
    for rel in repo_files(src):
        parts = rel.split("/")
        if any(excluded(x) for x in parts):
            continue
        p = src / rel
        # a symlinked file, or a file reached through a symlinked directory, is skipped
        if any((src / "/".join(parts[:i])).is_symlink() for i in range(1, len(parts) + 1)) or not p.is_file():
            continue
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest / rel)


def leftovers(dest: Path) -> list[str]:
    bad = []
    for dirpath, dirnames, filenames in os.walk(dest):
        for n in dirnames + filenames:
            p = Path(dirpath) / n
            if n == ".git" or n.startswith(".env") or p.is_symlink():
                bad.append(str(p.relative_to(dest)))
    return bad


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Make a throwaway, secret-free copy of a repo for review.")
    ap.add_argument("--path", required=True)
    args = ap.parse_args(argv)
    src = Path(args.path).resolve()
    if not src.is_dir():
        print(f"not a directory: {src}", file=sys.stderr)
        return 2
    dest = Path(tempfile.mkdtemp(prefix="readiness-review-"))
    copy(src, dest)
    bad = leftovers(dest)
    if bad:
        shutil.rmtree(dest, ignore_errors=True)
        print(f"refusing: the copy still held {', '.join(bad[:5])}; deleted it", file=sys.stderr)
        return 1
    print(dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
