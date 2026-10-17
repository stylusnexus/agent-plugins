<!-- skill-readme:begin -->
# agent-watchdog

Use when asked to watch, babysit, audit, review, compare, or fix another agent's work from a Codex session ID, Claude Code session/transcript, chat/thread link, PR, branch, log, or pasted run summary. Monitor until the other agent is done or blocked, reconstruct what the user asked, inspect what the agent actually changed and verified, report gaps, and optionally make scoped fixes when the user authorizes repair.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Audits a pasted transcript or summary only; no repo diff, CI or session-file access.

Part of the [second-opinion](../../README.md) pack.

## When and how to use it

**Use it when:** Another agent says it finished and you want proof against your original request.

**Try:** `Audit the Claude Code session for the login fix and list any gaps.`

**Skip it when:** You want your own current work reviewed, not another agent's run.

## What it looks like

*Example output, invented data.*

```text
Status          Done
Requested       Add CSV export to the reports page, with a test; no schema changes.
Observed        Export button and route added; agent says "all tests pass".
Gaps
  Bug                export route skips the team filter (app/api/reports/export.ts:22)
  Verification miss  claimed test run not in the transcript; CI shows 1 failing test
  Scope drift        renamed two unrelated helpers in lib/format.ts
Fixes made      (audit only, none)
Remaining risk  CI red until the failing test is fixed; rename needs a decision.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install second-opinion@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install second-opinion@stylus-nexus` do the same. This installs the whole second-opinion pack, so debug-feedback-loop, efficient-frontier-routing, llm-council, plan-arbiter and spec-review come with it.

Call it as `/second-opinion:agent-watchdog`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **second-opinion**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add second-opinion@stylus-nexus
```

This installs the whole second-opinion pack, so debug-feedback-loop, efficient-frontier-routing, llm-council, plan-arbiter and spec-review come with it. In Codex, type `$` and the skill name (`$second-opinion:agent-watchdog`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill agent-watchdog
```

Skills arrive without a pack prefix: `/agent-watchdog` in most agents and `@agent-watchdog` in Windsurf. opencode shows `/agent-watchdog` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/second-opinion/skills/agent-watchdog .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `agent-watchdog` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/second-opinion/skills
   zip -r agent-watchdog.zip agent-watchdog
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `agent-watchdog.zip`.

**Limit:** Audits a pasted transcript or summary only; no repo diff, CI or session-file access.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole second-opinion pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Audits a pasted transcript or summary only; no repo diff, CI or session-file access.

</details>
<!-- skill-readme:end -->

## /agent-watchdog

Audit another agent's work from a session, transcript, PR, branch, or run
summary.

`/agent-watchdog` is for the common handoff where one agent needs to watch
another agent finish, then check whether the work actually matches what was
asked.

## What It Does

- Resolves Codex, Claude Code, PR, branch, transcript, or pasted run artifacts.
- Waits for completion when the user asks to watch.
- Reconstructs the original request and later scope changes.
- Checks the agent's claims against diffs, files, tests, CI, screenshots, and
  review state.
- Reports gaps, weak verification, scope drift, and residual risk.
- Makes narrow fixes when the user explicitly authorizes repair.

## When To Use It

Use it when a user says things like:

- "Watch this session until done and audit it."
- "Claude finished, check what it did and fix gaps."
- "Compare these two agents' work."
- "Babysit this PR and make sure the agent actually handled the feedback."

Skip it for normal code review when there is no other agent session or run to
audit.

## Modes

- Watch only: monitor and report, no edits.
- Audit: inspect the work and produce a gap report, no edits.
- Audit and fix: repair clear gaps with targeted validation.
- Compare: evaluate multiple sessions against the same request.
