<!-- skill-readme:begin -->
# privacy-audit

Data inventory and privacy audit for a product — enumerate exactly what user data is collected and where it lands (Neon/Supabase tables, logs, PostHog, Stripe, email provider, Better Stack/Sentry), check alignment with the privacy policy, verify GDPR export/delete paths exist, and grep for PII leaking into logs or API responses. Use when asked to "audit privacy," "check what data we collect," before a launch, or after adding a new data-collecting feature (signup field, analytics event, webhook).

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Works on a repo archive you upload; live logs, API responses and third-party deletion cannot be checked.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** You add a signup field or an analytics event and need to know where the data goes.

**Try:** `Audit what user data we collect, where it is stored, and whether export and delete work.`

**Skip it when:** You need the policy text written. Use legal-docs, which builds on this audit's data inventory.

## What it looks like

*Example output, invented data.*

```text
| Data         | Source            | Storage                 | Retention       | Third parties   |
| email        | signup form       | users.email             | until deletion  | payments, email |
| IP address   | request logs      | log host                | 30 days         | log host        |
| BYOK API key | settings form     | users.api_key_encrypted | until deletion  | none            |
| page events  | analytics capture | analytics person record | provider default| analytics       |

Leak (top finding): lib/auth.ts:57 logs the whole user object (email, password hash)
Policy gaps: session recordings collected but not disclosed
GDPR paths: export MISSING · delete PARTIAL (payments customer survives deletion)
Fix order: 1 log leak  2 policy gap  3 delete cascade  4 export route
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it.

Call it as `/hardening:privacy-audit`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:privacy-audit`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill privacy-audit
```

Skills arrive without a pack prefix: `/privacy-audit` in most agents and `@privacy-audit` in Windsurf. opencode shows `/privacy-audit` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/privacy-audit .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `privacy-audit` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/hardening/skills
   zip -r privacy-audit.zip privacy-audit
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `privacy-audit.zip`.

**Limit:** Works on a repo archive you upload; live logs, API responses and third-party deletion cannot be checked.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole hardening pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Works on a repo archive you upload; live logs, API responses and third-party deletion cannot be checked.

</details>
<!-- skill-readme:end -->
