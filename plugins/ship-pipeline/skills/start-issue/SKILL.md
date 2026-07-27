---
name: start-issue
description: "Issue intake ritual before starting any work on a GitHub issue. Repo-agnostic — reads the full issue (body + comments), verifies the work isn't already shipped, checks premises against live code, captures a baseline, and creates a correctly-named branch off the integration branch. Defers to a repo-local start-issue skill when one exists. Usage: /start-issue <issue-number>"
---

# Start Issue — Intake Ritual (repo-agnostic)

## Overview

Hour-sinks at the start of work trace to the same roots: acting on an issue's title alone, a stale premise, or a wrong branch. This skill front-loads the checks that prevent that. Output is a ~15-line intake packet — never a data dump.

**If the current repo has its own `.claude/skills/start-issue/` or `.agents/skills/start-issue/`, that version is authoritative — follow it instead.** This global version is the fallback for repos without one.

**Announce at start:** "Running /start-issue intake for #<N>."

## Step 1: Read the WHOLE issue

```bash
gh issue view <N> --comments
```

Body AND every comment. Extract: scope, explicit out-of-scope notes, acceptance criteria, decisions made in comments (rationale, scope shifts, de-promotions), linked issues/PRs.

## Step 2: Verify the work isn't already done

In repos with a dev→main promotion flow, issues typically close at MAIN — an OPEN issue may already be merged to the integration branch. Prior phases also satisfy later phases incidentally.

```bash
gh pr list --state all --search "<N>" --json number,title,state,baseRefName,mergedAt --limit 10
gh issue list --state all --search "<key words from title>" --json number,title,state --limit 10
```

Then **grep the code** for the capability itself — roadmap docs and issue states both lag the code. If the issue is more than ~1 month old, treat every premise as unverified and re-check each claimed gap against the source.

**Stop condition**: if the work already shipped, report that with evidence and STOP — the correct action is closing/commenting the issue, not re-building.

## Step 3: Branch correctly

```bash
git branch --show-current   # never trust a session-start snapshot
git status --short          # resolve uncommitted work before switching
git remote -v               # learn the remote name(s) — don't assume origin
```

Detect the integration branch (a `dev`/`develop` branch that PRs target, else the default branch), sync it, and branch as the repo's convention dictates — check recent branch names (`git branch -a | head -20`); `type/<issue-number>-<kebab-slug>` is the common pattern. Never work directly on the default or integration branch.

## Step 4: Capture the baseline

For TypeScript repos: record the current typecheck error count (`npm run typecheck` or `npx tsc --noEmit`, count errors). Your change's bar is "no worse than baseline", and a drop is a cleared defect worth stating in the PR. Check what the repo's build actually gates — many builds skip type-checking entirely.

## Step 5: Domain pre-checks (conditional)

- Touches a database → verify the live schema before planning (`db-truth`).
- The repo has domain-context skills or guidance docs for the touched subsystem → load them now.
- Touches billing/metered paths → note that every post-charge early return needs the same refund/rollback branching as the error path, with a dedicated test.

## Step 6: Emit the intake packet

~15 lines, no more:

```text
INTAKE #<N> — <title>
Goal: <one sentence>
In scope: <...>   Out of scope: <...>
Done when: <acceptance criteria>
Already-shipped check: <searched what, found what, verdict>
Premise check: <stale premises re-verified, or "issue is fresh">
Branch: <name>   Baseline: <typecheck count or n/a>
DB touched: <yes → `db-truth` done | no>
Test cases (plain English): <3-6 bullets a non-engineer can read>
Plan next: <plan mode | inline plan | trivial-fix, proceeding>
```

## Stop conditions

- Issue already shipped → report, don't build.
- Issue premises contradict live code → surface the contradiction, don't reconcile silently.
- Ambiguity about which repo/branch/worktree → ask, never guess.
- Scope depends on a decision only the user can make → state the question, state the default interpretation, proceed on the default.
