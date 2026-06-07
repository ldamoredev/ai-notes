---
title: "Structured outputs (JSON & schemas)"
description: Free-text is unparseable at scale. How to get reliable JSON via schema-constrained decoding, and why it beats "please respond in JSON".
tags: [prompt-engineering, structured-output, json, function-calling]
order: 5
updated: 2026-06-07
---
# Structured outputs (JSON & schemas)

To use an LLM inside software, you usually need **machine-readable** output, not prose.
Getting reliable structure is a solved-ish problem if you use the right mechanism
instead of just asking nicely.

## The progression of reliability

1. **"Respond in JSON"** in the prompt — works often, fails sometimes (extra prose,
   trailing commas, markdown fences). Don't rely on it for production.
2. **JSON mode** — the provider guarantees syntactically valid JSON, but not your
   shape.
3. **Schema-constrained / structured outputs** — you supply a JSON Schema (or
   Pydantic/Zod model) and the decoder is constrained to emit output that **conforms**.
   This is the robust option: the structure is enforced at
   [[ai/llms/decoding-and-sampling|decoding]] time, not hoped for.
4. **Function/tool calling** — the model emits a structured call matching a function
   signature; the same schema machinery underpins [[ai/agents-and-tools/index|tool use]].

## Practical guidance

- Prefer the API's **schema/structured-output** feature over prompt-only JSON.
- Keep schemas **flat and explicit**; describe each field; use enums for closed sets.
- Use **temperature ≈ 0** for structured/extraction tasks ([[ai/llms/decoding-and-sampling|decoding]]).
- Still **validate** on your side and handle parse failures gracefully — constraints
  reduce, not eliminate, surprises.

## Why it matters

Structured output is the seam between the probabilistic model and deterministic code.
It turns "an LLM said something" into "a typed object my system can act on" — the
foundation of [[ai/agents-and-tools/index|tool calling]], extraction pipelines, and
evaluable outputs.

**Connects to:** [[ai/llms/decoding-and-sampling|decoding]] ·
[[ai/agents-and-tools/index|tool/function calling]] ·
[[ai/prompt-engineering/evaluating-and-iterating-prompts|validating outputs]]
