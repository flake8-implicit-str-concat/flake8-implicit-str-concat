from __future__ import annotations

import ast
import io
import tokenize
from pathlib import Path

import pytest

import flake8_implicit_str_concat as m

FIXTURES_DIR = Path(__file__).parent / "fixtures"

# fmt: off
ISC001 = '''z = "The quick " "brown fox."'''
ISC002 = '''z = "The quick brown fox jumps over the lazy "\\\n"dog."'''
ISC003 = '''z = (
    "The quick brown fox jumps over the lazy "
    + "dog"
)
'''
# fmt: on


def _check(source_code: str) -> list[tuple[int, int, str, None]]:
    """Run the checker on source code and return results."""
    tree = ast.parse(source_code)
    file_tokens = list(
        tokenize.tokenize(
            readline=io.BytesIO(source_code.encode("utf-8")).readline,
        )
    )
    return list(m.Checker(tree, file_tokens).run())


@pytest.mark.parametrize(
    "source_code, expected",
    [
        (ISC001, "ISC001"),
        (ISC002, "ISC002"),
        (ISC003, "ISC003"),
    ],
)
def test_isc(source_code: str, expected: str) -> None:
    results = _check(source_code)
    assert len(results) == 1
    assert expected in results[0][2]


def test_isc004_fixture() -> None:
    """Test ISC004 against the fixture file (identical to Ruff's test fixture)."""
    source_code = (FIXTURES_DIR / "ISC004.py").read_text()
    results = _check(source_code)

    isc004_results = [r for r in results if "ISC004" in r[2]]

    # Should find exactly these violations at these lines
    expected_lines = [4, 11, 18, 30, 36, 42]
    actual_lines = sorted(r[0] for r in isc004_results)

    assert (
        actual_lines == expected_lines
    ), f"Expected ISC004 at lines {expected_lines}, got {actual_lines}"
