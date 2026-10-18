# The checks

Run them in order. The scorecard records every check, so nothing is hidden, but **the first class that fails gates the fixes**: list that class's fixes first, and hold later classes' fixes until it passes. Polishing trust copy on a page nobody understood is wasted work.

Every finding carries an evidence tag. See [evidence tags](#evidence-tags) below.

## 0. A problem worth solving

**Test.** Ask the owner to name one real person who has the problem, what that person does today, and how the owner knows. **Fail** if there is no such person or no evidence. **Route:** `pm-discovery`, from the `product-strategy` plugin. If it is not installed, write the one person, the current workaround and the evidence gap as `MISSING INFORMATION` and stop. Page copy cannot fix a problem nobody has.

## 1. Name and URL legibility

**Test.** Split the domain into every plausible word sequence. Say it aloud. Ask a reader to spell it back after hearing it. List each plausible misreading, including embarrassing ones. Record whether the label has hyphens or digits (`static_signals.py` reports this). **Pass:** one natural reading. **Concern:** a likely misreading or hard-to-spell name. **Fail:** a misreading most visitors would reach first. **Tag:** hyphens and digits are `mechanical`; misreadings are `LLM-only` until a second reader or a person agrees. **Route:** `mk-brand-kit` for a name-plus-pronunciation lockup, `mk-copy` for a tagline beside it. Renaming is the owner's decision; say so.

## 2. Comprehension

**Test.** The [staged read](staged-protocol.md), scored against the owner's truth. **Pass:** by stage 2 the reader gets who and problem right with confidence 70 or more. **Concern:** it arrives only at stage 3, or confidence sits at 55 to 69. **Fail:** who or problem is still wrong or missing at stage 3. **Route:** `mk-positioning` if the one-liner is unsettled, otherwise `mk-copy`.

## 3. Relevance and who it is for

**Test.** Does the first screen name a problem in the reader's own words, and a person who has it? Does any page say who it is not for? Do the title, headline, pricing and legal pages describe the same audience? **Fail:** no named problem, or two pages that name different audiences. When readers disagree about the audience, tag it `voices-disagree`: the disagreement is the finding. **Route:** `mk-audience`, then `mk-positioning`.

## 4. Claim typing

**Test.** Tag the headline and every section heading as one of:

- **feature**: names something the product has ("automatic sync").
- **outcome**: what the visitor gets or gets done ("never lose a plant to a missed watering").
- **differentiator**: something the visitor's named alternative does not do, stated against it.
- **table-stakes**: something every product in the category has. Judge against the named alternative.
- **proof**: evidence a visitor can check (a demo, a sourced number, a real named customer, a certification).

**Pass:** the first screen holds an outcome, and at least one differentiator appears on the page. **Fail:** nearly every heading is a bare feature or table-stakes. Report the counts. **Tag:** the text and counts are `mechanical`; the typing of each claim is judgement, so show the quoted line. **Route:** `mk-positioning`, then `mk-copy`.

## 5. Proof

**Test.** Can a visitor watching once state the problem and the result? List every demo, video and screenshot. For video, check for audio, narration, captions and controls (`videos` and `caption_tracks` in `static_signals.py` cover only video in the raw HTML; check the rendered page too). A silent montage with no captions of screens shows a product without saying anything. **Fail:** no demo, or one a visitor cannot follow without sound or explanation. **Tag:** attributes are `mechanical`; what a video shows is `NOT VERIFIED` unless someone watched it. **Route:** `mk-copy` for the script and captions, `mk-launch` if a launch asset is the real gap.

## 6. Trust

Six sub-checks. A visitor who says "I don't trust this" without inspecting anything is voicing a prior, not a finding: test whether the signals exist and are surfaced before concluding anything.

| # | Sub-check | Test | Evidence |
|---|---|---|---|
| 6a | Proof exists | A privacy or security page states where data lives, how it is protected, what is shared and with whom, and how to export and delete it | `mechanical` |
| 6b | Proof is surfaced | The strongest claim is on the first screen or on the card that asks for the data, not only behind a footer link | `mechanical` |
| 6c | AI processing is disclosed where the AI feature is advertised | If a feature sends a visitor's content to a third-party model, the feature's own card says so, not only the legal text | `mechanical` |
| 6d | Accountability | A named organization, its country, and a way to reach it. Never recommend naming an individual who has not agreed to it | `mechanical` |
| 6e | Promise versus maturity | Compare the sensitivity of what the product asks for (passwords, secrets, health, money, children) with the proof offered and the stage it admits to ("early", "beta"). Asking for the most sensitive data with the least proof is a Fail, whatever the encryption claims | judgement; quote the lines |
| 6f | Pricing story | If it is free, in beta or on a waitlist: does the page say why, and what happens later? Do not recommend "never offer free"; recommend explaining it | `mechanical` |

**Route:** `hardening:privacy-audit` and `hardening:legal-docs` from the `hardening` plugin for 6a to 6d; `mk-copy` to surface proof; `pm-strategy-fit` or `pricing-review` from `product-strategy` for 6f. If a routed skill is absent, list the missing page or sentence and mark the draft `HUMAN DECISION REQUIRED`.

## 7. Access and friction

**Test.** From a stranger's view, what does the main button say, and does it fit? "Sign in" is a poor first action for someone with no account. Look for contradictions ("join the waitlist" beside "try it now"), account walls in front of the first value, and the number of steps to first value. Do not click through: what lies behind a sign-in is `NOT VERIFIED`. **Tag:** button text and contradictions are `mechanical`. **Route:** `mk-copy`, then `mk-lifecycle` for the sequence after sign-up.

## 8. Machine legibility

**Test.** Run `scripts/static_signals.py`. Compare the raw HTML to the rendered page. Check: a descriptive title in the raw HTML, a meta description, Open Graph tags (what most link previews read), a canonical link, JSON-LD, a headline in the raw HTML, and a `noscript` fallback. **The JS-shell test:** if the raw HTML holds almost no visible text, give the machine view to a reader with no JavaScript and ask whether it could cite the product. **Fail:** a shell with a bare-name title and no description. **Tag:** `mechanical`. **Route:** `mk-search`; the markup change goes to whoever builds the site.

## 9. Model fit

**Test.** A visitor may suggest the product should be open source or self-hosted, free, or paid. Treat each as a hypothesis about trust or pricing, never as a diagnosis: check it against what the product is and can afford. Open source helps a visitor inspect the code; it does not fix a page nobody understood. **Tag:** `single-reader` unless several visitors say it independently. **Route:** `pm-strategy-fit` from `product-strategy`, or note it as an owner decision.

## Evidence tags

| Tag | Meaning |
|---|---|
| `mechanical` | A script or a direct look at the page text, markup or attributes confirms it |
| `multi-reader` | Two or more independent readers (people, or separately run reader stages) reached it on their own |
| `single-reader` | One reader said it |
| `LLM-only` | Only an AI reader said it, and nothing else confirms it |
| `voices-disagree` | Readers disagree, for example about who the product is for. The disagreement is the finding |

**Only `mechanical`, `multi-reader` and `voices-disagree` findings may enter the top fixes.** The rest go under "Hypotheses to verify", each with the cheapest check that would settle it.

## Routing when a skill is absent

| Routed to | If it is not installed |
|---|---|
| `mk-positioning` | Write the alternative, the differentiated capability, the value and the segment in one line each; mark it `HUMAN DECISION REQUIRED` |
| `mk-copy`, `mk-brand-kit`, `mk-lifecycle`, `mk-launch` | Describe the change in one sentence per finding and hand it to the owner or a writer; do not draft final copy here |
| `mk-audience`, `mk-search`, `mk-measurement`, `mk-outreach` | State the question the skill would answer and what evidence is missing |
| `pm-discovery`, `pm-strategy-fit`, `pricing-review` | State the open question and mark it `MISSING INFORMATION` |
| `hardening:privacy-audit`, `hardening:legal-docs` | List the missing disclosure and recommend a qualified review before publishing legal text |
