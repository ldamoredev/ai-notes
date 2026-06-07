---
title: "Evaluating RAG systems"
description: RAG evaluation separates retrieval quality, context quality, generation quality, citations, and end-to-end task success.
tags: [evaluation, rag, retrieval, groundedness]
order: 11
updated: 2026-06-07
---
# Evaluating RAG systems

RAG systems fail in stages. A bad answer might come from missing documents, poor
chunking, low recall, irrelevant context, weak synthesis, or fabricated citations, so
RAG evals must decompose the pipeline.

## Evaluation layers

| Layer | Key question | Example metric |
|---|---|---|
| Retrieval | did we retrieve the needed evidence? | recall@k, MRR, NDCG |
| Context | is the supplied context relevant and sufficient? | context precision, context recall |
| Generation | did the answer satisfy the question? | answer relevance, task rubric |
| Grounding | are claims supported by context? | faithfulness, citation support |
| Product | did the workflow solve the user job? | task success, time saved, escalation rate |

## Build the RAG eval set

- Use real questions when possible.
- Store the expected answer or grading rubric.
- Mark relevant chunks or source documents.
- Include unanswerable questions that should trigger abstention.
- Include stale, conflicting, and ambiguous documents if the product has them.

## Diagnose before fixing

- Low retrieval recall means prompt changes will not help much.
- High recall with poor answers points at synthesis, context ordering, or model choice.
- Good answers with weak citations are a citation-generation problem.
- Good offline scores with bad product feedback often mean the eval set is missing real user cases.

## Pitfall

End-to-end RAG scores are useful as a release signal but weak as a debugging tool. If
you do not measure retrieval separately, you will tune the wrong stage.

**Connects to:** [[ai/rag-and-retrieval/evaluating-rag|retriever vs generator eval]] ·
[[ai/rag-and-retrieval/rag-failure-modes|RAG failure modes]] ·
[[ai/evaluation/hallucination-detection|hallucination detection]]
