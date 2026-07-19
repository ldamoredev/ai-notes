#!/usr/bin/env python3
"""Glassbox v0: inspectable vector and probability primitives."""
from __future__ import annotations

import math
import random


def dot(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError(f"dot shape mismatch: {len(left)} != {len(right)}")
    return sum(a * b for a, b in zip(left, right))


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    if not matrix or any(len(row) != len(vector) for row in matrix):
        raise ValueError("matvec expects matrix shape [rows, len(vector)]")
    return [dot(row, vector) for row in matrix]


def stable_softmax(logits: list[float], temperature: float = 1.0) -> list[float]:
    if not logits:
        raise ValueError("softmax needs at least one logit")
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    scaled = [value / temperature for value in logits]
    offset = max(scaled)
    exponentials = [math.exp(value - offset) for value in scaled]
    total = sum(exponentials)
    return [value / total for value in exponentials]


def entropy(probabilities: list[float]) -> float:
    if any(value < 0 for value in probabilities) or not math.isclose(sum(probabilities), 1.0, abs_tol=1e-9):
        raise ValueError("entropy expects a probability distribution")
    return -sum(value * math.log(value) for value in probabilities if value > 0)


def cross_entropy_from_logits(logits: list[float], target_index: int) -> float:
    if target_index not in range(len(logits)):
        raise IndexError("target index outside vocabulary")
    probabilities = stable_softmax(logits)
    return -math.log(probabilities[target_index])


def sample_categorical(probabilities: list[float], rng: random.Random) -> int:
    if any(value < 0 for value in probabilities) or not math.isclose(sum(probabilities), 1.0, abs_tol=1e-9):
        raise ValueError("sampling expects normalized probabilities")
    threshold = rng.random()
    cumulative = 0.0
    for index, probability in enumerate(probabilities):
        cumulative += probability
        if threshold < cumulative:
            return index
    return len(probabilities) - 1


def main() -> None:
    vector = [2.0, -1.0]
    matrix = [[1.0, 3.0], [-2.0, 0.5], [0.0, 4.0]]
    logits = matvec(matrix, vector)
    probabilities = stable_softmax(logits)
    print(f"shape: matrix=[3,2], vector=[2], logits=[3]")
    print(f"logits: {[round(value, 4) for value in logits]}")
    print(f"probabilities: {[round(value, 6) for value in probabilities]}")
    print(f"sum(p): {sum(probabilities):.6f}")
    print(f"entropy_nats: {entropy(probabilities):.6f}")
    print(f"cross_entropy(target=2): {cross_entropy_from_logits(logits, 2):.6f}")
    print(f"sample(seed=7): {sample_categorical(probabilities, random.Random(7))}")


if __name__ == "__main__":
    main()
