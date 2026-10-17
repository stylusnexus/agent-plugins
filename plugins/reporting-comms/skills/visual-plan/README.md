<!-- skill-readme:begin -->
# visual-plan

Turn ordinary text plans into rich interactive visual plans with diagrams, file maps, annotated code, open questions, and UI/prototype review when useful.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)

> **Limits.** Claude app: Hosted mode may work if the Plan MCP is added as a custom connector (unverified); no repo access, so the source must be pasted. ChatGPT: Hosted mode only if the Plan MCP can be added as a ChatGPT connector (unverified); no repo access. Other agents: Local mode needs a shell, npx, network and a browser; hosted mode needs the Plan MCP set up by hand, and the skill has no inline fallback.

Part of the [reporting-comms](../../README.md) pack.

## When and how to use it

**Use it when:** You have a plan to approve and want diagrams and open questions beside it.

**Try:** `/visual-plan the plan to move reminders to per-plant timers`

**Skip it when:** You want to explain work that is already done. Use `visual-recap`.

## What it looks like

Example exchange, invented data (fictional project).

```text
You:    /visual-plan add travel mode to the reminder settings

Agent:  Read the settings screen, the reminder action, and the schedule schema.
        Mode: UI-first. The top canvas shows 3 states: settings, travel-mode
        sheet, and the paused banner on the home screen.
        Hard-to-reverse decision called out: where the pause dates are stored.
        Wrote plans/travel-mode/ (local files), ran plan local check, then serve.
        Plan: <local bridge URL printed by serve>
        Open questions (bottom form): catch up missed waterings, or skip them?
        Touches: settings screen, reminder action, schedule table.
        Review it and approve before I write any code.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install reporting-comms@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install reporting-comms@stylus-nexus` do the same. This installs the whole reporting-comms pack, so html, human-writing, recap-table, redline, visual-recap and writing-clearly-and-concisely come with it.

Call it as `/reporting-comms:visual-plan`, or let it start on its own when your request matches.

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

This installs the whole reporting-comms pack, so html, human-writing, recap-table, redline, visual-recap and writing-clearly-and-concisely come with it. In Codex, type `$` and the skill name (`$reporting-comms:visual-plan`), or run `/skills` to pick it.

**Note:** Needs npx and network (local mode) or the hosted Plan MCP.

</details>

<details>
<summary>Other agents, Skills CLI (partial)</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill visual-plan
```

Skills arrive without a pack prefix: `/visual-plan` in most agents and `@visual-plan` in Windsurf. opencode shows `/visual-plan` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Limit:** Local mode needs a shell, npx, network and a browser; hosted mode needs the Plan MCP set up by hand, and the skill has no inline fallback.

</details>

<details>
<summary>Other agents, by folder (partial)</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/reporting-comms/skills/visual-plan .agents/skills/
```

**Limit:** Local mode needs a shell, npx, network and a browser; hosted mode needs the Plan MCP set up by hand, and the skill has no inline fallback.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `visual-plan` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/reporting-comms/skills
   zip -r visual-plan.zip visual-plan
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `visual-plan.zip`.

**Limit:** Hosted mode may work if the Plan MCP is added as a custom connector (unverified); no repo access, so the source must be pasted.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole reporting-comms pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Hosted mode only if the Plan MCP can be added as a ChatGPT connector (unverified); no repo access.

</details>
<!-- skill-readme:end -->
