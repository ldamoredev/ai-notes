---
title: "Streaming and perceived latency"
description: Streaming does not make generation faster, but it can make the product feel responsive when the partial output is useful.
tags: [ai-product, streaming, latency, ux]
order: 2
updated: 2026-06-07
---
# Streaming and perceived latency

Streaming sends partial output as the model generates it. It does not reduce total
generation time, but it reduces perceived waiting and gives the user early evidence
that the system is working.

## When streaming helps

- Long-form drafting where the user can read while generation continues.
- Conversational answers where progressive text feels natural.
- Coding or writing tasks where partial output can be interrupted.
- Agent runs where progress events can explain what is happening.

Streaming is less useful when the output must be validated as a whole, such as strict
JSON, classification, or hidden tool-selection steps.

## Design the stream

- Start with a fast status state before tokens arrive.
- Stream meaningful progress, not only raw text.
- Allow cancel, pause, and edit when generation is long.
- Do not show unvalidated structured output as if it were final.
- Mark finality clearly once post-processing and safety checks pass.

## Latency budget

Perceived latency has several moments: time to first response, time to useful partial
output, time to final answer, and time to user action. Optimize the moment the user
actually feels.

## Pitfall

Streaming confident hallucinations faster is still a bad product. Pair streaming with
grounding, validation, and recovery controls.

**Connects to:** [[ai/mlops/serving-and-inference|serving and inference]] ·
[[ai/llms/decoding-and-sampling|decoding]] ·
[[ai/ai-product-engineering/latency-cost-quality-triangle|latency tradeoffs]]
