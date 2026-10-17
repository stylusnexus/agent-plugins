<!-- skill-readme:begin -->
# secrets-leak-audit

Use when checking whether API keys, tokens, passwords, or personal data can escape through git history, the client bundle, log lines, error reports, or API response payloads. Triggers: pre-launch review, a key found in a commit, a .env file that may have been tracked, a new public-prefixed environment variable (NEXT_PUBLIC_, VITE_, EXPO_PUBLIC_), a new logger or error-reporting integration, or a 'what does the client actually receive' question.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** An API key shows up in a commit, or you add a new public-prefixed env variable.

**Try:** `Check git history, the client bundle, logs and API responses for leaked secrets.`

**Skip it when:** You only want to know whether a dependency is compromised. Use exposure-scan.

## What it looks like

*Example output, invented data.*

```text
| Door           | Scanned                               | Hits | Action                      | Status |
| Git history    | all revisions, two scanners           | 1    | rotate at provider, then    | LEAK   |
|                |                                       |      | rewrite history             |        |
| Client bundle  | production build output               | 1    | MAPS public key: justified  | CLEAN  |
| Logs, errors   | log calls; staging error event read   | 2    | log named fields only       | LEAK   |
| API responses  | 3 heaviest endpoints captured         | 1    | /api/team returns password  | LEAK   |
|                |                                       |      | hash: add a field allowlist |        |

First required action: rotate the model API key found in a 2025 commit.
Noticed: credentialed URL in an agent config file -> agent-tooling-review
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, security-headers, threat-model and webhook-reliability come with it.

Call it as `/hardening:secrets-leak-audit`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, security-headers, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:secrets-leak-audit`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill secrets-leak-audit
```

Skills arrive without a pack prefix: `/secrets-leak-audit` in most agents and `@secrets-leak-audit` in Windsurf. opencode shows `/secrets-leak-audit` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/secrets-leak-audit .agents/skills/
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
