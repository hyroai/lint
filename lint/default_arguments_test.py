import ast

import gamla

from lint import default_arguments


def test_detect_default_arguments():
    gamla.pipe(
        [
            "def f(x=3): return x",
            "async def f(x=3): return x",
            "def f(x=3, y=4): return x + y",
            "lambda x=3: x",
            "lambda x=3, y=4: x + y",
        ],
        gamla.map(
            gamla.compose_left(
                ast.parse,
                default_arguments.detect,
                gamla.assert_that(gamla.nonempty),
            ),
        ),
        tuple,
    )


def test_detect_no_default_arguments():
    gamla.pipe(
        [
            "def f(x): return x",
            "async def f(x): return x",
            "def f(x, y): return x + y",
            "lambda x: x",
            "lambda x, y: x + y",
        ],
        gamla.map(
            gamla.compose_left(
                ast.parse,
                default_arguments.detect,
                gamla.assert_that(gamla.empty),
            ),
        ),
        tuple,
    )
