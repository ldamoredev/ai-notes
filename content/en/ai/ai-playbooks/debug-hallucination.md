---
title: "Debug a hallucination"
description: A diagnostic procedure for finding whether a hallucination came from missing context, bad retrieval, weak grounding, prompt pressure, or model behavior.
tags: [playbook, hallucination, debugging, rag]
order: 11
updated: 2026-07-20
kind: playbook
level: intermediate
status: current
prerequisites: [ai/rag-and-retrieval/grounding-and-citations]
last_verified: 2026-07-20
---
# Debug a hallucination

**Mental model:** an unsupported claim is a traceable failure of evidence availability, selection, synthesis, citation, or abstention policy—not automatically a model defect.

## Mechanism: claim → evidence → stage diagnosis

Use this playbook when an AI answer contains unsupported, contradicted, fabricated, or
overconfident claims.

## Inputs

- User request, prompt, retrieved context, answer, citations, model version, and trace.
- Expected answer or source of truth.
- Any user feedback or incident report.

## Procedure

1. Split the answer into factual claims.
2. Mark each claim as supported, contradicted, unsupported, or unverifiable against the available evidence.
3. Check whether the needed evidence was retrieved.
4. If evidence was missing, inspect query rewriting, chunking, indexing, permissions, and recall.
5. If evidence was present, inspect context ordering, prompt instructions, citation rules, and answer synthesis.
6. Check whether the UI or prompt forced an answer when abstention was appropriate.
7. Add the case to the eval set with expected evidence and groundedness criteria.
8. Choose one fix and re-run the relevant RAG or product eval suite.

## Diagnosis table

| Finding | Likely fix |
|---|---|
| Evidence not retrieved | retrieval, chunking, query transform, index freshness |
| Evidence retrieved but ignored | prompt, context ordering, model choice |
| Citation does not support claim | citation verification and stricter rubric |
| Evidence incomplete | abstention, clarification, or escalation |

## Pitfall

Do not label every hallucination as "model problem". Many are architecture problems:
missing evidence, unsafe product pressure, weak citation checks, or stale retrieval.

## Executable claim ledger

```python
claims = {"annual revenue doubled": "unsupported", "launch date": "supported"}
assert "unsupported" in claims.values()
print("requires abstention or retrieval repair")
```

Run with `python3`; expected output names the required next action. Do not release a prompt-only fix until retrieval and citation regressions pass.

## Sources

- [RAG](https://arxiv.org/abs/2005.11401) — retriever-generator formulation.
- [RAGAS](https://docs.ragas.io/) — component-level groundedness and retrieval metrics.

**Connects to:** [[ai/evaluation/hallucination-detection|hallucination detection]] ·
[[ai/llms/why-llms-hallucinate|why LLMs hallucinate]] ·
[[ai/rag-and-retrieval/rag-failure-modes|RAG failure modes]]
