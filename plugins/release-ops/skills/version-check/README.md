<!-- skill-readme:begin -->
# version-check

Analyze changes since the most recent version tag and recommend a semantic-version bump. Use before publishing to npm or when deciding whether a release should be a major, minor, or patch bump.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Can judge a pasted diff or commit list; cannot read git history itself.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** You have commits since the last tag and must pick major, minor or patch.

**Try:** `Should the next release of acme-sdk be a major, minor or patch bump?`

**Skip it when:** The release is already decided and you only want to publish. Use `npm-publish`.

## What it looks like

Example output, invented data.

```text
Version Check Report
====================
Current version: 2.4.1
Last tag: v2.4.1
Commits since tag: 7

Recommendation: MINOR bump -> 2.5.0
Reason: new backward-compatible features, no breaking changes

Evidence:
  - src/index.ts: added export createBatchClient (an addition, not a removal)
  - src/types/index.ts: new optional field timeoutMs? on ClientOptions
  - no commit message contains BREAKING CHANGE or feat!:

Changed files:
  src/index.ts (modified)
  src/batch.ts (added)
  src/types/index.ts (modified)

Bump to 2.5.0? Nothing changes until you confirm.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait and the-waiting come with it.

Call it as `/release-ops:version-check`, or let it start on its own when your request matches.

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

This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait and the-waiting come with it. In Codex, type `$` and the skill name (`$release-ops:version-check`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill version-check
```

Skills arrive without a pack prefix: `/version-check` in most agents and `@version-check` in Windsurf. opencode shows `/version-check` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/version-check .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `version-check` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/release-ops/skills
   zip -r version-check.zip version-check
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `version-check.zip`.

**Limit:** Can judge a pasted diff or commit list; cannot read git history itself.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole release-ops pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Can judge a pasted diff or commit list; cannot read git history itself.

</details>
<!-- skill-readme:end -->
