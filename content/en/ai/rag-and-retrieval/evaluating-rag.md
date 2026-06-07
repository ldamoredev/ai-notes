---
title: "Evaluating RAG: retriever vs generator"
description: RAG fails in two distinct places — retrieval and generation. Evaluate them separately, or you'll tune the wrong half.
tags: [rag, evaluation, ragas, metrics]
order: 9
updated: 2026-06-07
---
# Evaluating RAG: retriever vs generator

The cardinal rule of RAG evaluation: **measure the retriever and the generator
separately.** A bad final answer could mean the right chunk was never retrieved, or it
was retrieved and the model ignored or misused it — opposite fixes. One end-to-end
score hides which.

## Evaluate the retriever (did we fetch the right context?)

Treat it as a search problem with classic [[ai/foundations/evaluation-metrics|ranking
metrics]] on a set of `(query → relevant chunk)` pairs:

- **Recall@k** — is the needed chunk in the top k? (Usually the metric that matters
  most — if it's not retrieved, nothing downstream can save it.)
- **Precision@k / MRR / NDCG** — how high and how clean is the ranking?

## Evaluate the generator (given good context, was the answer good?)

Hold context fixed and judge the response, typically with an
[[ai/evaluation/index|LLM-as-judge]]:

- **Faithfulness / groundedness** — is every claim supported by the context (no
  [[ai/llms/why-llms-hallucinate|hallucination]])?
- **Answer relevance** — does it actually address the question?
- **Context precision/recall** — was the retrieved context relevant and sufficient?

Frameworks like **RAGAS** operationalize exactly these axes.

## Build the eval set

You need representative `(query, ground-truth answer, relevant chunks)` examples —
mine real queries, write expected answers, and mark which chunks are relevant. This is
the same discipline as [[ai/evaluation/index|building any eval set]]; without it you're
tuning by vibes.

## Pitfall

Optimizing the end-to-end score alone leads you to fiddle with prompts when the real
problem is recall (or vice versa). **Diagnose the stage first**, then fix that stage.

**Connects to:** [[ai/evaluation/index|evaluation discipline]] ·
[[ai/rag-and-retrieval/rag-failure-modes|failure modes]] ·
[[ai/foundations/evaluation-metrics|ranking metrics]]
