# Feeling and signature

What a page should make a visitor feel, and the one detail they remember. `critique.md` judges the result; this file sets the target before design and gives a check for each rule. Numbers marked "recommended" are defaults, not standards.

## 1. Name the feeling first

- Write one target feeling and its intensity on a five-step scale from calm to alarmed. Check: the brief holds one feeling word and one number. Two feelings at full strength is a different brief.
- Write three adjectives, drawn from the wanted-trait list below, that colour, type and photos must all express. Check: a reviewer who sees only the palette, only the type, and only the photos produces the same three words, or close. A set that only the type delivers means the system is not one system.
- Turn each adjective into one visible decision (a colour move, a face, a crop). Check: point to the element for each adjective; an adjective with no element is decoration.
- List traits to avoid beside the ones you want ("fun, not childish"; "calm, not sleepy"). Check: five to seven wanted traits, each with a stated opposite to avoid, and no avoided trait visible on the page.

## 2. Test the brand words against real people

- Ask five or more real customers or visitors which words describe the brand (recommended minimum, a small sample is still better than none). Compare with the team's own adjectives. Check: count the overlap. If fewer than half match, the direction sheet is aimed at the team, not the audience. Report this as MISSING INFORMATION when no customer input exists; do not invent customer words.

## 3. Journey with a feeling per step

- Write the outcome, then the touchpoints in order, each with one intended feeling. Check: every touchpoint has a feeling written beside it and a screen that delivers it.
- Payment and confirmation flows should feel dull and reassuring: few fields, costs and delivery dates shown early, no surprise. Check: count fields and surprises on the payment path against what the transaction needs; any decorative flourish there is a finding.

## 4. Small moments carry the feeling

- Error text, empty states, loading waits and button hover tone count as much as the hero. Check: read every error and loading message aloud; each must sound like the same voice as the headline and match the intensity from step 1.

## 5. Every decorative image earns its place

- Remove each image in turn. Check: if the page loses meaning, keep it; if it loses only decoration, cut it or give it a job (see `imagery.md` section 8, drawing the subject).

## 6. One focal point, one scale

- Squint (`critique.md` pass 2). Check: one mass leads and it is the most important content. Two equal masses leave the eye nowhere to go; shrink one.
- Derive type sizes and spacing from one declared ratio, with the ratio written in the tokens. Check: every size and gap is a step of that ratio. A steep ratio (recommended 1.5 or more) reads bold; a gentle one (about 1.2) reads quiet. This sits alongside the few-sizes rule in `type.md` section 2: pick few steps, all on one ratio.
- Light text on a dark ground: use a lighter weight and more line height than the light version (recommended: one weight step lighter, about 0.1 more leading) to cut glare. Check: compare the two themes side by side at the same size.

## 7. Phones get their own crop

- Re-crop each photo for the phone instead of shrinking the desktop crop; keep the subject large and the face inside the frame. Check: at 390 px wide the subject is still the largest thing in the image and is not cut. The mechanics are in `imagery.md` section 5 and `layout.md`.

## 8. One signature detail

- Choose one distinctive detail (a shape, a motion, a rule, an odd corner) and repeat it across templates. Three to five repeated details across a whole product is the upper range for a large system; a single detail used once feels disconnected. Check: list the templates; the detail appears in at least three of them in the same form.

## 9. Offsets: exact or clearly large

- An element is either exactly on the grid line or clearly pushed off it (recommended: roughly 20 to 30 px). Check: search the CSS for `translate`, `margin` and `top`/`left` offsets of 1 to 8 px; each reads as a bug rather than a choice. Fix by snapping to the grid or enlarging the offset.
