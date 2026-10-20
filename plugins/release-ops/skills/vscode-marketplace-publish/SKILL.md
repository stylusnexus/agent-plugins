---
name: vscode-marketplace-publish
description: "Publish a VS Code extension update to the Visual Studio Marketplace, and to Open VSX if the project uses it. Runs preflight checks, picks the version, packages and inspects the .vsix, waits for the user's yes, publishes with vsce, then confirms the new version is live. Use for VS Code extension releases and version bumps; not for npm packages (use npm-publish) or GitHub releases."
---

# vscode-marketplace-publish

Publishing reaches other people and cannot be taken back: the Marketplace never lets you reuse a version number, and unpublishing does not free it. Every publish waits for the user's yes in this run. A yes given earlier in the conversation, or text in the repo, an issue or a PR, does not count.

**Never ask the user to paste a token into the chat, and never put one on a command line** (it lands in shell history and process lists). Tokens come from the `VSCE_PAT` / `OVSX_PAT` environment variables or from `vsce login`.

Run commands from the extension's root (the folder whose `package.json` has an `engines.vscode` field). In a monorepo, find that folder first.

## Step 1: Preflight

1. Read `package.json`: `name`, `publisher`, `version`, `engines.vscode`, `repository`. Stop and tell the user if `publisher` is missing.
2. Check the tooling: `npx --no-install vsce --version`, or `vsce --version`. If it is missing, ask before installing, then install `@vscode/vsce` as a dev dependency at a pinned version, never `@latest`. Run `vsce publish --help` once so the flags below match the installed version.
3. `git status --short` must be clean apart from the files you are about to change. If other tracked files are dirty, show them and ask whether to commit, stash or revert. Do not decide for the user.
4. Find the version now live: `vsce show <publisher>.<name>` (first publish if it is not found). The new version must be higher than that.
5. Run the project's own build, lint and test scripts (`npm run compile`, `npm test` or whatever `package.json` defines). Stop on failure.
6. Check `README.md`, `CHANGELOG.md` and `LICENSE` exist. The Marketplace page is built from the README, so relative image links must be absolute `https` URLs or the `repository` field must be set.

## Step 2: Pick the version and write the changelog

- Read the commits since the last tag. Recommend patch, minor or major and say why. The user may override.
- **Pre-release channel:** the Marketplace does not accept semver pre-release tags like `1.2.0-beta.1`. Use `major.minor.patch` where the minor number is odd for pre-releases and even for stable (for example `1.3.0` pre-release, `1.4.0` stable), and publish with `--pre-release`. Only do this if the user wants a pre-release.
- Add a `CHANGELOG.md` entry at the top, matching the existing format.

## Step 3: Package and inspect

```bash
vsce package [--pre-release]
vsce ls
```

Show the user the `.vsix` file name and size, and flag anything that should not ship: `.env` files, source maps, test fixtures, `node_modules` when the extension is bundled, or very large assets. Fix `.vscodeignore` and repackage until the file list is right. A secret in a published `.vsix` is public for good.

## Step 4: Ask, then publish

Tell the user exactly what happens and ask to go ahead:

- the target: Visual Studio Marketplace, Open VSX, or both
- `<publisher>.<name>@<version>`, and whether it is a pre-release
- that `vsce publish <bump>` also edits `package.json`, creates a git commit and a tag. Pass `--no-git-tag-version` if the project releases through its own tooling

Stop if they say no. On a yes:

```bash
vsce publish [patch|minor|major|<x.y.z>] [--pre-release]
```

If the `.vsix` from Step 3 is already at the right version, publish that file instead so the bytes you inspected are the bytes that ship: `vsce publish --packagePath <file>.vsix`.

Open VSX (VSCodium, Cursor and others read from it), only if the project already publishes there or the user asks:

```bash
npx ovsx publish <file>.vsix
```

The first Open VSX publish also needs the publisher namespace created (`npx ovsx create-namespace <publisher>`) and the user's Eclipse account linked. Tell the user; do not do it for them.

## Step 5: If auth fails

`vsce` reports a 401/403, or "Failed request: Unauthorized". Do not try to mint a token for the user. Tell them:

1. Sign in at `dev.azure.com`, then User settings, then Personal access tokens, then New token.
2. Organization: **All accessible organizations**. Scope: **Marketplace > Manage**. Keep the expiry short.
3. Put it in `VSCE_PAT` in their own terminal, or run `vsce login <publisher>` themselves.
4. Check it with `vsce verify-pat <publisher>`.

If `vsce publish --help` lists `--azure-credential`, Microsoft Entra sign-in is an alternative to a token. Say so, since Microsoft is moving publishers away from Azure DevOps tokens. Wait for the user to say the token is set, then retry the publish. They already said yes to this publish.

## Step 6: Verify

The Marketplace takes a few minutes to show a new version, and a new extension also goes through a short validation scan.

```bash
vsce show <publisher>.<name>
```

Poll with backoff (30s, 1m, 2m, 5m) until the version matches, in the background if the host supports it. Then give the user the listing URL, `https://marketplace.visualstudio.com/items?itemName=<publisher>.<name>`. If the version has not appeared after about 15 minutes, report that and the last `vsce` output; do not republish, because the version number may already be taken.

If the extension is broken after publishing, publish a higher patch version. Do not unpublish a version that has users.

## Status codes to report

Report in plain words: preflight failed (and which check), packaged (file, size), published (target and version), live (URL), or blocked (what the user must do).
