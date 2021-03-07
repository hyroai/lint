import argparse
import csv
from typing import Optional, Sequence

import gamla


def _format_file(filename):
    with open(filename, mode="rb") as file_processed:
        content_before = file_processed.readlines()

    with open(filename, mode="r") as file_processed:
        rows = tuple(csv.reader(file_processed))

    with open(filename, mode="w") as file_processed:
        csv.writer(file_processed).writerows(
            gamla.pipe(
                rows, gamla.filter(gamla.identity), gamla.sort_by(gamla.head), tuple
            ),
        )

    with open(filename, mode="rb") as file_processed:
        content_after = file_processed.readlines()

    return content_before == content_after


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
