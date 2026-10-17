<!-- skill-readme:begin -->
# redline

Hand a draft, plan, report, or page to the human to mark up in a browser; Send returns one Markdown review file the agent applies. Use for anything a person must judge rather than a machine - "let me look at it", "let me mark it up", "/redline". Not for machine-checkable correctness (/prove-it, /code-review).

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Needs a local browser and your Downloads folder. ChatGPT: Needs a local browser page and your Downloads folder, with no stated fallback.

Part of the [reporting-comms](../../README.md) pack.

## When and how to use it

**Use it when:** A person must judge a draft by editing it and commenting on exact quotes.

**Try:** `/redline draft-announcement.md`

**Skip it when:** A test or a tool can answer the question. Run that instead.

## What it looks like

Example output, invented data (fictional project). Edits are the person's exact words and are applied verbatim. Comments are tied to a quote from the page.

```text
release-notes.redline.md

## Overall
Shorter. Lead with what users notice.

## Edits the human already made
### Lede
- before: Travel mode introduces a new paradigm for reminder scheduling.
- after:  Going away? Reminders now pause until you're back.

## Comments
### 1. Known issues
> may skip one watering across time zones
Say which time zones, or cut it.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install reporting-comms@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install reporting-comms@stylus-nexus` do the same. This installs the whole reporting-comms pack, so html, human-writing, recap-table, visual-plan, visual-recap and writing-clearly-and-concisely come with it.

Call it as `/reporting-comms:redline`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **reporting-comms**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add reporting-comms@stylus-nexus
```

This installs the whole reporting-comms pack, so html, human-writing, recap-table, visual-plan, visual-recap and writing-clearly-and-concisely come with it. In Codex, type `$` and the skill name (`$reporting-comms:redline`), or run `/skills` to pick it.

**Note:** Opens a local browser page and reads the returned file from your Downloads folder, which may prompt.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill redline
```

Skills arrive without a pack prefix: `/redline` in most agents and `@redline` in Windsurf. opencode shows `/redline` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Needs local file writes, a browser opener and read access to your Downloads folder.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/reporting-comms/skills/redline .agents/skills/
```

**Note:** Needs local file writes, a browser opener and read access to your Downloads folder.

</details>

<details>
<summary>Claude app: not supported</summary>

**Why:** Needs a local browser and your Downloads folder.

</details>

<details>
<summary>ChatGPT: not supported</summary>

**Why:** Needs a local browser page and your Downloads folder, with no stated fallback.

</details>
<!-- skill-readme:end -->
