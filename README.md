# Stylus Nexus — Agent Plugins Marketplace

A plugin marketplace for AI coding agents. Plugins here share one body of skills + a pure-Python CLI,
and install natively into **Claude Code** and **OpenAI Codex**. Other agents (Cursor, Copilot, plain
terminal) install the same toolkit via its script.

> **Plugins ≠ one-format.** Claude Code and Codex have *separate* plugin systems. This repo carries a
> **per-host index** so each tool installs from the schema it understands:
> `.claude-plugin/marketplace.json` (Claude) and `.agents/plugins/marketplace.json` (Codex).

---

## Plugins

| Plugin | What it does | Source |
|---|---|---|
| **work-plan** | Track-aware daily planning over GitHub issues, plus `plan-status` doc/plan liveness. Pure-stdlib CLI + skills. | [stylusnexus/work-plan-toolkit](https://github.com/stylusnexus/work-plan-toolkit) |

---

## Install by agent

### Claude Code  (terminal, VS Code extension, JetBrains extension)

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install work-plan@stylus-nexus
```

Commands are **namespaced** under the plugin:

| Command | Does |
|---|---|
| `/work-plan:brief` | Multi-track daily snapshot |
| `/work-plan:handoff <track>` | Wrap up a work block (session log, next-up) |
| `/work-plan:orient [track]` | Re-orient on a track / cwd |
| `/work-plan:hygiene` | Weekly cleanup (refresh + reconcile + duplicates) |
| `/work-plan:status` | Doc & plan liveness (`plan-status`) |
| `/work-plan:run <subcommand>` | Anything else (`slot`, `close`, `reconcile`, `group`, `init-repo`, …) |

Update: `/plugin update work-plan@stylus-nexus`. Plugin config is shared between the Claude Code CLI
and its IDE extensions, so installing once covers all three surfaces.

### OpenAI Codex  (CLI, app, IDE extension)

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add work-plan@stylus-nexus
```

Invoke skills the Codex way (`@work-plan` / `/skills`). Codex reads the dedicated
`.agents/plugins/marketplace.json` index (it can't parse Claude's marketplace source format).

### Cursor / GitHub Copilot / plain terminal  (no plugin system)

These don't have a plugin marketplace — install the toolkit directly:

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

| Agent | How to install | Invoke as | Auto-update |
|---|---|---|---|
| **Claude Code** (CLI + VS Code/JetBrains ext) | `/plugin install work-plan@stylus-nexus` | `/work-plan:brief` … | `/plugin update` |
| **Codex** (CLI + app + IDE ext) | `codex plugin add work-plan@stylus-nexus` | `@work-plan` / `/skills` | `codex plugin` upgrade |
| **Cursor** | clone + `install.sh` + `.cursorrules` shim | `python3 …/work_plan.py` (alias `wp`) | re-run installer |
| **GitHub Copilot** | clone + `install.sh` + copilot-instructions shim | direct CLI | re-run installer |
| **Any other / terminal** | clone + `install.sh` | direct CLI | re-run installer |

---

## Prerequisites

The toolkit shells out to standard tools — install these **before** first use (the script installer
verifies them; plugin installs assume they're present):

- **`gh`** (GitHub CLI, authenticated: `gh auth login`) — all GitHub state, no tokens stored
- **`git`**, **`python3` (3.9+)**, **`yq` (mikefarah/yq, the Go build — *not* the Python jq wrapper)**

```bash
# macOS
brew install gh git python@3 yq
# Debian/Ubuntu: gh + yq via their official instructions; apt for git/python3
# Windows: winget install GitHub.cli Git.Git Python.Python.3 MikeFarah.yq
```

---

## Versioning & releases

Plugins use **CalVer** (`YYYY.MM.DD+<sha>`), auto-bumped on deploy and synced into both manifests.
Each marketplace entry is **pinned to a release tag** (not a moving branch), so installs are
reproducible; updates land when the tag (and this index's `ref`) advance.

## Notes

- Adding this marketplace is read-only — it registers an install source; nothing runs until you
  `install`/`add` a plugin.
- Issues / source for the work-plan plugin live in
  [stylusnexus/work-plan-toolkit](https://github.com/stylusnexus/work-plan-toolkit).
