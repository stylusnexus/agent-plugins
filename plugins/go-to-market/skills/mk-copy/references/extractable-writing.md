# Extractable-section writing

A landing page or README doesn't get read start to finish. A search result shows one snippet. An AI assistant answering a question quotes one sentence or paragraph. A teammate forwards one section to someone else with no other context attached. The practical test for every section: if this paragraph were the only thing someone ever saw, would it still make sense and still be true?

## Why this matters beyond SEO
The people building tools that read web pages for AI assistants describe the same problem from the other direction. The llms.txt specification explains the gap it exists to close: "Web pages are built for people... converting it back into clean text is difficult and imprecise," and its purpose is putting "concise, expert-level information gathered in a single, accessible location" somewhere a tool can use without wading through navigation chrome and marketing filler. (Source: llms.txt specification, spec authored by Jeremy Howard, first published 2024-09-03 — https://llmstxt.org/ — accessed 2026-09-24.) A page doesn't need an llms.txt file to benefit from that insight — the same clean, self-contained writing a curated file exists to summarize is what makes an ordinary page's own paragraphs quotable on their own.

There's outcome evidence behind this too, not just theory: a 2024 study testing content-optimization techniques against real generative-engine queries found they "can boost visibility by up to 40%" in AI-generated answers. (Source: Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande, "GEO: Generative Engine Optimization," KDD 2024 — https://arxiv.org/abs/2311.09735.) — writing choices at the content level measurably change whether a system surfaces and cites a source, on top of whatever they do for a human skimming the same page.

## Rules for a section that survives being lifted out
The first and fourth rules follow the U.S. government's own plain-language guidance: "Each paragraph should start with a topic sentence that captures the essence of everything in the paragraph," and "Limit each paragraph or section to one topic... Putting each topic in a separate paragraph makes your information easier to digest." (Source: Digital.gov, "Clear and short," Plain Language Guide Series — https://digital.gov/guides/plain-language/writing/clear-short, accessed 2026-09-24.)

- Open with a real subject and a real verb, not a pronoun that only makes sense after reading the section before it ("It handles this automatically" → name the product or feature instead).
- State the section's one claim in its first sentence; put supporting detail, caveats, and examples after it, not before.
- Define any acronym or piece of jargon the first time *this* section uses it — a reader who only ever sees this one section shouldn't hit an undefined term. This suite's own extension of the digital.gov guidance above, not stated on that page directly.
- Keep one section to one idea. A section trying to cover two things at once usually means neither half reads cleanly when quoted alone.
- Treat the README as the actual landing page for an open-source project, not a secondary document — this suite's own reasoning, not a cited study: a README is often the first and only thing a visitor reads before deciding whether to use the project, so its opening needs the same self-contained-section discipline as a hosted landing page (see the [README opening skeleton](../templates/readme-opening-skeleton.md)).

## The honesty check stays first
None of the above licenses inflating a claim to make a section sound more complete on its own — every fact still needs a real source, per the shared claim-sourcing rule (see [pre-publish content check](pre-publish-content-checklist.md)). A section that reads well in isolation but says something untrue is worse, not better, because it's exactly the sentence most likely to get quoted somewhere else.
