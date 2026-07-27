# Stylus Nexus — Agent Plugins Marketplace

![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-7C3AED)
![Codex](https://img.shields.io/badge/Codex-plugin-10A37F)

A plugin marketplace for AI coding agents — **8 plugins, 31 skills**. Installs natively into **Claude
Code** and **OpenAI Codex**, and reaches roughly seventy more agents (Cursor, Copilot, Gemini CLI,
Windsurf, Zed, opencode, Cline, Continue, Hermes and others) through the Skills CLI.

Every skill is repo-agnostic: it detects your repository's conventions rather than assuming its own,
and defers to a repo-local version of itself when your project defines one.

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
| [**ship-pipeline**](./plugins/ship-pipeline) | 7 | The daily loop: read the issue, ground assumptions in the live database, prove it works, review, merge, promote. | `start-issue` `db-truth` `prove-it` `review-merge-pipeline` `deploy` `db-migration-safety` `backup-verify` |
| [**reporting-comms**](./plugins/reporting-comms) | 6 | The last mile — turning agent output into something a person wants to read. Covers both format and prose. | `html` `visual-plan` `visual-recap` `recap-table` `writing-clearly-and-concisely` `human-writing` |
| [**second-opinion**](./plugins/second-opinion) | 5 | One premise: a single model's confident answer is not evidence. | `llm-council` `plan-arbiter` `spec-review` `agent-watchdog` `debug-feedback-loop` |
| [**hardening**](./plugins/hardening) | 5 | The unglamorous pre-launch gates — a missing rate limit, an unsigned webhook, a compromised dependency. | `rate-limit-audit` `exposure-scan` `auth-hardening` `webhook-reliability` `privacy-audit` |
| [**release-ops**](./plugins/release-ops) | 4 | Deciding the version, waiting on CI, publishing, and keeping dependencies current between releases. | `version-check` `pr-wait` `npm-publish` `dependency-upgrade` |
| [**codebase-intel**](./plugins/codebase-intel) | 4 | Building an accurate picture of a codebase, and the libraries it leans on, before changing it. | `codebase-health` `codebase-architecture-scanner` `grill-with-docs` `read-the-damn-docs` |

### Tool plugins

Two plugins ship executable code rather than markdown, so they live in their own repositories.

| Plugin | What it does |
|---|---|
| [**work-plan**](https://github.com/stylusnexus/work-plan-toolkit) | Track-aware daily planning over GitHub issues — shared git-synced tracks optionally pinned to a canonical plan branch, AI clustering, coverage, doc liveness, and dependency-aware next-up. Pure-stdlib Python CLI plus an accessible VS Code viewer with a repo-qualified dependency graph and confirm-gated writes. |
| [**defect-scan**](https://github.com/stylusnexus/defect-scan) | Language-aware defect hunter. Detects the stack, triages by risk, runs the real analyzers (ruff/mypy, tsc/eslint, rubocop/brakeman, optionally semgrep/gitleaks/bandit), then reports in confidence tiers across 15 language profiles — correlated against existing issues, with optional issue filing, safe autofix, and a cross-model second opinion. |

### Where to start

If you take exactly one, take **ship-pipeline** — it's the daily loop, and the rest is optional around
it. **reporting-comms** has the broadest appeal outside any one workflow. **hardening** and
**second-opinion** are situational but high-value when they apply. **release-ops** and
**codebase-intel** are deliberately narrow.

These packs have opinions — evidence before "done", detect rather than assume, one rule per owner.
That's useful if you share them and friction if you don't; each README states the opinion plainly
rather than burying it.

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
/plugin install release-ops@stylus-nexus
/plugin install work-plan@stylus-nexus
/plugin install defect-scan@stylus-nexus
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
codex plugin add release-ops@stylus-nexus
codex plugin add work-plan@stylus-nexus
codex plugin add defect-scan@stylus-nexus
```

Invoke skills the Codex way (`@work-plan` / `/skills`). Codex reads the dedicated
`.agents/plugins/marketplace.json` index (it can't parse Claude's marketplace source format).

### Cursor · GitHub Copilot · Gemini CLI · Windsurf · Zed · opencode · Cline · Continue · Hermes · ~60 more

Skill-only plugins (**ship-pipeline**, **reporting-comms**, **codebase-intel**, **second-opinion**, **hardening**, **release-ops**) install anywhere via the
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
