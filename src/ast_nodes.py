"""Strongly typed nodes for the SIPL abstract syntax tree."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeAlias


class Visitor(Protocol):
    def visit_program(self, node: Program) -> object: ...
    def visit_assign(self, node: Assign) -> object: ...
    def visit_seq(self, node: Seq) -> object: ...
    def visit_if(self, node: If) -> object: ...
    def visit_while(self, node: While) -> object: ...
    def visit_skip(self, node: Skip) -> object: ...
    def visit_number(self, node: Number) -> object: ...
    def visit_variable(self, node: Variable) -> object: ...
    def visit_arithmetic(self, node: Arithmetic) -> object: ...
    def visit_compare(self, node: Compare) -> object: ...
    def visit_boolean_or(self, node: BooleanOr) -> object: ...
    def visit_boolean_not(self, node: BooleanNot) -> object: ...


class Node:
    def accept(self, visitor: Visitor) -> object:
        names = {
            "BooleanOr": "boolean_or",
            "BooleanNot": "boolean_not",
        }
        method_name = names.get(self.__class__.__name__, self.__class__.__name__.lower())
        method = getattr(visitor, f"visit_{method_name}")
        return method(self)


class Expression(Node):
    pass


class BooleanExpression(Node):
    pass


class Statement(Node):
    pass


@dataclass(frozen=True)
class Program(Node):
    body: Statement


@dataclass(frozen=True)
class Assign(Statement):
    name: str
    expression: Expression


@dataclass(frozen=True)
class Seq(Statement):
    first: Statement
    second: Statement


@dataclass(frozen=True)
class If(Statement):
    condition: BooleanExpression
    then_branch: Statement
    else_branch: Statement


@dataclass(frozen=True)
class While(Statement):
    condition: BooleanExpression
    body: Statement


@dataclass(frozen=True)
class Skip(Statement):
    pass


@dataclass(frozen=True)
class Number(Expression):
    value: int


@dataclass(frozen=True)
class Variable(Expression):
    name: str


@dataclass(frozen=True)
class Arithmetic(Expression):
    operator: str
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Compare(BooleanExpression):
    operator: str
    left: Expression
    right: Expression


@dataclass(frozen=True)
class BooleanOr(BooleanExpression):
    left: BooleanExpression
    right: BooleanExpression


@dataclass(frozen=True)
class BooleanNot(BooleanExpression):
    operand: BooleanExpression


ArithmeticExpression: TypeAlias = Number | Variable | Arithmetic
BooleanExpr: TypeAlias = Compare | BooleanOr | BooleanNot

# Common name used for arithmetic operator nodes in AST examples.
BinOp = Arithmetic
