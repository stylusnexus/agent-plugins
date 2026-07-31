---
name: human-writing
description: Write content that sounds natural, conversational, and authentically human - avoiding AI-generated patterns, corporate speak, and generic phrasing. Also handles the "humanize this" / "humanise this" trigger - a meaning-preserving rewrite that strips signs of AI writing.
---

# Human-Style Writing

This skill helps you write content that reads like it was written by a real person with opinions, personality, and specific knowledge—not a corporate blog generator or AI assistant trying to sound helpful.

## Core Principle

**Write like you're explaining something to a colleague over coffee, not presenting to a board room.**

Good writing is specific, opinionated, and conversational. Bad writing is generic, safe, and sounds like every other tech blog.

## The "humanize this" Trigger

**Triggers: "humanize this" or "humanise this."** Both spellings. If no text follows the trigger, ask what should be humanized before doing anything else.

This is a *rewrite* mode, distinct from the rest of this skill. The sections below teach you to write well from scratch. This one takes existing text and subtracts machine residue from it.

### The contract

**Do:**
- Remove every tell in the checklist below that isn't doing genuine work in its sentence.
- Preserve meaning, facts, figures, names, dates, quotations, citations, and the order of claims exactly.
- Preserve hedges that reflect real uncertainty. An unsupported claim stated flatly is the worse failure.
- Return the rewritten text, then a short list of what changed and why.

**Don't:**
- Add new claims, examples, statistics, sources, or transitions that carry new information.
- Strengthen a claim past what the original supported. Cutting "arguably" from a genuinely arguable claim is a factual edit wearing a style edit's clothes.
- Flatten voice into neutral prose. You're removing machine residue, not personality.
- Guess. If removing a tell requires knowing something the text doesn't state, flag the passage and leave it.

### The checklist

From the Wikipedia editors' guide, [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

**Content**
- Significance and legacy inflation: "pivotal moment," "represents a shift," "left an indelible mark," "stands as a testament," "deeply rooted"
- Canned notability: "widely regarded," "has garnered attention," "profiled in"
- Trailing present-participle pseudo-analysis that asserts a connection without earning it: "highlighting the importance of...," "reflecting a broader trend...," "underscoring the need for..."
- Promotional register: "boasts a," "vibrant," "nestled in the heart of," "groundbreaking," "rich tapestry," "seamless," "cutting-edge"
- Vague attribution with no attributable party: "experts argue," "observers have noted," "industry reports suggest," "it is widely believed"
- The formulaic close: "Despite its success, X faces several challenges..." followed by speculative resolution

**Language**
- AI vocabulary at density: additionally, align with, bolster, crucial, delve, emphasize, enduring, foster, garner, highlight, intricate, leverage, meticulous, pivotal, realm, robust, showcase, streamline, tapestry, testament, underscore, vibrant. Any one is fine. Six in a page is a tell.
- Copulative avoidance: "is" inflated to "serves as" / "stands as" / "functions as"; "has" inflated to "boasts" / "features" / "maintains"
- Negative parallelism, all three shapes: "not only X but also Y," "it's not X, it's Y," "X rather than Y"
- Reflexive rule-of-three
- Elegant variation: synonym-swapping to dodge a repetition that was correct

**Style**
- Title Case Headings
- Mechanical boldface and "key takeaways" bolding
- Lists where every bullet is a **bold header:** plus an explanatory clause
- Em dashes as default subordinate-clause punctuation
- Emoji as formatting; tables for content that wasn't tabular; curly quotes; skipped heading levels

**Leakage to the user**
- "I hope this helps," "let me know if you'd like me to expand," "great question"
- Knowledge-cutoff disclaimers; unsubstituted placeholders (`[Company Name]`, `[citation needed]`)

**Model residue** — always cut, never stylistic
- ChatGPT: `contentReference`, `oaicite`, `turn0search0`
- Gemini: `[cite: 1]`, `[span_1]`
- Grok: `grok_card`, `grok_render_citation_card_json`
- DeepSeek: lenticular brackets, dagger symbols
- Perplexity: `attached_file`, `ppl-ai-file-upload`

### Guards against over-scrubbing

The guide's own caveats constrain how hard you scrub: AI detectors have non-trivial error rates, and humans distinguish AI text at roughly chance. **These are tells, not proof.** The signal is density and co-occurrence, never a single instance — most items above appear in good human prose at low frequency.

- **Rule-of-three** targets padding triples, not three-part structures doing analytical work. Cut the third adjective that was filler; keep the third cause that was a cause.
- **Protect the signs of human writing:** irregular syntax, fragments that land, a long sentence followed by three words, specific choices the writer could defend. These are the target state, not defects.
- **A load-bearing tell stays.** Flag it in the change list with the reason. Flagged retention is a correct outcome, not a failure.
- The output is not detector-proof, and that isn't the standard being met. Say so if asked.

## What Makes Writing Sound AI-Generated

### ❌ Patterns to Avoid

#### 1. Over-Enthusiastic Openings
```markdown
❌ "We're thrilled to announce..."
❌ "Today, we're excited to share..."
❌ "I'm delighted to introduce..."
❌ "Join us on this exciting journey..."

✅ "We built X because Y kept breaking."
✅ "Here's what we learned shipping X to production."
✅ "Most migration tools get you 70% of the way. Here's how we get to 95%."
```

#### 2. Vague Claims Without Evidence
```markdown
❌ "This revolutionary approach transforms how developers work."
❌ "Leveraging cutting-edge AI technology..."
❌ "A game-changing solution for modern development."
❌ "Unlock the full potential of your workflow."

✅ "Nango used this to migrate 47 repos in 3 days."
✅ "We tested this on Next.js App Router migration—reduced manual fixes from 800 to 40."
✅ "Stripe's migration guide is 12,000 words. This gets it down to 200 lines of code."
```

#### 3. Corporate Buzzword Soup
```markdown
❌ "Empowering developers to leverage synergies..."
❌ "Best-in-class solutions for enterprise-grade..."
❌ "Seamlessly integrate with your existing ecosystem..."
❌ "Drive innovation through collaborative paradigms..."

✅ "Works with whatever you're already using."
✅ "Detects edge cases your regex won't catch."
✅ "One command. No config file. No surprises."
```

#### 4. Unnecessary Hedging
```markdown
❌ "This might help you potentially improve..."
❌ "You could possibly consider..."
❌ "This may or may not be useful..."
❌ "Some users have reported that..."

✅ "This cuts migration time in half."
✅ "Use this when codemods aren't enough."
✅ "Three users reported this edge case. We fixed it."
```

#### 5. Generic Transitions
```markdown
❌ "Let's dive deep into..."
❌ "Without further ado..."
❌ "At the end of the day..."
❌ "It goes without saying..."

✅ Just start the next section. You don't need a transition.
✅ Or use a specific connector: "Here's why that matters:"
```

#### 6. Robotic Lists
```markdown
❌ "Here are 5 key benefits:
1. Enhanced productivity
2. Improved efficiency
3. Better collaboration
4. Increased flexibility
5. Streamlined workflows"

✅ "This saves you time in three ways:
- No more searching docs for edge cases—they're encoded in the package
- AI applies patterns consistently—you don't chase style violations
- Tests are generated, not written—coverage without the grind"
```

## What Makes Writing Sound Human

### ✅ Patterns to Use

#### 1. Specific Details
```markdown
❌ "Many developers struggle with migrations."
✅ "We've all copy-pasted from a migration guide, missed an edge case, and spent 2 hours debugging why tests fail."

❌ "Performance is significantly improved."
✅ "Query time dropped from 847ms to 12ms after adding the index."

❌ "Works with popular frameworks."
✅ "Tested on Next.js, Remix, SvelteKit, and Astro."
```

#### 2. Direct, Confident Language
```markdown
❌ "This approach may help you potentially improve your workflow."
✅ "This cuts your migration time in half."

❌ "You might want to consider using this feature."
✅ "Use this feature when you have more than 10 files to update."

❌ "Some users have found this useful."
✅ "Three teams adopted this last week. All three shipped in under 2 days."
```

#### 3. Honest Limitations
```markdown
❌ "Our comprehensive solution handles all use cases."
✅ "This won't catch dynamic imports or string templates. You'll need to fix those manually."

❌ "Perfectly seamless migration experience."
✅ "Expect about 5% of edge cases to need manual review. That's down from 30%."

❌ "Works with any codebase."
✅ "Works if you're on TypeScript 4.5+. Earlier versions need a polyfill."
```

#### 4. Conversational Asides
```markdown
✅ "You could write a 400-line script for this. We did. It broke on Unicode."
✅ "Turns out, most projects have 3-5 edge cases that codemods can't handle."
✅ "We tried docs. Developers don't read them. We tried linting. They ignore the warnings."
```

#### 5. Active Voice, Present Tense
```markdown
❌ "The package can be installed by running the command."
✅ "Install the package: prpm install @vendor/migration"

❌ "Improvements were made to the conversion quality."
✅ "We improved conversion quality from 78% to 94%."

❌ "It has been observed that users prefer..."
✅ "Users prefer X over Y by a 4:1 margin."
```

#### 6. Strong Opening Sentences
```markdown
❌ "In this post, we will discuss how migrations work."
✅ "Codemods automate 70% of migrations. This gets you to 95%."

❌ "Let me tell you about a new feature we've added."
✅ "You can now install an entire framework migration as a single package."

❌ "Today, I want to talk about our vision for the future."
✅ "Package managers changed how we ship code. We're doing the same for AI instructions."
```

## Tone Calibration

### Technical Posts
- **Voice**: Knowledgeable peer, not teacher
- **Assumptions**: Reader knows basics, wants specifics
- **Evidence**: Code examples, performance numbers, real packages
- **Length**: As long as needed to be complete, as short as possible to respect time

**Example:**
```markdown
# Converting Copilot Rules to Claude Format

GitHub Copilot uses a single `.github/copilot-instructions.md` file with YAML frontmatter. Claude uses separate skills in `.claude/skills/`.

Here's how we handle the conversion:

1. Parse the YAML frontmatter with js-yaml
2. Extract the `applyTo` glob patterns
3. Convert to Claude's `fileMatch` format
4. Split multi-concern rules into separate skills

Edge case: Copilot's `applyTo` supports negation patterns (`!**/*.test.ts`). Claude doesn't. We preserve these as comments and log a warning.

Conversion quality: 94% (6% requires manual review for negation patterns).
```

### Vision Posts
- **Voice**: Opinionated builder with receipts
- **Assumptions**: Reader is skeptical, needs convincing
- **Evidence**: Real-world examples, before/after, objections addressed
- **Length**: Long enough to make the case, tight enough to stay focused

**Example:**
```markdown
# Why Docs Aren't Enough

Stripe's migration guide is 12,000 words. It's comprehensive, well-written, and most developers skim it.

Why? Because reading docs requires:
1. Find the right section (3-5 minutes)
2. Understand the pattern (5-10 minutes)
3. Apply to your specific case (10-30 minutes)
4. Repeat 20-50 times per migration

That's 6-15 hours. And you'll still miss edge cases.

PRPM packages encode those patterns once. AI applies them consistently. Total time: 20 minutes.
```

### Tutorial Posts
- **Voice**: Experienced guide who's made the mistakes
- **Assumptions**: Reader wants to follow along, copy/paste, learn
- **Evidence**: Runnable examples, expected output, common pitfalls
- **Length**: Complete walkthrough with no missing steps

**Example:**
```markdown
# Publishing Your First PRPM Package

## What You'll Build

A Cursor rule that enforces "no default exports" across your TypeScript codebase. By the end, you'll have published it to the registry.

## Prerequisites

- Node.js 18+ (check: `node --version`)
- PRPM CLI installed (`npm install -g prpm`)
- GitHub account (for publishing)

## Step 1: Initialize the Package

```bash
$ mkdir no-default-exports
$ cd no-default-exports
$ prpm init

Format: cursor
Subtype: rule
Name: no-default-exports
Description: Enforce named exports in TypeScript
```

This creates `prpm.json` and `.cursorrules`.

## Step 2: Write the Rule

Edit `.cursorrules`:
[... full example ...]
```

## Structural Techniques

### 1. Start With The Punchline
```markdown
❌ "In this article, we'll explore the challenges of API migrations, discuss various approaches, and ultimately present a solution."

✅ "API migrations fail because docs explain the 'what' but not the 'why.' Here's how to ship the reasoning with the code."
```

### 2. Use Subheadings as Scannable Statements
```markdown
❌ ## Introduction
❌ ## Background
❌ ## Methodology
❌ ## Results

✅ ## The Problem: Docs Go Stale
✅ ## Why Codemods Aren't Enough
✅ ## What PRPM Packages Add
✅ ## Real Example: Next.js App Router
```

### 3. Show, Don't Just Tell
```markdown
❌ "The conversion process is simple and efficient."

✅ "Here's the entire conversion:
```bash
$ prpm install @nextjs/app-router-migration --as cursor
$ cursor apply @nextjs/app-router-migration
✓ Migrated 47 files
⚠ 3 files need manual review (dynamic imports)
```
Done in 90 seconds."
```

### 4. Break Up Walls of Text
- Use subheadings every 2-3 paragraphs
- Insert code blocks to give eyes a break
- Use bullet lists for 3+ related items
- Add horizontal rules for major section breaks
- Use blockquotes for important callouts

### 5. End With Action, Not Summary
```markdown
❌ "In conclusion, we've discussed how PRPM packages work and why they're useful for migrations."

✅ "Try it:
```bash
prpm install @popular/package-name
```

Have questions? Follow [@prpmdev](https://twitter.com/prpmdev) or [open an issue](https://github.com/pr-pm/prpm/issues)."
```

## Voice Examples from PRPM

### Good (from VISION.md):
> "Codemods automate the first 60–80% of migrations. Docs explain the rest. Developers still wrestle with edge cases, conventions, and tests."

**Why it works:** Specific percentages, clear problem statement, no fluff.

> "You could read 47 migration guides. Or install one package."

**Why it works:** Concrete number, stark contrast, confident.

> "We tried this on Nango's SDK migration. 47 repos, 3 days, zero regressions."

**Why it works:** Real company, real numbers, honest outcome.

### Bad (AI-generated style):
> "Our innovative platform leverages cutting-edge AI to streamline your development workflow."

**Why it fails:** Buzzwords, vague, could describe anything.

> "We're excited to announce a revolutionary new approach to migrations."

**Why it fails:** Over-enthusiastic, no specifics, marketing speak.

> "This powerful solution empowers teams to unlock their full potential."

**Why it fails:** Empty claims, corporate jargon, meaningless.

## Self-Check Questions

Before publishing, ask:

1. **Would a human say this out loud?** If not, rewrite.
2. **Is every claim backed by evidence?** If not, add specifics or remove the claim.
3. **Could this sentence appear in any other company's blog?** If yes, make it specific to PRPM.
4. **Does this assume the reader is dumb?** If yes, trust them more.
5. **Am I hedging because I'm uncertain?** If yes, verify facts or own the uncertainty.
6. **Is this a transition I can delete?** If yes, delete it.
7. **Does this open with enthusiasm instead of information?** If yes, lead with the info.

## Quick Fixes

### If it sounds too formal:
- Replace "utilize" → "use"
- Replace "in order to" → "to"
- Replace "at this point in time" → "now"
- Replace "for the purpose of" → "for" or "to"
- Cut "very," "really," "quite," "actually"

### If it sounds too generic:
- Add a specific number
- Name a real company/project
- Include a code example
- Mention a concrete edge case
- Quote user feedback

### If it sounds too salesy:
- Replace superlatives with comparisons
- Replace "revolutionary" with "different because"
- Replace "amazing" with specific benefits
- Remove exclamation points (except in code comments where appropriate)
- Cut the first paragraph (usually marketing fluff)

## Remember

PRPM users are developers. They have good bullshit detectors. Write like you respect their intelligence and their time.

**Good writing is revision.** First draft: get ideas down. Second draft: cut 30%. Third draft: add specifics. Fourth draft: read it out loud.

If you wouldn't say it in a GitHub issue comment, don't put it in a blog post.
