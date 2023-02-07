"""
Flake8 plugin to encourage correct string literal concatenation.

Forbid implicitly concatenated string literals on one line such as those
introduced by Black.
Forbid all explicitly concatenated strings, in favour of implicit concatenation.
"""

import ast
import sys
import tokenize
from dataclasses import dataclass
from typing import Iterable, List, Tuple

if sys.version_info >= (3, 10):
    from itertools import pairwise
else:
    from more_itertools import pairwise


__all__ = ["__version__", "Checker"]
__version__ = "0.4.0"

_ERROR = Tuple[int, int, str, None]


def _implicit(file_tokens: Iterable[tokenize.TokenInfo]) -> Iterable[_ERROR]:
    return (
        (
            *a.end,
            "ISC001 implicitly concatenated string literals on one line"
            if a.end[0] == b.start[0]
            else "ISC002 implicitly concatenated string literals "
            "over continuation line",
            None,
        )
        for (a, b) in pairwise(file_tokens)
        if a.type == b.type == tokenize.STRING
    )


def _explicit(root_node: ast.AST) -> Iterable[_ERROR]:
    return (
        (
            node.lineno,
            node.col_offset,
            "ISC003 explicitly concatenated string should be implicitly concatenated",
            None,
        )
        for node in ast.walk(root_node)
        if isinstance(node, ast.BinOp)
        and isinstance(node.op, ast.Add)
        and all(
            isinstance(operand, (ast.Str, ast.Bytes, ast.JoinedStr))
            for operand in [node.left, node.right]
        )
    )


@dataclass(frozen=True)
class Checker:
    name = __name__
    version = __version__
    tree: ast.AST
    file_tokens: List[tokenize.TokenInfo]

    def run(self) -> Iterable[_ERROR]:
        yield from _implicit(self.file_tokens)
        yield from _explicit(self.tree)
