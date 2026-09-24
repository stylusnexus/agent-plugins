# Contributing

This repo is a plugin marketplace for AI coding agents: six markdown skill packs under
`plugins/`, plus two tool plugins (`work-plan`, `defect-scan`) that live in their own
repositories and are only referenced here. This guide covers the markdown skill packs.

## Adding a skill to an existing pack

1. Create `plugins/<pack>/skills/<skill-name>/SKILL.md`. The directory name is what
   users invoke (`/prove-it`, `/ship-pipeline:prove-it`), so it must match the skill's
   `name:` frontmatter field exactly.
2. Frontmatter must be valid YAML and include both `name` and `description`:

   ```yaml
   ---
   name: your-skill-name
   description: One or two sentences a model uses to decide when to trigger this skill.
   ---
   ```

   The most common way to break this silently: an unquoted `: ` inside a frontmatter
   value. YAML reads that colon-space as a nested mapping and the **whole** frontmatter
   block fails to parse — the skill loads with no name and no description, and a
   model-invoked skill with no description can never fire. Quote any value that
   contains `: `.
3. The file must be named exactly `SKILL.md` (uppercase). `skill.md` resolves on
   case-insensitive macOS but is invisible on Linux and to anything that expects the
   documented filename.
4. Update **both**:
   - the root `README.md` pack table (bump the `#` column and add the skill to the
     `Skills` cell, backtick-quoted)
   - `plugins/<pack>/README.md` (its own skills table, and its rule-ownership table if
     the skill owns a concern)
5. Run the checks locally (below) before opening a PR.

## Adding a new pack

Same as above, plus:

- `plugins/<pack>/.claude-plugin/plugin.json` and `plugins/<pack>/.codex-plugin/plugin.json`
  (Claude Code and Codex read separate manifest shapes — copy an existing pack's pair
  and adjust `name`, `description`, and `keywords`).
- An entry in **both** `.claude-plugin/marketplace.json` and
  `.agents/plugins/marketplace.json`. These two indexes must stay in sync — a pack
  listed in one and not the other installs silently for one harness and not the other.
- `plugins/<pack>/README.md` following the shape of an existing pack: a skills table,
  a rule-ownership table, install instructions, prerequisites.
- A row in the root `README.md`'s pack table, and the headline skill/plugin counts
  updated to match.

## Skill-writing conventions

- Repo-agnostic: a skill should detect a project's own conventions rather than assume
  its own, and defer to a repo-local override of itself when one exists (see any
  `ship-pipeline` skill for the pattern).
- No private or copied third-party material. If you're drawing on a public source
  (a spec, a vendor's docs, a published algorithm), cite it in the skill text or a
  `references/` file rather than presenting it as original.
- No owner-private names, products, or internal paths in skill or agent text — this
  ships to every installer. `scripts/check-private-terms.sh` enforces this against
  `scripts/private-terms.txt`.

## Running the checks locally

```bash
sh scripts/check-manifest-sync.sh      # the two marketplace manifests agree
python3 scripts/check-skills.py        # every SKILL.md is loadable
python3 scripts/check-links.py         # every relative link/anchor resolves
python3 scripts/check-readme.py        # README tables match plugins/ on disk
python3 scripts/gen-catalog.py --check # README catalogue and skills.sh.json are current
sh scripts/check-private-terms.sh      # no owner-private terms in skill/agent text
sh scripts/test-plugin-scripts.sh      # any plugin script's own tests pass
npx --yes cspell@10 --no-progress "plugins/**/*.md" "README.md"
```

`npm run lint` runs everything the `hygiene` job in `ci.yml` gates on every PR
(`check-links.py`, `check-readme.py`, `check-private-terms.sh`,
`test-plugin-scripts.sh`, and `cspell`); `npm run check` runs the
`manifest-sync` job's pair (`check-manifest-sync.sh`, `check-skills.py`).

## Commits and PR titles

PR titles are Conventional Commits — this repo squash-merges, so the PR title
becomes the permanent commit message. Conventional titles keep `git log` and
the changelog readable:

```
type(scope): summary
```

Types: `feat fix chore docs test refactor perf ci build style revert`. Scope is
usually the pack or script name (`feat(hardening): add auth-hardening skill`).
`pr-title.yml` flags a PR whose title doesn't match -- it isn't a required
check on this repo's branch protection, so a mismatched title won't block a
merge unless a maintainer adds it as one.

## Pull requests

- Keep a PR scoped to one pack or one concern where practical.
- If your skill changes the skill set of a pack, run `check-readme.py` — it will
  tell you exactly which README table is now out of sync.
- After changing a pack's skill table, run `python3 scripts/gen-catalog.py` to
  regenerate the root README catalogue and `skills.sh.json`.
- New skills need at least one worked example in the SKILL.md body, not just the
  frontmatter description.
