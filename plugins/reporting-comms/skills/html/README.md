<!-- skill-readme:begin -->
# html

Turn complex output (plans, code reviews, research, comparisons, configs, reports) into a single self-contained, reading-first HTML artifact. Structure before style, inline CSS only, no network calls, Markdown export for handoff. Use when the user says "make this an HTML page/report/artifact", "turn this into HTML", "/html", asks for a visual explainer, decision page, code-review page, a summary, recap, wrap-up or handover *page* (including "make it ADHD friendly" or "accessible"; branch or PR recaps use visual-recap, recap tables use recap-table), or a small one-file editor, or when a terminal answer is too long/dense to read comfortably.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Can build the HTML file in the sandbox for download, without grounding in your repo.

Part of the [reporting-comms](../../README.md) pack.

## When and how to use it

**Use it when:** A plan, review or report is too long to read in the terminal.

**Try:** `/html turn this code review into a readable page`

**Skip it when:** The idea is still rough. Keep it in Markdown.

## What it looks like

Example output, invented data (fictional project). The outline of a summary page: under 200 body words, and a drawing in every section after the title.

```text
artifacts/html/sprint-summary.html            (one file, inline CSS, no network)

Plant Ledger: sprint 14 summary
  What this is: the state of the reminders rework at the end of the sprint

AT A GLANCE      [ 12 files ]   [ 3 of 4 tasks done ]   [ 1 blocked ]
BODY             flow drawing: schedule > reminder queue > push > phone
                 bar chart: reminders sent late, 9% before > 1% after
DECISIONS        ● Queue moved to a background job
                 ● Retries capped at 3
OPEN AND NEXT    ○ Travel mode: blocked on the time-zone fix
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install reporting-comms@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install reporting-comms@stylus-nexus` do the same. This installs the whole reporting-comms pack, so human-writing, recap-table, redline, visual-plan, visual-recap and writing-clearly-and-concisely come with it.

Call it as `/reporting-comms:html`, or let it start on its own when your request matches.

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

This installs the whole reporting-comms pack, so human-writing, recap-table, redline, visual-plan, visual-recap and writing-clearly-and-concisely come with it. In Codex, type `$` and the skill name (`$reporting-comms:html`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill html
```

Skills arrive without a pack prefix: `/html` in most agents and `@html` in Windsurf. opencode shows `/html` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/reporting-comms/skills/html .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `html` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/reporting-comms/skills
   zip -r html.zip html
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `html.zip`.

**Limit:** Can build the HTML file in the sandbox for download, without grounding in your repo.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole reporting-comms pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Can build the HTML file in the sandbox for download, without grounding in your repo.

</details>
<!-- skill-readme:end -->
