"""Disallow broad exception handlers in Python source files.

Flags ``except:``, ``except Exception`` and ``except BaseException`` (also inside
a tuple, or as ``except*``).  Only handlers on *added* lines (via
``git diff --cached``) are checked, so existing handlers are grandfathered in.
Test files are skipped.

A broad handler is allowed when it re-raises (bare ``raise``, ``raise e`` or
``raise ... from e``), or when the ``except`` line carries
``# noqa: BLE001 - <reason>``.  An opt-out without a reason is still flagged.
"""

import argparse
import ast
import re
import subprocess
import warnings
from typing import Optional, Sequence

_BROAD_NAMES = frozenset({"Exception", "BaseException"})

_HUNK_RE = re.compile(r"\+(\d+)(?:,(\d+))?")

_NOQA_RE = re.compile(
    r"#\s*noqa:(?:\s*[A-Z]+[0-9]+\s*,)*\s*BLE001\b(?:\s*,\s*[A-Z]+[0-9]+\b)*(?P<reason>.*)",
)

_REASON_PUNCTUATION = " \t-–—:"

_BROAD = "broad exception handler"
_MISSING_REASON = "`# noqa: BLE001` needs a reason, e.g. `# noqa: BLE001 - <why>`"


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


def _is_caught_name(node: Optional[ast.expr], name: Optional[str]) -> bool:
    return name is not None and isinstance(node, ast.Name) and node.id == name


def _walk_skipping_scopes(nodes: list[ast.stmt]):
    stack: list[ast.AST] = list(nodes)
    while stack:
        node = stack.pop()
        yield node
        if not isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef),
        ):
            stack.extend(ast.iter_child_nodes(node))


def _reraises(handler: ast.ExceptHandler) -> bool:
    return any(
        isinstance(node, ast.Raise)
        and (
            node.exc is None
            or _is_caught_name(node.exc, handler.name)
            or _is_caught_name(node.cause, handler.name)
        )
        for node in _walk_skipping_scopes(handler.body)
    )


def _opt_out_problem(line: str) -> Optional[str]:
    """Return ``""`` for a valid opt-out, an error for one without a reason, else ``None``."""
    match = _NOQA_RE.search(line)
    if not match:
        return None
    return "" if match.group("reason").strip(_REASON_PUNCTUATION) else _MISSING_REASON


def find_broad_handlers(source: str, added_lines: set[int]) -> list[tuple[int, str]]:
    """Return ``(line_number, problem)`` for disallowed broad handlers on added lines."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(source)
    except SyntaxError:
        return []
    lines = source.splitlines()
    findings: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if (
            not isinstance(node, ast.ExceptHandler)
            or node.lineno not in added_lines
            or not _is_broad(node.type)
            or _reraises(node)
        ):
            continue
        opt_out = _opt_out_problem(lines[node.lineno - 1])
        if opt_out is None:
            findings.append((node.lineno, _BROAD))
        elif opt_out:
            findings.append((node.lineno, opt_out))
    return sorted(findings)


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
        for lineno, problem in find_broad_handlers(
            _git("show", f":{filepath}"),
            added,
        ):
            errors.append(f"  {filepath}:{lineno}: {problem}")

    if errors:
        print(  # noqa: T201
            "Broad exception handlers (bare `except:`, `except Exception`, "
            "`except BaseException`) in staged changes:\n",
        )
        print("\n".join(errors))  # noqa: T201
        print(  # noqa: T201
            "\nCatch only the specific exceptions you expect, e.g. `except TimeoutError:`."
            "\nA broad handler is allowed if it re-raises, or with"
            " `# noqa: BLE001 - <reason>` on the `except` line.",
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
