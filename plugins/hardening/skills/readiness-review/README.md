<!-- skill-readme:begin -->
# readiness-review

Read-only launch-readiness review of any repo and its live product, written as one report. Answers two questions with evidence. Is the code healthy (security, architecture, live database structure, unfinished features)? Can a user do the core jobs, is it hard to use, does it look finished, would they pay? Runs deterministic scanners, a reviewer pass over a secret-free copy of the repo, and a look-only browser walk as a non-admin test account, then ends with a findings list the human files. Use on /readiness-review, "is this ready to launch", "is the code healthy", "would a user pay for this", or a recurring pre-launch check. Never files issues, comments, pushes, or writes to a database.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** You plan a launch and want one report on code health and the user experience.

**Try:** `/readiness-review` (with a `.readiness-review.yaml` that names the staging URL and a non-admin test account)

**Skip it when:** You need a fix applied. It writes only a local report and never changes code, files issues or writes to the database.

## What it looks like

*Example output, invented data.*

```text
# Readiness review: example-invoices (2026-01-12)
## Verdict
not ready -- code: 2 high findings in export and team access; product: core job
"create and send" could not be exercised in look-only mode.
## Launch blockers
3 of 5 still open (#41, #52, #60)
## Product walk
Mode: look-only
| Job             | Stage | Can do        | Friction (where)              | Looks finished | Top issue      |
| Find an invoice | core  | yes           | low                           | finished       | none           |
| Create and send | core  | not exercised | medium (Send below the fold)  | rough          | hidden on phone |
### Would they pay
not yet: the pricing page lists a Team plan the code does not have
## Not checked
Dependabot: NOT VERIFIED (HTTP 403)
## Findings to file
[high] fix(export): route returns other teams' rows -- new
[medium] fix(pricing): Team plan promised but missing -- looks like existing #117
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it.

Call it as `/hardening:readiness-review`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:readiness-review`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill readiness-review
```

Skills arrive without a pack prefix: `/readiness-review` in most agents and `@readiness-review` in Windsurf. opencode shows `/readiness-review` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/readiness-review .agents/skills/
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
