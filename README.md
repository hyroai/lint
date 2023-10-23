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

## Adding a new hook to hyro-hooks

The steps to add a new hook to the hyro-hooks:
1. create the hook script file under lint folder
2. add a test file to make sure your script is working
3. add your hook to `setup.py` under "console_scripts", like in this example where `format-csv` is the hook id and `lint.format_csv:main` is the route to the script:
    ```python
    "console_scripts": [
        "format-csv=lint.format_csv:main",
    ]
    ```
4. add your hook id and the files that will be formatted to the lint repo hooks under `hyro-hooks.yaml`:
    ```yaml
    repo: https://github.com/hyroai/lint
    rev: 7dbcd130e0c22c8f08292d8527826cf08b756e56
    hooks:
      - id: format-csv
        files: triplets.csv
    ```
5. after you merge your changes into master update the commit hash in `hyro-hooks.yaml` from the previous step to be the latest one in master
6. after that update is merged you can update the latest commit hash in all repos that use the hyro-hooks