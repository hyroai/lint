import argparse
from typing import Optional, Sequence

import gamla


def _remove_empty_lines_in_file(filename):
    with open(filename, mode="rb") as file_processed:
        lines = file_processed.readlines()
    non_empty_lines = [line for line in lines if line]
    with open(filename, mode="wb") as file_processed:
        for line in non_empty_lines:
            file_processed.write(line)
    return len(lines) == len(non_empty_lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    return gamla.pipe(
        argv,
        parser.parse_args,
        gamla.attrgetter("filenames"),
        gamla.map(_remove_empty_lines_in_file),
        tuple,
        gamla.ternary(gamla.allmap(gamla.identity), gamla.just(0), gamla.just(1)),
    )


if __name__ == "__main__":
    exit(main())
