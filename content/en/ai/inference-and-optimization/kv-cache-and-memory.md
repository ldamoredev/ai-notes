---
title: "The KV cache and memory"
description: The KV cache stores attention keys and values for prior tokens, making decoding faster but turning long-context serving into a memory problem.
tags: [inference, kv-cache, memory, attention]
order: 3
updated: 2026-06-07
---
# The KV cache and memory

During generation, a transformer needs previous tokens to predict the next token. The
KV cache stores the attention keys and values for those previous tokens so the model
does not recompute them from scratch at every decoding step.

## Why it matters

| Benefit | Cost |
|---|---|
| Faster decoding | more VRAM per request |
| Reuses previous attention state | memory grows with context length |
| Enables streaming generation | batching becomes harder as sequences vary |
| Avoids repeated prefill work | cache management becomes a serving problem |

The cache scales with number of layers, hidden size, heads, sequence length, batch
size, and precision. Long-context serving is often memory-capacity bound.

## PagedAttention idea

PagedAttention treats KV cache memory more like virtual memory: split cache blocks into
pages, allocate them as requests grow, and reduce fragmentation. This is one reason
engines like vLLM can serve more concurrent requests efficiently.

## Optimization levers

- Limit maximum context length where the product allows it.
- Use prefix caching when many requests share prompt prefixes.
- Quantize KV cache where supported and quality allows.
- Evict or compact cache for long-running sessions.
- Batch requests with compatible sequence lengths.

## Pitfall

Context windows are not free. A model that supports a huge context can still be too
expensive or memory-hungry to serve at that length for every request.

**Connects to:** [[ai/llms/context-window-and-kv-cache|context window and KV cache]] ·
[[ai/inference-and-optimization/gpu-and-hardware-basics|GPU memory]] ·
[[ai/llms/long-context-and-lost-in-the-middle|long context]]
