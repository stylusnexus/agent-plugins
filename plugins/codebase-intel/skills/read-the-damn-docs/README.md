<!-- skill-readme:begin -->
# read-the-damn-docs

Use when implementing, integrating, upgrading, debugging, or answering anything involving third-party APIs, libraries, frameworks, CLIs, cloud services, model/provider SDKs, fast-moving product behavior, user requests for latest/current/official behavior, unfamiliar repo docs/specs, errors that may indicate API drift, or high-stakes auth, security, billing, data, migration, deployment, compliance, or privacy behavior. Forces Codex to web-search for current official docs and read primary docs before assuming from memory.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Web search works; the repo-docs step is skipped and `npm view` version checks cannot run. Other agents: Web search is the core step; Gemini CLI/Antigravity CLI, Cursor and opencode (with a search provider) have it, Copilot, Windsurf and Cline are not verified.

Part of the [codebase-intel](../../README.md) pack.

## When and how to use it

**Use it when:** You add or upgrade a library and must not guess its current API.

**Try:** `Add payment-provider webhooks to this app. Read the current official docs first.`

**Skip it when:** The task uses only your own code, has no outside API, and no repo doc or spec defines the behaviour.

## What it looks like

*Example exchange, invented data.*

```text
You:   Wire up payment-provider webhooks in our Next.js app.

Agent: Checking the docs before writing code.
       - Installed: next 15.x; provider SDK 17.x (from package.json)
       - Read: the provider's webhook signature guide, its retry policy page,
         and Next.js route handler docs for reading the raw request body
       - From the docs: verify against the raw body, not parsed JSON; the
         provider retries failed deliveries, so dedupe on the event id
       Implementing that now, then running the typecheck and a signed test event.
       Docs consulted are listed at the end of my answer.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install codebase-intel@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install codebase-intel@stylus-nexus` do the same. This installs the whole codebase-intel pack, so codebase-architecture-scanner, codebase-health and grill-with-docs come with it.

Call it as `/codebase-intel:read-the-damn-docs`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **codebase-intel**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add codebase-intel@stylus-nexus
```

This installs the whole codebase-intel pack, so codebase-architecture-scanner, codebase-health and grill-with-docs come with it. In Codex, type `$` and the skill name (`$codebase-intel:read-the-damn-docs`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI (partial)</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill read-the-damn-docs
```

Skills arrive without a pack prefix: `/read-the-damn-docs` in most agents and `@read-the-damn-docs` in Windsurf. opencode shows `/read-the-damn-docs` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Limit:** Web search is the core step; Gemini CLI/Antigravity CLI, Cursor and opencode (with a search provider) have it, Copilot, Windsurf and Cline are not verified.

</details>

<details>
<summary>Other agents, by folder (partial)</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/codebase-intel/skills/read-the-damn-docs .agents/skills/
```

**Limit:** Web search is the core step; Gemini CLI/Antigravity CLI, Cursor and opencode (with a search provider) have it, Copilot, Windsurf and Cline are not verified.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `read-the-damn-docs` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/codebase-intel/skills
   zip -r read-the-damn-docs.zip read-the-damn-docs
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `read-the-damn-docs.zip`.

**Limit:** Web search works; the repo-docs step is skipped and `npm view` version checks cannot run.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole codebase-intel pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Web search works; the repo-docs step is skipped and `npm view` version checks cannot run.

</details>
<!-- skill-readme:end -->

## /read-the-damn-docs

Make agents web-search for the docs before they guess.

`/read-the-damn-docs` is a docs-first discipline skill for implementation,
debugging, and technical answers that depend on versioned or external behavior.
It tells the agent when docs are mandatory, why web search is usually the right
way to find them, which sources count as authoritative, and how to report the
evidence it used.

## What It Does

- Forces a docs pass for third-party APIs, libraries, frameworks, CLIs, cloud
  services, model SDKs, and provider integrations.
- Directs the agent to web-search for current official docs unless the relevant
  docs are already local or supplied by the user.
- Requires current version checks before adding packages or writing install,
  import, config, or CLI commands.
- Prioritizes local repo docs, specs, schemas, generated types, and tests for
  internal contracts.
- Treats auth, security, billing, data, migrations, deploys, quotas, caching,
  and compliance as docs-required surfaces.
- Makes the agent name the docs or files it relied on when that evidence affects
  the implementation.

## When To Use It

Use it when an agent might otherwise rely on stale model memory. Most of the
time, that means it should search the web for official docs first: latest/current
behavior, package setup, SDK usage, platform limits, provider APIs, upgrade
guides, framework config, OAuth, payments, webhooks, migrations, CI/CD, browser
APIs, and repo-specific contracts.

Skip it for trivial typo fixes, formatting, self-contained local code, or cases
where nearby tests and types fully answer the question.

## Examples

These should trigger docs before code:

- Adding Tailwind, Next.js, React, Vite, Nitro, Drizzle, Prisma, or an AI SDK.
- Streaming model responses with OpenAI, Anthropic, Google, or a provider SDK.
- Wiring Stripe webhooks, OAuth, GitHub Actions, Slack apps, or Notion APIs.
- Debugging deprecations, unknown config fields, missing exports, or changed
  framework defaults.
- Choosing a model, package, cloud API, storage strategy, or migration path.
- Implementing a repo-specific system where local docs, schemas, or generated
  clients define the contract.
