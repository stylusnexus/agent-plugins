---
name: review-slop
description: "This skill scans a branch diff before opening a PR for needless casts, unsupported abstractions, missing validation, misleading tests, and prose tells. Requires evidence and behavior-based repair criteria. Report-only, never fixes. Repo-agnostic; defers to a repo-local review-slop when one exists. Triggers on /review-slop and phrases like 'check this for slop', 'scan before the PR', 'does this read like AI wrote it'."
---

# Review Slop

Scan a branch diff for **AI-slop** — patterns that compile, pass lint, and read
plausibly, but leave the codebase worse. Include correctness gaps concealed by
plausible code or weak tests; passing checks do not establish every contract.

**Report-only. Never fix, unstage, or modify anything.** The value is a list a
human decides on. A scanner that also edits turns a review into a diff you now
have to review.

**If the current repo has its own `.claude/skills/review-slop/` or
`.agents/skills/review-slop/`, that version is authoritative — follow it
instead.** A repo-local version knows its own compliance rules, voice, and
known-broken patterns; this one only knows what holds everywhere.

## Step 1: get the diff

```sh
git status --short
git diff <integration-ref>...HEAD --stat
git diff <integration-ref>...HEAD
```

Discover the integration branch rather than assuming it — `main`, `master` and
`dev` are all common, and diffing from the wrong one either floods the report
with already-merged work or hides half the change. Resolve `<integration-ref>`
to a real local or remote-tracking ref before running the commands. Prefer the
PR's actual base when available. Fetch only when permitted; record when the
comparison uses an unrefreshed local ref.

Three-dot syntax compares the merge base of the integration ref and HEAD with
HEAD. Record both refs and their commit IDs so the scan has a reproducible scope.
It excludes staged, unstaged, and untracked changes. Report those exclusions;
inspect them separately only when requested. Never switch branches to review.

If the requested diff is empty, report **no changes scanned**, not a clean verdict.

## Evidence gate

Treat matches as candidates. Trace source, validation, callers, and tests before
reporting. Distinguish introduced problems from existing debt; deduplicate
shared causes. Mark unresolved contracts as questions, not confirmed findings.

Broad boundary types and runtime guards may be necessary. Check whether internal
types preserve validated information. Flag widening followed by unchecked casts,
or typed external input with no runtime validation.

## Step 2: route each file

Run the checks that apply. A file can match more than one.

| files | checks |
|---|---|
| `.ts` `.tsx` `.js` `.jsx` `.py` `.go` `.rs` | code |
| `.md` `.mdx` and other prose | prose |
| migrations, schema files | migration |

## Code checks

Assign severity by demonstrated impact: CRITICAL for exposure, data loss, or
bypassed safety boundaries; HIGH for substantive contract or maintenance problems;
WARNING for style and minor cleanup. A missing explanation alone is not CRITICAL.

**Type safety and exposure:**

1. A cast to `any` / `unknown` / `interface{}` where a concrete type is
   discoverable in-file or one import away.
2. A suppressed type error (`@ts-ignore`, `@ts-expect-error`, `# type: ignore`,
   `//nolint`) with no comment saying why.
3. A linter disabled inline with no explanation.
4. Removed code left as commented-out blocks — 3+ consecutive commented lines.
5. A privileged credential or admin client reachable from a code path that runs
   on the client.

**Unnecessary complexity:**

6. `try`/`catch` around operations proven not to throw. Inspect callees and
   language semantics: getters, proxies, and nominally pure computations can
   throw. A result-returning parser needs no catch only if its contract says so.
7. **Ghost abstraction**: a new function, component or class used in exactly one
   place that adds indirection without a useful contract or readability benefit.
   Single use alone is insufficient. For deduplication claims, identify removed
   duplication; preserve meaningful differences. Security and dependency boundaries
   can justify abstractions without reuse.
8. Defensive null checks contradicted by an established runtime contract;
   a static declaration alone does not establish trust in external data.
9. Debug logging outside a logger utility.
10. A comment that restates the signature without adding meaning — `// gets the
    user by id` above `getUserById(id)`.
11. A `TODO` describing the current task rather than flagging a deferred
    decision. "TODO: add error handling for this PR" is a note to nobody.
12. A compatibility shim or flag comment ("remove once X ships") with no issue
    number and no removal condition — that is how shims become permanent.
13. Re-exports added where a direct import would do the same work.

**Minor cleanup candidates:**

14. Suspiciously balanced 3-item lists where the third item was clearly invented
    to reach three.
15. New exports with no repository consumers or documented public API purpose.
    Search beyond the diff, including registration, reflection, and entry points.
16. Duplicated schema or type definitions that could share one source.
17. Names that restate the type — `userObject: User`, `itemsArray: Item[]`.

## Prose checks

Treat prose patterns as WARNING by default. Cite a concrete clarity problem;
symmetry or word choice alone does not establish AI authorship or a defect.

18. Hyperbole with nothing behind it: "unleash", "revolutionise",
    "game-changing", "seamlessly", "effortlessly", "powerful" standing alone.
19. Filler openers — "Let's take a look at…", "In this guide we'll explore…".
20. Bullet lists where every line is near-identical in length and shape.
21. Passive voice where active is shorter and clearer.
22. Claims about unshipped behaviour stated in the present tense.

## Migration checks

23. Missing replay guards where the migration runner requires repeatability.
    Check repository conventions; versioned, once-only migrations need not use
    `IF NOT EXISTS`, which can conceal an unexpected existing schema.
24. A non-immutable function (`NOW()`, `random()`) inside an index predicate.
25. A new table with no row-level security or access grants, in a database that
    uses them.
26. A replaced function that drops properties the original declared — replacing
    a definition usually resets everything not restated.

## Verification checks

Inspect whether mocks replace the behavior claimed as tested. Recommend a failing
input and observable side effect for each missing guarantee, plus integration or
user-flow coverage where relevant. Passing lint is insufficient evidence.

Report verification gaps separately from proven defects. Do not run state-changing
flows, install lint tools, or change enforcement as part of this report-only scan.

## Output

Group by severity, most severe first. Per finding:

- **Severity** — CRITICAL / HIGH / WARNING
- **Location** — `path:line`
- **What** — the pattern, in one line
- **Why it matters** — the consequence, not the rule number
- **Suggested fix** — what to do, not applied
- **Evidence** — supporting contract and caller/test locations
- **Acceptance** — observable behavior and a check that could disprove it

Reject suggestions that merely relocate casts or suppress warnings. Prefer a
bounded repair; label architectural questions separately. For recurring failures,
suggest a targeted check with actionable diagnostics, not blanket enforcement.

Close with counts at each severity and any unresolved questions or verification
gaps. Use a clear verdict only when none remain; distinguish no confirmed findings
from a completed clean review.

For a completed clean review, **name what was scanned** — how many files, which
scopes, and which refs. List skipped checks or unavailable evidence explicitly.
Never use "clean" for an empty or incomplete scan.

## Source

Evidence and verification guidance adapted from Builder.io's
[How to De-Slop an AI-Generated Codebase](https://www.builder.io/blog/de-slop-ai-generated-codebase)
(September 16, 2026). Keep scans report-only; the article's repair workflow does
not authorize edits.
