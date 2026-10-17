<!-- skill-readme:begin -->
# npm-publish

Release an npm package end to end — preflight checks, semver bump, changelog entry, git push, then publish. Rotates an expired npm token automatically through the browser rather than prompting for a one-time code. Use for npm or bun publishing and version bumps; not for GitHub releases or unrelated senses of 'release'.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Publishing needs a local repo, npm and Chrome. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** You are ready to release an npm package: bump, changelog, push and publish.

**Try:** `Publish acme-sdk as a patch release.`

**Skip it when:** You only want a bump recommendation, or you need a GitHub release. Use `version-check` for the first.

## What it looks like

The scripts print a status code; the agent reads it and tells you what happens next.

| Script prints | What the agent does |
|---|---|
| `PUBLISH_SUCCESS` | Runs the registry check in the background |
| `AUTH_FAILED` | Starts the token setup, in two phases |
| `FORM_READY:<username>` | Tells you to click **Generate token** in Chrome |
| `NOT_LOGGED_IN` | Asks you to sign in to npmjs.com in Chrome, then retries |
| `FORM_NOT_FOUND` | Says it could not find the token form |
| `TOKEN_SAVED` | Retries the publish |
| `CAPTURE_TIMEOUT` | Asks you to copy the token so it can write it to `~/.npmrc` |

It never asks you for a one-time code.

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, observability-setup, pr-wait, the-waiting and version-check come with it.

Call it as `/release-ops:npm-publish`, or let it start on its own when your request matches.

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

This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, observability-setup, pr-wait, the-waiting and version-check come with it. In Codex, type `$` and the skill name (`$release-ops:npm-publish`), or run `/skills` to pick it.

**Note:** Network steps need an approval; token rotation drives local Chrome and uses macOS pbcopy.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill npm-publish
```

Skills arrive without a pack prefix: `/npm-publish` in most agents and `@npm-publish` in Windsurf. opencode shows `/npm-publish` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Token rotation needs agent-browser, Chrome and macOS pbcopy.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/npm-publish .agents/skills/
```

**Note:** Token rotation needs agent-browser, Chrome and macOS pbcopy.

</details>

<details>
<summary>Claude app: not supported</summary>

**Why:** Publishing needs a local repo, npm and Chrome.

</details>

<details>
<summary>ChatGPT: not supported</summary>

**Why:** No access to your local repo or git and gh credentials by default.

</details>
<!-- skill-readme:end -->

## npm-publish

Publish npm packages from your coding agent with automatic token rotation. When your npm token expires, the skill uses agent-browser to create a new granular access token through Chrome — you click one button, the token is captured via clipboard, and publishing resumes automatically.

## Flow

```
preflight.sh → Agent writes CHANGELOG → release.sh → publish.sh → verify.sh
   (script)        (agent)                (script)     (script)     (background)
                                                          │
                                                     AUTH_FAILED?
                                                          │
                                                   setup-token.sh fill
                                                   (agent-browser fills form)
                                                          │
                                                   User clicks Generate
                                                          │
                                                   setup-token.sh capture
                                                   (clipboard → ~/.npmrc)
                                                          │
                                                   publish.sh retry
```

## Scripts

### preflight.sh

Checks the npm registry, handles version logic deterministically, builds, and outputs the commit log.

```bash
bash scripts/preflight.sh          # default: patch bump
bash scripts/preflight.sh minor    # minor bump
bash scripts/preflight.sh major    # major bump
```

Version logic:
- **local == npm** → bumps version (patch/minor/major)
- **local == npm+1** → no bump needed, ready to publish
- **local > npm+1** → gap detected (abandoned bumps), resets to npm+1
- Also updates `.claude-plugin/plugin.json` if present

### release.sh

Stages all tracked changes (`git add -u`), commits, pushes. Does NOT publish — returns `RELEASE_DONE` so the agent can call publish.sh separately and handle auth recovery.

Uses `git add -u` to catch all tracked file modifications (biome.json, source files, config changes) without the risk of `git add -A` pulling in untracked files like `.env` or credentials. Also explicitly adds `CHANGELOG.md` and `.claude-plugin/plugin.json` since those may be newly created. Reports staged files in output so the agent can confirm what's included.

```bash
bash scripts/release.sh                  # standard
bash scripts/release.sh --access public  # scoped @org/pkg
```

### publish.sh

Attempts `echo "" | bun publish`. Returns status codes:
- `PUBLISH_SUCCESS` — done
- `AUTH_FAILED` — token expired/missing, agent should run setup-token.sh

The piped ENTER auto-opens the OTP checkbox page when the token is valid but OTP is required.

### setup-token.sh

Two-phase token creation via agent-browser + Chrome:

**Phase 1 — `setup-token.sh fill`:**
1. Navigates to npmjs.com, detects username from DOM
2. Opens granular token creation page
3. Fills form: name "cli-publish", All packages, Read+write on packages and organizations, 7-day expiry
4. Returns `FORM_READY:<username>` — agent tells user to click Generate

**Phase 2 — `setup-token.sh capture`:**
1. Polls page for Copy button (token appears after user clicks Generate)
2. Clicks Copy → reads from clipboard via `pbpaste`
3. Writes `//registry.npmjs.org/:_authToken=<token>` to `~/.npmrc`
4. Clears clipboard immediately
5. Returns `TOKEN_SAVED`

**Security:** The token never appears in terminal output, shell history, or agent context. It flows: npm page → Copy button → system clipboard → `pbpaste` into file → clipboard cleared.

**Why granular tokens:** npm's CLI cannot create granular or automation tokens (`npm token create` only makes legacy publish tokens that require OTP every time). Granular tokens must be created through the website. agent-browser automates the form filling; the user's only interaction is clicking Generate.

### verify.sh

Confirms registry propagation with exponential backoff. Run as a background task.

```bash
bash scripts/verify.sh @scope/package 1.2.3
```

Backoff: 5s → 10s → 20s → 40s → 60s. Exits 0 when the version appears on npm.

## Authentication Architecture

The skill uses **granular access tokens** (7-day expiry) stored in `~/.npmrc`. This replaces the old approach of piping ENTER to `bun publish` for browser auth, which broke in bun 1.3.8 when tokens were fully expired (404 instead of auth prompt).

Token lifecycle:
1. **Token valid** → `bun publish` succeeds, may show OTP checkbox (piped ENTER opens it)
2. **Token expired** → `bun publish` returns 404 → `setup-token.sh` creates new token via Chrome → retry succeeds
3. **No token** → same as expired

The 7-day expiry keeps tokens short-lived. Rotation is automated, so short expiry adds security without friction.

## Agent Orchestration

Scripts output status codes. The agent interprets them and communicates with the user between phases. This matters because bash command output is collapsed in Claude Code — the user won't see `echo` statements from scripts. All user-facing messages must come from the agent directly.

Key status codes:
| Script | Code | Agent Action |
|--------|------|-------------|
| publish.sh | `PUBLISH_SUCCESS` | Tell user "Published", run verify.sh |
| publish.sh | `AUTH_FAILED` | Run setup-token.sh fill |
| setup-token.sh fill | `FORM_READY:<user>` | Tell user "Click Generate token in Chrome" |
| setup-token.sh fill | `NOT_LOGGED_IN` | Tell user "Sign in to npmjs.com in Chrome" |
| setup-token.sh capture | `TOKEN_SAVED` | Retry publish.sh |
| setup-token.sh capture | `CAPTURE_TIMEOUT` | Tell user to copy token manually |
| release.sh | `RELEASE_DONE:pkg:ver:flags` | Run publish.sh with flags |

## Form Interaction Details

npm's token creation page uses custom React components, not standard HTML form elements:

- **Permission dropdowns** (Packages, Organizations): Clickable divs that open `menuitemcheckbox` option lists. Pattern: click trigger → snapshot with `-C` flag → click menuitemcheckbox option.
- **Expiration dropdown**: Same pattern as permissions.
- **All packages radio**: Standard radio but `agent-browser click` doesn't reliably select it. Use `eval 'document.getElementById("packagesAll").click()'` instead.
- **Organization checkboxes**: Standard checkboxes, use `agent-browser check @ref` for each.

## Files

```
npm-publish/
├── SKILL.md              # Agent instructions (what the model reads)
├── README.md             # This file (human + developer docs)
└── scripts/
    ├── preflight.sh      # Check + bump + build + commit log
    ├── release.sh        # Commit + push (returns RELEASE_DONE)
    ├── publish.sh        # Try publish (returns PUBLISH_SUCCESS or AUTH_FAILED)
    ├── setup-token.sh    # Two-phase: fill form / capture token
    └── verify.sh         # Background: exponential backoff registry check
```

## Prerequisites

- **agent-browser** >= 0.20.0 (`bun install -g agent-browser`)
- **Chrome** with remote debugging enabled
- Logged into npmjs.com in Chrome (setup-token.sh will open the login page if not)
