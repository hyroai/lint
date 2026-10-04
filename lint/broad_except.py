"""Disallow broad exception handlers in Python source files.

Flags ``except:``, ``except Exception`` and ``except BaseException`` (also inside
a tuple, or as ``except*``).  Only handlers on *added* lines (via
``git diff --cached``) are checked, so existing handlers are grandfathered in.
Test files are skipped.
"""

import argparse
import ast
import re
import subprocess
import warnings
from typing import Optional, Sequence

_BROAD_NAMES = frozenset({"Exception", "BaseException"})

_HUNK_RE = re.compile(r"\+(\d+)(?:,(\d+))?")


def _is_broad(node: Optional[ast.expr]) -> bool:
    if node is None:
        return True
    if isinstance(node, ast.Name):
        return node.id in _BROAD_NAMES
    if isinstance(node, ast.Attribute):
        return node.attr in _BROAD_NAMES
    if isinstance(node, ast.Tuple):
        return any(map(_is_broad, node.elts))
    return False


def find_broad_handlers(source: str, added_lines: set[int]) -> list[int]:
    """Return line numbers of broad ``except`` clauses that sit on added lines."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(source)
    except SyntaxError:
        return []
    return sorted(
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.ExceptHandler)
        and node.lineno in added_lines
        and _is_broad(node.type)
    )


def _git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except subprocess.CalledProcessError, FileNotFoundError:
        return ""


def _added_line_numbers(filepath: str) -> set[int]:
    added: set[int] = set()
    for diff_line in _git("diff", "--cached", "-U0", "--", filepath).splitlines():
        if diff_line.startswith("@@"):
            match = _HUNK_RE.search(diff_line)
            if match:
                start = int(match.group(1))
                count = int(match.group(2) or 1)
                added.update(range(start, start + count))
    return added


def _is_test_file(filepath: str) -> bool:
    return filepath.endswith("_test.py")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Disallow broad exception handlers in staged Python changes.",
    )
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    errors: list[str] = []

    for filepath in args.filenames:
        if _is_test_file(filepath):
            continue
        added = _added_line_numbers(filepath)
        if not added:
            continue
        for lineno in find_broad_handlers(_git("show", f":{filepath}"), added):
            errors.append(f"  {filepath}:{lineno}")

    if errors:
        print(  # noqa: T201
            "Broad exception handlers (bare `except:`, `except Exception`, "
            "`except BaseException`) in staged changes:\n",
        )
        print("\n".join(errors))  # noqa: T201
        print(  # noqa: T201
            "\nCatch only the specific exceptions you expect, e.g. `except TimeoutError:`.",
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
