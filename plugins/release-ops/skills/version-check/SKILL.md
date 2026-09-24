---
name: version-check
description: Analyze changes since the most recent version tag and recommend a semantic-version bump. Use before publishing to npm or when deciding whether a release should be a major, minor, or patch bump.
---

# Version Check

Analyze changes since the last version tag and recommend a semver bump.

Use this skill before running `npm publish` or when deciding what version to bump to. Invoke with `/version-check`.

## When to Use

- Before publishing to npm
- When the user asks "what version should this be?"
- When the user says "bump", "version", or "publish"

## Process

1. Find the last git tag matching `v*` (e.g., `v0.2.0`)
2. Get the diff since that tag: `git diff <tag>..HEAD --stat` and `git log <tag>..HEAD --oneline`
3. Analyze the changes against these rules:

The examples below use a fictional package, `acme-sdk` — substitute the real repo's own file paths and exported names.

### Pre-1.0 Rules (current package version starts with 0.x)

| Bump | Trigger |
|---|---|
| **Minor** (0.x.0 -> 0.(x+1).0) | Any breaking change: renamed/removed exports from `src/index.ts`, changed required fields in `src/types/index.ts`, removed or renamed public methods in `src/client.ts` |
| **Patch** (0.x.y -> 0.x.(y+1)) | Bug fixes, new entries in `src/config/default-config.ts`, new eval samples, documentation, non-breaking additions |

### Post-1.0 Rules (package version >= 1.0.0)

| Bump | Trigger |
|---|---|
| **Major** (x.0.0 -> (x+1).0.0) | Breaking changes: renamed/removed exports, changed required fields in types, removed/renamed public methods |
| **Minor** (x.y.0 -> x.(y+1).0) | New features: new resource adapters, new config options, new public methods (backward-compatible) |
| **Patch** (x.y.z -> x.y.(z+1)) | Bug fixes, config updates, documentation changes |

### Breaking Change Signals

Look for these in the diff:
- Removed or renamed `export` statements in the package entry point
- Changed `interface`/`type` definitions with new required fields, removed fields, or type changes
- Renamed or removed public methods on the main exported class
- Any commit message containing `BREAKING CHANGE` or `feat!:`

### Non-Breaking Signals

- New `export` additions (not removals)
- New optional fields (with `?`) in interfaces
- New source files added (not modifying existing public API)
- Changes only in config/data files, scripts, docs, or tests

## Output Format

```
Version Check Report
====================
Current version: 0.2.0
Last tag: v0.2.0
Commits since tag: N

Recommendation: MINOR bump -> 0.3.0
Reason: Breaking changes detected

Evidence:
  - src/types/index.ts: Added required 'region' field to Widget interface
  - src/client.ts: Renamed fetchWidget() to fetchWidgetSync()
  - src/index.ts: Added new type exports (RetryConfig, WidgetSource)

Changed files:
  src/types/index.ts (modified)
  src/client.ts (modified)
  ...
```

4. Present the recommendation clearly
5. Ask the user to confirm before bumping

## Important

- Only recommend bumping. Do NOT run `npm version` or modify `package.json` without explicit user confirmation.
- If there are no changes since the last tag, say "Nothing to bump — no changes since last publish."
- If there is no git tag, use the initial commit as the baseline and note this.
