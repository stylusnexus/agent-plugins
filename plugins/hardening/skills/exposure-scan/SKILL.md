---
name: exposure-scan
description: Scan installed packages against bumblebee threat-intelligence exposure catalogs to detect known-compromised dependency releases from supply-chain campaigns. Use when checking for compromised packages, running a supply-chain or dependency security scan, auditing the machine after a reported npm/PyPI/Go/gem/extension compromise, or refreshing threat-intel catalogs.
---

# Exposure Scan

Machine-wide supply-chain check. Runs [bumblebee](https://github.com/perplexityai/bumblebee) to inventory every installed package (npm, Go, PyPI, RubyGems, MCP servers, editor + browser extensions) and match them against maintained **exposure catalogs** of known-compromised `(ecosystem, name, version)` releases. Emits findings only when a real match exists.

This is a personal/machine-level tool — it is global on purpose, not tied to any project.

## When to use

- "Am I running any compromised packages?" / supply-chain audit
- After news of an npm/PyPI/Go/gem or VS Code extension compromise — refresh catalogs, then scan
- Periodic hygiene check (`quick` is the fast option)

## Prerequisites (one-time)

`bumblebee` must be installed and on PATH:

```bash
go install github.com/perplexityai/bumblebee/cmd/bumblebee@9d22570f364a667eaf4dd11d1539fc4010edc0e4
# add to ~/.zshrc so it persists:  export PATH="$HOME/go/bin:$PATH"
```

The script auto-adds the directory `go install` writes binaries to (Go's configured bin directory, or else the first `GOPATH` entry's `bin`) to PATH for its own run and prints these instructions if the binary is missing.

## How to run

`scan.sh` ships next to this SKILL.md. Invoke it via a path relative to this skill's own directory:

```bash
bash <this skill's directory>/scan.sh <command>
```

| Command | What it does | Speed |
|---|---|---|
| `quick` (default) | Baseline package roots (the standard global/user dirs) | fastest |
| `deep` | Full `$HOME` walk — catches packages outside standard roots | minutes |
| `project <path>` | Scan one project/dir tree | seconds–minutes |
| `refresh` | Pull the catalogs at the pinned bumblebee commit into `~/.config/bumblebee/threat_intel` | seconds |
| `catalogs` | Show which catalogs are in use + entry counts | instant |

**Recommended flow:**
1. `scan.sh refresh` — get the catalogs for the pinned commit (do this first).
2. `scan.sh quick` — fast match against installed packages.
3. Only escalate to `deep` if quick is clean but you want full `$HOME` coverage, or you're investigating a specific reported compromise.

## Catalog freshness (the one thing to understand)

Both the bumblebee install command and `refresh` use one upstream commit, pinned as `BUMBLEBEE_SHA` in `scan.sh`, so a push to bumblebee's `main` cannot change what is installed or what is matched, and the catalog schema always matches the binary. Threat intel is published on `main` more often than that, so the pin needs bumping to pick up new campaigns: choose a newer commit whose code changes are at least two weeks old (catalog-only commits can be newer), read its diff, update `BUMBLEBEE_SHA`, rerun `go install` with the new SHA, then `refresh`. The script prefers the local cache at `~/.config/bumblebee/threat_intel/` and only falls back to the catalogs bundled in the Go module cache when that cache is empty. Override the cache location with `BUMBLEBEE_CATALOG_DIR`.

## Reading the result

- **`✅ CLEAN`** — no installed package matches a known-compromised release. (This is exact name+version matching, not a general CVE scan — clean here means you dodged these *named campaigns*, not that every dependency is vuln-free.)
- **`🚨 N EXPOSURE FINDING(S)`** — for each: severity, `ecosystem:package@version`, the campaign it belongs to, the evidence, and the exact `source_file` it was found in. Act on these: remove/downgrade the package, rotate any credentials it could have touched, and read the named campaign's report.

## Exit codes

| Exit | Meaning | What to do |
|---|---|---|
| `0` | `✅ CLEAN` — no installed package matches a catalog entry | Report clean, with the caveat above |
| `1` | Error: bumblebee missing, no catalogs, unknown command, `refresh` could not reach GitHub, or the scan ended with no `scan_summary` record and no findings | Fix the setup and rerun; never report this as clean |
| `2` | `🚨 N EXPOSURE FINDING(S)` | Act on the findings as described above |
| `3` | `catalogs` only: the catalog files do not share one `schema_version` | Run `refresh`, or remove the odd file out |

bumblebee's [README](https://github.com/perplexityai/bumblebee#output) states that every run ends with a `scan_summary` record, so a run without one is treated as a failed scan, not a clean one.

## Common mistakes

- **Reading CLEAN as "no vulnerabilities".** This is exact name+version matching against catalog entries, not a CVE scan.
- **Scanning with stale catalogs.** Skipping `refresh` checks against whatever intel shipped with the installed bumblebee version, and an old `BUMBLEBEE_SHA` misses campaigns published since that commit.
- **Starting with `deep`.** It walks all of `$HOME` and is slow; `quick` covers the standard package roots.
- **Treating every non-zero exit as findings.** Only exit `2` means findings; exit `1` means the scan did not complete.

## Notes

- Findings-only mode keeps output small; the script never saves the full package inventory.
- bumblebee writes diagnostics (such as configs it could not parse) to stderr, which the script discards. Run the printed `Running:` command directly to see them.
- To inventory everything (not just findings), run `bumblebee scan` directly without `--findings-only`.
