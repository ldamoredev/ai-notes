---
title: "The EU AI Act and risk tiers"
description: The EU AI Act applies obligations by role, system use, and timeline; classify the deployed system and retain evidence rather than labeling a model once.
tags: [eu-ai-act, regulation, risk-tiers, governance]
order: 8
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-ethics-and-governance/ai-governance-frameworks, ai/ai-ethics-and-governance/accountability-and-human-oversight]
last_verified: 2026-07-20
---
# The EU AI Act and risk tiers

**Mental model:** the EU AI Act is not a model leaderboard label. It is a regulation
whose applicability depends on the actor's role, the AI system or general-purpose AI
(GPAI) model, intended purpose, deployment context, geographic scope, and staged
application dates. Classify the deployed system and maintain evidence as it changes.
This is a technical orientation, not legal advice.

## Mechanism: role + purpose + date → evidence

An organization identifies its legal role and system purpose, checks the applicable
provisions and application date, and turns each conclusion into versioned technical
evidence, owners, tests, and monitoring. A material system change reopens that loop.

## Do not flatten the Act into one four-tier diagram

The useful engineering map separates prohibited practices, high-risk systems,
transparency duties, GPAI-model provider duties, and the many systems that are not
high-risk but still face other law, contracts, or voluntary controls. These categories
can overlap by role: a provider of a GPAI model and a deployer of an application have
different responsibilities. A general “minimal risk” bucket is not a compliance safe
harbor.

| Question | Evidence to retain |
|---|---|
| Who are we: provider, deployer, importer, distributor, authorised representative? | contracts, technical control, market placement record |
| What is the intended purpose and affected domain? | product specification, user journey, decision owner |
| Does a prohibited-practice, high-risk, transparency, or GPAI provision apply? | classification rationale with cited articles |
| When does the relevant provision apply? | versioned implementation timeline and jurisdictional review |
| What changes the classification? | model, capability, user, data, authority, or market change trigger |

## Timeline is part of the control

The Act entered into force in August 2024 and applies in stages. Prohibited-practice
and AI-literacy provisions began applying in February 2025; GPAI provider obligations
began applying in August 2025. Other obligations follow their own transition dates.
The European Commission's timeline—not a blog post or this note—must be checked at
release because implementation instruments and dates can change.

## An executable classification record

Run with `python3`; expected output is `blocked: missing classification evidence`.

```python
record = {"role": "deployer", "purpose": "job-candidate triage",
          "jurisdiction": "EU", "articles_checked": [], "owner": "legal"}
required = ["role", "purpose", "jurisdiction", "articles_checked", "owner"]
if any(not record[k] for k in required):
    print("blocked: missing classification evidence")
```

The program deliberately does not decide legal classification. It prevents release
when an organization has failed to record the decision, evidence, and owner.

## Engineering implications when obligations apply

Translate a requirement into a verifiable artifact: risk-management record; data and
evaluation documentation; versioned technical documentation; logs and instructions
for deployers; human-oversight design; accuracy, robustness, and cybersecurity tests;
post-market monitoring; incident workflow. For GPAI providers, documentation,
copyright policy, training-content summary, and—where relevant—systemic-risk controls
are separate obligations. Do not assume a vendor's statement transfers responsibility
for the assembled application.

## Failure modes and decision rule

- Classifying only a base model ignores the intended purpose and deployer role.
- Treating “not high-risk” as “no obligations” ignores transparency and other law.
- Copying a date from a stale slide makes a correct control arrive too late.
- Documentation created at launch cannot reconstruct undocumented model or policy changes.

Escalate to qualified legal and compliance review before placing a system on the EU
market or materially changing its purpose, capability, or affected population. Keep
the technical team responsible for producing reproducible evidence, not for inventing
legal conclusions.

## Exercises

1. Add a model-version change trigger to the record and fail the release until classification is reconfirmed.
2. Map one system requirement to an artifact, owner, test, retention period, and rollback action.

**Connects to:** [[ai/ai-ethics-and-governance/ai-governance-frameworks|governance frameworks]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|human oversight]] · [[ai/ai-safety-and-security/index|security and threat modeling]] · [[ai/mlops/model-and-prompt-registry|version registry]]

## Sources

- [Regulation (EU) 2024/1689, official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) — primary legal text; use it for article-level claims.
- [European Commission: AI Act implementation timeline](https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline) — current staged-application timeline.
- [European Commission: AI Act policy page](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) — official overview and implementation material.
- [European Commission: GPAI provider guidelines](https://digital-strategy.ec.europa.eu/en/faqs/guidelines-obligations-general-purpose-ai-providers) — interpretation of GPAI provider obligations.
