"""Shared helpers for the readiness-review scanners: config loading, stack
detection, and file walking. Standard library only, except that the config
file is YAML, so load_config() needs PyYAML (the scanners that read config
declare it as an inline uv dependency).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from functools import lru_cache
from pathlib import Path

JS_CODE = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
PY_CODE = {".py"}
TEMPLATES = {".html", ".jinja", ".jinja2", ".j2", ".vue", ".svelte"}
# Never walked: dependencies, build output, virtualenvs, VCS metadata.
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "out", ".venv", "venv", "env",
             "__pycache__", ".turbo", ".vercel", "coverage", ".mypy_cache", ".pytest_cache",
             ".ruff_cache", "site-packages", ".tox", "vendor"}
TEST_PATH = re.compile(r"(__tests__|/tests?/|\.test\.|\.spec\.|/e2e/|/fixtures?/|\.stories\.|/test_[^/]*\.py$|_test\.py$)")

CONFIG_NAMES = (".readiness-review.yaml", ".readiness-review.yml", ".readiness-review.json")


def find_config(repo: Path) -> Path | None:
    for name in CONFIG_NAMES:
        p = repo / name
        if p.is_file():
            return p
    return None


def load_config(path: Path | None) -> dict:
    """Parse the per-repo config. Missing file -> {} (every section optional)."""
    if path is None:
        return {}
    text = path.read_text()
    if path.suffix == ".json":
        return json.loads(text) or {}
    import yaml  # PyYAML; declared as an inline dependency by callers
    return yaml.safe_load(text) or {}


def read(p: Path) -> str:
    try:
        return p.read_text(errors="replace")
    except OSError:
        return ""


@lru_cache(maxsize=8)
def repo_files(root: Path) -> tuple[str, ...]:
    """Every file the repo would commit: tracked plus untracked-but-not-ignored (read-only
    `git ls-files`). Outside a git repo, a walk that skips hidden, dependency, and build dirs."""
    try:
        r = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                           capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            return tuple(sorted({f for f in r.stdout.split("\0") if f}))
    except (OSError, subprocess.SubprocessError):
        pass
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        out += [str((Path(dirpath) / n).relative_to(root)) for n in filenames]
    return tuple(sorted(out))


def walk(root: Path, suffixes: set[str], include_tests: bool = False):
    """Yield the repo's files with a matching suffix, skipping dependency, build, and minified files."""
    for rel in repo_files(root):
        parts = rel.split("/")
        if any(d in SKIP_DIRS for d in parts[:-1]) or rel.endswith((".min.js", ".min.css")):
            continue
        p = root / rel
        if p.suffix not in suffixes or not p.is_file() or p.is_symlink():
            continue
        if not include_tests and TEST_PATH.search("/" + rel):
            continue
        yield p


def detect_stack(root: Path) -> dict:
    """Which of the supported stacks this repo looks like. More than one can be true."""
    pkg = read(root / "package.json")
    py = " ".join(read(root / n) for n in ("pyproject.toml", "requirements.txt", "setup.py", "setup.cfg", "Pipfile"))
    return {
        "nextjs": '"next"' in pkg,
        "node": bool(pkg),
        "python": bool(py.strip()) or any(True for _ in _first(walk(root, PY_CODE))),
        "fastapi": "fastapi" in py.lower(),
        "flask": "flask" in py.lower(),
        "django": "django" in py.lower(),
        "supabase": (root / "supabase").is_dir() or "@supabase/" in pkg or "supabase" in py.lower(),
    }


def _first(it):
    for x in it:
        yield x
        return
