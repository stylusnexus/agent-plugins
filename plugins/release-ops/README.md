# Release Ops

Five skills for getting a release out the door — deciding the version, waiting on CI, publishing, and keeping dependencies current between releases.

---

## The skills

| Skill | Use it when |
|---|---|
| `version-check` | You need to decide the next version. Reads the commits since the last tag and recommends major, minor, or patch, with the reasoning. |
| `pr-wait` | A PR is open and you want to block on CI rather than watch it, optionally merging when checks pass. |
| `the-waiting` | CI is running and you want to know how long is really left, or why a run is still pending. Estimates each job from its own history, spots runs stuck behind a cancelled one, and suggests something small to do meanwhile. Named for Tom Petty's "The Waiting", because it is the hardest part. |
| `npm-publish` | Publishing to npm or bun — preflight checks, semver bump, changelog entry, git push, publish, verify. Rotates an expired npm token through the browser instead of stopping to ask for a one-time code. |
| `dependency-upgrade` | Bulk dependency bumps. Treats them as a gated pipeline — inventory, batch, then type check, test, and E2E between batches — rather than one update command and hope. |

---

## Rule ownership

| Skill | Owns |
|---|---|
| `version-check` | Deciding *what* the next version should be |
| `pr-wait` | Waiting on CI for an open PR, and merging on green |
| `the-waiting` | Explaining a wait: time left, stuck runs, and what to do meanwhile. Never cancels, reruns, or merges |
| `npm-publish` | Everything from bump to published artifact, including auth |
| `dependency-upgrade` | Incoming dependency changes and the gates between batches |

**`version-check` recommends; `npm-publish` executes.** Run the first when you want the decision explained, the second when you've made it. `npm-publish` will bump on its own, so pairing them is optional rather than required.

`pr-wait` overlaps slightly with the `ship-pipeline` pack's `review-merge-pipeline`, which also pushes, opens a PR, and merges. The split: **`review-merge-pipeline` owns the whole path from unreviewed changes to merged; `pr-wait` owns only the tail** — a PR already exists, and you want to block on its checks. Reach for `pr-wait` when someone else opened the PR, or when you deliberately stopped at PR creation.

For repository activity summaries — what shipped, what's open, CI health — use `/work-plan:repo-activity-summary` from the `work-plan` plugin rather than looking for it here.

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install release-ops@stylus-nexus
```

Skills are namespaced: `/release-ops:npm-publish`.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add release-ops@stylus-nexus
```

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins --skill '*'
```

Skills arrive un-namespaced on this path, so they invoke as `/npm-publish`.

---

## Prerequisites

- **`gh`** (authenticated) — `pr-wait` reads check status through the GitHub CLI
- **`npm`** or **`bun`** — `npm-publish` supports either
- **`agent-browser`** — only for `npm-publish`'s token rotation; without it, publishing still works when your existing npm auth is valid
- **`uv`** for Python projects — `dependency-upgrade` uses `npm` for Node/TypeScript and `uv` for Python

## Security note

`npm-publish` handles registry credentials. Its `setup-token.sh` writes an npm auth token to `~/.npmrc`, and the token-rotation flow drives a browser to mint a new granular access token. No credentials are stored in this repository, and none are transmitted anywhere except to the npm registry — but read the scripts before first use, as you should with anything that touches publish rights.

The publish path deliberately pushes to git **before** publishing to npm, so a published version always corresponds to a commit that exists upstream.

## License

MIT © Stylus Nexus Holdings LLC — see the [repository LICENSE](../../LICENSE).
