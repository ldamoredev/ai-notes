#!/usr/bin/env python3
"""Glassbox v4 experiment: causal scaled dot-product self-attention."""
from __future__ import annotations

import math

from .v0_math import dot, stable_softmax

Matrix = list[list[float]]


def transpose(matrix: Matrix) -> Matrix:
    if not matrix or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("transpose expects a rectangular matrix")
    return [list(column) for column in zip(*matrix)]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    if not left or not right or len(left[0]) != len(right):
        raise ValueError("matmul inner dimensions must match")
    columns = transpose(right)
    return [[dot(row, column) for column in columns] for row in left]


def causal_attention(query: Matrix, key: Matrix, value: Matrix) -> tuple[Matrix, Matrix]:
    if not query or len(query) != len(key) or len(key) != len(value):
        raise ValueError("Q, K, and V need the same sequence length")
    width = len(query[0])
    if width == 0 or any(len(row) != width for row in query + key):
        raise ValueError("Q and K need a shared non-empty d_k")
    scale = math.sqrt(width)
    scores = matmul(query, transpose(key))
    weights: Matrix = []
    for row_index, row in enumerate(scores):
        masked = [score / scale if column <= row_index else -math.inf for column, score in enumerate(row)]
        weights.append(stable_softmax(masked))
    return weights, matmul(weights, value)


def main() -> None:
    query = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    key = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    value = [[1.0, 0.0], [0.0, 2.0], [3.0, 1.0]]
    weights, output = causal_attention(query, key, value)
    print("shapes: Q=K=V=[3,2], scores=[3,3], output=[3,2]")
    for index, row in enumerate(weights):
        print(f"attention[{index}]: {[round(value, 6) for value in row]} sum={sum(row):.6f}")
    for index, row in enumerate(output):
        print(f"output[{index}]: {[round(value, 6) for value in row]}")


if __name__ == "__main__":
    main()
