<!-- skill-readme:begin -->
# human-writing

Write content that sounds natural, conversational, and authentically human - avoiding AI-generated patterns, corporate speak, and generic phrasing. Also handles the "humanize this" / "humanise this" trigger - a meaning-preserving rewrite that strips signs of AI writing.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [reporting-comms](../../README.md) pack.

## When and how to use it

**Use it when:** A draft sounds like an AI wrote it.

**Try:** `humanize this: [paste the draft]`

**Skip it when:** You only need shorter text with the same tone. Use `writing-clearly-and-concisely`.

## What it looks like

Example exchange, invented text (fictional project).

```text
You:    humanize this: "We're thrilled to announce Travel Mode, a pivotal
        feature that seamlessly pauses your watering reminders while you're
        away, highlighting our commitment to plant lovers."

Agent:  Travel mode pauses your watering reminders while you're away.

        What changed:
        - cut "We're thrilled to announce" (enthusiastic opening)
        - cut "pivotal" and "seamlessly" (AI vocabulary, promotional)
        - cut "highlighting our commitment..." (trailing pseudo-analysis)
        - "Travel Mode" to "Travel mode" (title case)
        Kept: the one claim, unchanged. Nothing added.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install reporting-comms@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install reporting-comms@stylus-nexus` do the same. This installs the whole reporting-comms pack, so html, recap-table, redline, visual-plan, visual-recap and writing-clearly-and-concisely come with it.

Call it as `/reporting-comms:human-writing`, or let it start on its own when your request matches.

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

This installs the whole reporting-comms pack, so html, recap-table, redline, visual-plan, visual-recap and writing-clearly-and-concisely come with it. In Codex, type `$` and the skill name (`$reporting-comms:human-writing`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill human-writing
```

Skills arrive without a pack prefix: `/human-writing` in most agents and `@human-writing` in Windsurf. opencode shows `/human-writing` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/reporting-comms/skills/human-writing .agents/skills/
```

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `human-writing` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/reporting-comms/skills
   zip -r human-writing.zip human-writing
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `human-writing.zip`.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole reporting-comms pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
