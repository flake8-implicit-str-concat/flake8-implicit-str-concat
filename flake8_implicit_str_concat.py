"""
Flake8 plugin to encourage correct string literal concatenation.

Forbid implicitly concatenated string literals on one line such as those
introduced by Black.
Forbid all explicitly concatenated strings, in favour of implicit concatenation.
"""

from __future__ import annotations

import ast
import tokenize
from dataclasses import dataclass
from itertools import pairwise

TYPE_CHECKING = False

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

__all__ = ["Checker", "__version__"]
__version__ = "0.4.0"

_ERROR = tuple[int, int, str, None]

# Token types to skip when checking for consecutive strings
_SKIP_TOKEN_TYPES = frozenset(
    {
        tokenize.NL,
        tokenize.NEWLINE,
        tokenize.INDENT,
        tokenize.DEDENT,
        tokenize.COMMENT,
        tokenize.ENCODING,
        tokenize.ENDMARKER,
    }
)

# Significant token types that break implicit concatenation
_SIGNIFICANT_TOKEN_TYPES = frozenset(
    {
        tokenize.NAME,
        tokenize.NUMBER,
        tokenize.STRING,
    }
)


def _implicit(file_tokens: Iterable[tokenize.TokenInfo]) -> Iterable[_ERROR]:
    return (
        (
            *a.end,
            (
                "ISC001 implicitly concatenated string literals on one line"
                if a.end[0] == b.start[0]
                else (
                    "ISC002 implicitly concatenated string literals "
                    "over continuation line"
                )
            ),
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
        and all(_is_string_node(operand) for operand in [node.left, node.right])
    )


def _in_collection(
    root_node: ast.AST,
    file_tokens: Sequence[tokenize.TokenInfo],
) -> Iterable[_ERROR]:
    """Detect unparenthesized implicit string concatenation in collections (ISC004)."""
    # Pre-build token index for O(1) lookups
    token_index = {id(t): i for i, t in enumerate(file_tokens)}

    # Get STRING tokens with their indices
    string_tokens = [
        (t, token_index[id(t)]) for t in file_tokens if t.type == tokenize.STRING
    ]
    if len(string_tokens) < 2:
        return

    # Find all implicit string concatenations (consecutive STRING tokens in token
    # order). These may have NL/NEWLINE/COMMENT tokens between them but no other
    # significant tokens.
    implicit_concats = []
    for (a, a_idx), (b, b_idx) in pairwise(string_tokens):
        if _are_consecutive_strings(a_idx, b_idx, file_tokens):
            implicit_concats.append((a, b, a_idx, b_idx))

    if not implicit_concats:
        return

    # Find all collections and check if any implicit concat is inside them
    for node in ast.walk(root_node):
        if not isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            continue

        for elt in node.elts:
            # Only flag direct string constants or f-strings, not nested structures
            if not _is_string_node(elt):
                continue

            # Check if any implicit concat falls within this element
            for a, b, a_idx, b_idx in implicit_concats:
                if not _token_in_node(a, elt):
                    continue

                # Check if the concatenation is parenthesized
                if _is_parenthesized(a_idx, b_idx, file_tokens):
                    continue

                yield (
                    a.end[0],
                    a.end[1],
                    (
                        "ISC004 unparenthesized implicit string concatenation "
                        "in collection (missing comma?)"
                    ),
                    None,
                )


def _is_string_node(node: ast.expr) -> bool:
    """Check if an AST node is a string constant or f-string."""
    return isinstance(node, ast.JoinedStr) or (
        isinstance(node, ast.Constant) and isinstance(node.value, (str, bytes))
    )


def _token_in_node(token: tokenize.TokenInfo, node: ast.expr) -> bool:
    """Check if a token falls within an AST node's range."""
    if not hasattr(node, "end_lineno") or not hasattr(node, "end_col_offset"):
        return False

    start = (node.lineno, node.col_offset)
    end = (node.end_lineno, node.end_col_offset)
    return start <= token.start and token.end <= end


def _are_consecutive_strings(
    a_idx: int,
    b_idx: int,
    file_tokens: Sequence[tokenize.TokenInfo],
) -> bool:
    """Check if two STRING tokens are consecutive (no significant tokens between)."""
    for i in range(a_idx + 1, b_idx):
        if file_tokens[i].type not in _SKIP_TOKEN_TYPES:
            return False
    return True


def _is_parenthesized(
    first_idx: int,
    last_idx: int,
    file_tokens: Sequence[tokenize.TokenInfo],
) -> bool:
    """Check if a string concatenation is wrapped in parentheses."""
    # Look backwards from first string for left parenthesis
    paren_depth = 0
    found_lparen = False
    for i in range(first_idx - 1, -1, -1):
        t = file_tokens[i]
        if t.type == tokenize.OP:
            if t.string == ")":
                paren_depth += 1
            elif t.string == "(":
                if paren_depth > 0:
                    paren_depth -= 1
                else:
                    found_lparen = True
                    break
            elif t.string == ",":
                # Hit a comma before finding opening paren - not parenthesized
                return False
        elif t.type in _SIGNIFICANT_TOKEN_TYPES:
            # Hit another significant token - not parenthesized
            return False

    if not found_lparen:
        return False

    # Look forwards from last string for right parenthesis
    paren_depth = 0
    for i in range(last_idx + 1, len(file_tokens)):
        t = file_tokens[i]
        if t.type == tokenize.OP:
            if t.string == "(":
                paren_depth += 1
            elif t.string == ")":
                if paren_depth > 0:
                    paren_depth -= 1
                else:
                    return True
            elif t.string == ",":
                # Hit a comma before finding closing paren - not parenthesized
                return False
        elif t.type in _SIGNIFICANT_TOKEN_TYPES:
            # Hit another significant token - not parenthesized
            return False

    return False


@dataclass(frozen=True)
class Checker:
    name = __name__
    version = __version__
    tree: ast.AST
    file_tokens: list[tokenize.TokenInfo]

    def run(self) -> Iterable[_ERROR]:
        yield from _implicit(self.file_tokens)
        yield from _explicit(self.tree)
        yield from _in_collection(self.tree, self.file_tokens)
