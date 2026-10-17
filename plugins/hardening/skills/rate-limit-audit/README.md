<!-- skill-readme:begin -->
# rate-limit-audit

Pre-launch gate that inventories every endpoint calling a paid API (LLM, email, SMS) and every auth endpoint, verifies a rate limiter exists, and actually tests it with scripted burst requests to confirm 429s fire. Use before launching a new product/feature, after adding an LLM-calling or auth route, or when asked to check rate limiting.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** You add an LLM, email or SMS route, or a login route, before launch.

**Try:** `Find every route that calls a paid API or handles login, and burst-test each limiter.`

**Skip it when:** The route cannot be reached by users and calls no paid API.

## What it looks like

*Example output, invented data.*

```text
| Route or action          | Class | Limiter                       | Tested |
| POST /api/chat           | LLM   | found: 20 / 10 min, user id   | yes    |
| POST /api/auth/login     | auth  | found: 5 / 15 min, IP + email | yes    |
| action sendInvite        | email | none   <- blocks launch       | no     |

Burst test, POST /api/chat (limit 20 / 10 min)
  sequential:      20 200
                    5 429
  concurrent:      23 200
                    2 429
  rerun inside one window: 23 x 200 again -> check and increment are not
  atomic; limiter broken under concurrency. Fix before marking passed.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it.

Call it as `/hardening:rate-limit-audit`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:rate-limit-audit`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill rate-limit-audit
```

Skills arrive without a pack prefix: `/rate-limit-audit` in most agents and `@rate-limit-audit` in Windsurf. opencode shows `/rate-limit-audit` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/rate-limit-audit .agents/skills/
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
