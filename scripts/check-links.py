#!/usr/bin/env python3
"""Verify every relative link in the documentation actually resolves.

Scans plugins/**, README.md, and docs/** for:
  - Markdown links / images: [text](target) and ![alt](target)
  - HTML href="..." / src="..." attributes

For each RELATIVE target (absolute URLs like https://, mailto:, tel:, and
protocol-relative //host links are skipped -- those are out of this repo's
control):
  - the target path must exist on disk, resolved relative to the file that
    references it
  - a #fragment on a target must resolve to a real heading anchor in that
    markdown file, using GitHub's heading-slug rules (lowercase, strip
    punctuation, spaces -> hyphens, de-duplicated with -1/-2/... suffixes)

A dead relative link is invisible until someone actually clicks it -- this
walks the filesystem instead of waiting for that. Pure standard library so
CI needs no install step.
"""
import os
import re
import sys
import urllib.parse

ROOTS = ["plugins", "README.md", "docs"]

MD_LINK_RE = re.compile(r'!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)')
HTML_ATTR_RE = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)
HTML_TAG_RE = re.compile(r'<[a-zA-Z!][^<>]*>')
INLINE_CODE_RE = re.compile(r'`[^`]*`')
FENCE_RE = re.compile(r'^\s*(```|~~~)')
ATX_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')

errors = []
_slug_cache = {}


def github_slug(text):
    """Approximate GitHub's heading -> #anchor slug algorithm."""
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[*_~]', '', text)
    text = text.strip().lower()
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE)
    text = re.sub(r'\s+', '-', text)
    return text


def heading_slugs(path):
    """Return the set of valid #anchor slugs for a markdown file (dedup rules applied)."""
    if path in _slug_cache:
        return _slug_cache[path]
    slugs = set()
    seen = {}
    in_fence = False
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError:
        _slug_cache[path] = slugs
        return slugs
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = ATX_HEADING_RE.match(line)
        if not m:
            continue
        base = github_slug(m.group(2))
        if not base:
            continue
        n = seen.get(base, 0)
        seen[base] = n + 1
        slugs.add(base if n == 0 else f"{base}-{n}")
    _slug_cache[path] = slugs
    return slugs


def iter_scanned_files():
    for root in ROOTS:
        if os.path.isfile(root):
            if root.endswith((".md", ".html")):
                yield root
        elif os.path.isdir(root):
            for dirpath, dirnames, filenames in sorted(os.walk(root)):
                dirnames[:] = sorted(d for d in dirnames if d != ".git")
                for fn in sorted(filenames):
                    if fn.endswith((".md", ".html")):
                        yield os.path.join(dirpath, fn)


def is_external(target):
    return bool(SCHEME_RE.match(target)) or target.startswith("//")


def check_file(path):
    in_fence = False
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, start=1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            scan_line = line
            if path.endswith(".md"):
                # Inline code spans (`like this`) are illustrative text, not live
                # markup or links -- e.g. a checklist showing `<img src="http...">`
                # as an example of what NOT to ship. Drop them before matching.
                scan_line = INLINE_CODE_RE.sub("", scan_line)
            md_targets = MD_LINK_RE.findall(scan_line)
            # Only treat href/src as a real HTML attribute inside an actual tag
            # (<a href="...">), not e.g. a JS variable assignment like
            # `var SRC = "...";` that happens to match the same regex shape.
            html_targets = []
            for tag in HTML_TAG_RE.findall(scan_line):
                html_targets.extend(HTML_ATTR_RE.findall(tag))
            targets = md_targets + html_targets
            for raw in targets:
                raw = raw.strip()
                if not raw or is_external(raw):
                    continue
                filepart, _, fragment = raw.partition("#")
                filepart = urllib.parse.unquote(filepart)
                if filepart == "":
                    target_path = path
                else:
                    target_path = os.path.normpath(os.path.join(os.path.dirname(path), filepart))
                    if not os.path.exists(target_path):
                        errors.append(
                            f"{path}:{lineno}: broken link {raw!r} -> {target_path} does not exist"
                        )
                        continue
                if fragment and os.path.isfile(target_path) and target_path.endswith(".md"):
                    slugs = heading_slugs(target_path)
                    frag = urllib.parse.unquote(fragment).lower()
                    if frag not in slugs:
                        shown = ", ".join(sorted(slugs)[:10]) + (" ..." if len(slugs) > 10 else "")
                        errors.append(
                            f"{path}:{lineno}: anchor #{fragment} not found in {target_path} "
                            f"(known anchors: {shown})"
                        )


def main():
    files = list(iter_scanned_files())
    if not files:
        print(f"no .md/.html files found under {', '.join(ROOTS)} -- nothing to check")
        return 0
    for f in files:
        check_file(f)
    if errors:
        print(f"{len(errors)} broken link(s)/anchor(s) found:\n", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"all relative links and anchors resolved across {len(files)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
