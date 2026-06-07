---
title: "Model and prompt registry"
description: A registry records the releaseable behavior bundle: model, prompt, retrieval index, tools, evals, approvals, and rollback target.
tags: [mlops, registry, prompts, release-management]
order: 3
updated: 2026-06-07
---
# Model and prompt registry

A registry is the source of truth for what can be deployed. In LLM systems, that means
more than model weights: prompts, retrieval indexes, tool schemas, guardrails, and eval
results are part of the release.

## What belongs in the registry

| Artifact | Why |
|---|---|
| Model or adapter | The learned component |
| Prompt template | The instruction and output contract |
| Retrieval config | Index version, chunking, embedding model, reranker |
| Tool schema | What the model can call |
| Eval report | Evidence that this version is safe to release |
| Approval / owner | Accountability and rollback contact |

The registry should point to immutable artifacts. Mutable "latest" names are fine for
humans but dangerous as release dependencies.

## Stages

Use explicit lifecycle stages: draft, candidate, staging, production, archived. Promotion
should require passing the eval suite and recording the decision.

## Rollback design

Every release should know its rollback target. For LLM apps, rollback may mean reverting
a prompt while keeping the same model, or reverting a retrieval index while keeping the
same prompt.

## Pitfall

If prompt changes ship outside the registry, production behavior can drift without a
model release. Treat prompts as code and as release artifacts.

**Connects to:** [[ai/prompt-engineering/system-prompts-and-roles|system prompts]] ·
[[ai/rag-and-retrieval/vector-databases-and-indexes|vector indexes]] ·
[[ai/mlops/ci-cd-for-ml|CI/CD]]
