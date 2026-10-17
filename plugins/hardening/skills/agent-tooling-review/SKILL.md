---
name: agent-tooling-review
description: "Use when connecting, auditing, or widening the permissions of tooling an AI agent can call: MCP servers, plugins, skills, database or GitHub connections, API tokens issued to an agent, or an agent that will run unattended (scheduled, looped, event-triggered, background, CI). Triggers: a new MCP or plugin is about to be added, an agent needs write access it did not have, a connection points at production, an unattended job is being set up, or a tool's description changed after approval."
---

# Agent Tooling Review

## Overview

Every MCP server, plugin, and credential handed to an agent is a dependency that can run commands and read files, and the agent cannot tell a legitimate tool description from a poisoned one. The rule is **least privilege from the first connection**: read-only until a task needs write, scoped to the repositories and tables the task touches, production last. Unattended agents get a tighter version of the same review because nobody is watching the next step.

Anything that cannot be checked in the current environment (no network, no registry access, server not safe to start) is marked **UNVERIFIED** in the output. UNVERIFIED never counts as a pass, and a connection whose provenance is UNVERIFIED stays disconnected.

Before starting, check for a repo-local policy: `AGENTS.md`, `CLAUDE.md`, `SECURITY.md`, an approved-tools list, or a repo-local `agent-tooling-review` skill. It is authoritative when present; this skill is the fallback.

## Scope

- **Repository review (default):** connection config checked into or used by the repo, plus CI workflows. Do not read the reviewer's own home-directory config; it would mix personal connections into the repo's inventory.
- **Personal-machine review (only when asked):** add the user-level config for the agent host in question.
- **Tools the app gives its own model** (functions exposed to an LLM inside a product) are out of scope here. Hand them to `llm-app-security` and note the handoff.

State the task that justifies the connections. If none was given, write "Assumed task: ..." and mark task-matching checks as assumed.

## Workflow

### Inventory

1. Find every connection. Read whole files rather than grepping fragments, so arguments and environment blocks are visible, and **redact credential values in anything you print or paste** (show the key name and the scope, never the secret).
   ```bash
   REDACT='s#(://[^:/@]+:)[^@]+@#\1<redacted>@#; s/((token|key|secret|password)[A-Za-z_"]*[=:][[:space:]]*"?)[^",[:space:]${]+/\1<redacted>/I'
   # repo-level agent config, per host; absent files are listed so a missing host is explicit
   for f in .mcp.json .claude/settings.json .claude/settings.local.json .cursor/mcp.json .vscode/mcp.json .codex/config.toml; do
     if [ -f "$f" ]; then echo "== $f"; sed -E "$REDACT" "$f"; else echo "-- absent: $f"; fi
   done
   # CI jobs that run an agent: read each matching workflow in full, redacted
   for f in $(grep -rlE 'claude|codex|gemini|aider|anthropic|openai|--dangerously|allowedTools|skip-permissions' .github/workflows 2>/dev/null); do
     echo "== $f"; sed -E "$REDACT" "$f"
   done
   ```
   A `${{ secrets.NAME }}` reference is a credential: record the secret's name, and mark its scope UNVERIFIED unless the repo documents it or the owner confirms it. Token scope cannot be read from a token value; get it from the provider's token settings page or API, or ask the owner.
   Build a table: connection, host, maintainer or source, transport (stdio local / remote URL), credential held (name and exact scope), environment reached, access level, verdict.

### Per-connection checks

2. **Provenance.** Maintainer, source repository, last release, user count. These need registry or network access; offline, write UNVERIFIED. A remote server with no visible maintainer, or a package published recently by a single maintainer, stays disconnected until someone has read its code or a trusted party vouches for it. Unpinned launchers (`npx -y pkg`, `latest`) are a finding: pin an exact version.

3. **Requested permissions.** Compare what the tools can do against the task. Get the tool list from the server's source, its registry page, or its documentation. **Never start an unvetted server just to list its tools**; that runs its code before the review has happened. If the list cannot be read safely, write UNVERIFIED.

4. **Credential scope.** For each credential, record the exact scope string:
   - GitHub: fine-grained token limited to named repositories and minimum scopes (`contents:read` before `contents:write`). A classic token with `repo`, `workflow`, or `admin:*` is a finding.
   - Database: a role with `SELECT` only, on the schemas the task needs, with a statement timeout. The application's own role is a write role. Credentials inline in a URL in a tracked file are a finding and are also a leak (see `secrets-leak-audit`).
   - Cloud and SaaS: a key for one project or workspace, never account-level or billing-level.

5. **Environment.** Classify from hostnames, project IDs, and variable names (`prod`, `live`, `primary`). If the environment cannot be determined, treat the connection as production. Dev first, staging second, production last and only after the same task has run clean elsewhere. One credential reaching two environments is a production credential.

6. **Tool-description integrity.** Tool descriptions are prompt text the agent obeys. Keep a checked-in snapshot of each approved description and diff it on upgrade:
   ```bash
   mkdir -p .agent-tooling
   # one line per tool: server, tool name, sha256 of its description (paste descriptions from the approved source)
   printf '%s\n' "<server> <tool> $(printf '%s' "$DESCRIPTION" | shasum -a 256 | cut -d' ' -f1)" >> .agent-tooling/descriptions.sha256
   ```
   A hash that changes without a version bump, or a description that gained instructions ("always also call", "ignore previous", encoded text), is tool poisoning: disconnect. For servers whose files are on disk (vendored plugins, local scripts, skill and rules files), also run a deterministic scan; remote servers cannot be scanned this way and stay UNVERIFIED:
   ```bash
   npx @stylusnexus/agentarmor@<exact-version> scan <local-dir-or-file> --fail-on medium
   ```
   The scanner is itself a downloaded package: look up its current version (`npm view @stylusnexus/agentarmor version`), write that exact version into the command and the report, and skip the scan when offline or when there are no local files to scan. A skipped scan is UNVERIFIED.

### Unattended agents

7. When the agent runs without a person watching each step (`/schedule`, `/loop`, cron, webhook, CI), all seven controls are required. A control passes only when fully met; a partial control (a log nobody reads, an approval that can be skipped) is a fail.

   | Control | Pass looks like |
   |---|---|
   | Narrow job | One task, stated in one sentence, with explicit out-of-scope areas |
   | Scoped repository access | Token limited to the repositories the job touches |
   | Least-privilege credentials | Separate from any attended session; read-only where the job only reads |
   | Safe stopping points | On an unexpected state the job stops and reports instead of improvising |
   | Full action log | Every tool call and its arguments recorded where a person will read it |
   | Human approval gate | No merge, deploy, send, post, publish, delete, or payment without a person confirming that specific action; permission-skipping flags are a fail |
   | Blast radius | The worst case with these credentials is written down and acceptable |

   For CI also check: workflow `permissions:` block present and minimal, actions pinned to a commit SHA, agent CLI version pinned, job timeout and concurrency limit set, and untrusted text (issue titles, PR bodies, comments) passed to the agent as quoted data, never as instructions.

### Decide and narrow

8. One verdict per connection: **keep**, **narrow** (state the new scope), **disconnect**. When asked to make changes, apply the narrowing and record it. When the review is read-only, list each change as REQUIRED, leave the checklist item "narrowing applied" open, and say who needs to make the change. Re-review when a task needs wider access and narrow back when it ends.

## Checklist

- [ ] Repo-local policy checked first
- [ ] Every connection and every CI agent job inventoried, credentials redacted in the record
- [ ] Provenance recorded or marked UNVERIFIED; unpinned launchers flagged
- [ ] Each credential's exact scope recorded and matched to the stated or assumed task
- [ ] Environment classified; unknown treated as production
- [ ] Tool descriptions snapshotted and diffed, or marked UNVERIFIED
- [ ] Every unattended job scored against all seven controls
- [ ] Each connection has a verdict; narrowing applied, or listed as REQUIRED with an owner

## Output

The inventory table with a verdict column and exact credential scopes, the seven-control table for each unattended job, and a list of everything marked UNVERIFIED with what would verify it. "Least privilege" without the scope string is unverified.

## Common mistakes

- **Starting wide to save a round trip.** The widening becomes permanent; nobody narrows later.
- **Treating a popular server as vetted.** Popularity measures installs, not review.
- **One token for everything.** A leaked attended-session token should not run the nightly job, and the reverse.
- **Approving once.** Descriptions and permissions change on upgrade; re-check on every version bump.
- **Running the server to inspect it.** That is the exposure the review exists to prevent.
- **Confusing a log with a gate.** Logging a destructive action after it ran is forensics, not control.

## Stop conditions

Stop means: do not connect, widen, or run anything further, record the finding, and finish the report.

- A connection holds production write credentials and no current task needs them.
- A tool description differs from its approved snapshot: disconnect, and treat earlier sessions as suspect until the diff is explained.
- An unattended job can take an irreversible or outward-facing action without a human gate: it does not run until the gate exists.
