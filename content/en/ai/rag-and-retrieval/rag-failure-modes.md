---
title: "RAG failure modes"
description: A field guide to why RAG answers go wrong — and which stage to fix for each symptom. Most "the LLM is dumb" complaints are retrieval bugs.
tags: [rag, debugging, failure-modes]
order: 10
updated: 2026-06-10
---
# RAG failure modes

**Mental model:** RAG is a pipeline, and pipelines fail at stages. The productive
debugging habit is mapping each **symptom** to the **stage that owns it**, because the
fixes are different and non-overlapping. Barnett et al. 2024 catalogued this from
field case studies as "Seven Failure Points When Engineering a RAG System"
([arXiv:2401.05856](https://arxiv.org/abs/2401.05856)) — missing content, missed
top-k, consolidation loss, extraction failure, wrong format, wrong specificity,
incomplete answers. The table below is that taxonomy reorganized by *what you observe*.

## The failure map

| Symptom | Owning stage | Fix |
|---|---|---|
| Answer misses a fact that **is** in the corpus | retrieval recall | [[ai/rag-and-retrieval/chunking|chunking]], [[ai/rag-and-retrieval/hybrid-search|hybrid search]], `ef_search` ([[ai/rag-and-retrieval/vector-databases-and-indexes|index recall]]) |
| Right doc retrieved but ranked below the cut | ranking | [[ai/rag-and-retrieval/reranking|reranker]], smaller k after rerank |
| Exact term/code/name not found | lexical gap | [[ai/rag-and-retrieval/hybrid-search|BM25 branch]] |
| Chunk retrieved but answer ignores it | generation | [[ai/rag-and-retrieval/grounding-and-citations|grounding prompt]], fewer chunks, better ordering |
| Confident claims no chunk supports | grounding | refusal instruction, faithfulness eval, citation verification |
| Follow-up questions retrieve nonsense | query | [[ai/rag-and-retrieval/query-transformations|conversational rewriting]] |
| Answer cites the wrong year's policy | corpus hygiene | dedup, version filtering, `updated` metadata |
| Partial answers to multi-part questions | query/synthesis | decomposition; check all sub-answers retrieved |
| Answer buried/diluted with many chunks | context | rerank harder, trim k ([[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]]) |
| Other tenant's data in an answer | **security, not quality** | DB-side ACL filters — stop and fix before anything else ([[ai/ai-safety-and-security/data-and-pii-leakage|PII leakage]]) |

## Two structural traps (no tuning fixes these)

- **The answer isn't in the corpus.** Retrieval surfaces what exists; coverage gaps
  need *content*. Detect by tagging eval failures as "missing content" vs "missed
  retrieval" — the ratio tells you whether to invest in pipeline or in docs.
- **Stale or duplicated index.** Near-duplicate chunks crowd the top-k with redundant
  text (squeezing out the second fact you needed); deleted docs whose vectors linger
  serve zombie answers. Index lifecycle (update/delete/dedup) is unglamorous and
  load-bearing.

## The debugging method

1. **Pull the trace** for the failing query — query (raw + rewritten), retrieved
   chunk ids + scores, final prompt, answer
   ([[ai/rag-and-retrieval/rag-first-pass-design|you logged all of this]]).
2. **Read the retrieved chunks.** This single step classifies the failure as
   retrieval vs generation in under a minute, and it's the step people skip in favor
   of prompt-fiddling.
3. **Fix the earliest broken stage first** — recall before ranking before generation.
   A grounding fix on top of a recall bug just produces better-phrased wrong answers.
4. **Change one thing, re-run the [[ai/rag-and-retrieval/evaluating-rag|eval set]].**
   Two simultaneous changes = zero attributable learning.

A worked example: "answers about the refund policy are wrong" → trace shows retrieval
returned 2023-policy chunks ranked above the 2025 update → not a prompt problem, not a
model problem: a corpus-versioning problem. The fix (filter superseded docs, or boost
by `updated`) is invisible if you start from the prompt.

## Monitoring failures in production

Offline evals catch regressions; production catches distribution shift. Cheap signals
to wire into [[ai/mlops/llm-observability-and-tracing|tracing]] dashboards:

- **Top-1 retrieval score per query** — a sagging distribution means queries are
  drifting away from the corpus (new product area, new jargon).
- **Refusal rate** ("can't find this") — a spike means a coverage gap or a retrieval
  regression; a fall after a prompt change may mean grounding eroded.
- **Citation-verification sample rate** ([[ai/rag-and-retrieval/grounding-and-citations|verification]])
  — rising unsupported-claim rate is the hallucination alarm.
- **k-position of clicked/used citations** — if users keep needing the 7th chunk,
  ranking is weak.

> "The LLM gave a bad answer" is usually "retrieval gave it bad context." Read the
> chunks before touching the prompt or the model.

**Connects to:** [[ai/rag-and-retrieval/evaluating-rag|evaluating RAG]] ·
[[ai/rag-and-retrieval/chunking|chunking]] ·
[[ai/llms/why-llms-hallucinate|hallucination]] ·
[[ai/ai-playbooks/debug-hallucination|debug playbook]]

## Sources

- [Barnett et al. 2024 — Seven Failure Points When Engineering a RAG System (arXiv:2401.05856)](https://arxiv.org/abs/2401.05856) — the field-study taxonomy this note reorganizes; short and concrete.
- [Liu et al. 2023 — Lost in the Middle (arXiv:2307.03172)](https://arxiv.org/abs/2307.03172) — why correct-but-buried context still fails; the U-shaped attention result.
- [Chroma — Context Rot (2025)](https://research.trychroma.com/context-rot) — 18-model study showing degradation grows with input length even far below the window limit; the case for aggressive trimming.
- [Hamel Husain — Your AI Product Needs Evals (2024)](https://hamel.dev/blog/posts/evals/) — the look-at-your-data discipline (trace review, error categorization) this debugging method comes from.
- [Eugene Yan — RAG failure taxonomy in production posts](https://eugeneyan.com/writing/llm-patterns/) — practitioner-grade symptom→fix mappings consistent with the table above.
