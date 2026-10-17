---
name: dependency-upgrade
description: Safe batch dependency upgrades across a codebase — inventory outdated packages (npm outdated / uv lock --upgrade), group by risk (patch/minor/major), upgrade in waves with tsc/test/Playwright gates, read changelogs for majors, run `exposure-scan` for supply-chain checks, and land one PR per wave. Use when asked to "upgrade dependencies," "bump packages," "clear npm outdated," or on a periodic maintenance pass.
---

# Dependency Upgrade

## Overview
Bulk dependency bumps are routine but not risk-free — a single bad major-version bump can break a build silently until deploy, and supply-chain compromises (the kind `exposure-scan` catches) don't announce themselves. This skill treats upgrades as a small pipeline with gates, not a single `npm update` and a prayer. Node/TypeScript projects use `npm`; Python projects use `uv`. Run Playwright E2E where the project has it — applications that render a UI — and skip it for pure libraries.

## Workflow

1. **Inventory.** Run the right command for the stack:
   - Node/TS: `npm outdated --json` for a structured list of current/wanted/latest per package.
   - Python (uv-managed): `uv tree --outdated` to list the latest available version of each package, and `uv lock --upgrade --dry-run` to preview lockfile changes without writing them.
   - Record: package name, current version, latest version, and whether the jump is patch/minor/major (semver diff).

2. **Group by risk**, not alphabetically:
   - **Patch (x.y.Z):** bug fixes only, per semver contract. Batch these together — low risk, high volume.
   - **Minor (x.Y.z):** new features, should be backward compatible. Batch by ecosystem (all `@types/*` together, all `eslint-*` together) to keep changelogs reviewable in one pass.
   - **Major (X.y.z):** breaking changes possible/likely. One package (or tightly coupled group, e.g., `next` + `eslint-config-next` + `@next/*`) per wave — never bundle unrelated majors together.

3. **Upgrade in waves**, smallest risk first:
   - **Wave 1 — patches:** `npm update <pkg>...`, or `uv lock --upgrade-package <name>` per package then `uv sync`; run gates, one PR. `npm update` stays inside the ranges declared in `package.json`, so it never moves a major. `uv lock --upgrade` (no package) moves everything as far as `pyproject.toml` bounds allow, which can include majors on unbounded dependencies — prefer `--upgrade-package` here.
   - **Wave 2 — minors:** `npm install <pkg>@^<x.y>` per ecosystem group, or `uv lock --upgrade-package <name>` then `uv sync`; run gates, one PR per group (or one PR if the groups are small and unrelated-but-safe).
   - **Wave 3+ — majors:** changelog read first (see step 4), then `npm install <pkg>@<major>`, or raise the bound in `pyproject.toml` and run `uv lock --upgrade-package <name>` then `uv sync`; run gates, one PR per major (one package or tightly coupled group).
   - Never combine a major bump with unrelated patch/minor bumps in the same PR — if something breaks, you want to know which bump did it without bisecting a mixed diff.

4. **Read changelogs before any major bump.** Pull the changelog/release notes (GitHub releases page, or the package's `CHANGELOG.md`) for every version between current and target — not just the latest entry. Look specifically for: removed APIs, config-file format changes, Node/TypeScript minimum-version bumps, peer-dependency changes. For framework majors (Next.js, React, Prisma) check the official migration guide, not just the changelog — use WebSearch/Context7 if available rather than relying on memory, since major-version migration steps change and training data may be stale.

5. **Run the gates for every wave, in this order**, stopping at the first failure:
   - `tsc --noEmit` — type-check gate, catches API surface changes immediately.
   - Unit/integration test suite — catches behavioral regressions.
   - `npx playwright test` (projects with an E2E suite) — catches UI/E2E regressions the type checker can't see, especially after UI-library or Next.js bumps.
   - If any gate fails: run the same gate on the base commit the wave branched from. Fails there too → pre-existing; stop and report it, and do not blame or ship the bump. Passes there → the bump caused it.

6. **Run `exposure-scan`** before finalizing any wave — this checks installed packages against threat-intel catalogs of known-compromised releases. Run it especially for major bumps that pull in new transitive dependencies, since a new sub-dependency is a new unvetted surface.

7. **Lockfile hygiene:** commit the updated lockfile (`package-lock.json` / `uv.lock`) in the same PR as the version bump — never let `package.json` and the lockfile drift. Don't hand-edit lockfiles; regenerate them via the package manager. Before pushing, confirm the lockfile matches the manifest: `npm ci` succeeds (it errors when `package.json` and `package-lock.json` disagree) or `uv lock --check` passes.

8. **One PR per wave**, titled per Conventional Commits: `chore(deps): bump patch dependencies` / `chore(deps): bump next to v15` etc. Squash-merge per house convention, feature-branch naming `chore/<issue>-deps-<wave>` if an issue number exists, otherwise a clear branch name.

## Checklist
- [ ] Full inventory taken (`npm outdated` / `uv tree --outdated`) before touching anything
- [ ] Packages grouped patch/minor/major, majors split one-per-wave (or tightly coupled group)
- [ ] Changelogs/migration guides read for every major, using current docs (WebSearch/Context7) not memory
- [ ] Gates run in order per wave: `tsc --noEmit` → tests → Playwright (where applicable)
- [ ] `exposure-scan` run per wave, especially majors with new transitive deps
- [ ] Lockfile committed alongside `package.json`/`pyproject.toml` changes, and `npm ci` / `uv lock --check` passes
- [ ] One PR per wave with a Conventional Commit title

## Pass/fail per wave

- **Pass:** every gate green on the wave branch; `exposure-scan` clean; lockfile and manifest committed together; lockfile check passes.
- **Fail:** any gate red that is green on the base commit; any `exposure-scan` hit; lockfile out of sync with the manifest.

## Common mistakes

- Running `npm update` and expecting majors; it only moves within declared ranges.
- Bumping a major after reading only the latest release's notes.
- Re-running a red gate until it turns green instead of finding the cause.
- Committing `package.json` without the lockfile, or the reverse.

Sources: [`npm update`](https://docs.npmjs.com/cli/commands/npm-update), [`npm ci`](https://docs.npmjs.com/cli/commands/npm-ci), [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

## Output
A wave plan (table: package / current / target / risk tier / wave) up front, then per-wave PRs with gate results pasted into the PR description as evidence.

## Stop Conditions
- Any gate fails and the cause isn't clearly the dependency bump (looks like a pre-existing flake or unrelated issue) → stop and investigate before merging; don't paper over a red gate by re-running until it's green.
- `exposure-scan` flags a package as matching a known-compromised release → stop immediately, do not proceed with that upgrade, and surface it — this is a supply-chain incident, not a routine finding.
- A major bump's migration guide requires a schema migration (Prisma major, database driver major) against a production database → confirm a fresh backup that restores with the `backup-verify` skill and follow `db-migration-safety` (both in the `ship-pipeline` pack) before applying anything beyond a dev/staging environment.
