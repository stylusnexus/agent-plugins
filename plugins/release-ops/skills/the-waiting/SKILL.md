---
name: the-waiting
description: "Use while waiting on CI, a deploy, or a release run and you want to know how long is really left. Estimates each running job's finish from its own recent history, spots runs stuck behind a cancelled run that never stopped, and suggests a few small tasks for the meantime. Report-only; never cancels, reruns, or merges. Triggers on /the-waiting and phrases like 'how long is CI going to take', 'why is this still pending', 'what's the hold-up', 'the waiting is the hardest part'."
---

# The Waiting

Tell the person what they are waiting on, how long it will really take, and
whether it is actually moving. Then give them something small to do meanwhile.

**Report-only. Never cancel, rerun, force-cancel, approve, or merge anything.**
Name the command that would fix a stuck run; the person decides whether to run it.
`pr-wait` owns blocking on checks and merging on green. This skill owns the
explanation.

**If the current repo has its own `.claude/skills/the-waiting/` or
`.agents/skills/the-waiting/`, that version is authoritative — follow it
instead.**

Requires `gh`, authenticated for the repository.

## Step 1: find what is being waited on

Take the argument if one is given: a PR number, a run ID, or a branch. With no
argument, use the current branch's PR (`gh pr view --json number,headRefOid`); with
no PR, the latest runs for the current branch.

Read status for the **exact head commit**, never the PR-level rollup, which mixes
check runs from earlier commits:

```sh
gh api "repos/{owner}/{repo}/commits/<sha>/check-runs?per_page=100"
gh api "repos/{owner}/{repo}/actions/runs?head_sha=<sha>"
```

If nothing is queued or running, say so and stop. Report what finished, with
conclusions. Treat `cancelled` and `timed_out` as failures, not as benign states.

## Step 2: estimate each running job

For each job still `queued` or `in_progress`:

1. Find its workflow and job name.
2. Pull the same job's durations from the last 10–20 **successful** runs of that
   workflow (`actions/runs?workflow_id=…&status=success`, then `…/jobs`).
3. Report elapsed, typical (median) and slow (p90), and the time left against
   the median.
4. If elapsed is past p90, say it is running long. If it is near the job's
   `timeout-minutes`, say when the timeout will end it.

Say how many past runs the estimate rests on. With fewer than five, say the
estimate is rough. A job whose duration depends on what changed (a path-filtered
or "changed files only" test lane) has two populations; say which one this run
is likely in, and why.

## Step 3: check that it is actually moving

Look for these, in this order:

| Sign | Likely cause | What to suggest |
|---|---|---|
| A run is `pending` with zero jobs, and an older run of the same workflow and branch is still `in_progress` | The old run was cancelled but a job gated on `if: always()` ignores cancellation, and it holds the concurrency slot | Force-cancel the old run: `gh api -X POST repos/{owner}/{repo}/actions/runs/<old-id>/force-cancel`. The lasting fix is `!cancelled()` in place of `always()` in job conditions. |
| A job is `queued` for minutes with no runner | No online runner matches its labels (self-hosted machine asleep, label typo), or the account's minutes are exhausted | Check `actions/runners`; check the billing budget. |
| Runs show `action_required` | A bot-opened PR, or a first-time contributor, needs approval before workflows run | Approve in the PR's Checks tab, or merge with the repository's bypass rules. |
| Everything is green, but the PR is still blocked | A required check never reported, often because a skipped job and a required job share a name | Compare the branch protection or ruleset's required contexts with the check runs for the head commit. |

Confirm each sign against the data before naming it. Say "not stuck" when
nothing matches; a slow job is not a stuck job.

## Step 4: one line of levity

Add one short, dry line in the spirit of a rock band stuck at sound check, about
this particular wait. Write a fresh line each time. Never quote song lyrics.
A title-length nod is the limit. Skip it entirely when the news is bad (a
failure, a stuck run the person must fix) or when they ask for no jokes.

Examples of the register, not lines to reuse:

- "The headliner is your test suite, and it's still tuning."
- "Roadies report the type checker is on its third encore."
- "Sound check's running long. Nobody touch the faders."

## Step 5: something to do meanwhile

Offer up to three things that fit inside the time left, each doable in under
five minutes, from the same repository:

- a PR waiting on the person's review (`gh pr list --search "review-requested:@me"`)
- one of their own open PRs with a failing or stale check
- a small open issue assigned to them

List them. Do not start them.

## Output

Lead with the answer:

```
Unit Tests (full suite): 23m elapsed, usually 31m (p90 36m, 12 runs) → ~8m left.
Type Check: done ✓.  Nothing stuck.
```

Then any stuck-run finding with its command, then the one line of levity, then
the meantime list. Keep the whole report under 15 lines.
