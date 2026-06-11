---
title: "Guardrails & human-in-the-loop"
description: An agent that can act can act wrongly. Input/output guardrails, approval gates for high-impact actions, and designing the human checkpoint.
tags: [agents, guardrails, human-in-the-loop, safety]
order: 9
updated: 2026-06-10
---
# Guardrails & human-in-the-loop

**Mental model:** guardrails are checks that run **outside the model** — code that
inspects what goes in, what comes out, and what's about to execute. The model's own
judgment is a quality feature; guardrails are the safety system, and the two must not
be confused: anything enforced only in the prompt is enforced only against polite
inputs. Match the strength of the checkpoint to the **blast radius** of the action.

## The three guardrail surfaces

- **Input** — before text reaches the agent: tenant/permission resolution, off-policy
  request filtering, flagging untrusted content sources
  ([[ai/ai-safety-and-security/input-output-guardrails|input/output guardrails]]).
  Note what input filters *can't* do: reliably catch
  [[ai/ai-safety-and-security/indirect-prompt-injection|indirect injection]] in
  fetched content — that's why action-layer gates exist.
- **Output** — before a response ships: schema validation
  ([[ai/prompt-engineering/structured-outputs|structured outputs]] make this
  mechanical), PII redaction, policy/brand filters, citation checks
  ([[ai/rag-and-retrieval/grounding-and-citations|grounding]]).
- **Action** — before a tool call executes: the layer unique to agents, and the one
  that matters most. Allowlists, argument validation, and approval gates by
  reversibility tier ([[ai/agents-and-tools/autonomy-and-control|least privilege]]).

## An approval gate, concretely

The pattern: classify tools by impact; high-impact calls get persisted as *pending
actions* and the loop pauses until a human decides. This is interruption-and-resume,
not a yes/no popup bolted on:

```typescript
const GATED = new Set(["send_email", "issue_refund", "delete_record"]);

async function executeGated(
  block: Anthropic.ToolUseBlock,
  taskId: string,
): Promise<Anthropic.ToolResultBlockParam> {
  if (!GATED.has(block.name)) {
    return executeDirect(block); // reversible tier: run + log
  }
  // persist the proposal; the agent loop suspends here
  const approval = await db.insert(pendingActions).values({
    taskId,
    tool: block.name,
    args: block.input,
    toolUseId: block.id,
    proposedAt: new Date(),
    // what the reviewer needs to decide FAST:
    summary: await summarizeIntent(block),     // "Refund $84 to cust_9 for order o_122 (damaged)"
    evidence: lastNObservations(taskId, 3),     // why the agent thinks so
  }).returning();
  notifyReviewer(approval[0]);
  throw new AwaitingApproval(taskId);           // resume the loop on decision webhook
}
// On approve: execute, append the tool_result, continue the loop.
// On reject: append tool_result { is_error: true, content: reviewer's reason } —
// the agent sees WHY and can propose an alternative instead of dying.
```

Two design points carry the value: the loop **resumes with the decision in context**
(a rejection with a reason is an observation the agent learns from this task), and
the reviewer sees a **summary + evidence**, not a raw trace.

## Escalation patterns beyond the binary gate

- **Confidence routing** — auto-handle routine cases; route low-confidence or
  high-value ones to humans. Thresholds come from
  [[ai/agents-and-tools/evaluating-agents|eval data]], not intuition.
- **Propose-then-batch** — the agent drafts N actions (replies, fixes); a human
  reviews the batch. Often 10× reviewer throughput vs gating one action at a time.
- **Post-hoc sampling** — for auto-run tiers, humans audit a sample of completed
  actions; the rate adapts to the observed error rate. This is HITL for actions too
  cheap to gate.
- **Kill switch + budgets** — a global pause and per-task spend caps are guardrails
  of last resort; they turn incidents into log lines
  ([[ai/agents-and-tools/agent-failure-modes|runaway loops]]).

## Design the human moment (or it's theater)

The failure mode of HITL is **rubber-stamping**: a reviewer facing 80 opaque
approvals/day approves them all in batch mode. Measured countermeasures:

- Show **intent + evidence + diff**, not transcripts. "Refund $84 — order marked
  delivered-damaged, photo attached, within policy" is decidable in 5 seconds.
- **Track decision time and override rate.** Median approval in <3s with a ~0% reject
  rate means the gate is theater — either the agent is genuinely reliable (promote
  the tool to auto-run + sampling) or reviewers are saturated (lower the gate rate).
- **Make rejection cheap and informative** — one click + a reason field that flows
  back into the agent's context and into your
  [[ai/evaluation/designing-eval-sets|eval set]] as a labeled failure.

Approval data is a free labeled dataset: every approve/reject is a ground-truth
judgment on agent behavior. Feed it back into evals and autonomy-promotion decisions
([[ai/mlops/feedback-loops|feedback loops]]).

## Production lens

Gates add latency by design — minutes-to-hours, not ms — so the *product* must
absorb it: async task UX ("I'll notify you when sent") rather than a spinner.
Instrument the pipeline: gate hit rate, approval latency, override rate, and
incidents-per-1000-auto-runs are the four numbers that tell you whether to widen or
tighten autonomy. Expect the steady state to be **mostly auto-run with sampled
audit** — gates concentrated on the irreversible 5%.

## Failure modes

- **Prompt-only guardrails** — "never delete without asking" is bypassed by the first
  good injection; enforcement lives in code/permissions.
- **Gate fatigue** — over-gating reversible actions trains reviewers to approve
  blindly, which then defeats the gates on irreversible ones.
- **Approval without context** — a bare "agent wants to run issue_refund" forces the
  reviewer to either dig (slow) or guess (unsafe).
- **No resume path** — gates that kill the task instead of suspending it make HITL so
  painful that teams turn it off.

**Connects to:** [[ai/agents-and-tools/autonomy-and-control|least privilege]] ·
[[ai/ai-safety-and-security/excessive-agency|excessive agency]] ·
[[ai/ai-product-engineering/human-in-the-loop-and-trust|HITL UX]] ·
[[ai/mlops/human-in-the-loop-production|HITL in production]]

## Sources

- [OWASP — LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — names human approval for high-impact actions as a primary mitigation.
- [Anthropic — Building Effective Agents (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents) — checkpoints and human feedback loops as core agent architecture, not afterthoughts.
- [Anthropic docs — Mitigate prompt injection](https://platform.claude.com/docs/en/about-claude/use-case-guides/mitigate-prompt-injections) — why action-layer gates are the injection defense that actually holds.
- [OpenAI — A Practical Guide to Building Agents (2025)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — converging vendor guidance on guardrail layering and escalation design.
