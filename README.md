# Stylus Nexus — Agent Plugins Marketplace

[![skills.sh](https://skills.sh/b/stylusnexus/agent-plugins)](https://skills.sh/stylusnexus/agent-plugins)
[![npm](https://img.shields.io/npm/v/@stylusnexus/agent-plugins)](https://www.npmjs.com/package/@stylusnexus/agent-plugins)
[![npm downloads](https://img.shields.io/npm/dm/@stylusnexus/agent-plugins)](https://www.npmjs.com/package/@stylusnexus/agent-plugins)
[![CI](https://github.com/stylusnexus/agent-plugins/actions/workflows/ci.yml/badge.svg)](https://github.com/stylusnexus/agent-plugins/actions/workflows/ci.yml)
[![plugins](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fstylusnexus%2Fagent-plugins%2Fmain%2F.claude-plugin%2Fmarketplace.json&query=%24.plugins.length&label=plugins)](./.claude-plugin/marketplace.json)
[![GitHub stars](https://img.shields.io/github/stars/stylusnexus/agent-plugins)](https://github.com/stylusnexus/agent-plugins/stargazers)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-7C3AED)
![Codex](https://img.shields.io/badge/Codex-plugin-10A37F)

A plugin marketplace for AI coding agents — **10 plugins, 61 skills**. Installs natively into **Claude
Code** and **OpenAI Codex**, and reaches roughly seventy more agents (Cursor, Copilot, Gemini CLI,
Windsurf, Zed, opencode, Cline, Continue, Hermes and others) through the Skills CLI.

Every skill is repo-agnostic: it detects your repository's conventions rather than assuming its own,
and defers to a repo-local version of itself when your project defines one.

**[Browse the catalogue →](https://claude.ai/code/artifact/667c2158-4833-4535-a5c5-a5597dea8fea)** — every pack, what it's for, and how to install it on your agent.

> ⚠️ **Trust before you install.** Plugins run code on your machine. Review a plugin's source before
> installing it. Everything here is open-source — links are in the table below.

> **Plugins ≠ one format.** Claude Code and Codex have *separate* plugin systems, so this repo carries
> a **per-host index**: `.claude-plugin/marketplace.json` (Claude) and `.agents/plugins/marketplace.json`
> (Codex). You add the *same* marketplace either way; each tool reads the schema it understands.

---

## Plugins

### Skill packs

Eight packs, grouped by the job rather than the technology. Each pack's README carries a
**rule-ownership table** so the skills inside it don't compete for the same trigger.

| Pack | # | What it's for | Skills |
|---|---|---|---|
| [**ship-pipeline**](./plugins/ship-pipeline) | 9 | The daily loop: read the issue, ground assumptions in the live database, prove it works, review, merge, promote — one issue or a batch. | `start-issue` `db-truth` `prove-it` `review-slop` `review-merge-pipeline` `deploy` `ship-issues` `db-migration-safety` `backup-verify` |
| [**reporting-comms**](./plugins/reporting-comms) | 7 | The last mile — turning agent output into something a person wants to read, and getting their judgment back. | `html` `visual-plan` `visual-recap` `recap-table` `writing-clearly-and-concisely` `human-writing` `redline` |
| [**second-opinion**](./plugins/second-opinion) | 5 | One premise: a single model's confident answer is not evidence. | `llm-council` `plan-arbiter` `spec-review` `agent-watchdog` `debug-feedback-loop` |
| [**hardening**](./plugins/hardening) | 5 | The unglamorous pre-launch gates — a missing rate limit, an unsigned webhook, a compromised dependency. | `rate-limit-audit` `exposure-scan` `auth-hardening` `webhook-reliability` `privacy-audit` |
| [**release-ops**](./plugins/release-ops) | 5 | Deciding the version, waiting on CI, publishing, and keeping dependencies current between releases. | `version-check` `pr-wait` `the-waiting` `npm-publish` `dependency-upgrade` |
| [**product-strategy**](./plugins/product-strategy) | 14 | Deciding what to build and why — vision, strategy, value, objectives, roadmaps and discovery, taught as it goes. | `product-manager` `pm-vision` `pm-strategy` `pm-strategy-fit` `pm-canvas` `pm-value-proposition` `pm-objectives` `pm-roadmap` `pm-discovery` `pm-growth` `pm-market-analysis` `pm-capabilities` `pm-teams` `pm-visuals` |
| [**go-to-market**](./plugins/go-to-market) | 12 | Getting a product noticed on a small team's hours — positioning, copy, launches, community, outreach, email and measurement. | `marketing-lead` `mk-positioning` `mk-audience` `mk-copy` `mk-brand-kit` `mk-search` `mk-launch` `mk-community` `mk-founder-content` `mk-outreach` `mk-lifecycle` `mk-measurement` |
| [**codebase-intel**](./plugins/codebase-intel) | 4 | Building an accurate picture of a codebase, and the libraries it leans on, before changing it. | `codebase-health` `codebase-architecture-scanner` `grill-with-docs` `read-the-damn-docs` |

#### Every skill, by pack

<!-- catalog:start -->
<details>
<summary><b>ship-pipeline</b> · 9 skills</summary>

| Skill | Use it when |
|---|---|
| `backup-verify` | Backup existence and restore-testing; the go/no-go before a risky mutation |
| `db-migration-safety` | Writing schema change — expand-contract sequencing, idempotency, backfills |
| `db-truth` | Reading schema truth — shape, relationships, permissions, and post-apply confirmation |
| `deploy` | Production promotion, merge strategy, release-tooling compatibility |
| `prove-it` | Evidence standards, gate discovery, the evidence table, `UNVERIFIED` labeling |
| `review-merge-pipeline` | Review orchestration, commit/push/PR mechanics, merge-target detection, head-SHA and required-check confirmation before merge |
| `review-slop` | Report-only slop findings, severity calibration, and suggested repair criteria |
| `ship-issues` | Batch orchestration — per-issue status, grouping into branches, consult-before-asking, post-deploy validation, the batch report. |
| `start-issue` | Issue comprehension, prior-art checking, baseline capture, branch naming |

[Pack README →](./plugins/ship-pipeline)

</details>

<details>
<summary><b>reporting-comms</b> · 7 skills</summary>

| Skill | Use it when |
|---|---|
| `html` | Output is complex enough that a wall of terminal text loses it — plans, code reviews, research, comparisons, configs, reports. |
| `human-writing` | Text reads as machine-generated: corporate speak, generic phrasing, the familiar AI cadence. |
| `recap-table` | Someone asks "what did you change?" or wants a before/after comparison. |
| `redline` | The human needs to judge a draft, plan, or report and describing the problems in chat is slower than fixing them. |
| `visual-plan` | A text plan would land better as an interactive document: diagrams, file maps, annotated code, open questions, and UI review where it helps. |
| `visual-recap` | A PR, branch, commit, or diff needs explaining — renders it with diagrams, file maps, API and schema summaries, and annotated diffs. |
| `writing-clearly-and-concisely` | Any prose a human will read — docs, commit messages, error messages, explanations. |

[Pack README →](./plugins/reporting-comms)

</details>

<details>
<summary><b>second-opinion</b> · 5 skills</summary>

| Skill | Use it when |
|---|---|
| `agent-watchdog` | Another agent's work needs watching, auditing, comparing, or fixing, from a session ID or transcript. |
| `debug-feedback-loop` | A bug needs a fast, deterministic pass/fail signal before hypothesising about causes — the step most debugging skips. |
| `llm-council` | A question, idea, or decision is consequential enough to want five advisors analysing it independently before synthesis — rather than one answer delivered confidently. |
| `plan-arbiter` | Two or more plans are on the table and someone has to compare, cross-review, merge, judge, or arbitrate between them. |
| `spec-review` | A spec or requirements doc is drafted or about to be implemented. |

[Pack README →](./plugins/second-opinion)

</details>

<details>
<summary><b>hardening</b> · 5 skills</summary>

| Skill | Use it when |
|---|---|
| `auth-hardening` | Auth is in place and needs auditing — session and cookie configuration, CSRF, OAuth scopes, per-route protection. |
| `exposure-scan` | Periodically, and after any dependency change. |
| `privacy-audit` | User data is collected and someone needs to say exactly what and where. |
| `rate-limit-audit` | Before launch, or after adding an endpoint that calls a paid API (LLM, email, SMS) or handles auth. |
| `webhook-reliability` | Designing or reviewing webhooks in either direction: signature verification, idempotency, retry and backoff, dead letters, monitoring. |

[Pack README →](./plugins/hardening)

</details>

<details>
<summary><b>release-ops</b> · 5 skills</summary>

| Skill | Use it when |
|---|---|
| `dependency-upgrade` | Bulk dependency bumps. |
| `npm-publish` | Publishing to npm or bun — preflight checks, semver bump, changelog entry, git push, publish, verify. |
| `pr-wait` | A PR is open and you want to block on CI rather than watch it, optionally merging when checks pass. |
| `the-waiting` | CI is running and you want to know how long is really left, or why a run is still pending. |
| `version-check` | You need to decide the next version. |

[Pack README →](./plugins/release-ops)

</details>

<details>
<summary><b>product-strategy</b> · 14 skills · 2 agents</summary>

| Skill | Use it when |
|---|---|
| `pm-canvas` | Filling in, teaching, or reviewing a one-page product strategy canvas. |
| `pm-capabilities` | Mapping the business capabilities a strategy needs, and the gaps. |
| `pm-discovery` | Planning interviews, testing assumptions, Kano surveys, journey maps, or A/B tests. |
| `pm-growth` | Acquisition, activation, retention, referral loops, and monetization. |
| `pm-market-analysis` | Five Forces, PESTLE, SWOT, and other views of the market around you. |
| `pm-objectives` | Setting OKRs, key metrics, or a North Star metric. |
| `pm-roadmap` | Building an outcome roadmap, prioritizing, or writing a PRD or user stories. |
| `pm-strategy` | Choosing where to play and how to win, and the trade-offs that come with it. |
| `pm-strategy-fit` | Checking that strategic choices reinforce each other and are hard to copy. |
| `pm-teams` | Setting up empowered product teams and team-level objectives. |
| `pm-value-proposition` | Working out customer value, alternatives, and a value curve. |
| `pm-vision` | Defining a mission, vision, or winning aspiration: what success should mean. |
| `pm-visuals` | Turning any of the above into a diagram (Mermaid by default) or an HTML page. |
| `product-manager` | You want a chief PM to lead the work end to end, or to teach you while you do it. |

Agents (Claude Code): `business-capability-modeler` `product-manager`

[Pack README →](./plugins/product-strategy)

</details>

<details>
<summary><b>go-to-market</b> · 12 skills · 2 agents</summary>

| Skill | Use it when |
|---|---|
| `marketing-lead` | You want a marketing plan, or don't know why nobody is using the product. |
| `mk-audience` | Choosing the first customer, writing an ideal customer profile, and finding who influences the buyer. |
| `mk-brand-kit` | Settling a product's voice, palette, fonts, and logo use, and picking a design tool. |
| `mk-community` | Taking part in Discord servers, subreddits, forums, and open-source communities without spamming them. |
| `mk-copy` | Writing or editing a landing page, README opening, store listing, or announcement. |
| `mk-founder-content` | Founder posts, building in public, newsletters, and finding the stories worth telling. |
| `mk-launch` | Planning a launch or relaunch: Show HN, Product Hunt, release-day posts, and the readout afterwards. |
| `mk-lifecycle` | Waitlist, onboarding, activation, upgrade, and win-back email sequences. |
| `mk-measurement` | Choosing what to measure, reading whether a channel worked, and running trustworthy experiments. |
| `mk-outreach` | Cold email, press and podcast pitches, design partners, and warm introductions. |
| `mk-positioning` | Working out who the product is for, what it beats, and how to say it in one line. |
| `mk-search` | Getting found in search and cited by AI assistants: citable pages, `llms.txt`, test-question panels. |

Agents (Claude Code): `audience-scout` `marketing-lead`

[Pack README →](./plugins/go-to-market)

</details>

<details>
<summary><b>codebase-intel</b> · 4 skills</summary>

| Skill | Use it when |
|---|---|
| `codebase-architecture-scanner` | You need architecture documentation that doesn't exist yet — layered high-level and detailed docs, with C4 context and sequence diagrams. |
| `codebase-health` | Onboarding somewhere unfamiliar, planning a refactor, or diagnosing why one area keeps breaking. |
| `grill-with-docs` | A plan is drafted and needs challenging against the domain model that's already there, sharpening terminology and updating docs rather than inventing parallel vocabulary. |
| `read-the-damn-docs` | Anything touching a third-party API, library, framework, CLI, cloud service, or provider SDK. |

[Pack README →](./plugins/codebase-intel)

</details>

<details>
<summary><b>A–Z index</b> · every skill and its pack</summary>

| Skill | Pack |
|---|---|
| `agent-watchdog` | [second-opinion](./plugins/second-opinion) |
| `auth-hardening` | [hardening](./plugins/hardening) |
| `backup-verify` | [ship-pipeline](./plugins/ship-pipeline) |
| `codebase-architecture-scanner` | [codebase-intel](./plugins/codebase-intel) |
| `codebase-health` | [codebase-intel](./plugins/codebase-intel) |
| `db-migration-safety` | [ship-pipeline](./plugins/ship-pipeline) |
| `db-truth` | [ship-pipeline](./plugins/ship-pipeline) |
| `debug-feedback-loop` | [second-opinion](./plugins/second-opinion) |
| `dependency-upgrade` | [release-ops](./plugins/release-ops) |
| `deploy` | [ship-pipeline](./plugins/ship-pipeline) |
| `exposure-scan` | [hardening](./plugins/hardening) |
| `grill-with-docs` | [codebase-intel](./plugins/codebase-intel) |
| `html` | [reporting-comms](./plugins/reporting-comms) |
| `human-writing` | [reporting-comms](./plugins/reporting-comms) |
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
| `npm-publish` | [release-ops](./plugins/release-ops) |
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
| `privacy-audit` | [hardening](./plugins/hardening) |
| `product-manager` | [product-strategy](./plugins/product-strategy) |
| `prove-it` | [ship-pipeline](./plugins/ship-pipeline) |
| `rate-limit-audit` | [hardening](./plugins/hardening) |
| `read-the-damn-docs` | [codebase-intel](./plugins/codebase-intel) |
| `recap-table` | [reporting-comms](./plugins/reporting-comms) |
| `redline` | [reporting-comms](./plugins/reporting-comms) |
| `review-merge-pipeline` | [ship-pipeline](./plugins/ship-pipeline) |
| `review-slop` | [ship-pipeline](./plugins/ship-pipeline) |
| `ship-issues` | [ship-pipeline](./plugins/ship-pipeline) |
| `spec-review` | [second-opinion](./plugins/second-opinion) |
| `start-issue` | [ship-pipeline](./plugins/ship-pipeline) |
| `the-waiting` | [release-ops](./plugins/release-ops) |
| `version-check` | [release-ops](./plugins/release-ops) |
| `visual-plan` | [reporting-comms](./plugins/reporting-comms) |
| `visual-recap` | [reporting-comms](./plugins/reporting-comms) |
| `webhook-reliability` | [hardening](./plugins/hardening) |
| `writing-clearly-and-concisely` | [reporting-comms](./plugins/reporting-comms) |

</details>
<!-- catalog:end -->

### Tool plugins

Two plugins ship executable code rather than markdown, so they live in their own repositories.

| Plugin | What it does |
|---|---|
| [**work-plan**](https://github.com/stylusnexus/work-plan-toolkit) | Track-aware daily planning over GitHub issues — shared git-synced tracks optionally pinned to a canonical plan branch, AI clustering, coverage, doc liveness, and dependency-aware next-up. Pure-stdlib Python CLI plus an accessible VS Code viewer with a repo-qualified dependency graph and confirm-gated writes. |
| [**defect-scan**](https://github.com/stylusnexus/defect-scan) | Language-aware defect hunter. Detects the stack, triages by risk, runs the real analyzers (ruff/mypy, tsc/eslint, rubocop/brakeman, optionally semgrep/gitleaks/bandit), then reports in confidence tiers across 15 language profiles — correlated against existing issues, with optional issue filing, safe autofix, and a cross-model second opinion. |

### A note on fit

These packs have opinions — evidence before "done", detect rather than assume, one rule per owner.
That's useful if you share them and friction if you don't; each README states the opinion plainly
rather than burying it.

---

## Install

Two steps: **add the marketplace once**, then **install whichever packs you want**. Skipping to
"install everything" is a valid choice — it's 61 skills, all inert until their trigger matches.

### Claude Code  (terminal · VS Code extension · JetBrains extension)

```
/plugin marketplace add stylusnexus/agent-plugins
```

Then pick — one, several, or the lot:

```
/plugin install ship-pipeline@stylus-nexus       # just the daily loop
/plugin install hardening@stylus-nexus           # add another whenever
```

Or browse them visually with `/plugin` → **Discover**, which lists all ten with descriptions.

### OpenAI Codex  (CLI · app · IDE extension)

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
```

Codex reads its own index at `.agents/plugins/marketplace.json` — same marketplace, different
schema. In the Codex CLI and IDE extension, type `$` and a skill name (`$prove-it`) or run `/skills`
to pick one; in the ChatGPT app, type `@`.

### Everything else — Cursor · Copilot · Gemini CLI · Windsurf · Zed · opencode · Cline · Continue · Hermes · ~60 more

The [Skills CLI](https://github.com/vercel-labs/skills) detects which agents you already have and
writes to each one's skills directory. No marketplace step — one command does both:

```bash
npx skills add stylusnexus/agent-plugins                    # choose interactively
npx skills add stylusnexus/agent-plugins --skill '*'        # all 61 skills
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

### What you type afterwards

Where a skill came from decides its name:

| Installed via | Invoke as | Why |
|---|---|---|
| Claude Code plugin | `/ship-pipeline:prove-it` | Plugins namespace their skills, so two packs can share a skill name without colliding |
| Codex plugin | `$prove-it`, or `/skills` to pick | Codex mentions skills with `$` (the ChatGPT app uses `@`) |
| Skills CLI / npm | `/prove-it` | Installed as plain skills, no namespace |

Most skills are **model-invoked** — you don't type them at all. `prove-it` fires when you're
wrapping up work, `read-the-damn-docs` when you touch an unfamiliar API. Typing the name forces it.

### Recipes by goal

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

`work-plan` and `defect-scan` are tools rather than skill packs — take them if you want GitHub-issue
planning or a defect scanner specifically.

### Staying up to date

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

### Removing

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

Plugin config is shared between the Claude Code CLI and its IDE extensions, so installing once
covers all three surfaces.

### work-plan without a plugin system

`work-plan` ships a Python CLI and a VS Code viewer, so on agents with no plugin support it installs
directly:

```bash
git clone https://github.com/stylusnexus/work-plan-toolkit
cd work-plan-toolkit && ./install.sh        # macOS / Linux / WSL
#   Windows:               .\install.ps1
#   Codex skills dir:      ./install.sh --target=$HOME/.agents
```

Its commands are namespaced under the plugin when installed that way:

| Command | Does |
|---|---|
| `/work-plan:brief` | Multi-track daily snapshot |
| `/work-plan:handoff <track>` | Wrap up a work block (session log, next-up) |
| `/work-plan:orient [track]` | Re-orient on a track / cwd |
| `/work-plan:hygiene` | Weekly cleanup (refresh + reconcile + duplicates) |
| `/work-plan:status` | Doc & plan liveness (`plan-status`) |
| `/work-plan:run <subcommand>` | Anything else (`slot`, `close`, `reconcile`, `group`, `coverage`, …) |

---

## Compatibility at a glance

The **eight skill packs** are plain markdown, so they reach every agent the Skills CLI supports.
**work-plan** and **defect-scan** ship executable code and install from their own repositories.

| Agent | Skill packs | Tool plugins | Invoke as |
|---|---|---|---|
| **Claude Code** (CLI · VS Code · JetBrains) | `/plugin install <pack>@stylus-nexus` | `/plugin install work-plan@stylus-nexus` | `/ship-pipeline:prove-it` · `/work-plan:brief` |
| **Codex** (CLI · app · IDE) | `codex plugin add <pack>@stylus-nexus` | `codex plugin add work-plan@stylus-nexus` | `$prove-it` · `/skills` |
| **Cursor** | `npx skills add stylusnexus/agent-plugins` | clone + `install.sh` + `.cursorrules` shim | `/prove-it` · `python3 …/work_plan.py` |
| **GitHub Copilot** | `npx skills add stylusnexus/agent-plugins` | clone + `install.sh` + copilot-instructions shim | `/prove-it` · direct CLI |
| **Gemini CLI · Windsurf · Zed · opencode · Cline · Continue · Hermes · Goose · Warp · Amp · Junie · Roo · Qwen Code · Trae · Aider · +more** | `npx skills add stylusnexus/agent-plugins` | — | `/prove-it` |
| **Any other / terminal** | `npx skills add stylusnexus/agent-plugins -a universal` | clone + `install.sh` | `/prove-it` · direct CLI |

See [Staying up to date](#staying-up-to-date) for each host's update commands.

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
│   └── go-to-market/
├── scripts/
│   ├── check-manifest-sync.sh   # the two indexes must agree
│   ├── check-skills.py          # every SKILL.md must actually load
│   ├── check-readme.py          # README tables and counts match plugins/
│   ├── gen-catalog.py           # writes the skill catalogue and skills.sh.json
│   ├── check-links.py           # relative links and anchors resolve
│   └── check-private-terms.sh   # nothing private ships in a skill
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
