#!/usr/bin/env python3
"""Lint every SKILL.md shipped by an in-repo plugin.

These defects all fail SILENTLY -- the harness logs nothing useful, the skill simply
never triggers -- so they are gated here instead of being discovered in the wild:

  1. unquoted ": " in a frontmatter value
     YAML reads the colon-space as a nested mapping, the WHOLE frontmatter block
     fails to parse, and the skill loads with no name and no description. A
     model-invoked skill with no description can never fire. Bitten three times.
  2. lowercase skill.md
     Resolves on case-insensitive macOS, invisible on Linux and to any consumer
     that expects the documented filename.
  3. duplicate-download artifacts ("skill (1).md")
     A stale older copy sitting beside the current one.
  4. name/description missing, or name disagreeing with its directory.

Pure standard library so CI needs no install step.
"""
import os
import re
import sys

PLUGINS = "plugins"
errors = []
checked = 0


def frontmatter_problems(text):
    """Return a list of problems with the YAML frontmatter block."""
    if text.startswith("﻿"):
        return ["byte-order mark before the opening --- (frontmatter will not be recognized)"]
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return ["missing opening --- delimiter"]
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return ["frontmatter block is never closed by a --- line"]

    problems, keys = [], []
    for raw in m.group(1).split("\n"):
        line = raw.rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1] in (" ", "\t", "-"):      # continuation or list item
            continue
        km = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s+(.*))?$", line)
        if not km:
            problems.append(f"line is not a valid YAML key/value pair: {line[:70]!r}")
            continue
        key, val = km.group(1), (km.group(2) or "").strip()
        keys.append(key)
        if not val or val.startswith(('"', "'", "|", ">", "[", "{")):
            continue                          # quoted/blocked/collection values are safe
        if ": " in val or val.endswith(":"):
            problems.append(
                f'unquoted ": " inside `{key}` -- YAML reads it as a nested mapping and '
                f"drops the ENTIRE frontmatter block. Wrap the value in double quotes. "
                f"Offending value: {val[:70]!r}"
            )
    for required in ("name", "description"):
        if required not in keys:
            problems.append(f"missing required `{required}` field")
    return problems


if not os.path.isdir(PLUGINS):
    print(f"no {PLUGINS}/ directory -- nothing to lint")
    sys.exit(0)

for plugin in sorted(os.listdir(PLUGINS)):
    skills_dir = os.path.join(PLUGINS, plugin, "skills")
    if not os.path.isdir(skills_dir):
        continue
    for skill in sorted(os.listdir(skills_dir)):
        d = os.path.join(skills_dir, skill)
        if not os.path.isdir(d):
            continue
        where = f"{plugin}/{skill}"
        names = os.listdir(d)

        for n in names:
            if re.search(r"\(\d+\)", n):
                errors.append(f"{where}: stale duplicate file {n!r} -- delete it")

        if "SKILL.md" not in names:
            miscased = [n for n in names if n.lower() == "skill.md"]
            if miscased:
                errors.append(
                    f"{where}: file is named {miscased[0]!r}, not 'SKILL.md' -- "
                    f"undiscoverable on case-sensitive filesystems"
                )
            else:
                errors.append(f"{where}: no SKILL.md (found: {sorted(names)})")
            continue

        checked += 1
        with open(os.path.join(d, "SKILL.md"), encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for p in frontmatter_problems(text):
            errors.append(f"{where}: {p}")

        nm = re.search(r"^name:\s*\"?([A-Za-z0-9_-]+)", text, re.M)
        if nm and nm.group(1) != skill:
            errors.append(
                f"{where}: frontmatter name {nm.group(1)!r} does not match its "
                f"directory {skill!r} -- the directory name is what users invoke"
            )

if errors:
    print(f"{len(errors)} problem(s) found:\n", file=sys.stderr)
    for e in errors:
        print(f"  {e}", file=sys.stderr)
    sys.exit(1)

print(f"all {checked} SKILL.md file(s) valid (frontmatter parses, names match, no stale copies)")
