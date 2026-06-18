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
| **work-plan** | Track-aware daily planning over GitHub issues — shared tracks (git-synced `.work-plan/`, optionally pinned to a canonical `plan-branch`; `push-track` promotes a private track to it), AI clustering (`group`/`auto-triage` with `--limit` for large repos), coverage, `plan-status` doc liveness with drift detection, batched GraphQL fetches, and **dependency-aware next-up** with per-track ordering presets. Pure-Python-stdlib CLI + a theme-aware, accessible VS Code viewer: sidebar tree with a visibility×tier exposure badge, a Mermaid graph with **GitHub-native blocked-by edges**, **per-issue in-progress badge/toggle** and **blocked-by/blocking dependency chips**, **next-up controls** (Set Next-Up + a Set Next-Up Order… preset picker), **proactive auto-slot suggestions** for untracked issues (AI or offline (no AI), with a compare-and-swap collision guard so an assisted write never clobbers a concurrent change), a **Plans view** with confirm-gated frontmatter writes (verdict / acknowledge / drift-baseline) + track↔plan links, fast-fail GitHub auth, a gated GitHub issue-close, and confirm-gated public-repo writes. | [stylusnexus/work-plan-toolkit](https://github.com/stylusnexus/work-plan-toolkit) |

---

## Install by agent

### Claude Code  (terminal · VS Code extension · JetBrains extension)

```
/plugin marketplace add stylusnexus/agent-plugins
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
codex plugin add work-plan@stylus-nexus
```

Invoke skills the Codex way (`@work-plan` / `/skills`). Codex reads the dedicated
`.agents/plugins/marketplace.json` index (it can't parse Claude's marketplace source format).

### Cursor / GitHub Copilot / plain terminal  (no plugin system)

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

| Agent | Install | Invoke as | Update |
|---|---|---|---|
| **Claude Code** (CLI + VS Code/JetBrains ext) | `/plugin install work-plan@stylus-nexus` | `/work-plan:brief` … | `/plugin update` |
| **Codex** (CLI + app + IDE ext) | `codex plugin add work-plan@stylus-nexus` | `@work-plan` / `/skills` | `codex plugin` upgrade |
| **Cursor** | clone + `install.sh` + `.cursorrules` shim | `python3 …/work_plan.py` (alias `wp`) | re-run installer |
| **GitHub Copilot** | clone + `install.sh` + copilot-instructions shim | direct CLI | re-run installer |
| **Any other / terminal** | clone + `install.sh` | direct CLI | re-run installer |

---

## Repository structure

```
agent-plugins/
├── .claude-plugin/
│   └── marketplace.json     # Claude index   (source: github, repo)
├── .agents/plugins/
│   └── marketplace.json     # Codex index    (source: url + policy + category)
├── LICENSE
└── README.md
```

Both indexes list the same plugins, pinned to the same release tag — so Claude and Codex install
identical, reproducible versions.

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
