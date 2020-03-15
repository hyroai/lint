import argparse
import ast
from typing import Optional, Sequence

import toolz
from toolz import curried

import gamla
from lint import redundant_lambda

_RULES = (redundant_lambda.detect,)

_file_contents_to_messages = toolz.compose_left(
    gamla.log_text("{}"), open, lambda f: f.read(), ast.parse, gamla.juxtcat(*_RULES)
)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    return toolz.pipe(
        argv,
        parser.parse_args,
        lambda args: args.filenames,
        curried.mapcat(_file_contents_to_messages),
        curried.map(print),
        tuple,
        gamla.curried_ternary(toolz.identity, gamla.just(1), gamla.just(0)),
    )


if __name__ == "__main__":
    exit(main())
