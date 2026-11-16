"""Lark parser and parse-tree-to-AST transformer for SIPL."""

from __future__ import annotations

from pathlib import Path

from lark import Lark, Transformer, Tree

try:  # Support both ``import parser`` and ``import src.parser``.
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
        Statement,
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
        Statement,
    )


GRAMMAR_PATH = Path(__file__).resolve().parent.parent / "grammar.lark"


class SIPLTransformer(Transformer):
    """Convert Lark's concrete parse tree into typed SIPL dataclasses."""

    def start(self, items):
        return Program(items[0])

    def sequence(self, items):
        result = items[0]
        for statement in items[1:]:
            result = Seq(result, statement)
        return result

    def assignment(self, items):
        name, expression = items
        return Assign(str(name), expression)

    def if_statement(self, items):
        condition, then_branch, else_branch = items
        return If(condition, then_branch, else_branch)

    def while_statement(self, items):
        condition, body = items
        return While(condition, body)

    def block(self, items):
        return items[0]

    def skip_statement(self, _items):
        return Skip()

    def number(self, items):
        return Number(int(items[0]))

    def variable(self, items):
        return Variable(str(items[0]))

    def add(self, items):
        return Arithmetic("+", items[0], items[1])

    def subtract(self, items):
        return Arithmetic("-", items[0], items[1])

    def multiply(self, items):
        return Arithmetic("*", items[0], items[1])

    def equal(self, items):
        return Compare("=", items[0], items[1])

    def greater(self, items):
        return Compare(">", items[0], items[1])

    def boolean_or_op(self, items):
        return BooleanOr(items[0], items[1])

    def boolean_not(self, items):
        return BooleanNot(items[0])


_parser = Lark.open(
    str(GRAMMAR_PATH),
    parser="earley",
    ambiguity="resolve",
    start="start",
)


def parse_tree(source: str) -> Tree:
    """Return Lark's concrete parse tree for SIPL source."""
    return _parser.parse(source)


def parse(source: str) -> Program:
    """Parse SIPL source and return its :class:`Program` AST."""
    return SIPLTransformer().transform(parse_tree(source))


parse_program = parse
