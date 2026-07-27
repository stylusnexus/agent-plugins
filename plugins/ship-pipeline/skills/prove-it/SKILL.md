---
name: prove-it
description: End-of-work evidence protocol that proves a feature WORKS, not that checks pass. Repo-agnostic — discovers what CI actually gates (often far less than a green check implies), runs both static gates, targeted tests, terminus checks for threaded values, one real persistence round-trip, and render-surface verification, then emits a claim→command→result evidence table. Defers to a repo-local prove-it skill when one exists. Use before declaring any feature done and before shipping.
---

# Prove It — evidence before "done" (repo-agnostic)

## Overview

Features have passed build + typecheck + tests + review + deploy and still been **dead in production**, because no gate ever exercised the real write. Green checks measure what the checks measure — this skill measures whether the feature works. It ends in a table where every claim carries the command that proves it.

**If the current repo has its own `.claude/skills/prove-it/`, that version is authoritative — follow it instead.** This global version is the fallback.

**Announce at start:** "Running /prove-it verification."

**The rule underneath every step**: a claim without a command is labeled `UNVERIFIED` in the final table. An honest UNVERIFIED outranks a confident guess.

## Step 0: Discover what CI actually gates

Read the repo's CI workflows once (`.github/workflows/`). Many repos gate far less than their green checks imply — lint-only PR gates are common, and some builds skip type-checking (`ignoreBuildErrors`). Everything CI does NOT run, you run locally.

## Step 1: Both static gates

Run the typecheck AND the build — neither substitutes for the other (builds catch bundler/route/import errors types miss; typecheck catches what a lenient build ignores). If the repo tracks a baseline error count, compare against it and state both numbers.

## Step 2: Targeted tests, honestly run

- New behavior must have a test that **fails without the change**. Name it. If you can't articulate which test that is, the behavior is untested.
- Server-only code runs in a node test environment, not the jsdom default.
- DB-writing tests: confirm which env file the runner loads before letting them write anywhere.
- Never adapt production code to satisfy a mock; fix the mock. Mocks must respect schema invariants.
- Multi-case harnesses: verify exit-code honesty — a failing case must fail the run.

## Step 3: Terminus check for threaded values

List every value the change threads through ≥2 hops (UI → state → route → service → DB, or config → orchestrator → downstream call). For each, point to the test **at the terminus** proving arrival. Threaded values survive every intermediate hop's review and die unobserved — this is a recurring silent-drop bug class.

## Step 4: One real round-trip

If the feature persists anything: perform ONE real write **through the production entry path** (the API route / orchestrator — not a direct service call, which bypasses routing, budgeting, and error handling) against a local stack, then read it back and show the result.

## Step 5: Render-surface proof

For anything user-facing: load the **actual route** in a browser or a quick E2E spec — a component file existing is not proof it renders. Verify the route, the mode, and reachability; check the console. If the feature has multiple creation/entry surfaces that don't share code, verify each. Repeatable click-paths get formalized as a script; ad-hoc clicking is one-off sanity only.

## Step 6: Money audit (metered/billed paths only)

If the change touches a path that charges, meters, or debits: enumerate EVERY early return after the charge point — each must refund/rollback, each with a dedicated test. Loops that gained side effects: state why concurrent invocation is safe (queues are usually at-least-once).

## Step 7: Emit the evidence table

The table is the deliverable:

```text
| # | Claim                        | Command / location             | Result        |
|---|------------------------------|--------------------------------|---------------|
| 1 | Types clean (baseline N→N)   | <typecheck cmd>                | PASS          |
| 2 | Build passes                 | <build cmd>                    | PASS          |
| 3 | New behavior tested          | <test file> (fails w/o change) | PASS          |
| 4 | Value reaches terminus       | <query / test>                 | PASS          |
| 5 | Renders at <route>           | browser / e2e + console clean  | PASS          |
| 6 | <anything unprovable>        | —                              | UNVERIFIED: … |
```

UNVERIFIED rows get one line of why and what it would take. Never promote UNVERIFIED to PASS by rewording.

## Stop conditions

- A verification fails twice after a reasonable fix → stop, report commands + output + best hypothesis. Don't loop a third time; don't weaken the check to pass it.
- Verification reveals the feature works differently than specified → surface before shipping.
- A step can't run (no local stack, no browser) → mark UNVERIFIED, don't simulate it.
