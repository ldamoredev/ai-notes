---
title: Start Here — AI from First Principles to Production
description: How to navigate AI Atlas, read its mathematics, run Glassbox labs, validate claims, and choose a learning path.
tags: [orientation, learning-path, atlas]
order: 1
updated: 2026-07-19
kind: playbook
level: beginner
status: current
last_verified: 2026-07-19
---
# Start Here — AI from First Principles to Production

AI Atlas is a canonical, executable map of intelligent systems. It does not attempt to summarize every paper; it makes the important computation inspectable—from representation, assumptions, objective, forward pass, loss, gradients, and learned parameters to inference, evaluation, product behavior, and operations.

The working thesis is **from first principles to production systems**. You should be able to explain what happened inside a model call, reproduce a bounded mechanism, measure whether it worked, and identify what changed when it became a product.

## Prerequisites

You need basic programming fluency: variables, functions, loops, tests, command-line execution, and reading a stack trace. Python is the main language for mathematical and model labs; TypeScript appears where agents, tools, and product boundaries make it the clearer choice.

You do not need advanced mathematics before starting. You do need to pause when notation is undefined, work through numerical examples, and resist treating an equation as understood merely because it looks familiar.

## The learning graph

1. Read the phase pages in order.
2. Skim branch indexes before diving into individual notes.
3. Follow prerequisites before jumping to an advanced mechanism.
4. Run linked labs; predict output before execution.
5. Compare expected and observed behavior.
6. Record failures, uncertainty, environment, and versions.
7. Use playbooks when a concept must become a repeatable procedure.

The main sequence is:

```text
problem formulation
→ data and representation
→ objective and assumptions
→ model architecture
→ forward computation
→ loss
→ gradients and optimization
→ learned representation
→ inference and decoding
→ evaluation
→ product and operational behavior
```

## Choose a learning path

### First Principles

[[ai/mathematics-for-ai/index|Mathematics]] → [[ai/computation-and-autodiff/index|computation and autodiff]] → [[ai/deep-learning/index|deep learning]] → [[ai/model-architectures/index|architectures]] → [[ai/llms/index|language and foundation models]].

Use this route if framework abstractions still feel magical.

### AI Engineer

[[ai/machine-learning/index|Statistical ML]] → [[ai/data-for-ai/index|data]] → [[ai/deep-learning/index|deep learning]] → [[ai/fine-tuning-and-alignment/index|training and adaptation]] → [[ai/inference-and-optimization/index|inference]] → [[ai/evaluation/index|evaluation]] → [[ai/mlops/index|MLOps]].

Use this route to take systems from experiment to reliable service.

### LLM Systems

[[ai/model-architectures/self-attention-from-first-principles|Self-attention]] → [[ai/llms/from-prompt-to-generated-token|prompt to token]] → [[ai/prompt-engineering/index|context engineering]] → [[ai/rag-and-retrieval/index|retrieval]] → [[ai/agents-and-tools/index|agents]] → [[ai/evaluation/index|evals]] → [[ai/ai-safety-and-security/index|security]].

Use this route when you already build with model APIs but want the hidden stack exposed.

### Research Literacy

[[ai/mathematics-for-ai/index|Mathematics]] → [[ai/research-and-experimentation/index|paper reading and reproduction]] → [[ai/evaluation/nondeterminism-and-reproducibility|reproducibility]] → [[ai/interpretability/index|interpretation]] → evidence logs.

Use this route to evaluate claims instead of following release narratives.

### Product and Production

[[ai/foundations/when-not-to-use-ai|Problem framing]] → [[ai/data-for-ai/index|data]] → baseline → [[ai/evaluation/index|evals]] → [[ai/ai-product-engineering/index|product]] → deployment → [[ai/mlops/monitoring-and-drift|monitoring]].

Use this route when the unit of success is a user decision, not a model score.

## How to read the mathematics

For every equation:

1. Identify each symbol and its type or shape.
2. State what is fixed and what can change.
3. Compute one tiny numerical example.
4. Check units, ranges, and normalization.
5. Implement the operation without the high-level framework helper.
6. Compare an analytical result with a numerical check when derivatives are involved.

If a note uses mathematics without making these steps possible, treat it as incomplete.

## How to use Glassbox AI Lab

Glassbox AI Lab is the spine project in [[ai/research-and-experimentation/index|Research and Experimentation]]. Start with `labs/glassbox/README.md`; run each milestone's tests; then deliberately break a stated invariant. The goal is not to collect demos. The goal is to connect an observed failure to a mathematical or system assumption.

Every completed milestone must include a learning question, architecture, executable code, fixture or dataset, tests, seed, metrics, expected output, failure modes, and postmortem.

## How to validate a claim

1. Write the claim narrowly enough to be falsifiable.
2. Find the primary paper, official specification, source code, or legal text.
3. Record date, version, dataset, hardware, metric, and comparison baseline.
4. Separate the authors' measurement from your inference.
5. Look for ablations, confidence intervals, negative results, and known contamination.
6. Reproduce the smallest behavior that matters.
7. Mark what remains uncertain.

“State of the art,” “emergent,” “aligned,” “interpretable,” and “production-ready” are incomplete claims without a dated task, metric, comparison, and scope.

## How editorial labels work

- `kind` says what the page is for: concept, derivation, implementation, system, playbook, paper guide, or lab.
- `level` says what background the exposition assumes: beginner, intermediate, or advanced.
- `status` says whether evidence is current, needs review, is outdated, planned, or experimental.
- `last_verified` means a real source and mechanism review occurred on that date. It is never bulk-filled.

## Your first loop

Read [[ai/must-know|Must Know]], then [[ai/mathematics-for-ai/vectors-matrices-and-tensors|Vectors, Matrices, and Tensors]], [[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|Probability, Likelihood, and Uncertainty]], [[ai/mathematics-for-ai/gradient-descent-and-optimization|Gradient Descent and Optimization]], and [[ai/computation-and-autodiff/backpropagation-from-first-principles|Backpropagation from First Principles]]. Run Glassbox v0 and v1. Only then jump to [[ai/model-architectures/self-attention-from-first-principles|Self-Attention from First Principles]].

**Connects to:** [[ai/phase-00-orientation|Phase 00 — Orientation]] · [[ai/research-and-experimentation/index|Research and Experimentation]] · [[ai/ai-playbooks/index|AI Playbooks]]

## Sources

- [Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/) — a broad map of classical and statistical AI.
- [Mathematics for Machine Learning](https://mml-book.github.io/) — prerequisite mathematics tied to ML mechanisms.
- [Dive into Deep Learning](https://d2l.ai/) — executable, shape-aware deep-learning text.
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/) — the bridge from models to production systems.

## First Loop

Start with [[ai/must-know|Must Know]], then read [[ai/foundations/mental-models-for-ai|Mental Models for AI Systems]] and [[ai/llms/transformer-attention-map|Transformer Attention Map]].
