<!-- skill-readme:begin -->
# webhook-reliability

Design or review inbound and outbound webhooks for signature verification, idempotency, retry/backoff, dead-letter recording, replay tooling, and timeout budgets. Use when building a new webhook handler or emitter, reviewing an existing one (Stripe, GitHub, or a custom outbound webhook), or investigating a "webhook silently didn't fire" report.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Design is text; auditing an existing handler needs the code pasted in.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** You write a payment webhook handler, or a provider event was lost without any error.

**Try:** `Review the payments webhook handler for signature, duplicate events and retries.`

**Skip it when:** The app sends and receives no webhooks.

## What it looks like

*Example output, invented data.*

```text
Inbound: POST /api/webhooks/payments (provider retries for 3 days)
  Signature checked before parsing    present   raw body, constant-time compare, length check
  Idempotency on provider event id    present   unique (provider, externalId), same transaction
  Fast ack, slow work queued          present
  Non-2xx when recording fails        MISSING   catch block logs and returns 200
  Dead-letter table                   present
  Dead-letter table monitored         MISSING   no alert on new rows: false confidence
  Duplicate delivery skipped          shown     test replays event 4821 -> "Already processed"

Inbound: POST /api/webhooks/repo-events (provider does not auto-retry)
  Scheduled redelivery of failures    MISSING
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers and threat-model come with it.

Call it as `/hardening:webhook-reliability`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers and threat-model come with it. In Codex, type `$` and the skill name (`$hardening:webhook-reliability`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill webhook-reliability
```

Skills arrive without a pack prefix: `/webhook-reliability` in most agents and `@webhook-reliability` in Windsurf. opencode shows `/webhook-reliability` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/webhook-reliability .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `webhook-reliability` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/hardening/skills
   zip -r webhook-reliability.zip webhook-reliability
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `webhook-reliability.zip`.

**Limit:** Design is text; auditing an existing handler needs the code pasted in.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole hardening pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Design is text; auditing an existing handler needs the code pasted in.

</details>
<!-- skill-readme:end -->
