---
title: Mathematics for AI
description: The mathematical language of representations, uncertainty, objectives, gradients, and stable computation in AI.
tags: [mathematics, linear-algebra, probability, optimization]
order: 0
updated: 2026-07-19
status: current
level: beginner
---
# Mathematics for AI

Mathematics is not decoration around an AI model. It specifies the objects a system represents, the assumptions it makes, the objective it optimizes, and the uncertainty it cannot remove.

## Mental model

Linear algebra describes representation and transformation. Probability describes uncertainty and conditioning. Calculus describes local change. Optimization turns an objective into parameter updates. Information theory measures coding, surprise, and distribution mismatch. Numerical analysis determines whether those operations survive finite precision.

## Current foundation notes

- [[ai/mathematics-for-ai/vectors-matrices-and-tensors|Vectors, Matrices, and Tensors]]
- [[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|Probability, Likelihood, and Uncertainty]]
- [[ai/mathematics-for-ai/gradient-descent-and-optimization|Gradient Descent and Optimization]]
- [[ai/mathematics-for-ai/information-theory-entropy-and-divergence|Information Theory, Entropy, and Divergence]]

## Candidate note roadmap

- `differential-calculus-and-chain-rule` — derivatives, partials, Jacobians, and the chain rule.
- `statistics-estimation-and-confidence` — estimators, bias, variance, intervals, and hypothesis tests.
- `common-probability-distributions` — Bernoulli, categorical, Gaussian, exponential, and heavy tails.
- `bayes-rule-and-probabilistic-inference` — priors, likelihoods, posteriors, and approximation.
- `cross-entropy-and-kl-divergence` — objectives, coding interpretations, and directionality.
- `convexity-and-non-convex-objectives` — what convex intuition buys and where it stops.
- `constrained-optimization-and-lagrange-multipliers` — constraints, duality, and regularization.
- `numerical-stability-for-ai` — overflow, underflow, log-sum-exp, conditioning, and precision.

## Scope and dependencies

No proof is included merely for prestige. Every derivation must define symbols, show shapes, include a small numerical check, and connect to a computation used elsewhere in the Atlas. Start here before autodiff, neural networks, probabilistic reasoning, or evaluation statistics.

**Connects to:** [[ai/computation-and-autodiff/index|Computation and Autodiff]] · [[ai/foundations/index|Learning Foundations]] · [[ai/machine-learning/index|Statistical Machine Learning]]

## Core sources

- [Mathematics for Machine Learning](https://mml-book.github.io/) — free canonical bridge from linear algebra, calculus, and probability to ML.
- [Probabilistic Machine Learning: An Introduction](https://probml.github.io/pml-book/book1.html) — modern treatment of uncertainty, inference, and learning.
- [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/) — the reference for convex objectives, duality, and optimization structure.
- [Dive into Deep Learning — Preliminaries](https://d2l.ai/chapter_preliminaries/index.html) — executable notation and tensor-oriented examples.
