---
title: Foundations
description: The model-agnostic mental models behind AI — what learning optimizes, why models generalize or fail, data, uncertainty, and evaluation.
tags: [foundations, vocabulary]
order: 0
updated: 2026-06-07
---
# Foundations

Foundations hold the concepts that make every later branch easier. These notes are
**model-agnostic**: they apply to a logistic regression and to a frontier LLM
alike, because both are systems that learn a function from data and then have to
behave on data they have never seen.

If you only internalize one thing here: **machine learning is the discipline of
generalizing from finite examples to unseen cases — everything else is detail in
service of that.**

## Core concepts

- [[ai/foundations/how-learning-works|How learning works: loss, objective, and ERM]]
- [[ai/foundations/generalization-and-overfitting|Generalization, overfitting & the bias–variance tradeoff]]
- [[ai/foundations/inductive-bias-and-no-free-lunch|Inductive bias & the no-free-lunch idea]]
- [[ai/foundations/types-of-learning|Types of learning: supervised, unsupervised, self-supervised, RL]]

## Data & uncertainty

- [[ai/foundations/data-splits-and-leakage|Train/validation/test splits & data leakage]]
- [[ai/foundations/distribution-shift|The data distribution & distribution shift]]
- [[ai/foundations/probability-and-uncertainty|Probability & uncertainty for ML]]
- [[ai/foundations/features-and-dimensionality|Features, representations & the curse of dimensionality]]

## The math you actually use

- [[ai/foundations/linear-algebra-for-ml|Linear algebra intuition: the dot product as similarity]]
- [[ai/foundations/gradient-descent-intuition|Gradient descent: how models actually learn]]
- [[ai/foundations/information-theory-basics|Information theory: entropy, cross-entropy & KL]]

## Judging models

- [[ai/foundations/evaluation-metrics|Evaluation metrics & what they hide]]

## Systems view

- [[ai/foundations/mental-models-for-ai|Mental models for AI systems]]

## Knowing the limits

- [[ai/foundations/when-not-to-use-ai|When not to use AI]] recognizes where rules, humans, or simpler software beat a model.

## Core sources

- 3Blue1Brown — *Essence of Linear Algebra* and *Neural Networks* (visual intuition).
- StatQuest (Josh Starmer) — bias/variance, cross-validation, metrics.
- James, Witten, Hastie, Tibshirani — *An Introduction to Statistical Learning* (ISLP).
- Aurélien Géron — *Hands-On Machine Learning* (3rd ed.).
- Google — *Machine Learning Crash Course*.
