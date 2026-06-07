---
title: "The data distribution & distribution shift"
description: Models assume tomorrow looks like the training data. When that breaks — and it always does — performance silently decays.
tags: [foundations, distribution-shift, drift, robustness]
order: 7
updated: 2026-06-07
---
# The data distribution & distribution shift

Every model is trained on a **sample from some distribution** and silently assumes
production data comes from the same one. When the real world drifts away from that
assumption, accuracy drops — often without any error, just quietly worse outputs.

## A vocabulary for what changed

- **Covariate shift** — the inputs change, the input→output relationship doesn't.
  (New user demographics; a camera with different lighting.)
- **Label shift** — the mix of outcomes changes. (Fraud base rate jumps during a
  holiday.)
- **Concept drift** — the input→output relationship itself changes. (What counts as
  "spam" evolves as spammers adapt.) The hardest kind.

## Why it's the default, not the exception

- The world is non-stationary: behavior, language, prices, and adversaries move.
- Your training set is a *snapshot*; deployment is a *stream*.
- Feedback loops: the model's own actions change the distribution it later sees
  (a recommender reshapes what users click).

## Detecting and responding

- **Monitor inputs**, not just outputs — track feature distributions and flag when
  production data drifts from training (PSI, KS tests, embedding-distance checks).
- **Monitor a proxy for quality** when labels are delayed (confidence, human
  override rate, downstream metrics).
- Respond with **retraining**, recency-weighting, or — for LLM systems — refreshing
  the [[ai/rag-and-retrieval/index|retrieved context]] so facts stay current
  without touching weights.

## For LLMs specifically

A model's **knowledge cutoff** is a built-in distribution shift the day it ships:
the world keeps moving, the weights don't. This is the core argument for retrieval
over fine-tuning when facts change.

**Connects to:** [[ai/foundations/data-splits-and-leakage|realistic splits]] ·
[[ai/mlops/index|monitoring & drift]] ·
[[ai/rag-and-retrieval/index|RAG for fresh facts]]
