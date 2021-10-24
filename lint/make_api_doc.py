"""Script for updating api.rst in accordance with changes in the repository"""
import importlib
import inspect
import sys
from typing import Any, Text, Tuple

import gamla

_PACKAGE_NAME = sys.argv[1]


def _module_filter(module):
    return (
        inspect.ismodule(module)
        and _PACKAGE_NAME in str(module)
        and "test" not in str(module)
    )


def _get_modules(package) -> Tuple[Tuple[Text, Any], ...]:
    return tuple(inspect.getmembers(package, _module_filter))


def _get_function_table_entries(module: Tuple[Text, Any]) -> Text:
    return "".join(
        [
            f"   {o[0]}\n"
            for o in inspect.getmembers(module)
            if inspect.isfunction(o[1]) and o[0][0] != "_"
        ],
    )


def _concat_module_table_string(string_so_far: Text, module: Tuple[Text, Any]) -> Text:
    return "".join(
        gamla.concat_with(
            f"{module[0]}\n{len(module[0]) * '-'}\n\n.. currentmodule:: {_PACKAGE_NAME}.{module[0]}\n\n.. autosummary::\n{_get_function_table_entries(module[1])}\n",
            string_so_far,
        ),
    )


def _concat_module_members_string(
    string_so_far: Text,
    module: Tuple[Text, Any],
) -> Text:
    return "".join(
        gamla.concat_with(
            f".. automodule:: {_PACKAGE_NAME}.{module[0]}\n   :members:\n\n",
            string_so_far,
        ),
    )


def _create_api_string(modules: Tuple[Tuple[Text, Any], ...]) -> Text:
    return gamla.reduce(
        _concat_module_members_string,
        gamla.reduce(_concat_module_table_string, "API\n===\n\n", modules)
        + "Definitions\n-----------\n\n",
        modules,
    )


def main():
    with open("./docs/source/api.rst", "w") as new_api_file:
        new_api_file.write(
            _create_api_string(_get_modules(importlib.import_module(".", _PACKAGE_NAME))),
        )
    return 0


if __name__ == "__main__":
    exit(main())
