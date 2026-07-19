---
title: "Vision Transformers"
description: Vision Transformers treat images as sequences of patches, letting transformer attention model global visual relationships.
tags: [vision-transformer, vit, attention, computer-vision]
order: 6
updated: 2026-06-07
---
# Vision Transformers

Vision Transformers adapt the transformer idea to images by splitting an image into
patches and treating those patches like tokens. Attention then models relationships
across the whole image.

## Images as tokens

1. Split the image into fixed-size patches.
2. Flatten each patch and project it into an embedding.
3. Add positional information so the model knows where patches came from.
4. Process the patch sequence with transformer layers.
5. Use pooled or special-token representations for classification, retrieval, or downstream tasks.

## Why ViTs matter

| Strength | Explanation |
|---|---|
| Global context | attention can connect distant regions directly |
| Scaling | works well with large datasets and model sizes |
| Transfer | pretrained visual encoders adapt to many tasks |
| Multimodal fit | patch tokens can be fused with language tokens |

CNNs still provide strong inductive biases for locality. ViTs trade some of that bias
for scale and flexible token-based architecture.

## Common variants

- Pure ViT encoders for classification and representation learning.
- Hybrid CNN-transformer models.
- Vision encoders paired with language models.
- Diffusion transformers that replace U-Nets in generative pipelines.

## Pitfall

Patch tokens are not words. Small objects, precise geometry, and dense spatial tasks
can be hard if patching loses detail or if training data lacks the right supervision.

**Connects to:** [[ai/model-architectures/self-attention-from-first-principles|attention]] ·
[[ai/deep-learning/cnns|CNNs]] ·
[[ai/llms/the-decoder-transformer|transformers]]
