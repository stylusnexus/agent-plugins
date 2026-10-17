#!/usr/bin/env python3
"""Verify compatibility.json against the skills on disk and the pack READMEs.

compatibility.json records, for every skill, how well it works on five hosts:
Claude Code, the Claude app, Codex, ChatGPT and other agents installed through
the Skills CLI. This check fails when:

  1. a skill folder under plugins/*/skills has no entry, or an entry has no
     skill folder, or an entry names the wrong pack;
  2. a level is not one of full / partial / no, or a partial / no level has
     no note;
  3. a pack README's badge line, limits line or "Compatibility at a glance"
     table row no longer matches the JSON (or a skill is missing from them);
  4. a skill folder has no README.md, or its README's badge line or limits
     line no longer matches the JSON (scripts/gen-skill-readme.py writes them).

The badges and table rows are rendered here from the JSON and compared as
exact text, so editing the JSON means updating the README lines to match.

Pure standard library so CI needs no install step.
"""
import json
import os
import re
import sys
import urllib.parse

PLUGINS_DIR = "plugins"
COMPAT = "compatibility.json"
LEVELS = ("full", "partial", "no")
HOSTS = ("claude_code", "claude_app", "codex", "chatgpt", "other")
SYMBOL = {"full": "✔", "partial": "◐", "no": "✖"}
COLOR = {"full": "brightgreen", "partial": "yellow", "no": "lightgrey"}
ROOT_LINK = "../../README.md#compatibility"
SKILL_ROOT_LINK = "../../../../README.md#compatibility"  # from plugins/<pack>/skills/<skill>/
SECTION = "## What it looks like"
GLANCE_HEADER = "| Skill | Claude Code | Claude app | Codex | ChatGPT | Other agents |"

errors = []


def sub_levels(entry):
    """The five (label, {level, note}) pairs of one skill entry, in display order."""
    return [
        ("Claude Code", entry["claude"]["code"]),
        ("Claude app", entry["claude"]["app"]),
        ("Codex", entry["codex_chatgpt"]["codex"]),
        ("ChatGPT", entry["codex_chatgpt"]["chatgpt"]),
        ("Other agents", entry["other"]),
    ]


def _part(text):
    return urllib.parse.quote(text.replace("-", "--").replace("_", "__"), safe="")


def badge(label, message, local_level, alt, link=ROOT_LINK):
    url = f"https://img.shields.io/badge/{_part(label)}-{_part(message)}-{COLOR[local_level]}"
    return f"[![{alt}]({url})]({link})"


def badge_line(entry, link=ROOT_LINK):
    c, a = entry["claude"]["code"]["level"], entry["claude"]["app"]["level"]
    x, g = entry["codex_chatgpt"]["codex"]["level"], entry["codex_chatgpt"]["chatgpt"]["level"]
    o = entry["other"]["level"]
    return " ".join([
        badge("Claude", f"Code {SYMBOL[c]} · app {SYMBOL[a]}", c, f"Claude: Code {c}, app {a}", link),
        badge("Codex / ChatGPT", f"Codex {SYMBOL[x]} · ChatGPT {SYMBOL[g]}", x,
              f"Codex / ChatGPT: Codex {x}, ChatGPT {g}", link),
        badge("Other agents", SYMBOL[o], o, f"Other agents: {o}", link),
    ])


def limits_line(entry):
    """One blockquote line naming every partial / no sub-level, or None."""
    limited = [(label, sub["note"]) for label, sub in sub_levels(entry) if sub["level"] != "full"]
    if not limited:
        return None
    parts, used = [], set()
    for i, (label, note) in enumerate(limited):
        if i in used:
            continue
        labels = [label]
        for j in range(i + 1, len(limited)):
            if j not in used and limited[j][1] == note:
                labels.append(limited[j][0])
                used.add(j)
        parts.append(f"{' and '.join(labels)}: {note}")
    return "> **Limits.** " + " ".join(parts)


def glance_row(name, entry):
    return f"| {name} | " + " | ".join(SYMBOL[s["level"]] for _, s in sub_levels(entry)) + " |"


def glance_block(names, skills):
    rows = [glance_row(n, skills[n]) for n in names]
    return "\n".join([
        "<details>",
        "<summary>Compatibility at a glance</summary>",
        "",
        GLANCE_HEADER,
        "|---|---|---|---|---|---|",
        *rows,
        "",
        f"✔ full · ◐ partial · ✖ no. What each host means, and the limits behind each mark: [Compatibility]({ROOT_LINK}).",
        "",
        "</details>",
    ])


def skills_on_disk():
    found = {}
    if not os.path.isdir(PLUGINS_DIR):
        return found
    for pack in sorted(os.listdir(PLUGINS_DIR)):
        d = os.path.join(PLUGINS_DIR, pack, "skills")
        if not os.path.isdir(d):
            continue
        for s in sorted(os.listdir(d)):
            if os.path.isfile(os.path.join(d, s, "SKILL.md")):
                found[s] = pack
    return found


def section_lines(lines):
    """(start, end) line indexes of the '## What it looks like' section, fences respected."""
    start, fence = None, False
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        if fence:
            continue
        if start is None and line.strip() == SECTION:
            start = i
        elif start is not None and line.startswith("## "):
            return start, i
    return (start, len(lines)) if start is not None else (None, None)


SUMMARY_RE = re.compile(r'^<summary>(?:<b>|<code>)([a-z0-9-]+)(?:</b>|</code>)')


def check_entries(data, disk):
    if not isinstance(data.get("updated"), str):
        errors.append(f"{COMPAT}: 'updated' must be a date string")
    if set(data.get("levels", {})) != set(LEVELS):
        errors.append(f"{COMPAT}: 'levels' must define exactly {', '.join(LEVELS)}")
    if set(data.get("hosts", {})) != set(HOSTS):
        errors.append(f"{COMPAT}: 'hosts' must define exactly {', '.join(HOSTS)}")
    skills = data.get("skills", {})
    for name in sorted(set(disk) - set(skills)):
        errors.append(f"{COMPAT}: no entry for skill '{name}' (plugins/{disk[name]}/skills/{name})")
    for name in sorted(set(skills) - set(disk)):
        errors.append(f"{COMPAT}: entry '{name}' has no skill folder under plugins/*/skills/")
    good = {}
    for name, entry in sorted(skills.items()):
        if name in disk and entry.get("pack") != disk[name]:
            errors.append(f"{COMPAT}: '{name}' says pack '{entry.get('pack')}', but it lives in '{disk[name]}'")
        try:
            subs = sub_levels(entry)
        except (KeyError, TypeError):
            errors.append(f"{COMPAT}: '{name}' needs claude.code, claude.app, codex_chatgpt.codex, "
                          f"codex_chatgpt.chatgpt and other")
            continue
        ok = True
        for label, sub in subs:
            level = sub.get("level") if isinstance(sub, dict) else None
            if level not in LEVELS:
                errors.append(f"{COMPAT}: '{name}' {label} level {level!r} is not one of {', '.join(LEVELS)}")
                ok = False
            elif level != "full" and not (isinstance(sub.get("note"), str) and sub["note"].strip()):
                errors.append(f"{COMPAT}: '{name}' {label} is '{level}' but has no note")
                ok = False
        if ok:
            good[name] = entry
    return good


def check_readme(pack, names, skills):
    readme = os.path.join(PLUGINS_DIR, pack, "README.md")
    if not os.path.isfile(readme):
        errors.append(f"{readme}: file not found")
        return
    with open(readme, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    start, end = section_lines(lines)
    if start is None:
        errors.append(f"{readme}: no '{SECTION}' section to hold the compatibility badges")
        return

    # Glance table: one row per skill in the pack, each matching the JSON.
    try:
        h = lines.index(GLANCE_HEADER, start, end)
    except ValueError:
        errors.append(f"{readme}: no 'Compatibility at a glance' table in '{SECTION}'")
    else:
        rows, j = {}, h + 2
        while j < end and lines[j].startswith("|"):
            cells = [c.strip() for c in lines[j].strip("|").split("|")]
            rows[cells[0]] = lines[j]
            j += 1
        for n in names:
            if n in skills and rows.get(n) != glance_row(n, skills[n]):
                errors.append(f"{readme}: glance-table row for '{n}' should read: {glance_row(n, skills[n])}")
        for n in sorted(set(rows) - set(names)):
            errors.append(f"{readme}: glance table lists '{n}', which is not a skill in this pack")

    # Badge line (and limits line) as the first lines of each skill's <details> body.
    expected = {badge_line(skills[n]) for n in names if n in skills}
    for i in range(start, end):
        m = SUMMARY_RE.match(lines[i].strip())
        if not m or m.group(1) not in skills or m.group(1) not in names:
            continue
        n = m.group(1)
        body = [k for k in range(i + 1, end) if lines[k].strip()]
        want = badge_line(skills[n])
        if not body or lines[body[0]] != want:
            errors.append(f"{readme}:{i + 2}: '{n}' badge line should be the first line in its <details> "
                          f"body and read:\n      {want}")
            continue
        lim = limits_line(skills[n])
        nxt = lines[body[1]] if len(body) > 1 else ""
        if lim and nxt != lim:
            errors.append(f"{readme}:{body[0] + 2}: '{n}' limits line should follow its badges and read:\n      {lim}")
        if not lim and nxt.startswith("> **Limits.**"):
            errors.append(f"{readme}:{body[1] + 1}: '{n}' is full everywhere, so it takes no limits line")

    # Every badge line anywhere in the README must be a current one for this pack.
    for i, line in enumerate(lines):
        if "img.shields.io/badge/Claude-" in line and line not in expected:
            errors.append(f"{readme}:{i + 1}: badge line does not match {COMPAT} for any skill in this pack")


def check_skill_readme(pack, name, entry):
    """The skill's own README carries exactly one badge line, and the limits line, from the JSON."""
    readme = os.path.join(PLUGINS_DIR, pack, "skills", name, "README.md")
    if not os.path.isfile(readme):
        errors.append(f"{readme}: file not found -- run python3 scripts/gen-skill-readme.py")
        return
    with open(readme, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    want = badge_line(entry, SKILL_ROOT_LINK)
    hits = [i for i, line in enumerate(lines) if "img.shields.io/badge/Claude-" in line]
    if len(hits) != 1 or lines[hits[0]] != want:
        errors.append(f"{readme}: needs exactly one badge line, reading:\n      {want}")
        return
    nxt = next((line for line in lines[hits[0] + 1:] if line.strip()), "")
    lim = limits_line(entry)
    if lim and nxt != lim:
        errors.append(f"{readme}:{hits[0] + 1}: limits line should follow the badges and read:\n      {lim}")
    if not lim and nxt.startswith("> **Limits.**"):
        errors.append(f"{readme}:{hits[0] + 1}: '{name}' is full everywhere, so it takes no limits line")


def main():
    if not os.path.isfile(COMPAT):
        print(f"{COMPAT}: file not found", file=sys.stderr)
        return 1
    try:
        with open(COMPAT, encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as e:
        print(f"{COMPAT}: invalid JSON ({e})", file=sys.stderr)
        return 1
    disk = skills_on_disk()
    skills = check_entries(data, disk)
    for pack in sorted(set(disk.values())):
        check_readme(pack, sorted(s for s, p in disk.items() if p == pack), skills)
    for name, pack in sorted(disk.items()):
        if name in skills:
            check_skill_readme(pack, name, skills[name])
    if errors:
        print(f"{len(errors)} compatibility problem(s) found:\n", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"{COMPAT} covers all {len(disk)} skills and matches every pack README's badges and table "
          f"and every skill README's badges")
    return 0


if __name__ == "__main__":
    sys.exit(main())
