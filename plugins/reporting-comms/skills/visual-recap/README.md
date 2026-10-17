<!-- skill-readme:begin -->
# visual-recap

Turn a PR, branch, commit, or git diff into an interactive visual recap with diagrams, file maps, API/schema summaries, annotated diffs, and focused review notes.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)

> **Limits.** Claude app: Hosted mode may work if the Plan MCP is added as a custom connector (unverified); no repo access, so the source must be pasted. ChatGPT: Hosted mode only if the Plan MCP can be added as a ChatGPT connector (unverified); no repo access. Other agents: Local mode needs a shell, npx, network and a browser; hosted mode needs the Plan MCP set up by hand, and the skill has no inline fallback.

Part of the [reporting-comms](../../README.md) pack.

## When and how to use it

**Use it when:** A branch or PR is finished and a reviewer needs the shape of the change first.

**Try:** `/visual-recap the reminder-timer branch`

**Skip it when:** The change is not written yet. Use `visual-plan`.

## What it looks like

Example output, invented data (fictional project). Follows the skill's fixed order, top to bottom, and its budgets.

```text
Recap: travel mode for reminders                   (title, under 70 characters)
1 UI headline   before/after wireframes: settings screen, then the new sheet
                after-only: paused banner on the home screen
2 Narrative     2 paragraphs: why reminders pause, and the time-zone risk
3 data-model    schedules table: pause_start added, pause_end added
  api-endpoint  POST /schedules/{id}/pause (added)
4 file-tree     9 files: 6 modified, 3 added
5 Key changes   5 tabs, each a split diff with a one-line summary and notes
Not included    secrets in config: redacted as <redacted>
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install reporting-comms@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install reporting-comms@stylus-nexus` do the same. This installs the whole reporting-comms pack, so html, human-writing, recap-table, redline, visual-plan and writing-clearly-and-concisely come with it.

Call it as `/reporting-comms:visual-recap`, or let it start on its own when your request matches.

**Note:** Needs npx and network (local mode) or the hosted Plan MCP.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **reporting-comms**. Plugins do not load in the app's cloud sessions.

**Note:** Needs npx and network (local mode) or the hosted Plan MCP.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add reporting-comms@stylus-nexus
```

This installs the whole reporting-comms pack, so html, human-writing, recap-table, redline, visual-plan and writing-clearly-and-concisely come with it. In Codex, type `$` and the skill name (`$reporting-comms:visual-recap`), or run `/skills` to pick it.

**Note:** Needs npx and network (local mode) or the hosted Plan MCP.

</details>

<details>
<summary>Other agents, Skills CLI (partial)</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill visual-recap
```

Skills arrive without a pack prefix: `/visual-recap` in most agents and `@visual-recap` in Windsurf. opencode shows `/visual-recap` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Limit:** Local mode needs a shell, npx, network and a browser; hosted mode needs the Plan MCP set up by hand, and the skill has no inline fallback.

</details>

<details>
<summary>Other agents, by folder (partial)</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/reporting-comms/skills/visual-recap .agents/skills/
```

**Limit:** Local mode needs a shell, npx, network and a browser; hosted mode needs the Plan MCP set up by hand, and the skill has no inline fallback.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `visual-recap` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/reporting-comms/skills
   zip -r visual-recap.zip visual-recap
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `visual-recap.zip`.

**Limit:** Hosted mode may work if the Plan MCP is added as a custom connector (unverified); no repo access, so the source must be pasted.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole reporting-comms pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Hosted mode only if the Plan MCP can be added as a ChatGPT connector (unverified); no repo access.

</details>
<!-- skill-readme:end -->
