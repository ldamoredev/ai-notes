---
title: "Assembling context: order & format"
description: Same information, different arrangement, different answer. How ordering, formatting, and delimiters shape how reliably a model uses the context you give it.
tags: [prompt-engineering, context-engineering, formatting]
order: 11
updated: 2026-06-07
---
# Assembling context: order & format

Once you've selected what to include ([[ai/prompt-engineering/managing-the-context-window|context
management]]), *how you lay it out* measurably changes results. The model reads a flat
token stream — structure and position are signals.

## Order matters

- **Edges beat the middle** — put the most important instructions and context near the
  **start or end** ([[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]]).
- **Stable first** — keep the unchanging prefix (system prompt, long reference docs) at
  the top so it's [[ai/llms/context-window-and-kv-cache|cacheable]].
- **Instruction placement** — for long inputs, repeating the key instruction *after*
  the context (as well as before) often helps the model not "forget" the task.

## Format matters

- **Delimit clearly** — separate sections with headers, XML-like tags, or fences so the
  model knows where the document ends and instructions begin. This also reduces
  [[ai/ai-safety-and-security/index|injection]] confusion.
- **Label retrieved chunks** — include source/title so the model can
  [[ai/rag-and-retrieval/index|cite]] and you can trace grounding.
- **Match the model's training** — markdown and clean structure are well-represented in
  pretraining; consistent formatting is easier for the model to parse than walls of
  text.

## A workable default layout

1. System prompt / role + rules (stable, cacheable).
2. Long reference material or retrieved context, clearly delimited and labeled.
3. Few-shot examples (if any).
4. The user's request and the key instruction, at the end.

## Pitfall

Don't blur boundaries between *instructions* and *data*. Untrusted retrieved or
user-supplied text placed without delimiters invites
[[ai/ai-safety-and-security/index|prompt injection]] and makes the model treat data as
commands.

**Connects to:** [[ai/prompt-engineering/managing-the-context-window|context management]] ·
[[ai/llms/long-context-and-lost-in-the-middle|attention bias]] ·
[[ai/ai-safety-and-security/index|injection via context]]
