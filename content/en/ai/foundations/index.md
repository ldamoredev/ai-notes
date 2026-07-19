---
title: Learning Foundations
description: The model-agnostic mental models behind AI — what learning optimizes, why models generalize or fail, data, uncertainty, and evaluation.
tags: [foundations, vocabulary]
order: 0
updated: 2026-06-07
---
# Learning Foundations

Foundations hold the concepts that make every later branch easier. These notes are
**model-agnostic**: they apply to a logistic regression and to a frontier LLM
alike, because both are systems that learn a function from data and then have to
behave on data they have never seen.

If you only internalize one thing here: **machine learning is the discipline of
generalizing from finite examples to unseen cases — everything else is detail in
service of that.**

## Mental model

A learning system turns finite observations into behavior on unseen inputs. Its core contract is therefore not training fit but generalization under explicit assumptions about data, loss, inductive bias, and deployment distribution.

## Roadmap: core concepts

- [[ai/foundations/how-learning-works|How learning works: loss, objective, and ERM]]
- [[ai/foundations/generalization-and-overfitting|Generalization, overfitting & the bias–variance tradeoff]]
- [[ai/foundations/inductive-bias-and-no-free-lunch|Inductive bias & the no-free-lunch idea]]
- [[ai/foundations/types-of-learning|Types of learning: supervised, unsupervised, self-supervised, RL]]

## Data & uncertainty

- [[ai/foundations/data-splits-and-leakage|Train/validation/test splits & data leakage]]
- [[ai/foundations/distribution-shift|The data distribution & distribution shift]]
- [[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|Probability & uncertainty for ML]]
- [[ai/foundations/features-and-dimensionality|Features, representations & the curse of dimensionality]]

## The math you actually use

- [[ai/mathematics-for-ai/vectors-matrices-and-tensors|Linear algebra intuition: the dot product as similarity]]
- [[ai/mathematics-for-ai/gradient-descent-and-optimization|Gradient descent: how models actually learn]]
- [[ai/mathematics-for-ai/information-theory-entropy-and-divergence|Information theory: entropy, cross-entropy & KL]]

## Judging models

- [[ai/foundations/evaluation-metrics|Evaluation metrics & what they hide]]

## Systems view

- [[ai/foundations/mental-models-for-ai|Mental models for AI systems]]

## Knowing the limits

- [[ai/foundations/when-not-to-use-ai|When not to use AI]] recognizes where rules, humans, or simpler software beat a model.

**Connects to:** [[ai/mathematics-for-ai/index|Mathematics for AI]] · [[ai/machine-learning/index|Statistical Machine Learning]] · [[ai/evaluation/index|Evaluation and Measurement]]

## Core sources

- [An Introduction to Statistical Learning](https://www.statlearning.com/) — accessible statistical-learning theory with exercises and labs.
- [Understanding Machine Learning](https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/) — formal treatment of learnability, generalization, and optimization.
- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) — production-oriented decision rules and system failure patterns.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) — an operational rubric for production readiness and technical debt.
