---
title: "Evaluating agents"
description: Agents are multi-step and non-deterministic, so a final-answer score isn't enough. Evaluate trajectories, tool use, cost, and outcomes — with traces.
tags: [agents, evaluation, observability, trajectory]
order: 11
updated: 2026-06-10
---
# Evaluating agents

**Mental model:** an agent takes a variable-length, non-deterministic path, so a
single run proves almost nothing and a final-answer score hides *how* the answer was
reached. Agent evaluation judges **distributions of trajectories**: did it succeed,
how reliably across repeats, by what path, at what cost, within what permissions.

## Reliability, not capability: pass@k vs pass^k

The metric that reframed the field comes from **τ-bench** (Yao et al. 2024,
[arXiv:2406.12045](https://arxiv.org/abs/2406.12045)): **pass^k** — the probability
that *all k* independent runs of the same task succeed — versus pass@k (at least one
succeeds). Capability demos quote pass@k; production cares about pass^k, and it
falls fast: a task with 80% per-run success has pass^8 ≈ 17%. τ-bench's headline
finding was exactly this gap — agents that looked strong on single runs were wildly
inconsistent across repeats. Report success rate **over N≥5 runs per task**, never
one.

```typescript
// pass^k from repeated runs — the honest reliability number
export async function passHatK(task: EvalTask, k: number): Promise<number> {
  const results = await Promise.all(
    Array.from({ length: k }, () => runAgent(task.input).then(task.check).catch(() => false)),
  );
  return results.every(Boolean) ? 1 : 0; // aggregate over the task suite for the metric
}
```

## What to measure (the five axes)

| Axis | Metric | Catches |
|---|---|---|
| **Outcome** | task success against a *verifiable end state* (test passes, record updated, answer matches) | the headline |
| **Reliability** | pass^k over repeats | flakiness hidden by demos |
| **Trajectory** | right tools, no repeated/wasteful steps, recovered from errors | lucky successes that won't generalize |
| **Efficiency** | turns, tokens, $ per task, latency | cost regressions; the 40-turn success that should be a failure |
| **Safety** | stayed in [[ai/agents-and-tools/autonomy-and-control|permissions]], gates triggered correctly | the success that violated policy en route |

Outcome checks should be **programmatic** wherever possible (state assertions, test
suites — the SWE-bench model); use [[ai/evaluation/llm-as-judge|LLM-as-judge]] with a
rubric only for what code can't check (was the research answer comprehensive?), and
validate the judge against human labels first.

## Trajectory evaluation without drowning

You can't hand-read 50 tasks × 8 runs. The working pyramid:

- **Programmatic trajectory checks** — assertions on the trace: `called search before
  answering`, `no tool called twice with identical args`, `≤ N turns`, `no gated tool
  without approval`. Cheap, deterministic, run in CI.
- **LLM judge over the trace** — rubric-scored review of a sample ("did the agent
  verify before declaring success?"); calibrate against human review.
- **Human deep-reads** — a handful of failures per eval run, because
  [[ai/agents-and-tools/agent-failure-modes|failure taxonomy]] comes from reading,
  not from scores.

All three consume the same artifact: **complete traces** (every thought, tool call,
result, token count), which is why
[[ai/mlops/llm-observability-and-tracing|tracing]] is the prerequisite — in
Langfuse/OTel terms, one trace per task run, one span per turn, tool spans nested.
You cannot evaluate what you didn't record.

## Public benchmarks (use to pick models, not to grade your product)

| Benchmark | Domain | Why it matters |
|---|---|---|
| SWE-bench Verified (Jimenez et al. 2023, [arXiv:2310.06770](https://arxiv.org/abs/2310.06770); 500 human-verified tasks, OpenAI 2024) | real GitHub issue → passing patch | the coding-agent standard |
| τ-bench / τ²-bench ([arXiv:2406.12045](https://arxiv.org/abs/2406.12045), [arXiv:2506.07982](https://arxiv.org/abs/2506.07982)) | tool-agent-user dialogs with policy adherence | reliability (pass^k) + rule-following |
| GAIA (Mialon et al. 2023, [arXiv:2311.12983](https://arxiv.org/abs/2311.12983)) | general assistant tasks, web+tools | breadth; easy for humans, hard for agents |
| OSWorld (Xie et al. 2024, [arXiv:2404.07972](https://arxiv.org/abs/2404.07972)) | real desktop computer use | GUI agents, state-based scoring |
| Terminal-Bench (2025) | terminal/CLI operation | the daily-driver skill for coding agents |

Caveats: scores move quarterly (check leaderboards, not blog posts); contamination
and harness-gaming are documented problems; and **none of them measure *your* task
distribution** — a model's SWE-bench rank is a prior, your 30-task suite is the
evidence.

## Building your suite

Same discipline as [[ai/evaluation/designing-eval-sets|any eval set]], plus
agent-specifics: define tasks by **end state**, not by expected path (paths legitimately
vary); seed each task's environment deterministically (fixtures, mocked externals —
flaky tools make reliability unmeasurable); include **adversarial tasks**
(unachievable goals → should report failure, not fabricate success; injected content
in tool results → should not comply); and re-run the suite on *every* prompt, tool,
or model change — agents regress sideways (a tool description tweak fixes task 3 and
breaks task 11), which is invisible without the full matrix
([[ai/evaluation/prompt-regression-testing|regression testing]]).

## Failure modes

- **Single-run evals** — non-determinism means you measured noise.
- **Outcome-only scoring** — passes hide unsafe/expensive paths; track the five axes.
- **Mocked-everything environments** — an agent eval whose tools never fail measures
  a world that doesn't exist; inject realistic tool errors.
- **Eval-set overfitting** — tuning prompts against the same 20 tasks until they
  pass is training on the test set; hold out tasks, rotate from production traces.

**Connects to:** [[ai/evaluation/evaluating-agent-systems|evaluation branch view]] ·
[[ai/agents-and-tools/agent-failure-modes|failure modes]] ·
[[ai/mlops/llm-observability-and-tracing|tracing & observability]] ·
[[ai/evaluation/llm-as-judge|LLM-as-judge]]

## Sources

- [Yao et al. 2024 — τ-bench (arXiv:2406.12045)](https://arxiv.org/abs/2406.12045) — pass^k and the reliability gap; the paper that made "agents are flaky" measurable.
- [Jimenez et al. 2023 — SWE-bench (arXiv:2310.06770)](https://arxiv.org/abs/2310.06770) + [SWE-bench Verified (OpenAI, 2024)](https://openai.com/index/introducing-swe-bench-verified/) — verifiable end-state evaluation done right.
- [Mialon et al. 2023 — GAIA (arXiv:2311.12983)](https://arxiv.org/abs/2311.12983) — the "easy for humans, hard for agents" design philosophy.
- [Xie et al. 2024 — OSWorld (arXiv:2404.07972)](https://arxiv.org/abs/2404.07972) — state-based scoring for computer-use agents.
- [Anthropic — How we built our multi-agent research system (2025)](https://www.anthropic.com/engineering/multi-agent-research-system) — practical section on evaluating non-deterministic agents (LLM judges + end-state checks + human spot reads).
- [Hamel Husain — Your AI Product Needs Evals (2024)](https://hamel.dev/blog/posts/evals/) — the trace-reading discipline that underlies all of this.
