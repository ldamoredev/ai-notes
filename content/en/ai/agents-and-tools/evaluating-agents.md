---
title: "Evaluating agents"
description: Evaluate an agent as a distribution of constrained trajectories: verified outcomes, repeatability, safety, latency, and cost.
tags: [agents, evaluation, observability, trajectory]
order: 11
updated: 2026-07-20
kind: implementation
level: intermediate
status: current
prerequisites: [ai/evaluation/designing-eval-sets, ai/agents-and-tools/react-loop]
last_verified: 2026-07-20
---
# Evaluating agents

**Mental model:** an agent is not a completion model with a longer prompt. It samples a
variable-length trajectory through state and tools. An eval therefore asks: *did the
verifiable end state occur repeatedly, by an allowed path, within a resource budget?*
A fluent final response is evidence only after those questions.

## Mechanism: constrained trajectory evaluation

The harness fixes an initial state, executes the policy, records actions and
observations, checks the end state and path constraints, then aggregates repetitions.
Changing any model, prompt, tool, or policy reruns the same contract.

## The five axes

| Axis | Observable metric | Example oracle |
|---|---|---|
| Outcome | success rate | test suite passes; record has expected version |
| Reliability | repeated-task success | all 5 seeded attempts meet the oracle |
| Trajectory | policy and recovery checks | no duplicate call; searched before answer |
| Efficiency | p50/p95 turns, tokens, latency, cost | task remains below release budget |
| Safety | authority and gate violations | no irreversible action without approval |

`pass@k` means at least one of `k` attempts succeeds; it is useful for search but
does not describe a product expected to work every time. `pass^k` asks whether all
`k` independent attempts succeed. For per-run success `0.8`, `pass^8 = 0.8^8 ≈
0.168`: a demo can look capable while a repeated workflow is unreliable.

## Build an eval fixture, not a prompt collection

Each task needs an initial state, allowed tools and permissions, deterministic or
versioned dependencies, an end-state oracle, a budget, and expected failure cases.
Specify end state rather than one exact path: the agent may legitimately use different
searches, but it may not send an email or invent a record. Include adversarial fixtures
such as unavailable data, a transient tool error, and untrusted text containing an
instruction. Keep development and holdout tasks separate.

## Executable aggregation

Run with `python3`; expected output: `pass@5 1 pass^5 0 rate 0.8`.

```python
runs = [True, True, False, True, True]
print("pass@5", int(any(runs)), "pass^5", int(all(runs)), "rate", sum(runs) / len(runs))
assert sum(runs) / len(runs) == 0.8
```

Store the per-run trace beside this result. A failure needs tool inputs, validated
outputs, policy decisions, retry reason, token count, and environment version. Do not
store private chain-of-thought as an observability requirement; structured action and
observation traces are sufficient for the operational questions.

## Judge hierarchy and failure modes

Use deterministic state assertions first, rubric-constrained model judging only for
qualities that cannot be mechanically checked, and human review to calibrate judges
and inspect surprises. Common mistakes are a single run, outcome-only scoring,
mocking away every tool failure, and repeatedly tuning on the same small suite. The
decision rule is simple: do not promote a change unless it clears outcome, safety, and
budget thresholds on the holdout distribution; investigate any slice regression even
when the aggregate improves.

## Production lens and exercises

Run the fixture for each model, prompt, tool, retrieval, or policy change. Dashboard
success by task slice and p95 cost; retain failed traces as labeled regression cases.
Roll back a release when a safety violation rises, a critical task falls below its
threshold, or p95 cost breaches its cap.

1. Add a `no_external_write` trajectory assertion to a task.
2. Create a five-run fixture where a retry recovers once but an identical retry fails;
   decide which trace is acceptable and encode the rule.

**Connects to:** [[ai/evaluation/evaluating-agent-systems|agent-system evaluation]] · [[ai/agents-and-tools/agent-failure-modes|failure modes]] · [[ai/mlops/llm-observability-and-tracing|tracing]] · [[ai/agents-and-tools/guardrails-and-human-in-the-loop|approval gates]]

## Sources

- [τ-bench](https://arxiv.org/abs/2406.12045) — repeated-use reliability and policy-adherence evaluation.
- [SWE-bench](https://arxiv.org/abs/2310.06770) — state-verifiable evaluation tasks for software changes.
- [OSWorld](https://arxiv.org/abs/2404.07972) — end-state evaluation for computer-use agents.
- [NIST AI RMF: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — risk-aware evaluation and measurement framing.
