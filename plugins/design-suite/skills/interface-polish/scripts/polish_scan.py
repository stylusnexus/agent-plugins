#!/usr/bin/env python3
"""Static scan of CSS, HTML and JSX/TSX for the checkable rules in the interface-polish and
accessibility-review skills. It reads source only. A hit is a place to look, not a verdict, and a
clean scan proves nothing about the rendered page.

    polish_scan.py src/                  # report
    polish_scan.py src/ --json           # machine-readable
    polish_scan.py src/ --fail-on-hits   # exit 1 when anything is reported (for CI)

Silence a line with `polish-scan-ignore` in a comment on that line or the line above.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

EXTENSIONS = {".css", ".scss", ".html", ".htm", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".mdx"}
SKIP_DIRS = {"node_modules", ".next", "dist", "build", ".git", "coverage", ".turbo", "out", ".vercel"}

# Rules that can span lines, matched against the whole file: (id, pattern, message)
TEXT_RULES = [
    ("scroll-listener", r"addEventListener\(\s*['\"]scroll['\"]",
     "Prefer IntersectionObserver or CSS scroll-driven animation for reveals (motion.md)."),
    ("infinite-motion", r"animation[\w-]*\s*:[^;{}]*(?<![\w-])infinite(?![\w-])",
     "Looping motion that runs over 5 seconds needs a pause control (WCAG 2.2.2) and a reduced-motion rule."),
]

# (id, pattern, message) checked line by line
LINE_RULES = [
    ("transition-all", r"transition\s*:\s*all(?![\w-])|(?<![\w-])transition-all(?![\w-])",
     "Name the properties that change instead of `transition: all` (motion.md)."),
    ("viewport-height", r"(?<![\w-])100vh\b|(?<![\w-])h-screen\b|(?<![\w-])min-h-screen\b",
     "Full-height blocks jump under mobile browser bars; consider dvh or svh (layout-and-states.md)."),
    ("negative-tracking", r"letter-spacing\s*:\s*-|(?<![\w-])tracking-(?:tight|tighter)\b",
     "Negative tracking belongs at display sizes only; check this text is large (typography-and-colour.md)."),
    ("hover-only-reveal", r"group-hover:(?:block|flex|grid|visible|opacity-100)|:hover[^{]*\{[^}]*display\s*:\s*(?:block|flex|grid)",
     "Content shown only on hover has no touch or keyboard path; add focus and tap equivalents (accessibility-review)."),
    ("infinite-motion", r"(?<![\w-])animate-(?:spin|pulse|bounce|ping)(?![\w-])",
     "Looping motion that runs over 5 seconds needs a pause control (WCAG 2.2.2) and a reduced-motion rule."),
    ("custom-cursor", r"(?<![\w-])cursor\s*:\s*url\(",
     "Custom cursors can hide the pointer or lose contrast; confirm it is worth it."),
]

# Tight tracking is fine on display text: a heading, display, title or hero rule, or a 24px+ size.
DISPLAY_TEXT = re.compile(r"\b(?:h[1-3]|display|head(?:ing|line)?|title|hero|kpi)\b|font-size\s*:\s*(?:2[4-9]|[3-9]\d|\d{3,})px|text-(?:2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)\b")
OUTLINE_OFF = re.compile(r"outline\s*:\s*(?:none|0(?:px)?)(?![\w.-])|(?<![\w-])(?:focus:)?outline-(?:none|0)\b|(?<![\w-])focus:ring-0\b")
OUTLINE_REPLACEMENT = re.compile(r"focus-visible|focus:ring|ring-\d|focus:outline-\d|outline-\[|box-shadow|:focus\s*\{[^}]*outline\s*:\s*[^n0]")
SHADOW = re.compile(r"box-shadow\s*:[^;{}]*|shadow-\[[^\]]*\]")
BLACK_ALPHA = [
    re.compile(r"rgba?\(\s*0\s*[, ]\s*0\s*[, ]\s*0\s*[,/]\s*([\d.]+%?)\s*\)"),
    re.compile(r"hsla?\(\s*[\d.]+(?:deg)?\s*[, ]\s*[\d.]+%\s*[, ]\s*0%\s*[,/]\s*([\d.]+%?)\s*\)"),
]
BLACK_HEX = re.compile(r"#000000([0-9a-f]{2})(?![0-9a-f])|#000([0-9a-f])(?![0-9a-f])", re.I)


def black_alphas(shadow):
    """Alpha values (0-1) of every pure-black colour in a shadow declaration."""
    found = []
    for pattern in BLACK_ALPHA:
        for m in pattern.finditer(shadow):
            v = m.group(1)
            found.append(float(v[:-1]) / 100 if v.endswith("%") else float(v))
    for m in BLACK_HEX.finditer(shadow):
        digits = m.group(1) or m.group(2) * 2
        found.append(int(digits, 16) / 255)
    return found


SMALL_PX = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)px|text-\[(\d+(?:\.\d+)?)px\]")
RADIUS = re.compile(r"border-radius\s*:\s*([^;}\"'<]+)|(?<![\w-])rounded(?:-[a-z]+)?(?:-(?:none|sm|md|lg|xl|2xl|3xl|full|\[[^\]]+\]))?(?![\w-])")
ZINDEX = re.compile(r"z-index\s*:\s*(-?\d+)|(?<![\w-])z-(?:\[(-?\d+)\]|(\d+))(?![\w-])")
REDUCED_MOTION = re.compile(r"prefers-reduced-motion|motion-reduce:|motion-safe:")
MOTION = re.compile(r"(?<![\w-])transition\s*:|(?<![\w-])animation[\w-]*\s*:|@keyframes|(?<![\w-])animate-|(?<![\w-])transition-(?:all|colors|opacity|transform|shadow)\b")


def files_under(paths):
    for p in paths:
        p = Path(p)
        if p.is_file():
            yield p
            continue
        for f in sorted(p.rglob("*")):
            if f.suffix in EXTENSIONS and f.is_file() and not (SKIP_DIRS & set(f.relative_to(p).parts)):
                yield f


def scan_file(path):
    hits, radii, zindexes = [], defaultdict(list), defaultdict(list)
    uses_motion = has_reduced = False
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return hits, radii, zindexes, uses_motion, has_reduced

    def report(n, rule, message):
        above = lines[n - 2].strip() if n > 1 else ""
        comment_only = above.startswith(("/*", "//", "<!--", "{/*", "#", "*")) and "polish-scan-ignore" in above
        ignored = "polish-scan-ignore" in lines[n - 1] or comment_only
        if not ignored:
            hits.append({"file": str(path), "line": n, "rule": rule, "message": message, "text": lines[n - 1].strip()[:160]})

    for n, line in enumerate(lines, 1):
        for rule, pattern, message in LINE_RULES:
            if re.search(pattern, line):
                if rule == "negative-tracking" and DISPLAY_TEXT.search(line):
                    continue
                report(n, rule, message)
        if OUTLINE_OFF.search(line):
            window = "\n".join(lines[n - 1:n + 2])
            if not OUTLINE_REPLACEMENT.search(window):
                report(n, "outline-removed", "Focus outline removed with no visible replacement nearby (keyboard-and-focus.md).")
        for m in SMALL_PX.finditer(line):
            size = float(m.group(1) or m.group(2))
            if size < 12:
                report(n, "small-text", f"Text at {size:g}px; labels should stay at 12px or larger (typography-and-colour.md).")
        for m in RADIUS.finditer(line):
            radii[(m.group(1) or m.group(0)).strip()].append(n)
        for m in ZINDEX.finditer(line):
            zindexes[m.group(1) or m.group(2) or m.group(3)].append(n)
        uses_motion = uses_motion or bool(MOTION.search(line))
        has_reduced = has_reduced or bool(REDUCED_MOTION.search(line))
    text = "\n".join(lines)
    starts = [m.start() for m in re.finditer(r"^", text, re.M)]

    def line_of(offset):
        return sum(1 for st in starts if st <= offset)

    for rule, pattern, message in TEXT_RULES:
        for m in re.finditer(pattern, text):
            report(line_of(m.start()), rule, message)
    for m in SHADOW.finditer(text):
        for alpha in black_alphas(m.group(0)):
            if alpha > 0.08:
                report(line_of(m.start()), "heavy-black-shadow", f"Black shadow at alpha {alpha:.2g}; recommended at or below about 0.08, tinted to the surface (surfaces-and-spacing.md).")
    hits.sort(key=lambda h: h["line"])
    return hits, radii, zindexes, uses_motion, has_reduced


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on-hits", action="store_true", help="exit 1 if anything is reported")
    parser.add_argument("--max-radii", type=int, default=4, help="report when more distinct radius values than this (default 4)")
    parser.add_argument("--max-zindex", type=int, default=6, help="report when more distinct z-index values than this (default 6)")
    args = parser.parse_args()

    for p in args.paths:
        if not p.exists():
            parser.error(f"no such path: {p}")
    hits, radii, zindexes = [], defaultdict(list), defaultdict(list)
    scanned = 0
    motion_files, reduced_files = [], []
    for f in files_under(args.paths):
        scanned += 1
        h, r, z, motion, reduced = scan_file(f)
        hits += h
        for k, v in r.items():
            radii[k] += [(str(f), n) for n in v]
        for k, v in z.items():
            zindexes[k] += [(str(f), n) for n in v]
        if motion:
            motion_files.append(str(f))
        if reduced:
            reduced_files.append(str(f))

    summary = []
    if len(radii) > args.max_radii:
        summary.append({"rule": "radius-scale", "message": f"{len(radii)} distinct radius values: {', '.join(sorted(radii))}. Each should map to a named role (surfaces-and-spacing.md)."})
    if len(zindexes) > args.max_zindex:
        summary.append({"rule": "z-index-scale", "message": f"{len(zindexes)} distinct z-index values: {', '.join(sorted(zindexes, key=int))}. Keep layers in one documented scale."})
    if motion_files and not reduced_files:
        summary.append({"rule": "no-reduced-motion", "message": f"Motion is used in {len(motion_files)} file(s) and no prefers-reduced-motion or motion-reduce rule was found in the scanned set."})

    if args.json:
        print(json.dumps({"scanned": scanned, "hits": hits, "summary": summary}, indent=2))
    else:
        by_file = defaultdict(list)
        for h in hits:
            by_file[h["file"]].append(h)
        for file, items in by_file.items():
            print(file)
            for h in items:
                print(f"  {h['line']:>4}  {h['rule']:<20} {h['message']}\n        {h['text']}")
        for s in summary:
            print(f"\n[{s['rule']}] {s['message']}")
        print(f"\n{scanned} file(s) scanned, {len(hits)} line hit(s), {len(summary)} set-wide note(s).")
        print("Static text match only. It cannot see computed styles, design tokens or the rendered page.")
    if not scanned:
        print("Nothing was scanned: no matching files under the given paths.", file=sys.stderr)
        return 2
    return 1 if args.fail_on_hits and (hits or summary) else 0


if __name__ == "__main__":
    sys.exit(main())
