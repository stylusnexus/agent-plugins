#!/usr/bin/env python3
"""Report what a crawler that does not run JavaScript sees on one page.

Usage:
    python3 static_signals.py https://example.com/
    python3 static_signals.py --file saved-page.html

Fetches the raw HTML (or reads a saved copy) and prints one JSON object with the
signals a cold-visit audit needs: title, meta description, Open Graph and Twitter
tags, canonical link, JSON-LD blocks, headline text, noscript fallback, video
and caption-track counts, how much visible text the raw HTML holds, and a
`js_shell` verdict when it holds almost none. It only reads: one GET request,
no cookies, no forms, no clicks, no sign-in.

Pure standard library.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

MAX_BYTES = 2_000_000
TIMEOUT_SECONDS = 20
USER_AGENT = "first-contact-audit/1.0 (read-only; one GET request)"
SKIP_TEXT = {"script", "style", "noscript", "template", "head", "title"}
# Below this many visible characters a page with scripts is treated as a shell.
SHELL_TEXT_LIMIT = 200


class Signals(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta = {}
        self.open_graph = {}
        self.twitter = {}
        self.canonical = None
        self.lang = None
        self.json_ld = 0
        self.h1 = []
        self.noscript_chars = 0
        self.videos = []
        self.tracks = 0
        self.iframes = 0
        self.scripts = 0
        self.visible_chars = 0
        self._skip = []
        self._in_title = False
        self._in_h1 = 0
        self._h1_parts = []
        self._ld_open = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang") or None
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = a.get("name", "").lower()
            prop = a.get("property", "").lower()
            content = a.get("content", "").strip()
            if name == "description":
                self.meta["description"] = content
            elif name == "viewport":
                self.meta["viewport"] = content
            elif prop.startswith("og:"):
                self.open_graph[prop[3:]] = content
            elif name.startswith("twitter:"):
                self.twitter[name[8:]] = content
        elif tag == "link":
            rel = a.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonical = a.get("href") or None
        elif tag == "script":
            self.scripts += 1
            if a.get("type", "").lower() == "application/ld+json":
                self.json_ld += 1
        elif tag == "video":
            self.videos.append({"src": a.get("src", ""), "muted": "muted" in a,
                                "controls": "controls" in a, "autoplay": "autoplay" in a})
        elif tag == "track":
            self.tracks += 1
        elif tag == "iframe":
            self.iframes += 1
        elif tag == "h1":
            self._in_h1 += 1
            self._h1_parts = [] if self._in_h1 == 1 else self._h1_parts
        elif tag == "body":
            # A head left unclosed must not hide the whole body.
            self._skip = [t for t in self._skip if t not in ("head", "title")]
            self._in_title = False
        if tag in SKIP_TEXT:
            self._skip.append(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1" and self._in_h1:
            self._in_h1 -= 1
            if self._in_h1 == 0:
                text = re.sub(r"\s+", " ", " ".join(self._h1_parts)).strip()
                if text:
                    self.h1.append(text)
        if tag in SKIP_TEXT and tag in self._skip:
            # Pop back to the matching open tag so a stray end tag cannot unbalance the stack.
            while self._skip and self._skip.pop() != tag:
                pass

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if "noscript" in self._skip:
            self.noscript_chars += len(data.strip())
        if self._in_h1:
            self._h1_parts.append(data)
        if not self._skip:
            self.visible_chars += len(re.sub(r"\s+", "", data))


def analyse(html, url=None, status=None):
    parser = Signals()
    parser.feed(html)
    parser.close()
    host = urllib.parse.urlsplit(url).hostname if url else None
    label = host.split(".")[-2] if host and host.count(".") >= 1 else host
    js_shell = parser.visible_chars < SHELL_TEXT_LIMIT and parser.scripts > 0
    return {
        "url": url,
        "http_status": status,
        "domain": {
            "host": host,
            "name_label": label,
            "name_length": len(label) if label else None,
            "has_digits_or_hyphens": bool(label and re.search(r"[\d-]", label)),
        },
        "lang": parser.lang,
        "title": re.sub(r"\s+", " ", parser.title).strip(),
        "meta_description": parser.meta.get("description"),
        "has_viewport": "viewport" in parser.meta,
        "open_graph": parser.open_graph,
        "twitter_card": parser.twitter,
        "canonical": parser.canonical,
        "json_ld_blocks": parser.json_ld,
        "h1": parser.h1,
        "noscript_text_chars": parser.noscript_chars,
        "videos": parser.videos,
        "caption_tracks": parser.tracks,
        "iframes": parser.iframes,
        "script_tags": parser.scripts,
        "visible_text_chars": parser.visible_chars,
        "js_shell": js_shell,
        "js_shell_note": (
            "The raw HTML holds almost no visible text. A crawler or reader that does not run "
            "JavaScript sees only the title and meta description. Compare with the rendered page."
            if js_shell else None
        ),
    }


def fetch(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise ValueError("only http and https URLs are fetched")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        raw = response.read(MAX_BYTES + 1)
        charset = response.headers.get_content_charset() or "utf-8"
        return raw[:MAX_BYTES].decode(charset, errors="replace"), response.geturl(), response.status


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("url", nargs="?", help="http(s) URL to fetch with one GET request")
    ap.add_argument("--file", help="read a saved HTML file instead of fetching")
    args = ap.parse_args(argv)
    if bool(args.url) == bool(args.file):
        ap.error("give either a URL or --file, not both")
    try:
        if args.file:
            with open(args.file, encoding="utf-8", errors="replace") as handle:
                html, url, status = handle.read(), None, None
        else:
            html, url, status = fetch(args.url)
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1
    print(json.dumps(analyse(html, url, status), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
