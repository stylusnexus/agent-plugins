<!-- skill-readme:begin -->
# api-design

REST conventions for Next.js App Router route handlers — resource naming, versioning, cursor pagination, one error envelope, Zod request/response validation, status-code rules, OpenAPI generated from Zod, and response scrubbing (no secrets, hashes, or other users' data). Use when asked to "design an API route", "add a new endpoint", "review this route handler", "fix our error responses", or "generate API docs".

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Designs and reviews pasted route handlers; cannot detect the repo's own conventions.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** You are adding or reviewing a Next.js route handler and want one consistent error and validation style.

**Try:** `Review the new /api/projects route handler against our API conventions`

**Skip it when:** The API uses GraphQL or tRPC.

## What it looks like

Example exchange, invented data.

```text
> /api-design review app/api/projects

- app/api/projects/route.ts:22   findMany() with no select returns the owner's
  passwordHash. Blocking: choose fields with select at the query.
- app/api/projects/route.ts:9    limit comes from the query string with no cap.
  Cap it at 100 on the server.
- app/api/projects/[projectId]/route.ts:31   returns 403 for another user's
  private project, which confirms it exists. Return 404.
- app/api/projects/[projectId]/route.ts:47   returns 200 with { "error": ... }.
  Use the error envelope with code NOT_FOUND and status 404.
Holds: plural nested paths, no version prefix, Zod input validation,
  OpenAPI regenerated in this PR.
Verdict: FAIL (a sensitive field is returned).
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:api-design`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **ship-pipeline**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
```

This installs the whole ship-pipeline pack, so analytics-instrumentation, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:api-design`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill api-design
```

Skills arrive without a pack prefix: `/api-design` in most agents and `@api-design` in Windsurf. opencode shows `/api-design` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/api-design .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `api-design` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/ship-pipeline/skills
   zip -r api-design.zip api-design
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `api-design.zip`.

**Limit:** Designs and reviews pasted route handlers; cannot detect the repo's own conventions.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole ship-pipeline pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Designs and reviews pasted route handlers; cannot detect the repo's own conventions.

</details>
<!-- skill-readme:end -->
