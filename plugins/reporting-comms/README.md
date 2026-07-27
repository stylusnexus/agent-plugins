# Reporting & Comms

Six skills for the last mile: turning what an agent produced into something a person actually wants to read.

Agents are good at generating volume and bad at presentation. These skills cover both halves of the problem — the *format* (a self-contained HTML artifact, an interactive plan, a comparison table) and the *prose* (removing AI tells, corporate register, and padding).

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

---

## Rule ownership

Each concern has one owner, so six skills don't all fire on the same prompt.

| Skill | Owns |
|---|---|
| `html` | Static report rendering — the single-file artifact and its layout |
| `visual-plan` | Forward-looking documents: plans, proposals, open questions |
| `visual-recap` | Backward-looking documents: what a diff, PR, or branch actually changed |
| `recap-table` | Tabular comparison — before/after, what-changed — inline, not a rendered page |
| `writing-clearly-and-concisely` | Concision and structure: cutting, ordering, sentence mechanics |
| `human-writing` | Register and voice: removing AI tells and corporate tone |

The pairing worth keeping straight: **`writing-clearly-and-concisely` decides what to cut; `human-writing` decides how what remains should sound.** Run them in that order — tightening after a voice pass usually undoes it.

`visual-plan` and `visual-recap` split on direction of time. If you want a page about work not yet done, that's `visual-plan`; work already done, `visual-recap`. `recap-table` is the lightweight alternative to either when a table answers the question.

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install reporting-comms@stylus-nexus
```

Skills are namespaced: `/reporting-comms:html`, `/reporting-comms:recap-table`.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add reporting-comms@stylus-nexus
```

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins --skill '*'
```

Skills arrive un-namespaced on this path, so they invoke as `/html`, `/recap-table`.

## License

MIT © Stylus Nexus Holdings LLC — see the [repository LICENSE](../../LICENSE).
