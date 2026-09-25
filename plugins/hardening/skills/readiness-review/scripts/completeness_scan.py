#!/usr/bin/env python3
"""completeness_scan.py -- leads for unfinished features and code-visible accessibility gaps.

Read-only. Looks for routes that answer "not implemented", thrown or raised
not-implemented errors, UI handlers that do nothing, "coming soon" text,
TODO/FIXME density, images without alt text, and icon-only buttons without a
label. Test files are skipped. Leads, not verdicts: the reviewer triages.

Supported: TypeScript/JavaScript (incl. JSX/TSX), Python, and HTML-style
templates. Accessibility checks only run on markup (JSX/TSX, templates).

Usage: completeness_scan.py --path <repo> [--json]
Exit 0 = the scan ran; 2 = bad arguments.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rr_common import JS_CODE, PY_CODE, TEMPLATES, detect_stack, read, walk  # noqa: E402

MARKUP = {".tsx", ".jsx"} | TEMPLATES
NOT_IMPL_ROUTE = re.compile(r"status(?:_code)?\s*[:=]\s*501\b|HTTP_501|['\"`]not implemented['\"`]", re.I)
NOT_IMPL_THROW_JS = re.compile(r"throw new Error\(\s*['\"`][^'\"`]*(not implemented|unimplemented|todo)", re.I)
NOT_IMPL_RAISE_PY = re.compile(r"raise\s+NotImplementedError")
ABSTRACT_PY = re.compile(r"@abstractmethod|\bProtocol\b|\bABC\b")
NOOP_HANDLER = re.compile(r"\bon[A-Z]\w*=\{\s*\(\s*\)\s*=>\s*(\{\s*\}|undefined|null)\s*\}")
COMING_SOON = re.compile(r"coming soon", re.I)
TODO = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
IMG_NO_ALT = re.compile(r"<(img|Image)\b(?![^>]*\balt=)[^>]*>", re.S)
ICON_BUTTON_NO_LABEL = re.compile(r"<(button|Button)\b(?![^>]*\baria-label)[^>]*>\s*<[A-Z]\w*Icon\b[^>]*/>\s*</\1>", re.S)


def scan(root: Path) -> dict:
    rel = lambda p: str(p.relative_to(root))
    out = {k: [] for k in ("not_implemented_routes", "not_implemented_errors", "noop_handlers", "coming_soon",
                           "images_without_alt", "icon_buttons_without_label")}
    todo_by_area: Counter = Counter()
    todo_files: Counter = Counter()
    files = list(walk(root, JS_CODE | PY_CODE | TEMPLATES))
    for p in files:
        t, r = read(p), rel(p)
        is_route = ("/api/" in "/" + r and p.name.split(".")[0] == "route") or "/pages/api/" in "/" + r \
            or (p.suffix == ".py" and re.search(r"@\s*\w+(?:\.\w+)*\.(get|post|put|patch|delete|route)\(", t))
        if is_route and NOT_IMPL_ROUTE.search(t):
            out["not_implemented_routes"].append(r)
        if p.suffix in JS_CODE and NOT_IMPL_THROW_JS.search(t):
            out["not_implemented_errors"].append(r)
        if p.suffix == ".py" and NOT_IMPL_RAISE_PY.search(t) and not ABSTRACT_PY.search(t):
            out["not_implemented_errors"].append(r)
        n = len(NOOP_HANDLER.findall(t))
        if n:
            out["noop_handlers"].append(f"{r} ({n})")
        if p.suffix in MARKUP:
            if COMING_SOON.search(t):
                out["coming_soon"].append(r)
            if IMG_NO_ALT.search(t):
                out["images_without_alt"].append(r)
            if ICON_BUTTON_NO_LABEL.search(t):
                out["icon_buttons_without_label"].append(r)
        k = len(TODO.findall(t))
        if k:
            todo_files[r] = k
            todo_by_area["/".join(r.split("/")[:3])] += k
    for key in list(out):
        out[key] = sorted(out[key])
    out["files_scanned"] = len(files)
    out["todo_total"] = sum(todo_files.values())
    out["todo_by_area_top"] = [{"area": a, "count": c} for a, c in todo_by_area.most_common(10)]
    out["todo_files_top"] = [{"file": f, "count": c} for f, c in todo_files.most_common(15)]
    stack = detect_stack(root)
    out["not_checked"] = []
    if not any(p.suffix in MARKUP for p in files):
        out["not_checked"].append("accessibility: no JSX/TSX or HTML templates found")
    if not (stack["node"] or stack["python"]):
        out["not_checked"].append("no supported stack detected: only TODO density and text checks ran")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Unfinished-feature and accessibility leads over a repository.")
    ap.add_argument("--path", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    root = Path(args.path)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    res = scan(root)
    print(json.dumps(res, indent=2) if args.json else "\n".join(
        f"{k}: {v if isinstance(v, int) else len(v)}" for k, v in res.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
