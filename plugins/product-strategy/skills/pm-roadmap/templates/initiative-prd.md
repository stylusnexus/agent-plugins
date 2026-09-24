# Initiative brief (living decision document)

Fill in only the sections that actually help someone make a decision — an empty "Risks" section is worse than an omitted one. Draft with product, design and engineering perspectives in mind even if only one person is writing; note an unknown collaborator explicitly rather than inventing a name to fill a row.

- **Decision needed:** the specific choice this document exists to support, who makes it, and by when. State draft vs. accepted, and the date of that status.
- **Problem and evidence:** the problem in plain terms, who it affects and how badly, and the evidence behind that claim — not just the request that prompted this brief. Note what's still unverified.
- **Options considered:** the realistic alternatives, including doing nothing and **build vs. buy/partner** as a real, priced option rather than an assumed "we build it" — with what each would cost and what each would give up. A brief with exactly one option in it usually means the comparison hasn't happened yet.
- **Recommended option and scope:** which option is proposed and why.
- **Acceptance criteria:** the specific, checkable conditions that mean this is done — written so "done" isn't a judgment call later.
- **Smallest first slice:** the smallest piece of this that would still be useful on its own, shipped before the rest. Map each proposed piece of work back to the outcome it's meant to serve. State explicit non-goals.
- **Rejected or deferred:** options and scope that were considered and set aside, with the one-line reason — not just the option that won.
- **Risks and open questions:** what's been tested, what residual risk is being knowingly accepted, who owns watching it, and what would trigger a re-check. Include business-model or go-to-market dependencies when relevant. Explicitly check: does this depend on an outside approval with its own lead time (e.g. a third-party app-store or marketplace review)? Does it write to users' existing data in a way that can't be cleanly undone — and if so, what's the non-destructive rollback or disconnect path, distinct from a data-loss revert?
- **Success measures:** how the team will know the decision paid off — the baseline, the target and its rationale where known, and the time horizon. Mark anything still proposed as proposed, not settled. Keep this list of outcome/usage measures separate from system-health monitoring (errors, latency, availability) — they answer different questions and belong in different places.
- **Dates:** one table, one row per date (kickoff, review, launch, dependency deadlines). Mark each row **estimate** or **commitment** — never leave the distinction implicit in prose.
- **Rollout:** dependencies; how the launch is sequenced; what gets monitored after launch and how to roll back; when success will be reviewed.
- **References and change log:** links to research, prior decisions, the detailed implementation, and any launch or support material — pointing at the project's real source of truth rather than duplicating it here.

Keep it short. A brief's job is to support a decision and keep collaborators aligned — it is not itself permission to build or ship, and it doesn't replace the acceptance criteria or technical documentation the team needs to actually do the work.
