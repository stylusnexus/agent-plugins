<!-- skill-readme:begin -->
# legal-docs

Draft or review the customer-facing legal documents of a small SaaS - Terms of Service, Privacy Policy, refund policy, and acceptable use policy - in plain English, with placeholders instead of invented facts, a check that every claim matches what the product actually does, and a not-legal-advice notice on every draft. Use when asked to "write terms", "draft a privacy policy", "update our ToS", "write a refund policy", or before launching a product or feature that changes what data is collected or how billing works.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Drafts from pasted facts; cannot check each claim against your code and config.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** You launch a small SaaS and need a first draft of the terms or privacy policy.

**Try:** `Draft a privacy policy for this app from what the code actually collects.`

**Skip it when:** You need legal advice or a final document. A lawyer must review every draft.

## What it looks like

*Example output, invented data.*

```text
> Draft for review. This is not legal advice and has not been reviewed by a lawyer.

## What we collect
- Your name and email, when you sign up.
- The titles and times of events you add.
- Your IP address, kept in server logs for 30 days.

## Who we share it with
- Payments, analytics, email, error tracking, hosting (each linked to its DPA)

## Your choices and rights
To get a copy of your data, email [PRIVACY_CONTACT_EMAIL].

Open questions for the lawyer: EU signups -> legal basis and Article 13 contents;
CCPA thresholds (owner to check). Gap: notes promise "download all your data",
no export flow exists, so the draft says "contact us".
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it.

Call it as `/hardening:legal-docs`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:legal-docs`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill legal-docs
```

Skills arrive without a pack prefix: `/legal-docs` in most agents and `@legal-docs` in Windsurf. opencode shows `/legal-docs` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/legal-docs .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `legal-docs` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/hardening/skills
   zip -r legal-docs.zip legal-docs
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `legal-docs.zip`.

**Limit:** Drafts from pasted facts; cannot check each claim against your code and config.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole hardening pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Drafts from pasted facts; cannot check each claim against your code and config.

</details>
<!-- skill-readme:end -->
