"""
Forbid implicitly concatenated string literals on one line such as those
introduced by black
"""

from __future__ import generator_stop

import itertools
import tokenize
from typing import Iterable, List, Tuple, TypeVar

import attr

__all__ = ["__version__", "Checker"]
__version__ = "0.0.0.post0"

_ERROR = Tuple[int, int, str, None]

T = TypeVar('T')


def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def _run(file_tokens: Iterable[tokenize.TokenInfo]) -> Iterable[_ERROR]:
    return (
        (
            *a.end,
            "implicit-str-concat implicitly concatenated string literals on one line",
            None,
        )
        for (a, b) in pairwise(file_tokens)
        if a.type == b.type == tokenize.STRING
    )


@attr.s(frozen=True, auto_attribs=True)
class Checker:
    name = __name__
    version = __version__
    tree: object
    file_tokens: List[tokenize.TokenInfo]

    def run(self) -> Iterable[_ERROR]:
        return _run(self.file_tokens)
