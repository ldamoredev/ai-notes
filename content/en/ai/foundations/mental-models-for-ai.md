---
title: Mental Models for AI Systems
description: A compact set of mental models for thinking about AI systems beyond model demos.
tags: [foundations, systems, evaluation]
order: 13
updated: 2026-06-07
---
# Mental Models for AI Systems

An AI system is a loop: inputs, model behavior, product constraints, evaluation signals, and human feedback. The model is important, but it is not the whole system.

## Useful Frames

- **Model as component:** treat the model as one fallible service in a larger product.
- **Distribution shift:** ask what changes between the examples you test and the users you serve.
- **Error budget:** decide which failures are tolerable, visible, recoverable, or unacceptable.

## Link Forward

Use this note before designing [[ai/rag-and-retrieval/rag-first-pass-design|RAG First-Pass Design]] or writing an evaluation playbook.
