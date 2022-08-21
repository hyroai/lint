import argparse
import csv
from typing import Optional, Sequence

import gamla

# def _duplicate_object(rows):
#     def _duplicate_object(object_key):
#         return gamla.pipe(rows, gamla.filter(gamla.))
#
#     return _duplicate_object


def _format_file(filename):
    with open(filename, mode="r") as file_processed:
        rows = tuple(csv.reader(file_processed))

        duplicated_objects = gamla.pipe(
            rows,
            gamla.filter(
                gamla.compose_left(
                    gamla.second,
                    gamla.contains(
                        frozenset(
                            {
                                "action/event",
                                "action/suggestions",
                                "action/switch_command",
                                "concept/action",
                            },
                        ),
                    ),
                ),
            ),
            gamla.map(gamla.nth(2)),
            gamla.count_by(gamla.identity),
            gamla.valfilter(gamla.greater_than(1)),
            dict.keys,
            tuple
        )

    if duplicated_objects:
        print(  # noqa:T201
            f"[{filename}] - Some objects are used more than once: {', '.join(duplicated_objects)}.",
        )

    return not bool(duplicated_objects)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    return gamla.pipe(
        argv,
        parser.parse_args,
        gamla.attrgetter("filenames"),
        gamla.map(_format_file),
        tuple,
        gamla.ternary(gamla.allmap(gamla.identity), gamla.just(0), gamla.just(1)),
    )


if __name__ == "__main__":
    exit(main())
