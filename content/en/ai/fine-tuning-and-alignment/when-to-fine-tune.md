---
title: "When to fine-tune vs prompt vs RAG"
description: Fine-tuning is for behavior, not fresh knowledge. Use this decision frame before changing model weights.
tags: [fine-tuning, rag, prompting, decision]
order: 1
updated: 2026-06-07
---
# When to fine-tune vs prompt vs RAG

Fine-tuning is expensive because it changes weights, deployment shape, and evaluation
surface. Before doing it, prove that cheaper adaptation — prompt or retrieval — cannot
produce the behavior you need.

## The adaptation ladder

| Need | First tool | Why |
|---|---|---|
| Better instructions, tone, or output shape | [[ai/prompt-engineering/index|Prompting]] | Behavior can be specified at runtime. |
| Fresh or private knowledge | [[ai/rag-and-retrieval/why-rag|RAG]] | Knowledge stays outside the weights and can update. |
| Stable style or task skill across many calls | [[ai/fine-tuning-and-alignment/supervised-fine-tuning|SFT]] | The behavior becomes default. |
| Smaller, cheaper specialized model | [[ai/fine-tuning-and-alignment/distillation|Distillation]] | Transfer a large model's behavior into a smaller one. |

Fine-tuning should be a response to repeated evidence, not optimism. If a prompt
change fixes the failure, you do not need a fine-tune yet.

## Good reasons to fine-tune

- You have many examples of the exact behavior you want.
- The desired format must be reliable across thousands of calls.
- The base model understands the domain but fails the style, policy, or procedure.
- You need a smaller model to imitate a stronger one for cost or latency.
- You can evaluate the fine-tuned behavior with held-out examples.

## Bad reasons to fine-tune

- "The model does not know our latest docs" → use retrieval.
- "The prompt is messy" → fix context engineering first.
- "We want fewer hallucinations" → evaluate grounding and evidence use first.
- "We have a pile of raw logs" → raw logs are not a training dataset.

## Pitfall

Fine-tuning for facts bakes stale knowledge into the model and makes updates slow.
Use [[ai/rag-and-retrieval/index|retrieval]] for knowledge, and fine-tune for behavior.

**Connects to:** [[ai/prompt-engineering/prompt-to-context-engineering|context engineering]] ·
[[ai/rag-and-retrieval/why-rag|why RAG]] ·
[[ai/fine-tuning-and-alignment/evaluating-a-finetune|fine-tune evaluation]]
