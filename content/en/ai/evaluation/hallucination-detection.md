---
title: "Hallucination detection"
description: Hallucination detection checks whether claims are supported by evidence, not whether the answer merely sounds plausible.
tags: [evaluation, hallucination, groundedness, rag]
order: 6
updated: 2026-06-07
---
# Hallucination detection

Hallucination detection is the practice of finding unsupported or contradicted claims
in generated output. In production, the practical question is usually groundedness:
are the answer's claims supported by the context the system was allowed to use?

## What counts as a hallucination

- Unsupported claim: the answer states something not present in the evidence.
- Contradicted claim: the answer conflicts with the evidence.
- Fabricated citation: the answer cites a source, section, or URL that does not support it.
- Overgeneralization: the answer expands a narrow fact into a broad conclusion.
- Missing uncertainty: the answer should say the evidence is incomplete but presents certainty.

## Detection approaches

| Approach | Works when | Weakness |
|---|---|---|
| Claim extraction plus evidence check | answers have separable factual claims | can miss implicit claims |
| LLM judge for groundedness | evidence is provided and rubric is clear | judge may over-trust fluent text |
| Citation verification | citations are required | citations can be relevant but insufficient |
| Human review | stakes are high or ambiguous | expensive and slower |

## Design for detectability

- Require citations or quoted evidence for factual answers.
- Keep retrieved context attached to traces.
- Ask the model to state uncertainty when evidence is missing.
- Separate "answer quality" from "evidence support" in the eval rubric.

## Pitfall

Do not treat hallucination as a mysterious model property only. Many hallucinations in
RAG products are system failures: poor retrieval, missing context, ambiguous prompt,
or UI that forces an answer when the right behavior is to abstain.

**Connects to:** [[ai/llms/why-llms-hallucinate|why LLMs hallucinate]] ·
[[ai/rag-and-retrieval/grounding-and-citations|grounding and citations]] ·
[[ai/evaluation/evaluating-rag-systems|RAG system eval]]
