# Stylus Nexus — Agent Plugins Marketplace

![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-7C3AED)
![Codex](https://img.shields.io/badge/Codex-plugin-10A37F)

A plugin marketplace for AI coding agents. Plugins here share one body of skills + a pure-Python CLI,
and install natively into **Claude Code** and **OpenAI Codex**. Other agents (Cursor, Copilot, plain
terminal) install the same toolkit via its script.

> ⚠️ **Trust before you install.** Plugins run code on your machine. Review a plugin's source before
> installing it. Everything here is open-source — links are in the table below.

> **Plugins ≠ one format.** Claude Code and Codex have *separate* plugin systems, so this repo carries
> a **per-host index**: `.claude-plugin/marketplace.json` (Claude) and `.agents/plugins/marketplace.json`
> (Codex). You add the *same* marketplace either way; each tool reads the schema it understands.

---

## Plugins

| Plugin | What it does | Source |
|---|---|---|
| **second-opinion** | Five skills on one premise: a single model's confident answer is not evidence. `llm-council` runs a question past five advisors who analyse independently before synthesis; `plan-arbiter` compares, judges, and merges competing plans; `spec-review` checks a spec's claims against the real codebase before code embeds a wrong data-model assumption; `agent-watchdog` audits another agent's work from its session or transcript; `debug-feedback-loop` builds a deterministic pass/fail signal for a bug **before** hypothesising. | [`plugins/second-opinion`](./plugins/second-opinion) |
| **hardening** | Five pre-launch gates for the unglamorous security work. `rate-limit-audit` inventories every paid-API and auth endpoint and checks each has a limit; `exposure-scan` checks installed packages (npm, Go, PyPI, RubyGems, MCP servers) against threat-intelligence catalogs for known-compromised releases; `auth-hardening` audits session, cookie, CSRF and OAuth-scope config; `webhook-reliability` covers signature verification, idempotency, retries and dead letters; `privacy-audit` inventories what user data is collected and where it lands, checked against the code rather than the policy. | [`plugins/hardening`](./plugins/hardening) |
| **reporting-comms** | Six skills for the last mile — turning agent output into something a person wants to read. `html` renders plans, reviews, and research as a self-contained HTML artifact; `visual-plan` and `visual-recap` turn text plans and git diffs into interactive documents with diagrams, file maps, and annotated code; `recap-table` produces before/after and what-changed tables; `writing-clearly-and-concisely` and `human-writing` tighten the prose itself and strip AI tells. | [`plugins/reporting-comms`](./plugins/reporting-comms) |
| **codebase-intel** | Four skills for understanding a codebase before changing it. `codebase-health` reports complexity hotspots, churn, and bus factor; `codebase-architecture-scanner` generates layered architecture docs with C4 and sequence diagrams; `grill-with-docs` challenges a plan against the existing domain model; `read-the-damn-docs` grounds third-party API behavior in current documentation instead of recall. | [`plugins/codebase-intel`](./plugins/codebase-intel) |
| **ship-pipeline** | Seven repo-agnostic skills for the ship half of the development loop — `start-issue` (full-issue intake, prior-art check, baseline, branch naming), `db-truth` (ground schema claims in the live database; confirm migrations landed), `prove-it` (end-of-work evidence protocol that emits a claim→command→result table and labels anything unprovable **UNVERIFIED**), `review-merge-pipeline` (verify → review → fix → commit → push → PR → merge, detecting the integration branch instead of assuming one), `deploy` (production promotion with merge strategy inferred from history), `db-migration-safety` (expand-contract, idempotent SQL, batched backfills), and `backup-verify` (confirms backups exist **and restore**). Every skill defers to a repo-local version of itself when the project defines one. | [`plugins/ship-pipeline`](./plugins/ship-pipeline) |
| **defect-scan** | Language-aware defect hunter for Claude Code and Codex. Detects the stack, triages files by risk, runs the real analyzers (ruff/mypy, tsc/eslint, rubocop/brakeman, optionally semgrep/gitleaks/bandit), then reasons over 15 language profiles and reports findings in confidence tiers — correlated against existing GitHub issues, with optional issue filing (`--file-issues`), safe autofix (`--fix`), and a cross-model second opinion (`--cross-model`). | [stylusnexus/defect-scan](https://github.com/stylusnexus/defect-scan) |
| **work-plan** | Track-aware daily planning over GitHub issues — shared tracks (git-synced `.work-plan/`, optionally pinned to a canonical `plan-branch`; `push-track` promotes a private track to it), AI clustering (`group`/`auto-triage`), coverage, `plan-status` doc liveness, and **dependency-aware next-up**. Pure-Python-stdlib CLI + an accessible VS Code viewer with a **repo-qualified dependency graph**, per-issue in-progress/dependency controls, proactive auto-slot suggestions, and a Plans view with confirm-gated writes and **repository-contained plan links**. Shared-tier paths are contained, plan stamping is hard-link safe, and script installers preserve unmanaged or modified launchers through content-verified ownership. | [stylusnexus/work-plan-toolkit](https://github.com/stylusnexus/work-plan-toolkit) |

---

## Install by agent

### Claude Code  (terminal · VS Code extension · JetBrains extension)

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install ship-pipeline@stylus-nexus
/plugin install reporting-comms@stylus-nexus
/plugin install codebase-intel@stylus-nexus
/plugin install second-opinion@stylus-nexus
/plugin install hardening@stylus-nexus
/plugin install work-plan@stylus-nexus
```

…or browse interactively: `/plugin` → **Discover**. Commands install **namespaced** under the plugin:

| Command | Does |
|---|---|
| `/work-plan:brief` | Multi-track daily snapshot |
| `/work-plan:handoff <track>` | Wrap up a work block (session log, next-up) |
| `/work-plan:orient [track]` | Re-orient on a track / cwd |
| `/work-plan:hygiene` | Weekly cleanup (refresh + reconcile + duplicates) |
| `/work-plan:status` | Doc & plan liveness (`plan-status`) |
| `/work-plan:run <subcommand>` | Anything else (`slot`, `close`, `reconcile`, `group`, `coverage`, `auto-triage`, `init-repo`, …) |

Update: `/plugin update work-plan@stylus-nexus`. Plugin config is shared between the Claude Code CLI
and its IDE extensions, so installing once covers all three surfaces.

### OpenAI Codex  (CLI · app · IDE extension)

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
codex plugin add reporting-comms@stylus-nexus
codex plugin add codebase-intel@stylus-nexus
codex plugin add second-opinion@stylus-nexus
codex plugin add hardening@stylus-nexus
codex plugin add work-plan@stylus-nexus
```

Invoke skills the Codex way (`@work-plan` / `/skills`). Codex reads the dedicated
`.agents/plugins/marketplace.json` index (it can't parse Claude's marketplace source format).

### Cursor · GitHub Copilot · Gemini CLI · Windsurf · Zed · opencode · Cline · Continue · Hermes · ~60 more

Skill-only plugins (**ship-pipeline**, **reporting-comms**, **codebase-intel**, **second-opinion**, **hardening**) install anywhere via the
[Skills CLI](https://github.com/vercel-labs/skills), which detects the coding agents you already
have and writes to each one's skills directory:

```bash
npx skills add stylusnexus/agent-plugins                  # pick interactively
npx skills add stylusnexus/agent-plugins --skill '*'      # take everything
npx skills add stylusnexus/agent-plugins -a cursor -a github-copilot   # target specific agents
```

Skills arrive **un-namespaced** on this path, so they invoke as `/prove-it` rather than
`/ship-pipeline:prove-it`. Update later with `npx skills update`.

### work-plan on agents without a plugin system

Install the toolkit directly:

```bash
git clone https://github.com/stylusnexus/work-plan-toolkit
cd work-plan-toolkit && ./install.sh        # macOS / Linux / WSL
#   Windows:               .\install.ps1
#   Codex skills dir:      ./install.sh --target=$HOME/.agents
```

That gives the bare `/work-plan <subcommand>` (or `python3 .../work_plan.py <subcommand>`). For
Cursor/Copilot prompt-engineering shims, see the toolkit's
[README → Compatible tools](https://github.com/stylusnexus/work-plan-toolkit#compatible-tools).

---

## Compatibility at a glance

**Skill-only plugins** (ship-pipeline, reporting-comms, codebase-intel, second-opinion, hardening) reach every agent the Skills CLI supports.
**work-plan** additionally ships a Python CLI + VS Code viewer, so it needs its own installer off the plugin path.

| Agent | ship-pipeline | work-plan | Invoke as |
|---|---|---|---|
| **Claude Code** (CLI + VS Code/JetBrains ext) | `/plugin install ship-pipeline@stylus-nexus` | `/plugin install work-plan@stylus-nexus` | `/ship-pipeline:prove-it` · `/work-plan:brief` |
| **Codex** (CLI + app + IDE ext) | `codex plugin add ship-pipeline@stylus-nexus` | `codex plugin add work-plan@stylus-nexus` | `@ship-pipeline` / `/skills` |
| **Cursor** | `npx skills add stylusnexus/agent-plugins` | clone + `install.sh` + `.cursorrules` shim | `/prove-it` · `python3 …/work_plan.py` |
| **GitHub Copilot** | `npx skills add stylusnexus/agent-plugins` | clone + `install.sh` + copilot-instructions shim | `/prove-it` · direct CLI |
| **Gemini CLI · Windsurf · Zed · opencode · Cline · Continue · Hermes · Goose · Warp · Amp · Junie · Roo · Qwen Code · Trae · Aider · +more** | `npx skills add stylusnexus/agent-plugins` | — | `/prove-it` |
| **Any other / terminal** | `npx skills add stylusnexus/agent-plugins -a universal` | clone + `install.sh` | `/prove-it` · direct CLI |

Update skill-only installs with `npx skills update`; plugin installs with `/plugin update` or the Codex equivalent.

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
│   └── hardening/
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

## Update & uninstall

```bash
# Claude Code
/plugin update work-plan@stylus-nexus
/plugin uninstall work-plan@stylus-nexus
/plugin marketplace remove stylus-nexus

# Codex
codex plugin remove work-plan@stylus-nexus
codex plugin marketplace remove stylus-nexus
```

---

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
