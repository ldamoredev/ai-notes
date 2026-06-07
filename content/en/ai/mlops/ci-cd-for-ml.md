---
title: "CI/CD for ML systems"
description: ML CI/CD gates releases with tests for code, data, prompts, evals, artifacts, and deployment behavior.
tags: [mlops, cicd, deployment, regression-testing]
order: 7
updated: 2026-06-07
---
# CI/CD for ML systems

CI/CD for ML is not just "deploy the code." It gates a behavior bundle: code, data
transforms, model or prompt version, retrieval config, eval results, and rollback plan.

## CI checks

- Unit tests for data transforms and prompt assembly.
- Schema checks for datasets and feature inputs.
- Eval smoke tests for target behavior.
- Regression tests for safety, format, and latency.
- Artifact validation: model loads, prompt renders, index exists, tool schema parses.

For LLM systems, include replay tests from real traces and exact checks for
[[ai/prompt-engineering/structured-outputs|structured outputs]].

## CD checks

Deployment should be staged: candidate, shadow, canary, ramp, production. Monitor
quality and system metrics at each step before expanding traffic.

| Release pattern | Use when |
|---|---|
| Shadow | You can run new behavior without user impact |
| Canary | You need limited real-user exposure |
| Blue/green | You need fast rollback |
| Feature flag | You need per-segment control |

## Rollback

Rollback must be tested. Know whether you are rolling back code, model, prompt, index,
tool config, or all of them.

## Pitfall

A green deploy that skips evals is only proving the server starts. ML CI/CD must test
behavior, not just uptime.

**Connects to:** [[ai/mlops/model-and-prompt-registry|registry]] ·
[[ai/evaluation/index|evaluation]] ·
[[ai/mlops/llm-observability-and-tracing|trace replay]]
