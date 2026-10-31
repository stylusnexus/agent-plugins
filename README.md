# Stylus Nexus — Agent Plugins Marketplace

[![skills.sh](https://img.shields.io/badge/skills.sh-listed-black)](https://skills.sh/stylusnexus/agent-plugins)
[![npm](https://img.shields.io/npm/v/@stylusnexus/agent-plugins)](https://www.npmjs.com/package/@stylusnexus/agent-plugins)
[![npm downloads](https://img.shields.io/npm/dm/@stylusnexus/agent-plugins)](https://www.npmjs.com/package/@stylusnexus/agent-plugins)
[![CI](https://github.com/stylusnexus/agent-plugins/actions/workflows/ci.yml/badge.svg)](https://github.com/stylusnexus/agent-plugins/actions/workflows/ci.yml)
[![plugins](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fstylusnexus%2Fagent-plugins%2Fmain%2F.claude-plugin%2Fmarketplace.json&query=%24.plugins.length&label=plugins)](./.claude-plugin/marketplace.json)
[![GitHub stars](https://img.shields.io/github/stars/stylusnexus/agent-plugins)](https://github.com/stylusnexus/agent-plugins/stargazers)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-7C3AED)
![Codex](https://img.shields.io/badge/Codex-plugin-10A37F)

A plugin marketplace for AI coding agents — **11 plugins, 89 skills**. Installs natively into **Claude
Code** and **OpenAI Codex**, and installs into roughly 77 more agents' skill folders through the
Skills CLI. Documented skill support has been checked for only a few of those: Gemini CLI/Antigravity
CLI, Cursor, GitHub Copilot, Windsurf, opencode and Cline. See [Compatibility](#compatibility).

Most skills are repo-agnostic: they detect your repository's conventions rather than assuming their
own, and many defer to a repo-local version of themselves when your project defines one. api-design,
stripe-billing, auth-hardening and privacy-audit assume a Next.js/TypeScript stack.

**[Browse the catalogue →](https://stylusnexus.github.io/agent-plugins/)** — every pack, what it's for, and how to install it on your agent.

> ⚠️ **Trust before you install.** Plugins run code on your machine. Review a plugin's source before
> installing it. Everything here is open-source — links are in the table below.

> **Plugins ≠ one format.** Claude Code and Codex have *separate* plugin systems, so this repo carries
> a **per-host index**: `.claude-plugin/marketplace.json` (Claude) and `.agents/plugins/marketplace.json`
> (Codex). You add the *same* marketplace either way; each tool reads the schema it understands.

---

## Plugins

### Skill packs

Nine packs, grouped by the job rather than the technology. Each pack's README carries a
**rule-ownership table** so the skills inside it don't compete for the same trigger.

| Pack | # | What it's for | Skills |
|---|---|---|---|
| [**ship-pipeline**](./plugins/ship-pipeline) | 15 | The daily loop: read the issue, ground assumptions in the live database, prove it works, review, merge, promote — one issue or a batch. | `start-issue` `db-truth` `prove-it` `review-slop` `review-merge-pipeline` `deploy` `ship-issues` `db-migration-safety` `backup-verify` `api-design` `stripe-billing` `analytics-instrumentation` `feature-flags` `ux-review` `cdf` |
| [**reporting-comms**](./plugins/reporting-comms) | 7 | The last mile — turning agent output into something a person wants to read, and getting their judgment back. | `html` `visual-plan` `visual-recap` `recap-table` `writing-clearly-and-concisely` `human-writing` `redline` |
| [**second-opinion**](./plugins/second-opinion) | 6 | One premise: one confident answer is not evidence. Independent passes, arbitration and checks against the code; llm-council's advisors are the same model, and spec-review calls a different one. | `llm-council` `plan-arbiter` `spec-review` `agent-watchdog` `debug-feedback-loop` `efficient-frontier-routing` |
| [**hardening**](./plugins/hardening) | 12 | The unglamorous pre-launch gates — a missing rate limit, an unsigned webhook, a compromised dependency — one read-only launch-readiness verdict, design-time and agent-era audits, and draft legal documents for a lawyer to review. | `rate-limit-audit` `exposure-scan` `auth-hardening` `webhook-reliability` `privacy-audit` `readiness-review` `threat-model` `security-headers` `secrets-leak-audit` `agent-tooling-review` `llm-app-security` `legal-docs` |
| [**release-ops**](./plugins/release-ops) | 10 | Deciding the version, waiting on CI, publishing, keeping dependencies current, watching production, handling incidents and support tickets, and auditing model API spend. | `version-check` `pr-wait` `the-waiting` `npm-publish` `dependency-upgrade` `observability-setup` `incident-response` `customer-support-triage` `llm-cost-audit` `vscode-marketplace-publish` |
| [**product-strategy**](./plugins/product-strategy) | 15 | Deciding what to build and why — vision, strategy, value, objectives, roadmaps, discovery and pricing, taught as it goes. | `product-manager` `pm-vision` `pm-strategy` `pm-strategy-fit` `pm-canvas` `pm-value-proposition` `pm-objectives` `pm-roadmap` `pm-discovery` `pm-growth` `pm-market-analysis` `pm-capabilities` `pm-teams` `pm-visuals` `pricing-review` |
| [**go-to-market**](./plugins/go-to-market) | 12 | Getting a product noticed on a small team's hours — positioning, copy, launches, community, outreach, email and measurement. | `marketing-lead` `mk-positioning` `mk-audience` `mk-copy` `mk-brand-kit` `mk-search` `mk-launch` `mk-community` `mk-founder-content` `mk-outreach` `mk-lifecycle` `mk-measurement` |
| [**design-suite**](./plugins/design-suite) | 7 | Reviewing and shaping UI and UX work — flows and states, interface polish, art direction, accessibility against WCAG 2.2, dashboards, mobile, and information architecture. | `ui-ux` `interface-polish` `art-direction` `accessibility-review` `dashboard-design` `mobile-design` `information-architecture` |
| [**codebase-intel**](./plugins/codebase-intel) | 5 | Building an accurate picture of a codebase, and the libraries it leans on, before changing it. | `codebase-health` `codebase-architecture-scanner` `grill-with-docs` `read-the-damn-docs` `teach-code-to-mastery` |

#### Every skill, by pack

<!-- catalog:start -->
<details>
<summary><b>ship-pipeline</b> · 15 skills</summary>

| Skill | What it covers |
|---|---|
| `analytics-instrumentation` | PostHog event taxonomy — `object_verb` naming, property schemas, identify/reset/group calls, PII exclusion, LLM usage events, and the starter dashboards |
| `api-design` | Route handler conventions — resource naming, versioning, pagination, the error envelope, Zod request/response validation, status codes, generated OpenAPI, and response scrubbing |
| `backup-verify` | Backup existence and restore-testing; the go/no-go before a risky mutation |
| `cdf` | Output format for issue lists — one comma-separated line of numbers, nothing added |
| `db-migration-safety` | Writing schema change — expand-contract sequencing, idempotency, backfills |
| `db-truth` | Reading schema truth — shape, relationships, permissions, and post-apply confirmation |
| `deploy` | Production promotion, merge strategy, release-tooling compatibility, the frozen source commit, live-artifact match, smoke and rollback evidence, closing only issues proved shipped |
| `feature-flags` | Flag lifecycle — naming, rollout versus kill switch, rollout stages, kill-switch alerts, testing both paths, and stale-flag cleanup |
| `prove-it` | Evidence standards, gate discovery, the evidence table, `UNVERIFIED` labeling |
| `review-merge-pipeline` | Review orchestration, commit/push/PR mechanics, merge-target detection, evidence tied to the head commit, head-SHA, approval and required-check confirmation before merge |
| `review-slop` | Report-only slop findings, severity calibration, and suggested repair criteria |
| `ship-issues` | Batch orchestration — per-issue status, grouping into branches, consult-before-asking, post-deploy validation, the batch report. Owns no step the skills above own. |
| `start-issue` | Issue comprehension, prior-art checking, baseline capture, branch naming |
| `stripe-billing` | Subscription billing code — Checkout Sessions, customer portal, plan changes and proration, trials, dunning, and the signed, idempotent Stripe webhook handler |
| `ux-review` | Visual UX review of screenshots — the checklist, per-screenshot ratings and severities, and opt-in issue filing that follows the repo's own labels and templates |

[Pack README →](./plugins/ship-pipeline)

</details>

<details>
<summary><b>reporting-comms</b> · 7 skills</summary>

| Skill | What it covers |
|---|---|
| `html` | Output is complex enough that a wall of terminal text loses it — plans, code reviews, research, comparisons, configs, reports. Produces one self-contained, reading-first HTML file. |
| `human-writing` | Text reads as machine-generated: corporate speak, generic phrasing, the familiar AI cadence. Rewrites toward something conversational and specific. |
| `recap-table` | Someone asks "what did you change?" or wants a before/after comparison. Produces the table, not another paragraph. |
| `redline` | The human needs to judge a draft, plan, or report and describing the problems in chat is slower than fixing them. Opens it in a browser for direct editing and anchored comments; returns one Markdown review. |
| `visual-plan` | A text plan would land better as an interactive document: diagrams, file maps, annotated code, open questions, and UI review where it helps. |
| `visual-recap` | A PR, branch, commit, or diff needs explaining — renders it with diagrams, file maps, API and schema summaries, and annotated diffs. |
| `writing-clearly-and-concisely` | Any prose a human will read — docs, commit messages, error messages, explanations. Applies Strunk's rules and cuts what isn't carrying weight. |

[Pack README →](./plugins/reporting-comms)

</details>

<details>
<summary><b>second-opinion</b> · 6 skills</summary>

| Skill | What it covers |
|---|---|
| `agent-watchdog` | Another agent's work needs watching, auditing, comparing, or fixing, from a session ID or transcript. |
| `debug-feedback-loop` | A bug needs a fast, deterministic pass/fail signal before hypothesising about causes — the step most debugging skips. |
| `efficient-frontier-routing` | Any task in Claude Code or Codex where the model should match the work: small tasks stay local, routine work goes to cheaper subagents, and difficult decisions or risky reviews go to a stronger one. |
| `llm-council` | A question, idea, or decision is consequential enough to want five advisors analysing it independently before synthesis — rather than one answer delivered confidently. |
| `plan-arbiter` | Two or more plans are on the table and someone has to compare, cross-review, merge, judge, or arbitrate between them. Picks on reasoning, not on whichever was written last. |
| `spec-review` | A spec or requirements doc is drafted or about to be implemented. Verifies its claims against the real codebase — catching wrong data-model assumptions before code embeds them. |

[Pack README →](./plugins/second-opinion)

</details>

<details>
<summary><b>hardening</b> · 12 skills</summary>

| Skill | What it covers |
|---|---|
| `agent-tooling-review` | An MCP server, plugin, or token is being connected to an agent, or an agent will run unattended. Applies least privilege and a human gate on irreversible actions. |
| `auth-hardening` | Auth is in place and needs auditing — session and cookie configuration, CSRF, OAuth scopes, per-route protection. |
| `exposure-scan` | Periodically, and after any dependency change. Checks installed packages across npm, Go, PyPI, RubyGems, and MCP servers against threat-intelligence catalogs for known-compromised releases. |
| `legal-docs` | Drafting or reviewing Terms of Service, a Privacy Policy, a refund policy, or an acceptable use policy. Checks every claim against what the product actually does and marks every draft as not legal advice, for a lawyer to review. |
| `llm-app-security` | A feature sends untrusted content to a model or lets a model act. Maps input-to-sink paths, requires gates on output and actions, and proves them with a public adversarial corpus. |
| `privacy-audit` | User data is collected and someone needs to say exactly what and where. Produces the inventory and checks it against the code and infra — not against what the privacy policy claims. |
| `rate-limit-audit` | Before launch, or after adding an endpoint that calls a paid API (LLM, email, SMS) or handles auth. Inventories every such endpoint and checks each actually has a limit. |
| `readiness-review` | Before launch, or on a recurring schedule, to answer "is the code healthy and can a user actually do the core jobs?" in one report. Read-only: scans, a reviewer pass over a secret-free copy, a look-only walk of the live product, and a findings list you file yourself. |
| `secrets-leak-audit` | Before launch, or after a key shows up somewhere it should not. Checks git history, the production bundle, logs and error reports, and API responses. |
| `security-headers` | Before launch, or after a proxy or domain change. Captures the deployed response, assigns one owning layer per header, and rolls out CSP report-only first. |
| `threat-model` | A feature is being designed and nobody has written down who could abuse it. Produces the boundary-and-threat table before code, and names which other skill verifies each control. |
| `webhook-reliability` | Designing or reviewing webhooks in either direction: signature verification, idempotency, retry and backoff, dead letters, monitoring. |

[Pack README →](./plugins/hardening)

</details>

<details>
<summary><b>release-ops</b> · 10 skills</summary>

| Skill | What it covers |
|---|---|
| `customer-support-triage` | A support email or ticket needs handling. Classifies it, tries to reproduce bugs, sets severity, files a GitHub issue with no customer PII, checks refunds against the written policy, and drafts the reply for a person to send. |
| `dependency-upgrade` | Bulk dependency bumps. Treats them as a gated pipeline — inventory, batch, then type check, test, and E2E between batches — rather than one update command and hope. |
| `incident-response` | A service is down, erroring, or degraded in production. Sets severity, runs a fixed triage order, decides on rollback first, drafts user comms, and writes a one-page blameless postmortem. |
| `llm-cost-audit` | The model API bill is high or due a review. Reconciles tracked cost with the provider's bill, checks each call site's model tier, finds caching and batch savings using the provider's current prices, and ends in a savings table. |
| `npm-publish` | Publishing to npm or bun — preflight checks, semver bump, changelog entry, git push, publish, verify. Rotates an expired npm token through the browser instead of stopping to ask for a one-time code. |
| `observability-setup` | You are launching a service or auditing its monitoring. Wires a health-check endpoint, uptime checks, log forwarding, error tracking, LLM cost tracking, and page-versus-ticket alert thresholds. |
| `pr-wait` | A PR is open and you want to block on CI rather than watch it, optionally merging when checks pass. |
| `the-waiting` | CI is running and you want to know how long is really left, or why a run is still pending. Estimates each job from its own history, spots runs stuck behind a cancelled one, and suggests something small to do meanwhile. Named for Tom Petty's "The Waiting", because it is the hardest part. |
| `version-check` | You need to decide the next version. Reads the commits since the last tag and recommends major, minor, or patch, with the reasoning. |
| `vscode-marketplace-publish` | Publishing a VS Code extension update — preflight, version, package check, then publish to the Visual Studio Marketplace (and Open VSX if you use it) and confirm it is live. Waits for your yes before anything goes out. |

[Pack README →](./plugins/release-ops)

</details>

<details>
<summary><b>product-strategy</b> · 15 skills · 2 agents</summary>

| Skill | What it covers |
|---|---|
| `pm-canvas` | Filling in, teaching, or reviewing a one-page product strategy canvas. |
| `pm-capabilities` | Mapping the business capabilities a strategy needs, and the gaps. |
| `pm-discovery` | Planning interviews, testing assumptions, Kano surveys, journey maps, or A/B tests. |
| `pm-growth` | Acquisition, activation, retention, referral loops, and monetization. |
| `pm-market-analysis` | Five Forces, PESTLE, SWOT, and other views of the market around you. |
| `pm-objectives` | Setting OKRs, key metrics, or a North Star metric. Includes a 40-entry metric catalog. |
| `pm-roadmap` | Building an outcome roadmap, prioritizing, or writing a PRD or user stories. |
| `pm-strategy` | Choosing where to play and how to win, and the trade-offs that come with it. |
| `pm-strategy-fit` | Checking that strategic choices reinforce each other and are hard to copy. |
| `pm-teams` | Setting up empowered product teams and team-level objectives. |
| `pm-value-proposition` | Working out customer value, alternatives, and a value curve. |
| `pm-vision` | Defining a mission, vision, or winning aspiration: what success should mean. |
| `pm-visuals` | Turning any of the above into a diagram (Mermaid by default) or an HTML page. |
| `pricing-review` | Reviewing pricing and packaging, or before changing prices: value metric, tiers, willingness-to-pay evidence, a sourced competitor scan, and a grandfathering plan for existing customers. |
| `product-manager` | You want a chief PM to lead the work end to end, or to teach you while you do it. Routes to the skills below. |

Agents (Claude Code): `business-capability-modeler` `product-manager`

[Pack README →](./plugins/product-strategy)

</details>

<details>
<summary><b>go-to-market</b> · 12 skills · 2 agents</summary>

| Skill | What it covers |
|---|---|
| `marketing-lead` | You want a marketing plan, or don't know why nobody is using the product. Routes to the skills below and teaches as it goes. |
| `mk-audience` | Choosing the first customer, writing an ideal customer profile, and finding who influences the buyer. |
| `mk-brand-kit` | Settling a product's voice, palette, fonts, and logo use, and picking a design tool. |
| `mk-community` | Taking part in Discord servers, subreddits, forums, and open-source communities without spamming them. |
| `mk-copy` | Writing or editing a landing page, README opening, store listing, or announcement. |
| `mk-founder-content` | Founder posts, building in public, newsletters, and finding the stories worth telling. |
| `mk-launch` | Planning a launch or relaunch: Show HN, Product Hunt, release-day posts, and the readout afterwards. |
| `mk-lifecycle` | Waitlist, onboarding, activation, upgrade, and win-back email sequences. |
| `mk-measurement` | Choosing what to measure, reading whether a channel worked, and running trustworthy experiments. |
| `mk-outreach` | Cold email, press and podcast pitches, design partners, and warm introductions. |
| `mk-positioning` | Working out who the product is for, what it beats, and how to say it in one line. Built on April Dunford's positioning method. |
| `mk-search` | Getting found in search and cited by AI assistants: citable pages, `llms.txt`, test-question panels. |

Agents (Claude Code): `audience-scout` `marketing-lead`

[Pack README →](./plugins/go-to-market)

</details>

<details>
<summary><b>design-suite</b> · 7 skills · 8 agents</summary>

| Skill | What it covers |
|---|---|
| `accessibility-review` | You want a keyboard, screen-reader, contrast, reflow, target-size or motion review against WCAG 2.2 AA, with prioritised findings and fixes. |
| `art-direction` | A page or screen looks generic, templated or "AI-made", or you are building a landing page, portfolio, product page or app screen and want a deliberate look: it deals researched directions, enforces a no-slop house style and checks the result in a real browser. |
| `dashboard-design` | You are designing or fixing a dashboard, console, status view, or data-heavy screen, including stale, missing and partial data. |
| `information-architecture` | You are organising navigation, labels, taxonomy, URLs or content types, or chasing a "people cannot find X" report. |
| `interface-polish` | A screen works but looks uneven: spacing, radii, shadows, type, colour, dark mode, motion, or missing hover, focus, loading, empty and error states. |
| `mobile-design` | A flow must work on phones and small windows: touch targets, navigation, mobile forms, slow or offline networks, and web-versus-native questions. |
| `ui-ux` | You are designing or reviewing a flow, screen, form, or state, or want a design brief or an implementation handoff. The entry point: it frames the user task, then routes to the skills below. |

Agents (Claude Code): `accessibility-expert` `dashboard-designer` `design-ui-engineer` `direction-reviewer` `information-architect` `mobile-design-expert` `ui-ux-lead` `ux-designer`

[Pack README →](./plugins/design-suite)

</details>

<details>
<summary><b>codebase-intel</b> · 5 skills</summary>

| Skill | What it covers |
|---|---|
| `codebase-architecture-scanner` | You need architecture documentation that doesn't exist yet — layered high-level and detailed docs, with C4 context and sequence diagrams. |
| `codebase-health` | Onboarding somewhere unfamiliar, planning a refactor, or diagnosing why one area keeps breaking. Reports complexity hotspots, churn, bus factor, and velocity from git history. |
| `grill-with-docs` | A plan is drafted and needs challenging against the domain model that's already there, sharpening terminology and updating docs rather than inventing parallel vocabulary. |
| `read-the-damn-docs` | Anything touching a third-party API, library, framework, CLI, cloud service, or provider SDK. Goes to current documentation instead of trusting recall. |
| `teach-code-to-mastery` | You want to really understand a diff, PR, module or algorithm, not just read a summary. Teaches one stage at a time and checks you can explain it back before moving on. |

[Pack README →](./plugins/codebase-intel)

</details>

<details>
<summary><b>A–Z index</b> · every skill and its pack</summary>

| Skill | Pack |
|---|---|
| `accessibility-review` | [design-suite](./plugins/design-suite) |
| `agent-tooling-review` | [hardening](./plugins/hardening) |
| `agent-watchdog` | [second-opinion](./plugins/second-opinion) |
| `analytics-instrumentation` | [ship-pipeline](./plugins/ship-pipeline) |
| `api-design` | [ship-pipeline](./plugins/ship-pipeline) |
| `art-direction` | [design-suite](./plugins/design-suite) |
| `auth-hardening` | [hardening](./plugins/hardening) |
| `backup-verify` | [ship-pipeline](./plugins/ship-pipeline) |
| `cdf` | [ship-pipeline](./plugins/ship-pipeline) |
| `codebase-architecture-scanner` | [codebase-intel](./plugins/codebase-intel) |
| `codebase-health` | [codebase-intel](./plugins/codebase-intel) |
| `customer-support-triage` | [release-ops](./plugins/release-ops) |
| `dashboard-design` | [design-suite](./plugins/design-suite) |
| `db-migration-safety` | [ship-pipeline](./plugins/ship-pipeline) |
| `db-truth` | [ship-pipeline](./plugins/ship-pipeline) |
| `debug-feedback-loop` | [second-opinion](./plugins/second-opinion) |
| `dependency-upgrade` | [release-ops](./plugins/release-ops) |
| `deploy` | [ship-pipeline](./plugins/ship-pipeline) |
| `efficient-frontier-routing` | [second-opinion](./plugins/second-opinion) |
| `exposure-scan` | [hardening](./plugins/hardening) |
| `feature-flags` | [ship-pipeline](./plugins/ship-pipeline) |
| `grill-with-docs` | [codebase-intel](./plugins/codebase-intel) |
| `html` | [reporting-comms](./plugins/reporting-comms) |
| `human-writing` | [reporting-comms](./plugins/reporting-comms) |
| `incident-response` | [release-ops](./plugins/release-ops) |
| `information-architecture` | [design-suite](./plugins/design-suite) |
| `interface-polish` | [design-suite](./plugins/design-suite) |
| `legal-docs` | [hardening](./plugins/hardening) |
| `llm-app-security` | [hardening](./plugins/hardening) |
| `llm-cost-audit` | [release-ops](./plugins/release-ops) |
| `llm-council` | [second-opinion](./plugins/second-opinion) |
| `marketing-lead` | [go-to-market](./plugins/go-to-market) |
| `mk-audience` | [go-to-market](./plugins/go-to-market) |
| `mk-brand-kit` | [go-to-market](./plugins/go-to-market) |
| `mk-community` | [go-to-market](./plugins/go-to-market) |
| `mk-copy` | [go-to-market](./plugins/go-to-market) |
| `mk-founder-content` | [go-to-market](./plugins/go-to-market) |
| `mk-launch` | [go-to-market](./plugins/go-to-market) |
| `mk-lifecycle` | [go-to-market](./plugins/go-to-market) |
| `mk-measurement` | [go-to-market](./plugins/go-to-market) |
| `mk-outreach` | [go-to-market](./plugins/go-to-market) |
| `mk-positioning` | [go-to-market](./plugins/go-to-market) |
| `mk-search` | [go-to-market](./plugins/go-to-market) |
| `mobile-design` | [design-suite](./plugins/design-suite) |
| `npm-publish` | [release-ops](./plugins/release-ops) |
| `observability-setup` | [release-ops](./plugins/release-ops) |
| `plan-arbiter` | [second-opinion](./plugins/second-opinion) |
| `pm-canvas` | [product-strategy](./plugins/product-strategy) |
| `pm-capabilities` | [product-strategy](./plugins/product-strategy) |
| `pm-discovery` | [product-strategy](./plugins/product-strategy) |
| `pm-growth` | [product-strategy](./plugins/product-strategy) |
| `pm-market-analysis` | [product-strategy](./plugins/product-strategy) |
| `pm-objectives` | [product-strategy](./plugins/product-strategy) |
| `pm-roadmap` | [product-strategy](./plugins/product-strategy) |
| `pm-strategy` | [product-strategy](./plugins/product-strategy) |
| `pm-strategy-fit` | [product-strategy](./plugins/product-strategy) |
| `pm-teams` | [product-strategy](./plugins/product-strategy) |
| `pm-value-proposition` | [product-strategy](./plugins/product-strategy) |
| `pm-vision` | [product-strategy](./plugins/product-strategy) |
| `pm-visuals` | [product-strategy](./plugins/product-strategy) |
| `pr-wait` | [release-ops](./plugins/release-ops) |
| `pricing-review` | [product-strategy](./plugins/product-strategy) |
| `privacy-audit` | [hardening](./plugins/hardening) |
| `product-manager` | [product-strategy](./plugins/product-strategy) |
| `prove-it` | [ship-pipeline](./plugins/ship-pipeline) |
| `rate-limit-audit` | [hardening](./plugins/hardening) |
| `read-the-damn-docs` | [codebase-intel](./plugins/codebase-intel) |
| `readiness-review` | [hardening](./plugins/hardening) |
| `recap-table` | [reporting-comms](./plugins/reporting-comms) |
| `redline` | [reporting-comms](./plugins/reporting-comms) |
| `review-merge-pipeline` | [ship-pipeline](./plugins/ship-pipeline) |
| `review-slop` | [ship-pipeline](./plugins/ship-pipeline) |
| `secrets-leak-audit` | [hardening](./plugins/hardening) |
| `security-headers` | [hardening](./plugins/hardening) |
| `ship-issues` | [ship-pipeline](./plugins/ship-pipeline) |
| `spec-review` | [second-opinion](./plugins/second-opinion) |
| `start-issue` | [ship-pipeline](./plugins/ship-pipeline) |
| `stripe-billing` | [ship-pipeline](./plugins/ship-pipeline) |
| `teach-code-to-mastery` | [codebase-intel](./plugins/codebase-intel) |
| `the-waiting` | [release-ops](./plugins/release-ops) |
| `threat-model` | [hardening](./plugins/hardening) |
| `ui-ux` | [design-suite](./plugins/design-suite) |
| `ux-review` | [ship-pipeline](./plugins/ship-pipeline) |
| `version-check` | [release-ops](./plugins/release-ops) |
| `visual-plan` | [reporting-comms](./plugins/reporting-comms) |
| `visual-recap` | [reporting-comms](./plugins/reporting-comms) |
| `vscode-marketplace-publish` | [release-ops](./plugins/release-ops) |
| `webhook-reliability` | [hardening](./plugins/hardening) |
| `writing-clearly-and-concisely` | [reporting-comms](./plugins/reporting-comms) |

</details>
<!-- catalog:end -->

### Tool plugins

Two plugins ship executable code rather than markdown, so they live in their own repositories.

| Plugin | What it does |
|---|---|
| [**work-plan**](https://github.com/stylusnexus/work-plan-toolkit) | Track-aware daily planning over GitHub issues — shared git-synced tracks optionally pinned to a canonical plan branch, AI clustering, coverage, doc liveness, and dependency-aware next-up. Pure-stdlib Python CLI plus an accessible VS Code viewer with a repo-qualified dependency graph and confirm-gated writes. Includes a one-command dependency check (`doctor`), a stale-tracks view and label search. |
| [**defect-scan**](https://github.com/stylusnexus/defect-scan) | Language-aware defect hunter. Detects the stack, triages by risk, runs the real analyzers (ruff/mypy, tsc/eslint, rubocop/brakeman, optionally semgrep/gitleaks/bandit), then reports in confidence tiers across 15 language profiles — correlated against existing issues, with optional issue filing, safe autofix, and a cross-model second opinion. |

> **Also available outside the plugin system:** work-plan ships a standalone **[VS Code extension](https://marketplace.visualstudio.com/items?itemName=stylusnexus.work-plan-viewer)** — a visual sidebar, dependency graph, and track editor over the same CLI (VS Code Marketplace + [Open VSX](https://open-vsx.org/extension/stylusnexus/work-plan-viewer)) — and an **npm CLI**: `npm install -g @stylusnexus/work-plan`. See the [toolkit install guide](https://github.com/stylusnexus/work-plan-toolkit#quick-install).

### A note on fit

These packs have opinions — evidence before "done", detect rather than assume, one rule per owner.
That's useful if you share them and friction if you don't; each README states the opinion plainly
rather than burying it.

### More skills

Eve McGivern, who maintains these packs, also publishes a personal marketplace,
[evemcgivern-skills](https://github.com/evemcgivern/agent-skills), with more skills for Claude Code
and Codex: agent working habits (model routing, handoffs, a background-dispatch orchestrator),
plain writing, and everyday engineering. Add it the same way:
`/plugin marketplace add evemcgivern/agent-skills`.

---

## Compatibility

Each skill's example in its pack README starts with three badges, and each pack README opens its
examples with a **Compatibility at a glance** table. The data behind both is
[`compatibility.json`](./compatibility.json), and `scripts/check-compat.py` keeps them in step.

| Host | Badge | What it covers |
|---|---|---|
| **Claude Code** | Claude: Code | CLI, desktop and IDE extensions, with the pack installed as a plugin |
| **Claude app** | Claude: app | claude.ai on the web, desktop and mobile, with the skill uploaded |
| **Codex** | Codex / ChatGPT: Codex | Codex CLI, app and IDE extension, with the pack installed as a plugin |
| **ChatGPT** | Codex / ChatGPT: ChatGPT | ChatGPT Chat and Work |
| **Other agents** | Other agents | Agents that read SKILL.md folders and run shell commands, installed through the Skills CLI |

✔ **full**: the skill does its whole job there. ◐ **partial**: it runs, but a named step is lost;
the **Limits** line under the badges says which. ✖ **no**: it cannot do its core job there. Badge
colour follows the agent on your machine (Claude Code, Codex, other agents): green for full, yellow
for partial, grey for no.

**"app" means a remote sandbox.** The Claude app and ChatGPT run skills in the cloud, with no access
to your local files, repo or local shell (ChatGPT Work can run code and shell commands in its own
managed, isolated environment). Pure-conversation skills work there. Skills that read code work on a
repo archive you upload, with the live steps lost. Skills that need your live repo, git, `gh`, a live
database or a local browser do not work, and neither does efficient-frontier-routing, because
neither app offers subagents with a choice of model. These 21 can't run in ChatGPT or the Claude
app: backup-verify, codebase-health,
db-truth, debug-feedback-loop, dependency-upgrade, deploy, efficient-frontier-routing,
exposure-scan, npm-publish, pr-wait, prove-it, rate-limit-audit, readiness-review, redline,
review-merge-pipeline, review-slop, secrets-leak-audit, ship-issues, spec-review, start-issue,
the-waiting.

**Where agents look for skills.** `.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI,
Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Windsurf's own
folder is `.devin/skills`, and it also reads `.claude/skills` when its Claude Code config reading is
on. Cline needs its own folder, `.cline/skills`, or reads `.claude/skills`; it does not read
`.agents/skills`. The Skills CLI writes into each detected
agent's own folder, so you don't have to choose. Gemini CLI's docs say Antigravity CLI replaced it
for unpaid and Google One users on 18 June 2026.

**Shared files travel with each skill.** Every pm-* skill and six mk-* skills (mk-copy,
mk-founder-content, mk-launch, mk-lifecycle, mk-outreach, mk-search) carry their own copy of their
pack's shared principles file, so a single-skill install (`--skill pm-canvas`) or a Claude app upload
of one folder has everything the SKILL.md reads; `scripts/check-shared-sync.sh` keeps each copy
identical to the canonical file. Links to other skills' reference files are optional reading and
still need the whole pack. product-manager routes to its sibling skills, so it needs the pack.

**Plugin agents stay behind.** The Skills CLI installs skills only. The eleven plugin agents
(audience-scout and marketing-lead in go-to-market, product-manager and business-capability-modeler
in product-strategy, and the seven design agents in design-suite) arrive only with the Claude Code plugin. mk-audience carries the audience-scout
brief in its own `references/` folder and runs that step inline when the agent is absent.

---

## Install

Two steps: **add the marketplace once**, then **install whichever packs you want**. Skipping to
"install everything" is a valid choice — it's 82 skills, all inert until their trigger matches.

Pick your tool, copy the command, then open its section below for the rest.

| Tool | Best way | Command to copy |
|---|---|---|
| **Claude Code** (terminal · VS Code · JetBrains) | Plugin marketplace | `/plugin marketplace add stylusnexus/agent-plugins` |
| **OpenAI Codex** (CLI · app · IDE) | Plugin marketplace | `codex plugin marketplace add stylusnexus/agent-plugins` |
| **Cursor · Copilot · Gemini CLI · ~60 more** | Skills CLI | `npx skills add stylusnexus/agent-plugins` |
| **No plugin system** (work-plan only) | Clone + install script | `git clone https://github.com/stylusnexus/work-plan-toolkit` |

<details>
<summary><b>Claude Code</b> (terminal · VS Code extension · JetBrains extension)</summary>

Add the marketplace once:

```
/plugin marketplace add stylusnexus/agent-plugins
```

Then pick — one, several, or the lot:

```
/plugin install ship-pipeline@stylus-nexus       # just the daily loop
/plugin install hardening@stylus-nexus           # add another whenever
```

Or browse them visually with `/plugin` → **Discover**, which lists all ten with descriptions.

<details>
<summary>More</summary>

Plugin config is shared between the Claude Code CLI and its IDE extensions, so installing once
covers all three surfaces.

For several packs in one line, see **Recipes by goal** below.

Skills carry the pack name: `/ship-pipeline:prove-it`. Updating and removing are in their own
sections below.

</details>
</details>

<details>
<summary><b>OpenAI Codex</b> (CLI · app · IDE extension)</summary>

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
```

In the Codex CLI and IDE extension, type `$` and a skill name (`$ship-pipeline:prove-it`) or run
`/skills` to pick one. In ChatGPT, type `@` and the skill name; the 21 skills listed under
[Compatibility](#compatibility) can't run there, because they need your local repo, git or a browser,
or (efficient-frontier-routing) subagents with a choice of model.

<details>
<summary>More</summary>

Codex reads its own index at `.agents/plugins/marketplace.json` — same marketplace, different
schema. Plugin skills carry the pack name, as in Claude Code.

For several packs in one line, see **Recipes by goal** below.

Updating and removing are in their own sections below.

</details>
</details>

<details>
<summary><b>Cursor · Copilot · Gemini CLI · Windsurf · Zed · opencode · Cline · Continue · Hermes · ~60 more</b></summary>

The [Skills CLI](https://github.com/vercel-labs/skills) detects which agents you already have and
writes to each one's skills directory. No marketplace step — one command does both:

```bash
npx skills add stylusnexus/agent-plugins                    # choose interactively
npx skills add stylusnexus/agent-plugins --skill '*'        # all 82 skills
```

Skills install without a pack prefix. How you call one depends on the agent: `/prove-it` in Cursor,
Copilot and Cline, `@prove-it` in Windsurf, `/prove-it` in opencode only when the skill sets an
opencode-specific metadata field, and in Gemini CLI the model activates a skill itself once you
approve it.

<details>
<summary>More</summary>

Take only some skills, or look first:

```bash
npx skills add stylusnexus/agent-plugins --skill prove-it   # exactly one
npx skills add stylusnexus/agent-plugins --skill html redline   # several
npx skills add stylusnexus/agent-plugins --list             # see what's there first
```

Target specific agents instead of all detected ones:

```bash
npx skills add stylusnexus/agent-plugins -a cursor -a github-copilot
```

Or via npm, which forwards to the same CLI:

```bash
npx @stylusnexus/agent-plugins --skill '*'
```

</details>
</details>

<details>
<summary><a id="work-plan-without-a-plugin-system"></a><b>work-plan without a plugin system</b> (clone + install script)</summary>

`work-plan` ships a Python CLI and a VS Code viewer, so on agents with no plugin support it installs
directly:

```bash
git clone https://github.com/stylusnexus/work-plan-toolkit
cd work-plan-toolkit && ./install.sh        # macOS / Linux / WSL
```

<details>
<summary>More</summary>

Other targets:

```bash
.\install.ps1                              # Windows
./install.sh --target=$HOME/.agents        # Codex skills dir
```

Install `gh`, `git`, `python3` and `yq` first — see
[work-plan: prerequisites, security, versioning](#work-plan-prerequisites-security-versioning).

`work-plan` and `defect-scan` are tools rather than skill packs — take them if you want GitHub-issue
planning or a defect scanner specifically.

Its commands are namespaced under the plugin when installed that way:

| Command | Does |
|---|---|
| `/work-plan:brief` | Multi-track daily snapshot |
| `/work-plan:handoff <track>` | Wrap up a work block (session log, next-up) |
| `/work-plan:orient [track]` | Re-orient on a track / cwd |
| `/work-plan:hygiene` | Weekly cleanup (refresh + reconcile + duplicates) |
| `/work-plan:status` | Doc & plan liveness (`plan-status`) |
| `/work-plan:run <subcommand>` | Anything else (`slot`, `close`, `reconcile`, `group`, `coverage`, …) |

</details>
</details>

<details>
<summary><a id="recipes-by-goal"></a><b>Recipes by goal</b></summary>

| Goal | Take |
|---|---|
| Ship code every day without breaking things | `ship-pipeline` `second-opinion` |
| Get ready to launch | `hardening` `release-ops` `go-to-market` |
| Decide what to build, and why | `product-strategy` `second-opinion` |
| Get a product noticed on a few hours a week | `go-to-market` `reporting-comms` |
| Find your way around an unfamiliar codebase | `codebase-intel` `reporting-comms` |
| Make agent output easier to read and review | `reporting-comms` |

Install a recipe in one line (swap in the packs you want):

```bash
for p in ship-pipeline second-opinion; do claude plugin install $p@stylus-nexus; done   # Claude Code
for p in ship-pipeline second-opinion; do codex plugin add $p@stylus-nexus; done        # Codex
```

</details>

<details>
<summary><a id="what-you-type-afterwards"></a><b>What you type afterwards</b></summary>

Where a skill came from decides its name:

| Installed via | Invoke as | Why |
|---|---|---|
| Claude Code plugin | `/ship-pipeline:prove-it` | Plugins namespace their skills, so two packs can share a skill name without colliding |
| Codex plugin | `$ship-pipeline:prove-it`, or `/skills` to pick | Codex also prefixes plugin skills with the pack name, and mentions them with `$` (ChatGPT uses `@`, and the 21 skills listed under [Compatibility](#compatibility) can't run there) |
| Skills CLI / npm | `/prove-it` in most agents, `@prove-it` in Windsurf | Installed as plain skills, no namespace; opencode shows `/prove-it` only when the skill sets an opencode-specific metadata field, and Gemini CLI activates a skill itself after you approve it |

Most skills are **model-invoked** — you don't type them at all. `prove-it` fires when you're
wrapping up work, `read-the-damn-docs` when you touch an unfamiliar API. Typing the name forces it.

</details>

<details>
<summary><a id="staying-up-to-date"></a><b>Updating</b></summary>

**Claude Code.** Third-party marketplaces don't auto-update by default. Turn it on once: run
`/plugin`, open **Marketplaces**, choose `stylus-nexus`, and select **Enable auto-update**. Updates
then arrive in the background, and Claude Code asks you to run `/reload-plugins`. To update by hand:

```bash
claude plugin marketplace update stylus-nexus
claude plugin update ship-pipeline@stylus-nexus      # once per pack you use
```

**Codex.** Refresh the marketplace, then re-add each pack you use; re-adding replaces the installed
copy with the current one.

```bash
codex plugin marketplace upgrade stylus-nexus
codex plugin add ship-pipeline@stylus-nexus          # once per pack you use
```

**Skills CLI.** `npx skills update`

In-repo packs carry no version number, so every change merged here counts as an update.

</details>

<details>
<summary><a id="removing"></a><b>Uninstalling</b></summary>

```
/plugin uninstall ship-pipeline@stylus-nexus         # Claude Code
/plugin marketplace remove stylus-nexus
```

```
codex plugin remove ship-pipeline@stylus-nexus       # Codex
codex plugin marketplace remove stylus-nexus
```

```bash
npx skills remove prove-it                           # Skills CLI
```

</details>

---

## Compatibility at a glance

The **eight skill packs** are plain markdown, so the Skills CLI can install them into every agent it
supports; how well each skill runs there is under [Compatibility](#compatibility).
**work-plan** and **defect-scan** ship executable code and install from their own repositories.

<details>
<summary><b>All supported agents</b></summary>

| Agent | Skill packs | Tool plugins | Invoke as |
|---|---|---|---|
| **Claude Code** (CLI · VS Code · JetBrains) | `/plugin install <pack>@stylus-nexus` | `/plugin install work-plan@stylus-nexus` | `/ship-pipeline:prove-it` · `/work-plan:brief` |
| **Codex** (CLI · app · IDE) | `codex plugin add <pack>@stylus-nexus` | `codex plugin add work-plan@stylus-nexus` | `$ship-pipeline:prove-it` · `/skills` |
| **Cursor** | `npx skills add stylusnexus/agent-plugins` | clone + `install.sh` + `.cursorrules` shim | `/prove-it` · `python3 …/work_plan.py` |
| **GitHub Copilot** | `npx skills add stylusnexus/agent-plugins` | clone + `install.sh` + copilot-instructions shim | `/prove-it` · direct CLI |
| **Gemini CLI · Windsurf · Zed · opencode · Cline · Continue · Hermes · Goose · Warp · Amp · Junie · Roo · Qwen Code · Trae · Aider · +more** | `npx skills add stylusnexus/agent-plugins` | — | `/prove-it` in most · `@prove-it` in Windsurf · opencode only with an opencode metadata field · Gemini CLI activates skills itself after you approve |
| **Any other / terminal** | `npx skills add stylusnexus/agent-plugins -a universal` | clone + `install.sh` | `/prove-it` · direct CLI |

</details>

See **Updating** under [Install](#install) for each host's update commands.

---

## Repository structure

```
agent-plugins/
├── .claude-plugin/
│   └── marketplace.json     # Claude index   (source: "./plugins/…" or github+repo)
├── .agents/plugins/
│   └── marketplace.json     # Codex index    (source: local+path, or url + policy + category)
├── plugins/                 # in-repo plugins
│   ├── ship-pipeline/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .codex-plugin/plugin.json   # Codex reads its own manifest dir
│   │   ├── skills/<name>/SKILL.md
│   │   └── README.md
│   ├── reporting-comms/
│   ├── codebase-intel/
│   ├── second-opinion/
│   ├── hardening/
│   ├── release-ops/
│   ├── product-strategy/
│   ├── go-to-market/
│   └── design-suite/
├── scripts/
│   ├── check-manifest-sync.sh   # the two indexes must agree
│   ├── check-skills.py          # every SKILL.md must actually load
│   ├── check-readme.py          # README tables and counts match plugins/
│   ├── gen-catalog.py           # writes the skill catalogue and skills.sh.json
│   ├── check-links.py           # relative links and anchors resolve
│   ├── check-private-terms.sh   # checks private terms; allows exact public references
│   └── test-private-terms.sh    # proves public-reference exceptions stay narrow
├── site/                        # the catalogue page, published to GitHub Pages
├── skills.sh.json               # skills.sh groupings, one per pack
├── LICENSE
└── README.md
```

Both indexes list the same plugins. Plugins hosted in their own repositories are **pinned to a
release tag**, so Claude and Codex install identical, reproducible versions. Plugins that live in
this repository are referenced by relative path and carry no version number, so each merged change
reaches users as an update.

---

## work-plan: prerequisites, security, versioning

These apply to the **work-plan** tool plugin, not the skill packs. Each pack lists its own
prerequisites in its README.

### Prerequisites

The toolkit shells out to standard tools — install these **before** first use (the script installer
verifies them; plugin installs assume they're present):

- **`gh`** (GitHub CLI, authenticated via `gh auth login`) — all GitHub access; no tokens stored
- **`git`**, **`python3` (3.9+)**, **`yq`** — the **mikefarah/yq** Go build, *not* the Python jq wrapper

```bash
# macOS
brew install gh git python@3 yq
# Debian/Ubuntu: gh + yq per their official install docs; apt for git/python3
# Windows: winget install GitHub.cli Git.Git Python.Python.3 MikeFarah.yq
```

---

### Security

- **No token storage.** The toolkit reuses your existing `gh auth` — it never reads, writes, or stores GitHub credentials.
- **Public-repo guard.** Every write to a public repo (or unknown visibility) is gated behind a confirm-token flow. The CLI prints `{needs_confirm: true, token: …}` and exits without writing. The VS Code viewer surfaces this as a **"Write anyway / Keep private"** modal. Private repos write straight through.
- **Local-only writes.** All mutations go to local markdown files — GitHub is never written (except the opt-in `suggest-priorities --apply` for priority labels).
- **No telemetry, no daemon.** No cache, no sync loop — `git pull` is the sync mechanism for shared tracks.

### Versioning & releases

work-plan uses **CalVer** (`YYYY.MM.DD+<sha>`), auto-bumped on deploy and synced into both manifests.
Each marketplace entry is **pinned to a release tag** (not a moving branch), so installs are
reproducible; updates land when the tag (and this index's `ref`) advance.

## Resources

- work-plan source & issues: [stylusnexus/work-plan-toolkit](https://github.com/stylusnexus/work-plan-toolkit)
- Claude Code plugins: <https://code.claude.com/docs/en/plugins>
- Codex plugins: <https://developers.openai.com/codex/plugins>

## License

MIT © Stylus Nexus Holdings LLC — see [LICENSE](LICENSE).
