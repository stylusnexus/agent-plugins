---
name: pr-wait
description: Wait for GitHub PR CI checks to complete, then optionally merge
color: blue
---

# Wait for PR Checks

Monitor GitHub PR CI checks and wait for them to complete. Optionally auto-merge when all checks pass.

## Usage

```bash
/pr-wait <pr_number> [auto_merge] [max_wait_minutes] [check_interval]
```

## Arguments

- **pr_number** (required): GitHub PR number to monitor
- **auto_merge** (optional, default: false): Set to "true" to auto-merge after checks pass
- **max_wait_minutes** (optional, default: 20): Maximum time to wait in minutes
- **check_interval** (optional, default: 60): Seconds between status checks

## Examples

```bash
# Monitor PR #172 (manual merge)
/pr-wait 172

# Monitor and auto-merge PR #172
/pr-wait 172 true

# Wait up to 30 minutes, check every 90 seconds
/pr-wait 172 false 30 90

# Auto-merge with custom timing
/pr-wait 172 true 15 45
```

## Behavior

1. **Initial Status**: Shows current state of all CI checks
2. **Polling**: Periodically checks status at specified interval
3. **Progress Updates**: Shows which checks are still running
4. **Completion**:
   - If `auto_merge=false`: Reports final status and exits
   - If `auto_merge=true`: Merges PR and optionally deletes branch
5. **Timeout**: If checks don't complete within max_wait_minutes, reports status and exits

## Implementation

### Step 0: Handle --help flag

**FIRST**: Check if the first argument is `--help`, `-h`, or `help`. If so, display usage and exit:

```
pr-wait - Monitor GitHub PR CI checks and optionally auto-merge

Usage:
  /pr-wait <pr_number> [auto_merge] [max_wait_minutes] [check_interval]
  /pr-wait --help

Arguments:
  pr_number         GitHub PR number to monitor (required)
  auto_merge        Auto-merge after checks pass: true|false (default: false)
  max_wait_minutes  Maximum wait time in minutes (default: 20)
  check_interval    Seconds between status checks (default: 60)

Examples:
  # Monitor PR (manual merge)
  /pr-wait 123

  # Monitor and auto-merge
  /pr-wait 123 true

  # Custom timing: 30 min max, check every 90s
  /pr-wait 123 false 30 90

  # Auto-merge with custom timing
  /pr-wait 123 true 15 45

Features:
  ⏱️  Configurable check interval (default: 60s)
  ⏰ Timeout protection (default: 20 minutes)
  🤖 Auto-merge option (squash + delete branch)
  📊 Real-time progress with timestamps
  ✅ Success validation (won't merge if checks fail)
```

Then **exit immediately** without running any checks.

### Step 1: Validate and parse arguments

Validate that pr_number is provided and is numeric.

### Step 2-8: Monitor and merge

1. Record the commit being checked: `gh pr view <pr_number> --json state,headRefOid` (exit with a clear error if the PR doesn't exist or isn't `OPEN`).
2. Read check state with `gh pr checks <pr_number> --json name,state,bucket`. `bucket` is one of `pass`, `fail`, `pending`, `skipping`, `cancel` (per `gh pr checks --help`). Do **not** read `gh pr view --json statusCheckRollup` and test `status`: legacy commit-status entries (`StatusContext`) carry only `state` and return `status: null`, so they look pending forever.
3. `gh pr checks` exits with code `8` while checks are pending (documented in `gh pr checks --help`). That is "still running", not a failure — don't abort the poll on it.
4. Poll at the specified interval using `sleep <check_interval>`
5. Calculate timeout based on `max_wait_minutes * 60 / check_interval` iterations
6. Show progress with timestamps and the names of checks whose `bucket` is `pending`
7. When no check is `pending`:
   - Show final status per check
   - **Passed** = every check is `pass` or `skipping`. Any `fail` or `cancel` = failed.
   - If `auto_merge=true` and all checks passed:
     - Run `gh pr merge <pr_number> --squash --delete-branch --match-head-commit <headRefOid>` — `--match-head-commit` makes `gh` refuse the merge if someone pushed after the checks you watched ran.
     - Confirm with `gh pr view <pr_number> --json state --jq .state` → `MERGED`
8. Handle edge cases:
   - PR doesn't exist or isn't open
   - No CI checks configured: report it and **never auto-merge** a PR with zero checks — ask the user
   - Checks fail or are cancelled
   - Timeout reached

## Output Format

```
Monitoring PR #172 CI checks...
Check interval: 60s | Max wait: 20 minutes | Auto-merge: enabled

=== Initial Status ===
✅ Build and Test: pass
⏳ E2E Tests: pending
⏳ Lighthouse CI: pending

[1] 09:50:00 - 2 checks still running:
  ⏳ E2E Tests
  ⏳ Lighthouse CI

[2] 09:51:00 - 1 check still running:
  ⏳ Lighthouse CI

[3] 09:52:00 - All checks complete!

=== Final Status ===
✅ Build and Test: pass
✅ E2E Tests: pass
✅ Lighthouse CI: pass

🎉 All checks passed! Merging PR #172...
✅ PR #172 merged and branch deleted successfully!
```

## Error Handling

- **PR not found**: Exit with clear error message
- **Checks failed**: Show which checks failed, do NOT merge
- **Timeout**: Show current status, exit without merging
- **Merge conflict**: Show error, suggest resolution steps
- **Head moved / merge refused by `--match-head-commit`**: report the `gh` error and re-run `/pr-wait` on the new head instead of merging
- **Branch protection blocks the merge**: report it. Never retry with `--admin` to get past failing or pending checks

## Common mistakes

- Reading `statusCheckRollup` and checking only `status` — commit-status entries have `state`, not `status`, so they look permanently pending. Use `bucket` from `gh pr checks --json`.
- Treating exit code `8` from `gh pr checks` as a failure.
- Merging without `--match-head-commit`, which can merge a commit whose checks never ran.
- Auto-merging a PR that has zero checks.
