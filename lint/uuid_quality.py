"""Detect hand-typed / non-random UUIDs in Python source files.

Only inspects *added* lines (via ``git diff --cached``), so existing UUIDs are
grandfathered in.  Test files are skipped because test fixtures commonly use
placeholder UUIDs on purpose.

Detection
---------
1. UUID version — must be v4, v5, or v7.
2. Interleaved sequential nibbles — catches UUIDs like ``e1d2c3b4-a5f6-…``
   that satisfy v4 format but were clearly typed by hand.
3. Straight sequential nibbles — catches runs like ``0a1b2c3d4e5f``.

A suspicious UUID is allowed when its line carries
``# noqa: UUID001 - <reason>``.  An opt-out without a reason is still flagged.
"""

import argparse
import re
import subprocess
import uuid
from typing import Optional, Sequence

_UUID_RE = re.compile(
    r"""['"]"""
    r"""([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"""
    r"""['"]"""
)

_HUNK_RE = re.compile(r"\+(\d+)")

_NOQA_RE = re.compile(
    r"#\s*noqa:(?:\s*[A-Z]+[0-9]+\s*,)*\s*UUID001\b(?:\s*,\s*[A-Z]+[0-9]+\b)*(?P<reason>.*)",
)

_REASON_PUNCTUATION = " \t-–—:"

_MISSING_REASON = "`# noqa: UUID001` needs a reason, e.g. `# noqa: UUID001 - <why>`"

_ALLOWED_VERSIONS = {4, 5, 7}

_PERMANENT_ALLOWLIST: set[str] = {
    "00000000-0000-0000-0000-000000000000",
}


def _to_nibbles(hex_str: str) -> list[int]:
    return [int(c, 16) for c in hex_str.replace("-", "").lower()]


def _has_sequential_run(
    nibbles: list[int], min_run: int, allowed_steps: set[int]
) -> bool:
    """Detect an arithmetic run of *min_run* nibbles whose step is in *allowed_steps*."""
    for start in range(len(nibbles) - min_run + 1):
        window = nibbles[start : start + min_run]
        diffs = {(window[i + 1] - window[i]) % 16 for i in range(len(window) - 1)}
        if len(diffs) == 1 and next(iter(diffs)) in allowed_steps:
            return True
    return False


_PLUS_MINUS_ONE = {1, 15}
_ANY_NONZERO = set(range(1, 16))


def _has_interleaved_sequence(nibbles: list[int]) -> bool:
    """Detect patterns where every-other nibble forms an arithmetic run.

    Example: ``e1d2c3b4`` — even nibbles e,d,c,b descend by 1; odd nibbles
    1,2,3,4 ascend by 1.
    """
    return any(
        _has_sequential_run(nibbles[offset::2], 5, _PLUS_MINUS_ONE)
        for offset in (0, 1)
    )


def _has_straight_sequence(nibbles: list[int]) -> bool:
    """Detect a straight run of nibbles with constant non-zero step."""
    return _has_sequential_run(nibbles, 6, _ANY_NONZERO)


def check_uuid(u: str) -> Optional[str]:
    """Return an error string if *u* looks suspicious, else ``None``."""
    lower = u.lower()

    if lower in _PERMANENT_ALLOWLIST:
        return None

    try:
        parsed = uuid.UUID(lower)
    except ValueError:
        return "invalid UUID"

    if parsed.version not in _ALLOWED_VERSIONS:
        return f"non-random UUID (version={parsed.version})"

    nibbles = _to_nibbles(lower)
    if _has_interleaved_sequence(nibbles) or _has_straight_sequence(nibbles):
        return "sequential pattern detected — looks hand-typed"

    return None


def _opt_out_problem(line: str) -> Optional[str]:
    """Return ``""`` for a valid opt-out, an error for one without a reason, else ``None``."""
    match = _NOQA_RE.search(line)
    if not match:
        return None
    return "" if match.group("reason").strip(_REASON_PUNCTUATION) else _MISSING_REASON


def find_suspicious_uuids(line: str) -> list[tuple[str, str]]:
    """Return a list of ``(uuid, problem)`` tuples for suspicious UUIDs on *line* that are not opted out."""
    findings: list[tuple[str, str]] = []
    for match in _UUID_RE.finditer(line):
        u = match.group(1)
        error = check_uuid(u)
        if not error:
            continue
        opt_out = _opt_out_problem(line)
        if opt_out is None:
            findings.append((u, error))
        elif opt_out:
            findings.append((u, opt_out))
    return findings


def _get_added_lines(filepath: str) -> list[tuple[int, str]]:
    """Return ``(line_number, text)`` pairs for every added line in the staged diff."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "-U0", "--", filepath],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    added: list[tuple[int, str]] = []
    current_line = 0
    for diff_line in result.stdout.splitlines():
        if diff_line.startswith("@@"):
            match = _HUNK_RE.search(diff_line)
            if match:
                current_line = int(match.group(1)) - 1
        elif diff_line.startswith("+") and not diff_line.startswith("+++"):
            current_line += 1
            added.append((current_line, diff_line[1:]))
        elif not diff_line.startswith("-"):
            current_line += 1

    return added


def _is_test_file(filepath: str) -> bool:
    return "_test.py" in filepath or "/test_" in filepath


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Detect hand-typed UUIDs in staged Python changes."
    )
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    errors: list[str] = []

    for filepath in args.filenames:
        if _is_test_file(filepath):
            continue

        for lineno, line in _get_added_lines(filepath):
            for u, error in find_suspicious_uuids(line):
                errors.append(f"  {filepath}:{lineno}: {u} — {error}")

    if errors:
        print("Suspicious UUIDs in staged changes:\n")  # noqa: T201
        print("\n".join(errors))  # noqa: T201
        print(  # noqa: T201
            '\nFix: python3 -c "import uuid; print(uuid.uuid4())"'
            "\nIf the UUID is intentional, add `# noqa: UUID001 - <reason>` on its line.",
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
