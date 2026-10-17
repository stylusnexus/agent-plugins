# Citable writing

Writing that a search engine or an AI assistant can both find and lift a correct fact from. Reachability and quality are separate failure points, and either one alone sinks a page: a well-written page that's login-gated is unreachable no matter how quotable its sentences are, and a fully public page can still fail to hand over a clean fact if it never states one plainly.

## Being reachable at all
Google's own documentation on AI Overviews and AI Mode states plainly that "there are no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary" beyond ordinary Search eligibility — a page has to be "indexed and eligible to be shown in Google Search with a snippet." Practically: no client-JS-only rendering that hides the content from a crawler, no login wall or paywall in front of it, not PDF-only, and "important content available in textual form" rather than locked inside an image. (Source: Google, "AI features and your website," https://developers.google.com/search/docs/appearance/ai-features, accessed 2026-09-24.)

## Being worth citing once you're found
Reachability gets a page into consideration; it doesn't make the content good. Google's helpful-content guidance asks whether a page offers "original information, reporting, research, or analysis" and a "substantial, complete, or comprehensive description" of the topic, and warns against content "primarily made to attract visits from search engines" rather than to help a specific reader. (Source: Google, "Creating helpful, reliable, people-first content," https://developers.google.com/search/docs/fundamentals/creating-helpful-content, accessed 2026-09-24, page last updated 2025-12-10.)

For AI assistants specifically, there's controlled evidence that content-level changes move the needle: a 2024 academic study tested content-optimization techniques against a benchmark of real queries and found they "can boost visibility by up to 40% in generative engine responses" — the size of the effect varied by technique and domain, so treat that figure as an upper bound from one study, not a guaranteed lift. (Source: Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande, "GEO: Generative Engine Optimization," KDD 2024 — https://arxiv.org/abs/2311.09735.)

## What that means for how you write a section
The first two rules below follow the U.S. government's own plain-language guidance, not an SEO or AI-specific idea: "Each paragraph should start with a topic sentence that captures the essence of everything in the paragraph," and "Limit each paragraph or section to one topic... Putting each topic in a separate paragraph makes your information easier to digest." (Source: Digital.gov, "Clear and short," Plain Language Guide Series — https://digital.gov/guides/plain-language/writing/clear-short, accessed 2026-09-24.)

- Put the actual answer near the top of the section, before the supporting detail — a reader or model skimming for one answer shouldn't have to read the whole page.
- Keep one section to one idea (per the digital.gov guidance above) — a section covering two things at once is harder to lift cleanly whichever half gets quoted.
- Name the subject again occasionally instead of leaning on "it" for several sentences running; a model seeing one paragraph out of context needs the sentence to still make sense.
- State facts as facts, with a source or checkable product behavior behind each one, not a vague claim nobody could quote with confidence.
- Define any term or acronym the first time a section uses it, not just once at the top of the page — sections get quoted individually. This suite's own extension of the digital.gov guidance above, not stated on that page directly.

## Where structured data fits
Structured data (schema.org markup) isn't required for basic indexing or AI features — it's optional, for enhanced result types. Google's own numbers argue for adding it once the content itself is solid: Rotten Tomatoes measured "a 25% higher click-through rate for pages enhanced with structured data," Nestlé "an 82% higher click through rate" on rich-result pages. The guidance favors "fewer but complete and accurate" properties over filling in every possible one — markup describes real content, it doesn't replace writing it. (Source: Google, "Understand how structured data works," https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data, accessed 2026-09-24.)
