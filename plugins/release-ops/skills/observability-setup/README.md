<!-- skill-readme:begin -->
# observability-setup

Wire a web service for observability sized for a small team - health-check endpoint, uptime checks, log forwarding, error tracking, product analytics, LLM cost tracking, and page-vs-ticket alert thresholds. Examples use Render, Better Stack, Sentry, and PostHog. Use when launching a new service, auditing monitoring on an existing one, or on "set up monitoring", "add a health check", "forward logs", "we get paged too much", or "alert fatigue".

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Writes the health route and alert table; the done criteria need the live host, monitor and error tracker.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** You launch a new web service, or you get paged too often and want better alerts.

**Try:** `Audit the monitoring on our orders-api service and tell me what is missing.`

**Skip it when:** The service is already down. Use `incident-response`.

## What it looks like

Example output, invented data.

```text
Monitoring audit: notes-api (existing service)
[x] GET /api/health returns 200 with the DB up, 503 with it down (both tested)
[ ] Host health check path not set: a deploy that can't reach the DB still gets traffic
[x] Uptime monitor on /api/health every 1 min, confirmation period 2 min, pages on-call
[ ] No test log line in the log tool: the log stream is not configured
[x] Test exception visible in the error tracker with area=billing
[ ] Alert table still has the template numbers; not agreed with whoever gets paged

Gaps: 3. Set the health check path first.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, pr-wait, the-waiting, version-check and vscode-marketplace-publish come with it.

Call it as `/release-ops:observability-setup`, or let it start on its own when your request matches.

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

This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, pr-wait, the-waiting, version-check and vscode-marketplace-publish come with it. In Codex, type `$` and the skill name (`$release-ops:observability-setup`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill observability-setup
```

Skills arrive without a pack prefix: `/observability-setup` in most agents and `@observability-setup` in Windsurf. opencode shows `/observability-setup` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/observability-setup .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `observability-setup` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/release-ops/skills
   zip -r observability-setup.zip observability-setup
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `observability-setup.zip`.

**Limit:** Writes the health route and alert table; the done criteria need the live host, monitor and error tracker.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole release-ops pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Writes the health route and alert table; the done criteria need the live host, monitor and error tracker.

</details>
<!-- skill-readme:end -->
