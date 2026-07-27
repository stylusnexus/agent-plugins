---
name: debug-feedback-loop
disable-model-invocation: true
description: >
  Construct a fast, deterministic pass/fail signal for a bug BEFORE hypothesising —
  the missing mechanics behind "reproduce the bug". Offers a ladder of loop-construction
  techniques (failing test, curl/CLI harness, headless browser, trace replay, bisection,
  fuzz, differential), ranked falsifiable hypotheses, and tagged-instrumentation cleanup.
  Use when a bug is hard to reproduce, flaky/non-deterministic, lacks an obvious repro,
  or when getting a reliable signal is the bottleneck. Complements (does not replace)
  systematic-debugging, which owns root-cause discipline — reach for this when the hard
  part is getting a signal, not staying disciplined.
---

# Debug Feedback Loop

`systematic-debugging` owns the **discipline** — no fixes before root cause, one variable at
a time, question the architecture after 3 failed fixes. This skill owns the **mechanics** it
assumes: how to actually construct the fast, deterministic pass/fail signal that every later
phase consumes. Use them together — this is the "Reproduce" step done properly.

## The thesis

**The feedback loop is the work.** A fast, deterministic, agent-runnable pass/fail signal for
the bug is 90% of the fix — bisection, hypothesis-testing, and instrumentation all just consume
it. Without one, no amount of reading code will save you. Spend disproportionate effort here.
Be aggressive. Refuse to give up.

## 1. Build the loop — climb the ladder

Try these in roughly this order; stop at the first that gives a reliable signal.

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server (Next.js route, API handler).
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser** (Playwright) — drives the UI, asserts on DOM / console / network.
5. **Replay a captured trace.** Save a real request / payload / event log to disk; replay it
   through the code path in isolation. (PostHog event, HAR, webhook body.)
6. **Throwaway harness.** Spin up a minimal subset — one service, mocked deps — that hits the
   bug code path in a single function call.
7. **Property / fuzz loop.** For "sometimes wrong output": run 1000 random inputs, watch for it.
8. **Bisection harness.** If it appeared between two known states (commit, dataset, version),
   automate "boot at state X, check, repeat" so `git bisect run` can drive it.
9. **Differential loop.** Same input through old-vs-new (or two configs); diff the outputs.
10. **HITL bash script.** Last resort — if a human must click, drive *them* with a structured
    script so the loop still captures output that feeds back to you.

Build the right loop and the bug is 90% fixed.

## 2. Iterate on the loop itself

Treat the loop as a product. Once you have *a* loop:
- **Faster?** Cache setup, skip unrelated init, narrow scope. (A 2s deterministic loop is a
  superpower; a 30s flaky one is barely better than nothing.)
- **Sharper?** Assert on the specific symptom, not "didn't crash".
- **More deterministic?** Pin time, seed RNG, isolate filesystem, freeze network.

## 3. Non-deterministic bugs

The goal isn't a clean repro — it's a **higher reproduction rate**. Loop the trigger 100×,
parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable;
1% is not. Keep raising the rate until it's debuggable, then proceed.

## 4. Rank hypotheses against the loop

Once the loop reproduces the bug, generate **3–5 ranked hypotheses before testing any of them** —
single-hypothesis generation anchors on the first plausible idea. Each must be **falsifiable**:

> "If X is the cause, then changing Y makes the bug disappear / changing Z makes it worse."

If you can't state the prediction, it's a vibe — sharpen or discard it. **Show the ranked list
before testing** — domain knowledge often re-ranks instantly ("we just deployed #3"). Don't
block on it if the user is AFK; proceed with your ranking.

## 5. Instrument with tagged probes

Each probe maps to one prediction from §4. Change one variable at a time.
- Prefer **debugger / REPL** over logs — one breakpoint beats ten logs.
- **Tag every debug log** with a unique prefix, e.g. `[DBG-a4f2]`. Cleanup at the end is a
  single grep. Untagged probes survive into commits; tagged ones die.
- For **performance** regressions, logs lie — establish a baseline measurement (timing harness,
  `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## 6. Lock it down — or report the missing seam

Write the regression test **before the fix**, but only if a **correct seam** exists — one that
exercises the real bug pattern as it occurs at the call site. A too-shallow seam (single-caller
test for a multi-caller bug) gives false confidence.

**If no correct seam exists, that itself is the finding.** The architecture is preventing the
bug from being locked down — note it, fix at the best available seam, and route the structural
problem to an architecture review *after* the fix lands.

## When you genuinely can't build a loop

Stop and say so explicitly. List what you tried. Ask the user for one of: (a) access to an
environment that reproduces it, (b) a captured artifact (HAR, log dump, core dump, timestamped
screen recording), or (c) permission to add temporary production instrumentation. **Do not
hypothesise without a loop.**

## Fits with

- **systematic-debugging** — the discipline this plugs into; this is its "Reproduce" step.
- **verification-before-completion** — re-run the loop against the original (un-minimised)
  scenario before claiming the fix works; grep out every `[DBG-...]` probe.
- **test-driven-development** — for turning the minimised repro into a proper failing test.

---
<!-- Mechanics adapted from the loop-construction discipline in mattpocock/skills `diagnose`
     (MIT). Reframed as a companion to the superpowers systematic-debugging skill. -->
