# Release Checklist

- [ ] Get `main` to the appropriate code release state.
      [GitHub Actions](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/actions)
      should be running cleanly for all merges to `main`.
      [![GitHub Actions status](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/workflows/Test/badge.svg)](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/actions)

* [ ] Start from a freshly cloned repo and bump version number:

```sh
cd /tmp
rm -rf flake8-implicit-str-concat
git clone https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat
cd flake8-implicit-str-concat
edit flake8_implicit_str_concat.py
```

- [ ] Commit and push:

```sh
git add flake8_implicit_str_concat.py
git commit -m "bump version"
git push
```

- [ ] (Optional) Create a distribution and release on **TestPyPI**:

```sh
python -m pip install -U pip build keyring twine
rm -rf build dist
python -m build
python -m twine check --strict dist/* && python -m twine upload --repository testpypi dist/*
```

- [ ] (Optional) Check **test** installation:

```sh
python -m pip uninstall -y flake8-implicit-str-concat
python -m pip install -U -i https://test.pypi.org/simple/ flake8-implicit-str-concat --extra-index-url https://pypi.org/simple --pre
python -m flake8 --version
```

- [ ] Create a distribution and release on **live PyPI**:

```sh
python -m pip install -U pip build keyring twine
rm -rf build dist
python -m build
python -m twine check --strict dist/* && python -m twine upload -r pypi dist/*
```

- [ ] Check installation:

```sh
python -m pip uninstall -y flake8-implicit-str-concat
python -m pip install -U flake8-implicit-str-concat
python -m flake8 --version
```

- [ ] Draft a new release:
      https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/releases/new

- [ ] "Choose a tag" > enter new version (e.g. "0.4.0") > "Create new tag"
- [ ] Leave "Release title" empty
- [ ] Click "Generate release notes" and amend if needed
- [ ] Publish release
