---
title: RAG First-Pass Design
description: A small checklist for designing a first useful RAG system.
tags: [rag, retrieval, engineering]
order: 1
updated: 2026-06-07
---
# RAG First-Pass Design

A first-pass RAG system should optimize for inspectability before cleverness. If you cannot explain where an answer came from, you cannot evaluate it.

## Minimum Design

1. Define the answerable question set.
2. Choose source documents and ownership rules.
3. Pick chunk boundaries that preserve meaning.
4. Store citations with retrieved chunks.
5. Evaluate retrieval separately from final answer quality.

## Failure Signals

Watch for correct-looking answers with missing citations, retrieval hits that are semantically close but task-irrelevant, and prompts that hide evidence instead of exposing it.
