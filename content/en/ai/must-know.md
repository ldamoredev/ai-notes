---
title: Must Know — Twelve Rules for Thinking Clearly About AI
description: Twelve first-principles rules that prevent magical thinking about objectives, data, uncertainty, evaluation, deployment, agents, and oversight.
tags: [orientation, fundamentals, vocabulary]
order: 2
updated: 2026-07-19
kind: concept
level: beginner
status: current
last_verified: 2026-07-19
---
# Must Know — Twelve Rules for Thinking Clearly About AI

The minimum useful AI literacy is not a list of tools. It is a set of constraints on what you are allowed to claim about a system.

## 1. AI is not magic

A model computes a parameterized function. Even when the function is enormous, the path is still inputs → representations → operations → outputs. Training adds an objective, error signal, derivatives or another update rule, and data. If an explanation skips those objects, it has hidden the mechanism.

## 2. Models optimize objectives

A system gets better at what its training and selection process rewards—not at “intelligence” in general. Cross-entropy, preference scores, rewards, ranking metrics, and human choices are proxies. Goodhart's law applies: when a proxy becomes the target, behavior can exploit the gap.

Ask: what scalar or ordering signal selected these parameters, outputs, or policies?

## 3. Data defines behavior

Data determines coverage, correlations, labels, omissions, and representational harms. Architecture and scale cannot recover evidence that is absent or distinguish a spurious correlation without a useful signal. Dataset construction is part of model specification.

Ask: which population, time period, sampling process, annotation policy, and contamination risks produced the examples?

## 4. Generalization is empirical

Low training error does not prove performance on unseen cases. Generalization depends on the relationship among train data, inductive bias, capacity, regularization, selection, and deployment distribution. Measure on data that represents the decision you will actually make.

Ask: unseen relative to what process, and with what confidence interval?

## 5. Correlation is not causation

Predictive association can be useful without identifying an intervention effect. A model trained on observational data may use proxies and confounders. Do not turn feature importance, attention, or a high predictive score into a causal story without a causal design.

Ask: what intervention or identification assumption supports the causal language?

## 6. Benchmarks are partial

A benchmark is a dataset, protocol, metric, and time-stamped comparison. It can saturate, leak into training data, reward shortcuts, or omit product constraints. A leaderboard position is evidence about that protocol, not a universal capability ordering.

Ask: dataset version, prompt/evaluation protocol, contamination controls, compute budget, metric uncertainty, and task relevance.

## 7. Generative models model distributions

An autoregressive language model estimates a conditional distribution over the next token. A diffusion model learns a denoising process related to a data distribution. Sampling selects one possible output. Fluent generation is compatible with factual error because likelihood and truth are different objectives.

Ask: what distribution is represented, how is an output sampled, and what external evidence constrains it?

## 8. Confidence is not truth

Token probability is not calibrated factual confidence. A classifier score may also be miscalibrated under shift. Calibration is an empirical relationship between predicted confidence and observed frequency for a defined population.

Ask: confidence in which event, calibrated on which distribution, and checked how recently?

## 9. Evaluation must match the product

Offline model quality is only one component. Evaluate retrieval, tool contracts, latency, cost, abstention, security, user comprehension, downstream decisions, and recovery. A system can improve a benchmark while making the product worse.

Ask: which user decision or operational outcome does the metric represent?

## 10. Deployment changes the system

Real users adapt, adversaries probe, traffic drifts, feedback loops reshape data, and infrastructure fails. Prompts, models, datasets, indexes, tools, policies, and UI are all versioned system components. Monitoring and rollback are part of correctness.

Ask: what will detect degradation, who owns the alert, and what is the safe fallback?

## 11. Tools and agents expand the threat surface

A model that can read untrusted content and invoke tools connects probabilistic interpretation to real authority. Prompt injection, excessive agency, confused-deputy behavior, non-idempotent retries, and insecure outputs become system risks. Capability and permission must be separate.

Ask: what can the agent read, decide, write, spend, send, or delete—and where is approval enforced outside the model?

## 12. Human oversight must be designed

“A human is in the loop” is not a control unless that person has time, context, authority, a usable interface, and a clear escalation path. Automation bias and alert fatigue can make nominal review weaker than an explicit automated stop.

Ask: what evidence is shown, what action can the reviewer take, what happens on timeout, and how is disagreement recorded?

## A compact inspection checklist

For any AI claim or feature, write down:

1. Problem and decision.
2. Representation and data provenance.
3. Assumptions and objective.
4. Forward computation and learned parameters.
5. Inference and decoding policy.
6. Evaluation protocol and uncertainty.
7. Failure modes and adversaries.
8. Latency, cost, observability, and fallback.
9. Human responsibility and rollback.

If several entries are unknown, the system is not yet understood.

**Connects to:** [[ai/start-here|Start Here]] · [[ai/foundations/mental-models-for-ai|Mental Models for AI Systems]] · [[ai/evaluation/index|Evaluation and Measurement]] · [[ai/ai-safety-and-security/index|AI Safety and Security]]

## Sources

- [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) — a concise historical claim about general methods and computation; read critically, not as a universal law.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — operational framing for mapping, measuring, managing, and governing AI risk.
- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) — connects intended use, evaluation, limitations, and documentation.
- [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565) — specification, robustness, oversight, and side-effect problems stated as technical research questions.
