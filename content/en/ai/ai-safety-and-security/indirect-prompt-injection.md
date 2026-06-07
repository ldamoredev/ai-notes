---
title: "Indirect prompt injection"
description: Indirect prompt injection hides malicious instructions in data the model reads, such as webpages, emails, documents, search results, or tool output.
tags: [ai-safety, prompt-injection, rag, agents]
order: 3
updated: 2026-06-07
---
# Indirect prompt injection

Indirect prompt injection is more dangerous than the obvious version because the user
may never see the attack. The malicious instructions live inside retrieved documents,
webpages, emails, calendar events, support tickets, tool output, or other data the
model is asked to read.

## The core failure

The system asks the model to process untrusted data, and the model treats part of that
data as instructions. In a RAG system, the injected text may arrive through retrieval.
In an agent, it may arrive through browsing, email, files, or tool responses.

| Source | Example risk |
|---|---|
| Webpage | hidden text tells the agent to exfiltrate data |
| Email | attacker message instructs summarizer to reveal private context |
| Document | retrieved chunk tells model to ignore citation rules |
| Tool output | external API response steers the next tool call |
| Memory | poisoned memory changes future behavior |

## Controls

- Label retrieved content as untrusted data, not instructions.
- Separate instructions from context in prompt structure and formatting.
- Restrict tools available while processing untrusted content.
- Validate tool calls against the user's original intent, not the retrieved text.
- Use allowlisted destinations, schemas, and permissions.
- Log source documents and tool outputs for incident review.

## RAG-specific concerns

RAG increases exposure because the model consumes large volumes of text that may not be
curated. Retrieval relevance is not the same as trustworthiness. A highly relevant
chunk can still contain malicious instructions.

## Pitfall

Sanitizing obvious phrases is brittle. Attackers can phrase instructions indirectly or
encode them in benign-looking text. Treat untrusted content as data by architecture,
not by keyword filter.

**Connects to:** [[ai/rag-and-retrieval/grounding-and-citations|grounding and citations]] ·
[[ai/rag-and-retrieval/rag-failure-modes|RAG failure modes]] ·
[[ai/agents-and-tools/agent-computer-interface|agent-computer interface]]
