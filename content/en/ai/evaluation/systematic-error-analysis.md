---
title: "Systematic error analysis"
description: Error analysis turns failed eval cases into slices, root causes, and a prioritized improvement backlog.
tags: [evaluation, error-analysis, debugging]
order: 10
updated: 2026-06-07
---
# Systematic error analysis

Error analysis is where evals become engineering direction. Aggregate scores tell you
whether quality changed; error analysis tells you what to fix next.

## The loop

1. Collect failures from eval runs, production traces, human review, and support.
2. Label each failure with task, slice, root cause, severity, and fix path.
3. Count failures by bucket and product impact.
4. Prioritize the biggest high-impact buckets.
5. Add representative cases to the regression suite.
6. Re-run after each fix and compare against the baseline.

## Useful failure buckets

| Bucket | Typical fix |
|---|---|
| Missing context | retrieval, chunking, query rewriting |
| Misread context | prompt, rubric, model choice |
| Unsupported claim | grounding check, abstention, citation rules |
| Bad tool call | tool schema, examples, permission design |
| Format failure | structured output schema, parser, retry |
| Unsafe answer | guardrail, policy prompt, human review |
| Cost or latency spike | routing, caching, model choice |

## Slice the errors

- By user intent and task type.
- By document type, language, length, and freshness.
- By model, prompt version, retriever version, and tool version.
- By customer segment, risk level, or traffic source.

## Pitfall

Do not let every failure become a one-off prompt patch. If failures cluster, fix the
system component responsible. If they do not cluster, improve coverage and keep
watching.

**Connects to:** [[ai/machine-learning/error-analysis|ML error analysis]] ·
[[ai/evaluation/designing-eval-sets|eval sets]] ·
[[ai/mlops/llm-observability-and-tracing|tracing]]
