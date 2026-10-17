<!-- skill-readme:begin -->
# security-headers

Use when checking or setting HTTP security headers on a deployed site or API: Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy. Triggers: pre-launch review, a new domain or reverse proxy, a scanner report (Mozilla Observatory, securityheaders.com) with a bad grade, an XSS or clickjacking finding, or an auth response that browsers are caching.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Grades pasted header output or uploaded config; cannot capture the deployed response itself.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** A scanner gives your site a bad grade, or you move to a new domain or proxy.

**Try:** `Check the security headers on staging and tell me who sets each one.`

**Skip it when:** You need a launch pass but have no deployed URL. Without one it can only read config and flag what is missing.

## What it looks like

*Example output, invented data.*

```text
Captured on staging (deployed): page /pricing, API /api/me, asset /static/app.js

| Header                    | Current value                       | Owner         | Status      |
| Strict-Transport-Security | max-age=31536000; includeSubDomains | framework cfg | PASS        |
| Content-Security-Policy   | Report-Only, reports not yet read   | middleware    | CONDITIONAL |
| X-Frame-Options           | DENY                                | framework cfg | PASS        |
| X-Content-Type-Options    | missing on /static/app.js           | CDN and app   | FAIL        |
| Referrer-Policy           | strict-origin-when-cross-origin     | framework cfg | PASS        |
| Permissions-Policy        | missing                             | none          | FAIL        |
| Cache-Control on /api/me  | public, max-age=60                  | route handler | FAIL        |
| X-Powered-By              | bare framework name                 | framework     | FAIL (low)  |

Verdict: not ready. /api/me is cacheable by a shared cache (session-leak path).
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, threat-model and webhook-reliability come with it.

Call it as `/hardening:security-headers`, or let it start on its own when your request matches.

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

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, llm-app-security, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:security-headers`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill security-headers
```

Skills arrive without a pack prefix: `/security-headers` in most agents and `@security-headers` in Windsurf. opencode shows `/security-headers` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/security-headers .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `security-headers` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/hardening/skills
   zip -r security-headers.zip security-headers
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `security-headers.zip`.

**Limit:** Grades pasted header output or uploaded config; cannot capture the deployed response itself.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole hardening pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Grades pasted header output or uploaded config; cannot capture the deployed response itself.

</details>
<!-- skill-readme:end -->
