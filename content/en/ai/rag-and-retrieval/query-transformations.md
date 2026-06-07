---
title: "Query transformations (rewriting, HyDE, multi-query)"
description: The user's raw question is often a poor search query. Rewriting, expansion, multi-query, and HyDE reshape it to retrieve better.
tags: [rag, query-rewriting, hyde, multi-query]
order: 7
updated: 2026-06-07
---
# Query transformations (rewriting, HyDE, multi-query)

There's a mismatch between how people *ask* and how answers are *written*. A terse,
pronoun-laden, multi-part question rarely matches document phrasing. Query
transformation reshapes the query before retrieval — often a bigger win than tuning the
index.

## The techniques

- **Query rewriting** — clean up and resolve the query: expand abbreviations, fix
  context-dependent references, and (in chat) **rewrite a follow-up into a standalone
  question** using history ("what about the second one?" → a full query).
- **Query expansion** — add synonyms/related terms so [[ai/rag-and-retrieval/hybrid-search|keyword]]
  and dense search cast a wider net.
- **Multi-query** — generate several paraphrases of the question, retrieve for each, and
  union the results. Covers more phrasings and reduces sensitivity to wording.
- **Decomposition** — split a multi-part question into sub-queries, retrieve for each,
  then answer ([[ai/prompt-engineering/task-decomposition|task decomposition]] applied to
  retrieval).
- **HyDE (Hypothetical Document Embeddings)** — have the LLM draft a *hypothetical
  answer*, then embed **that** to search. The hypothetical answer looks more like the
  target documents than the question does, improving dense recall.

## When to use which

- Conversational RAG → **rewrite follow-ups to standalone** (almost mandatory).
- Vocabulary mismatch / recall gaps → multi-query or HyDE.
- Compound questions → decomposition.

## The cost

Each transform adds an **extra LLM call** (latency + tokens) before retrieval even
starts, and multi-query multiplies retrieval work. Add them when evaluation shows a
recall problem — not by default.

## Pitfall

Transformations can drift from user intent (an over-eager rewrite changes the
question). [[ai/rag-and-retrieval/evaluating-rag|Measure]] retrieval before and after;
keep the original query in the mix as a fallback.

**Connects to:** [[ai/rag-and-retrieval/hybrid-search|recall]] ·
[[ai/prompt-engineering/task-decomposition|decomposition]] ·
[[ai/rag-and-retrieval/evaluating-rag|measuring retrieval]]
