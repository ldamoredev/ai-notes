from __future__ import annotations

import math
import random
import unittest

from .v0_math import cross_entropy_from_logits, dot, sample_categorical, stable_softmax
from .v1_autodiff import Value, centered_difference, function
from .v4_attention import causal_attention
from .v4_token_trace import generate_one


class MathTests(unittest.TestCase):
    def test_dot_rejects_shape_mismatch(self) -> None:
        with self.assertRaises(ValueError):
            dot([1.0], [1.0, 2.0])

    def test_stable_softmax_survives_large_logits(self) -> None:
        probabilities = stable_softmax([1000.0, 1001.0, 999.0])
        self.assertTrue(all(math.isfinite(value) for value in probabilities))
        self.assertAlmostEqual(sum(probabilities), 1.0)

    def test_cross_entropy_prefers_target_logit(self) -> None:
        self.assertLess(cross_entropy_from_logits([0.0, 3.0], 1), cross_entropy_from_logits([3.0, 0.0], 1))

    def test_sampling_is_seeded(self) -> None:
        self.assertEqual(sample_categorical([0.2, 0.8], random.Random(7)), 1)


class AutodiffTests(unittest.TestCase):
    def test_gradients_match_centered_difference(self) -> None:
        x = Value(1.5)
        y = Value(-2.0)
        output = (x * y + x**2).tanh()
        output.backward()
        self.assertAlmostEqual(x.grad, centered_difference(lambda candidate: function(candidate, y.data), x.data), places=6)
        self.assertAlmostEqual(y.grad, centered_difference(lambda candidate: function(x.data, candidate), y.data), places=6)

    def test_shared_subexpression_accumulates_gradient(self) -> None:
        x = Value(3.0)
        output = x * x + x
        output.backward()
        self.assertAlmostEqual(x.grad, 7.0)


class AttentionTests(unittest.TestCase):
    def test_causal_mask_and_row_normalization(self) -> None:
        qkv = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
        weights, output = causal_attention(qkv, qkv, qkv)
        self.assertEqual((len(output), len(output[0])), (3, 2))
        for row_index, row in enumerate(weights):
            self.assertAlmostEqual(sum(row), 1.0)
            self.assertTrue(all(row[column] == 0.0 for column in range(row_index + 1, len(row))))


class TokenTraceTests(unittest.TestCase):
    def test_trace_exposes_probability_and_selection(self) -> None:
        trace = generate_one("ab", temperature=0.8, seed=7)
        self.assertEqual(trace["token_ids"], [1, 2])
        self.assertAlmostEqual(sum(trace["probabilities"]), 1.0)  # type: ignore[arg-type]
        self.assertEqual(trace["selected_token"], "c")


if __name__ == "__main__":
    unittest.main()
