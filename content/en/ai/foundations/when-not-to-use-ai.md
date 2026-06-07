---
title: "When not to use AI"
description: The most senior AI skill is recognizing when ML/LLMs are the wrong tool. Where rules, humans, or simpler software beat a model — and the questions to ask first.
tags: [foundations, scoping, judgment, decision]
order: 14
updated: 2026-06-07
---
# When not to use AI

Knowing when *not* to reach for AI is as valuable as knowing how to build it. Models
add cost, latency, [[ai/llms/why-llms-hallucinate|unpredictability]], and a maintenance
burden. If a deterministic solution works, it is almost always better — cheaper, faster,
testable, and explainable.

## Prefer something simpler when…

- **A rule or formula suffices.** If the logic is known and stable ("flag orders over
  $10k"), write the rule. ML to relearn a known rule is wasted complexity.
- **You can't tolerate being wrong.** ML is probabilistic; for tasks needing
  guaranteed correctness (accounting, safety interlocks), use deterministic code, with
  AI at most assisting a human.
- **There's no data** (supervised ML) or no way to verify outputs (generative). No
  [[ai/foundations/how-learning-works|signal]] in, nothing reliable out.
- **The stakes are high and unmonitored.** High blast radius + no
  [[ai/agents-and-tools/guardrails-and-human-in-the-loop|human oversight]] is where AI
  failures become incidents.
- **Explainability is mandatory** (some legal/medical/credit contexts) and the model
  can't provide it ([[ai/ai-ethics-and-governance/transparency-and-explainability|transparency]]).
- **A heuristic gets you 90%** at 1% of the cost and effort — ship that first.

## Questions to ask before adding a model

1. What decision does the output drive, and what does a wrong answer cost?
2. Could a rule, lookup, or existing software do this acceptably?
3. Is there data / a way to evaluate quality? ([[ai/evaluation/index|If you can't eval
   it, you can't trust it.]])
4. Can we tolerate variability and the occasional confident error?
5. Who is accountable when it's wrong, and can a human catch it?

## The nuance for LLMs

LLMs lowered the barrier — you can "solve" a task with a prompt and no training data.
That makes it tempting to use them *everywhere*, including where a regex, a database
query, or a form would be more reliable and far cheaper. Use the LLM for the genuinely
fuzzy, language-shaped part; use plain software for the rest.

## Pitfall

"AI" as a mandate rather than a tool — adding a model because it's expected, then
inheriting hallucinations, cost, and latency to solve a problem deterministic code had
already solved. Start from the problem, not the technology.

**Connects to:** [[ai/foundations/mental-models-for-ai|mental models for AI systems]] ·
[[ai/machine-learning/supervised-learning-workflow|frame the problem]] ·
[[ai/ai-product-engineering/the-ai-application-stack|the smallest stack that works]]
