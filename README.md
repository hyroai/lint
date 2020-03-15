[![Build Status](https://travis-ci.com/hyroai/lint.svg?branch=master)](https://travis-ci.com/hyroai/lint)

# Lint

Python static analysis linting tools.

## Pre-commit config

```yaml
repos:
  - repo: https://github.com/hyroai/lint
    rev: master
    hooks:
      - id: static-analysis
```
