import argparse
import ast
from typing import Optional, Sequence, Tuple

import gamla

from lint import (
    comment,
    dead_code,
    development_functions,
    environment_vars,
    redundant_lambda,
    validate_multiple_languages,
)

_file_contents_to_messages = gamla.compose_left(
    gamla.log_text("{}"),
    open,
    lambda f: f.read(),
    gamla.juxtcat(
        gamla.compose_left(
            ast.parse,
            gamla.juxtcat(
                redundant_lambda.detect,
                dead_code.detect,
                environment_vars.detect,
                development_functions.detect,
                validate_multiple_languages.detect,
            ),
        ),
        comment.detect,
    ),
    tuple,
)


def _pretty_print_findings(findings: Tuple[str, ...], filename: str):
    print(filename)  # noqa
    for finding in findings:
        print(finding)  # noqa


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    return gamla.pipe(
        argv,
        parser.parse_args,
        gamla.attrgetter("filenames"),
        gamla.map(gamla.pair_with(_file_contents_to_messages)),
        gamla.filter(gamla.head),
        gamla.map(gamla.side_effect(gamla.star(_pretty_print_findings))),
        tuple,
        gamla.ternary(gamla.identity, gamla.just(1), gamla.just(0)),
    )


if __name__ == "__main__":
    exit(main())
