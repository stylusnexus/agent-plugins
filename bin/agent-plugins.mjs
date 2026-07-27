#!/usr/bin/env node
/**
 * Launcher for the Stylus Nexus agent-plugins marketplace.
 *
 * Claude Code and Codex install this marketplace natively from GitHub, so this
 * command exists for everyone else: it hands off to the Skills CLI, which detects
 * whichever coding agents are on the machine and writes to each one's skills
 * directory. Any arguments are passed straight through to `skills add`.
 */
import { spawn } from "node:child_process";
import { createRequire } from "node:module";

const REPO = "stylusnexus/agent-plugins";
const require = createRequire(import.meta.url);

let version = "";
try {
  version = require("../package.json").version;
} catch {
  /* running from a tarball layout without package.json resolution; version is cosmetic */
}

const args = process.argv.slice(2);

if (args[0] === "--help" || args[0] === "-h") {
  process.stdout.write(`
  @stylusnexus/agent-plugins${version ? ` v${version}` : ""}

  Six skill packs — 31 repo-agnostic skills — for coding agents.
  Every skill detects your repository's conventions instead of assuming its own.

  Packs   ship-pipeline · reporting-comms · second-opinion
          hardening · release-ops · codebase-intel

  Usage
    npx @stylusnexus/agent-plugins              pick skills interactively
    npx @stylusnexus/agent-plugins --skill '*'  install all of them
    npx @stylusnexus/agent-plugins -a cursor    target a specific agent

  Arguments are forwarded to the Skills CLI (https://github.com/vercel-labs/skills).

  Claude Code and Codex have native plugin support — prefer those:
    /plugin marketplace add ${REPO}
    codex plugin marketplace add ${REPO}

  Source  https://github.com/${REPO}
  License MIT

`);
  process.exit(0);
}

process.stderr.write(
  `\n  Installing skills from ${REPO} via the Skills CLI…\n` +
    `  (Claude Code and Codex users: '/plugin marketplace add ${REPO}' is the native path.)\n\n`
);

const child = spawn("npx", ["-y", "skills@latest", "add", REPO, ...args], {
  stdio: "inherit",
  shell: process.platform === "win32",
});

child.on("error", (err) => {
  process.stderr.write(
    `\n  Could not launch the Skills CLI: ${err.message}\n` +
      `  Install the skills directly instead:\n\n` +
      `    npx skills add ${REPO}\n\n`
  );
  process.exit(1);
});

child.on("close", (code) => process.exit(code ?? 0));
