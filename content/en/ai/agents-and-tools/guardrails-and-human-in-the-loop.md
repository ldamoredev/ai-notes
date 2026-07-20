---
title: "Guardrails & human-in-the-loop"
description: Guardrails enforce deterministic boundaries around an agent; human review is meaningful only when it has authority, evidence, and a resumable decision.
tags: [agents, guardrails, human-in-the-loop, safety]
order: 9
updated: 2026-07-20
kind: implementation
level: intermediate
status: current
prerequisites: [ai/agents-and-tools/autonomy-and-control, ai/ai-safety-and-security/input-output-guardrails]
last_verified: 2026-07-20
---
# Guardrails & human-in-the-loop

**Mental model:** the model proposes; deterministic infrastructure decides what may
execute. A guardrail is a check outside the model at an input, output, or—most
importantly—action boundary. Human-in-the-loop (HITL) is not a popup: it is a durable
state transition from *proposed* to *approved*, *rejected*, or *expired*.

## Mechanism: enforce before side effect

The executor classifies a proposed action, validates its current state and authority,
persists a decision record when required, and only then performs the side effect. The
model receives the approved or rejected result; it never decides the boundary itself.

## Classify the action, not the sentence

| Tier | Example | Control |
|---|---|---|
| 0: read-only | list an order | tenant authorization, log |
| 1: reversible | create draft | schema/semantic validation, audit log |
| 2: consequential | send external email | explicit approval or narrowly tested policy |
| 3: irreversible/high-impact | refund, delete, disclose data | human approval, dual control where warranted, kill switch |

Prompt instructions can improve behavior but cannot enforce this table. Validate
identity, scope, arguments, policy, and current state in the executor. Tool results
and retrieved text are untrusted data, so they cannot upgrade an action's authority.

## A resumable approval artifact

```python
from dataclasses import dataclass
@dataclass
class Proposal:
    tool: str; args: dict; evidence: list[str]; status: str = "pending"

def decide(p: Proposal, approved: bool, reason: str):
    p.status = "approved" if approved else "rejected"
    return {"status": p.status, "reason": reason, "resume_with": p.status == "approved"}

p = Proposal("issue_refund", {"order": "o_12", "amount": 84}, ["delivered-damaged"])
print(decide(p, False, "photo evidence is missing"))
```

Run with `python3`; **expected output** has status `rejected`. Persist the proposal before
notifying a reviewer. On rejection, append the reason as a tool result so the agent
can propose an alternative; never silently execute or discard the decision.

## Design the reviewer’s evidence

Show intent, affected object, policy basis, relevant evidence, proposed diff, and
reversibility. Measure decision time, rejection/override rate, stale-approval rate,
approval latency, and incidents per thousand autonomous actions. Near-zero rejections with two-second
approvals may mean a safe auto-run tier—or reviewer fatigue. Sampled post-hoc audit is
appropriate only after eval evidence supports it.

## Failure modes and decision rule

- Input/output filters alone miss harmful but valid-looking actions.
- A reviewer without power, time, or context is a rubber stamp, not oversight.
- A gate that kills the task loses repair context; use suspend-and-resume.
- Over-gating cheap reversible actions delays users and trains blanket approval.

Gate any external, irreversible, high-value, or permission-expanding action until a
measured policy permits otherwise. When approval latency conflicts with product UX,
make the task asynchronous rather than weakening the control.

## Exercises

1. Add expiry and a version check to the artifact; reject a decision after the order changes.
2. Classify five tools in your product and justify one promotion from approval to sampled audit with eval metrics.

**Connects to:** [[ai/agents-and-tools/autonomy-and-control|least privilege]] · [[ai/agents-and-tools/evaluating-agents|evaluation]] · [[ai/agents-and-tools/agent-failure-modes|failure containment]] · [[ai/ai-safety-and-security/indirect-prompt-injection|prompt injection]]

## Sources

- [OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — action authority and excessive-permission risks.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — governance and risk-management controls across the lifecycle.
- [OpenAI: A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — layered guardrails and escalation patterns.
- [Anthropic: Mitigate prompt injection](https://platform.claude.com/docs/en/about-claude/use-case-guides/mitigate-prompt-injections) — why enforcement belongs at the action layer.
