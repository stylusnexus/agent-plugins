<!-- skill-readme:begin -->
# threat-model

Use when a new feature, route, integration, or data flow is about to be designed or built and nobody has written down who could abuse it and how. Triggers: a spec or plan with no security section, a PR that adds a trust boundary (new input, new external service, new privileged action), a launch review that asks 'what could go wrong', or a request to 'threat model' something.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Builds the threat table from spec text; no search of the code for boundaries and no write-back to the repo.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** A spec adds public share links and has no security section.

**Try:** `Threat model the public invoice share links before we build them.`

**Skip it when:** The code is already written and you want a line-by-line review, or you need one control checked in depth.

## What it looks like

*Example output, invented data.*

```text
Scope: public share links for invoices. Assets: invoice data, customer emails,
the email-sending bill. Actors: anonymous visitor, signed-in user, other tenant.

| # | Boundary          | Actor        | Threat (STRIDE)          | Lk   | Im   | Control                   | Verified by         | Status      |
| 1 | B1 browser -> API | anonymous    | I: guesses share link ID | med  | high | 128-bit random token      | auth-hardening      | OPEN        |
| 2 | B1 browser -> API | other tenant | E: reads other team data | med  | high | undecided: login needed?  | auth-hardening      | OPEN-BLOCKS |
| 3 | B2 API -> email   | signed-in    | D: resend loop, big bill | high | med  | 5 per hour per sender     | rate-limit-audit    | OPEN        |
| 4 | B3 payment hook   | anyone       | S: forged "paid" event   | low  | high | signature + idempotency   | webhook-reliability | MITIGATED   |

B1: S none · T none · R none · I #1 · D none · E #2
B2: S none · T none · R none · I none · D #3 · E none

Gate list: auth-hardening (B1, blocking) -> rate-limit-audit (B2) -> webhook-reliability (B3)
Record: 2026-01-12, example-agent (model name), B1-B3, accepted risks: none
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers and webhook-reliability come with it.

Call it as `/hardening:threat-model`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:threat-model`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill threat-model
```

Skills arrive without a pack prefix: `/threat-model` in most agents and `@threat-model` in Windsurf. opencode shows `/threat-model` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/threat-model .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `threat-model` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/hardening/skills
   zip -r threat-model.zip threat-model
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `threat-model.zip`.

**Limit:** Builds the threat table from spec text; no search of the code for boundaries and no write-back to the repo.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole hardening pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Builds the threat table from spec text; no search of the code for boundaries and no write-back to the repo.

</details>
<!-- skill-readme:end -->
