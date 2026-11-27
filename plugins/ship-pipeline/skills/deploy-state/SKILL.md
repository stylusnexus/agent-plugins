---
name: deploy-state
description: "Use when someone asks what is lined up for the next deployment or release, what is merged but not live, what is waiting to ship, or to put together a batch of issues or pull requests to deploy."
metadata:
  argument-hint: "[--no-save]"
---

# Deploy state

Answer one question: **what goes out in the next deployment, and what stands in its way?** The lineup includes work that is planned for it, even if not built yet. Check it live. A saved list, an issue comment or your memory of the session is a claim to verify, never the answer.

If the current repo has its own `.claude/skills/deploy-state/` or `.agents/skills/deploy-state/`, that version is authoritative. Follow it instead.

**Read-only**, with one exception: saving the lineup file after the user agrees (step 5). Never merge, push a branch, close an issue or deploy from this skill.

## 1. Learn the repo's release rules

Read the agent instructions (`AGENTS.md`, `CLAUDE.md`), any deploy runbook or deploy skill, and the CI workflows. Find:

- **Branches:** which one is integration and which one production deploys from. Confirm with the host's config or CLI where you can; do not assume `dev` and `main`.
- **Release-size rules:** minimum or maximum pull requests per release, daily caps, named exceptions. Check for a script or CI job that enforces them, and read the script: it can be stricter than the written guide.
- **Order rules:** database migrations, feature flags, anything that must ship before something else.

A rule you could not find is `Not found`, not "none". When a rule uses a word it never defines (for example "large"), say it is undefined, give the numbers, and ask; do not decide it yourself.

## 2. Find what is live and what is waiting

Fetch first with a plain `git fetch <remote>` (do not prune or delete refs). Then collect five groups.

| Group | How to find it |
|---|---|
| **On integration, not live** | First compare the two trees: `git diff --stat <prod> <integration>`. Empty means nothing is waiting. Otherwise list what merged since the commit the last release actually shipped: the head of the last pull request merged into production that carried code. A version-bump or changelog bot pull request is not that release. |
| **Open pull requests** | Target branch, draft state, mergeable state and check results for the current head commit. |
| **Unpushed local work** | Branches and worktrees with unfinished work that exists only here. Name them as local only (see below). |
| **Asked for, not finished** | Work that is part of an active goal, or that the user asked to have implemented: from this conversation, the saved lineup, and any goal or plan file the repo's instructions name. It can be planned for the next deployment before it is built. An open issue alone is not a request. |
| **Deploying now** | A release merged but not yet confirmed live on every service. Use the host's CLI or API when the repo has one; otherwise report `Not found`. |

- After squash merges, `<prod>..<integration>` and "ahead by N" overcount. Trust the tree diff and merged pull requests.
- The same applies to local branches: most "unpushed" commits are leftovers of squash merges. For each recent branch, check whether a merged pull request has that branch and head (`gh pr list --state merged --head <branch> --json headRefOid`) before listing it. Say how far back you looked.
- If the only difference from production changes nothing a user would notice (notes, plans, internal docs), say so.
- Read each open pull request's body and latest comments, not only its status: holds such as "do not merge yet", required backups and owed checks live there.
- To see whether checks ran on a current base, test `git merge-base --is-ancestor <remote>/<integration> <head>`; if it fails, say the checks ran on an older base.
- A mergeable state of `UNKNOWN`, checks that ran on an older head or older base, or checks that never ran mean **unverified**, not clean.
- An issue note such as "still to build" or "not live yet" goes stale. Before repeating it, check the production branch and open pull requests.

## 3. Compare with the saved lineup

Look for a saved lineup in this order: a path the repo's instructions name, `.work-plan/next-deploy.md`, `docs/next-deploy.md`.

If one exists, compare it with step 2 and report every difference: listed but already live, listed but missing or closed, waiting but not listed.

If none exists, **say so**, then propose one:

1. Built work first: merged to integration, then open pull requests closest to ready.
2. Then work the user asked for or put in an active goal, whether or not it is built yet. Include it as **planned**, with what is left before it can ship.
3. Then other urgent open issues, from one priority source in this order: the list the repo's instructions name (such as a launch list), else the release milestone, else priority labels. Show at most ten and say how many more there are. Write **build status not checked** unless you checked the production branch, open pull requests and local branches; an open issue or its label does not prove nothing is built.
4. Fit the group to the release-size and order rules. If no group fits, say which rule blocks it and give the closest options. Never relabel work (calling small changes large, or a routine change urgent) to get past a rule.

## 4. Report

Lead with one line: what the next deployment is, or that no lineup is set. Then one table:

| Item | What users get | State | Before it can ship |
|---|---|---|---|

- **State** is one of: on integration · PR ready (checks passed on current head and base) · PR unverified · PR failing · PR draft · PR conflicting · held (quote the hold) · local only · planned, in progress · planned, not started · not built (checked) · build status not checked. A planned item is part of the lineup but never counts as ready: say what is left, and note whether the release could go without it. Count only built work against release-size rules, and say how the count changes when planned items land.
- Below it, list what is waiting for later and why, then the rules that shape this release (size, order, deadlines).
- Describe changes by what a user sees, with the PR or issue number.
- Say what you did not check.

Example, invented data:

```text
No saved lineup. Proposed next deployment: 2 changes on dev plus 1 PR (the size rule needs 5-10, or 2-3 large).

| Item              | What users get          | State          | Before it can ship              |
| #41 export limits | Larger exports          | on integration | nothing                         |
| #44 sign-in fix   | Fewer failed sign-ins   | on integration | nothing                         |
| #47 saved filters | Filters stay after exit | PR unverified  | rerun checks; migration after 0912 |
| #52 bulk delete   | Delete many at once     | planned, not started | build, review, checks      |

Rule problem: 3 changes, only #47 is large. Options: wait for 2 more small PRs, or ship #44 alone if it qualifies as a named exception.
Later: #60 (open issue, not requested).
Not checked: whether #41 works on the live host.
```

## 5. Ask before saving

Before asking, settle two things:

1. **The exact path:** the saved lineup found in step 3, else `.work-plan/next-deploy.md` when `.work-plan/` exists, else `docs/next-deploy.md`. A path the repo's instructions name wins.
2. **Who could read it once committed:**
   - **Repository visibility** (for example `gh repo view --json visibility`). In a public repository, anyone can read the file in any folder.
   - **Published folders:** the GitHub Pages source (`gh api repos/OWNER/REPO/pages`), deploy workflows, and site configs (`mkdocs.yml`, `docusaurus.config.*`, `_config.yml`) that include the folder. A private repository can still publish a public site.

Ask the user with the question tool if the host has one (`AskUserQuestion` in Claude Code), otherwise in a short numbered list. The question must:

- name the exact path;
- say when the file could become public, and why (public repository, or published folder);
- say "not checked" for whichever of the two you could not check, never "private";
- say they can name a different path in the repo's instructions.

Offer: save this lineup, change it, or don't save. Put the recommended option first. When the folder is published, never recommend saving there: recommend an unpublished path or not saving.

Save only after a yes, to that path. Write the date, the integration and production commits you checked, the items with their states, and open decisions. With `--no-save`, skip this step. Committing or pushing the file needs its own yes unless the repo's instructions already allow it.

## Common mistakes

| Mistake | Instead |
|---|---|
| Listing pull requests as ready without checking the current head | Mark them `PR unverified` |
| Repeating an issue note about what is built or live | Check the branch and the pull requests |
| Learning the release-size rule when CI fails | Read the enforcing script in step 1 |
| Ignoring migration dates | A change dated earlier than one already live may be refused: list the order |
| Leaving out finished local work | List it as `local only` |
| Leaving out requested work because it is not built | List it as `planned` |
| Treating every open issue as planned | Only goal items and explicit implementation requests |
| Asking to save without showing where, or who could read it | Name the path; say if the repository or folder is public, or that you did not check |
