# Stylus Nexus — Agent Plugins Marketplace

![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-7C3AED)
![Codex](https://img.shields.io/badge/Codex-plugin-10A37F)

A plugin marketplace for AI coding agents — **8 plugins, 35 skills**. Installs natively into **Claude
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

Six packs, grouped by the job rather than the technology. Each pack's README carries a
**rule-ownership table** so the skills inside it don't compete for the same trigger.

| Pack | # | What it's for | Skills |
|---|---|---|---|
| [**ship-pipeline**](./plugins/ship-pipeline) | 9 | The daily loop: read the issue, ground assumptions in the live database, prove it works, review, merge, promote — one issue or a batch. | `start-issue` `db-truth` `prove-it` `review-slop` `review-merge-pipeline` `deploy` `ship-issues` `db-migration-safety` `backup-verify` |
| [**reporting-comms**](./plugins/reporting-comms) | 7 | The last mile — turning agent output into something a person wants to read, and getting their judgment back. | `html` `visual-plan` `visual-recap` `recap-table` `writing-clearly-and-concisely` `human-writing` `redline` |
| [**second-opinion**](./plugins/second-opinion) | 5 | One premise: a single model's confident answer is not evidence. | `llm-council` `plan-arbiter` `spec-review` `agent-watchdog` `debug-feedback-loop` |
| [**hardening**](./plugins/hardening) | 5 | The unglamorous pre-launch gates — a missing rate limit, an unsigned webhook, a compromised dependency. | `rate-limit-audit` `exposure-scan` `auth-hardening` `webhook-reliability` `privacy-audit` |
| [**release-ops**](./plugins/release-ops) | 5 | Deciding the version, waiting on CI, publishing, and keeping dependencies current between releases. | `version-check` `pr-wait` `the-waiting` `npm-publish` `dependency-upgrade` |
| [**codebase-intel**](./plugins/codebase-intel) | 4 | Building an accurate picture of a codebase, and the libraries it leans on, before changing it. | `codebase-health` `codebase-architecture-scanner` `grill-with-docs` `read-the-damn-docs` |

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
"install everything" is a valid choice — it's 35 skills, all inert until their trigger matches.

### Claude Code  (terminal · VS Code extension · JetBrains extension)

```
/plugin marketplace add stylusnexus/agent-plugins
```

Then pick — one, several, or the lot:

```
/plugin install ship-pipeline@stylus-nexus       # just the daily loop
/plugin install hardening@stylus-nexus           # add another whenever
```

Or browse them visually with `/plugin` → **Discover**, which lists all eight with descriptions.

### OpenAI Codex  (CLI · app · IDE extension)

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
```

Codex reads its own index at `.agents/plugins/marketplace.json` — same marketplace, different
schema. Invoke the Codex way: `@ship-pipeline` or `/skills`.

### Everything else — Cursor · Copilot · Gemini CLI · Windsurf · Zed · opencode · Cline · Continue · Hermes · ~60 more

The [Skills CLI](https://github.com/vercel-labs/skills) detects which agents you already have and
writes to each one's skills directory. No marketplace step — one command does both:

```bash
npx skills add stylusnexus/agent-plugins                    # choose interactively
npx skills add stylusnexus/agent-plugins --skill '*'        # all 35 skills
npx skills add stylusnexus/agent-plugins --skill prove-it   # exactly one
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
| Claude Code / Codex plugin | `/ship-pipeline:prove-it` | Plugins namespace their skills, so two packs can share a skill name without colliding |
| Skills CLI / npm | `/prove-it` | Installed as plain skills, no namespace |

Most skills are **model-invoked** — you don't type them at all. `prove-it` fires when you're
wrapping up work, `read-the-damn-docs` when you touch an unfamiliar API. Typing the name forces it.

### Which packs to take

| Take | If |
|---|---|
| `ship-pipeline` | You want one thing. It's the daily loop. |
| `reporting-comms` | Your agent's output is hard to read, or you'd rather mark a draft up than describe it |
| `hardening` | You're heading for a launch, or touched auth/payments/data-export |
| `second-opinion` | A decision is expensive to get wrong |
| `release-ops` | You publish packages |
| `codebase-intel` | You're new to a codebase, or about to refactor something load-bearing |

`work-plan` and `defect-scan` are tools rather than skill packs — take them if you want GitHub-issue
planning or a defect scanner specifically.

### Updating and removing

```bash
npx skills update                                    # Skills CLI installs
```

```
/plugin update ship-pipeline@stylus-nexus            # Claude Code
/plugin uninstall ship-pipeline@stylus-nexus
/plugin marketplace remove stylus-nexus
```

```
codex plugin remove ship-pipeline@stylus-nexus       # Codex
codex plugin marketplace remove stylus-nexus
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

The **six skill packs** are plain markdown, so they reach every agent the Skills CLI supports.
**work-plan** and **defect-scan** ship executable code and install from their own repositories.

| Agent | Skill packs | Tool plugins | Invoke as |
|---|---|---|---|
| **Claude Code** (CLI · VS Code · JetBrains) | `/plugin install <pack>@stylus-nexus` | `/plugin install work-plan@stylus-nexus` | `/ship-pipeline:prove-it` · `/work-plan:brief` |
| **Codex** (CLI · app · IDE) | `codex plugin add <pack>@stylus-nexus` | `codex plugin add work-plan@stylus-nexus` | `@ship-pipeline` · `/skills` |
| **Cursor** | `npx skills add stylusnexus/agent-plugins` | clone + `install.sh` + `.cursorrules` shim | `/prove-it` · `python3 …/work_plan.py` |
| **GitHub Copilot** | `npx skills add stylusnexus/agent-plugins` | clone + `install.sh` + copilot-instructions shim | `/prove-it` · direct CLI |
| **Gemini CLI · Windsurf · Zed · opencode · Cline · Continue · Hermes · Goose · Warp · Amp · Junie · Roo · Qwen Code · Trae · Aider · +more** | `npx skills add stylusnexus/agent-plugins` | — | `/prove-it` |
| **Any other / terminal** | `npx skills add stylusnexus/agent-plugins -a universal` | clone + `install.sh` | `/prove-it` · direct CLI |

Update skill-pack installs with `npx skills update`; plugin installs with `/plugin update` or the
Codex equivalent.

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
│   └── release-ops/
├── scripts/
│   ├── check-manifest-sync.sh   # the two indexes must agree
│   └── check-skills.py          # every SKILL.md must actually load
├── LICENSE
└── README.md
```

Both indexes list the same plugins. Plugins hosted in their own repositories are **pinned to a
release tag**, so Claude and Codex install identical, reproducible versions; plugins that live in
this repository are referenced by relative path and version through their own `plugin.json`.

---

## Prerequisites

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

## Security

- **No token storage.** The toolkit reuses your existing `gh auth` — it never reads, writes, or stores GitHub credentials.
- **Public-repo guard.** Every write to a public repo (or unknown visibility) is gated behind a confirm-token flow. The CLI prints `{needs_confirm: true, token: …}` and exits without writing. The VS Code viewer surfaces this as a **"Write anyway / Keep private"** modal. Private repos write straight through.
- **Local-only writes.** All mutations go to local markdown files — GitHub is never written (except the opt-in `suggest-priorities --apply` for priority labels).
- **No telemetry, no daemon.** No cache, no sync loop — `git pull` is the sync mechanism for shared tracks.

## Versioning & releases

Plugins use **CalVer** (`YYYY.MM.DD+<sha>`), auto-bumped on deploy and synced into both manifests.
Each marketplace entry is **pinned to a release tag** (not a moving branch), so installs are
reproducible; updates land when the tag (and this index's `ref`) advance.

## Resources

- Plugin source & issues: [stylusnexus/work-plan-toolkit](https://github.com/stylusnexus/work-plan-toolkit)
- Claude Code plugins: <https://code.claude.com/docs/en/plugins>
- Codex plugins: <https://developers.openai.com/codex/plugins>

## License

MIT © Stylus Nexus Holdings LLC — see [LICENSE](LICENSE).
