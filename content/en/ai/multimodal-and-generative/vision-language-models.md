---
title: "Vision-language models and multimodal LLMs"
description: Vision-language models connect images and text for captioning, OCR, visual question answering, grounding, and multimodal reasoning.
tags: [vision-language, multimodal-llms, visual-reasoning]
order: 7
updated: 2026-06-07
---
# Vision-language models and multimodal LLMs

Vision-language models let language systems consume visual information. They can
caption images, answer questions about screenshots, read documents, inspect charts, and
connect visual evidence to text reasoning.

## Architecture pattern

| Part | Role |
|---|---|
| Vision encoder | converts image patches or regions into visual embeddings |
| Projector | maps visual embeddings into the language model's token space |
| Language model | performs instruction following and text generation |
| Grounding layer | links text outputs to image regions or evidence |

Some systems fuse modalities early inside one model; others use separate encoders and
connect them through adapters.

## Product tasks

- Screenshot understanding and UI assistance.
- Document OCR, table extraction, and layout-aware QA.
- Image captioning and accessibility descriptions.
- Visual search and product matching.
- Chart interpretation and report generation.
- Robot or agent perception in controlled environments.

## Evaluation needs

Visual answers should be checked for object recognition, spatial relationships, OCR,
grounding, refusal behavior, and hallucinated visual details. A fluent answer can still
invent objects that are not in the image.

## Pitfall

Multimodal LLMs can sound certain about visual content they misread. For high-stakes
work, expose evidence regions or screenshots so users can verify the answer.

**Connects to:** [[ai/llms/base-vs-instruct|instruction-tuned models]] ·
[[ai/evaluation/hallucination-detection|hallucination detection]] ·
[[ai/ai-product-engineering/handling-errors-and-hallucinations-in-ui|hallucinations in UI]]
