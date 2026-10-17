<!-- skill-readme:begin -->
# recap-table

Use when the user asks to recap, summarize, or show work as a table; wants a before/after or what-changed comparison; asks "what did you change", "recap that", "show me a table"; or invokes /recap-table. Works in any project.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [reporting-comms](../../README.md) pack.

## When and how to use it

**Use it when:** You want a quick before and after of what changed.

**Try:** `/recap-table what did you change?`

**Skip it when:** The answer is one fact. Just say it in a sentence.

## What it looks like

Example output, invented data (fictional project). One row for each change that actually moved.

| Area | Before | After |
|------|--------|-------|
| Reminder timing | Fired on a fixed daily timer | Fires at each plant's due time |
| Travel | Reminders kept firing while away | Paused, then caught up on return |
| Missed reminder | Silently dropped | Retried up to 3 times |

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install reporting-comms@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install reporting-comms@stylus-nexus` do the same. This installs the whole reporting-comms pack, so html, human-writing, redline, visual-plan, visual-recap and writing-clearly-and-concisely come with it.

Call it as `/reporting-comms:recap-table`, or let it start on its own when your request matches.

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

This installs the whole reporting-comms pack, so html, human-writing, redline, visual-plan, visual-recap and writing-clearly-and-concisely come with it. In Codex, type `$` and the skill name (`$reporting-comms:recap-table`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill recap-table
```

Skills arrive without a pack prefix: `/recap-table` in most agents and `@recap-table` in Windsurf. opencode shows `/recap-table` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/reporting-comms/skills/recap-table .agents/skills/
```

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `recap-table` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/reporting-comms/skills
   zip -r recap-table.zip recap-table
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `recap-table.zip`.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole reporting-comms pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
