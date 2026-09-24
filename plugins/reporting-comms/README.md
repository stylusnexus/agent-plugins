# Reporting & Comms

Seven skills for the last mile: turning what an agent produced into something a person actually wants to read — and getting their judgment back.

Agents are good at generating volume and bad at presentation. These skills cover both halves of the problem — the *format* (a self-contained HTML artifact, an interactive plan, a comparison table) and the *prose* (removing AI tells, corporate register, and padding).

Six of them run agent→human. `redline` runs the other direction: the human marks the artifact up in a browser and the agent applies what comes back.

---

## The skills

| Skill | Use it when |
|---|---|
| `html` | Output is complex enough that a wall of terminal text loses it — plans, code reviews, research, comparisons, configs, reports. Produces one self-contained, reading-first HTML file. |
| `visual-plan` | A text plan would land better as an interactive document: diagrams, file maps, annotated code, open questions, and UI review where it helps. |
| `visual-recap` | A PR, branch, commit, or diff needs explaining — renders it with diagrams, file maps, API and schema summaries, and annotated diffs. |
| `recap-table` | Someone asks "what did you change?" or wants a before/after comparison. Produces the table, not another paragraph. |
| `writing-clearly-and-concisely` | Any prose a human will read — docs, commit messages, error messages, explanations. Applies Strunk's rules and cuts what isn't carrying weight. |
| `human-writing` | Text reads as machine-generated: corporate speak, generic phrasing, the familiar AI cadence. Rewrites toward something conversational and specific. |
| `redline` | The human needs to judge a draft, plan, or report and describing the problems in chat is slower than fixing them. Opens it in a browser for direct editing and anchored comments; returns one Markdown review. |

---

## Rule ownership

Each concern has one owner, so seven skills don't all fire on the same prompt.

| Skill | Owns |
|---|---|
| `html` | Static report rendering — the single-file artifact and its layout |
| `visual-plan` | Forward-looking documents: plans, proposals, open questions |
| `visual-recap` | Backward-looking documents: what a diff, PR, or branch actually changed |
| `recap-table` | Tabular comparison — before/after, what-changed — inline, not a rendered page |
| `writing-clearly-and-concisely` | Concision and structure: cutting, ordering, sentence mechanics |
| `human-writing` | Register and voice: removing AI tells and corporate tone |
| `redline` | The return path — collecting a human's edits and anchored comments off a rendered artifact |

The pairing worth keeping straight: **`writing-clearly-and-concisely` decides what to cut; `human-writing` decides how what remains should sound.** Run them in that order — tightening after a voice pass usually undoes it.

`visual-plan` and `visual-recap` split on direction of time. If you want a page about work not yet done, that's `visual-plan`; work already done, `visual-recap`. `recap-table` is the lightweight alternative to either when a table answers the question.

`redline` splits from all six on **direction**, not subject. The others end when a person starts reading; `redline` starts there. It chains after any of them: render with `html`, mark up with `redline`, apply, repeat.

One rule crosses the pack and is worth stating once: **wording a human typed into a redline is final.** Neither prose skill may rewrite it, and no later editing pass may reflow it away. A skill that "improves" a human's own sentence has overruled the person the review existed to serve.

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install reporting-comms@stylus-nexus
```

Skills are namespaced: `/reporting-comms:html`, `/reporting-comms:redline`.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add reporting-comms@stylus-nexus
```

In Codex, type `$` and a skill name to use it (`$reporting-comms:html`; Codex prefixes plugin skills with the pack name), or run `/skills` to pick one.

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins --skill html human-writing recap-table redline visual-plan visual-recap writing-clearly-and-concisely
```

Skills arrive un-namespaced on this path, so they invoke as `/html`, `/redline`.

## License

MIT © Stylus Nexus Holdings LLC — see the [repository LICENSE](../../LICENSE).
