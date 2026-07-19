---
title: Machine Learning
description: The classical ML toolkit and the supervised workflow — the methods and habits that still underpin (and out-ship) a lot of "AI".
tags: [machine-learning, supervised-learning]
order: 0
updated: 2026-06-07
---
# Machine Learning

Where [[ai/foundations/index|Foundations]] holds the model-agnostic concepts, this
branch is the **practical classical toolkit**: the algorithms, the supervised
workflow, and the habits that decide whether a model is trustworthy. Most of it
predates deep learning — and for tabular data it still wins, ships faster, and is
far easier to debug than a neural net.

> Rule of thumb: reach for a gradient-boosted tree before a neural network on
> tabular data. Start simple; earn complexity.

## Mental model

Statistical machine learning selects a hypothesis from data under a loss, regularization, and validation protocol. The algorithm matters, but representation, leakage control, calibration, and error analysis usually determine whether measured performance survives deployment.

## Roadmap: workflow and algorithms

- [[ai/machine-learning/supervised-learning-workflow|The supervised learning workflow, end to end]]
- [[ai/machine-learning/error-analysis|Error analysis: reading your model's mistakes]]
- [[ai/machine-learning/ml-pipelines-and-leakage|Pipelines & preventing preprocessing leakage]]

## Core algorithms

- [[ai/machine-learning/linear-and-logistic-regression|Linear & logistic regression]]
- [[ai/machine-learning/decision-trees-and-ensembles|Decision trees & ensembles (RF, gradient boosting)]]
- [[ai/machine-learning/knn-and-svm|kNN & SVM: distance and margins]]
- [[ai/machine-learning/clustering-and-pca|Clustering & PCA: learning without labels]]

## Making models work

- [[ai/machine-learning/feature-engineering|Feature engineering]]
- [[ai/machine-learning/regularization-l1-l2|Regularization: L1, L2 & how they differ]]
- [[ai/machine-learning/cross-validation|Cross-validation done right]]
- [[ai/machine-learning/class-imbalance|Handling class imbalance]]
- [[ai/machine-learning/hyperparameter-tuning|Hyperparameter tuning]]

**Connects to:** [[ai/foundations/index|Learning Foundations]] · [[ai/data-for-ai/index|Data for AI]] · [[ai/evaluation/index|Evaluation and Measurement]]

## Core sources

- [An Introduction to Statistical Learning](https://www.statlearning.com/) — theory, algorithms, and reproducible labs.
- [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/) — deeper treatment of supervised and unsupervised methods.
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — canonical implementation semantics and model-selection guidance.
- [Pattern Recognition and Machine Learning](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) — probabilistic framing of classical ML methods.
- StatQuest — trees, boosting, and ROC/PR intuition.
