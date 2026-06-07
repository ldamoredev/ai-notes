---
title: "CLIP and shared embedding spaces"
description: CLIP-style models learn a shared text-image embedding space by training paired encoders with contrastive learning.
tags: [clip, multimodal, embeddings, contrastive-learning]
order: 5
updated: 2026-06-07
---
# CLIP and shared embedding spaces

CLIP-style models align text and images in one embedding space. A caption and its
matching image should land near each other; mismatched pairs should land farther apart.

## How contrastive alignment works

| Component | Role |
|---|---|
| Image encoder | maps image into vector space |
| Text encoder | maps caption into vector space |
| Positive pair | image and its associated text |
| Negative pairs | other images and captions in the batch |
| Contrastive loss | pulls positives together and pushes negatives apart |

The result is a representation where text can search images, images can search text,
and generative models can be guided by language.

## What CLIP enables

- Zero-shot image classification with text labels.
- Text-to-image retrieval and image search.
- Prompt-based conditioning for generative models.
- Similarity scoring between image and caption.
- Multimodal embedding features for downstream tasks.

## Limits

- Web-scale captions are noisy and biased.
- Similarity does not prove factual correctness or safety.
- Text in images, counting, fine-grained spatial reasoning, and rare concepts can fail.
- The embedding space reflects the data distribution it was trained on.

## Pitfall

CLIPScore-like metrics can reward prompt similarity while missing visual defects,
social context, or whether the image is safe to use.

**Connects to:** [[ai/deep-learning/embeddings-and-latent-spaces|embeddings]] ·
[[ai/multimodal-and-generative/evaluating-generative-media|generative media eval]] ·
[[ai/data-for-ai/data-for-llms|large-scale data curation]]
