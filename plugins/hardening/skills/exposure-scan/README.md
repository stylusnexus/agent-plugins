<!-- skill-readme:begin -->
# exposure-scan

Scan installed packages against bumblebee threat-intelligence exposure catalogs to detect known-compromised dependency releases from supply-chain campaigns. Use when checking for compromised packages, running a supply-chain or dependency security scan, auditing the machine after a reported npm/PyPI/Go/gem/extension compromise, or refreshing threat-intel catalogs.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** A compromised package is reported and you need to know if your machine has it. Refresh the catalogs first; a campaign not yet listed won't match.

**Try:** `Refresh the threat catalogs, then run a quick exposure scan.`

**Skip it when:** You want a CVE scan of your project dependencies. This only matches named campaigns.

## What it looks like

*Sketch built from the fields the SKILL.md lists, invented data. Exact script formatting may differ.*

```text
$ scan.sh refresh      # pull current catalogs first
$ scan.sh quick
🚨 1 EXPOSURE FINDING(S)
  severity     critical
  package      npm:example-color-utils@4.2.1
  campaign     example-campaign-2026
  evidence     release published from a hijacked maintainer account
  source_file  <global npm root>/example-color-utils/package.json
exit 2  -> remove or downgrade, rotate credentials it could reach, read the campaign report

Exit 0 CLEAN (named campaigns only, not a CVE scan) · 1 scan did not finish, never clean
     2 findings · 3 catalog files disagree on schema version
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it.

Call it as `/hardening:exposure-scan`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:exposure-scan`), or run `/skills` to pick it.

**Note:** Network steps need an approval; installing the scanner needs network.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill exposure-scan
```

Skills arrive without a pack prefix: `/exposure-scan` in most agents and `@exposure-scan` in Windsurf. opencode shows `/exposure-scan` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/exposure-scan .agents/skills/
```

</details>

<details>
<summary>Claude app: not supported</summary>

**Why:** Runs in a remote sandbox without your local repo, git remotes or credentials.

</details>

<details>
<summary>ChatGPT: not supported</summary>

**Why:** No access to your local repo or git and gh credentials by default.

</details>
<!-- skill-readme:end -->
