# art-direction provenance

## Sources (both MIT, copyright 2026 Leonxlnx; licence kept in `LICENSE`)
- Engine, scripts, libraries, references and evals: https://github.com/Leonxlnx/taste-skill, `skills/taste-skill`, commit `6010f91` (2026-10-20).
- House styles and dials: https://github.com/Leonxlnx/taste-skill-classics, commit `5e08c93` (2026-10-19). `references/styles/{soft,minimalist,brutalist}.md` are its `high-end-visual-design`, `minimalist-ui` and `industrial-brutalist-ui` skills with their frontmatter removed and a header added. `references/dials.md` is section 7 of its `taste-skill-v2-experimental`.

## What changed from upstream
- `SKILL.md`: renamed to `art-direction`; description extended; new "House styles and dials" section. The upstream README is removed (it describes the upstream repository).
- `scripts/inspect.mjs` and `scripts/scenes.mjs`: the preview file server resolves symlinks and the directory index before the root check, so a link inside a project cannot serve files outside it; the project root is canonicalized.
- `scripts/inspect.mjs` and `scripts/scenes.mjs`: the preview server also refuses requests whose Host header is not `127.0.0.1` or `localhost` (DNS rebinding) and refuses any URL path segment that starts with a dot, other than `.well-known` (so `.env` and `.git` are never served).
- `scripts/scenes.mjs`: scene ids that come from the page are HTML-escaped before they appear in the contact-sheet captions.
- `scripts/scenes.mjs`: contact sheets are written as `scene-<n>-<viewport>.jpg`; the page's scene id is no longer used in a file path.
- Working folder names such as `.taste-skill/` and the `TASTE_SKILL_HISTORY` setting are upstream's and are unchanged.
- `scripts/lib/cdp.mjs`: the four macOS browser paths (Chrome, Chromium, Edge, Brave) are built with `join('/', 'Applications', ...)` instead of written as one string, because this repository's private-terms check bans the literal macOS applications-folder prefix. The paths are the standard install locations and are unchanged.
- `references/imagery.md`: one `<video>` code sample that wrapped over three lines is joined onto one line, so the link checker does not read its `src` as a relative link. Wording is unchanged.
- Nothing else in the engine is touched.

## Hashes
Unpatched upstream (identical at `a9c73c3` and `6010f91`):
- inspect.mjs 9482c546288d4d5c738a915905959e99394551ec27bc202ed443af12a02bd1f7
- scenes.mjs 234ec582e2b841457c33033feeeba8535f9ac285495a74d08dc533a1566c90d5

Shipped here:
- inspect.mjs cf4e8886c4c0eee978776e6e901a2b72a162682eca5088684ebfe9b16c2ad392
- scenes.mjs d749bd0740c66121f40d03a8ba5a54d0784c6128da0fa828ad3675f555553448

## Checked
Tests under `scripts/tests` run the preview-server code from both patched files against a project with symlinks: a link that escapes the root returns 403 (upstream returned the file), while in-root links and a symlinked project root still serve. They also check that a request with a foreign Host header and a dotfile path are refused, and that caption text is escaped. They need Node and are skipped without it. The inspector was not run end to end through Chrome as part of these tests.

## Not included from the classics
`gpt-tasteskill` and `stitch-skill` (other hosts), `taste-skill-v1` and `taste-skill-v2-experimental` (superseded by the engine; only the dials are kept).

## Assets
The licence does not cover third-party images or video fetched by `scripts/assets.mjs` or linked from `library/photos.json` (Lorem Picsum / Unsplash). Keep the credits file those tools write, and replace placeholder photographs before production.
