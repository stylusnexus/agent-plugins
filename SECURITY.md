# Security Policy

## Scope

This repository ships **markdown skills that instruct an AI coding agent, and shell
helper scripts those skills can invoke.** The realistic risk surface here is:

- A skill's instructions causing an agent to run a destructive or unsafe shell command.
- A shell script under `plugins/*/skills/*/scripts/` doing something unsafe (unsanitized
  input, unsafe temp-file handling, an unpinned/untrusted download).
- Supply-chain risk in `bin/`, `package.json`, or a GitHub Actions workflow.
- A manifest (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`)
  or `plugin.json` pointing installers at something other than what it claims to.

This repo does not run a server, does not handle user credentials, and does not
process end-user data — most classic web-app vulnerability classes don't apply.

## Reporting a vulnerability

**Please do not open a public GitHub issue for a security report.**

Private vulnerability reporting is enabled on this repository. Use it to report:

1. Go to the repository's **Security and quality** tab.
2. Click **Report a vulnerability** to open the advisory form.
3. Fill in a title and description of the issue — a proof-of-concept skill invocation
   or script input that demonstrates the problem is the most useful thing you can
   include. Affected version/commit and suggested severity are optional but help
   triage.
4. Submit. This opens a private draft security advisory visible only to maintainers
   and repository admins — it does not create a public issue or notify anyone else.

You'll get an acknowledgement, and can continue the conversation privately on the
advisory thread, including collaborating on a fix via the temporary private fork
GitHub offers from that screen if one is warranted.

If private vulnerability reporting isn't available for any reason, open a regular
issue asking a maintainer to reach out for a private channel — don't include exploit
details in that issue.

## Supported versions

This package doesn't maintain long-lived version branches; security fixes land on
the latest published version. If you're on an older tagged release, please update
before reporting to confirm the issue still reproduces.

## Disclosure

We'll credit reporters (unless you ask not to be) once a fix is published. There's
no bug bounty — this is an open-source marketplace, not a funded program.
