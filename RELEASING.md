# Release Checklist

- [ ] Check tests pass on
      [GitHub Actions](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/actions)
      [![GitHub Actions status](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/actions/workflows/main.yml/badge.svg)](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/actions/workflows/main.yml)

- [ ] Go to the
      [Releases page](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/releases)
      and

  - [ ] Click "Draft a new release"

  - [ ] Click "Choose a tag"

  - [ ] Type the next `X.Y.Z` version and select "**Create new tag: X.Y.Z** on publish"

  - [ ] Leave the "Release title" blank (it will be autofilled)

  - [ ] Click "Generate release notes" and amend as required

  - [ ] Click "Publish release"

- [ ] Check the tagged
      [GitHub Actions build](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat/actions/workflows/release.yml)
      has deployed to
      [PyPI](https://pypi.org/project/flake8-implicit-str-concat/#history)

- [ ] Check installation:

  ```bash
  python -m pip uninstall -y  flake8-implicit-str-concat \
  && python -m pip install -U flake8-implicit-str-concat \
  && flake8 --version | grep  flake8-implicit-str-concat
  ```
