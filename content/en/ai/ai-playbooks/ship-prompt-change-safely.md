---
title: "Ship a prompt change safely"
description: A release procedure for treating prompt edits like product logic: versioned, evaluated, compared, monitored, and rolled back when needed.
tags: [playbook, prompts, release, evaluation]
order: 7
updated: 2026-07-20
kind: playbook
level: intermediate
status: current
prerequisites: [ai/evaluation/prompt-regression-testing]
last_verified: 2026-07-20
---
# Ship a prompt change safely

**Mental model:** a prompt is production logic. Treat every edit as a versioned behavioral change with a baseline, holdout comparison, launch gate, monitoring plan, and rollback owner.

## Mechanism: candidate → differential eval → gradual release or rollback

Use this playbook when a prompt edit is ready to move beyond local testing and into a
shared environment, release branch, or production traffic.

## Inputs

- Current prompt version and candidate prompt version.
- Regression eval suite and high-risk manual cases.
- Product metrics, cost target, latency target, and safety gates.
- Rollback path and owner.

## Procedure

1. Write the reason for the change and the expected behavior improvement.
2. Change one prompt variable at a time when possible.
3. Run the regression suite against baseline and candidate.
4. Compare pass rate, slice-level failures, cost, latency, refusals, and format validity.
5. Inspect examples where the candidate differs from the baseline.
6. Run targeted cases for known risks and previous incidents.
7. Version the prompt and release notes in the registry.
8. Deploy gradually if traffic or risk justifies it.
9. Monitor production traces and feedback for regressions.
10. Roll back if release gates fail or a serious new failure appears.

## Release gate

| Gate | Example |
|---|---|
| Quality | no drop on target eval slices |
| Format | structured outputs still parse |
| Safety | no new unsafe or over-refusal pattern |
| Cost | token and model usage within budget |
| Latency | p95 within product target |

## Pitfall

Do not ship because the edited prompt fixes the single example that annoyed you. That
example is now a dev case; the regression suite decides.

**Connects to:** [[ai/evaluation/prompt-regression-testing|prompt regression testing]] ·
[[ai/prompt-engineering/evaluating-and-iterating-prompts|evaluating prompts]] ·
[[ai/mlops/model-and-prompt-registry|prompt registry]]

## Executable release gate

```python
baseline, candidate, safety_ok = .88, .90, True
print("release" if candidate >= baseline and safety_ok else "rollback")
```

Run with `python3`; expected output is `release`. Compare critical slices, p95 latency, cost, format validity, refusals, and incident cases—not one aggregate score.

## Sources

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — lifecycle controls.
- [HELM](https://crfm.stanford.edu/helm/) — scenario-based evaluation.
- [OpenAI Cookbook](https://cookbook.openai.com/) — executable eval patterns.
