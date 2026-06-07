---
title: Evaluate RAG Answer Quality
description: A small playbook for checking answer quality, evidence use, and retrieval fit.
tags: [playbook, rag, evaluation]
order: 1
updated: 2026-06-07
---
# Evaluate RAG Answer Quality

Use this playbook when a RAG prototype starts producing plausible answers and needs a disciplined quality check.

## Steps

1. Create 20 representative questions with expected evidence.
2. Log retrieved chunks, final answer, citations, and latency.
3. Score retrieval relevance before scoring the answer.
4. Mark answer failures as missing evidence, wrong evidence, bad synthesis, or unsafe response.
5. Promote recurring failures into regression tests.

## Output

Produce a short eval note with pass rate, failure clusters, examples, and the next change to test.
