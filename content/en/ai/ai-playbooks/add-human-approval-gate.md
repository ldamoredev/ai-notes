---
title: "Add a human approval gate"
description: Add a resumable, evidence-based approval boundary to consequential AI actions without creating rubber-stamp oversight.
tags: [playbook, human-in-the-loop, agents, safety]
order: 10
updated: 2026-07-20
kind: playbook
level: intermediate
status: current
prerequisites: [ai/agents-and-tools/guardrails-and-human-in-the-loop]
last_verified: 2026-07-20
---
# Add a human approval gate

**Mental model:** the model proposes; infrastructure authorizes. A gate is a persisted state transition—proposed, approved, rejected, expired—not a modal dialog. Use it when an action is external, irreversible, financially consequential, permission-expanding, or regulated.

## Mechanism: proposal → policy → revalidated action

## Procedure

1. Inventory actions and classify blast radius, reversibility, target, and authority.
2. Define auto-run, sampled-audit, and approval tiers with a policy owner.
3. Persist the proposal before notification: tool, arguments, evidence, policy, version, expiry, and idempotency key.
4. Show a reviewer intent, target, diff, evidence, risk, and undo/appeal path.
5. On approval, revalidate state and execute once; on rejection, append the reason to the agent trace.
6. Measure approval latency, overrides, stale decisions, incidents, and reviewer workload.

```python
proposal = {"status":"pending", "amount":84, "order_version":3}
def approve(p, current_version):
    if p["order_version"] != current_version: return "reject: stale proposal"
    p["status"] = "approved"; return "execute once"
print(approve(proposal, 4))
```

Run with `python3`; expected output is `reject: stale proposal`. The executor, not the model, owns that check.

## Definition of done

| Requirement | Verification |
|---|---|
| No bypass path | all lower-level tools enforce the same policy |
| Useful review | reviewer sees evidence and can reject with reason |
| Safe resume | decision is idempotent and revalidates current state |
| Recovery | expiry, kill switch, rollback, and audit record exist |

Over-gating reversible actions creates fatigue; under-gating high-impact actions creates unbounded blast radius. Promote an action only after holdout evals and sampled audits demonstrate it clears safety and quality thresholds.

## Failure modes

Reject stale proposals, duplicate execution, missing evidence, and any route that bypasses the same authorization policy. A reviewer without time, authority, or a rejection reason is not meaningful oversight.

## Exercises

1. Add expiry and a duplicate-execution test to the artifact.
2. Classify five product tools and justify one sampled-audit tier.

**Connects to:** [[ai/agents-and-tools/guardrails-and-human-in-the-loop|guardrails]] · [[ai/agents-and-tools/autonomy-and-control|least privilege]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|oversight]]

## Sources

- [OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — action-authority risks.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — governance controls.
- [OpenAI: A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — layered guardrails.
