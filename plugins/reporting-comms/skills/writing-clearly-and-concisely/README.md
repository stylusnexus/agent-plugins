<!-- skill-readme:begin -->
# writing-clearly-and-concisely

Apply Strunk's timeless writing rules to ANY prose humans will read—documentation, commit messages, error messages, explanations, reports, or UI text. Makes your writing clearer, stronger, and more professional.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [reporting-comms](../../README.md) pack.

## When and how to use it

**Use it when:** You write docs, commit messages or error text that people must read fast.

**Try:** `Tighten this error message using the clear writing rules.`

**Skip it when:** The text must sound personal and casual. Use `human-writing`.

## What it looks like

Example edit, invented text (fictional project).

> **Before:** It should be noted that reminders were not able to be delivered by the system in a number of cases when the user was traveling.
>
> **After:** Reminders failed for some traveling users.
>
> Rules applied: 10 (use active voice), 11 (put statements in positive form), 13 (omit needless words).

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install reporting-comms@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install reporting-comms@stylus-nexus` do the same. This installs the whole reporting-comms pack, so html, human-writing, recap-table, redline, visual-plan and visual-recap come with it.

Call it as `/reporting-comms:writing-clearly-and-concisely`, or let it start on its own when your request matches.

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

This installs the whole reporting-comms pack, so html, human-writing, recap-table, redline, visual-plan and visual-recap come with it. In Codex, type `$` and the skill name (`$reporting-comms:writing-clearly-and-concisely`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill writing-clearly-and-concisely
```

Skills arrive without a pack prefix: `/writing-clearly-and-concisely` in most agents and `@writing-clearly-and-concisely` in Windsurf. opencode shows `/writing-clearly-and-concisely` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/reporting-comms/skills/writing-clearly-and-concisely .agents/skills/
```

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `writing-clearly-and-concisely` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/reporting-comms/skills
   zip -r writing-clearly-and-concisely.zip writing-clearly-and-concisely
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `writing-clearly-and-concisely.zip`.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole reporting-comms pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
