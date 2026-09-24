---
name: redline
description: "Hand a draft, plan, report, or page to the human to mark up in a browser; Send returns one Markdown review file the agent applies. Use for anything a person must judge rather than a machine - \"let me look at it\", \"let me mark it up\", \"/redline\". Not for machine-checkable correctness (/prove-it, /code-review)."
args: "<file.md | file.html> [--comment-only] [--flags <scan-report>]"
---

# Redline — the human→agent return path

## Overview

Every other review path in this ecosystem runs agent→agent: a second model reads the work and judges it. This one runs the other direction. The human is the judge, and the bottleneck was never their judgment — it's the channel. Describing a wording change in chat costs more keystrokes than making it, and "the third paragraph feels off" throws away the exact phrase that caused the feeling.

`/redline` renders the artifact as a self-contained page where the human edits text directly and attaches comments to exact quotes, then returns one Markdown file with everything anchored.

**No dependencies.** One generated HTML file, everything inline, no network requests, no server, no npm or pip install, nothing to vet. It is the `html` skill's artifact rules plus a review layer.

**If the current repo has its own `.claude/skills/redline/` or `.agents/skills/redline/`, that version is authoritative — follow it instead.** This global version is the fallback.

**Announce at start:** "Opening this for markup — edit and comment in the browser, then hit Send."

**The rule underneath every step**: an edit the human already made is a decision, not a suggestion. Carry their wording verbatim.

## When this fires, and when it doesn't

| Question | Skill |
|---|---|
| Does this document say the right thing? | **`redline`** |
| Does the code work? | `prove-it` |
| Is the diff sound? | `code-review` / `review-merge-pipeline` |
| Is one model's confident answer enough? | `second-opinion` skills |
| Does the output need rendering at all? | `html` — then `redline` its output |

`html` owns producing the page. This skill owns getting judgment back off it. They chain.

Do not reach for this on machine-checkable claims. If a test can answer the question, run the test.

## The three modes

| Mode | Flag | The human can | Use it for |
|---|---|---|---|
| **edit + comment** | default | Type over text, comment on selections | Drafts, plans, reports — anything they'd otherwise describe in chat |
| **comment only** | `--comment-only` | Comment on selections and blocks | Reader-effect passes where rewriting would corrupt the method (see the blind-read note below) |
| **triage** | `--flags <report>` | Sort pre-flagged spans into violation / exception, plus the above | Acting on a scanner's line-anchored output |

Edit mode **downgrades itself to comment-only automatically** when the page renders itself with script — a chart or any scripted DOM. An "edit" captured from a page the script is rewriting is meaningless, and writing it back would corrupt the file. The page says so plainly when this happens.

## Step 1: Build the page

Read `template.html` from this skill directory and substitute four things:

| Placeholder | Value |
|---|---|
| `DOC_TITLE` | The filename the human will recognise, e.g. `draft.md` |
| `SOURCE_PATH` | Absolute path to the **source** file — used as the persistence key |
| `REVIEW_MODE` | `edit` or `comment` |
| `<!--CONTENT-->` | The rendered content |

For a Markdown source, render it to HTML for the content block. **The `.md` file itself is never written by this skill** — edits come back as feedback for you to apply to the source, preserving its syntax.

Write the result next to the source as `<name>.redline.html`, and give regions names — the returned review uses them instead of guessing from the DOM:

```html
<p data-block="Problem body">…</p>
<div data-container="Metrics callout">…</div>
```

Two content rules: escape any literal `</script>` inside the content (it will close the page's own script and break the review), and keep the page self-contained — no remote fonts, images, or scripts.

### Triage mode

To act on a scanner report, wrap each flagged span before injecting:

```html
Prompt-only practice has a <span data-flag="hedge">ceiling</span>, because…
```

Each flagged span becomes a card the human sorts into **violation** or **exception**, with an optional reason. This is the shape `detect-then-repair` Step 2 needs — the returned table already excludes nothing, so read the verdict column and build the repair input from the violations alone.

## Step 2: Open it

| Platform | Command |
|---|---|
| macOS | `open <name>.redline.html` |
| Linux | `xdg-open <name>.redline.html` |
| Windows | `start <name>.redline.html` |

Tell the human what they can do, in one line: type over text to change it, select a phrase to comment on it, then hit **Send**. `Revert edits` restores the page as you left it. Their work survives a reload — it's kept in `localStorage` against the source path.

## Step 3: Wait for Send

Send writes `<name>.redline.md` to their downloads folder. Two ways to pick it up:

- **Default — just wait for them.** Say "tell me when you've hit Send," and read the file on their next message. In a chat harness the human is right there; a blocking poll buys nothing and risks stranding them.
- **Hands-off — watch for the file.** Use `Monitor` (or an equivalent watch) on the expected path so you pick it up without another turn. Do not busy-loop a foreground `sleep`.

The downloads folder is platform-specific — resolve it before you look:

| Platform | Path | Newest review |
|---|---|---|
| macOS / Linux | `~/Downloads` | `ls -t ~/Downloads/*.redline.md 2>/dev/null \| head -1` |
| Windows | `%USERPROFILE%\Downloads` | `dir /b /o-d "%USERPROFILE%\Downloads\*.redline.md"` |

If the human has redirected their browser downloads elsewhere, ask rather than guess.

## Step 4: Apply the review

The returned Markdown is written to be read by a person and parsed by you:

```markdown
## Overall
Tighten the risks section.

## Edits the human already made
### Pull quote
- **before:** Voice accrues from compounded rejections.
- **after:** Voice accrues from the rejections you keep.

## Triage
| flag | text | verdict | why |
|---|---|---|---|
| hedge | ceiling | violation |  |
| em-dash-tell | not just | exception | quoted specimen, ships as-is |

## Comments
### 1. Lede
> grew 40% last quarter

_anchor: …lost context **grew 40% last quarter**, and three teams…_

Cite the source for this.
```

Three rules, in priority order:

1. **`Edits` are already decided — `after` is the human's exact wording.** Apply it verbatim to the source.
2. **`Comments` are anchored to a quote.** Act on the quoted text, not your memory of the document.
3. **`exception` verdicts ship untouched.** The human ruled; a flagged span they called an exception is not yours to fix.

### A human edit is immune to the prose skills

This pack contains skills whose whole job is rewriting prose. Once a human has typed their own wording, it is out of scope for all of them:

- Do **not** run `writing-clearly-and-concisely` over a human's `after` text to tighten it.
- Do **not** run `human-writing` over it to adjust register.
- Do **not** fold it into a later pass that reflows the surrounding paragraph.

They read the sentence in context and chose those words. A skill that "improves" them has silently overruled the person the review existed to serve. If their wording genuinely breaks something — a factual error, a broken build, a compliance problem — say so in chat and leave the text alone until they decide.

### Apply to the source, not the rendered page

The `.redline.html` is disposable. Edits belong in whatever the page was generated *from*:

- Reviewed a `.md`? Apply to that Markdown, preserving its syntax.
- Page built from MDX or Markdown — including anything served out of a `plans/<slug>/` MDX folder? Apply to the **source**, then rebuild. The rendered HTML is a casualty of the next build, not a destination.
- Genuinely hand-authored HTML? Apply there.

If you cannot tell which case you are in, ask before applying — a wrong guess loses their work silently.

## Step 5: Round two

Rebuild the page from the updated source and reopen it. Stop when the human says done, or sends an empty review. Then report what changed — `recap-table` is usually the right shape for "here's what your feedback did."

Delete the `.redline.html` and the downloaded `.redline.md` when the loop ends, unless the review is worth keeping as a record — in a writing practice it often is.

## A note on blind reads

If the artifact is going through a reader-effect review — a blind read, a cold-reader test — use `--comment-only`. Those methods are **report-first, not rewrite-first** by design; putting a cursor in the text invites line-editing and destroys the very thing the read is measuring. Run the blind read comment-only, decide, and only then open an edit-mode pass to act on what it found.
