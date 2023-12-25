import argparse
import json
from typing import Optional, Sequence

import gamla

_sort_by_key = gamla.sort_by(gamla.itemgetter("key"))


def sort_assistant_configurations_v2(initial_assistant_configuration: dict) -> dict:
    initial_assistant_configuration["base_skill"]["configuration"].update(
        {
            "configuration": _sort_by_key(
                initial_assistant_configuration["base_skill"]["configuration"][
                    "configuration"
                ],
            ),
        },
    )
    if initial_assistant_configuration["context"] is not None:
        initial_assistant_configuration["context"]["configuration"].update(
            {
                "configuration": _sort_by_key(
                    initial_assistant_configuration["context"]["configuration"][
                        "configuration"
                    ],
                ),
            },
        )
    initial_assistant_configuration.update(
        {
            "skills": gamla.pipe(
                initial_assistant_configuration["skills"],
                gamla.map(
                    gamla.valmap(
                        gamla.when(
                            gamla.is_instance(dict),
                            gamla.valmap(
                                gamla.when(gamla.is_instance(list), _sort_by_key),
                            ),
                        ),
                    ),
                ),
                tuple,
            ),
        },
    )

    return initial_assistant_configuration


# TODO(Reut): Deprecated. remove when we are on v2 only (ENG-8353).
def sort_assistant_configurations_v1(initial_assistant_configuration: dict) -> dict:
    initial_assistant_configuration["base_skill"].update(
        {
            "configuration": _sort_by_key(
                initial_assistant_configuration["base_skill"]["configuration"],
            ),
        },
    )
    initial_assistant_configuration["context"].update(
        {
            "configuration": _sort_by_key(
                initial_assistant_configuration["context"]["configuration"],
            ),
        },
    )
    initial_assistant_configuration.update(
        {
            "skills": gamla.pipe(
                initial_assistant_configuration["skills"],
                gamla.map(
                    gamla.valmap(
                        gamla.when(gamla.is_instance(list), _sort_by_key),
                    ),
                ),
                tuple,
            ),
        },
    )
    return initial_assistant_configuration


def _format_file(filename):
    with open(filename, mode="r") as file_processed:
        content_before = json.loads(file_processed.read())
        if "version" not in content_before.keys() or (
            content_before["version"] == "V1"
        ):
            sorted_content = sort_assistant_configurations_v1(content_before)
        else:
            sorted_content = sort_assistant_configurations_v2(content_before)

    identical = sorted_content == content_before
    if not identical:
        with open(filename, mode="w") as file_processed:
            file_processed.write(json.dumps(sorted_content))
            print(f"File {filename} has been modified.")  # noqa:T201

    return identical


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
