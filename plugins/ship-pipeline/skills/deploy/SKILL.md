---
name: deploy
description: Promote the integration branch to production. Repo-agnostic — detects the repo's branch names, merge strategy, and release tooling from its own history, and defers to any repo-local runbook. Use when ready to push to production.
allowed-tools: Bash(git:*), Bash(gh:*), Bash(npm:*), Bash(npx:*), Bash(cargo:*), Bash(go:*), Bash(python3:*), Bash(python:*), Bash(jq:*), Bash(grep:*), Bash(sed:*), Bash(awk:*), Bash(comm:*), Bash(tr:*), Bash(sort:*), Bash(head:*), Bash(echo:*), Bash([ *)
---

# Deploy to Production (generic)

## Overview

Promote the **integration branch** (`$INTEGRATION` — where feature work lands, commonly `dev`) to the **release branch** (`$RELEASE` — what ships to production, commonly `main`) for a production deploy. This skill is **repo-agnostic**: it detects each project's conventions and runs the right steps, rather than assuming a specific host, versioning tool, database, or branch names. Steps marked **(CONDITIONAL)** only run when the repo actually has that machinery.

**Announce at start:** "Running production deploy."

## Step 0: Detect repo conventions — and defer to any repo-local runbook

**Do this first. Never assume.** A wrong assumption here (which branch is the release branch, squash vs merge, release-please vs none, which remote) corrupts every later step.

```bash
SLUG=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
REMOTE=$(git remote | grep -qx upstream && echo upstream || echo origin)   # primary remote
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
echo "repo=$SLUG remote=$REMOTE default=$DEFAULT_BRANCH"
# Anchor to remotes/$REMOTE/ specifically — an unanchored match also catches
# a local branch or another remote's same-named branch, which can point the
# rest of this skill at the wrong branch.
git branch -a | grep -oE "remotes/$REMOTE/(dev|develop|staging)$" | sed 's#.*/##' | sort -u
```

1. **Defer to a repo-local deploy runbook if one exists.** Check, in order: the project `CLAUDE.md`/`AGENTS.md` for a "Releasing"/"Deploy" section, a project-level `.claude/skills/deploy/` or `.agents/skills/deploy/`, `CONTRIBUTING.md`, `docs/DEPLOY*`/`RELEASING*`. **If the repo documents its own deploy process, follow THAT** — use this skill only for scaffolding it leaves unspecified, including which branch is `$RELEASE`. Some repos explicitly forbid generic deploy automation (e.g. a self-contained version-bump flow); honor that.

2. **Determine `$RELEASE`** — the branch that actually ships to production. This is the identical detection `review-merge-pipeline` uses for its own `$PRODUCTION`, so the two skills never disagree about which repos are two-trunk:
   - If the runbook above names a release branch, use that.
   - Otherwise, if `$DEFAULT_BRANCH` itself matches `dev`/`develop`/`staging` — ask the user which branch actually ships; don't assume `$DEFAULT_BRANCH` is production. Gate on `$DEFAULT_BRANCH`'s own name only, not on whether the candidate listing below is non-empty — a stray `dev`-shaped branch elsewhere in the repo isn't evidence about what `$DEFAULT_BRANCH` is. This is also the case that matters most to catch: a repo whose default branch **is** `dev` (a dev→main promotion flow) must not fall through to "usually `$DEFAULT_BRANCH`" and get misread as single-trunk — that skips the whole promotion this skill exists to run.
   - Otherwise, `$RELEASE = $DEFAULT_BRANCH`.

3. **Determine `$INTEGRATION`** — the branch feature work merges into before release, commonly `dev`/`develop`/`staging`. If the branch listing above (anchored to `remotes/$REMOTE/`) found exactly one candidate that differs from `$RELEASE`, that's `$INTEGRATION`. **If it found more than one candidate** (e.g. both `dev` and `staging` exist on `$REMOTE`), STOP and ask the user which one is the real integration branch — don't guess between them.

   If the repo has **no separate integration branch** (deploys straight from `$RELEASE`, or uses `release/*`), there is nothing for this skill to promote — report that and stop; don't force an integration→release flow. (This is the same condition `ship-issues` Phase 5 checks before deciding whether to call this skill at all — a single-trunk repo skips straight to its post-deploy validation phase instead.) If either branch can't be determined from repo conventions or a runbook, **ask the user** rather than guessing, then set them explicitly:
   ```bash
   INTEGRATION=<detected or user-provided>
   RELEASE=<detected or user-provided>
   ```
   Every command below uses `$INTEGRATION`/`$RELEASE` — substitute the real values you detected.

   **Before the first push this session into `$INTEGRATION`** (Step 1.5 or Step 10 below), confirm the branch by name against either a repo-local runbook or the user — a regex match alone is not enough authority to push into a branch other automation may depend on.

4. **Detect post-deploy machinery** so you know which conditional steps apply:
   - **Versioning:** release-please (`release-please-config.json` / `.release-please-manifest.json`) · a version-bump GH workflow (`.github/workflows/*version*`, often committing `VERSION`/manifests with `[skip ci]`) · manual `VERSION` · none.
   - **Merge strategy:** release-please and other title-driven changelogs **require `--squash`** (the PR title becomes the changelog commit). Repos that keep `$RELEASE`/`$INTEGRATION` aligned via merge commits use `--merge`. Match the repo's existing history (`git log $REMOTE/$RELEASE --merges --oneline | head`); if unknown, default to `--squash`.
   - **DB migrations (CONDITIONAL):** `supabase/migrations/`, `prisma/migrations/`, `migrations/`, etc. Also determine whether migrations **auto-apply on promotion** — a Supabase GitHub integration, a CI hook, or similar triggered by the merge to `$RELEASE` — versus requiring the separate manual apply in Step 8.5. Check a repo-local runbook for this explicitly. If migrations auto-apply on the promotion merge, the merge itself is the risky mutation, not a later step — see the gate in Step 6.5.
   - **Publish targets (CONDITIONAL):** npm (`package.json` + a publish workflow), a VS Code extension (`vscode/package.json`), Docker, GitHub Release, etc.
   - **Host:** Render/Vercel/Fly/etc. auto-deploy on `$RELEASE` push, or a manual deploy. Usually inferable from config; not required to proceed.

Record what you found — later steps reference it. Throughout this skill, substitute the real `$REMOTE`/`$SLUG`/`$INTEGRATION`/`$RELEASE` you detected.

## Step 1: Switch to the integration branch and sync remote refs

```bash
git checkout "$INTEGRATION" && git pull
# Fast-forward local $RELEASE to match the remote, so every later
# "$RELEASE..$INTEGRATION" ref compares against fresh upstream state (a stale
# local $RELEASE produces false-positive phantom-drift and wrong
# PREV_DEPLOY_BASE values).
git fetch "$REMOTE" "$RELEASE:$RELEASE"

# Push target: the remote $INTEGRATION actually tracks — not $REMOTE above,
# which deliberately prefers "upstream" for READS (the canonical source of
# truth for $RELEASE in a fork). Pushing to upstream by default breaks fork
# workflows: upstream is typically read-only for you. Verified: `git
# rev-parse --abbrev-ref --symbolic-full-name <branch>@{u}` works without
# checking that branch out, and fails cleanly (non-zero, no output) when no
# upstream is configured for it.
PUSH_REMOTE=$(git rev-parse --abbrev-ref --symbolic-full-name "$INTEGRATION@{u}" 2>/dev/null | sed 's#/.*##')
PUSH_REMOTE=${PUSH_REMOTE:-origin}
```

## Step 1.5: Back-sync async post-deploy artifacts (CONDITIONAL)

**Applies only if the repo's versioning lands commits on `$RELEASE` only** (a release-please release commit, a `[skip ci]` version/manifest bump, a changelog transform). These are async/manual and drift behind `$INTEGRATION` until the next deploy; if not synced, the next deploy hits a merge conflict on those files.

```bash
git fetch "$REMOTE" "$RELEASE"
git log "$INTEGRATION..$REMOTE/$RELEASE" --oneline --format="%s"
```

Classify what came back:

- **Only the repo's known version/changelog artifacts** (e.g. `chore(version):`/`chore($RELEASE): release`/changelog files) → back-merge them, taking the release branch's side on the generated files:
  ```bash
  git merge "$REMOTE/$RELEASE" --no-edit
  # On conflict, the ONLY expected paths are the generated version/changelog files; take theirs.
  git push "$PUSH_REMOTE" "$INTEGRATION"
  ```
- **Any other commit on `$RELEASE`** (a hotfix pushed direct to the release branch, an unexpected file) → **STOP and ask the user.** Do not auto-resolve. Recommended framing: if it's docs-only and `git merge --no-commit --no-ff "$REMOTE/$RELEASE"` is conflict-clean, the safest path is usually to back-merge it before continuing (otherwise every future deploy re-flags it); offer "skip" and "pause deploy" as secondary options.

**Repos with no release-only automation** (the version stamp is part of the squash, or there's no versioning) can skip this step.

## Step 2: Check what's being deployed (phantom-diff aware)

**File diff is necessary but NOT sufficient — also identify what's genuinely new.**

```bash
# All files differing between the release and integration branches (may include phantom diff).
git diff "$RELEASE..$INTEGRATION" --stat

# Integration-side commits genuinely NEW since the previous deploy's base.
# Filter out the repo's version/changelog automation commits (adjust the regex to
# the repo's convention), then take the most recent remaining first-parent commit
# on $RELEASE — that's the previous deploy.
PREV_DEPLOY_BASE=$(git log "$REMOTE/$RELEASE" --first-parent --format="%H %s" \
  | grep -vE 'chore\(version\)|chore\('"$RELEASE"'\): release|chore\(changelog\)' \
  | head -1 | awk '{print $1}')
echo "PREV_DEPLOY_BASE: $PREV_DEPLOY_BASE  (confirm this is your last deploy commit)"
git log "$PREV_DEPLOY_BASE..$INTEGRATION" --oneline --no-merges --first-parent
```

**Sanity-check the anchor.** If the first-parent list shows commits older than ~24h since the last deploy, `$RELEASE` HEAD is probably a non-deploy commit (a direct-push docs PR, a hotfix the filter missed). Override with the previous deploy PR's merge SHA:
```bash
PREV_DEPLOY_BASE=$(gh pr view <prev-deploy-pr> --repo "$SLUG" --json mergeCommit --jq '.mergeCommit.oid')
```

**PHANTOM DIFF WARNING.** A `--squash` deploy replaces N integration-branch commits with one new-SHA release commit, so the old commits' *content* is on `$RELEASE` but their *SHAs* aren't in `$RELEASE`'s ancestry. The next `git diff "$RELEASE..$INTEGRATION"` re-surfaces that content as if new (a one-bugfix deploy can show a 12,000-line diff). **Classify deploy size by the integration-side first-parent commit list, not the file diff.** Cross-reference:
- file diff tiny + commit list huge → phantom; trust the file diff.
- file diff huge + commit list tiny → trust the commit list; the PR title must describe only those commits (re-listing already-shipped features pollutes the changelog).
- both large → genuinely large; both small/zero → minimal/abort if zero.

(Merge-commit deploys, `--merge`, don't create this phantom — but the back-merge in Step 10 keeps `$RELEASE`/`$INTEGRATION` aligned regardless.)

If `git diff --stat` is empty, abort: "Nothing to deploy."

## Step 3: Build / test gate

Run the repo's gate — whatever its CI requires before merge:
```bash
npm run build        # or: cargo build · go build · python -m unittest discover · npm test · etc.
```
If it fails, abort. Do not deploy a broken build.

### Step 3.5: Pre-Deploy Verification — Version Gates & Realistic-Scale Perf

A green build and passing unit tests do NOT catch two classes of regression that only surface in production conditions. Check both before merging — a real incident needed a same-day emergency hotfix for each.

**(a) Version/compatibility gates must never point ahead of what THIS deploy ships.** Any "requires version ≥ X" constant — a client gating the API, a mobile companion gating the backend, a feature-flag minimum, an extension gating a CLI — must be **≤ the version this deploy actually stamps**. A gate set to a guessed/future version rejects the very artifact it ships beside, so every updated user hits a false "incompatible / please update" error that updating cannot fix.

```bash
# Surface min-version / compatibility constants touched since the last deploy.
git diff "$PREV_DEPLOY_BASE..$INTEGRATION" \
  -G'(MIN_|_MIN|minVersion|min_version|requires.{0,12}version|COMPAT)' \
  -- '*.ts' '*.tsx' '*.js' '*.py' '*.json' '*.go' '*.rs'
```

For each gate found, confirm it is `≤` the version going out now. If a gate is documented as "set at deploy time," **set it now** — do not ship the placeholder. Where practical, back it with a guard test (`gate ≤ repo version`) so the mistake fails CI, not users.

A real incident: a VS Code extension shipped `MIN_CLI_VERSION` one day ahead of the CLI it deployed beside (a gate dated one day past the CLI's own version); every updated user got a false "CLI version may be incompatible" warning, fixed only by a same-day patch hotfix. A `meetsMinVersion(<repo VERSION>, MIN_CLI_VERSION)` guard test now enforces the invariant. Principle is general: **never gate ahead of your own deploy.**

**(b) Perf-smoke against realistic-scale data, not a toy dataset.** O(n) regressions — N+1 queries, unbounded scans, per-item subprocess/RPC fan-out — are invisible on seed data and brutal in production. Before deploying anything that touches a hot path (a list/query/render that runs on load), time it against **production-scale volume**:

- Run a `performance-test` skill if the repo has one, or time the touched endpoint/query/command against a prod-sized fixture (not the dev seed).
- Specifically hunt for work that is O(rows × something): a per-row query, a per-record external call, a loop that re-scans, the same expensive read repeated per item instead of memoized once.

A real incident: a per-track git scan was O(branches) in subprocesses and called once per track; on a clone with hundreds of branches × dozens of tracks it turned a 12-second operation into ~16 minutes, hanging the client on every load. Unit tests and a small-repo smoke both passed — only realistic scale exposed it. The fix (batch + memoize) was easy; the **miss was not running a scale smoke before shipping.**

## Step 4: Determine commit type + PR title

The squash commit's title is what a title-driven changelog (release-please, a version-bump workflow) reads, and it's what users see as the release note. Make it real.

1. Scan integration-side commits since the last deploy for prefixes — bound by **time**, not the `$RELEASE..$INTEGRATION` range (which walks the integration branch's whole feature line):
   ```bash
   git log "$INTEGRATION" --first-parent --no-merges \
     --since="$(git log -1 --format=%cI "$PREV_DEPLOY_BASE")" --oneline
   ```
2. Pick the highest-priority conventional type present: `feat` > `fix` > `perf` > `refactor` > `chore`.
3. Collect scopes from commits that touch files actually in the diff.

**The title must describe what shipped** — `chore: deploy to production` produces an empty changelog. Good: `feat(graph,detail): blocked-by surfacing + dep chips`.

## Step 5: Create the deploy PR (integration → release)

```bash
gh pr create --base "$RELEASE" --head "$INTEGRATION" \
  --title "<type>(<scopes>): <2-3 key changes>" \
  --body "<summary + the genuinely-new commit list from Step 2>"
```
If the repo's versioning derives the changelog from the PR body (e.g. a version-bump workflow), write the body **as the changelog entry**.

## Step 6: Confirm checks for the exact head SHA

**Read check results for the exact head SHA, never the PR-level rollup** — the rollup mixes in runs from earlier commits pushed to the same PR.

```bash
HEAD_SHA=$(gh pr view <pr-number> --repo "$SLUG" --json headRefOid --jq .headRefOid)

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
RULESET_REQUIRED=$(gh api "repos/$SLUG/rules/branches/$RELEASE" \
  --jq '[.[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context] | unique' 2>/dev/null)
echo "$RULESET_REQUIRED" | jq -e 'type == "array"' >/dev/null 2>&1 || RULESET_REQUIRED='[]'

CLASSIC_REQUIRED=$(gh api "repos/$SLUG/branches/$RELEASE" \
  --jq '.protection.required_status_checks.contexts // []' 2>/dev/null)
echo "$CLASSIC_REQUIRED" | jq -e 'type == "array"' >/dev/null 2>&1 || CLASSIC_REQUIRED='[]'

REQUIRED=$(jq -c -n --argjson a "$RULESET_REQUIRED" --argjson b "$CLASSIC_REQUIRED" '($a + $b) | unique')
echo "Required checks on $RELEASE: $REQUIRED"

# Check Runs API, paginated — a single-page read can silently truncate a long list.
gh api --paginate "repos/$SLUG/commits/$HEAD_SHA/check-runs?per_page=100" \
  --jq '.check_runs[] | "\(.name): \(.status)/\(.conclusion)"'

# Legacy Statuses API — some CI still reports here, not Check Runs. Also
# paginated: this endpoint defaults to 30 per page (max 100 per GitHub's
# docs), so a commit with many contexts can silently truncate without it.
gh api --paginate "repos/$SLUG/commits/$HEAD_SHA/status?per_page=100" \
  --jq '.statuses[] | "\(.context): \(.state)"'
```

Wait for anything pending — `gh pr checks <pr-number> --repo "$SLUG" --watch` as a convenience wait, or the `pr-wait` skill in `release-ops` — then **re-run the two API calls above**; the watch rollup is not itself the merge gate.

Cross-reference every name in `$REQUIRED` against both outputs:
- Missing from both entirely → **treat as failure**, not "not applicable" (a job killed by `timeout-minutes` reports `cancelled`, not `failure`, and a required check that never ran looks benign unless you check for its absence explicitly).
- Check Runs: `status` must be `completed`, and `conclusion` must be `success`, `skipped`, or `neutral` — GitHub's protected-branches docs treat all three as passing ("Required status checks must have a successful, skipped, or neutral status before collaborators can make changes to a protected branch"). `cancelled`/`timed_out`/`failure`/`action_required`/`stale` → **treat as failure**.
- Legacy Statuses: `state` must be `success`.
- Anything else → stop, report, do not merge.

## Step 6.5: Migration backup gate (CONDITIONAL)

**If Step 0 found migrations auto-apply on this promotion**, run `backup-verify` and get a confirmed restorable backup **before** merging — the merge itself is the mutation here, not a later manual step, and it can't be undone by a PR revert once schema has changed. Do not proceed to Step 7 without this confirmation.

## Step 7: Merge

Merge pinned to the exact SHA you just verified in Step 6:
```bash
gh pr merge <pr-number> --repo "$SLUG" --squash --match-head-commit "$HEAD_SHA"   # title-driven changelog / release-please
# OR
gh pr merge <pr-number> --repo "$SLUG" --merge  --match-head-commit "$HEAD_SHA"   # repos that keep $RELEASE/$INTEGRATION aligned via merge commits
```
**Never pass `--admin`** unless the user has explicitly asked for it, in this session, for this specific PR. `--admin` bypasses branch protection and merge-queue requirements — it is not a default convenience for a solo/CI-gated workflow. If a required check is genuinely missing or failing, that's Step 6 telling you not to merge, not a reason to reach for `--admin`.

**If `$RELEASE` requires a merge queue:** `gh pr merge` does not merge immediately — it enables auto-merge (checks not yet passed) or adds the PR to the queue (checks passed), per `gh pr merge --help`. Passing `--squash`/`--merge` here is safe even then: `gh` warns ("The merge strategy for `<base>` is set by the merge queue") and proceeds to enqueue using the queue's own configured strategy rather than erroring or ignoring the request silently (verified against `cli/cli`'s `pkg/cmd/pr/merge/merge.go`: `canMerge()` returns immediately for a queue-required PR, and `merge()` only warns before setting `payload.auto = true`). The PR will read `OPEN` with a merge queued, not `MERGED`, until the queue processes it; Step 8 below accounts for this.

## Step 8: Verify merged

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
Expect `state: MERGED`. If `$RELEASE` requires a merge queue (Step 7), a fresh merge may instead read `state: OPEN` with a non-null `mergeQueueEntry` — poll again (it clears to `null` and `state` flips to `MERGED` once the queue processes it) before treating it as unmerged.

If the repo stamps version async (release-please PR, or a `version-bump` workflow firing on merge), wait for that commit to land on `$RELEASE` before publishing:
```bash
# Poll until the version/changelog commit appears, e.g.:
gh api "repos/$SLUG/commits/$RELEASE" --jq '.commit.message' | head -1
```

## Step 8.5: Post-deploy actions (CONDITIONAL — only what the repo has)

Run only the ones that apply (from Step 0):

- **DB migrations** — if the host auto-deploys code but not schema, apply pending migrations immediately after merge, **gated on a confirmed restorable `backup-verify` backup — not just user confirmation to proceed — and never auto-applied** (they can't be rolled back by a PR revert). Run `backup-verify` now if Step 6.5 didn't already produce a confirmed backup for this deploy:
  ```bash
  npx supabase db push        # or: npx prisma migrate deploy · etc.
  ```
  Report the migration status in the final summary either way (silence here has caused schema-cache outages).
- **Package/artifact publishes** — npm, VS Code extension, Docker, GitHub Release — via the repo's workflows (e.g. `gh workflow run npm-publish.yml --ref "$RELEASE" -f dry_run=false`). Mind same-day version collisions (date-derived versions may need a suffix; hand-set extension versions must be bumped per publish).
- **Back-merge the async version stamp** into `$INTEGRATION` (see Step 10) so the next deploy doesn't drift.

## Step 9: Close referenced issues (CONDITIONAL)

**The rule:** GitHub closes an issue linked with a closing keyword (`Closes`/`Fixes`/`Resolves #N`) when the PR merges into the repository's **default branch** — whichever branch that actually is, regardless of merge method (squash, merge commit, or rebase). A PR merged into any other branch has no effect on the issue.

That means `$DEFAULT_BRANCH` (from Step 0) decides where this already happened, not `$RELEASE`:
- **If `$INTEGRATION` is the default branch:** issues already closed when their PR merged into `$INTEGRATION`, long before this deploy — there is nothing to close here. Don't re-run closure logic against this promotion's PR list.
- **If `$RELEASE` is the default branch** (or the repo has no separate integration branch): this promotion's merge is what closes issues referenced in its own PR body. Manual closing is still usually needed for the underlying work, though — and for a reason that's easy to get backwards: `$INTEGRATION` PRs commonly DO carry `Fixes #N`, but because they merge into `$INTEGRATION`, not the default branch, GitHub's linker ignores the keyword outright ("If the pull request targets any other branch, then these keywords are ignored, no links are created, and merging the PR has no effect on the issues" — GitHub docs). It's not that the keyword is missing; it's that the branch it merged into never triggers it. Extract issue numbers from **integration-side work since the last deploy, bounded by TIME** (not a SHA range — the integration branch's first-parent line diverges from `$RELEASE` and over-reports):

```bash
[ -n "$PREV_DEPLOY_BASE" ] || { echo "PREV_DEPLOY_BASE is empty — Step 2's anchor detection failed (found no prior version/changelog commit and no override was set). STOP: don't run the time window below against an undefined base."; exit 1; }
T_PREV=$(git log -1 --format=%ct "$PREV_DEPLOY_BASE")   # epoch seconds — do NOT use %cI (local-offset string) compared against gh's Z-suffixed timestamps; "12:42" > "09:58" as strings even when 12:42Z is earlier
[ -n "$T_PREV" ] || { echo "T_PREV is empty — \$PREV_DEPLOY_BASE ($PREV_DEPLOY_BASE) didn't resolve to a real commit. STOP: an empty bound here breaks the jq filter below (it becomes 'fromdateiso8601) > )', a syntax error) rather than silently matching everything or nothing."; exit 1; }
gh pr list --repo "$SLUG" --base "$INTEGRATION" --state merged --limit 200 \
  --json number,title,body,mergedAt \
  --jq "[.[] | select((.mergedAt | fromdateiso8601) > $T_PREV)]" > /tmp/deploy-prs.json
```

Two-pass extraction — **only auto-close on an explicit closure directive at line start**; log the rest for review (bare contextual `#N` mentions have silently closed in-flight issues before):

```bash
CORPUS=$(jq -r '.[] | .title + "\n" + (.body // "")' /tmp/deploy-prs.json)
# -i: GitHub's closing keywords are case-insensitive ("The keywords can be
# followed by colons or in uppercase" — GitHub docs; `closes #10`, `Closes
# #10`, and `CLOSES #10` all link identically), so a case-sensitive grep
# silently drops lowercase-typed closures.
# GitHub's closing-keyword list is exactly these nine words — no "by" variant
# ("closed by #123" isn't a recognized closing syntax; verified against
# GitHub's docs) — so a rule with an optional "( by)?" segment matches text
# GitHub itself would never treat as a closure and risks a false-positive close.
CLOSURE_NUMS=$(echo "$CORPUS" \
  | grep -oiE '^[-*[:space:]]*(Close|Closes|Closed|Fix|Fixes|Fixed|Resolve|Resolves|Resolved):?[[:space:]]+#[0-9]+' \
  | grep -oE '#[0-9]+' | tr -d '#' | sort -u)
# Everything else: log for manual review, do NOT close.
# sort -u (lexical), not -n: `comm` compares both streams byte-for-byte in
# the order it received them and requires that to be lexical/collating
# order — feeding it numerically-sorted input breaks it whenever numeric and
# lexical order diverge (e.g. "10" sorts before "9" numerically but after it
# lexically). Verified: with `sort -n -u` on inputs {9,10,21} vs {10}, `comm
# -23` wrongly reports "10" as ALL-only even though it's in both files; with
# `sort -u` it correctly reports only {9,21}.
ALL_NUMS=$(echo "$CORPUS" | grep -oE '#[0-9]+' | tr -d '#' | sort -u)
comm -23 <(echo "$ALL_NUMS") <(echo "$CLOSURE_NUMS") | sed 's/^/  review: #/'
```

Close only genuinely open ISSUES — filter out PR numbers first. `gh issue view <N>` does **not** skip PR numbers: GitHub's Issue API treats a PR as an issue too, so `gh issue view <PR-number>` resolves successfully and returns that PR's own state (`OPEN` for an open PR), not an error (verified live: `gh issue view` on an open PR number returned `{"state":"OPEN"}`, exit 0 — the old state-only check would have closed it). Use the REST issues endpoint instead, whose `pull_request` field distinguishes a PR from a real issue:
```bash
for num in $CLOSURE_NUMS; do
  STATE=$(gh api "repos/$SLUG/issues/$num" --jq 'select(.pull_request == null) | .state' 2>/dev/null)
  [ "$STATE" = "open" ] \
    && gh issue close "$num" --repo "$SLUG" --comment "Shipped in #<deploy-pr>." --reason completed
done
```

## Step 10: Back-merge release → integration (align after the deploy)

A `--squash` deploy (or an async version stamp) leaves `$RELEASE` with commits `$INTEGRATION` lacks. Back-merge so future `git diff "$RELEASE..$INTEGRATION"` is clean and the next deploy's anchors stay correct:
```bash
git checkout "$INTEGRATION"
git fetch "$REMOTE" "$RELEASE"
git merge --no-ff "$REMOTE/$RELEASE" -m "chore(deploy): back-merge $RELEASE after #<deploy-pr>"
git push "$PUSH_REMOTE" "$INTEGRATION"
# Diff against $REMOTE/$RELEASE, NOT a bare $RELEASE. The fetch above (with
# no destination ref given) updates the remote-tracking ref $REMOTE/$RELEASE
# but does NOT update a same-named local branch, so a local $RELEASE left over from Step 1
# ("git fetch $REMOTE $RELEASE:$RELEASE") is stale by exactly this deploy's
# merge. Reproduced in scratch: after a squash-merge to the remote's release
# branch, diffing against the stale local $RELEASE re-showed the whole
# deploy's content as a false "real content, STOP" alarm, while diffing
# against the freshly-updated $REMOTE/$RELEASE was correctly empty.
git diff "$REMOTE/$RELEASE..$INTEGRATION" --stat   # should be empty / near-empty; if real content, STOP and investigate
```

## Step 11: Return to the integration branch

```bash
git checkout "$INTEGRATION" && git pull
```

## Step 12: Report

```
Deploy complete:
- Repo / PR: <slug> #<num> (<url>)
- Files changed: <count> (+<ins>/-<del>)
- Version: <stamped version, or "n/a">
- Publishes: <npm@x / extension vY / none>
- Migrations: <none / applied <list> / PENDING — user declined>
- Host: <auto-deploys from $RELEASE / manual>
```

Always state the migration and publish status explicitly — even "none."

## Flags

- `--dry-run` — show what would deploy without merging.
- `--force` — skip the build gate (emergency hotfix only).

## Error Handling

| Error | Action |
|-------|--------|
| No separate integration branch (single-trunk repo) | Report there's nothing to promote; stop. This is expected, not an error — the same condition `ship-issues` Phase 5 checks before calling this skill at all. |
| Multiple integration-branch candidates, or branch model otherwise unclear | STOP at Step 0; ask the user how they deploy. |
| Repo has its own deploy runbook | Follow it; use this skill only for gaps. |
| Build/test fails | Stop. Fix on the integration branch, retry. |
| Nothing to deploy | Abort. |
| Unexpected commit on `$RELEASE` (Step 1.5) | STOP and ask; don't auto-resolve. |
| Version gate ahead of deploy (Step 3.5a) | Fix the gate before merging; don't ship the placeholder. |
| Scale-perf regression (Step 3.5b) | Fix (batch/memoize/index) before merging; a hot path that's slow at scale is a production incident. |
| Required check missing/failing/cancelled for `$HEAD_SHA` (Step 6) | Don't merge. Fix and re-push, or report the check as the blocker. |
| Migrations auto-apply on promotion with no confirmed restorable backup (Step 6.5) | Don't merge. Run `backup-verify` first. |
| Pending migrations (Step 8.5) | Surface; wait for explicit confirmation; never auto-apply. |
| Publish version collision | Bump/suffix per the registry's rule; don't silently no-op. |
