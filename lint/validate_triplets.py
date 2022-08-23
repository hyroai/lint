import argparse
import csv
from typing import Optional, Sequence

import gamla


def get_duplicated_objects(relations):
    return gamla.compose_left(
        gamla.filter(
            gamla.compose_left(
                gamla.second,
                gamla.contains(frozenset(relations)),
            ),
        ),
        gamla.mapcat(gamla.compose_left(gamla.nth(2), gamla.split_text(","))),
        gamla.count_by(gamla.identity),
        gamla.valfilter(gamla.greater_than(1)),
        dict.keys,
        tuple,
    )


def _format_file(relations):
    def format_file(filename):
        with open(filename, mode="r") as file_processed:
            duplicated_objects = gamla.pipe(
                file_processed,
                csv.reader,
                tuple,
                get_duplicated_objects(relations),
            )

        if duplicated_objects:
            print(  # noqa:T201
                f"[{filename}] - Some objects are used more than once: {', '.join(duplicated_objects)}.",
            )

        return not bool(duplicated_objects)

    return format_file


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    parser.add_argument("--relations", nargs="+", default=[])
    args = parser.parse_args(argv)
    return gamla.pipe(
        args.filenames,
        gamla.map(_format_file(args.relations)),
        tuple,
        gamla.ternary(gamla.allmap(gamla.identity), gamla.just(0), gamla.just(1)),
    )


if __name__ == "__main__":
    exit(main())
