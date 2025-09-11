# flake8-implicit-str-concat

[![PyPI version](https://img.shields.io/pypi/v/flake8-implicit-str-concat.svg)](https://pypi.org/project/flake8-implicit-str-concat)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/flake8-implicit-str-concat.svg)](https://pypi.org/project/flake8-implicit-str-concat)
[![PyPI downloads](https://img.shields.io/pypi/dm/flake8-implicit-str-concat.svg)](https://pypistats.org/packages/flake8-implicit-str-concat)
[![GitHub Actions status](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/workflows/Test/badge.svg)](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/actions)
[![Codecov](https://codecov.io/gh/flake8-implicit-str-concat/flake8-implicit-str-concat/branch/main/graph/badge.svg)](https://codecov.io/gh/flake8-implicit-str-concat/flake8-implicit-str-concat)
[![Licence](https://img.shields.io/github/license/flake8-implicit-str-concat/flake8-implicit-str-concat.svg)](LICENSE)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)
[![Tidelift](https://tidelift.com/badges/package/pypi/flake8-implicit-str-concat)](https://tidelift.com/subscription/pkg/pypi-flake8-implicit-str-concat?utm_source=pypi-flake8-implicit-str-concat&utm_medium=referral&utm_campaign=readme)

This is a plugin for the Python code-checking tool [Flake8](https://flake8.pycqa.org/)
to encourage correct string literal concatenation.

It looks for style problems like implicitly concatenated string literals on the same
line (which can be introduced by the code-formatting tool
[Black](https://github.com/psf/black/issues/26)), or unnecessary plus operators for
explicit string literal concatenation.

## Install

```sh
pip install flake8-implicit-str-concat
```

## Example

```console
$ cat example.py
s = ('111111111111111111111'
     '222222222222222222222')
$ black example.py
reformatted example.py
All done! ✨ 🍰 ✨
1 file reformatted.
$ cat example.py
s = "111111111111111111111" "222222222222222222222"
$ flake8 example.py
example.py:1:28: ISC001 implicitly concatenated string literals on one line
$ edit example.py # Remove the " " and save
$ cat example.py
s = "111111111111111111111222222222222222222222"
$ black example.py
All done! ✨ 🍰 ✨
1 file left unchanged.
$ flake8 example.py
$
```

## Violation codes

The plugin uses the prefix `ISC`, short for Implicit String Concatenation.

| Code   | Description                                                      |
| ------ | ---------------------------------------------------------------- |
| ISC001 | implicitly concatenated string literals on one line              |
| ISC002 | implicitly concatenated string literals over continuation line   |
| ISC003 | explicitly concatenated string should be implicitly concatenated |

## Release notes

You can find the release notes on the
[releases page](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/releases).
