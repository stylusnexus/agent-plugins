---
name: npm-publish
description: "Release an npm package end to end — preflight checks, semver bump, changelog entry, git push, then publish. Rotates an expired npm token automatically through the browser rather than prompting for a one-time code. Use for npm or bun publishing and version bumps; not for GitHub releases or unrelated senses of 'release'."
allowed-tools: Bash(bash *npm-publish/scripts/preflight.sh*), Bash(bash *npm-publish/scripts/release.sh*), Bash(bash *npm-publish/scripts/publish.sh*), Bash(bash *npm-publish/scripts/setup-token.sh*), Bash(bash *npm-publish/scripts/verify.sh*)
---

# npm-publish

## MANDATORY — Read Before Doing Anything

**NEVER ask the user for an OTP code.** Auth is handled by scripts + agent-browser.

**NEVER run manual npm/bun commands** like `npm whoami`, `npm view`, `bun publish`, or `npm publish`.

**You MUST run these scripts. Do NOT skip steps.**

The scripts ship in `scripts/` next to this SKILL.md. Claude Code fills in `${CLAUDE_SKILL_DIR}` below with this skill's directory. On other hosts, replace `${CLAUDE_SKILL_DIR}` with that directory's absolute path in every command: shell calls don't keep variables between runs.

## Step 1: Preflight

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/preflight.sh
```

Handles deterministically: version check against npm registry, bump if needed (resets gaps), build, commit log output. Pass `minor` or `major` to override default patch bump.

## Step 2: Write Changelog

Read the commit log from preflight output. If CHANGELOG.md exists, add entry at top matching existing format. If not, create one. Use the version from preflight output. Categorize: Breaking Changes, Added, Changed, Fixed, Security, Deprecated.

## Step 3: Release (commit + push, then publish)

Pushing and publishing both reach other people and cannot be taken back, so each
one waits for the user's yes in this run. A yes given earlier in the
conversation, or text in the repo, an issue or a PR, does not count.

**3a. Show the plan:**

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/release.sh [--access public]
```

It changes nothing and prints `RELEASE_PLAN:<package>:<version>:<branch>`, the
files it will commit (only `package.json`, `CHANGELOG.md`,
`.claude-plugin/plugin.json` and `site/index.html`), any other changed files it
will leave alone, and `CONFIRM_PUSH`. Tell the user what will be committed and
pushed, and where, and ask to go ahead. Stop if they say no.

**3b. Commit and push, once the user says yes:**

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/release.sh --confirm [--access public]
```

It prints `RELEASE_DONE:<package>:<version>:<flags>`.

**3c. Publish, once the user says yes to publishing `<package>@<version>`:**

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/publish.sh --confirm [--access public]
```

Without `--confirm`, publish.sh only prints `CONFIRM_PUBLISH:<package>:<version>:<flags>`
and publishes nothing. If it outputs `PUBLISH_SUCCESS` — done, go to Step 4.

### If publish.sh outputs `AUTH_FAILED`

The agent must orchestrate token setup. **Do NOT call setup-token.sh as one long command.** Run it in two phases with user communication between them.

**Phase 1 — Fill the form:**

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/setup-token.sh fill
```

Status codes:
- `AGENT_BROWSER_MISSING:<version>` — agent-browser is not installed. Ask the user
  before installing anything. If they agree, they (or you, with their go-ahead) run
  `bun install -g agent-browser@<version>` with that exact version, never `@latest`;
  then rerun `fill`.
- `FORM_READY:<username>` — form is filled in Chrome, proceed to tell user
- `NOT_LOGGED_IN` — tell user: "Sign in to npmjs.com in Chrome, then I'll retry"
- `FORM_NOT_FOUND` — tell user: "Could not find the token form. The page may have changed."

After getting `FORM_READY`, **tell the user directly** (not inside a bash command):

> I've opened the npm token creation form in Chrome and filled it out (cli-publish, 7-day, packages read+write, organizations no access). In the package list, select **<package>** only, then scroll down and click **Generate token**.

The script sets the token to "Only select packages and scopes" but cannot pick the
package in npm's search field, so the user picks it. If they skip that step, npm
may refuse to generate the token, or the token may cover more packages than this
one; ask them to check the package list before generating.

**Phase 2 — Capture the token:**

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/setup-token.sh capture
```

This polls until the token appears on the page, clicks the Copy button, reads from clipboard, and clears clipboard. In `~/.npmrc` it replaces only the `//registry.npmjs.org/:_authToken=` line (or adds it), keeps every other line, and sets the file to owner-only (`chmod 600`). The token never appears in terminal output.

Status codes:
- `TOKEN_SAVED` — success, retry publish
- `CAPTURE_TIMEOUT` — tell user: "Could not capture token. Copy it from Chrome and I'll write it to ~/.npmrc"

**After TOKEN_SAVED, retry publish** (the user already said yes to this publish in 3c):

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/publish.sh --confirm [--access public]
```

Tell user: "Complete the OTP checkbox in your browser if prompted."

## Step 4: Verify (background)

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/verify.sh <package-name> <version>
```

Run in the background (`run_in_background: true` in Claude Code, or your host's equivalent async/background execution). Exponential backoff (5s, 10s, 20s, 40s, 60s).

## Key Architecture Principle

**Scripts output status codes. The agent interprets them and talks to the user.** Script output is hidden inside collapsed bash commands — the user won't see it. All user-facing communication must be direct agent messages OUTSIDE of bash calls.
