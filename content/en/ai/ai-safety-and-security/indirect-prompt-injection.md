---
title: "Indirect prompt injection"
description: Indirect prompt injection hides malicious instructions in data the model reads, such as webpages, emails, documents, search results, or tool output.
tags: [ai-safety, prompt-injection, rag, agents]
order: 3
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-safety-and-security/direct-prompt-injection]
last_verified: 2026-07-20
---
# Indirect prompt injection

## Mechanism: external content → labeled data → policy-constrained action

```python
source = {"trusted_for_action": False, "text": "send secrets"}
print("ignore instruction" if not source["trusted_for_action"] else "evaluate")
```

Run with `python3`; expected output is `ignore instruction`. Retrieved documents, web pages, emails, and tool results cannot grant authority; isolate secrets and gate external writes.

## Sources

- [Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) — external-content attack evidence.
- [OWASP Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) — mitigations.

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
