---
title: "Grounding & citations"
description: Retrieval only helps if the model actually uses the sources and you can verify it did. Prompting for grounded, cited answers and checking faithfulness.
tags: [rag, grounding, citations, faithfulness]
order: 8
updated: 2026-06-07
---
# Grounding & citations

Retrieving good chunks is necessary but not sufficient — the model still has to **answer
from them** rather than from its [[ai/llms/pretraining-next-token|parametric memory]].
Grounding is making (and proving) that the answer rests on the retrieved sources.

## Prompt for grounded behavior

- **Instruct explicitly**: "Answer **only** using the provided context. If the answer
  isn't there, say you don't know." This is the main lever against
  [[ai/llms/why-llms-hallucinate|hallucination]] in RAG.
- **Label sources** in the context (IDs/titles) and ask the model to **cite** them
  inline, so claims map to chunks.
- Use low [[ai/llms/decoding-and-sampling|temperature]] for factual grounding.

## Citations: trust and traceability

Citations do double duty: they let *users* verify, and they let *you* debug — a wrong
answer with a citation shows whether retrieval or generation failed. Make citations
**checkable** (link to the chunk/source), not decorative.

## Faithfulness vs correctness

Two different questions, both required:

- **Faithfulness / groundedness** — does the answer follow from the retrieved context
  (no unsupported claims)?
- **Correctness** — is it actually right (the context could be wrong or incomplete)?

A faithful answer to a bad chunk is still wrong. [[ai/rag-and-retrieval/evaluating-rag|RAG
evaluation]] measures both, plus whether the cited chunk truly supports the claim.

## Pitfall

Models will happily "cite" a source that doesn't support the statement, or blend
retrieved facts with memorized ones. Don't trust citations to be accurate by default —
[[ai/rag-and-retrieval/evaluating-rag|verify]] that cited spans actually contain the
claim, especially for high-stakes outputs.

**Connects to:** [[ai/llms/why-llms-hallucinate|hallucination]] ·
[[ai/rag-and-retrieval/evaluating-rag|faithfulness eval]] ·
[[ai/prompt-engineering/anatomy-of-a-prompt|grounding instructions]]
