# Ship Pipeline

Fourteen repo-agnostic skills for the ship half of the development loop — from reading the issue to promoting to production, with evidence at every gate.

Every skill detects the repository's own conventions rather than assuming a house style. The shipping-loop skills (`start-issue` through `ship-issues` in the table below) **defer to a repo-local version of themselves** when the project defines one (`.claude/skills/<name>/`), and `review-merge-pipeline` defers to a repo-local release runbook. Install it globally; override it per-repo where a project has stronger rules.

---

## The loop

| Phase | Skill | What it does |
|---|---|---|
| **Intake** | `start-issue` | Reads the full issue — body *and* comments, where scope changes hide. Checks whether the work already shipped, captures a baseline, branches off the detected integration branch. |
| **Ground** | `db-truth` | Verifies schema claims against the live database before you design against them, and confirms migrations actually landed after you apply them. |
| **Verify** | `prove-it` | End-of-work evidence protocol. Discovers what CI *actually* gates, runs both static gates, checks threaded values at their terminus, does one real round-trip, and emits a claim→command→result table. |
| **Inspect** | `review-slop` | Reports needless complexity, validation gaps, misleading test coverage, and prose problems with evidence and acceptance criteria. Makes no edits. |
| **Ship** | `review-merge-pipeline` | One shot: verify → review → fix → commit → push → PR → merge. Detects the merge target instead of assuming one. |
| **Promote** | `deploy` | Integration branch → production, with the repo's own merge strategy inferred from its history. |
| **Batch** | `ship-issues` | Carries a set of issues through the loop above in one run: grounds and groups them, reports status before any edit, then calls `start-issue`, `prove-it` and `review-merge-pipeline` per group. For a ship/deploy/release request it also runs `deploy` once for the whole batch and validates against production; for an "implement and merge" request it stops after the merges. |
| **Schema** | `db-migration-safety` | Expand-contract migrations, idempotent SQL, batched backfills. |
| **Schema** | `backup-verify` | Confirms backups exist **and actually restore** — into a scratch branch, with smoke queries and timestamped evidence. |
| **Build** | `api-design` | REST conventions for Next.js route handlers — resource naming, versioning, cursor pagination, one error envelope, Zod validation, and OpenAPI generated from Zod. |
| **Build** | `stripe-billing` | Stripe subscriptions in a Next.js app — Checkout, customer portal, signed and idempotent webhooks, proration, trials, and dunning. |
| **Build** | `analytics-instrumentation` | PostHog event taxonomy and instrumentation review — naming, flat properties, identify/reset/group, PII exclusion, and a starter dashboard set. |
| **Review** | `ux-review` | Reads screenshots (Playwright visual snapshots or any folder) and rates each against a UX checklist — layout, spacing, hierarchy, consistency, accessibility, mobile. Reports findings; files GitHub issues only when you ask. |
| **Output** | `cdf` | Prints a list of GitHub issues as one plain comma-separated line of numbers, nothing else. |

### Why `prove-it` is not "trust but verify"

Trust-but-verify presumes a claim is sound and spot-checks it. `prove-it` inverts the burden of proof: nothing is done until a command's output backs it, and anything unprovable is stamped `UNVERIFIED` rather than assumed fine. The premise is uncomfortable — features that passed build, typecheck, tests, review, *and* deploy, and were still dead in production, because no gate ever exercised a real write.

> An honest `UNVERIFIED` outranks a confident guess.

---

## Rule ownership

Each concern lives in exactly one skill. When a task crosses domains, the owner below keeps the rule and the others name only the handoff — this is what stops fourteen skills from firing on the same prompt.

| Skill | Owns |
|---|---|
| `start-issue` | Issue comprehension, prior-art checking, baseline capture, branch naming |
| `db-truth` | **Reading** schema truth — shape, relationships, permissions, and post-apply confirmation |
| `db-migration-safety` | **Writing** schema change — expand-contract sequencing, idempotency, backfills |
| `backup-verify` | Backup existence and restore-testing; the go/no-go before a risky mutation |
| `prove-it` | Evidence standards, gate discovery, the evidence table, `UNVERIFIED` labeling |
| `review-slop` | Report-only slop findings, severity calibration, and suggested repair criteria |
| `review-merge-pipeline` | Review orchestration, commit/push/PR mechanics, merge-target detection, head-SHA and required-check confirmation before merge |
| `deploy` | Production promotion, merge strategy, release-tooling compatibility |
| `api-design` | Route handler conventions — resource naming, versioning, pagination, the error envelope, Zod request/response validation, status codes, generated OpenAPI, and response scrubbing |
| `stripe-billing` | Subscription billing code — Checkout Sessions, customer portal, plan changes and proration, trials, dunning, and the signed, idempotent Stripe webhook handler |
| `analytics-instrumentation` | PostHog event taxonomy — `object_verb` naming, property schemas, identify/reset/group calls, PII exclusion, LLM usage events, and the starter dashboards |
| `ux-review` | Visual UX review of screenshots — the checklist, per-screenshot ratings and severities, and opt-in issue filing that follows the repo's own labels and templates |
| `cdf` | Output format for issue lists — one comma-separated line of numbers, nothing added |
| `ship-issues` | Batch orchestration — per-issue status, grouping into branches, consult-before-asking, post-deploy validation, the batch report. Owns no step the skills above own. |

`ux-review` judges what a screenshot shows; it is not a full accessibility audit. A screenshot cannot prove contrast ratios, focus order, or label associations, so it flags likely accessibility problems and leans on axe (when installed) to confirm them. `readiness-review` in the `hardening` pack can also report accessibility findings, but as one category of a code-level launch-readiness verdict, not from screenshots.

`stripe-billing` owns the Stripe webhook handler, including its signature check and idempotency. For webhook delivery in general, use `webhook-reliability` from the `hardening` pack. `api-design` owns route shape and error envelopes; `auth-hardening` (also in `hardening`) owns who may call a route.

The three database skills are the pairing most worth keeping straight: **`db-truth` reads, `db-migration-safety` writes, `backup-verify` is the safety net before either touches production.**

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install ship-pipeline@stylus-nexus
```

Plugin skills are namespaced: `/ship-pipeline:prove-it`, `/ship-pipeline:deploy`, and so on.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
```

In Codex, type `$` and a skill name to use it (`$ship-pipeline:prove-it`; Codex prefixes plugin skills with the pack name), or run `/skills` to pick one.

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins            # pick interactively
npx skills add stylusnexus/agent-plugins --skill analytics-instrumentation api-design backup-verify cdf db-migration-safety db-truth deploy prove-it review-merge-pipeline review-slop ship-issues start-issue stripe-billing ux-review  # this pack
```

The [Skills CLI](https://github.com/vercel-labs/skills) detects which agents you have installed and writes to each one's skills directory. Skills arrive un-namespaced here, so they invoke as `/prove-it` rather than `/ship-pipeline:prove-it`.

---

## Prerequisites

The skills shell out to standard tooling; install what your workflow touches:

- **`git`** and **`gh`** (authenticated via `gh auth login`) — issue intake, PR creation, merging
- **A typecheck and build command** — discovered from the repo, not assumed
- **Database CLI** *(only for the schema skills)* — `psql`, the Supabase CLI, or the Neon CLI, depending on your stack

## Safety notes

- `ship-issues` runs the whole loop for every issue you pass it, but "the whole loop" depends on how you ask: a ship/deploy/release request merges the batch AND deploys it to production; an "implement and merge" request stops after the merges and does not run `deploy` — though merged code may already be live if your host deploys from the branch it merged into. Either way it never bypasses a failing or missing required check.
- `review-merge-pipeline` merges pull requests. Read it before first use, and pass `--no-merge` to stop at PR creation while you get a feel for it.
- `deploy` promotes to production. It fast-forwards local refs and compares against fresh upstream state before acting.
- `backup-verify` and `db-migration-safety` are deliberately conservative: they print the affected scope before any destructive step.

## License

MIT © Stylus Nexus Holdings LLC — see the [repository LICENSE](../../LICENSE).
