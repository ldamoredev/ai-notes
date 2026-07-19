---
title: "CNNs: convolution & spatial structure"
description: Convolutional networks bake the structure of images into the architecture — locality and translation invariance — and that inductive bias is why they won vision.
tags: [deep-learning, cnn, convolution, vision]
order: 6
updated: 2026-06-07
---
# CNNs: convolution & spatial structure

A convolutional neural network is a network whose [[ai/foundations/inductive-bias-and-no-free-lunch|inductive
bias]] matches images: nearby pixels relate, and a pattern means the same thing
wherever it appears. Encoding that into the architecture is why CNNs dominated
vision for a decade.

## Convolution: a small filter, slid everywhere

Instead of connecting every pixel to every neuron, a CNN slides small **filters**
(e.g. 3×3) across the image. Each filter learns to detect a local pattern — an edge,
a texture — and applies the **same weights everywhere** (weight sharing). Two big
wins:

- **Locality** — neurons look at small neighborhoods, matching how visual structure
  works.
- **Translation invariance** — a cat detector fires whether the cat is top-left or
  center, because the filter is shared across positions.

Weight sharing also means **far fewer parameters** than a fully-connected net on the
same image — less [[ai/foundations/generalization-and-overfitting|overfitting]], less
compute.

## The hierarchy of features

Stacked convolutions build a feature hierarchy: early layers detect edges and
colors, middle layers detect textures and parts, deep layers detect objects.
**Pooling** (downsampling) shrinks spatial size and grows the receptive field, so
deeper neurons "see" more of the image. This is [[ai/foundations/features-and-dimensionality|representation
learning]] made spatial.

## Where CNNs stand now

CNNs still power most production vision (classification, detection, segmentation) and
are cheap and fast. Vision Transformers (ViT) now match or beat them at large scale —
but ViTs need more data precisely because they *lack* the convolutional bias and must
learn locality from scratch. The trade is the same one everywhere: stronger prior vs
more data (and the [[ai/model-architectures/self-attention-from-first-principles|attention]] story carries
straight into [[ai/llms/index|LLMs]]).

## Pitfall

CNNs assume grid-structured, locally-correlated data. Forcing them onto tabular data
(no spatial structure) wastes their bias — [[ai/machine-learning/decision-trees-and-ensembles|trees]]
usually win there.

**Connects to:** [[ai/foundations/inductive-bias-and-no-free-lunch|inductive bias]] ·
[[ai/model-architectures/self-attention-from-first-principles|attention vs convolution]] ·
[[ai/foundations/features-and-dimensionality|feature hierarchy]]
