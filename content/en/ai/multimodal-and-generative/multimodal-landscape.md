---
title: "The multimodal landscape"
description: Multimodal AI connects text, image, audio, video, documents, sensors, and actions through shared representations and generative models.
tags: [multimodal, generative, representations]
order: 1
updated: 2026-06-07
---
# The multimodal landscape

Multimodal AI is about models that understand or generate more than text. The central
problem is aligning signals with different structures: pixels, waveforms, tokens,
frames, layouts, sensor streams, and actions.

## Modalities and tasks

| Modality | Understanding tasks | Generative tasks |
|---|---|---|
| Image | classification, detection, OCR, captioning | text-to-image, editing, inpainting |
| Audio | speech recognition, speaker ID | TTS, voice conversion, music |
| Video | action recognition, tracking, temporal QA | video synthesis, editing, interpolation |
| Document | layout parsing, table extraction | report generation, visual QA |
| 3D/action | scene understanding, robotics | object generation, planning, control |

## Two big patterns

- **Shared embedding spaces** align modalities so text and images can be compared,
searched, and conditioned together.
- **Generative models** learn to produce media from noise, latent variables, prompts,
or other modalities.

Modern systems often combine both: a text encoder guides an image or video generator,
then another multimodal model evaluates or edits the result.

## Why it is harder than text

- Inputs are larger and more expensive to process.
- Quality is more subjective and multi-dimensional.
- Evaluation needs human judgment, perceptual metrics, and safety review.
- Outputs can create direct social risk through impersonation, misinformation, and provenance loss.

## Pitfall

Do not assume text-era product patterns transfer cleanly. Media generation needs
controls for ownership, consent, safety, provenance, and visual quality that text-only
systems often postpone.

**Connects to:** [[ai/deep-learning/embeddings-and-latent-spaces|latent spaces]] ·
[[ai/multimodal-and-generative/clip-and-shared-embedding-spaces|CLIP]] ·
[[ai/ai-ethics-and-governance/index|AI ethics and governance]]
