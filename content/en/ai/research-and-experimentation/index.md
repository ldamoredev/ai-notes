---
title: Research and Experimentation
description: A durable practice for reading papers, reconstructing claims, reproducing results, and separating evidence from hypothesis and marketing.
tags: [research, experiments, reproducibility, papers]
order: 0
updated: 2026-07-19
status: planned
level: intermediate
---
# Research and Experimentation

Research literacy is the ability to turn a claim into inspectable evidence: define what was measured, reconstruct the method, check uncertainty and baselines, reproduce a bounded result, and record what remains unknown.

## Mental model

A research claim is a scoped relationship between a method, evidence, assumptions, and uncertainty. Reading reconstructs that chain; experimentation tests it; reproduction records which parts survive a new implementation or environment.

## Glassbox AI Lab

Glassbox AI Lab is the Atlas spine project. It progresses from scalar operations and probability through autodiff, neural networks, a mini-transformer, training/adaptation, inference, retrieval, agents, multimodality, and production operations. Each milestone must ship code, fixtures, tests, metrics, expected output, failure injection, and a postmortem.

Implemented starting artifacts live in `labs/glassbox/`:

- v0 — numerical foundations and stable probability.
- v1 — scalar reverse-mode autodiff with gradient checks.
- v4 experiment — tiny self-attention and token-generation traces used by flagship notes.

## Candidate note roadmap

- `how-to-read-an-ai-paper` — problem, prior work, claim, method, evidence, and limitations.
- `reconstruct-a-claim-from-results` — metric, dataset, comparison, uncertainty, and valid scope.
- `review-methodology-and-statistics` — controls, ablations, power, intervals, and multiple comparisons.
- `detect-benchmark-gaming-and-contamination` — leakage, cherry-picking, saturation, and hidden test adaptation.
- `reproduce-a-paper-result` — environment, data, seeds, baselines, deviations, and report.
- `compare-papers-with-an-evidence-matrix` — align tasks, assumptions, compute, metrics, and confidence.
- `maintain-a-research-log` — decisions, failures, hypotheses, artifacts, and provenance.
- `evidence-hypothesis-and-marketing` — language rules for calibrated technical claims.
- `follow-a-fast-moving-field` — alerts, primary sources, verification cadence, and knowledge decay.

## Review protocol

Do not summarize the abstract and call it understanding. Recreate at least one table, plot, derivation, or executable behavior when the claim matters. Record hardware, versions, data, seeds, and deviations. A failed reproduction is a result if the failure is characterized.

**Connects to:** [[ai/evaluation/nondeterminism-and-reproducibility|Nondeterminism and Reproducibility]] · [[ai/ai-playbooks/build-eval-set-from-scratch|Build an Eval Set from Scratch]] · [[ai/mathematics-for-ai/index|Mathematics for AI]]

## Core sources

- [ML Reproducibility Checklist](https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf) — concrete evidence and reporting expectations.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) — tests that connect experimentation to production readiness.
- [Stanford CS336: Language Modeling from Scratch](https://stanford-cs336.github.io/spring2025/) — full-stack reconstruction of modern language modeling.
- [Papers with Code](https://paperswithcode.com/) — useful index for artifacts and benchmarks; verify against the primary paper and repository.
