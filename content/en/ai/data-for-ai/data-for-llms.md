---
title: "Data for LLMs"
description: LLM data work covers corpus selection, filtering, deduplication, mixture design, licensing, quality signals, and safety filtering at scale.
tags: [data-for-ai, llms, pretraining]
order: 8
updated: 2026-06-07
---
# Data for LLMs

LLMs are shaped by enormous data mixtures: web text, books, code, dialogue, academic
text, synthetic examples, instruction data, preference data, and domain corpora. At
that scale, data curation becomes model design.

## Pretraining corpus decisions

- Source selection: web, code, books, papers, forums, documentation, domain corpora.
- Quality filtering: remove spam, boilerplate, low-information pages, and broken text.
- Deduplication: reduce memorization and prevent repeated low-quality documents from dominating.
- Mixture weights: decide how much code, math, multilingual, domain, and conversational data to include.
- Licensing and consent: ensure data can be used for the intended purpose.
- Safety filtering: reduce harmful, private, or policy-violating content where required.

## LLM data stages

| Stage | Data type |
|---|---|
| Pretraining | broad next-token corpus |
| Instruction tuning | task-following examples |
| Preference tuning | comparisons or ranked responses |
| Fine-tuning | domain or product-specific behavior |
| Evaluation | held-out tasks, safety checks, and product cases |

## Scale changes the failure modes

At internet scale, tiny percentages become millions of examples. Deduplication,
contamination checks, privacy filtering, and provenance tracking matter because manual
inspection can only sample the corpus.

## Pitfall

More tokens are not automatically better. Low-quality, duplicated, stale, or
contaminated tokens can waste compute and teach the wrong distribution.

**Connects to:** [[ai/llms/pretraining-next-token|next-token pretraining]] ·
[[ai/fine-tuning-and-alignment/supervised-fine-tuning|supervised fine-tuning]] ·
[[ai/fine-tuning-and-alignment/direct-preference-optimization|DPO]]
