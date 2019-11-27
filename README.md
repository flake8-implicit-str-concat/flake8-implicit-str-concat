# flake8-implicit-str-concat

[![PyPI version](https://img.shields.io/pypi/v/flake8-implicit-str-concat.svg)](https://pypi.org/project/flake8-implicit-str-concat)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/flake8-implicit-str-concat.svg)](https://pypi.org/project/flake8-implicit-str-concat)
[![PyPI downloads](https://img.shields.io/pypi/dm/flake8-implicit-str-concat.svg)](https://pypistats.org/packages/flake8-implicit-str-concat)
[![GitHub](https://img.shields.io/github/license/keisheiled/flake8-implicit-str-concat.svg)](LICENSE)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Forbid implicitly concatenated string literals on one line such as those
introduced by [Black](https://github.com/psf/black/issues/26).

## Install

```
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
example.py:1:28: implicit-str-concat implicitly concatenated string literals on one line
$ edit example.py # Remove the " " and save
$ cat example.py
s = "111111111111111111111222222222222222222222"
$ black example.py
All done! ✨ 🍰 ✨
1 file left unchanged.
$ flake8 example.py
$
```
