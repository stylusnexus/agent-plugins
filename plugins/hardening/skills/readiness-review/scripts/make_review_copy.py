#!/usr/bin/env python3
"""make_review_copy.py -- a throwaway copy of the repo for the reviewer to read.

Copies the repository's own files (what `git ls-files` lists: tracked plus
untracked-but-not-ignored) into a new temporary directory, WITHOUT .git,
any .env* file, credential files (SECRET_NAMES), dependency and build
directories, symlinks (a link could point back at a secret outside the
copy), binary files, and files over the size cap. Then walks the copy and
refuses to hand it over if any excluded name survived. Prints the copy's
path on stdout and a JSON count of what was skipped on stderr. The
original repo is only read.

Usage: make_review_copy.py --path <repo> [--max-file-bytes N]
Exit 0 = copy ready (path on stdout); 1 = verification failed (copy deleted).
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rr_common import SKIP_DIRS, repo_files  # noqa: E402


# Credential files and folders, matched against every path segment (fnmatch, case-insensitive).
SECRET_NAMES = (
    ".git", ".env*", ".npmrc", ".pypirc", ".netrc", ".git-credentials", ".aws", ".ssh",
    "*.pem", "*.key", "*.p12", "*.pfx", "id_rsa*", "id_ed25519*",
    "*credentials*.json", "*service-account*.json",
)
# Matched against the whole relative path instead: only this file in this folder is a secret.
SECRET_PATHS = ("*.docker/config.json", ".docker/config.json")
BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico", ".bmp", ".tif", ".tiff", ".psd",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp3", ".wav", ".ogg", ".flac", ".m4a", ".mp4", ".mov", ".webm", ".avi", ".mkv",
    ".zip", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar", ".tar", ".jar",
    ".glb", ".gltf", ".wasm", ".onnx", ".bin", ".safetensors", ".pt", ".pth", ".ckpt", ".h5", ".npy",
    ".pdf", ".sqlite", ".db", ".so", ".dylib", ".dll", ".exe", ".class", ".pyc",
}
DEFAULT_MAX_FILE_BYTES = 1_000_000


def excluded(name: str) -> bool:
    n = name.lower()
    return n in SKIP_DIRS or any(fnmatch.fnmatch(n, pat) for pat in SECRET_NAMES)


def secret_path(rel: str) -> bool:
    return any(fnmatch.fnmatch(rel.lower(), pat) for pat in SECRET_PATHS)


def is_binary(p: Path) -> bool:
    if p.suffix.lower() in BINARY_EXT:
        return True
    try:
        with open(p, "rb") as fh:
            return b"\0" in fh.read(8192)
    except OSError:
        return True


def copy(src: Path, dest: Path, max_bytes: int = DEFAULT_MAX_FILE_BYTES) -> dict:
    """Copy the reviewable files; return counts of what was skipped and why."""
    skipped = {"secret_or_excluded": 0, "symlink": 0, "binary": 0, "too_large": 0,
               "binary_bytes": 0, "too_large_bytes": 0}
    for rel in repo_files(src):
        parts = rel.split("/")
        if any(excluded(x) for x in parts) or secret_path(rel):
            skipped["secret_or_excluded"] += 1
            continue
        p = src / rel
        # a symlinked file, or a file reached through a symlinked directory, is skipped
        if any((src / "/".join(parts[:i])).is_symlink() for i in range(1, len(parts) + 1)):
            skipped["symlink"] += 1
            continue
        if not p.is_file():
            continue
        size = p.stat().st_size
        if size > max_bytes:
            skipped["too_large"] += 1
            skipped["too_large_bytes"] += size
            continue
        if is_binary(p):
            skipped["binary"] += 1
            skipped["binary_bytes"] += size
            continue
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest / rel)
    return skipped


def leftovers(dest: Path) -> list[str]:
    bad = []
    for dirpath, dirnames, filenames in os.walk(dest):
        for n in dirnames + filenames:
            p = Path(dirpath) / n
            rel = str(p.relative_to(dest))
            if (n.lower() not in SKIP_DIRS and excluded(n)) or secret_path(rel) or p.is_symlink():
                bad.append(str(p.relative_to(dest)))
    return bad


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Make a throwaway, secret-free copy of a repo for review.")
    ap.add_argument("--path", required=True)
    ap.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES,
                    help="skip any file larger than this (operator's choice; default 1 MB)")
    args = ap.parse_args(argv)
    src = Path(args.path).resolve()
    if not src.is_dir():
        print(f"not a directory: {src}", file=sys.stderr)
        return 2
    dest = Path(tempfile.mkdtemp(prefix="readiness-review-"))
    skipped = copy(src, dest, args.max_file_bytes)
    bad = leftovers(dest)
    if bad:
        shutil.rmtree(dest, ignore_errors=True)
        print(f"refusing: the copy still held {', '.join(bad[:5])}; deleted it", file=sys.stderr)
        return 1
    print(dest)
    print(json.dumps({"skipped": skipped, "max_file_bytes": args.max_file_bytes}), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
