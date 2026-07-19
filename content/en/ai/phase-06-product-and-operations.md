---
title: Phase 06 — Product and Operations
description: Product framing, MLOps, observability, monitoring, feedback, reliability, releases, rollbacks, cost, and human review.
tags: [phase, product, mlops, operations]
order: 9
updated: 2026-07-19
---
# Phase 06 — Product and Operations

Deployment changes the system. Real traffic changes inputs and incentives; infrastructure adds latency and failure; interfaces shape user behavior; feedback loops change future data; and every model, prompt, dataset, tool, and policy needs a version and rollback path.

## Mental model

Production is a feedback system: user decisions create traffic and data; infrastructure and models transform them; observations drive releases. Reliability requires traceable versions, bounded fallbacks, human ownership, and rehearsed recovery.

## Roadmap through the branches

- [[ai/ai-product-engineering/index|AI Product Engineering]]
- [[ai/mlops/index|MLOps and Operations]]

## Exit criteria

You can frame the user decision, establish a non-AI baseline, budget latency and cost, trace end-to-end behavior, monitor drift and failures, route to fallbacks or humans, stage releases, and rehearse rollback and incident response.

**Connects to:** [[ai/phase-05-measurement-and-trust|Phase 05 — Measurement and Trust]] · [[ai/phase-always-active|Labs, Research and Playbooks]]

## Core sources

- [Hidden Technical Debt in ML Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) — production coupling and feedback debt.
- [Continuous Delivery for Machine Learning](https://martinfowler.com/articles/cd4ml.html) — reproducible releases and feedback.
- [People + AI Guidebook](https://pair.withgoogle.com/guidebook/) — human-centered product controls.
