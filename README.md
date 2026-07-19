# AI Atlas

AI Atlas is a framework-free, bilingual knowledge system for learning artificial intelligence from first principles to production systems. English is canonical; Spanish is a path-matched overlay with explicit English fallback when a translation is missing or stale.

The Atlas is organized around one question: **what happens between input and output, how was it learned, what can fail, and what evidence supports the claim?** Its spine project, Glassbox AI Lab, turns that question into executable milestones from scalar math to a production AI system.

Live site: [ldamoredev.github.io/ai-notes](https://ldamoredev.github.io/ai-notes/)

## What is included

- 24 knowledge branches grouped into 8 phases.
- Canonical English notes plus Spanish overlays and honest fallback SEO.
- Six mechanism-first flagship notes with numerical examples and runnable artifacts.
- Glassbox labs for stable probability, reverse-mode autodiff, causal attention, and token generation traces.
- Client-side search, dark/light themes, responsive navigation, JSON-LD, sitemap, Open Graph, and legacy redirects.
- Source, content, localization, link, SEO, and generated-site validators.

The current editorial debt is intentionally visible. Many inherited atomic notes remain concise pre-refoundation material; `AI-ATLAS-AUDIT.md` scores every canonical page and `CONTENT-PLAN.md` defines the rewrite queue.

## Architecture

```text
build.py                         # Standard-library static generator
content/en/ai/                   # Canonical English source
content/es/ai/                   # Spanish overlays at identical paths
labs/glassbox/                   # Executable spine-project experiments
scripts/audit_content.py         # Full inventory and 12-dimension scoring
scripts/validate_content.py      # Taxonomy/editorial/migration contracts
scripts/validate_site.py         # HTML/link/SEO/localization/asset checks
static/assets/atlas.css          # Glassbox design system
static/assets/search.js          # Search, theme, drawer, locale behavior
site/                            # Generated output; never edit by hand
AI-ATLAS-AUDIT.md                # Evidence-backed current-state audit
MIGRATION-MAP.md                 # Old → new taxonomy and URL policy
CONTENT-PLAN.md                  # Editorial roadmap and Glassbox v0→v10
SOURCES.md                       # Full-URL primary-source registry
GLOSSARY.md                      # ES conventions and Atlas terminology
```

## Build and verify

The generator has no required third-party dependency. CI installs `markdown` and `pygments` for richer rendering; the built-in fallback remains the authoring compatibility target.

```bash
python3 -m py_compile build.py scripts/*.py
python3 build.py
python3 scripts/validate_content.py
python3 scripts/validate_site.py
python3 -m unittest labs.glassbox.test_glassbox -v
```

The build must finish with `unresolved links: 0`. `build.py` deletes and regenerates `site/`; source changes belong under `content/`, `static/`, or `labs/`.

Serve locally because search uses `fetch`:

```bash
python3 -m http.server 8011 --directory site
```

Open `http://127.0.0.1:8011/en/` or `http://127.0.0.1:8011/es/`.

## Taxonomy

| Phase | Branches |
|---|---|
| 00 Orientation | Start Here, Must Know, registry, learning paths |
| 01 Foundations | Mathematics; Computation & Autodiff; Classical AI; Learning Foundations; Statistical ML; Data |
| 02 Learning & Models | Deep Learning; Reinforcement Learning; Model Architectures; Language/Foundation Models; Multimodal AI |
| 03 Training & Inference | Training & Adaptation; Inference Systems |
| 04 Context & Agency | Context Engineering; Retrieval & Knowledge; Agents & Tools |
| 05 Measurement & Trust | Evaluation; Interpretability; Safety & Security; Ethics & Governance |
| 06 Product & Operations | AI Product Engineering; MLOps & Operations |
| ★ Always active | Research & Experimentation; AI Playbooks |

The source of truth for labels, groups, accents, icons, and editorial statuses is `BRANCHES` in `build.py`. `BRANCHES_ES` must contain exactly the same slugs.

## Glassbox AI Lab

Implemented artifacts:

```bash
python3 labs/glassbox/v0_math.py
python3 labs/glassbox/v1_autodiff.py
python3 labs/glassbox/v4_attention.py
python3 -m labs.glassbox.v4_token_trace
```

The roadmap runs from v0 math and probability through autodiff, neural networks, a tensor framework, a mini-transformer, training, inference, retrieval, agents, multimodality, and a production AI system. Every milestone must include deterministic fixtures, tests, expected output, failure injection, metrics, and a short postmortem.

## Add or rewrite a note

Create `content/en/ai/<branch>/<slug>.md`:

```yaml
---
title: "Note title"
description: One-line SEO and search description.
tags: [topic-a, topic-b]
order: 4
updated: 2026-07-19
kind: concept
level: intermediate
status: review-needed
prerequisites: [ai/branch/prerequisite]
last_verified: 2026-07-19
# draft: true
---
```

A canonical deep note contains:

- A durable mental model before taxonomy.
- Mechanism and notation with defined symbols and shapes.
- A small numerical walkthrough.
- An executable artifact and a verification command.
- What frameworks or abstractions hide.
- Failure modes, trade-offs, and a decision rule.
- A production lens: latency, cost, memory, observability, and reliability where relevant.
- Exercises, `**Connects to:**` wikilinks, and 3–8 primary sources with full URLs.

Use path-form wikilinks:

```markdown
[[ai/model-architectures/self-attention-from-first-principles|Self-attention]]
```

Only link to existing canonical pages or indexes. Add the note to its branch index, rebuild, and run both validators.

## Spanish overlays

An overlay must use the same relative path:

```text
content/en/ai/llms/tokenization.md
content/es/ai/llms/tokenization.md
```

Spanish uses technical Rioplatense voseo and mirrors the English structure and evidence density. Missing, empty, draft, or `translation: stale` overlays render the English content under Spanish UI with a visible banner, `lang="en"`, English canonical URL, `noindex, follow`, and no false Spanish `hreflang` or sitemap entry.

## URL migrations

Do not silently move published slugs. Add old-to-new IDs to `LEGACY_REDIRECTS`, update wikilinks, and record the decision in `MIGRATION-MAP.md`. The build emits locale-prefixed and default-locale redirect pages. Validators assert every target exists.

## Deployment

GitHub Actions builds and validates on every push to `main`, then deploys `site/` through GitHub Pages. The generated directory does not need hand edits or source changes.

For another host or fork:

```bash
SITE_URL="https://example.com/ai-notes" GITHUB_URL="https://github.com/example/ai-notes" python3 build.py
```

Regenerate raster brand assets after editing their SVG sources:

```bash
./scripts/rasterize-brand-assets.sh
```

Author and maintainer: **Lautaro Damore**.
