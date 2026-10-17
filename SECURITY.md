# Security Policy

## Scope

This repository ships **markdown skills that instruct an AI coding agent, and shell
and Python helper scripts those skills can invoke.** The realistic risk surface here is:

- A skill's instructions causing an agent to run a destructive or unsafe shell command.
- A skill acting on instructions planted in text it reads (an issue, a PR, a comment,
  a web page) instead of on the user's request.
- A script under `plugins/` doing something unsafe (unsanitized input, unsafe
  temp-file handling, an unpinned or untrusted download).
- Supply-chain risk in `bin/`, `package.json`, or a GitHub Actions workflow.
- A manifest (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`)
  or `plugin.json` pointing installers at something other than what it claims to.

This repo does not run a server and does not process end-user data, so most classic
web-app vulnerability classes don't apply. It does handle credentials in two places:

- `npm-publish`'s `setup-token.sh` writes an npm auth token to `~/.npmrc`.
- `readiness-review`'s `db_facts.py` reads a database connection string to run
  read-only queries.

## Reporting a vulnerability

**Please do not open a public GitHub issue for a security report.**

Private vulnerability reporting is enabled on this repository. Use it to report:

1. Go to the repository's **Security** tab.
2. Click **Report a vulnerability** to open the advisory form.
3. Fill in a title and description of the issue — a proof-of-concept skill invocation
   or script input that demonstrates the problem is the most useful thing you can
   include. Affected version/commit and suggested severity are optional but help
   triage.
4. Submit. This opens a private draft security advisory visible only to maintainers
   and repository admins — it does not create a public issue or notify anyone else.

You'll get an acknowledgement, and can continue the conversation privately on the
advisory thread, including collaborating on a fix via the temporary private fork
GitHub offers from that screen if one is warranted.

If private vulnerability reporting isn't available for any reason, open a regular
issue asking a maintainer to reach out for a private channel — don't include exploit
details in that issue.

## Supported versions

There are no long-lived version branches. Security fixes land on `main`, and the
supported versions are:

- the latest commit on `main`;
- the latest version published to npm as `@stylusnexus/agent-plugins`.

The npm package is a launcher. `npx @stylusnexus/agent-plugins` runs the Skills CLI,
which installs the skills from this repository's `main` branch, not from the files in
the npm package. Claude Code and Codex also install from `main`. So a fix on `main`
reaches new installs before the next npm release. If you're on an older copy, update
before reporting to confirm the issue still reproduces.

## Security posture

Each statement below can be checked in this repository or its GitHub settings.

### What the skills and scripts do

- Most skills are instructions only. They run nothing by themselves; the agent runs
  commands, under the host's own permission prompts.
- Scripts that only read: `readiness-review/scripts/` (reads a copy of the repo, GitHub facts through
  `gh`, and the database read-only with a timeout), `spec-review.sh` (runs Codex with a
  read-only sandbox), `npm-publish/scripts/verify.sh`, and the
  `pm-discovery` and `pm-objectives` scripts in `product-strategy`.
- Scripts that write: `exposure-scan/scan.sh` scans installed packages read-only,
  but `scan.sh refresh` writes catalogs to `~/.config/bumblebee/threat_intel` (or
  `BUMBLEBEE_CATALOG_DIR`). `readiness-review` writes its report (owner-only, never
  inside the reviewed repo). `npm-publish`'s `preflight.sh` bumps the version in local files,
  `release.sh` commits and pushes, `publish.sh` publishes to npm, and `setup-token.sh`
  replaces one line in `~/.npmrc` and sets it to owner-only.
- No script sends telemetry. Data leaves the machine only through a step the skill
  names: `git push`, PRs and merges through `gh`, `npm publish`, GitHub API reads,
  `exposure-scan refresh` (downloads catalogs), `spec-review` (sends the spec and
  repo context to the Codex model), and `visual-plan`/`visual-recap` (download their
  CLI from npm, and publish to the hosted Plan service only when the user asks).

### Where a skill pushes, merges, deploys or publishes

These skills run `git`, `gh` or `npm` with effects other people see. Each one stops
for the user at these points:

- `npm-publish`: asks before it pushes and again before it publishes. The push and
  publish scripts are not pre-approved in the skill's `allowed-tools`, so the host
  also prompts before each run. Both refuse (`DIRTY_TREE`) while tracked files have
  uncommitted changes, so nothing is published that is not in git.
- `review-merge-pipeline`: merges only when the user invoked it in this run, never
  with `--admin`, and only the reviewed commit (`--match-head-commit`) with every
  required check passing. `--no-merge` stops at the PR.
- `ship-issues`: merges without asking only when the user's request says to merge or
  ship ("merge when green", "implement and merge", "ship these"). Otherwise it opens
  every PR without merging, lists them with their head SHAs, and asks once. It deploys only when the user asked to ship, deploy
  or release in this run.
- `deploy`: shows the list of issues it would close and closes only the ones the user
  confirms. A migration needs a confirmed restorable backup first.
- `pr-wait`: merges only when called with `auto_merge` set to true.
- `the-waiting`: report-only. It never cancels, reruns, approves or merges; any fix
  it names is a command for the user to run.

### Threat model for skills

- **Prompt injection from issue and PR text.** `start-issue`, `ship-issues`,
  `review-merge-pipeline` and `deploy` treat issue, PR and comment text as untrusted
  data, never instructions. Text there never authorizes a merge, a deploy or an issue
  closure. A decision found there is treated as still open; one that changes scope,
  security, data handling or spend is confirmed with the user before it is built.
- **Remote content.** `exposure-scan` downloads its catalogs from one pinned commit
  and parses them as JSON. Treat any page or file a skill fetches as data, not as
  instructions.
- **`npx` and other installs.** In `SKILL.md` text and scripts, commands that fetch a
  tool from outside the project being worked on name exact versions:
  `@agent-native/core@0.200.0` in `visual-plan` and `visual-recap`, `skills@1.7.0`
  in the launcher, `agent-browser@0.38.2` for `npm-publish`, and a bumblebee commit
  SHA for `exposure-scan`. The pinned version is the protection: a new upstream
  publish cannot change what runs. npx does not ask before installing when an agent
  runs it, so the agent host's own permission prompt is where you approve each
  command. Pins are bumped only to releases at least two weeks old. The install
  lines in the READMEs and on the site (`npx skills add …`) are for people to run
  and use the newest Skills CLI; `npx skills@1.7.0 add …` pins it.
- **External plugins.** `work-plan` and `defect-scan` live in their own repositories.
  The marketplace manifests pin them by tag (`work-plan` `v2026.10.06-4ae1fe1`,
  `defect-scan` `v1.13.0`), not by commit SHA, so they trust those repositories not
  to move a tag.

### Supply-chain controls

- Every GitHub Action in `.github/workflows/` is pinned to a full commit SHA, with the
  release in a trailing comment.
- Dependabot (`.github/dependabot.yml`) opens weekly PRs to update those pins.
- Each workflow sets its own token permissions, and the repository's default
  workflow token is read-only.
- npm publishing is set up to run from `.github/workflows/npm-publish.yml`: it
  publishes only on `main` (a run on any other branch fails), with `--provenance`,
  and still uses an `NPM_TOKEN` secret. Anyone holding a publish token for the
  package, or using the `npm-publish` skill, can also publish from their own
  machine, without provenance. Provenance exists only for versions the workflow
  publishes after this change; earlier versions, including 1.4.1, have none.
- Secret scanning and push protection are on. CodeQL default setup is on for
  Actions, JavaScript/TypeScript and Python.
- The npm package has no dependencies and no install scripts.

### Repository protections

- A ruleset on `main` blocks deletion and force-pushes, requires a pull request, and
  requires the `check` (manifest-sync) and `hygiene` (ci) status checks.
- GitHub Actions cannot approve pull requests.
- Repository and organization admins can bypass the ruleset.

### Before you run a skill

- Read its `SKILL.md` and any script next to it. They are short, and they are what
  the agent will follow.
- Pin what you install: a marketplace tag or commit, or a copy of the skill folder
  you have read, rather than whatever is newest.
- Keep your agent's permission prompts on for commands that push, merge, deploy or
  publish.

## Disclosure

We'll credit reporters (unless you ask not to be) once a fix is published. There's
no bug bounty — this is an open-source marketplace, not a funded program.
