import argparse
import csv
from typing import Optional, Sequence

import gamla


def _get_objects_from_relations(relations):
    return gamla.compose_left(
        gamla.filter(
            gamla.compose_left(
                gamla.second,
                gamla.contains(frozenset(relations)),
            ),
        ),
        gamla.mapcat(gamla.compose_left(gamla.nth(2), gamla.split_text(","))),
    )


def get_duplicated_references(relations):
    return gamla.compose_left(
        _get_objects_from_relations(relations),
        gamla.count_by(gamla.identity),
        gamla.valfilter(gamla.greater_than(1)),
        dict.keys,
        tuple,
    )


def get_detached_references(relations):
    return gamla.compose_left(
        gamla.juxt(
            gamla.compose_left(_get_objects_from_relations(relations), set),
            gamla.compose_left(gamla.map(gamla.head), set),
        ),
        gamla.star(set.difference),
        tuple,
    )


def _format_file(relations):
    def format_file(filename):
        with open(filename, mode="r") as file_processed:
            duplicated_references, detached_references = gamla.pipe(
                file_processed,
                csv.reader,
                tuple,
                gamla.juxt(
                    get_duplicated_references(relations),
                    get_detached_references(relations),
                ),
            )

        if duplicated_references:
            print(  # noqa:T201
                f"[{filename}] - Some references are used more than once: {', '.join(duplicated_references)}.",
            )

        if detached_references:
            print(  # noqa:T201
                f"[{filename}] - Some references are defined but not used: {', '.join(detached_references)}.",
            )

        return not bool(duplicated_references) and not bool(detached_references)

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
