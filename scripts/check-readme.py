#!/usr/bin/env python3
"""Verify the README tables and headline counts match what's actually on disk.

Three things drift silently when a skill is added/removed/renamed and the
docs aren't updated to match:

  1. The root README's "Skill packs" table (Pack / # / What it's for / Skills)
     must list exactly the skills that exist under plugins/<pack>/skills/ --
     no missing, no extra -- and its "#" column must match that count.
  2. The root README's headline ("**N plugins, M skills**") must match the
     real totals: N = in-repo packs + rows in the "Tool plugins" table,
     M = sum of the "#" column above.
  3. Each plugins/<pack>/README.md must mention every skill under that pack's
     skills/ directory (found as a table cell that is exactly one backticked
     name), and mention no skill that doesn't exist.

The table format is read from the README rather than hardcoded (look for the
header row whose first cell is "Pack" / "Plugin"), so formatting can move
around -- but the skill SET comparison is strict.

Pure standard library so CI needs no install step.
"""
import json
import os
import re
import sys

PLUGINS_DIR = "plugins"
ROOT_README = "README.md"

errors = []


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_separator(line):
    return bool(re.match(r'^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$', line.strip()))


def find_table(lines, header_first_cell):
    """Return (rows, header_line_index) for the first table whose header's first
    cell matches header_first_cell (case-insensitive), or (None, None)."""
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        cells = split_row(line)
        if not cells or cells[0].lower() != header_first_cell.lower():
            continue
        if i + 1 >= len(lines) or not is_separator(lines[i + 1]):
            continue
        rows = []
        j = i + 2
        while j < len(lines) and lines[j].strip().startswith("|"):
            rows.append(split_row(lines[j]))
            j += 1
        return rows, i
    return None, None


def actual_skills(pack_dir):
    """Skill directory names under plugins/<pack_dir>/skills/ that contain a SKILL.md."""
    skills_dir = os.path.join(PLUGINS_DIR, pack_dir, "skills")
    if not os.path.isdir(skills_dir):
        return []
    return sorted(
        d for d in os.listdir(skills_dir)
        if os.path.isfile(os.path.join(skills_dir, d, "SKILL.md"))
    )


def check_root_readme():
    if not os.path.isfile(ROOT_README):
        errors.append(f"{ROOT_README}: file not found")
        return

    with open(ROOT_README, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()

    pack_rows, _ = find_table(lines, "Pack")
    if pack_rows is None:
        errors.append(f"{ROOT_README}: could not find the skill-pack table (header cell 'Pack')")
        pack_rows = []

    tool_rows, _ = find_table(lines, "Plugin")
    if tool_rows is None:
        errors.append(f"{ROOT_README}: could not find the tool-plugins table (header cell 'Plugin')")
        tool_rows = []

    on_disk_packs = sorted(
        d for d in os.listdir(PLUGINS_DIR)
        if os.path.isdir(os.path.join(PLUGINS_DIR, d, "skills"))
    ) if os.path.isdir(PLUGINS_DIR) else []

    declared_packs = {}  # pack name -> (declared count, set of declared skill names, row)
    for row in pack_rows:
        if not row:
            continue
        m = re.search(r'\[\*\*([A-Za-z0-9_-]+)\*\*\]\(\./plugins/([A-Za-z0-9_-]+)\)', row[0])
        if not m:
            errors.append(f"{ROOT_README}: pack table row does not link a ./plugins/<name>: {row[0]!r}")
            continue
        name = m.group(2)
        count = None
        if len(row) > 1 and row[1].strip().isdigit():
            count = int(row[1].strip())
        else:
            errors.append(f"{ROOT_README}: pack '{name}' row has no numeric '#' cell")
        skills_cell = row[-1] if row else ""
        declared_skills = set(re.findall(r'`([A-Za-z0-9_-]+)`', skills_cell))
        declared_packs[name] = (count, declared_skills)

    for pack in on_disk_packs:
        real = set(actual_skills(pack))
        if pack not in declared_packs:
            errors.append(f"{ROOT_README}: pack '{pack}' exists under plugins/ but has no row in the pack table")
            continue
        count, declared_skills = declared_packs[pack]
        missing = real - declared_skills
        extra = declared_skills - real
        if missing:
            errors.append(f"{ROOT_README}: pack '{pack}' table is missing skill(s): {sorted(missing)}")
        if extra:
            errors.append(f"{ROOT_README}: pack '{pack}' table lists skill(s) that don't exist: {sorted(extra)}")
        if count is not None and count != len(real):
            errors.append(
                f"{ROOT_README}: pack '{pack}' declares '# {count}' but plugins/{pack}/skills/ has {len(real)}"
            )
        if count is not None and count != len(declared_skills):
            errors.append(
                f"{ROOT_README}: pack '{pack}' declares '# {count}' but its Skills cell lists {len(declared_skills)}"
            )

    for name in declared_packs:
        if name not in on_disk_packs:
            errors.append(f"{ROOT_README}: pack table lists '{name}' but plugins/{name}/skills/ does not exist")

    tool_names = []
    for row in tool_rows:
        if not row:
            continue
        m = re.search(r'\[\*\*([A-Za-z0-9_-]+)\*\*\]\(https?://[^)]+\)', row[0])
        if m:
            tool_names.append(m.group(1))
    if not tool_names:
        errors.append(f"{ROOT_README}: tool-plugins table has no recognizable '[**name**](https://...)' rows")

    total_skills_declared = sum(c for c, _ in declared_packs.values() if c is not None)
    total_plugins_declared = len(declared_packs) + len(tool_names)

    headline = re.search(r'\*\*(\d+)\s+plugins?,\s*(\d+)\s+skills?\*\*', text)
    if not headline:
        errors.append(f"{ROOT_README}: no headline of the form '**N plugins, M skills**' found")
    else:
        hp, hs = int(headline.group(1)), int(headline.group(2))
        if hp != total_plugins_declared:
            errors.append(
                f"{ROOT_README}: headline says {hp} plugins, but the pack table ({len(declared_packs)}) "
                f"+ tool table ({len(tool_names)}) = {total_plugins_declared}"
            )
        if hs != total_skills_declared:
            errors.append(
                f"{ROOT_README}: headline says {hs} skills, but the pack table '#' column sums to {total_skills_declared}"
            )

    marketplace_path = os.path.join(".claude-plugin", "marketplace.json")
    if os.path.isfile(marketplace_path):
        try:
            with open(marketplace_path, encoding="utf-8") as fh:
                mp = json.load(fh)
            mp_count = len(mp.get("plugins", []))
            if headline and mp_count != int(headline.group(1)):
                errors.append(
                    f"{ROOT_README}: headline says {headline.group(1)} plugins, but "
                    f"{marketplace_path} lists {mp_count}"
                )
        except (OSError, json.JSONDecodeError) as e:
            errors.append(f"{marketplace_path}: could not read/parse ({e})")


def check_plugin_readmes():
    if not os.path.isdir(PLUGINS_DIR):
        return
    for pack in sorted(os.listdir(PLUGINS_DIR)):
        pack_path = os.path.join(PLUGINS_DIR, pack)
        skills_dir = os.path.join(pack_path, "skills")
        if not os.path.isdir(skills_dir):
            continue
        readme = os.path.join(pack_path, "README.md")
        real = set(actual_skills(pack))
        if not os.path.isfile(readme):
            errors.append(f"{readme}: file not found (pack has {len(real)} skill(s))")
            continue
        with open(readme, encoding="utf-8") as fh:
            lines = fh.readlines()
        mentioned = set()
        for line in lines:
            if not line.strip().startswith("|") or is_separator(line):
                continue
            for cell in split_row(line):
                m = re.match(r'^`([A-Za-z0-9][A-Za-z0-9_-]*)`$', cell.strip())
                if m:
                    mentioned.add(m.group(1))
        missing = real - mentioned
        # 'extra' is only meaningful for tokens that look like OTHER skill names
        # (avoid flagging incidental single-backtick cells like flags or commands
        # that happen not to be a skill in this pack).
        extra = (mentioned - real) & set().union(*(actual_skills(p) for p in os.listdir(PLUGINS_DIR)))
        if missing:
            errors.append(f"{readme}: missing skill(s) from its own table(s): {sorted(missing)}")
        if extra:
            errors.append(f"{readme}: table(s) mention skill(s) not in this pack: {sorted(extra)}")


def main():
    check_root_readme()
    check_plugin_readmes()
    if errors:
        print(f"{len(errors)} README/skill-set mismatch(es) found:\n", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print("README pack tables, plugin READMEs, and headline counts all match plugins/ on disk")
    return 0


if __name__ == "__main__":
    sys.exit(main())
