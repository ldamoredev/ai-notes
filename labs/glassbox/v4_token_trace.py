#!/usr/bin/env python3
"""Glassbox v4 experiment: expose every stage from text to one generated token."""
from __future__ import annotations

import random

from .v0_math import sample_categorical, stable_softmax

VOCABULARY = [" ", "a", "b", "c"]
TOKEN_TO_ID = {token: index for index, token in enumerate(VOCABULARY)}
# Rows are logits for the next token conditioned on the current final token.
BIGRAM_LOGITS = [
    [-1.0, 2.0, 0.5, 0.0],
    [-0.5, 0.2, 2.2, 0.0],
    [-0.2, 0.0, 0.3, 2.4],
    [1.8, 0.6, -0.2, 0.1],
]


def encode(text: str) -> list[int]:
    try:
        return [TOKEN_TO_ID[character] for character in text]
    except KeyError as error:
        raise ValueError(f"character outside tiny vocabulary: {error.args[0]!r}") from error


def decode(token_ids: list[int]) -> str:
    return "".join(VOCABULARY[token_id] for token_id in token_ids)


def generate_one(text: str, temperature: float, seed: int) -> dict[str, object]:
    token_ids = encode(text)
    if not token_ids:
        raise ValueError("prompt must contain at least one token")
    logits = BIGRAM_LOGITS[token_ids[-1]]
    probabilities = stable_softmax(logits, temperature)
    selected_id = sample_categorical(probabilities, random.Random(seed))
    return {
        "text": text,
        "token_ids": token_ids,
        "last_token": token_ids[-1],
        "logits": logits,
        "temperature": temperature,
        "probabilities": probabilities,
        "selected_id": selected_id,
        "selected_token": decode([selected_id]),
    }


def main() -> None:
    trace = generate_one("ab", temperature=0.8, seed=7)
    for key, value in trace.items():
        if key == "probabilities":
            value = [round(number, 6) for number in value]  # type: ignore[arg-type]
        print(f"{key}: {value!r}")


if __name__ == "__main__":
    main()
