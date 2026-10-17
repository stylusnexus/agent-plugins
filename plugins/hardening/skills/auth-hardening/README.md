<!-- skill-readme:begin -->
# auth-hardening

NextAuth v5 security audit and hardening checklist — session/cookie config, CSRF, OAuth scopes, per-route role checks, password-reset/OTP rate limits, secret rotation, session invalidation on privilege change. Use when adding auth to a new product, auditing an existing NextAuth v5 app, or reviewing any PR that touches session/role/permission code.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Design guidance works; the audit half searches your routes and needs the repo.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** You are adding sign-in to a NextAuth v5 app, or a PR changes role or session code.

**Try:** `Audit auth on every route in this app and tell me which ones skip the ownership check.`

**Skip it when:** The app does not use NextAuth v5, or the change does not touch sign-in, sessions, roles or permissions.

## What it looks like

*Example output, invented data.*

```text
| Route                              | Session check | Ownership/role check | Rate limit |
| GET    /api/projects/[id]          | Y             | Y                    | n/a        |
| DELETE /api/projects/[id]          | Y             | N   <- high priority | n/a        |
| server action updateSettings       | Y             | Y                    | n/a        |
| POST   /api/auth/reset-password    | n/a           | n/a                  | N          |

High: DELETE /api/projects/[id] checks that a session exists, never that the
caller owns the project. Fix: load the project, compare ownerId, return 404
(not 403) so the caller cannot learn the ID is real.
Reset password: limit by IP and by target email, same response either way.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it.

Call it as `/hardening:auth-hardening`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:auth-hardening`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill auth-hardening
```

Skills arrive without a pack prefix: `/auth-hardening` in most agents and `@auth-hardening` in Windsurf. opencode shows `/auth-hardening` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/auth-hardening .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `auth-hardening` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/hardening/skills
   zip -r auth-hardening.zip auth-hardening
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `auth-hardening.zip`.

**Limit:** Design guidance works; the audit half searches your routes and needs the repo.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole hardening pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Design guidance works; the audit half searches your routes and needs the repo.

</details>
<!-- skill-readme:end -->
