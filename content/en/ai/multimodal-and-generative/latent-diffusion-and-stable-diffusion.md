---
title: "Latent diffusion and Stable Diffusion"
description: Latent diffusion runs denoising in a compressed representation, making high-resolution image generation cheaper than pixel-space diffusion.
tags: [diffusion, latent-space, stable-diffusion]
order: 3
updated: 2026-06-07
---
# Latent diffusion and Stable Diffusion

Latent diffusion moves the diffusion process from pixel space into a compressed latent
space. Stable Diffusion popularized this design because it makes high-quality
text-to-image generation much cheaper.

## Why latent space helps

Pixel images are large. A 1024 x 1024 RGB image has millions of values, and denoising
that directly is expensive. A variational autoencoder compresses the image into a
smaller latent grid, the diffusion model denoises there, and the decoder maps the final
latent back to pixels.

## Core pipeline

| Part | Role |
|---|---|
| Text encoder | turns prompt text into conditioning vectors |
| VAE encoder | compresses images into latent space during training |
| U-Net or transformer denoiser | predicts noise in latent space |
| Sampler | steps from noise toward a clean latent |
| VAE decoder | converts final latent into an image |

## What Stable Diffusion made practical

- Running text-to-image models on consumer GPUs.
- Fine-tuning style, subject, or product concepts with adapters.
- Image-to-image workflows that preserve composition.
- Inpainting and outpainting with masks.
- Open ecosystem tooling around checkpoints, LoRAs, ControlNet, and Diffusers.

## Pitfall

Latent compression is lossy. Fine details, text rendering, hands, small objects, and
precise spatial relationships can degrade because the model never denoises full pixels
directly.

**Connects to:** [[ai/deep-learning/embeddings-and-latent-spaces|latent spaces]] ·
[[ai/multimodal-and-generative/text-to-image-conditioning-and-cfg|conditioning and CFG]] ·
[[ai/fine-tuning-and-alignment/lora-and-adapters|LoRA adapters]]
