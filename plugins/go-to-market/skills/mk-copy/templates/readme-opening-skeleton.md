# README opening skeleton

Fill-in form for a README's opening section, derived from [extractable-section writing](../references/extractable-writing.md). Treat this as the project's actual landing page — a stranger who reads only this section should understand and be able to act on it. Delete every instruction line (in *italics*) once its field is filled.

## Title and one-line description

- **Project name:** →
- **One sentence, plain value proposition:** *What does this do, for whom, stated as a concrete action — not "empower your workflow."*
  →

## Opening paragraph

*Open with a real subject and a real verb — not a pronoun that only makes sense after reading something earlier. State the one claim this project makes in the first sentence; put caveats and detail after it. Before or alongside that claim, say in one real sentence why the problem is worth a reader's time — a concrete cost or friction it causes, not an adjective ("slow," "painful") standing in for one. Define any acronym or piece of jargon the first time this section uses it.*

→

## What it does (concrete, not abstract)

*One or two sentences a reader could act on immediately — a command to run, a problem it solves, a before/after.*

→

## Quick start

*The smallest real example that shows the thing working. Real command, real output — not a description of what it would show.*

```
[real install/run command]
```

→ (real, checkable output or result)

## Real evidence this works

*Only if it exists and is real: a real badge (build status, downloads or GitHub star count from an actual public counter — link it so it's checkable, don't restate the number as static text that goes stale), a real link to it in use, a real user's own words with their permission. This is where a star count belongs, if used at all — never in the opening paragraph or one-line value proposition above, where it would read as a claim about the product rather than a checkable proof point. Omit the section entirely rather than filling it with something unverified — an unsourced popularity or usage claim is worse than no claim.*

→

## Claim → source table

| Claim in this README | Source |
|---|---|
| | |

---

### Example (fictional)

*Illustrative only — a made-up project, no real-world numbers.*

- **Project name:** culvert
- **One-line value proposition:** "Find broken links in your docs before they ship."
- **Opening paragraph:** "culvert scans the rendered HTML your docs site actually builds — not your markdown source — so it catches links that break after templating and redirects run, which a markdown linter can't see."
- **Quick start:** `npx culvert ./dist` → "3 broken links found in ./dist/guide/setup.html"
