#!/usr/bin/env python3
"""Generate the README skill catalogue and skills.sh.json from what's on disk.

Writes two things:

  1. The block between <!-- catalog:start --> and <!-- catalog:end --> in the
     root README: every pack's skills and agents, then an A-Z index.
  2. skills.sh.json: one skills.sh grouping per pack, in pack-table order.

Each skill's summary is its row in the pack's own README table, so the pack
README stays the single place it's written.
Pack order and pack descriptions come from the root README's pack table.

  python3 scripts/gen-catalog.py          # rewrite both files
  python3 scripts/gen-catalog.py --check  # exit 1 if either is stale (CI)

Pure standard library so CI needs no install step.
"""
import json
import os
import re
import sys

PLUGINS_DIR = "plugins"
ROOT_README = "README.md"
SKILLS_SH = "skills.sh.json"
START, END = "<!-- catalog:start -->", "<!-- catalog:end -->"


def pack_table(readme_text):
    """(pack, description) pairs from the root README's 'Pack' table, in order."""
    packs, in_table = [], False
    for line in readme_text.splitlines():
        if line.startswith("| Pack |"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            m = re.match(r"\| \[\*\*([a-z0-9-]+)\*\*\]\(\./plugins/[a-z0-9-]+\) \| \d+ \| (.+?) \|", line)
            if m:
                packs.append((m.group(1), m.group(2)))
    return packs


def clean(text):
    return text.replace("**", "").strip().rstrip("|").strip()


def skill_rows(pack):
    """skill -> summary, from the first table row naming it in the pack README."""
    with open(os.path.join(PLUGINS_DIR, pack, "README.md"), encoding="utf-8") as fh:
        text = fh.read()
    rows = {}
    for m in re.finditer(r"^\| `([a-z0-9-]+)` \| (.+)$", text, re.M):
        rows.setdefault(m.group(1), clean(m.group(2)))
    return rows


def skills_of(pack):
    d = os.path.join(PLUGINS_DIR, pack, "skills")
    return sorted(s for s in os.listdir(d) if os.path.isfile(os.path.join(d, s, "SKILL.md")))


def agents_of(pack):
    d = os.path.join(PLUGINS_DIR, pack, "agents")
    return sorted(f[:-3] for f in os.listdir(d) if f.endswith(".md")) if os.path.isdir(d) else []


def build(readme_text):
    packs = pack_table(readme_text)
    out, index, groupings = [], [], []
    for pack, desc in packs:
        rows = skill_rows(pack)
        skills = skills_of(pack)
        missing = [s for s in skills if s not in rows]
        if missing:
            sys.exit(f"plugins/{pack}/README.md: no table row for {missing}")
        agents = agents_of(pack)
        out.append(f"<details>\n<summary><b>{pack}</b> · {len(skills)} skills"
                   f"{f' · {len(agents)} agents' if agents else ''}</summary>\n")
        out.append("| Skill | What it covers |\n|---|---|")
        out.extend(f"| `{s}` | {rows[s]} |" for s in skills)
        if agents:
            out.append(f"\nAgents (Claude Code): {' '.join(f'`{a}`' for a in agents)}")
        out.append(f"\n[Pack README →](./plugins/{pack})\n\n</details>\n")
        index.extend((s, pack) for s in skills)
        groupings.append({"title": pack, "description": desc, "skills": skills})
    index.sort()
    out.append("<details>\n<summary><b>A–Z index</b> · every skill and its pack</summary>\n")
    out.append("| Skill | Pack |\n|---|---|")
    out.extend(f"| `{s}` | [{p}](./plugins/{p}) |" for s, p in index)
    out.append("\n</details>")
    catalog = "\n".join(out)
    sh = {"$schema": "https://skills.sh/schemas/skills.sh.schema.json",
          "notGrouped": "bottom", "groupings": groupings}
    return catalog, json.dumps(sh, indent=2, ensure_ascii=False) + "\n"


def main():
    with open(ROOT_README, encoding="utf-8") as fh:
        readme = fh.read()
    if START not in readme or END not in readme:
        sys.exit(f"{ROOT_README}: missing {START} / {END} markers")
    catalog, sh = build(readme)
    head, rest = readme.split(START, 1)
    tail = rest.split(END, 1)[1]
    new_readme = f"{head}{START}\n{catalog}\n{END}{tail}"
    old_sh = open(SKILLS_SH, encoding="utf-8").read() if os.path.isfile(SKILLS_SH) else ""

    if "--check" in sys.argv:
        stale = [f for f, old, new in ((ROOT_README, readme, new_readme), (SKILLS_SH, old_sh, sh)) if old != new]
        if stale:
            print(f"stale: {', '.join(stale)} -- run python3 scripts/gen-catalog.py", file=sys.stderr)
            return 1
        print("README catalogue and skills.sh.json match plugins/ on disk")
        return 0

    with open(ROOT_README, "w", encoding="utf-8") as fh:
        fh.write(new_readme)
    with open(SKILLS_SH, "w", encoding="utf-8") as fh:
        fh.write(sh)
    print(f"wrote {ROOT_README} catalogue and {SKILLS_SH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
