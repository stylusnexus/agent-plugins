<!-- skill-readme:begin -->
# dependency-upgrade

Safe batch dependency upgrades across a codebase — inventory outdated packages (npm outdated / uv lock --upgrade), group by risk (patch/minor/major), upgrade in waves with tsc/test/Playwright gates, read changelogs for majors, run `exposure-scan` for supply-chain checks, and land one PR per wave. Use when asked to "upgrade dependencies," "bump packages," "clear npm outdated," or on a periodic maintenance pass.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** `npm outdated` lists many packages and you want safe upgrades in small waves.

**Try:** `Upgrade our outdated dependencies in waves and open one PR per wave.`

**Skip it when:** You need one package bumped by hand, or you want to publish a release.

## What it looks like

Example output, invented data.

```text
Wave plan (from npm outdated --json)
package              current   target    risk    wave
@types/node          22.7.4    22.7.9    patch   1
zod                  3.23.6    3.23.8    patch   1
eslint-plugin-react  7.35.0    7.37.2    minor   2
next                 14.2.15   15.0.3    major   3 (with eslint-config-next)
eslint-config-next   14.2.15   15.0.3    major   3

Gates per wave: tsc --noEmit → tests → npx playwright test, then exposure-scan
Wave 1  PASS  all gates green, exposure-scan clean → chore(deps): bump patch dependencies
Wave 2  PASS  all gates green, exposure-scan clean → chore(deps): bump eslint plugins
Wave 3  FAIL  tsc red; green on the base commit, so the bump caused it. Not shipped.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so customer-support-triage, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait, the-waiting and version-check come with it.

Call it as `/release-ops:dependency-upgrade`, or let it start on its own when your request matches.

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

This installs the whole release-ops pack, so customer-support-triage, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait, the-waiting and version-check come with it. In Codex, type `$` and the skill name (`$release-ops:dependency-upgrade`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill dependency-upgrade
```

Skills arrive without a pack prefix: `/dependency-upgrade` in most agents and `@dependency-upgrade` in Windsurf. opencode shows `/dependency-upgrade` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/dependency-upgrade .agents/skills/
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
