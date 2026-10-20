<!-- skill-readme:begin -->
# customer-support-triage

Support inbox workflow for a small team - classify each request (bug, feature request, billing, how-to), attempt reproduction, assign severity, file a standard GitHub issue with no customer PII, check refund requests against the written policy, and draft the reply for a human to send. Use when triaging support email or tickets, or when asked to "handle this support request", "file this bug", or "draft a reply to this customer".

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Classifies and drafts from a pasted ticket; no reproduction, error-tracker search or issue filing.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** A customer email arrived and you need it classified, filed, and a reply drafted.

**Try:** `Triage this support email: the customer says the export button does nothing.`

**Skip it when:** The message is a sales lead, or you want the reply sent for you. It files the GitHub issue but only drafts the reply.

## What it looks like

Example output, invented data.

```text
P0: possible double charge on ticket #5120.

Category: Billing (also tagged bug)
Severity: P0 - two charges for the same billing period
Checked: the billing provider shows two successful charges 4 minutes apart
  on one subscription; the error tracker shows a webhook retry at that time
Issue: #461 filed from the template, "Reported by: ticket #5120", existing
  bug and priority labels. No name or email in the body.
Refund: inside the written policy (duplicate charge). Prepared, not issued:
  $12.00, the second charge, reason "duplicate". Waiting for a person to confirm.

DRAFT reply, for the support owner to send:
  Thanks for flagging this. You were charged twice for October, and that's
  on us. We've prepared a refund of $12.00 for the duplicate charge and will
  confirm once it's issued. We're also fixing the cause.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait, the-waiting, version-check and vscode-marketplace-publish come with it.

Call it as `/release-ops:customer-support-triage`, or let it start on its own when your request matches.

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

This installs the whole release-ops pack, so dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait, the-waiting, version-check and vscode-marketplace-publish come with it. In Codex, type `$` and the skill name (`$release-ops:customer-support-triage`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill customer-support-triage
```

Skills arrive without a pack prefix: `/customer-support-triage` in most agents and `@customer-support-triage` in Windsurf. opencode shows `/customer-support-triage` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/customer-support-triage .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `customer-support-triage` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/release-ops/skills
   zip -r customer-support-triage.zip customer-support-triage
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `customer-support-triage.zip`.

**Limit:** Classifies and drafts from a pasted ticket; no reproduction, error-tracker search or issue filing.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole release-ops pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Classifies and drafts from a pasted ticket; no reproduction, error-tracker search or issue filing.

</details>
<!-- skill-readme:end -->
