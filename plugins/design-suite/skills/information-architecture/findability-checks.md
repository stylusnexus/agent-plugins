# Findability checks

Findability is about whether real people find what they need. An AI cannot observe real people. Use this file to (a) do expert work the AI can do, labelled as expert review, and (b) write plans for tests that must be run with real people. Never report results of tests that were not run.

## 1. Content inventory (AI can do this from the product or repository)

Build a table of what exists:

| ID | Title/label | Type | URL or route | Parent | Owner | Last updated | Audience | Task served | Notes |

Method: crawl the navigation and sitemap, list routes in the code, list menu and settings entries, list docs. Record how many clicks each item is from home by the shortest path and by the most visible path. Mark MISSING INFORMATION for owners, dates and audience if not available.

Before changing any layout, also record the page tree, the main navigation and the key conversion paths as they are now, so a restyle can be compared (see url-and-content-model.md, restyling without restructuring).

Review the inventory for: duplicates, orphans (no path in), dead ends (no path out), outdated items, items with several names, items in more than one place, and important tasks with deep or hidden paths.

## 2. Scenario walkthroughs (expert review)

Label the output "Expert walkthrough by AI; not evidence of user success."

1. List 8 to 15 realistic tasks (recommended range). Use supplied tasks, support questions or owner-defined tasks; otherwise mark them as proposed.
2. For each, state a user goal in the user's words, not in menu labels. Example: "Find out why my last payment failed", not "Open Billing".
3. Starting from the entry point (home, search, link from email), choose at each step the link a person using only the visible labels would plausibly pick. Note: label ambiguity, competing options, hidden items, and where a wrong turn is likely.
4. Record the path and any dead end.

| Task | Start | Expected path (labels) | Competing labels at risk | Likely wrong turn | Steps | Verdict (clear / risky / unclear) | Fix |

Pitfall: the person writing the structure knows where things are. Describe the first impression, not the knowledge. Mark verdicts as hypotheses.

## 3. Tree test (plan; run with real people)

Tests the hierarchy with text labels only, no visual design.
- Needs: the proposed hierarchy as text, 8 to 15 tasks, a way to present them (a tool or a spreadsheet), real participants from the target audience.
- Participants: the number is a decision for the product owners; larger samples give steadier results. Do not state a number as required here. Recruit people who actually do the task. MISSING INFORMATION until selected.
- Each task: one question phrased without using menu labels; one or more correct destinations; participants click through the tree and choose where they would look.
- Record: success (picked a correct destination), directness (without backtracking), time, first click, and where failures landed.
- Analyse: tasks with many wrong first clicks point to a label or grouping problem. Look at where people went instead.
- Pass criteria: set before running and agreed by the product owners. No pass score is supplied here. MISSING INFORMATION.
- Run it on the current structure first as a baseline, then the proposal.
- Product owner approval required before contacting any user.

## 4. Card sort (plan; run with real people)

Reveals how people group and name things.
- Open sort: participants create and name their own groups. Use when exploring.
- Closed sort: participants place cards into given categories. Use to validate a draft.
- Cards: 30 to 60 items is a common range (recommended); too many tire participants. Choose items that represent the content, in plain wording, one concept per card, avoiding labels that give away the group.
- Participants from the real audience; number decided by the product owners. MISSING INFORMATION.
- Analyse: agreement between participants, frequently paired cards, group names used, cards that are not grouped consistently.
- Treat results as input to your judgement, not as a ready-made structure.
- Product owner approval required before recruiting or contacting participants.

## 5. Other checks that need real data or people

- Search log review: top queries, queries with no results, queries followed by reformulation. Requires supplied logs; if none, MISSING INFORMATION.
- First-click tests on actual pages.
- Support questions and feedback themes that name content people could not find. Supplied evidence only.
- Moderated sessions: ask users to find items while thinking aloud.
- Analytics on navigation use; treat with care and cite source and date.

## 6. Accessibility checks the AI can plan

- Reading and tab order match the structure.
- Navigation exposed with landmarks and current-page state.
- Page titles unique and descriptive (WCAG 2.4.2); headings form a logical outline.
- More than one way to reach pages in a set, such as navigation plus search or sitemap (WCAG 2.4.5, level AA).
- Link purpose clear from text (2.4.4).
- Consistent navigation and consistent identification across pages (3.2.3, 3.2.4).
Mark each as needing a browser or assistive-technology run before it is claimed to pass.

## 7. Reporting

Report in three sections: Done by AI (inventory, expert walkthrough), Plans for real people (tree test, card sort, others, with draft tasks and cards), MISSING INFORMATION (tasks, audience, logs, participants, pass criteria). Never merge them into one confidence statement.
