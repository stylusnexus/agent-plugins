---
name: review-merge-pipeline
description: Automated pipeline that verifies changes with `prove-it`, code-reviews them, fixes issues found, commits, pushes, creates a PR, and merges. Detects the repo's integration branch rather than assuming one. Accepts an optional worktree path argument and flags --base / --no-prove / --no-review / --no-merge / --rebase / --cross-model. Use when work is done and you want to ship it without manual steps.
---

# Review-Merge Pipeline

## Overview

One-shot pipeline: **code review → fix → commit → push → PR → merge**. No manual steps, no questions — review, open the PR, and merge it. (Merging is not a production deploy unless your host deploys from the PR's base branch.)

**Announce at start:** "Running the review-merge pipeline."

## Prerequisites

**Merge target:** Detect the repo's integration branch — don't assume. If an integration branch exists alongside the production branch (commonly `dev`, `develop`, or `staging`), PRs target it and production promotion happens separately via the `deploy` skill. If the repo ships from a single branch, PRs target that branch directly.

```bash
SLUG=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
REMOTE=$(git remote | grep -qx upstream && echo upstream || echo origin)   # READ remote — see the push-remote note in Step 0.5
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
git remote show "$REMOTE" | sed -n 's/.*HEAD branch: //p'   # sanity-check against the above
# Anchor to remotes/$REMOTE/ specifically — an unanchored match also catches
# a local branch or another remote's same-named branch.
CANDIDATES=$(git branch -a | grep -oE "remotes/$REMOTE/(dev|develop|staging)$" | sed 's#.*/##' | sort -u)
echo "default=$DEFAULT_BRANCH candidates=$CANDIDATES"
```

**`PRODUCTION` is not necessarily `$DEFAULT_BRANCH`.** Same trap the `deploy` skill guards against for its `$RELEASE` — and both skills use the identical detection below, so a repo is never read as two-trunk by one and single-trunk by the other:
1. **Defer to a repo-local runbook if one exists** — check, in order: `CLAUDE.md`/`AGENTS.md` for a "Releasing"/"Deploy" section, a project-level `.claude/skills/deploy/` or `.agents/skills/deploy/`, `CONTRIBUTING.md`, `docs/DEPLOY*`/`RELEASING*`. If it names a production/release branch, use that.
2. **Otherwise, if `$DEFAULT_BRANCH` itself matches `dev`/`develop`/`staging`** — ask the user which branch actually ships; don't assume `$DEFAULT_BRANCH` is production. Gate on `$DEFAULT_BRANCH`'s own name only, not on whether `$CANDIDATES` is non-empty — a stray `dev`-shaped branch elsewhere in the repo isn't evidence about what `$DEFAULT_BRANCH` is. This is also the case that matters most to catch: a repo whose default branch IS `dev` (a dev→main promotion flow) must not be misread as single-trunk.
3. **Otherwise**, `PRODUCTION=$DEFAULT_BRANCH`.

```bash
PRODUCTION=<repo-local runbook value, user-provided, or $DEFAULT_BRANCH per the above>
```

If `$CANDIDATES` has more than one entry (e.g. both `dev` and `staging` exist on `$REMOTE`), STOP and ask the user which one PRs actually target. Otherwise set `BASE` explicitly to that single candidate, or to `$PRODUCTION` if the repo ships from a single branch:

```bash
BASE=<the single candidate, $PRODUCTION, or user-provided>
```

Pass `--base <branch>` to override the detected target. Every step below uses `$BASE`, `$REMOTE`, `$SLUG`, and `$PRODUCTION` as set here — never a hard-coded branch name.

**The feature-branch and pending-changes check, and the push-remote detection, happen in Step 0.5 below** — after Step 0 resolves the real working directory (a worktree argument changes which branch is actually checked out; checking here, before that resolution, would check the wrong branch).

## The Pipeline

### Step 0: Handle Worktree Argument (Optional)

The skill accepts an optional worktree path as its first argument:

```
/review-merge-pipeline .worktrees/my-feature
/review-merge-pipeline /absolute/path/to/worktree
```

**If a path argument is provided:**

1. Resolve to an absolute path and verify it exists:
   ```bash
   WT_PATH="$(cd "$ARG" 2>/dev/null && pwd -P)" || { echo "Path does not exist: $ARG"; exit 1; }
   ```
   Use `pwd -P` (physical path), not bare `pwd` — `git worktree list --porcelain` reports the canonical, symlink-resolved path, and a bare `pwd` preserves a symlink component in `$ARG`'s path instead of resolving it. Verified in scratch: entering a worktree through a symlinked path, bare `pwd` printed the symlink's own path while `pwd -P` printed the same physical path `git worktree list --porcelain` reports — with bare `pwd`, Step 0's exact-string match in the next step fails even for a genuinely registered worktree.
2. Verify it's a registered git worktree:
   ```bash
   git worktree list --porcelain | grep -q "^worktree $WT_PATH$" || { echo "Not a registered git worktree: $WT_PATH. Run 'git worktree list' to see registered worktrees."; exit 1; }
   ```
3. Remember the caller's directory so the final cleanup step can return there:
   ```bash
   ORIGINAL_PWD="$(pwd)"
   cd "$WT_PATH"
   ```
4. All subsequent pipeline steps (build check, review, commit, push, PR, merge) run **inside the worktree**.

**If no argument is provided:** The pipeline runs in the current working directory (original behavior — no change).

**Why this matters:** Worktrees let you ship a completed branch without disturbing another feature branch you're working on in the primary checkout. The post-merge step (Return to Dev) is worktree-aware — see Step 8.

### Step 0.5: Pre-flight checks

Now that the working directory is resolved (the worktree from Step 0, or the primary checkout):

```bash
# Push target: the remote the CURRENT branch tracks — not $REMOTE from
# Prerequisites, which deliberately prefers "upstream" for READS. Pushing to
# upstream by default breaks fork workflows: upstream is typically read-only
# for you there. Verified: `git rev-parse --abbrev-ref --symbolic-full-name
# @{u}` fails cleanly (non-zero exit, no stdout) when the current branch has
# no upstream configured yet — the common case for a brand-new feature
# branch — so this falls back to origin rather than to $REMOTE.
PUSH_REMOTE=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null | sed 's#/.*##')
PUSH_REMOTE=${PUSH_REMOTE:-origin}
```

1. You're on a feature branch — not `$BASE` and not `$PRODUCTION`. If on either, abort with: "Cannot run pipeline on <branch>. Create a feature branch first."
2. There are staged or unstaged changes, or unpushed commits — if nothing to ship, abort with: "Nothing to ship."

### Step 1: Verification Gate (`prove-it`)

**Default behavior:** Run the `prove-it` skill (both static gates, targeted tests, terminus checks, real persistence round-trip, render-surface proof → evidence table). If a `prove-it` evidence table was already produced for these exact changes earlier in this session, reuse it in the PR body instead of re-running.

**If `--no-prove` was passed** (or the change is docs-only), the floor is still the static gates — and note that a build alone is often NOT a type gate (many repos set `ignoreBuildErrors` or equivalent):

```bash
npm run typecheck 2>/dev/null || npx tsc --noEmit   # TS repos
npm run build  # or cargo build, go build, etc.
```

**If the diff touches migration files** (`supabase/migrations/`, `prisma/migrations/`, `migrations/`, or the repo's documented path — same detection `deploy` uses): require `db-truth` Part B evidence (ledger listing + object probed in the target DB) before proceeding to merge.

**If `$BASE` is `$PRODUCTION` itself** (a single-trunk repo with no separate integration branch — see Prerequisites) **and the diff touches migration files:** this merge IS the risky mutation against production directly, with no later `deploy` promotion to gate it the way `deploy` Step 6.5 does for a two-trunk repo. Run `backup-verify` and get a confirmed restorable backup before merging. Do not proceed to Step 7 without it.

**If any gate fails:** Fix the errors, re-run. Do NOT proceed to review with a failing gate. UNVERIFIED rows in the evidence table get called out in the PR body, never silently dropped.

### Step 2: Code Review

Launch a code-review agent for all uncommitted changes (or all commits on the branch if already committed) — `pr-review-toolkit:code-reviewer` if your setup has it, otherwise the closest equivalent code-review agent or skill available.

Pass the agent a clear description of what changed and why, plus `git diff` output.

Focus the review on:
- Bugs and logic errors
- Security vulnerabilities
- Accessibility issues
- Project convention violations (check CLAUDE.md or AGENTS.md)

**If `--cross-model` flag is set:** ALSO dispatch a parallel review via Codex's native `review` subcommand. Codex catches a different class of issues than the layered Claude reviewer (different model = different blind spots). Run in the SAME message as the layered review, not after, so both run in parallel.

**Pin the reviewer model explicitly.** Don't rely on a bare model alias — it can silently resolve to a different tier or change routing under you. Check your installed Codex CLI's own docs/`--help` for how to pin a specific model and reasoning effort (typically `-c model=...` / `-c model_reasoning_effort=...`; exact flags and accepted values vary by CLI version — verify rather than assume). Tier by stakes: a stronger model and higher reasoning effort for billing/auth/schema/security/multi-system changes (the mandatory cross-model class); a lighter pin for routine second opinions.

```bash
codex review --uncommitted -c model=<your pinned model> -c model_reasoning_effort=<tier for these stakes> "<context paragraph: what changed and why, including specific things to weigh>"
```

For post-commit pipelines (most common), use `--base` instead. Check `codex review --help` on your installed version for whether `--base` can be combined with a `[PROMPT]` argument — this has changed across CLI versions; if it can't, rely on the model pin + the diff and put review emphasis in the layered reviewer's prompt:

```bash
codex review --base "$BASE" -c model=<your pinned model> -c model_reasoning_effort=<tier for these stakes>
```

With `--uncommitted`, the `[PROMPT]` argument carries the same context paragraph you give the layered reviewer — model-specific instruction tuning ("things I want you to find that our primary reviewer might miss") improves cross-model differentiation. Codex returns its findings to stdout. Capture and consolidate with the layered findings in Step 3.

**Do not use** the `codex:codex-rescue` subagent for this — `codex review` is the native, direct path. The rescue subagent is for substantial coding handoffs, not pre-merge review.

### Step 3: Fix Issues

Consolidate findings from the layered reviewer AND (if `--cross-model`) the codex review. Deduplicate convergent catches; preserve unique catches from either reviewer.

For each issue found:

| Confidence | Action |
|------------|--------|
| 90-100 (Critical) | **Must fix** before proceeding |
| 80-89 (Important) | **Fix** unless it's a pre-existing pattern or out of scope |
| < 80 (Minor) | **Skip** — note in PR description if relevant |

After fixing, re-run the build to verify fixes don't break anything.

**If the review found 0 critical/important issues:** Skip to Step 4.

**In the PR description**, when `--cross-model` was used, note which findings came from each reviewer (especially unique catches from Codex — they demonstrate the cross-model value).

### Step 4: Commit

If there are uncommitted changes, commit them:

```bash
git add <specific files>
git commit -m "<conventional commit message>

<host agent's co-author trailer, if it uses one — e.g. Co-Authored-By: Claude <noreply@anthropic.com>>"
```

Follow the project's commit conventions (check CLAUDE.md or AGENTS.md). Use conventional commits by default. Any co-author trailer should match the current model identity — check the conversation's environment block for the model name and ID.

### Step 5: Push

Push BEFORE creating the PR. `gh pr create` builds the PR from the remote tip, so an unpushed commit ships a partial PR that stays green all the way through merge.

```bash
git push -u "$PUSH_REMOTE" <branch-name>
```

### Step 6: Create PR

Target the merge target detected in Prerequisites (or `--base`), never a hard-coded branch — a default-base PR can land straight on production.

```bash
gh pr create --base "$BASE" --title "<conventional commit title>" --body "$(cat <<'EOF'
## Summary
<2-4 bullet points describing what changed>

## Code Review
<Brief summary of review findings and fixes applied>

## Test plan
- [ ] <verification steps>

<host agent's standard attribution trailer, if it has one — e.g. Claude Code's
"🤖 Generated with [Claude Code](https://claude.com/claude-code)"; Codex has its
own trailer or none. Omit this line entirely if the host doesn't use one.>
EOF
)"
```

**If the project uses milestones:** Add `--milestone "<milestone name>"` if you can determine the right one from context (check CLAUDE.md or AGENTS.md, issue references, or memory).

**If the PR closes an issue:** Include `Closes #<number>` in the body.

**Confirm the PR carries your commit:**

```bash
HEAD_SHA=$(git rev-parse HEAD)
[ "$(gh pr view <pr-number> --repo "$SLUG" --json headRefOid --jq .headRefOid)" = "$HEAD_SHA" ] || { echo "PR head != local HEAD — push again before going further"; exit 1; }
```

### Step 7: Merge

Confirm the required checks passed **for `$HEAD_SHA`**, not from the PR rollup, which mixes in runs from older commits:

```bash
# Required check set: UNION of ruleset-required and classic-protection-required
# checks — a branch can be gated by BOTH simultaneously (verified live against
# a real repo), so falling back to classic only when the ruleset list is empty
# misses checks the ruleset doesn't define. Read classic requirements off the
# "Get a branch" endpoint (`.protection.required_status_checks.contexts`), not
# the branch-protection-specific endpoint: the latter 404s ("Branch not
# protected") for a merely-unprotected branch and needs push access, while
# `GET /repos/{owner}/{repo}/branches/{branch}` needs only read access and
# returns a clean 200 (`{"enabled":false,...}`) instead — verified live
# against a real repo: `/branches/main/protection` 404'd on an unprotected
# branch where `/branches/main` returned 200 with the same information one
# level down. Still validate as a real JSON array before the union — an
# unexpected non-2xx response writes its error body to stdout even with --jq
# set, and skipping that validation corrupts REQUIRED with the literal error
# payload (confirmed: `jq` then hard-errors trying to add an array and that
# object).
RULESET_REQUIRED=$(gh api "repos/$SLUG/rules/branches/$BASE" \
  --jq '[.[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context] | unique' 2>/dev/null)
echo "$RULESET_REQUIRED" | jq -e 'type == "array"' >/dev/null 2>&1 || RULESET_REQUIRED='[]'

CLASSIC_REQUIRED=$(gh api "repos/$SLUG/branches/$BASE" \
  --jq '.protection.required_status_checks.contexts // []' 2>/dev/null)
echo "$CLASSIC_REQUIRED" | jq -e 'type == "array"' >/dev/null 2>&1 || CLASSIC_REQUIRED='[]'

REQUIRED=$(jq -c -n --argjson a "$RULESET_REQUIRED" --argjson b "$CLASSIC_REQUIRED" '($a + $b) | unique')
echo "Required checks on $BASE: $REQUIRED"

# Check Runs API, paginated — a single-page read can silently truncate a long list.
gh api --paginate "repos/$SLUG/commits/$HEAD_SHA/check-runs?per_page=100" \
  --jq '.check_runs[] | "\(.name): \(.status)/\(.conclusion)"'

# Legacy Statuses API — some CI still reports here, not Check Runs. Also
# paginated: this endpoint defaults to 30 per page (max 100 per GitHub's
# docs), so a commit with many contexts can silently truncate without it.
gh api --paginate "repos/$SLUG/commits/$HEAD_SHA/status?per_page=100" \
  --jq '.statuses[] | "\(.context): \(.state)"'
```

Cross-reference every name in `$REQUIRED` against both outputs: missing from both entirely counts as missing, not "not applicable" — a job killed by `timeout-minutes` reports `cancelled`, not `failure`, and looks benign unless you check for its absence explicitly. For Check Runs, `status` must be `completed` and `conclusion` must be `success`, `skipped`, or `neutral` — GitHub's protected-branches docs treat all three as passing ("Required status checks must have a successful, skipped, or neutral status before collaborators can make changes to a protected branch"). Treat `cancelled`, `timed_out`, `failure`, `action_required`, and `stale` as failures. For legacy Statuses, `state` must be `success`. Wait for pending checks to finish (the `pr-wait` skill in `release-ops` does this), then re-run both API calls above. Then merge, pinned to the commit you verified:

```bash
gh pr merge <pr-number> --repo "$SLUG" --squash --match-head-commit "$HEAD_SHA"
```

Use `--squash` by default (single clean commit). Never pass `--admin` or otherwise bypass branch protection unless the user explicitly asks for it on this PR.

**If `$BASE` requires a merge queue:** `gh pr merge` does not merge immediately — it enables auto-merge (checks not yet passed) or adds the PR to the queue (checks passed), per `gh pr merge --help`. Passing `--squash` here is safe even then: `gh` warns ("The merge strategy for `<base>` is set by the merge queue") and proceeds to enqueue using the queue's own configured strategy rather than erroring (verified against `cli/cli`'s `pkg/cmd/pr/merge/merge.go`: `canMerge()` returns immediately for a queue-required PR, and `merge()` only warns before setting `payload.auto = true`). Expect `state: OPEN` with a merge queued, not `MERGED`, until the queue processes it — don't treat that as a failed merge.

**Verify merge succeeded:**
```bash
gh pr view <pr-number> --repo "$SLUG" --json state,autoMergeRequest --jq '{state, autoMerge: (.autoMergeRequest != null)}'

# autoMergeRequest doesn't distinguish "queued" from "just enabled" — gh pr
# view --json has no field for merge-queue membership (confirmed: not in its
# supported-fields list), so query the PR's mergeQueueEntry directly via
# GraphQL. Verified live via introspection: PullRequest.mergeQueueEntry
# exists in GitHub's schema and returns null when the PR isn't queued.
gh api graphql -f query='
  query($owner:String!, $repo:String!, $num:Int!) {
    repository(owner:$owner, name:$repo) {
      pullRequest(number:$num) { state mergeQueueEntry { state position } }
    }
  }' -f owner="${SLUG%/*}" -f repo="${SLUG#*/}" -F num=<pr-number> \
  --jq '.data.repository.pullRequest'
```

Expected: `state: MERGED` (or, on a merge-queue base, `state: OPEN` with a non-null `mergeQueueEntry` — poll again; it clears to `null` and `state` flips to `MERGED` once the queue processes it).

### Step 8: Return to Base Branch

**If the pipeline was run inside a worktree** (Step 0 resolved a path argument):

1. `cd "$ORIGINAL_PWD"` — return to the caller's original working directory.
2. Do NOT run `git checkout "$BASE"` inside the worktree. The base branch is likely checked out in the primary working directory; `git checkout` in a worktree would fail with "already checked out" or leave the worktree on a now-deleted branch.
3. Recommend the `finishing-a-development-branch` skill for worktree cleanup, if your setup has it — otherwise clean up manually, but only once the PR is actually `MERGED`:
   ```bash
   if [ "$(gh pr view <pr-number> --repo "$SLUG" --json state --jq .state)" = MERGED ]; then
     git worktree remove <worktree-path>
     git branch -D <merged-branch-name>
   else
     echo "PR not MERGED yet (still queued/OPEN) — not deleting the branch."
   fi
   ```
   A merge-queue PR reads `state: OPEN` with a queued `mergeQueueEntry` until the queue processes it (Step 7). Deleting the branch at that point is destructive if the queue then fails or is removed — the branch would be unrecoverable with no merged commit to fall back on. Wait for the poll in Step 7 to confirm `MERGED` before running this cleanup.

**Otherwise** (pipeline ran in the current working directory):

```bash
git checkout "$BASE" && git pull
```

### Step 9: Report

Print a concise summary:

```
Pipeline complete:
- PR: <url>
- Status: Merged to $BASE
- Review: <N> issues found, <M> fixed
```

## Error Handling

| Error | Action |
|-------|--------|
| Build fails after fixes | Stop. Report failures. Don't push broken code. |
| Push rejected | Pull and rebase, then retry once. If still fails, report. |
| PR creation fails | Check if PR already exists for this branch. If so, update it. |
| Merge fails | Report the failure. Don't force-merge. |
| Required check failing, cancelled, or missing for `$HEAD_SHA` | Don't merge. Fix and re-push, or report the check as the blocker. |
| Not on a feature branch (currently on `$BASE` or `$PRODUCTION`) | Abort — create a feature branch first. |
| Worktree path argument does not exist | Abort with: "Path does not exist: <arg>" |
| Worktree path argument is not a registered worktree | Abort with: "Not a registered git worktree: <arg>. Run 'git worktree list' to see registered worktrees." |
| Post-merge `git checkout` fails inside a worktree | Expected — do not retry. Skip to worktree cleanup (Step 8). |

## Flags and Options

The user may pass flags after the skill invocation:

- `--base <branch>` — Override the detected merge target instead of relying on branch detection.
- `--no-prove` — Skip the full `prove-it` protocol in Step 1. The static-gate floor and the migration → `db-truth` Part B conditional still run. Use for docs-only changes or when an evidence table already exists this session.
- `--no-review` — Skip code review (Steps 2-3). Use when review was already done.
- `--no-merge` — Stop after PR creation (skip Steps 7-8). Use when you want CI to run first.
- `--rebase` — Use `--rebase` instead of `--squash` for merge.
- `--cross-model` — During Step 2, ALSO run Codex's native `codex review` in parallel for a different-model second opinion. Consolidate findings in Step 3. Worth the ~30-60s extra latency when the change touches anything load-bearing (schema, AI prompts, security gates, retry/error paths). Different models catch different classes of bugs.

## Common Mistakes

**Merging with failing build**
- Always build-check before AND after fixing review issues.

**Committing unrelated files**
- Stage specific files, not `git add -A`. Never commit `.env`, credentials, or large binaries.

**Generic PR titles**
- Use conventional commit format: `type(scope): description`. Match the project's conventions.

**Skipping the return to base**
- In the primary working directory: always checkout the merge target branch and pull after merge. Stale branches cause confusion.
- In a worktree: do NOT `git checkout` inside the worktree — return to the caller's original directory and recommend cleanup via `finishing-a-development-branch` if your setup has it, otherwise the manual steps in Step 8.
