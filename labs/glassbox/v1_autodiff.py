#!/usr/bin/env python3
"""Glassbox v1: scalar reverse-mode automatic differentiation."""
from __future__ import annotations

import math
from collections.abc import Callable


class Value:
    def __init__(self, data: float, children: tuple["Value", ...] = (), operation: str = "", label: str = "") -> None:
        self.data = float(data)
        self.grad = 0.0
        self.children = children
        self.operation = operation
        self.label = label
        self._backward: Callable[[], None] = lambda: None

    def __add__(self, other: "Value | float") -> "Value":
        right = other if isinstance(other, Value) else Value(other)
        output = Value(self.data + right.data, (self, right), "+")

        def backward() -> None:
            self.grad += output.grad
            right.grad += output.grad

        output._backward = backward
        return output

    __radd__ = __add__

    def __mul__(self, other: "Value | float") -> "Value":
        right = other if isinstance(other, Value) else Value(other)
        output = Value(self.data * right.data, (self, right), "*")

        def backward() -> None:
            self.grad += right.data * output.grad
            right.grad += self.data * output.grad

        output._backward = backward
        return output

    __rmul__ = __mul__

    def __pow__(self, exponent: float) -> "Value":
        output = Value(self.data**exponent, (self,), f"**{exponent}")

        def backward() -> None:
            self.grad += exponent * self.data ** (exponent - 1) * output.grad

        output._backward = backward
        return output

    def __neg__(self) -> "Value":
        return self * -1.0

    def __sub__(self, other: "Value | float") -> "Value":
        return self + -other

    def __rsub__(self, other: "Value | float") -> "Value":
        return other + -self

    def tanh(self) -> "Value":
        value = math.tanh(self.data)
        output = Value(value, (self,), "tanh")

        def backward() -> None:
            self.grad += (1.0 - value**2) * output.grad

        output._backward = backward
        return output

    def backward(self) -> None:
        ordered: list[Value] = []
        visited: set[Value] = set()

        def visit(node: Value) -> None:
            if node in visited:
                return
            visited.add(node)
            for child in node.children:
                visit(child)
            ordered.append(node)

        visit(self)
        for node in ordered:
            node.grad = 0.0
        self.grad = 1.0
        for node in reversed(ordered):
            node._backward()

    def __repr__(self) -> str:
        return f"Value(data={self.data:.6f}, grad={self.grad:.6f}, op={self.operation!r})"


def function(x: float, y: float) -> float:
    return math.tanh(x * y + x * x)


def centered_difference(fn: Callable[[float], float], value: float, epsilon: float = 1e-6) -> float:
    return (fn(value + epsilon) - fn(value - epsilon)) / (2.0 * epsilon)


def main() -> None:
    x = Value(1.5, label="x")
    y = Value(-2.0, label="y")
    output = (x * y + x**2).tanh()
    output.backward()
    numeric_x = centered_difference(lambda candidate: function(candidate, y.data), x.data)
    numeric_y = centered_difference(lambda candidate: function(x.data, candidate), y.data)
    print(f"forward: {output.data:.8f}")
    print(f"dx analytical={x.grad:.8f} numerical={numeric_x:.8f}")
    print(f"dy analytical={y.grad:.8f} numerical={numeric_y:.8f}")
    print(f"gradient_check: {math.isclose(x.grad, numeric_x, rel_tol=1e-5, abs_tol=1e-6) and math.isclose(y.grad, numeric_y, rel_tol=1e-5, abs_tol=1e-6)}")


if __name__ == "__main__":
    main()
