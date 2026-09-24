---
name: ship-issues
description: "Take a batch of GitHub issues from intake through merge — and, only for a ship/deploy/release request, on through a production deploy and validation. 'Ship' means deploying to production: for that request it grounds every issue, reports status and grouping before any edit, implements each group, merges, deploys, and validates against production, calling start-issue, prove-it, review-merge-pipeline and deploy rather than restating them. An 'implement and merge' request stops after the merges — no promotion, no deploy. Repo-agnostic; defers to a repo-local ship-issues when one exists. Use on /ship-issues <N> <N> ..., or when asked to implement and ship/deploy/release several issues (deploys), or to implement and merge them (does not deploy)."
---

# Ship Issues — a batch from intake to production (repo-agnostic)

## Overview

The batch layer above `start-issue`. `start-issue` sets up ONE issue; this skill carries a SET of issues through grounding, grouping, implementation, merge, deploy and post-deploy checks. It owns the batch decisions (status, grouping, order, what to ask) and calls the per-step skills for everything else: it does not restate their rules.

**If the current repo has its own `.claude/skills/ship-issues/` or `.agents/skills/ship-issues/`, that version is authoritative — follow it instead.** This global version is the fallback.

**Usage:** `/ship-issues 101 204 317` (duplicates collapse; order doesn't matter).

**Authority.** Invoking this skill authorizes: branching, committing, pushing feature branches, opening PRs to the integration branch, and merging them once required checks pass. **Only for a ship/deploy/release request**, it additionally authorizes running `deploy` and read-only post-deploy validation — "ship" means production. For an "implement and merge" request, none of that is authorized: the run stops after Phase 4, merged and reported, without running `deploy`. Merged code may still go live on its own if the host deploys from the branch the PRs merge into (single-trunk repos, or hosts that deploy from the integration branch); Phase 1's report says which applies. It does NOT authorize: skipping a failed or missing required check, admin/bypass merges, force-pushes, applying a migration without the `backup-verify` check, or deciding a product question the consultations leave open.

**Announce at start:** "Running /ship-issues for #A, #B, #C."

## Phase 1 — Ground (no edits)

1. **Refresh refs and learn the branch model.** Fetch the primary remote (`git remote -v` — don't assume `origin`). Read the default branch from the host, not memory: `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`. Detect the integration branch the way `review-merge-pipeline` does. Compare against remote-tracking refs by full name (`refs/remotes/<remote>/<branch>`): a local branch named `<remote>/<branch>` would otherwise shadow it.
2. **Run `start-issue` Steps 1–2 per issue, without creating a branch.** It owns issue comprehension (body + every comment, where scope changes hide) and the already-shipped check (`stateReason: NOT_PLANNED` means closed without a fix — don't go looking for the code). Classify each issue from what it returns — every "done" or "partly done" claim carries a PR number plus a `file:line` or a live probe:
   - **Shipped** — closed as completed, the fix is on the production branch, and verified live when behaviour matters. CLOSED is not shipped: GitHub closes an issue with a closing keyword when its PR merges into the repository's *default branch*, regardless of merge method — and the default branch may be the integration branch, not production, so a closed issue can still be unreleased.
   - **Partly shipped** — say exactly what's left.
   - **Blocked** — name the one blocker (a missing decision, an unmerged dependency).
   - **Open work.**
3. **Check premises against live data** where an issue claims something about production (a count, a field name, a rate). Read-only queries only, and exclude test and internal accounts from anything counted. Schema claims go through `db-truth`.
4. **Group.** Issues that share files or a design decision go on one branch. Unrelated issues stay separate so one failure doesn't block the rest.
5. **Emit the grounding report** before touching a file:

```text
Base: <integration> = <sha>, <production> = <sha> (verified via gh). Unreleased on <integration>: <yes/no + evidence>.
Goes live on merge? <yes/no — does the host deploy from the branch these PRs merge into; evidence or "unknown">
| Issue | Status | What's left |
Groups: <group → issues → branch name>
Dependencies / blocked: <...>
Decisions needing consultation: <...>
```

Then proceed without waiting, unless a decision in Phase 2 stays unresolved.

## Phase 2 — Decide (consult before asking)

For each open decision, consult a specialist agent before escalating to the user — whichever your setup has for the question type (domain rules, backend or agent design, UI and interaction, data or schema). Ask for the verdict in the agent's opening lines; long reports lose their conclusion.

Ask the user only when a decision is still open after consultation AND it changes what gets built: one question, your default stated, then proceed on the default. Legal, licensing, security or secrets doubt is always a full stop.

## Phase 3 — Implement each group

Per group:

1. Per issue in the group, run `start-issue`'s Steps 1-2 (intake, already-shipped check) and Step 4 (baseline capture) — every issue needs its own comprehension and baseline, and `start-issue` owns both. Run `start-issue`'s Step 3 (branch creation) only ONCE for the whole group, using the group's branch name from Phase 1's grounding report — running it per issue would create a separate branch per issue and defeat the grouping Phase 1 just decided.
2. Load any repo-local domain-context skill or guidance doc for the subsystem the group touches.
3. Run independent groups in parallel, each in its own worktree, so one group's failure can't contaminate another's tree. Give each agent a self-contained packet: goal, decided rule, files, tests to write, stop conditions, and the deliverable in its opening lines. Match the model to the risk: a stronger model for core-pipeline, schema, auth or billing changes. When a worktree needs dependencies or env files, copy dependencies rather than symlinking them, and never link a production env file into a worktree.
4. Test-first where a test can lead.
5. `prove-it` before the PR. It owns the gates, the baseline comparison and the evidence table. Two batch-specific cautions when reading its results:
   - A worktree can report typecheck errors the primary checkout doesn't (a sub-package without its own dependencies installed). Diff the error lists against the baseline before blaming the change.
   - A network fetch failure during build, or a single test timeout under parallel load, gets one isolated rerun before it counts as a failure. A second identical failure is real.

## Phase 4 — Ship each group

1. `review-merge-pipeline` for each group, with `--cross-model` for anything touching billing, auth, schema, the core pipeline, or several systems. It owns review, fixes, push, PR creation against the detected integration branch, the head-SHA and required-check confirmation, and the merge — confirmed findings are fixed and re-verified through `prove-it` INSIDE that run, before it merges (its own Steps 2-3). This phase doesn't re-run or restate that.
2. If a finding surfaces only after a group has already merged — a slower cross-model pass landing late, or something Phase 6's production validation turns up — it goes into an explicit follow-up PR. Never reopen or push new fixes onto a branch that's already merged.
3. A group whose checks fail twice after a reasonable fix stops: record it as blocked with the commands and output, and continue with the other groups.

## Phase 5 — Deploy

**Run this phase (and Phase 6) only for a ship/deploy/release request.** If the request was to *merge* the batch — not ship, deploy, or release it — stop after Phase 4 and report; do not run `deploy`, and do not run Phase 6's production validation. "Ship" means production; it isn't a stronger synonym for "merge."

**If `$BASE` is already the production branch** (`$BASE` here is the merge target `review-merge-pipeline` detects per-group in its Prerequisites, not something this skill sets independently — a single-trunk repo with no separate integration branch), there's no promotion step to run — skip this phase and go straight to Phase 6. `review-merge-pipeline` already gated any migration-touching merge in that case on a confirmed `backup-verify` backup before merging (its Step 1) — this phase doesn't need to re-check it.

Otherwise, once every shippable group has merged, run `deploy` once for the batch — not once per group. It owns promotion, merge strategy, release tooling, migrations (including confirming a restorable backup before any promotion that auto-applies migrations) and issue closing; this skill defers to it for all of that rather than restating it.

**Find out when code actually goes live.** Some hosts deploy from the integration branch, so merged code is live before promotion; others deploy only from the production branch. Read the host config rather than assuming, and time Phase 6 from the real go-live point.

Record the release version, the production merge SHA, and the host's deploy ID for that SHA.

## Phase 6 — Validate against production

Only after the host reports the deploy live:

1. **Probe each group's acceptance signal** — the row, event, field or response the change was meant to produce — read-only.
2. **Exercise the changed path for real** when a group changed a generator, an export or another output surface: produce one real output through the production entry path and inspect it (for a document export, extract the text rather than eyeballing a thumbnail). Use the repo's own end-to-end or review skills where it has them.
3. **Before filing any follow-up,** search open and closed issues (`gh issue list --state all --search ...`) and file only what isn't there, with the repo's type label.

## Final report

Include:

- the issue grouping;
- per-issue status (merged, deployed, blocked, left open with the reason);
- the tests and commands run, with counts;
- the deployment identity (version, production SHA, host deploy ID);
- migration status;
- post-deploy validation evidence;
- unresolved risks;
- the decisions deferred to the user.

Label anything unverified as UNVERIFIED.

## Stop conditions

- An issue's premise contradicts live code or data → surface it in the grounding report; don't silently reconcile.
- A required check is failing or missing → that group doesn't merge. Never bypass it.
- A migration with no confirmed restorable backup → don't promote it.
- Ambiguity about which repo, branch or worktree → ask, never guess.
