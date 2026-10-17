<!-- skill-readme:begin -->
# analytics-instrumentation

PostHog event taxonomy and instrumentation review - object_verb naming, flat property schemas, identify/reset/group calls, PII exclusion, LLM usage events, a starter dashboard set (activation, retention, feature funnel), and a per-feature checklist. Use when instrumenting a new feature, auditing existing PostHog events, or setting up analytics for a new product, e.g. "add tracking", "what events should we fire", "review our PostHog events", "is there PII in analytics".

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Event taxonomy and code from pasted snippets only; no audit over the repo and no live PostHog check.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** You are adding tracking to a new feature, or want to check the PostHog events you already send.

**Try:** `Review our PostHog events for naming and personal data`

**Skip it when:** You need a one-off answer from existing data. This skill designs and audits events and dashboards; it does not run analyses.

## What it looks like

Example output, invented data.

```text
Capture calls found: 31 (rg -n "posthog\.capture\(")

PII in capture() properties: 2 hits
  src/share/dialog.tsx:58   project_shared { email: invitee.email }
  src/search/bar.tsx:21     search_submitted { query: input.value } (raw user input)
Names that break object_verb: 3, with a rename plan
  created_project     → project_created
  button_clicked      → project_export_clicked
  project_created_v2  → project_created plus a version property
identify(): on signup ✓, on login ✗ (src/auth/login.ts)
reset() on logout: ✓
Result: FAIL. The PII is already in production, so this goes to the
project owner (fix plus possible deletion of past events).
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:analytics-instrumentation`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **ship-pipeline**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
```

This installs the whole ship-pipeline pack, so api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:analytics-instrumentation`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill analytics-instrumentation
```

Skills arrive without a pack prefix: `/analytics-instrumentation` in most agents and `@analytics-instrumentation` in Windsurf. opencode shows `/analytics-instrumentation` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/analytics-instrumentation .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `analytics-instrumentation` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/ship-pipeline/skills
   zip -r analytics-instrumentation.zip analytics-instrumentation
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `analytics-instrumentation.zip`.

**Limit:** Event taxonomy and code from pasted snippets only; no audit over the repo and no live PostHog check.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole ship-pipeline pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Event taxonomy and code from pasted snippets only; no audit over the repo and no live PostHog check.

</details>
<!-- skill-readme:end -->
