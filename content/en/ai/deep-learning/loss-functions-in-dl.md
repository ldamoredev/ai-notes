---
title: "Loss functions in deep learning"
description: The loss is the goal you actually optimize. MSE vs cross-entropy vs contrastive — and how the loss quietly decides what your network becomes.
tags: [deep-learning, loss, cross-entropy, contrastive]
order: 10
updated: 2026-06-07
---
# Loss functions in deep learning

The loss is the single number a network is built to minimize, so it **defines the
task**. Same architecture, different loss → a classifier, a regressor, or an
embedding model. Choosing it well matters more than most architecture tweaks.

## The common losses

| Loss | Task | Pairs with output |
|---|---|---|
| **MSE / L1** | regression | linear output |
| **Cross-entropy** | classification | softmax (multi-class) or sigmoid (binary) |
| **Contrastive / triplet / InfoNCE** | learning [[ai/deep-learning/embeddings-and-latent-spaces|embeddings]] | normalized vectors |

## Why cross-entropy dominates classification

Cross-entropy comes straight from [[ai/foundations/information-theory-basics|information
theory]]: it measures the gap between predicted and true distributions and punishes
**confident wrong** answers hard. Paired with softmax, its gradient is clean and
strong even when the model is badly wrong — which is exactly when you want a big
learning signal. The next-token training of every [[ai/llms/index|LLM]] is just
cross-entropy over the vocabulary.

## Contrastive losses: learning a space, not a label

When the goal is a useful *representation* rather than a class, contrastive losses
pull similar items together and push dissimilar ones apart in vector space. This is
how text/image embedding models (and CLIP) are trained — and why
[[ai/rag-and-retrieval/index|semantic search]] works.

## The proxy-loss gap

The loss you can differentiate is often a **proxy** for what you really care about
(you can't backprop through "user satisfaction" or "accuracy@threshold"). Keep the
gap in mind: a falling loss is necessary, not sufficient — always check the real
[[ai/foundations/evaluation-metrics|metric]] too.

## Pitfall

Mismatching loss and output layer (e.g., softmax + MSE) trains slowly or not at all.
Match the loss to the task and the final activation.

**Connects to:** [[ai/foundations/information-theory-basics|cross-entropy]] ·
[[ai/foundations/how-learning-works|objective vs metric]] ·
[[ai/deep-learning/embeddings-and-latent-spaces|contrastive learning]]
