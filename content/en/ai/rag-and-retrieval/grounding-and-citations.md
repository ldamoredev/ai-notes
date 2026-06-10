---
title: "Grounding & citations"
description: Retrieval only helps if the model actually uses the sources and you can verify it did. Prompting for grounded, cited answers and checking faithfulness.
tags: [rag, grounding, citations, faithfulness]
order: 8
updated: 2026-06-10
---
# Grounding & citations

**Mental model:** retrieval gets the right text *near* the model; grounding makes the
model answer *from* it instead of from
[[ai/llms/pretraining-next-token|parametric memory]] — and gives you a way to verify
which one happened. An ungrounded RAG system is a hallucination engine with better
vibes: the retrieved chunks lend false authority to answers that never used them.

## The grounding prompt (the main lever)

The essential moves, in the system prompt:

```typescript
const system = `You answer questions using ONLY the provided source chunks.

Rules:
- Every factual claim must be supported by a chunk. Cite it inline as [chunk_id].
- If the chunks do not contain the answer, say "I can't find this in the available
  documents" — do NOT answer from general knowledge.
- If chunks conflict, surface the conflict and cite both.
- Quote exact figures, dates, and identifiers verbatim from the chunks.`;

const content = hits
  .map((h) => `<chunk id="${h.id}" source="${h.source}" updated="${h.updatedAt}">
${h.text}
</chunk>`)
  .join("\n") + `\n\nQuestion: ${question}`;
```

Why each piece: **explicit refusal instruction** is the single biggest hallucination
reducer in RAG (the model needs permission to not answer); **structured chunk
delimiters with ids** make citations mechanically checkable; **`updated` metadata**
lets the model prefer fresher sources on conflict. Claude is specifically trained to
respect XML-style document structure — see Anthropic's
[grounding guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips).

## API-enforced citations (Claude)

Prompted citations are free-text — the model can cite a chunk that doesn't support the
claim. Anthropic's **Citations API** (January 2025) moves citation extraction into the
API layer: pass sources as `document` (or `search_result`) content blocks with
`citations: {enabled: true}`, and the response interleaves text with citation objects
carrying **character-level offsets into your source text** — verifiable by string
slicing, not by trust:

```typescript
const msg = await anthropic.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{
    role: "user",
    content: [
      ...hits.map((h) => ({
        type: "document" as const,
        source: { type: "text" as const, media_type: "text/plain" as const, data: h.text },
        title: h.source,
        citations: { enabled: true },
      })),
      { type: "text", text: question },
    ],
  }],
});

for (const block of msg.content) {
  if (block.type === "text" && block.citations) {
    for (const c of block.citations) {
      // c.cited_text + char offsets into the document you supplied → render a
      // verifiable reference; the quoted span either exists in your source or not.
    }
  }
}
```

`search_result` content blocks (GA 2025) carry the same mechanism for tool-based
retrieval in [[ai/rag-and-retrieval/advanced-rag-patterns|agentic RAG]]. Decision
rule: if your product *displays* citations to users, use the API mechanism — free-text
citation formats break parsers and drift; if citations are only for internal
debugging, prompted `[chunk_id]` tags are fine.

## Faithfulness vs correctness

Two different questions, both required:

- **Faithfulness / groundedness** — does the answer follow from the retrieved context
  (no unsupported claims)? A property of *generation*.
- **Correctness** — is the answer actually true? A property of the *corpus + the whole
  pipeline*. A perfectly faithful answer to a stale chunk is still wrong.

Measure them separately ([[ai/rag-and-retrieval/evaluating-rag|RAG evaluation]]):
faithfulness via claim-by-claim [[ai/evaluation/llm-as-judge|LLM-judge]] checks
against the supplied context (RAGAS, Es et al. 2023,
[arXiv:2309.15217](https://arxiv.org/abs/2309.15217), operationalizes this);
correctness against ground-truth answers. Low faithfulness → fix prompts/model; low
correctness with high faithfulness → fix the corpus or retrieval.

## Citation verification (don't trust, check)

Models will cite a real chunk that doesn't support the sentence — fluent
citation-shaped noise. For high-stakes paths, verify offline (sampled) or online
(blocking):

- **Cheap deterministic check**: every quoted span/figure in the answer must appear as
  a substring in some cited chunk — catches fabricated numbers with zero model calls.
- **LLM verification**: per (claim, cited chunk) pair, "Does this chunk support this
  claim? yes/no" with a Haiku-class model; sample 5–10% of traffic and alert on the
  rate, wired into [[ai/mlops/llm-observability-and-tracing|tracing]].
- With the Citations API, step one is free: the API guarantees `cited_text` exists in
  the source; you only verify *support*, not *existence*.

## Failure modes

- **Parametric bleed-through** — the model blends a memorized (older) fact with
  retrieved text, producing a fluent hybrid no chunk contains. Detect via faithfulness
  evals.
- **Citation laundering** — citing the most-topical chunk for every sentence
  regardless of support. Per-claim verification is the only catch.
- **Refusal under-triggering after prompt edits** — a "be more helpful" prompt tweak
  quietly erodes "say you don't know"; keep unanswerable questions in the
  [[ai/evaluation/prompt-regression-testing|regression set]].
- **Conflicting chunks, silent pick** — without a conflict instruction the model picks
  one (often the stale one) and presents it with confidence.
- **Citations as UI decoration** — links nobody can click through to the exact span
  train users to ignore them. Citations must resolve to highlighted source text or
  they're theater.

## In practice

Grounding quality is a *product* surface, not just prompt hygiene: "answer + checkable
citation + honest refusal" is what separates a trustworthy internal tool from a
liability ([[ai/ai-product-engineering/handling-errors-and-hallucinations-in-ui|errors
in UI]]). Decide the refusal UX (what does "I can't find this" look like? does it
offer escalation?) with the same care as the answer UX — refusals are ~5–15% of
traffic in healthy corpora-backed systems.

**Connects to:** [[ai/llms/why-llms-hallucinate|hallucination]] ·
[[ai/rag-and-retrieval/evaluating-rag|faithfulness eval]] ·
[[ai/prompt-engineering/anatomy-of-a-prompt|prompt structure]] ·
[[ai/evaluation/hallucination-detection|detection techniques]]

## Sources

- [Anthropic docs — Citations](https://platform.claude.com/docs/en/build-with-claude/citations) — the API-enforced mechanism: document blocks, char-offset citation objects, supported formats.
- [Simon Willison — Anthropic's new Citations API (Jan 2025)](https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/) — sharp practitioner read on what API-level citations do and don't guarantee.
- [Es et al. 2023 — RAGAS (arXiv:2309.15217)](https://arxiv.org/abs/2309.15217) — defines faithfulness as claim-level entailment against context; the metric vocabulary everyone uses.
- [Anthropic docs — Long context tips](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips) — document structuring and quote-first patterns that measurably improve grounded answers with Claude.
- [Liu et al. 2023 — Evaluating Verifiability in Generative Search Engines (arXiv:2304.09848)](https://arxiv.org/abs/2304.09848) — measured how often deployed engines' citations fail to support their claims (~half of sentences fully supported); the motivation for verification.
