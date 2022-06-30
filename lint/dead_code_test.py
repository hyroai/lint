import ast

import gamla

from lint import dead_code


def test_allow_unused_public():
    gamla.pipe(
        'I_AM_A_CONSTANT = "asd"',
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.complement(gamla.count), AssertionError),
    )


def test_allow_double_underscore():
    gamla.pipe(
        'd.__getitem__("bla")',
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.complement(gamla.count), AssertionError),
    )


def test_disallow_unused_private():
    gamla.pipe(
        '_I_AM_A_CONSTANT = "asd"',
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.count, AssertionError),
    )


def test_allow_unused_public_function():
    gamla.pipe(
        "def hi():\n    return 1",
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.complement(gamla.count), AssertionError),
    )


def test_disallow_unused_private_function():
    gamla.pipe(
        "def _hi():\n    return 1",
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.count, AssertionError),
    )


def test_disallow_unused_async_private_function():
    gamla.pipe(
        "async def _hi():\n    return 1",
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.count, AssertionError),
    )


def test_class_methods_allowed():
    gamla.pipe(
        """@dataclasses.dataclass(frozen=True)
class SomeClass:
    # Some comment.
    text: Text
    _private_thing: Text = "bla"

    def is_something(self) -> bool:
        return self._private_thing in []
    """,
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.complement(gamla.count), AssertionError),
    )


def test_class_methods_disallowed():
    gamla.pipe(
        """@dataclasses.dataclass(frozen=True)
class SomeClass:
    # Some comment.
    text: Text
    _private_thing: Text = "bla"
""",
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.count, AssertionError),
    )


def test_private_class():
    gamla.pipe(
        "class _Something: pass; A = _Something()",
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.complement(gamla.count), AssertionError),
    )


def test_private_module():
    gamla.pipe(
        "from . import _a;print(_a.symbol)",
        ast.parse,
        dead_code.detect,
        gamla.check(gamla.complement(gamla.count), AssertionError),
    )
