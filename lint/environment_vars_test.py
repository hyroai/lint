import ast

import gamla

from lint import environment_vars


def test_use_of_getenv():
    gamla.pipe(
        'MY_ENV = os.getenv("MY_ENV")',
        ast.parse,
        environment_vars.detect,
        gamla.assert_that(gamla.nonempty),
    )


def test_use_of_environ():
    gamla.pipe(
        'MY_ENV = os.environ["MY_ENV"]',
        ast.parse,
        environment_vars.detect,
        gamla.assert_that(gamla.empty),
    )
