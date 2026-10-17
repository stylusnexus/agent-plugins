---
name: secrets-leak-audit
description: "Use when checking whether API keys, tokens, passwords, or personal data can escape through git history, the client bundle, log lines, error reports, or API response payloads. Triggers: pre-launch review, a key found in a commit, a .env file that may have been tracked, a new public-prefixed environment variable (NEXT_PUBLIC_, VITE_, EXPO_PUBLIC_), a new logger or error-reporting integration, or a 'what does the client actually receive' question."
---

# Secrets Leak Audit

## Overview

Secrets leave through four doors, and most teams guard one. This audit checks all four against the code and the built artifacts, not against the team's memory of what is safe: **git history**, the **client bundle**, **logs and error reports**, and **API responses**. A finding in any door is treated as a live leak until proven otherwise, and a secret that ever touched git is rotated, not deleted.

Repository-level static analysis and secret scanning belong to `defect-scan` (semgrep, gitleaks, bandit, brakeman) when that plugin is installed; this skill covers what those tools cannot see, the built output and the runtime channels, and tells you what to do with a hit. Check for a repo-local secrets policy first (`AGENTS.md`, `SECURITY.md`, a repo-local `secrets-leak-audit` skill); it is authoritative when present.

Status words: **LEAK** (a secret or personal data is exposed, confirmed from source, history, or a capture), **CLEAN** (checked with evidence and nothing found), **UNVERIFIED** (the check could not be run). "Confirmed from source, not captured live" is a LEAK with a note; it does not need a capture to count. A door with nothing found and no way to run the check is UNVERIFIED, never CLEAN.

## Workflow

**Prove each search can match before trusting an empty result.** A grep that prints nothing is identical whether the code is clean or the command is broken (bad glob, wrong directory, wrong flag). Before relying on an empty result, run the same command with a known-positive pattern (for example the word `import`) and confirm it prints matches; if it does not, fix the command first.

### Door 1: git history

1. Confirm ignore rules cover every env file variant (`.env*` with an exception for `.env.example`) and that none is tracked. A `.gitignore` containing only `.env` is incomplete. No output from the second command is the clean result:
   ```bash
   grep -nE '^\.env' .gitignore
   git ls-files | grep -iE '(^|/)\.env(\.|$)|credentials|secrets?\.(json|ya?ml)$|\.mcp\.json$'
   ```
2. Scan the full history, not just HEAD. **Run both scanners when available; a clean `gitleaks` result does not clear the door**, because detectors miss placeholder-looking or unusual keys and connection strings. Write reports to a private temporary directory, not a shared one:
   ```bash
   REPORT_DIR=$(mktemp -d)
   command -v gitleaks >/dev/null && gitleaks detect --source . --redact --report-format json --report-path "$REPORT_DIR/gitleaks.json"
   # always: key shapes and credentialed URLs across every revision
   git log -p --all | grep -noE 'AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9_-]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|sk_live_[0-9a-zA-Z]{24,}|ghp_[0-9a-zA-Z]{36}|whsec_[0-9a-zA-Z]{32,}|re_[0-9a-zA-Z]{20,}|xox[baprs]-[0-9A-Za-z-]{10,}|-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY|[a-z][a-z0-9+.-]*://[^:/[:space:]]+:[^@[:space:]]+@' | sed -E 's/^([0-9]+:)(.{8}).*/\1\2...<redacted>/' | head -40
   ```
   `-o` with the mask keeps the key itself out of the transcript: only the line number and the first eight characters print.
   Also read `git log -p -- .env` and any `.env*` or config file that ever appeared in `git ls-files` output, since a deleted file's contents are in history.
3. **Any hit in history is a burned secret.** Rotate it at the provider first, then remove it from history (`git filter-repo`) only if the repo is or may become public. Removal without rotation is theater.

### Door 2: client bundle

4. Build for production and grep the output, not the source. Frameworks inline anything with a public prefix, and a secret given a public prefix "to make it work" ships to every browser. If a build is not possible here, grep the source for public-prefixed variables instead, report the bundle as UNVERIFIED, and still report a public-prefixed variable that authenticates to a paid or privileged API as a LEAK:
   ```bash
   npm run build 2>/dev/null
   grep -rnoE 'NEXT_PUBLIC_[A-Z0-9_]+|VITE_[A-Z0-9_]+|EXPO_PUBLIC_[A-Z0-9_]+|REACT_APP_[A-Z0-9_]+' .next/static dist build 2>/dev/null | sort -u
   grep -rnoE 'sk-[A-Za-z0-9_-]{20,}|sk_live_|AKIA[0-9A-Z]{16}|whsec_|-----BEGIN' .next/static dist build 2>/dev/null | head
   ```
5. For each public-prefixed variable, write down why the browser needs it. Publishable keys (Stripe `pk_`, PostHog project key, Sentry DSN) are fine by design. Anything that authenticates the server to a paid or privileged API is not, and moves behind a server route.

### Door 3: logs and error reports

6. Find every log and error-capture call that includes a request, header, body, credential, or user object anywhere in its arguments. List the source directories first (`git ls-files | cut -d/ -f1 | sort -u`) rather than assuming `src`, because grep returns the same nonzero exit for "no matches" and "directory missing":
   ```bash
   grep -rnE '(console|logger|log)\.\w+\(.*\b(req|request|headers|body|ctx|user|session|token|password|authorization|cookie)\b' --include='*.js' --include='*.mjs' --include='*.ts' --include='*.tsx' --include='*.py' --include='*.rb' --include='*.go' --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git .
   grep -rnE 'JSON\.stringify\((req|headers|body|user|session)' --include='*.js' --include='*.mjs' --include='*.ts' --include='*.tsx' --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git .
   ```
   Headers carry `Authorization` and cookies; bodies carry passwords and OTPs; user objects carry email and hashes. Replace whole-object dumps with named, allowlisted fields.
7. Check the error reporter scrubs before send. Sentry, Bugsnag, and Rollbar each have a before-send hook; confirm it strips `Authorization`, `Cookie`, `Set-Cookie`, password and token fields, and that `sendDefaultPii` or its equivalent is off unless the privacy policy says otherwise.
8. Trigger one real error on staging with a fake token in the request and read the captured event end to end. The configuration is not evidence; the captured event is.

### Door 4: API responses

9. Inventory what the client receives. List every place a response is built, then read each one for what it returns. Query calls with no `select`, and whole-object serialization, are the signals:
   ```bash
   grep -rnE '(Next)?Response\.json\(|res\.(json|send)\(|return json\(' --include='*.js' --include='*.mjs' --include='*.ts' --include='*.tsx' --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git .
   grep -rnE '\.(findMany|findFirst|findUnique)\(' --include='*.js' --include='*.mjs' --include='*.ts' --include='*.tsx' --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git . | grep -v 'select'
   ```
   A route returning a database row without an allowlisted field list, or without an authorization check in front of it, is a finding even when no secret field name is visible in the grep.
   Fields that never belong in a response: password hashes, reset or verification tokens, API keys, internal foreign keys the client has no use for, other users' email addresses, Stripe customer IDs on public endpoints.
10. Capture real responses on staging for the three most data-heavy endpoints and read them as an attacker would. A field is a leak if it is present and the UI does not render it.

## Checklist

- [ ] `.env*` ignored and no env or credential file tracked
- [ ] Full history scanned; every hit rotated at the provider, not just removed
- [ ] Production bundle grepped; every public-prefixed variable justified in writing
- [ ] No whole-object logging of requests, headers, bodies, or users
- [ ] Error reporter scrub verified by a captured staging event
- [ ] No unbounded selects or raw model serialization on client-facing routes
- [ ] Real responses captured for the three heaviest endpoints and read field by field

## Output

One table, four doors as rows: what was scanned, the command, hits, action taken or required (rotated / removed / justified / scrubbed), status (LEAK / CLEAN / UNVERIFIED). Attach the raw command output, redacted, and the captured error event and API responses where captures were possible. List anything noticed outside the four doors (a credentialed MCP config, a secret in a prompt, a workflow token) under "Noticed" with the sibling skill that owns it; do not drop it. The checklist items map onto the doors: items 1 and 2 to Door 1, 3 to Door 2, 4 and 5 to Door 3, 6 and 7 to Door 4.

## Common mistakes

- **Scanning HEAD only.** The secret was committed in March and removed in April. It is still in `git log -p`.
- **Deleting instead of rotating.** Anyone who cloned, forked, or cached the repo has the key.
- **Trusting the prefix.** `NEXT_PUBLIC_ANTHROPIC_KEY` compiles and works. That is the problem.
- **Logging the request "just in dev".** The condition gets flipped, or the dev logger ships. Scrub unconditionally.
- **Reading the config instead of the event.** A `beforeSend` that returns the event unchanged looks identical in a code review. Without a capture, an error reporter with default PII enabled and no scrub hook is still a LEAK from config; the captured event upgrades it from "configured to leak" to "observed leaking".

## Stop conditions

Stop means: record the finding, finish the remaining doors read-only, and put the required rotation at the top of the report. The reviewer does not rotate keys unless the owner asked.

- A live secret is found anywhere in history or a bundle: rotation is the first required action; history cleanup comes after.
- A public-prefixed variable authenticates to a paid or privileged API: stop, this blocks launch until the call moves server-side.
- The error reporter captures `Authorization` or `Cookie` headers: stop and fix the scrub before the next deploy.
