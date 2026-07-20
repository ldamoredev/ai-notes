---
title: "Audit an app for prompt injection"
description: Threat-model and test direct and indirect prompt injection across inputs, retrieval, tools, identities, and high-impact actions.
tags: [playbook, security, prompt-injection]
order: 4
updated: 2026-07-20
kind: playbook
level: intermediate
status: current
prerequisites: [ai/ai-safety-and-security/indirect-prompt-injection, ai/agents-and-tools/autonomy-and-control]
last_verified: 2026-07-20
---
# Audit an app for prompt injection

**Mental model:** untrusted text is data, not authority. Prompt injection matters when text can influence a model that also has secrets, tools, or external write access. A refusal in one chat is not a control; authority must be enforced outside the model.

## Mechanism: untrusted source → proposed action → deterministic authorization

## Procedure

1. Map every direct and indirect text source: user input, web pages, emails, retrieval, files, and tool results.
2. Map secrets, identities, and every tool side effect reachable after each source.
3. Write attack fixtures that request secret disclosure, policy override, cross-tenant access, or unrelated external action.
4. Execute fixtures with tracing; record model output, proposed action, executor decision, and resulting state.
5. Verify tenant checks, allowlists, semantic validation, approval gates, and egress controls block the harm.
6. Add each successful bypass and its regression oracle to CI; remove unnecessary tool authority.

```python
def authorize(user_intent, action):
    return action in user_intent["allowed_actions"]
intent = {"allowed_actions": {"search_kb"}}
assert not authorize(intent, "send_email")
print("blocked: action exceeds user intent")
```

Run with `python3`; expected output proves an injected instruction cannot grant new authority.

## Evidence and decision rule

Keep the prompt template, malicious source, trace, tool call, policy decision, and state diff. A fix is valid only if the harmful action is prevented while legitimate tasks still work. Prioritize combinations of untrusted content, private data, and external writes; remove or gate at least one leg before release.

## Failure modes

Do not treat a single refusal as proof, or redact the trace that would expose a bypass. A model-facing filter cannot replace tenant checks, scoped credentials, and an action-layer gate.

## Exercises

1. Embed an action request in a retrieved document and assert the executor blocks it.
2. Test a tool result that contains a fake “system message.”

**Connects to:** [[ai/ai-safety-and-security/direct-prompt-injection|direct injection]] · [[ai/ai-safety-and-security/indirect-prompt-injection|indirect injection]] · [[ai/agents-and-tools/guardrails-and-human-in-the-loop|approval gates]]

## Sources

- [OWASP Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) — attack anatomy and mitigations.
- [Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) — external-content attack evidence.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — risk-management structure.
