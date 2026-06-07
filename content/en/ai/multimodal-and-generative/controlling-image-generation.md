---
title: "Controlling image generation"
description: Image generation becomes production-usable when prompts are combined with structural controls such as masks, poses, depth, edges, references, and adapters.
tags: [image-generation, controlnet, inpainting, adapters]
order: 8
updated: 2026-06-07
---
# Controlling image generation

Text prompts are expressive but imprecise. Production image workflows usually add
structural controls so the model respects layout, pose, identity, style, masks, or
brand constraints.

## Control channels

| Control | Use |
|---|---|
| Inpainting | edit a masked region while preserving the rest |
| Image-to-image | transform an existing image while keeping composition |
| ControlNet | condition on edge maps, depth, pose, segmentation, or sketches |
| LoRA/adapters | specialize style, subject, product, or domain |
| Reference image | preserve identity, style, or composition |
| Negative prompt | discourage known artifacts or unwanted content |

## Workflow pattern

1. Define what must stay fixed: layout, subject, style, brand, or object geometry.
2. Choose the control signal that represents that constraint.
3. Generate multiple candidates with fixed seed or controlled variation.
4. Evaluate prompt adherence, visual quality, artifacts, safety, and rights.
5. Keep provenance metadata for source images, adapters, prompts, and edits.

## Production concerns

- Consent for likeness, style, and source images.
- Consistency across a campaign or product catalog.
- Safety review for generated people, minors, logos, and protected attributes.
- Asset lineage when generated output enters a design workflow.

## Pitfall

More control can reduce creative variation. Treat controls as constraints you add
because the product needs them, not because every slider should be maxed out.

**Connects to:** [[ai/fine-tuning-and-alignment/lora-and-adapters|LoRA and adapters]] ·
[[ai/multimodal-and-generative/text-to-image-conditioning-and-cfg|conditioning and CFG]] ·
[[ai/data-for-ai/datasheets-and-data-documentation|data documentation]]
