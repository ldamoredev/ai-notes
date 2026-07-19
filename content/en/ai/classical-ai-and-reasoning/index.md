---
title: Classical AI and Reasoning
description: Search, planning, constraints, logic, probabilistic reasoning, and decision methods that remain essential outside generative modeling.
tags: [classical-ai, search, planning, reasoning]
order: 0
updated: 2026-07-19
status: planned
level: beginner
---
# Classical AI and Reasoning

AI predates statistical learning, and many important problems are still solved more reliably by explicit state, constraints, search, and planning. A generative model can propose; a classical algorithm can often verify, optimize, or guarantee.

## Mental model

Represent a problem as states, actions, constraints, beliefs, or logical propositions. Then apply an algorithm whose assumptions and guarantees match that representation. The hard part is often the state space and heuristic, not the syntax of the algorithm.

## Candidate note roadmap

- `state-spaces-and-uninformed-search` — BFS, DFS, uniform-cost search, completeness, and optimality.
- `heuristic-search-and-a-star` — admissibility, consistency, weighted A*, and memory tradeoffs.
- `constraint-satisfaction-problems` — variables, domains, propagation, backtracking, and heuristics.
- `planning-and-state-transition-systems` — STRIPS-style operators, planning graphs, and execution monitoring.
- `logic-and-knowledge-representation` — propositions, first-order logic, ontologies, and open/closed worlds.
- `expert-systems-and-rule-engines` — inference rules, conflict resolution, explanation, and maintenance costs.
- `bayesian-networks-and-probabilistic-reasoning` — conditional independence, exact inference, and approximation.
- `decision-theory-and-expected-utility` — actions under uncertainty, value of information, and risk preferences.
- `symbolic-statistical-and-neuro-symbolic-ai` — complementary strengths, integration patterns, and failure boundaries.
- `when-classical-ai-beats-a-generative-model` — verification, planning, optimization, latency, and determinism rules.

## Production lens

Classical components often become the control plane around learned components: route planners, constraint checkers, schedulers, authorization policies, validators, and deterministic fallbacks. Their state and decisions should be traced alongside model calls.

**Connects to:** [[ai/agents-and-tools/planning-and-decomposition|Planning and Decomposition]] · [[ai/reinforcement-learning/index|Reinforcement Learning]] · [[ai/ai-product-engineering/fallbacks-and-graceful-degradation|Fallbacks and Graceful Degradation]]

## Core sources

- [Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/) — canonical breadth across search, reasoning, planning, uncertainty, and learning.
- [Berkeley CS188](https://inst.eecs.berkeley.edu/~cs188/) — algorithms, projects, and executable teaching material.
- [Planning.wiki](https://planning.wiki/) — compact reference for automated-planning representations and algorithms.
- [Probabilistic Graphical Models course materials](https://cs.stanford.edu/~ermon/cs228/index.html) — probabilistic reasoning and graphical-model inference.
