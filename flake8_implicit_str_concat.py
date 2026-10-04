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

# Trivia token types ignored when looking for the adjacent significant token
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

# f-strings (Python 3.12+) and t-strings (Python 3.14+) tokenize as
# START...END token groups rather than single STRING tokens
_STRING_START_TYPES = frozenset(
    getattr(tokenize, name)
    for name in ("FSTRING_START", "TSTRING_START")
    if hasattr(tokenize, name)
)
_STRING_END_TYPES = frozenset(
    getattr(tokenize, name)
    for name in ("FSTRING_END", "TSTRING_END")
    if hasattr(tokenize, name)
)

# ast.TemplateStr is t-strings, Python 3.14+
_JOINED_STR_TYPES = (ast.JoinedStr, getattr(ast, "TemplateStr", ast.JoinedStr))


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
    chains = _concat_chains(file_tokens)
    if not chains:
        return

    # ast reports column offsets in bytes but tokenize in characters, so key
    # each chain by the (row, byte column) where its first token starts
    chain_starts = {}
    for chain in chains:
        token = file_tokens[chain[0][0]]
        row, col = token.start
        byte_col = len(token.line[:col].encode("utf-8"))
        chain_starts[(row, byte_col)] = chain

    for node in ast.walk(root_node):
        if not isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            continue

        for elt in node.elts:
            # Only flag direct string constants or f-strings, not nested structures
            if not _is_string_node(elt):
                continue

            # Python's ast collapses implicitly concatenated strings into a
            # single node, so a chain starting exactly where the element
            # starts is the element's own implicit concatenation
            elt_chain = chain_starts.get((elt.lineno, elt.col_offset))
            if elt_chain is None:
                continue

            if _is_parenthesized(elt_chain[0][0], elt_chain[-1][1], file_tokens):
                continue

            first_string_end = file_tokens[elt_chain[0][1]].end
            yield (
                *first_string_end,
                (
                    "ISC004 unparenthesized implicit string concatenation "
                    "in collection (missing comma?)"
                ),
                None,
            )


def _string_atoms(
    file_tokens: Sequence[tokenize.TokenInfo],
) -> Iterable[tuple[int, int]]:
    """Yield (first, last) token index ranges of individual string literals.

    A plain string literal is a single STRING token; an f-string or t-string
    spans a whole START...END token group (which may contain STRING tokens
    inside replacement fields that are not implicit concatenation).
    """
    depth = 0
    start = 0
    for i, token in enumerate(file_tokens):
        if token.type in _STRING_START_TYPES:
            if depth == 0:
                start = i
            depth += 1
        elif token.type in _STRING_END_TYPES:
            depth -= 1
            if depth == 0:
                yield start, i
        elif depth == 0 and token.type == tokenize.STRING:
            yield i, i


def _concat_chains(
    file_tokens: Sequence[tokenize.TokenInfo],
) -> list[list[tuple[int, int]]]:
    """Group adjacent string literals into implicit concatenation chains.

    Two literals are adjacent when only trivia tokens separate them. Returns
    only chains of two or more literals.
    """
    chains = []
    chain: list[tuple[int, int]] = []
    for first, last in _string_atoms(file_tokens):
        if chain and all(
            file_tokens[i].type in _SKIP_TOKEN_TYPES
            for i in range(chain[-1][1] + 1, first)
        ):
            chain.append((first, last))
        else:
            if len(chain) > 1:
                chains.append(chain)
            chain = [(first, last)]
    if len(chain) > 1:
        chains.append(chain)
    return chains


def _is_string_node(node: ast.expr) -> bool:
    """Check if an AST node is a string constant, f-string or t-string."""
    return isinstance(node, _JOINED_STR_TYPES) or (
        isinstance(node, ast.Constant) and isinstance(node.value, (str, bytes))
    )


def _next_significant(
    file_tokens: Sequence[tokenize.TokenInfo],
    indices: Iterable[int],
) -> tokenize.TokenInfo | None:
    """Return the first non-trivia token at the given indices, if any."""
    for i in indices:
        if file_tokens[i].type not in _SKIP_TOKEN_TYPES:
            return file_tokens[i]
    return None


def _is_parenthesized(
    first_idx: int,
    last_idx: int,
    file_tokens: Sequence[tokenize.TokenInfo],
) -> bool:
    """Check if a string concatenation is directly wrapped in parentheses."""
    before = _next_significant(file_tokens, range(first_idx - 1, -1, -1))
    after = _next_significant(file_tokens, range(last_idx + 1, len(file_tokens)))
    return (
        before is not None
        and before.exact_type == tokenize.LPAR
        and after is not None
        and after.exact_type == tokenize.RPAR
    )


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
