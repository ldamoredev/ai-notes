# AGENTS.md — AI Atlas

Operational contract for coding and editorial agents. Read this file first, then:

1. `CONTENT-PLAN.md` — taxonomy, status, rewrite order, Glassbox roadmap.
2. `AI-ATLAS-AUDIT.md` — page-level evidence and recommended action.
3. `MIGRATION-MAP.md` — canonical paths and redirect policy.
4. `SOURCES.md` — full-URL primary-source registry.
5. `GLOSSARY.md` — Spanish overlay conventions.

## Mission

AI Atlas is a static, framework-free, bilingual knowledge system for AI from first principles to production. English is canonical. Spanish is a complete path-matched overlay; missing, stale, draft, or empty ES content falls back to English with explicit language and SEO behavior.

Glassbox AI Lab is the executable spine. Explanations should expose representation, objective, computation, learning, inference, failure, and operations instead of stopping at framework calls.

## Build and release gates

```bash
python3 -m py_compile build.py scripts/*.py
python3 build.py
python3 scripts/validate_content.py
python3 scripts/validate_site.py
python3 -m unittest labs.glassbox.test_glassbox -v
```

- `unresolved links: 0` is mandatory and enforced as a build failure.
- `build.py` deletes and regenerates `site/`; never hand-edit generated output.
- Author for the built-in Markdown fallback: ATX headings, flat lists, tables, blockquotes, fenced code, and ordinary inline markup.
- After layout changes, inspect EN and ES home plus one article at desktop and mobile widths in dark and light themes.
- Do not commit unless the user explicitly asks.

Local server:

```bash
python3 -m http.server 8011 --directory site
```

## Repository map

```text
content/en/ai/<branch>/<slug>.md   # canonical source
content/es/ai/<branch>/<slug>.md   # full Spanish overlay at identical path
labs/glassbox/                     # executable v0→v10 spine artifacts
build.py                           # taxonomy, localization, renderer, SEO, redirects
static/assets/atlas.css            # Glassbox design system
static/assets/search.js            # client behavior
scripts/audit_content.py           # inventory + 12-score evidence rubric
scripts/validate_content.py        # source/editorial/migration contracts
scripts/validate_site.py           # generated HTML/link/SEO/asset contracts
site/                              # generated; never edit
```

## Taxonomy

There are **24 branches in 8 phases**:

- 00 Orientation.
- 01 Foundations: mathematics, computation/autodiff, classical AI, learning foundations, statistical ML, data.
- 02 Learning & Models: deep learning, RL, architectures, language/foundation models, multimodal AI.
- 03 Training & Inference: adaptation and inference systems.
- 04 Context & Agency: context engineering, retrieval, agents/tools.
- 05 Measurement & Trust: evaluation, interpretability, safety/security, ethics/governance.
- 06 Product & Operations: product engineering and MLOps.
- ★ Always active: research/experimentation and playbooks.

`BRANCHES` in `build.py` is the structural source of truth. `BRANCHES_ES` must have exact key parity. Every branch needs current EN and ES `index.md`; every phase needs a current EN and ES page. Indexes include a mental model, roadmap, cross-branch connections, at least three full source URLs, and internal links.

## Canonical note contract

Frontmatter:

```yaml
---
title: "Note title"
description: One-line SEO/search description.
tags: [topic-a, topic-b]
order: 4
updated: 2026-07-19
kind: concept
level: intermediate
status: review-needed
prerequisites: [ai/branch/prerequisite]
last_verified: 2026-07-19
# featured: true
# draft: true
---
```

Expanded metadata is required for flagships and recommended for every deep rewrite. Do not fake freshness: `last_verified` means the claims, URLs, and operational semantics were actually checked.

Body, density before length:

- H1 matches `title`.
- Mental model first, before taxonomy.
- Mechanism from first principles; define symbols, axes, shapes, assumptions, and data flow.
- Small numerical walkthrough where math matters.
- At least one artifact that runs as written, with verification command and expected behavior.
- Explain what frameworks or abstractions hide.
- Named techniques, papers, systems, dates, benchmarks, and primary links.
- Failure modes, trade-offs, and a decision rule.
- Production lens: latency, memory, throughput, cost, observability, reliability, and rollback where relevant.
- Exercises that require calculation, implementation, measurement, or deliberate breakage.
- Close with `**Connects to:**` wikilinks, then `## Sources` with 3–8 primary URLs and reading value.

Never write “studies show” without a source. Use `> ⚠️ Unverified — needs source` for an unresolved claim.

The six current flagships are the reference bar:

- `mathematics-for-ai/vectors-matrices-and-tensors`
- `mathematics-for-ai/probability-likelihood-and-uncertainty`
- `mathematics-for-ai/gradient-descent-and-optimization`
- `computation-and-autodiff/backpropagation-from-first-principles`
- `model-architectures/self-attention-from-first-principles`
- `llms/from-prompt-to-generated-token`

## Links and URL migrations

Use path-form links:

```markdown
[[ai/model-architectures/self-attention-from-first-principles|Self-attention]]
[[ai/x/y#heading|Label]]
```

Only link to an existing canonical note or index. Add new notes to the branch index. For a published move:

1. Create the new canonical file.
2. Update every source wikilink.
3. Add old/new IDs to `LEGACY_REDIRECTS`.
4. Record the rationale in `MIGRATION-MAP.md`.
5. Build and run both validators.

Do not rename a branch merely for a better display label; labels can change without breaking slugs.

## Glassbox lab contract

Each v0→v10 milestone ships:

- Dependency/environment contract.
- Deterministic fixture or versioned dataset.
- Tests and at least one failure injection.
- Expected output and verification command.
- Relevant metrics and resource cost.
- Known limits and short postmortem.
- Links from the associated note and branch.

Keep first-principles artifacts small and inspectable. Add frameworks only after the hidden mechanism has been named and tested.

## Spanish overlays

- Same path and structure as EN; translate labels, not canonical wikilink targets.
- Rioplatense voseo: `usá`, `tenés`, `podés`, `hacé`, `medí`.
- Keep established technical terms when that is how engineers actually speak; follow `GLOSSARY.md`.
- Code, commands, URLs, identifiers, tags, slugs, paper/model names, and metadata enum values stay unchanged.
- When an EN rewrite invalidates an overlay, add `translation: stale` immediately. The build will show honest English fallback and suppress false ES indexing.
- Translate only after the canonical note's interface stabilizes.

## Source and audit discipline

- Prefer primary papers, official standards, official docs, and complete textbooks.
- Verify version-sensitive claims against current authoritative sources.
- Use `python3 scripts/audit_content.py --write AI-ATLAS-AUDIT.md` after a material editorial batch.
- Static audit scores are triage evidence, not human technical review.
- Preserve the pre-refoundation baseline in the audit report so improvement claims remain falsifiable.

## Deployment

GitHub Pages deploys through `.github/workflows/deploy.yml`. CI builds with `SITE_URL` from Pages, runs content and site validation plus Glassbox tests, and uploads `site/`. Live URL: [https://ldamoredev.github.io/ai-notes/](https://ldamoredev.github.io/ai-notes/).
