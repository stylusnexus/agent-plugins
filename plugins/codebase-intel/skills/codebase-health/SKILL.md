---
name: codebase-health
description: Use when onboarding to an unfamiliar codebase, before major refactors, during periodic health checks, or when diagnosing why code keeps breaking. Also use when assessing bus factor, churn hotspots, or development velocity on any git repository.
---

# Codebase Health

Diagnose where a codebase hurts using git history — before reading a single file. Based on [5 Git Commands Before Reading Code](https://piechowski.io/post/git-commands-before-reading-code/).

## Args

`--help` — Print use cases and flag reference instead of running diagnostic.
`--since <period>` — Lookback window (default: `1 year ago`). Accepts any `git log --since` format.
`--top <N>` — Number of results per category (default: 20).

## --help Output

When invoked with `--help`, display the following and stop:

```
codebase-health — Git archaeology for codebase diagnosis

USAGE
  /codebase-health              Run full diagnostic on current repo
  /codebase-health --help       Show this help
  /codebase-health --since "6 months ago" --top 10

USE CASES
  Onboarding        You just joined a project. Before reading code, find
                    where the pain is: what files churn most, who knows
                    what, and where bugs cluster.

  Pre-Refactor      Before touching a module, check if it's a hotspot
                    (high churn + bugs) or stable code you'll destabilize.

  Health Check      Periodic audit: is velocity trending down? Are hotfixes
                    increasing? Is bus factor getting worse?

  Incident Review   After an outage, check firefighting patterns — how
                    often do reverts/hotfixes happen in the affected area?

  Architecture      Before proposing structural changes, find the real
                    coupling points (files that always change together).

  Team Planning     Identify knowledge silos before someone leaves.
                    Redistribute ownership of high-risk files.

WHAT YOU GET
  1. Churn Hotspots     — Most-modified files (high churn = high risk)
  2. Bus Factor         — Knowledge concentration across contributors
  3. Bug Clusters       — Files with most fix/bug commits
  4. Velocity Trend     — Monthly commit counts over time
  5. Firefighting Index — Reverts, hotfixes, emergency commits
  6. Cross-Reference    — Files appearing in BOTH churn AND bugs (priority targets)

FLAGS
  --since <period>   Lookback window (default: "1 year ago")
  --top <N>          Results per category (default: 20)
```

## Running the Diagnostic

Parse `--since` (default `"1 year ago"`) and `--top` (default `20`) from args. Run all 5 commands in parallel via Bash, then cross-reference.

### 1. Churn Hotspots

```bash
git log --format=format: --name-only --since="$SINCE" | sort | uniq -c | sort -nr | head -$TOP
```

High-churn files signal code the team keeps revisiting — either actively developed or poorly factored.

### 2. Bus Factor

```bash
git log --format='%aN' --since="$SINCE" | sort | uniq -c | sort -nr | head -$TOP
```

Note: `git shortlog -sn` can fail silently in non-TTY shells (e.g., Claude Code). The `git log` variant is more reliable.

If top 1-2 contributors own >60% of commits, flag as bus factor risk.

### 3. Bug Clusters

```bash
git log -i -E --grep="fix|bug|broken|patch|regression" --name-only --format='' --since="$SINCE" | sort | uniq -c | sort -nr | head -$TOP
```

Files with concentrated bug-fix commits. Extended regex includes `patch` and `regression` beyond the original article.

### 4. Velocity Trend

```bash
git log --format='%ad' --date=format:'%Y-%m' --since="$SINCE" | sort | uniq -c
```

Monthly commit counts. Look for: sustained drops (attrition?), spikes before deadlines, seasonal patterns.

### 5. Firefighting Index

```bash
git log --oneline --since="$SINCE" | grep -ciE 'revert|hotfix|emergency|rollback|urgent'
```

Also get total commits for the ratio:

```bash
git log --oneline --since="$SINCE" | wc -l
```

Report as: "X of Y commits (Z%) are firefighting."

### 6. Cross-Reference (the key insight)

After collecting churn and bug data, find files appearing in **both** lists. These are priority targets — code that changes constantly AND attracts bugs.

## Report Format

Present results as a structured report:

```
## Codebase Health Report — [repo name]
Period: [since] to now | Top: [N] per category

### Priority Targets (churn + bugs)
Files appearing in both hotspot lists. These hurt the most.

### Churn Hotspots
[top N with counts]

### Bug Clusters
[top N with counts]

### Bus Factor
[contributor breakdown with ownership %]
Risk: LOW/MEDIUM/HIGH (based on top-2 concentration)

### Velocity Trend
[monthly counts, note any significant changes]

### Firefighting Index
X of Y commits (Z%) — LOW (<2%) / MODERATE (2-5%) / HIGH (>5%)
```

## Interpreting Results

| Signal | What It Means | Action |
|--------|--------------|--------|
| File in churn AND bugs | Highest-risk code | Refactor or add tests first |
| Top 2 own >60% commits | Bus factor risk | Pair program, spread ownership |
| Firefighting >5% | Deploy confidence low | Improve CI/CD, add integration tests |
| Velocity dropping 3+ months | Team health issue | Not a code problem — escalate |
| Config files in churn top 5 | Environment instability | Standardize configs |
| Test files in bug clusters | Test suite is the problem | Fix test infrastructure |

## Common Mistakes

- **Reading code first**: The whole point is to diagnose BEFORE reading. Run this first.
- **Ignoring cross-references**: Individual lists are interesting; the intersection is actionable.
- **Short timeframes on old repos**: 1 year is the sweet spot. 3 months misses patterns; 5 years dilutes signal.
- **Counting generated files**: Filter out `*.lock`, `*.generated.*`, `database.ts` etc. from churn if they dominate.
