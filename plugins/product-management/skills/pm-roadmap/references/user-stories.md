# User stories and delivery slices

Informed by Paweł Huryn's *How to Write User Stories: The Ultimate Guide + 10 Examples*. This is original operational guidance; source originals are not included.

## Guide the work
Start with the user/context, problem evidence, strategic objective and desired outcome. A story is a concise conversation aid, not evidence that an idea is validated. Use either “As [user], I want [action], so that [outcome]” or a situation-led job story when that clarifies the need. Do not force bugs, technical enablers, research spikes or operational work into a fictional user persona.

Apply Card, Conversation and Confirmation: write a short statement; discuss rationale, alternatives, constraints and dependencies; record observable acceptance criteria. Preserve room to learn while keeping acceptance explicit. A story passing acceptance tests does not prove its customer outcome occurred.

Use INVEST (independent, negotiable, valuable, estimable, small, testable) as review prompts rather than absolute gates. Expose real dependencies instead of hiding them to claim independence. Scope to a useful, testable slice; avoid arbitrary universal story durations or epic sizes.

## Split to learn and deliver
Compare slices by core versus optional paths, workflow stage, separable business rule, useful interface section, data type, supported platform or audience. Prefer end-to-end user value. Where a technical enabler is necessary, label it honestly and connect it to the dependent outcome. Avoid months of untested groundwork.

A smaller slice must still preserve essential authorization, security, data integrity, accessibility and error handling for its declared scope. Do not apply the source's happy-path/nonfunctional splitting advice as permission to defer necessary safeguards. Unsupported states must fail safely or remain outside release scope.

Use a short title, story/context, outcome/evidence link, scope/non-goals, relevant flow/design, concise acceptance criteria, dependencies and measurement. Separate acceptance boundaries from detailed test procedures. Include meaningful empty/error/permission cases when relevant.

Refine collaboratively and just in time. Record material scope changes and reconsider estimates/dependencies; do not silently rewrite an accepted commitment. Archive or defer distant ideas according to project conventions, not a universal three-month deletion rule. PMs and engineers collaborate on consequences while engineers own implementation planning; roles and job titles are organization-specific.

## Worked example (fictional)
Title: Export a reading list
Story: As a reader sharing recommendations with a friend, I want to export my selected book list so that I can share it without requiring an account.
Outcome hypothesis: recipients can understand the recommendations without additional explanation.
Acceptance: only selected books appear; ordering and titles are preserved; private notes are excluded; empty selection is explained; failed export preserves the selection and offers retry. Export format and supported fields are explicit choices to settle, not assumed requirements.

Teach one story and one splitting decision with the user's actual product, then produce the requested artifact. Creating stories does not authorize publishing issues or implementing them.
