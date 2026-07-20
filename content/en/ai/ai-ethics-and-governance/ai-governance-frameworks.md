---
title: "AI governance frameworks"
description: Frameworks turn AI principles into decisions, evidence, controls, and review; use them as a traceable operating system, not a compliance checklist.
tags: [governance, nist-ai-rmf, iso-42001, risk-management]
order: 9
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-ethics-and-governance/accountability-and-human-oversight]
last_verified: 2026-07-20
---
# AI governance frameworks

**Mental model:** a governance framework is a repeatable mapping from a use case and
its harms to an owner, evidence, control, metric, and escalation path. It does not
certify that a system is fair or lawful; it makes the organization able to show how it
decided, measured, changed, and stopped the system.

## Mechanism: risk record → control → decision

For every material harm, create a versioned record, attach a testable control and
metric, and route the measured result to a named release, rollback, or remediation
decision. The framework is the loop that keeps those artifacts connected.

## Complementary lenses

| Framework | What it contributes | What it does not replace |
|---|---|---|
| NIST AI RMF | voluntary risk process: Govern, Map, Measure, Manage | law, sector rules, a technical test suite |
| NIST GenAI Profile | generative-AI risk considerations and actions | product-specific threat modeling |
| ISO/IEC 42001 | management-system and continual-improvement structure | evidence that one model is safe or accurate |
| OECD AI Principles | policy-level values and accountability | operational controls |
| EU AI Act | binding obligations where applicable | a complete global governance program |

Start with the applicable law and contracts, then use a framework to make the work
repeatable. The NIST AI RMF is voluntary and its guidance evolves; a risk register
must record the exact version, jurisdiction, and assumptions used.

## From principle to testable control

“Be transparent” is not a control. Convert it into a record such as: *for each user
decision, store the model version, input source classes, confidence/calibration where
relevant, explanation type, reviewer action, and appeal outcome for 180 days.* The
control has an owner, a test, a retention policy, a metric, and a rollback decision.

```python
risk = {"harm": "incorrect benefit denial", "owner": "risk-lead",
        "control": "human review", "metric": "appeal-overturn-rate",
        "threshold": 0.03, "rollback": "disable automated recommendation"}
required = ["harm", "owner", "control", "metric", "threshold", "rollback"]
assert all(risk.get(k) not in (None, "") for k in required)
print("governance record is testable")
```

Run with `python3`; expected output confirms that every decision has operational
fields. In production, validate records in the release workflow rather than trusting
a spreadsheet.

## Operating cadence

At intake, map intended use, affected people, dependencies, and unacceptable harms.
Before release, measure quality, slices, security, and residual risk against a stated
threshold. In operation, monitor drift, incidents, complaints, cost, and control
effectiveness. At review, decide to continue, constrain, retrain, roll back, or
retire. A framework is working only if a metric can cause one of those changes.

## Failure modes and decision rule

- Copying a framework’s labels without evidence produces compliance theater.
- Treating a vendor model card as system assurance omits prompts, retrieval, users,
  and actions.
- One global risk score hides non-compensable harms and jurisdiction-specific duties.
- Annual review alone misses fast changes in models, data, and tool permissions.

Choose the smallest framework set that satisfies the governing obligations and can be
operated continuously. If no owner, metric, or rollback action exists for a material
risk, the use case is not ready to release.

## Exercises

1. Convert a “privacy” principle into a measurable control with an owner and kill condition.
2. Create a crosswalk for one feature between NIST Map/Measure and its release test suite.

**Connects to:** [[ai/ai-ethics-and-governance/accountability-and-human-oversight|accountability]] · [[ai/ai-ethics-and-governance/eu-ai-act-risk-tiers|EU risk tiers]] · [[ai/mlops/monitoring-and-drift|monitoring]] · [[ai/ai-safety-and-security/index|security and threat modeling]]

## Sources

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — the voluntary Govern, Map, Measure, Manage process and current resources.
- [NIST AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) — suggested implementation actions and documentation practices.
- [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — GenAI-specific risks and suggested actions.
- [ISO/IEC 42001 overview](https://www.iso.org/standard/81230.html) — official description of the AI management-system standard.
- [OECD AI Principles](https://oecd.ai/en/ai-principles) — interoperable policy principles and accountability context.
