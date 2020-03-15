import ast

import redundant_lambda

import toolz

import gamla


def test_detect_redundant_lambda():
    toolz.pipe(
        """something = functools.lru_cache(maxsize=1024)(
    toolz.compose_left(
        toolz.pipe(
            _CONFIDENCE_ELEMENTS, curried.map(_collect_type), gamla.star(gamla.juxtcat)
        ),
        curried.filter(lambda element: element.confidence is not None),
        curried.map(lambda element: element.confidence),
        tuple,
        gamla.check(lambda x: toolz.identity(x), ValueError),
        gamla.average,
    )
)""",
        ast.parse,
        redundant_lambda.detect,
        tuple,
        gamla.check(toolz.identity, AssertionError),
    )
