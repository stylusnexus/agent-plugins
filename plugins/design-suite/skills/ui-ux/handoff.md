# Handoff and routing

The design lead is the entry point. Bring in only the specialists the problem needs. Specialists return findings to the lead; the product owner decides product trade-offs and authorises merge, publication and deployment.

## Routing

| Signal in the request | Route to | What to send | Expect back |
|---|---|---|---|
| Navigation, menus, labels, grouping, "can't find X" | Information architect (/information-architecture) | Task list, current structure, content inventory | Sitemap or hierarchy, taxonomy, task paths |
| Dashboard, console, metrics, status summary | Dashboard designer (/dashboard-design) | Decisions supported, data sources with owners | Layout by decision, state and freshness design |
| Phone, touch, responsive, offline, forms on small screens | Mobile design expert (/mobile-design) | Target devices if known, flows, current breakpoints | Mobile states, responsive rules |
| Keyboard, screen reader, contrast, target size, motion | Accessibility expert (/accessibility-review) | Screens or code, the states, interaction notes | Barriers with remediations and which need testing |
| Can users find this? Did this change bury or move something? Second opinion on placement | UX designer (ux-designer) | Diff or PR, screenshots, the task the user is doing | Findings with evidence, regressions, issues filed or linked |
| Approved design to build | design-ui-engineer | Handoff package below | Changed files, validation, unresolved requirements |
| Typography, surfaces, micro-interactions on a settled design | /interface-polish | Screens and tokens in use | Refinements within the existing system |
| A new look, a substantial redesign, or "this looks generic" | /art-direction | Brief, brand constraints, what imagery exists | A chosen direction, a built page or screen, and measured inspector results |

Dashboard design and information architecture may collaborate briefly on dense information. Accessibility and mobile are focused services; unresolved choices come back to the lead.

## Handoff package for design-ui-engineer

Send only after the product owner approves scope. Include:

1. Approved scope in one paragraph and what is explicitly out of scope.
2. The brief (design-brief-template.md) with open questions resolved or listed as blockers.
3. Screens and states: every state from flow-and-states.md per screen, with copy for each message and button label.
4. Layout and responsive rules: breakpoints used by the existing code, reflow behaviour, what stays visible.
5. Components to reuse from the existing codebase (file paths). No new dependency or design system unless the product owner approved it.
6. Interaction details: focus movement, keyboard behaviour, validation timing, feedback timing, destructive-action handling.
7. Data rules: source of truth, what is read-only, freshness and provenance display.
8. Acceptance criteria, each checkable.
9. How to verify: commands, pages, test accounts or fixtures if known; otherwise MISSING INFORMATION.

Ask the engineer to return: changed files, what was validated and how, what was not validated, deviations from the design with reasons, and requirements that remain unresolved. The engineer does not merge or deploy.

## Handoff to the accessibility expert

Include: the screens or code paths, the full state set, the intended keyboard path and focus order, dynamic content that updates without navigation (status messages, live regions), custom controls and their intended roles, colour tokens used for text and boundaries, target sizes, and any motion.

Ask for: barriers found, severity, a concrete fix each, and a clear split between what was checked by inspection and what needs a browser run, assistive-technology test, or people with disabilities. The expert does not claim conformance or certification. Do not paste conformance statements into the brief on the expert's behalf.

## Receiving work back

Check each returned item against the acceptance criteria. Record failures as findings, not as silent rewrites. Surface anything that changes scope, data authority or user-facing wording to the product owner before accepting it.
