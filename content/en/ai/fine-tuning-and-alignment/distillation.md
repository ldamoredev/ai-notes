---
title: "Distillation"
description: Distillation trains a smaller student model to imitate a stronger teacher, often trading raw capability for latency and cost.
tags: [fine-tuning, distillation, model-compression]
order: 10
updated: 2026-06-07
---
# Distillation

Distillation transfers behavior from a stronger teacher model to a smaller student.
The goal is not to beat the teacher; it is to capture enough of the teacher's behavior
for a narrower task at lower cost and latency.

## Teacher, student, traces

A distillation dataset often contains teacher-generated examples:

- User input or task context.
- Teacher response, tool call, or structured output.
- Optional rationale or intermediate trace.
- Quality labels or filters that remove weak teacher outputs.

The student is then trained with [[ai/fine-tuning-and-alignment/supervised-fine-tuning|SFT]]
or preference methods to imitate the behavior.

## When it makes sense

- The task is frequent enough that inference cost matters.
- A large model already performs well but is too slow or expensive.
- The behavior is narrow and stable.
- You can evaluate the student against production-like examples.

## What gets lost

Smaller students usually lose breadth, robustness, and out-of-domain reasoning. They
may imitate the teacher's format without matching its deeper judgment, especially on
edge cases.

## In practice

Distill a workflow, not a vague capability. Generate examples for the exact product
surface, filter aggressively, and compare student failures against the teacher and the
baseline model.

**Connects to:** [[ai/fine-tuning-and-alignment/when-to-fine-tune|adaptation ladder]] ·
[[ai/llms/quantization-and-inference|inference efficiency]] ·
[[ai/fine-tuning-and-alignment/evaluating-a-finetune|evaluation]]
