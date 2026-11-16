"""Command-line tools for running and visualizing SIPL programs."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from lark.tree import pydot__tree_to_png

try:  # Support ``python src/cli.py`` and ``python -m src.cli``.
    from .interpreter import Interpreter
    from .parser import parse, parse_tree
except ImportError:
    from interpreter import Interpreter
    from parser import parse, parse_tree


def _read_source(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Could not read {path}: {exc}") from exc


def run_file(path: Path) -> int:
    program = parse(_read_source(path))
    interpreter = Interpreter()
    final_state = interpreter.execute(program)
    print(f"Final state: {final_state}")
    return 0


def visualize_file(path: Path) -> int:
    source = _read_source(path)
    tree = parse_tree(source)
    program = parse(source)
    image_path = path.with_suffix(".parse_tree.png")
    try:
        pydot__tree_to_png(tree, str(image_path))
    except (ImportError, RuntimeError, OSError) as exc:
        raise SystemExit(f"Could not save parse tree image: {exc}") from exc

    print(f"Parse tree image: {image_path}")
    print(json.dumps(asdict(program), indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run or visualize SIPL programs.")
    commands = parser.add_subparsers(dest="command", required=True)

    run_command = commands.add_parser("run", help="execute a SIPL source file")
    run_command.add_argument("file", type=Path, help="path to a .sipl file")
    run_command.set_defaults(handler=lambda args: run_file(args.file))

    visualize_command = commands.add_parser(
        "visualize", help="save the parse tree image and print the AST JSON"
    )
    visualize_command.add_argument("file", type=Path, help="path to a .sipl file")
    visualize_command.set_defaults(handler=lambda args: visualize_file(args.file))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
