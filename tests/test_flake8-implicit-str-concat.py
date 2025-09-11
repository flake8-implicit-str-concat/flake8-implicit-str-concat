from __future__ import annotations

import ast
import io
import tokenize

import pytest

import flake8_implicit_str_concat as m

# fmt: off
ISC001 = '''z = "The quick " "brown fox."'''
ISC002 = '''z = "The quick brown fox jumps over the lazy "\\\n"dog."'''
ISC003 = '''z = (
    "The quick brown fox jumps over the lazy "
    + "dog"
)
'''
# fmt: on


@pytest.mark.parametrize(
    "source_code, expected",
    [
        (ISC001, "ISC001"),
        (ISC002, "ISC002"),
        (ISC003, "ISC003"),
    ],
)
def test_isc(source_code: str, expected: str) -> None:
    # Arrange
    tree = ast.parse(source_code)
    file_tokens = list(
        tokenize.tokenize(
            readline=io.BytesIO(
                initial_bytes=source_code.encode("utf-8"),
            ).readline,
        )
    )

    # Act
    results = list(m.Checker(tree, file_tokens).run())

    # Assert
    assert len(results) == 1
    assert expected in results[0][2]
