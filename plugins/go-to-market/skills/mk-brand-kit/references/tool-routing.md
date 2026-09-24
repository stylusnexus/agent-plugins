# Which tool, when, and why: template tool, design tool, or code

A non-designer building marketing assets from scratch, one at a time, drifts from the brand kit and burns time re-deciding colors on every asset. This reference states which of three kinds of tool produces which piece, so the choice gets made once per asset type instead of every time — it draws on [the brand anatomy and design principles](brand-anatomy-and-design-principles.md) for what a kit needs to define before any of this is useful.

## The three kinds of tool, and what each is actually for

- **A template-based design tool (e.g. Canva)** — marketing images: social cards, Open Graph/link-preview images, launch graphics, simple one-pagers. The reason to use one here specifically: templates plus a saved brand kit keep a non-designer's output consistent and fast, instead of starting from a blank canvas and re-picking colors every time.
- **A product design tool (e.g. Figma)** — product UI and design-system work: screens, components, and any design-to-code handoff that needs precise layout and states, not a static image.
- **Code (HTML/SVG, or a dedicated diagramming/HTML skill)** — README banners, generated images, and anything that must be versioned in the repo alongside the product it represents. This is the right choice whenever the asset should live in git history, be regenerated programmatically (an OG image built from the same data that renders a page), or match exact brand tokens defined in code rather than picked by eye.

## When NOT to reach for a template tool
- Anything that needs to be versioned in a repo and regenerated on a schedule or from data (OG images built per post, README banners) — that belongs in code, not a design tool a human has to manually re-export.
- Product UI, component states, or anything that needs to hand off to engineering as a spec — that's a product design tool's job.
- Anything requiring precise, code-level color/token accuracy tied to a design system already defined in the codebase — recreating those tokens by eye in a separate tool invites drift from [the exact hex values](brand-anatomy-and-design-principles.md) the kit defines.

## Connecting a design tool
If a task genuinely needs a connected design tool and it isn't connected yet: explain what connecting it will do (typically a one-time sign-in), then ask "I'd like to connect [tool] — OK?" and connect only after an explicit yes — a new connection should start scoped to what the task actually needs. Once connected, check what the tool's available actions actually are before assuming a specific feature exists; a design tool's own feature set changes over time.

## A first small task with a template tool
A good first task to build confidence without overcommitting: one Open Graph/social-preview image for an existing page, using the brand kit's palette and type roles once those exist.

Steps:
1. Confirm the brand kit's palette (hex values) and heading/body fonts are decided (see [brand kit canvas](../templates/brand-kit-canvas.md)) — a template tool needs real tokens to be useful, not placeholders.
2. Connect the tool if not already connected, after explaining what that does, and only after an explicit yes.
3. Check the tool's currently available templates/brand-kit features (a fresh check after connecting) rather than assuming a specific capability exists.
4. Build one image at the platform's current recommended size (check this at the time — social-preview dimensions change) using the brand palette and type.
5. Export and show it before publishing anywhere — this reference prepares the asset, it doesn't post it.

## How the split plays out by product shape
A product with app-store or social-launch surfaces (store feature graphics, launch social posts) leans on a template tool for those images, code for the landing page and any README-adjacent banners, and a product design tool only if the in-app UI gets a dedicated design pass. A product with no marketing-image surface beyond a repo social-preview card — a developer library, say — has almost everything belong in code instead: README banners, badges, and generated diagrams versioned in the repo, with a template tool having little role.
