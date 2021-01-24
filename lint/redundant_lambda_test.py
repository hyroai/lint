import ast

import gamla

from lint import redundant_lambda


def test_detect_redundant_lambda():
    gamla.pipe(
        """something = functools.lru_cache(maxsize=1024)(
    gamla.compose_left(
        gamla.pipe(
            _CONFIDENCE_ELEMENTS, gamla.map(_collect_type), gamla.star(gamla.juxtcat)
        ),
        gamla.filter(lambda element: element.confidence is not None),
        gamla.map(lambda element: element.confidence),
        tuple,
        gamla.check(lambda x: gamla.identity(x), ValueError),
        gamla.average,
    )
)""",
        ast.parse,
        redundant_lambda.detect,
        tuple,
        gamla.check(gamla.identity, AssertionError),
    )
