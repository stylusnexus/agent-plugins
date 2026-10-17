#!/usr/bin/env python3
"""Generate a README.md inside every skill folder from three sources.

  - SKILL.md frontmatter: the name and description.
  - compatibility.json: the level and note per host, which drive the
    collapsed Install steps.
  - the skill's entry in its pack README's "## What it looks like" section:
    the badge line, the limits line, the Use it when / Try / Skip it when
    lines and the example. These are copied verbatim, with relative links
    rewritten so they resolve from the skill folder. The pack README stays
    the one place this text is written.

Everything generated sits between the two markers below. Text an author adds
outside them is kept. A README that exists without the markers gets the
generated block put in front of its current text.

  python3 scripts/gen-skill-readme.py          # write every skill README
  python3 scripts/gen-skill-readme.py --check  # exit 1 if any is missing or stale (CI)

Pure standard library so CI needs no install step.
"""
import json
import os
import posixpath
import re
import sys

PLUGINS_DIR = "plugins"
COMPAT = "compatibility.json"
BEGIN, END = "<!-- skill-readme:begin -->", "<!-- skill-readme:end -->"
SECTION = "## What it looks like"
SUMMARY_RE = re.compile(r'^<summary>(?:<b>|<code>)([a-z0-9-]+)(?:</b>|</code>)')
FENCE_RE = re.compile(r'^\s*(```|~~~)')
MD_LINK_RE = re.compile(r'(\]\()([^)\s]+)(\))')
HTML_ATTR_RE = re.compile(r'((?:href|src)\s*=\s*["\'])([^"\']+)(["\'])', re.I)
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')
MARKETPLACE = "stylusnexus/agent-plugins"
MARKET_NAME = "stylus-nexus"
REPO_URL = "https://github.com/stylusnexus/agent-plugins"
SKILLS_CLI = "https://github.com/vercel-labs/skills"
WHOLE_PACK = "Install the whole pack"


# ---------- sources ----------

def frontmatter(path):
    """name and description from a SKILL.md, for the YAML shapes this repo uses."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        sys.exit(f"{path}: no frontmatter")
    lines = m.group(1).split("\n")
    out = {}
    i = 0
    while i < len(lines):
        km = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", lines[i])
        if not km:
            i += 1
            continue
        key, val = km.group(1), km.group(2).strip()
        cont = []
        j = i + 1
        while j < len(lines) and (lines[j][:1] in (" ", "\t") or not lines[j].strip()):
            cont.append(lines[j].strip())
            j += 1
        if val in (">", ">-", "|", "|-", ">+", "|+"):
            val = " ".join(c for c in cont if c)
        elif val.startswith('"'):
            val = json.loads(" ".join([val] + [c for c in cont if c]))
        elif val.startswith("'"):
            val = " ".join([val] + [c for c in cont if c])[1:-1].replace("''", "'")
        else:
            val = " ".join([val] + [c for c in cont if c])
        out[key] = val
        i = j
    return out.get("name"), out.get("description")


def rewrite_links(line, prefix):
    """Rebase relative link and image targets on one line, outside inline code."""
    def fix(target):
        if not target or SCHEME_RE.match(target) or target.startswith("//"):
            return target
        path, hash_, frag = target.partition("#")
        path = path or "README.md"
        return posixpath.normpath(posixpath.join(prefix, path)) + hash_ + frag

    parts = line.split("`")
    for k in range(0, len(parts), 2):
        seg = MD_LINK_RE.sub(lambda m: m.group(1) + fix(m.group(2)) + m.group(3), parts[k])
        parts[k] = HTML_ATTR_RE.sub(lambda m: m.group(1) + fix(m.group(2)) + m.group(3), seg)
    return "`".join(parts)


def rebase(block, prefix):
    out, fence = [], False
    for line in block:
        if FENCE_RE.match(line):
            fence = not fence
            out.append(line)
        else:
            out.append(line if fence else rewrite_links(line, prefix))
    return out


def trim(block):
    while block and not block[0].strip():
        block = block[1:]
    while block and not block[-1].strip():
        block = block[:-1]
    return block


def pack_entries(pack):
    """skill -> {badges, limits, usage[3], example[]} from the pack README."""
    readme = os.path.join(PLUGINS_DIR, pack, "README.md")
    with open(readme, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    entries, fence, in_section, i = {}, False, False, 0
    while i < len(lines):
        line = lines[i]
        if FENCE_RE.match(line):
            fence = not fence
        elif not fence and line.strip() == SECTION:
            in_section = True
        elif not fence and in_section and line.startswith("## "):
            break
        m = SUMMARY_RE.match(line.strip()) if (in_section and not fence) else None
        if not m:
            i += 1
            continue
        name, depth, f2, j = m.group(1), 1, False, i + 1
        while j < len(lines):
            if FENCE_RE.match(lines[j]):
                f2 = not f2
            elif not f2 and lines[j].strip().startswith("<details"):
                depth += 1
            elif not f2 and lines[j].strip() == "</details>":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = lines[i + 1:j]
        filled = [k for k, l in enumerate(body) if l.strip()]
        where = f"{readme}:{i + 1}: '{name}'"
        if not filled or "img.shields.io/badge/Claude-" not in body[filled[0]]:
            sys.exit(f"{where}: the first line of the entry must be its badge line")
        k = 1
        limits = None
        if body[filled[k]].startswith("> **Limits.**"):
            limits = body[filled[k]]
            k += 1
        want = ("**Use it when:**", "**Try:**", "**Skip it when:**")
        usage = [body[filled[k + n]] for n in range(3)] if len(filled) >= k + 3 else []
        if len(usage) != 3 or not all(u.startswith(w) for u, w in zip(usage, want)):
            sys.exit(f"{where}: after the badges (and limits) come the Use it when, Try and Skip it when lines")
        example = trim(body[filled[k + 2] + 1:])
        if not example:
            sys.exit(f"{where}: no example after the Skip it when line")
        entries[name] = {"badges": body[filled[0]], "limits": limits, "usage": usage, "example": example}
        i = j + 1
    return entries


# ---------- rendering ----------

def and_list(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def note_line(sub):
    if not sub.get("note"):
        return []
    label = "Note" if sub["level"] == "full" else "Limit"
    return [f"**{label}:** {sub['note']}", ""]


def details(summary, body):
    return ["<details>", f"<summary>{summary}</summary>", "", *body, "</details>", ""]


def not_supported(host, sub):
    return details(f"{host}: not supported", [f"**Why:** {sub['note']}", ""])


def install(skill, pack, siblings, entry):
    code, app = entry["claude"]["code"], entry["claude"]["app"]
    codex, gpt = entry["codex_chatgpt"]["codex"], entry["codex_chatgpt"]["chatgpt"]
    other = entry["other"]
    whole = (other.get("note") or "").startswith(WHOLE_PACK)
    others = [s for s in siblings if s != skill]
    with_pack = (f"This installs the whole {pack} pack, so {and_list(others)} "
                 f"{'comes' if len(others) == 1 else 'come'} with it.") if others else ""

    out = ["## Install", ""]
    if whole:
        out += [f"This skill reads shared files in its sibling skills, so install the whole {pack} pack. "
                "The Claude Code and Codex plugins do that already; with the Skills CLI or a folder "
                "copy, take every skill in the pack.", ""]

    def lvl(host, sub):
        return host if sub["level"] == "full" else f"{host} ({sub['level']})"

    if code["level"] == "no":
        out += not_supported("Claude Code (CLI)", code)
        out += not_supported("Claude Code desktop app", code)
    else:
        out += details(lvl("Claude Code (CLI)", code), [
            "Add the marketplace once, then install the pack:", "",
            "```bash",
            f"claude plugin marketplace add {MARKETPLACE}",
            f"claude plugin install {pack}@{MARKET_NAME}",
            "```", "",
            f"Inside a session, `/plugin marketplace add {MARKETPLACE}` and "
            f"`/plugin install {pack}@{MARKET_NAME}` do the same. {with_pack}".rstrip(), "",
            f"Call it as `/{pack}:{skill}`, or let it start on its own when your request matches.", "",
            *note_line(code),
        ])
        out += details(lvl("Claude Code desktop app", code), [
            "The desktop app's local sessions read the same plugin settings as the CLI, so a pack "
            "you installed from the terminal at user scope is already there.", "",
            "To install from the app, add the marketplace once from a terminal with "
            f"`claude plugin marketplace add {MARKETPLACE}`. Then, in a local or SSH session on the "
            "**Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, "
            f"and pick **{pack}**. Plugins do not load in the app's cloud sessions.", "",
            *note_line(code),
        ])

    if codex["level"] == "no":
        out += not_supported("Codex", codex)
    else:
        out += details(lvl("Codex", codex), [
            "```bash",
            f"codex plugin marketplace add {MARKETPLACE}",
            f"codex plugin add {pack}@{MARKET_NAME}",
            "```", "",
            f"{with_pack} In Codex, type `$` and the skill name (`${pack}:{skill}`), "
            "or run `/skills` to pick it.".lstrip(), "",
            *note_line(codex),
        ])

    if other["level"] == "no":
        out += not_supported("Other agents, Skills CLI", other)
        out += not_supported("Other agents, by folder", other)
    else:
        if whole:
            cli = ["This skill reads shared files in its sibling skills, so install every skill in the pack:", "",
                   "```bash", f"npx skills add {MARKETPLACE} --skill {' '.join(siblings)}", "```", ""]
            cp = f"cp -R agent-plugins/plugins/{pack}/skills/. .agents/skills/"
            cp_lead = "Copy every skill in the pack, so the shared files sit beside this one:"
        else:
            cli = ["```bash", f"npx skills add {MARKETPLACE} --skill {skill}", "```", ""]
            cp = f"cp -R agent-plugins/plugins/{pack}/skills/{skill} .agents/skills/"
            cp_lead = "Copy the skill folder:"
        out += details(lvl("Other agents, Skills CLI", other), [
            f"The [Skills CLI]({SKILLS_CLI}) finds the agents you have and writes the skill into "
            "each one's skills folder.", "",
            *cli,
            f"Skills arrive without a pack prefix: `/{skill}` in most agents and `@{skill}` in "
            f"Windsurf. opencode shows `/{skill}` only when the skill sets an opencode-specific "
            "metadata field, and Gemini CLI starts a skill itself after you approve it.", "",
            *note_line(other),
        ])
        out += details(lvl("Other agents, by folder", other), [
            "`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, "
            "opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read "
            "`.agents/skills`; use `.cline/skills` or `.claude/skills` there.", "",
            cp_lead, "",
            "```bash",
            f"git clone --depth 1 {REPO_URL}",
            "mkdir -p .agents/skills",
            cp,
            "```", "",
            *note_line(other),
        ])

    if app["level"] == "no":
        out += not_supported("Claude app", app)
    else:
        out += details(lvl("Claude app", app), [
            "1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team "
            "and Enterprise plans, an owner controls this.",
            f"2. Zip the skill folder, so the ZIP holds the `{skill}` folder:", "",
            "   ```bash",
            f"   git clone --depth 1 {REPO_URL}",
            f"   cd agent-plugins/plugins/{pack}/skills",
            f"   zip -r {skill}.zip {skill}",
            "   ```", "",
            "3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose "
            f"**Upload a skill** and pick `{skill}.zip`.", "",
            *note_line(app),
        ])

    if gpt["level"] == "no":
        out += not_supported("ChatGPT", gpt)
    else:
        out += details(lvl("ChatGPT", gpt), [
            f"ChatGPT gets this skill through the Codex plugin, which brings the whole {pack} pack. "
            "Run the two Codex commands above, then in ChatGPT type `@` and the skill name.", "",
            *note_line(gpt),
        ])
    return out


def render(skill, pack, siblings, desc, entry, compat):
    prefix = "../.."
    lines = [BEGIN, f"# {skill}", "", desc, "", rewrite_links(entry["badges"], prefix), ""]
    if entry["limits"]:
        lines += [rewrite_links(entry["limits"], prefix), ""]
    lines += [f"Part of the [{pack}](../../README.md) pack.", "",
              "## When and how to use it", ""]
    for u in entry["usage"]:
        lines += [rewrite_links(u, prefix), ""]
    lines += ["## What it looks like", "", *rebase(entry["example"], prefix), ""]
    lines += install(skill, pack, siblings, compat)
    while lines[-1] == "":
        lines.pop()
    return "\n".join(lines + [END])


def merge(old, block):
    """Replace the generated block in old text, or put it in front of text with no markers."""
    if old is None:
        return block + "\n"
    if BEGIN in old and END in old:
        head, rest = old.split(BEGIN, 1)
        return head + block + rest.split(END, 1)[1]
    return block + "\n\n" + old


def main():
    check = "--check" in sys.argv
    with open(COMPAT, encoding="utf-8") as fh:
        compat = json.load(fh)["skills"]
    stale, wrote, total = [], 0, 0
    for pack in sorted(os.listdir(PLUGINS_DIR)):
        sdir = os.path.join(PLUGINS_DIR, pack, "skills")
        if not os.path.isdir(sdir):
            continue
        siblings = sorted(s for s in os.listdir(sdir) if os.path.isfile(os.path.join(sdir, s, "SKILL.md")))
        entries = pack_entries(pack)
        for skill in siblings:
            total += 1
            if skill not in entries:
                sys.exit(f"plugins/{pack}/README.md: no '{SECTION}' entry for '{skill}'")
            if skill not in compat:
                sys.exit(f"{COMPAT}: no entry for '{skill}'")
            name, desc = frontmatter(os.path.join(sdir, skill, "SKILL.md"))
            if name != skill or not desc:
                sys.exit(f"{sdir}/{skill}/SKILL.md: frontmatter needs name '{skill}' and a description")
            block = render(skill, pack, siblings, desc, entries[skill], compat[skill])
            path = os.path.join(sdir, skill, "README.md")
            old = open(path, encoding="utf-8").read() if os.path.isfile(path) else None
            new = merge(old, block)
            if old == new:
                continue
            if check:
                stale.append(path)
            else:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
                wrote += 1
    if check:
        if stale:
            print(f"{len(stale)} skill README(s) missing or stale -- run python3 scripts/gen-skill-readme.py:",
                  file=sys.stderr)
            for p in stale:
                print(f"  {p}", file=sys.stderr)
            return 1
        print(f"all {total} skill READMEs match SKILL.md, {COMPAT} and the pack READMEs")
        return 0
    print(f"wrote {wrote} of {total} skill READMEs ({total - wrote} already current)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
