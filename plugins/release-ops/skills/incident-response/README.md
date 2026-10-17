<!-- skill-readme:begin -->
# incident-response

Production incident runbook for a small team - severity call, fixed triage order, rollback-first decision, user comms, and a one-page blameless postmortem. Use when a service is down, erroring, or degraded in production, e.g. "site is down", "we're getting 500s", "uptime alert fired", "users report errors", "was it the last deploy?", "roll back", or "write the postmortem".

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Severity, triage, comms and postmortem from pasted information; no log or monitor access and no rollback.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** A production service is down or erroring and you need a fixed order of steps.

**Try:** `The site is returning 500 errors since the last deploy. Run incident response.`

**Skip it when:** The problem is a slow build or a failing test on your laptop.

## What it looks like

| Level | Definition | Response time |
|---|---|---|
| S1 | Full outage, data loss risk, or payment/auth broken | Immediate, drop everything |
| S2 | Major feature broken, some users affected, no data risk | Within the hour |
| S3 | Minor bug, cosmetic, workaround exists | Next business day |

Unsure between S1 and S2? Treat it as S1.

Example output, invented data.

```text
Alert 14:02 UTC (uptime: notes-api down). Acknowledged, not resolved. Severity: S1.
Triage
  1. Uptime monitor: every region failing; not a monitor false positive
  2. Host logs, last 30 min: 5xx spike from 13:58, crash-loop restarts
  3. Error tracker: new TypeError in the session middleware
  4. Recent deploys: one at 13:55, 7 minutes before the alert
Decision: the deploy lines up and the cause isn't clear in 5 min → roll back first
  Host rollback to the 13:10 deploy. Auto-deploy is now off; re-enable after the fix.
  git revert 9f3c2e1, pushed, so the branch matches what is running
Recovery: green, error rate at baseline 14:19–14:31 (12 min) → resolved

Status page draft:
  We're aware of an issue affecting sign-in and are actively working on it.
  Your data is safe. We'll update this within 30 minutes.
Postmortem due by 14:02 UTC tomorrow; follow-ups filed as #455 and #456.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, llm-cost-audit, npm-publish, observability-setup, pr-wait, the-waiting and version-check come with it.

Call it as `/release-ops:incident-response`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **release-ops**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add release-ops@stylus-nexus
```

This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, llm-cost-audit, npm-publish, observability-setup, pr-wait, the-waiting and version-check come with it. In Codex, type `$` and the skill name (`$release-ops:incident-response`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill incident-response
```

Skills arrive without a pack prefix: `/incident-response` in most agents and `@incident-response` in Windsurf. opencode shows `/incident-response` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/incident-response .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `incident-response` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/release-ops/skills
   zip -r incident-response.zip incident-response
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `incident-response.zip`.

**Limit:** Severity, triage, comms and postmortem from pasted information; no log or monitor access and no rollback.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole release-ops pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Severity, triage, comms and postmortem from pasted information; no log or monitor access and no rollback.

</details>
<!-- skill-readme:end -->
