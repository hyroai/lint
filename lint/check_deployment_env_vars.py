"""Check that newly added env vars in Helm deployment templates are either
present in all other deployments or documented in an exceptions file.

Only inspects added lines in the staged diff (``git diff --cached``), so
existing per-service differences are grandfathered in.

The exceptions file (``deploy/env-var-exceptions.json``) in the consuming repo
documents vars that are intentionally absent from certain deployments:

    {
      "WIDGET_SERVER_SMS_ADDRESS": {
        "bot-archive": "transitive import only, not used by this service"
      }
    }
"""

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Optional, Sequence

import gamla

_ENV_VAR_RE = re.compile(r"^\s*-\s*name:\s*([A-Z][A-Z0-9_]+)\s*$")
_EXCEPTIONS_FILE = "deploy/env-var-exceptions.json"
_DEPLOYMENT_RE = re.compile(r"deploy/[^/]+/templates/deployment\.yaml$")

_vars_from_added_diff_lines = gamla.compose_left(
    str.splitlines,
    gamla.filter(lambda line: line.startswith("+") and not line.startswith("+++")),
    gamla.map(lambda line: line[1:]),
    gamla.filter(_ENV_VAR_RE.match),
    gamla.map(gamla.compose_left(_ENV_VAR_RE.match, lambda match: match.group(1))),
    frozenset,
)

_vars_from_content = gamla.compose_left(
    str.splitlines,
    gamla.filter(_ENV_VAR_RE.match),
    gamla.map(gamla.compose_left(_ENV_VAR_RE.match, lambda match: match.group(1))),
    frozenset,
)


def _unexcused_missing(var, source_chart, all_vars_by_chart, exceptions):
    return sorted(
        chart
        for chart, chart_vars in all_vars_by_chart.items()
        if chart != source_chart
        and var not in chart_vars
        and chart not in exceptions.get(var, {})
    )


def _format_error(var, source_chart, missing_charts):
    return (
        f"{var} (added to {source_chart}) is missing from: {', '.join(missing_charts)}\n"
        f"  Add it to those deployments, or document exceptions in {_EXCEPTIONS_FILE}:\n"
        f'    "{var}": {{\n'
        + "".join(
            f'      "{chart}": "reason why not needed here",\n' for chart in missing_charts
        )
        + "    }"
    )


def _stale_exceptions(new_vars_by_chart, exceptions):
    return tuple(
        f"{var} is now in {source_chart} but {source_chart} is still listed in {_EXCEPTIONS_FILE} — consider removing it."
        for source_chart, new_vars in new_vars_by_chart.items()
        for var in sorted(new_vars)
        if source_chart in exceptions.get(var, {})
    )


def detect(new_vars_by_chart, all_vars_by_chart, exceptions):
    return tuple(
        _format_error(var, source_chart, missing)
        for source_chart, new_vars in new_vars_by_chart.items()
        for var in sorted(new_vars)
        if (missing := _unexcused_missing(var, source_chart, all_vars_by_chart, exceptions))
    )


def _staged_diff(filepath):
    result = subprocess.run(
        ["git", "diff", "--cached", "-U0", "--", filepath],
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else ""


def _chart_name(deployment_path):
    return Path(deployment_path).parts[1]


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check deployment env var consistency across Helm charts."
    )
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    staged_files = [filepath for filepath in args.filenames if _DEPLOYMENT_RE.search(filepath)]
    if not staged_files:
        return 0

    all_deployments = {
        deployment.parts[1]: _vars_from_content(deployment.read_text())
        for deployment in Path("deploy").glob("*/templates/deployment.yaml")
    }
    if len(all_deployments) < 2:
        return 0

    exceptions_path = Path(_EXCEPTIONS_FILE)
    exceptions = (
        json.loads(exceptions_path.read_text()) if exceptions_path.exists() else {}
    )

    new_vars_by_chart = {
        _chart_name(filepath): _vars_from_added_diff_lines(_staged_diff(filepath))
        for filepath in staged_files
    }

    for warning in _stale_exceptions(new_vars_by_chart, exceptions):
        print(warning)  # noqa: T201

    errors = detect(new_vars_by_chart, all_deployments, exceptions)
    if errors:
        print("Deployment env var consistency check failed:")  # noqa: T201
        for error in errors:
            print(error)  # noqa: T201
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
