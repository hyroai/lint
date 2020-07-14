import ast

import gamla
import toolz

from lint import dead_code


def test_allow_unused_public():
    toolz.pipe(
        'I_AM_A_CONSTANT = "asd"',
        ast.parse,
        dead_code.detect,
        gamla.check(toolz.complement(toolz.count), AssertionError),
    )


def test_disallow_unused_private():
    toolz.pipe(
        '_I_AM_A_CONSTANT = "asd"',
        ast.parse,
        dead_code.detect,
        gamla.check(toolz.count, AssertionError),
    )


def test_allow_unused_public_function():
    toolz.pipe(
        "def hi():\n    return 1",
        ast.parse,
        dead_code.detect,
        gamla.check(toolz.complement(toolz.count), AssertionError),
    )


def test_disallow_unused_private_function():
    toolz.pipe(
        "def _hi():\n    return 1",
        ast.parse,
        dead_code.detect,
        gamla.check(toolz.count, AssertionError),
    )
