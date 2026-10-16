# Product Management

Fourteen product management skills adapted and maintained by Stylus Nexus. Start with `product-manager` for a guided conversation or invoke a focused skill for a specific decision. The suite connects strategy, evidence, measurable outcomes and delivery without requiring every framework for every question.

## Install

For Claude Code, add the marketplace and install the full plugin:

```text
/plugin marketplace add stylusnexus/agent-plugins
/plugin install product-management@stylus-nexus
```

For Codex, add this repository as a plugin marketplace and choose **Product Management**. The bundle includes a native Codex manifest. For local Claude Code testing, run `claude --plugin-dir ./plugins/product-management` from a checkout.

With Skills CLI, run `npx skills add stylusnexus/agent-plugins` and select all fourteen skills listed below. Keep them as sibling skill directories: cross-skill guidance assumes the complete suite. Individual skill selection is not a supported standalone installation. Scripts and fallback templates live inside their owning skill so they travel with Skills CLI copies. No global configuration or private source installation is required.

## Rule ownership

| Skill | Owns | Typical request |
|---|---|---|
| `product-manager` | Project grounding, shared evidence rules, guided coaching, routing, decision synthesis and artifact review | Help me decide what to build next |
| `pm-vision` | Purpose, mission, vision and winning aspiration | Clarify our product direction |
| `pm-strategy` | Where to play, how to win, alternatives and strategic trade-offs | Review our product strategy |
| `pm-value-proposition` | Customer jobs, promise, alternatives, value curves and messaging evidence | Develop a value proposition |
| `pm-objectives` | Objectives, OKRs, metric definitions, North Star and review cadence | Define success measures |
| `pm-roadmap` | Outcome sequencing, prioritization, initiative briefs and delivery handoff | Build an outcome roadmap |
| `pm-discovery` | Research provenance, assumptions, experiments, Kano and product risks | Design a test for this assumption |
| `pm-growth` | Adoption, distribution, retention, growth loops and economics | Find a sustainable growth approach |
| `pm-canvas` | Integrated Product Strategy Canvas and its attributed working template | Fill out a strategy canvas |
| `pm-capabilities` | L1/L2 business abilities, current/target gaps and build/buy/partner | Map capabilities needed by this strategy |
| `pm-strategy-fit` | Reinforcement, contradictions, defensibility and assumption tests | Stress-test these strategic choices |
| `pm-market-analysis` | Five Forces, PESTEL and SWOT with dated sources | Analyze this market |
| `pm-teams` | Ownership, empowered teams, collaboration and leadership | Improve product-team decision rights |
| `pm-visuals` | Diagram semantics, evidence parity, accessible tables and format verification | Visualize the strategy and its gaps |

Repository instructions and project-local skill versions take precedence. Shared principles live in `product-manager/references/principles.md`; focused skills own their topic-specific rules. Custom agents, including `business-capability-modeler`, are optional existing host capabilities. This plugin installs no agent wrappers, connectors, credentials, schedules or background services. Work locally when delegation is unavailable.

## Workshop visuals

The [workshop asset library](skills/pm-visuals/references/workshop-assets.md) includes
eight editable slides, individual SVGs and printable PDFs: Pareto analysis,
Porter's Five Forces, outcome roadmap, value curve, assumption map, customer
journey, strategy canvas and value proposition. Common-framework illustrations
are original Stylus Nexus designs; the two template adaptations retain their
CC BY-SA attribution. Example data is clearly fictional.

## Local tools

Python 3.9+; standard library only. Commands below run from this plugin directory:

```sh
python3 -B skills/pm-discovery/scripts/discovery_digest.py /path/to/evidence.jsonl
python3 -B skills/pm-objectives/scripts/metrics_lookup.py --category Activation --json
python3 -B -m unittest discover -s tests -v
```

The discovery digest validates JSONL evidence records and prints provenance flags and source counts. See its [schema and example](skills/pm-discovery/references/insight-sources.md). It does not retrieve references, determine truth, detect mislabelled synthetic content, infer prevalence or perform research.

The metrics lookup searches 55 candidate definitions and cautions. It does not query analytics, calculate live metrics or choose a metric for the user. Both commands read local files and print to stdout; neither writes inputs or accesses the network.

Offline HTML and browser-markup templates are bundled under `skills/product-manager/support/`. They are reference fallbacks, not extra discoverable skills. Browser markup downloads a local review file; it sends no messages. Native PDF, slides, spreadsheet exports and cloud diagrams require suitable host tools. Connector access and visual rendering must be verified per task.

## Sources, licenses and limits

See [public provenance](skills/product-manager/references/sources.md) and [third-party notices](THIRD-PARTY-NOTICES.md). Stylus Nexus owns this adaptation's workflow and packaging; framework authors retain their attribution. Third-party research originals, private installation records and backups are excluded.

Original Stylus Nexus PDFs, slides, spreadsheets, images and templates may be included, as may adaptations whose licenses permit distribution. Keep editable sources where practical and identify authorship, source material, modifications and the applicable license. Use our own wording, examples and design when explaining common methods. Reformatting, rebranding or extensive editing alone does not remove obligations attached to reused expression. Preserve existing attribution and ShareAlike terms on the identified adaptations, including exports to other formats. Packaging checks catch known private archives; they do not determine ownership or redistribution rights.

The plugin is mixed-license: original code and guidance use [MIT](LICENSE); the two adapted templates, their workshop exports, and the strategy-canvas panel in the example gallery use CC BY-SA 4.0. Preserve the notices when reusing those materials. The manifest expression is `MIT AND CC-BY-SA-4.0`, not a claim that third-party work is MIT.

Packaging checks cover local links, public-file scope, manifests, script behavior and relocation. They do not establish native host discovery, cloud connector access, browser rendering, returned-feedback application or real product outcomes. Fictional examples are not market evidence; public source links may change and require current verification when used for current claims.
