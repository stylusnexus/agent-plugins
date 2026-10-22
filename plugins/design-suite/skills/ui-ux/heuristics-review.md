# Heuristics review (expert review, not user research)

A heuristic pass is a structured inspection by someone applying established usability principles. It finds likely problems quickly. It does not show how real users behave, how often a problem occurs, or what matters most to them. State this in the output. Findings are hypotheses; list which need testing with real people.

Heading names follow the widely used ten usability heuristics (Nielsen Norman Group). The checks beneath are written for this suite.

## How to run it

1. Fix the scope: which task, which screens, which user, which device.
2. Walk the task once to learn it, then again slowly with the headings below.
3. Log each issue: location, heading, what you see, why it may hurt, severity, suggested fix.
4. Severity (recommended scale): 0 not a problem, 1 cosmetic, 2 minor, 3 major (likely to block or mislead), 4 critical (data loss, wrong outcome, or blocks the task). Severity is a judgement, not a measurement.
5. A single reviewer misses issues. If possible, repeat with a second perspective (for example the accessibility expert), and say when only one pass was done.

## The checks

1. Visibility of system status. Does every action get acknowledged? Is progress, current location, selection, and data freshness visible? Are loading, saving and sync states shown?
2. Match between system and the real world. Do labels use the user's words, not internal terms? Is order of information natural for the task? Do icons carry meaning without a label?
3. User control and freedom. Can the user cancel, undo, go back, close, and leave a flow without losing work? Is there an exit from every modal and mode?
4. Consistency and standards. Same word and same control for the same thing everywhere? Does it follow platform and web conventions (links look like links, primary action placement)? Does it match the product's existing components?
5. Error prevention. Are risky actions guarded (constraints, defaults, confirmation, undo)? Are inputs constrained to valid values (date pickers, formats shown, input types)? Are similar-looking actions kept apart?
6. Recognition rather than recall. Is needed information visible at the point of use? Are options listed rather than remembered? Do forms keep context (labels not just placeholders)?
7. Flexibility and efficiency of use. Are there shortcuts, defaults, bulk actions, saved filters for frequent users without burdening new ones? Does the keyboard path work end to end?
8. Aesthetic and minimalist design. Does each element support the task? Is the primary action clear? Is there competing emphasis, decorative noise, or dense text that hides the signal?
9. Help users recognise, diagnose and recover from errors. Are messages plain, specific, constructive and near the cause? Is input preserved? (See flow-and-states.md, error recovery.)
10. Help and documentation. Is help available in context, short, task-based, and findable? Is it needed because the interface is unclear (a design finding) rather than extra?

## Add-on checks when relevant

- Primary action: one primary action per view, with any second action clearly lower in visual weight. A default, not a law; some views need two equal choices.
- Decoration that looks like data: status dots, pagination counters, version stamps and badges appear only when they carry real state. Check that each maps to a data value.
- Trust elements (logos, quotes, numbers) are real or clearly labelled placeholder. Never present invented evidence as real.
- Marketing pages only: a quote fits a glance (about three lines, recommended) and carries a name and role; hero copy is a short value statement, one visual and one action.
- Accessibility: hand to the accessibility expert; note suspected issues only (focus order, contrast, name/role/value, target size) and mark them as needing browser or assistive-technology confirmation.
- Content states: run the full state set from flow-and-states.md.
- Mobile: touch and reflow checks from mobile-design.
- Data views: freshness and provenance checks from dashboard-design.

## Output

| # | Location | Heading | Observation | Why it may matter | Severity | Suggested fix | Needs testing with people? |

Close with: what was reviewed, what was not, number of reviewers (one AI pass unless stated), and the specific user tests that would confirm or overturn the top findings.
