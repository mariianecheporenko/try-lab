"""Visitor-based evaluator for SIPL programs."""

from __future__ import annotations

from typing import Any

try:  # Support both ``import interpreter`` and ``import src.interpreter``.
    from .ast_nodes import (
        Arithmetic,
        BooleanNot,
        BooleanOr,
        Compare,
        Program,
        Assign,
        Seq,
        If,
        While,
        Skip,
        Number,
        Variable,
        Node,
    )
except ImportError:
    from ast_nodes import (
        Arithmetic,
        BooleanNot,
        BooleanOr,
        Compare,
        Program,
        Assign,
        Seq,
        If,
        While,
        Skip,
        Number,
        Variable,
        Node,
    )


class Interpreter:
    """Execute SIPL AST nodes with a single mutable variable environment."""

    def __init__(self, *, trace: bool = True) -> None:
        self.state: dict[str, int] = {}
        self.trace = trace

    def _trace(self, event: str) -> None:
        if self.trace:
            print({"event": event, "state": self.state.copy()})

    def visit(self, node: Node) -> Any:
        return node.accept(self)

    def execute(self, program: Program) -> dict[str, int]:
        self.visit(program)
        return self.state

    def visit_program(self, node: Program) -> None:
        self.visit(node.body)

    def visit_assign(self, node: Assign) -> None:
        self._trace("assign")
        self.state[node.name] = self.visit(node.expression)

    def visit_seq(self, node: Seq) -> None:
        self._trace("sequence")
        self.visit(node.first)
        self.visit(node.second)

    def visit_if(self, node: If) -> None:
        self._trace("if")
        branch = node.then_branch if self.visit(node.condition) else node.else_branch
        self.visit(branch)

    def visit_while(self, node: While) -> None:
        self._trace("while")
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_skip(self, _node: Skip) -> None:
        self._trace("skip")

    def visit_number(self, node: Number) -> int:
        return node.value

    def visit_variable(self, node: Variable) -> int:
        try:
            return self.state[node.name]
        except KeyError as exc:
            raise NameError(f"SIPL variable {node.name!r} has not been assigned") from exc

    def visit_arithmetic(self, node: Arithmetic) -> int:
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.operator == "+":
            return left + right
        if node.operator == "-":
            return left - right
        if node.operator == "*":
            return left * right
        raise ValueError(f"Unknown arithmetic operator: {node.operator}")

    def visit_compare(self, node: Compare) -> bool:
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.operator == "=":
            return left == right
        if node.operator == ">":
            return left > right
        raise ValueError(f"Unknown comparison operator: {node.operator}")

    def visit_boolean_or(self, node: BooleanOr) -> bool:
        return self.visit(node.left) or self.visit(node.right)

    def visit_boolean_not(self, node: BooleanNot) -> bool:
        return not self.visit(node.operand)


def interpret(program: Program, *, trace: bool = True) -> dict[str, int]:
    """Execute a program using a new interpreter and return its final state."""
    return Interpreter(trace=trace).execute(program)
