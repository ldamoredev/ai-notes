---
title: "Evaluate RAG answer quality"
description: A procedural checklist for checking retrieval, answer quality, citations, groundedness, and product fit in a RAG system.
tags: [playbook, rag, evaluation]
order: 1
updated: 2026-07-20
kind: playbook
level: intermediate
status: current
prerequisites: [ai/rag-and-retrieval/evaluating-rag]
last_verified: 2026-07-20
---
# Evaluate RAG answer quality

**Mental model:** evaluate retrieval before generation. A fluent generator cannot ground an answer in evidence it never received.

## Mechanism: fixture → component scores → root-cause experiment

Use this playbook when a RAG prototype produces plausible answers and needs a disciplined
quality check before deeper tuning or release.

## Inputs

- A representative set of user questions.
- Retrieved chunks for each question.
- Generated answers, citations, latency, token counts, and model version.
- Expected answer or grading rubric for each question.

## Procedure

1. Pick 20-50 questions from real usage or realistic workflows.
2. Mark the source documents or chunks that should support each answer.
3. Run the current system and log query, retrieved chunks, answer, citations, latency, and cost.
4. Score retrieval first: needed evidence present, ranking quality, and context noise.
5. Score generation second: answer relevance, groundedness, citation support, and refusal behavior.
6. Label each failure as missing evidence, wrong evidence, bad synthesis, weak citation, unsafe answer, or product mismatch.
7. Group failures by root cause and choose one system change to test next.
8. Add recurring failures to the regression suite.

## Output

| Artifact | Contents |
|---|---|
| Eval summary | pass rate, top failure clusters, cost, latency |
| Failure table | question, retrieved context, answer, label, owner |
| Next experiment | one retrieval, prompt, chunking, reranking, or UI change |

## Pitfall

Do not tune the prompt before checking retrieval. If the right evidence is missing from
the context, the generator is being asked to solve the wrong problem.

**Connects to:** [[ai/evaluation/evaluating-rag-systems|evaluating RAG systems]] ·
[[ai/rag-and-retrieval/evaluating-rag|retriever vs generator eval]] ·
[[ai/rag-and-retrieval/grounding-and-citations|grounding and citations]]

## Executable failure label

```python
retrieved, supports_claim = False, False
print("retrieval failure" if not retrieved else "synthesis failure" if not supports_claim else "pass")
```

Run with `python3`; expected output is `retrieval failure`. Require evidence presence, citation support, answer quality, latency, and cost before promoting a change.

## Sources

- [RAGAS](https://docs.ragas.io/) — retrieval and generation component metrics.
- [BEIR](https://arxiv.org/abs/2104.08663) — heterogeneous retrieval evaluation.
- [RAG](https://arxiv.org/abs/2005.11401) — system formulation.
