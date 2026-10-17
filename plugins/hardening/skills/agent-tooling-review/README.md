<!-- skill-readme:begin -->
# agent-tooling-review

Use when connecting, auditing, or widening the permissions of tooling an AI agent can call: MCP servers, plugins, skills, database or GitHub connections, API tokens issued to an agent, or an agent that will run unattended (scheduled, looped, event-triggered, background, CI). Triggers: a new MCP or plugin is about to be added, an agent needs write access it did not have, a connection points at production, an unattended job is being set up, or a tool's description changed after approval.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Reviews pasted config by hand; no repo or CI inventory, hashing or AgentArmor scan.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** You are about to add an MCP server, or a nightly agent job needs write access.

**Try:** `Review the MCP connections in this repo and the nightly-triage job. Keep, narrow or disconnect each one.`

**Skip it when:** The tools belong to a model inside your own product. Use llm-app-security.

## What it looks like

*Example output, invented data.*

```text
| Connection  | Transport             | Credential and scope           | Env           | Verdict    |
| docs-search | stdio, pinned 1.4.2   | none                           | n/a           | keep       |
| repo-tools  | stdio, unpinned       | classic token: repo, workflow  | prod          | narrow: 1 repo,     |
|             |                       |                                |               | contents:read, pin  |
| db-query    | remote URL            | app's own role (write)         | unknown=prod  | disconnect |
UNVERIFIED: repo-tools provenance (offline); db-query tool list (not started, by rule)

Unattended job: nightly-triage (CI)
  PASS narrow job · PASS scoped repo access · FAIL least-privilege credentials (shares
  the attended token) · PASS safe stopping points · FAIL action log (nobody reads it)
  PASS human approval gate · FAIL blast radius (not written down)
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it.

Call it as `/hardening:agent-tooling-review`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **hardening**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add hardening@stylus-nexus
```

This installs the whole hardening pack, so auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:agent-tooling-review`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill agent-tooling-review
```

Skills arrive without a pack prefix: `/agent-tooling-review` in most agents and `@agent-tooling-review` in Windsurf. opencode shows `/agent-tooling-review` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/agent-tooling-review .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `agent-tooling-review` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/hardening/skills
   zip -r agent-tooling-review.zip agent-tooling-review
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `agent-tooling-review.zip`.

**Limit:** Reviews pasted config by hand; no repo or CI inventory, hashing or AgentArmor scan.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole hardening pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Reviews pasted config by hand; no repo or CI inventory, hashing or AgentArmor scan.

</details>
<!-- skill-readme:end -->
