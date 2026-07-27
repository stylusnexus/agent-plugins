---
name: html
description: Turn complex output (plans, code reviews, research, comparisons, configs, reports) into a single self-contained, reading-first HTML artifact. Structure before style, inline CSS only, no network calls, Markdown export for handoff. Use when the user says "make this an HTML page/report/artifact", "turn this into HTML", "/html", asks for a visual explainer, decision page, code-review page, or a small one-file editor, or when a terminal answer is too long/dense to read comfortably.
args: "<what to turn into an artifact, e.g. 'turn this code review into a readable page'>"
---

# HTML Artifact

Turn complex agent output into a **single self-contained HTML file a human will actually read**. The goal is not a pretty page — it is a clear artifact. Structure before style. Reading before interaction.

This skill follows one rule: **Markdown when the idea is still being shaped. HTML when the idea needs to be understood by a human** — reviewed, compared, or shared.

## When to use HTML vs Markdown

Reach for an HTML artifact when the output is something a person needs to *read once and understand*:

| Use Markdown for | Use HTML for |
|---|---|
| Notes, raw plans, scratch thinking | Reports, explainers |
| Source-of-truth files Claude re-reads | Code reviews, design comparisons |
| Project memory, docs edited many times | Decision pages, visual plans, prototypes |
| Anything still being shaped | Stakeholder summaries, anything someone else reads |

Do **not** turn everything into HTML — that gets messy. Write the source clearly (Markdown), then produce HTML when the output needs to be read, reviewed, or shared. When work belongs in a repo, keep the Markdown source and treat HTML as the presentation layer.

## Workflow

1. **Identify the artifact type** (see patterns below). If unclear, ask or pick the closest match.
2. **Gather the real content** — read the project files, diff, research, or options you're summarizing. Don't invent; pull from what's actually there.
3. **Choose the file path.** Default to `artifacts/html/<name>.html` relative to the working dir if inside a project, otherwise the current directory. Name it for the job: `project-explainer.html`, `code-review.html`, `decision.html`, `report.html`.
4. **Generate the file** following the Hard Rules below. Use `template.html` in this skill folder as the structural starting point.
5. **Run the self-review** (Safety + Quality checklists). Fix anything that fails.
6. **Tell the user the path** and how to open it (`open <path>` on macOS opens it in the default browser).

## Hard Rules — every artifact

These are non-negotiable. They keep artifacts portable, private, and trustworthy.

- **One self-contained `.html` file.** Everything inline.
- **Inline CSS only.** No external libraries, no remote fonts, no CDN links.
- **No network requests of any kind** — no remote scripts, images, analytics, trackers, or API calls. No forms that submit anywhere.
- **No secrets.** Never embed API keys, tokens, customer data, or credentials.
- **Clear summary at the top.** A reader should understand the gist in the first screen.
- **Simple sections** with real headings. Readable on laptop *and* mobile (use a max-width container and responsive units).
- **Tables only when they help.** Use inline **SVG** for simple diagrams (flows, boxes, arrows) — never a remote image.
- **Structure before style. Reading before interaction.** Add JS/interaction only when it earns its place.
- **Don't over-design.** Restraint reads as quality. The article's house palette: warm off-white background, near-black text, one muted terracotta/clay accent, generous whitespace, serif headings + clean sans body. `template.html` already encodes this.

### Optional, when genuinely useful

- **Copy/export buttons** (e.g. "Copy as Markdown", "Copy as JSON", "Copy diff"). Implement with a tiny inline script writing to the clipboard — no network.
- **A Markdown export section** if the artifact may need to flow back into notes/source-of-truth.
- **Light interaction** (tabs, toggles, drag-to-sort) *only* for editor-style artifacts where it removes real friction.

## Artifact patterns

Pick the one that fits. Each maps to a section layout in `template.html`.

- **Project explainer** — onboarding a codebase. Include: plain-English summary, folder map, ~10 most important files (as cards), a simple SVG data-flow diagram, what each major part does, what *not* to touch yet, common commands (code blocks), and a "first safe change" checklist.
- **Code review page** — from a git diff. Include: short summary of the change, files changed, a **risk level per file**, key code snippets with inline explanations beside them, possible bugs, missing tests, suggested fixes, and a final merge checklist. Make it readable for a developer who has 10 minutes. Make the risk *visible*, not pretty.
- **Decision page** — comparing options. For each option: what it means, when it's useful, cost, risk, complexity, what could go wrong, best use case. Add a comparison table, a final recommendation, and a **"What I would do first"** section. The page makes the decision easier to *see* — it does not make it for them.
- **Report / research summary** — summary, key findings, comparison table where relevant, and clear takeaways.
- **Small editing interface** — a throwaway one-file tool for one messy task (e.g. organize N ideas into Now/Next/Later/Cut, toggle config flags with guardrails). Keep it fully local: no backend, no database, no external scripts. End it with export buttons (copy as Markdown/JSON/prompt). It's not a real app — that's the point.

## Safety checklist (run before declaring done)

Scan the generated file and confirm:

- [ ] No external `<script src>`, no CDN/library links
- [ ] No remote fonts (`@font-face` with URLs, Google Fonts links)
- [ ] No remote images (`<img src="http...">`), tracking pixels, or analytics
- [ ] No `fetch`/`XMLHttpRequest`/network calls
- [ ] No forms that submit anywhere; no hidden network calls
- [ ] No API keys, tokens, secrets, or sensitive data embedded
- [ ] Opens and works offline in a browser

If any check fails, fix it before reporting completion. *A beautiful artifact is not worth leaking private work.*

## Quality checklist

- [ ] The summary at the top stands alone — reader gets the point in one screen
- [ ] Sections are scannable; headings are real and meaningful
- [ ] Tables/diagrams are used only where they add clarity
- [ ] Reads well at mobile width (no horizontal scroll)
- [ ] Not over-designed — restraint, not decoration
- [ ] If it's a source doc too: includes a Markdown export section

## Sharing

Simplest: open the `.html` locally. For teams: drop it in a docs folder, attach to a PR, or host as a static page. **For private/company work, keep artifacts local or inside approved systems — never upload sensitive code, data, secrets, or strategy to a public tool.**

## Source

This skill encodes the workflow from "HTML Is the New Output Layer for Claude Code": HTML as the human reading layer, Markdown as the memory layer.
