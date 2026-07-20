---
title: "Build an eval set from scratch"
description: Build a small, versioned, high-signal evaluation set with task contracts, slices, oracles, adversarial cases, owners, and a holdout.
tags: [playbook, evaluation, datasets]
order: 2
updated: 2026-07-20
kind: playbook
level: intermediate
status: current
prerequisites: [ai/evaluation/designing-eval-sets, ai/evaluation/task-specific-evals]
last_verified: 2026-07-20
---
# Build an eval set from scratch

**Mental model:** an eval set is a compact executable contract for a product decision, not a scrapbook of prompts. Each case links an initial condition to expected behavior, an oracle, a slice, and an owner.

## Mechanism: fixtures → oracle → release decision

Collect cases from production traces, experts, edge cases, and incidents; attach metadata and an end-state oracle; then run the same versioned fixtures before and after a change. Keep development, regression, and holdout splits separate so prompt tuning cannot become evaluation leakage.

```python
case = {"id":"refund_missing_photo", "split":"holdout", "risk":"high", "oracle":"must_request_evidence"}
assert case["split"] != "dev" and case["oracle"]
print("case is protected from prompt tuning")
```

Run with `python3`; expected output is `case is protected from prompt tuning`.

## Procedure

1. State the user task, acceptance threshold, and prohibited failure.
2. Collect 30–100 candidates and protect or remove sensitive data.
3. Add task, language, domain, source, difficulty, risk, and authority metadata.
4. Use deterministic checks where possible; calibrate rubrics and human samples otherwise.
5. Include refusal, abstention, escalation, tool-error, and adversarial cases.
6. Record quality, p95 latency, cost, and safety baseline; assign a refresh owner.

| Requirement | Check |
|---|---|
| Representative | main workflows and known failures exist |
| Sliceable | metadata supports segment analysis |
| Graded | every case has oracle or rubric |
| Versioned | fixtures and results reproduce |
| Governed | owner, refresh trigger, privacy policy |

Do not start with hundreds of random cases. Promote a change only when holdout quality, safety, and resource budgets clear their stated thresholds.

## Exercises

1. Create three negative cases where correct behavior is abstention.
2. Add a failure trace to regression and specify its oracle.

**Connects to:** [[ai/evaluation/designing-eval-sets|eval design]] · [[ai/evaluation/task-specific-evals|task evals]] · [[ai/mlops/feedback-loops|feedback loops]]

## Sources

- [HELM](https://crfm.stanford.edu/helm/) — scenario-based transparent evaluation.
- [NIST AI RMF: Measure](https://airc.nist.gov/airmf-resources/playbook/measure/) — evaluation guidance.
- [SWE-bench](https://arxiv.org/abs/2310.06770) — state-verifiable task construction.
