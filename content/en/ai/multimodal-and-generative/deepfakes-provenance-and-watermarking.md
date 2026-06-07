---
title: "Deepfakes, provenance, and watermarking"
description: Generative media risk includes impersonation, misinformation, consent violations, provenance loss, and weak or removable watermarking.
tags: [deepfakes, provenance, watermarking, safety]
order: 12
updated: 2026-06-07
---
# Deepfakes, provenance, and watermarking

Generative media can create convincing synthetic people, voices, events, and evidence.
The technical question is no longer only "can we generate it?" but also "can people
understand where it came from and whether it is trustworthy?"

## Risk categories

- Impersonation of real people through face, voice, or writing style.
- Non-consensual intimate or harmful imagery.
- Political or crisis misinformation.
- Fraud, social engineering, and fake evidence.
- Brand, copyright, and likeness misuse.
- Erosion of trust in authentic media.

## Provenance and watermarking

| Control | Role | Weakness |
|---|---|---|
| Visible disclosure | tells users content is synthetic | can be cropped or omitted |
| Metadata provenance | records creation and edit history | can be stripped |
| C2PA-style credentials | signed chain of content provenance | adoption and UX depend on ecosystem |
| Watermarking | embeds signal in media | may be removed or degraded |
| Detection model | flags likely synthetic media | arms race and false positives |

## Product mitigations

- Require consent for likeness and voice.
- Label generated or edited media clearly.
- Store prompt, model, source asset, edit, and approval metadata.
- Add human review for high-risk categories.
- Restrict generation of real-person impersonation and sensitive scenarios.
- Provide reporting and takedown workflows.

## Pitfall

Detection is not governance. A detector can help triage, but policy, provenance,
consent, audit trails, and product limits decide whether the system is responsible.

**Connects to:** [[ai/ai-safety-and-security/red-teaming-ai-systems|red teaming]] ·
[[ai/ai-ethics-and-governance/index|AI ethics and governance]] ·
[[ai/ai-product-engineering/product-guardrails|product guardrails]]
