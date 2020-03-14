import ast
import pathlib

import gamla
import toolz
from toolz import curried
import redundant_lambda

_RULES = (redundant_lambda.detect,)

_file_contents_to_messages = toolz.compose_left(
    gamla.log_text("{}"), open, lambda f: f.read(), ast.parse, gamla.juxtcat(*_RULES)
)


if __name__ == "__main__":
    toolz.pipe(
        pathlib.Path("./").glob("**/*.py"),
        curried.mapcat(_file_contents_to_messages),
        curried.map(print),
        tuple,  # Materialize.
    )
