---
title: "Inductive bias & the no-free-lunch idea"
description: Learning is impossible without assumptions. Inductive bias is the set of assumptions a model makes — and why architecture choices matter.
tags: [foundations, inductive-bias, generalization]
order: 3
updated: 2026-06-07
---
# Inductive bias & the no-free-lunch idea

Infinitely many functions fit any finite set of points. To pick one and expect it
to generalize, a learner must *prefer* some explanations over others. That set of
built-in preferences is its **inductive bias**.

## No free lunch, briefly

The no-free-lunch theorems say that, averaged over *all possible* problems, no
learning algorithm beats any other. The catch: real-world problems are not
uniformly random — they have structure (smoothness, locality, compositionality).
**A model wins by having a bias that matches the structure of your data.** There is
no universally best model, only a best match for a problem.

## Inductive bias is baked into the architecture

| Model | Inductive bias |
|---|---|
| Linear models | the relationship is (roughly) linear |
| CNNs | locality + translation invariance (nearby pixels relate) |
| RNNs | sequential order matters; recent context dominates |
| Transformers | any token can attend to any other; weak positional prior |
| Trees | axis-aligned, piecewise-constant splits |

This is why CNNs dominate images and transformers dominate language: their biases
fit the domain. It is also why transformers are *data-hungry* — a weaker prior
must be compensated with more examples.

## Practical consequences

- Choosing a model **is** choosing a bias. Match it to what you know about the data.
- Strong, correct priors mean you need **less data**. Weak priors mean you need
  **more** (and more compute). This is the core trade behind "just scale it."
- Feature engineering and data augmentation are ways to *inject* bias by hand.

## Pitfall

A wrong-but-confident bias generalizes badly in a way no amount of tuning fixes —
e.g., forcing a linear model onto a fundamentally nonlinear relationship.

**Connects to:** [[ai/foundations/generalization-and-overfitting|bias–variance]] ·
[[ai/foundations/features-and-dimensionality|features & representations]] ·
[[ai/deep-learning/index|deep learning]]
