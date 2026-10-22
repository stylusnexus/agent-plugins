# Contributing

This repo is a plugin marketplace for AI coding agents: nine markdown skill packs under
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
5. Add a compatibility entry for the skill to `compatibility.json` (a level for Claude
   Code, the Claude app, Codex, ChatGPT and other agents, with a note for every `partial`
   or `no`), then add its badge line, any limits line, and its row in the pack README's
   **Compatibility at a glance** table. `python3 scripts/check-compat.py` prints the exact
   lines it expects.
6. Add the skill's entry to the pack README's `## What it looks like` section: a collapsed
   `<details>` block whose body starts with the badge line, then the limits line if any,
   then the **Use it when:**, **Try:** and **Skip it when:** lines, then the example.
7. Run `python3 scripts/gen-skill-readme.py` to write the skill's own `README.md`. It copies
   the description from `SKILL.md`, the badges, usage lines and example from the pack README,
   and builds the install steps from `compatibility.json`. Edit those sources, not the text
   between the `<!-- skill-readme:begin -->` and `<!-- skill-readme:end -->` markers; text you
   add outside the markers is kept. `SKILL.md` must not link to the README: it is a supporting
   file for people, not for the agent.
8. Run the checks locally (below) before opening a PR.

## Adding a new pack

Same as above, plus:

- `plugins/<pack>/.claude-plugin/plugin.json` and `plugins/<pack>/.codex-plugin/plugin.json`
  (Claude Code and Codex read separate manifest shapes — copy an existing pack's pair
  and adjust `name`, `description`, and `keywords`).
- An entry in **both** `.claude-plugin/marketplace.json` and
  `.agents/plugins/marketplace.json`. These two indexes must stay in sync — a pack
  listed in one and not the other installs silently for one harness and not the other.
- `plugins/<pack>/README.md` following the shape of an existing pack: a skills table,
  a rule-ownership table, a `## What it looks like` section (where the compatibility
  table and badges go), install instructions, prerequisites.
- A row in the root `README.md`'s pack table, and the headline skill/plugin counts
  updated to match.

## Skill-writing conventions

- Repo-agnostic: a skill should detect a project's own conventions rather than assume
  its own, and defer to a repo-local override of itself when one exists (see any
  `ship-pipeline` skill for the pattern).
- Self-contained: a skill reads nothing outside its own folder, because a single-skill install
  or a Claude app upload has only that folder. Scripts live in the skill's own `scripts/`. If
  several skills need one file, keep a canonical copy in the owning skill, bundle a copy in each
  reader's `references/`, and add the pair to `scripts/check-shared-sync.sh`, which fails CI when
  they drift. A skill that depends on a plugin agent bundles the agent's brief the same way
  (`mk-audience/references/audience-scout-brief.md`) and says what to do when the agent is absent.
- Only Agent Skills frontmatter keys at the top level (`name`, `description`, `license`,
  `compatibility`, `metadata`, `allowed-tools`); the Claude app rejects any other key, so host-specific
  keys go under `metadata:`. `scripts/check-skills.py` enforces this.
- No private or copied third-party material. If you're drawing on a public source
  (a spec, a vendor's docs, a published algorithm), cite it in the skill text or a
  `references/` file rather than presenting it as original.
- No owner-private names, products, or internal paths in skill or agent text — this
  ships to every installer. `scripts/check-private-terms.sh` enforces this against
  `scripts/private-terms.txt`, plus a private list the maintainers hold. A PR can
  also get a warning that a line may use a private product's vocabulary: that
  isn't a failure, but check the line was written for this repo and not lifted
  from elsewhere. The root README and Pages site use the same private overlay;
  only the exact reviewed public-marketplace attribution in the README is
  allowlisted. Keep that exception line-specific, and update
  `scripts/test-private-terms.sh` if the public copy changes.

## Running the checks locally

```bash
sh scripts/check-manifest-sync.sh      # the two marketplace manifests agree
python3 scripts/check-skills.py        # every SKILL.md is loadable
python3 scripts/check-links.py         # every relative link/anchor resolves
python3 scripts/check-readme.py        # README tables match plugins/ on disk
python3 scripts/check-compat.py        # compatibility.json covers every skill; badges match it
python3 scripts/gen-catalog.py --check # README catalogue and skills.sh.json are current
python3 scripts/gen-skill-readme.py --check # every skill's README.md is current
sh scripts/check-shared-sync.sh        # bundled copies of shared files match their canonical source
sh scripts/check-private-terms.sh      # no owner-private terms in skill/agent text
sh scripts/test-private-terms.sh       # public-reference allowlist stays narrow
sh scripts/test-plugin-scripts.sh      # any plugin script's own tests pass
npx --yes cspell@10 --no-progress "plugins/**/*.md" "README.md"
```

`npm run lint` runs everything the `hygiene` job in `ci.yml` gates on every PR
(`check-links.py`, `check-readme.py`, `check-compat.py`, `gen-skill-readme.py --check`,
`check-shared-sync.sh`, `test-private-terms.sh`, `check-private-terms.sh`,
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
- After changing a skill's description, its pack README entry or its
  `compatibility.json` entry, run `python3 scripts/gen-skill-readme.py` to
  regenerate the skill READMEs.
- New skills need at least one worked example in the SKILL.md body, not just the
  frontmatter description.
