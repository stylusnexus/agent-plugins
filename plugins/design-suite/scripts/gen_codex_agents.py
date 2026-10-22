#!/usr/bin/env python3
"""Generate the Codex agents (codex-agents/*.toml) from the Claude agents (agents/*.md).

    gen_codex_agents.py            # write codex-agents/*.toml
    gen_codex_agents.py --check    # exit 1 if any file is missing, stale or has no Claude twin

A Codex agent is three keys: name, description, developer_instructions. They are taken from the
Claude agent's frontmatter and body, so the two sets cannot drift apart.
"""
import argparse
import json
import re
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]


def parse(md):
    """Return (name, description, body) from a Claude agent file."""
    m = re.match(r"---\n(.*?)\n---\n(.*)", md, re.S)
    if not m:
        raise ValueError("no frontmatter")
    fields = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip('"')
    return fields["name"], fields["description"], m.group(2).strip()


def toml_string(text):
    return json.dumps(text, ensure_ascii=False)  # a JSON string is a valid TOML basic string


def render(md):
    name, description, body = parse(md)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    instructions = "\n\n".join(paragraphs)
    return (f"name = {toml_string(name)}\n"
            f"description = {toml_string(description)}\n"
            f"developer_instructions = {toml_string(instructions)}\n")


def expected(pack=PACK):
    return {p.stem: render(p.read_text()) for p in sorted((pack / "agents").glob("*.md"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    out = PACK / "codex-agents"
    want = expected()
    problems = []
    for stem, text in want.items():
        target = out / f"{stem}.toml"
        if args.check:
            if not target.is_file():
                problems.append(f"missing {target.name}")
            elif target.read_text() != text:
                problems.append(f"stale {target.name}")
        else:
            out.mkdir(exist_ok=True)
            target.write_text(text)
    for extra in sorted(out.glob("*.toml")) if out.is_dir() else []:
        if extra.stem not in want:
            problems.append(f"{extra.name} has no Claude agent")
    for p in problems:
        print(p)
    if args.check and problems:
        return 1
    print(f"{len(want)} agent(s) {'checked' if args.check else 'written'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
