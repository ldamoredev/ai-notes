---
title: "Evaluating generative media"
description: Generative media evaluation mixes perceptual metrics, prompt adherence, task success, human review, safety checks, and provenance review.
tags: [evaluation, generative-media, metrics]
order: 11
updated: 2026-06-07
---
# Evaluating generative media

Generative media quality is multi-dimensional. An image can be beautiful but fail the
prompt, match the prompt but violate policy, or look good at thumbnail size while
containing subtle artifacts.

## Metric families

| Metric | Measures | Limits |
|---|---|---|
| FID | distribution similarity to reference images | weak for individual outputs |
| CLIPScore | text-image alignment | can miss quality and safety |
| Human preference | perceived quality and usefulness | expensive and subjective |
| Task success | whether output works in the product | requires task-specific rubrics |
| Safety checks | policy, likeness, explicit content, misinformation | false positives and misses |
| Provenance checks | source, watermark, disclosure, license | metadata can be stripped |

## Evaluation checklist

- Prompt adherence and required elements.
- Visual or audio quality.
- Artifact rate: hands, text, faces, background, motion, clipping.
- Diversity across seeds.
- Safety and policy compliance.
- Rights, consent, and provenance.
- Latency and cost for the target workflow.

## Human eval design

Use pairwise comparison when ranking candidates, rubric scoring when judging required
properties, and expert review when rights, safety, medical, legal, or brand constraints
matter.

## Pitfall

Do not optimize only for aesthetic preference. Product media often needs constraints:
accurate object, correct brand, consistent identity, usable layout, and safe context.

**Connects to:** [[ai/evaluation/task-specific-evals|task-specific evals]] ·
[[ai/evaluation/human-evaluation|human evaluation]] ·
[[ai/multimodal-and-generative/clip-and-shared-embedding-spaces|CLIPScore limits]]
