#!/usr/bin/env python3
"""redaction.py -- scrub known secret shapes from text before it is written anywhere.

A pragmatic pattern list, not data-loss prevention: it fails OPEN (a secret
with an unrecognized shape passes through), so it is a backstop behind
"never gather secrets in the first place", never the only control.

As a module: redact(text) -> (redacted_text, sorted_classes_found).
As a script: reads stdin, writes the redacted text to stdout, and prints the
classes it found to stderr.
"""
from __future__ import annotations

import re
import sys

_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)),
    ("anthropic_key", re.compile(r"sk-ant-[A-Za-z0-9_-]{12,}")),
    ("openai_key", re.compile(r"sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("slack_app_token", re.compile(r"xapp-[0-9]-[A-Za-z0-9-]{10,}")),
    ("github_token", re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("stripe_key", re.compile(r"(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}")),
    ("stripe_webhook_secret", re.compile(r"whsec_[A-Za-z0-9]{16,}")),
    ("supabase_secret_key", re.compile(r"sb_secret_[A-Za-z0-9_-]{16,}")),
    ("aws_access_key", re.compile(r"(?:AKIA|ASIA)[0-9A-Z]{16}")),
    ("google_api_key", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    ("bearer_token", re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{16,}")),
    # scheme://user:PASSWORD@host -- keep the scheme and host so the finding still reads
    ("url_password", re.compile(r"(?<=://)(?!\[REDACTED:)[^\s:/@]+:[^\s@/]+(?=@)")),
]


def redact(text: str) -> tuple[str, list[str]]:
    """Return (redacted_text, sorted_classes_found)."""
    found: set[str] = set()
    out = text
    for name, pat in _PATTERNS:

        def _repl(_m, _name=name):
            found.add(_name)
            return f"[REDACTED:{_name}]"

        out = pat.sub(_repl, out)
    return out, sorted(found)


if __name__ == "__main__":
    text, classes = redact(sys.stdin.read())
    sys.stdout.write(text)
    if classes:
        print(f"redacted: {', '.join(classes)}", file=sys.stderr)
