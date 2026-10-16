# Ship Pipeline

Eight repo-agnostic skills for the ship half of the development loop — from reading the issue to promoting to production, with evidence at every gate.

Every skill detects the repository's own conventions rather than assuming a house style, and each **defers to a repo-local version of itself** when the project defines one (`.claude/skills/<name>/`). Install it globally; override it per-repo where a project has stronger rules.

---

## The loop

| Phase | Skill | What it does |
|---|---|---|
| **Intake** | `start-issue` | Reads the full issue — body *and* comments, where scope changes hide. Checks whether the work already shipped, captures a baseline, branches off the detected integration branch. |
| **Ground** | `db-truth` | Verifies schema claims against the live database before you design against them, and confirms migrations actually landed after you apply them. |
| **Verify** | `prove-it` | End-of-work evidence protocol. Discovers what CI *actually* gates, runs both static gates, checks threaded values at their terminus, does one real round-trip, and emits a claim→command→result table. |
| **Inspect** | `review-slop` | Reports needless complexity, validation gaps, misleading test coverage, and prose problems with evidence and acceptance criteria. Makes no edits. |
| **Ship** | `review-merge-pipeline` | One shot: verify → review → fix → commit → push → PR → merge. Detects the merge target instead of assuming one. |
| **Promote** | `deploy` | Integration branch → production, with the repo's own merge strategy inferred from its history. |
| **Schema** | `db-migration-safety` | Expand-contract migrations, idempotent SQL, batched backfills. |
| **Schema** | `backup-verify` | Confirms backups exist **and actually restore** — into a scratch branch, with smoke queries and timestamped evidence. |

### Why `prove-it` is not "trust but verify"

Trust-but-verify presumes a claim is sound and spot-checks it. `prove-it` inverts the burden of proof: nothing is done until a command's output backs it, and anything unprovable is stamped `UNVERIFIED` rather than assumed fine. The premise is uncomfortable — features that passed build, typecheck, tests, review, *and* deploy, and were still dead in production, because no gate ever exercised a real write.

> An honest `UNVERIFIED` outranks a confident guess.

---

## Rule ownership

Each concern lives in exactly one skill. When a task crosses domains, the owner below keeps the rule and the others name only the handoff — this is what stops eight skills from firing on the same prompt.

| Skill | Owns |
|---|---|
| `start-issue` | Issue comprehension, prior-art checking, baseline capture, branch naming |
| `db-truth` | **Reading** schema truth — shape, relationships, permissions, and post-apply confirmation |
| `db-migration-safety` | **Writing** schema change — expand-contract sequencing, idempotency, backfills |
| `backup-verify` | Backup existence and restore-testing; the go/no-go before a risky mutation |
| `prove-it` | Evidence standards, gate discovery, the evidence table, `UNVERIFIED` labeling |
| `review-slop` | Report-only slop findings, severity calibration, and suggested repair criteria |
| `review-merge-pipeline` | Review orchestration, commit/push/PR mechanics, merge-target detection |
| `deploy` | Production promotion, merge strategy, release-tooling compatibility |

The three database skills are the pairing most worth keeping straight: **`db-truth` reads, `db-migration-safety` writes, `backup-verify` is the safety net before either touches production.**

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install ship-pipeline@stylus-nexus
```

Plugin skills are namespaced: `/ship-pipeline:prove-it`, `/ship-pipeline:deploy`, and so on.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
```

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins            # pick interactively
npx skills add stylusnexus/agent-plugins --skill '*'  # take all of them
```

The [Skills CLI](https://github.com/vercel-labs/skills) detects which agents you have installed and writes to each one's skills directory. Skills arrive un-namespaced here, so they invoke as `/prove-it` rather than `/ship-pipeline:prove-it`.

---

## Prerequisites

The skills shell out to standard tooling; install what your workflow touches:

- **`git`** and **`gh`** (authenticated via `gh auth login`) — issue intake, PR creation, merging
- **A typecheck and build command** — discovered from the repo, not assumed
- **Database CLI** *(only for the schema skills)* — `psql`, the Supabase CLI, or the Neon CLI, depending on your stack

## Safety notes

- `review-merge-pipeline` merges pull requests. Read it before first use, and pass `--no-merge` to stop at PR creation while you get a feel for it.
- `deploy` promotes to production. It fast-forwards local refs and compares against fresh upstream state before acting.
- `backup-verify` and `db-migration-safety` are deliberately conservative: they print the affected scope before any destructive step.

## License

MIT © Stylus Nexus Holdings LLC — see the [repository LICENSE](../../LICENSE).
