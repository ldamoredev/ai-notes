---
title: "Datasheets and data documentation"
description: Datasheets and data cards document why a dataset exists, how it was collected, what it contains, where it fails, and how it should be used.
tags: [data-for-ai, documentation, datasheets]
order: 11
updated: 2026-06-07
---
# Datasheets and data documentation

Dataset documentation makes data assumptions visible. A datasheet or data card records
how a dataset was created, what it represents, what it excludes, and how it should or
should not be used.

## What to document

- Motivation and intended use.
- Collection process, sources, time range, and sampling strategy.
- Labeling guidelines, annotator population, and agreement.
- Preprocessing, filtering, deduplication, and transformations.
- Composition by slices, language, geography, domain, and sensitive attributes where appropriate.
- Known gaps, biases, limitations, and prohibited uses.
- Privacy, consent, licensing, access, and retention.
- Maintenance plan and owner.

## Why it matters

| Use | Documentation helps |
|---|---|
| Training | choose appropriate data and avoid misuse |
| Evaluation | interpret scores and slice gaps |
| Auditing | trace provenance and decisions |
| Governance | assess privacy, consent, and risk |
| Handoffs | prevent context loss between teams |

## Keep it alive

Documentation should update when sources, labeling guidelines, filters, splits,
licensing, or known limitations change. A stale datasheet becomes a false sense of
control.

## Pitfall

Do not bury important limitations in prose nobody reads. Put critical restrictions,
coverage gaps, and prohibited uses in the first screen of the documentation.

**Connects to:** [[ai/data-for-ai/dataset-design-and-sampling|dataset design]] ·
[[ai/data-for-ai/privacy-and-pii-in-datasets|dataset privacy]] ·
[[ai/ai-ethics-and-governance/index|AI ethics and governance]]
