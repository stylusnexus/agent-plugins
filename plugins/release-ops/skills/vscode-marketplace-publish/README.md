<!-- skill-readme:begin -->
# vscode-marketplace-publish

Publish a VS Code extension update to the Visual Studio Marketplace, and to Open VSX if the project uses it. Runs preflight checks, picks the version, packages and inspects the .vsix, waits for the user's yes, publishes with vsce, then confirms the new version is live. Use for VS Code extension releases and version bumps; not for npm packages (use npm-publish) or GitHub releases.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Publishing needs a local extension repo, vsce and your publisher token. ChatGPT: No access to your local repo or git credentials by default.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** You are releasing a new version of a VS Code extension.

**Try:** `Publish the next patch of my VS Code extension.`

**Skip it when:** You are publishing an npm package. Use `npm-publish`.

## What it looks like

Example output, invented data.

```text
Preflight
  acme.acme-lint  live: 1.4.2  local: 1.4.2  -> next: 1.4.3 (patch)
  build, lint, tests: pass
  working tree: clean

Package
  acme-lint-1.4.3.vsix, 212 KB, 38 files
  flagged: src/**/*.map (12 source maps) -> added to .vscodeignore, repackaged: 26 files

Ready to publish acme.acme-lint@1.4.3 to the Visual Studio Marketplace.
This also edits package.json and creates a git commit and tag. Go ahead?
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait, the-waiting and version-check come with it.

Call it as `/release-ops:vscode-marketplace-publish`, or let it start on its own when your request matches.

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

This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait, the-waiting and version-check come with it. In Codex, type `$` and the skill name (`$release-ops:vscode-marketplace-publish`), or run `/skills` to pick it.

**Note:** Network steps need an approval.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill vscode-marketplace-publish
```

Skills arrive without a pack prefix: `/vscode-marketplace-publish` in most agents and `@vscode-marketplace-publish` in Windsurf. opencode shows `/vscode-marketplace-publish` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/vscode-marketplace-publish .agents/skills/
```

</details>

<details>
<summary>Claude app: not supported</summary>

**Why:** Publishing needs a local extension repo, vsce and your publisher token.

</details>

<details>
<summary>ChatGPT: not supported</summary>

**Why:** No access to your local repo or git credentials by default.

</details>
<!-- skill-readme:end -->
