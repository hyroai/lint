"""Script for updating api.rst in accordance with changes in the repository"""
import importlib
import inspect
import sys
from typing import Any, Callable, Iterable, Tuple

import gamla


def _module_filter(package_name: str):
    def module_filter(module):
        return (
            inspect.ismodule(module)
            and package_name in str(module)
            and "test" not in str(module)
        )

    return module_filter


def _get_function_table_entries(module: Tuple[str, Any]) -> str:
    return "".join(
        f"   {o[0]}\n"
        for o in inspect.getmembers(module)
        if inspect.isfunction(o[1]) and o[0][0] != "_"
    )


def _concat_module_table_string(package_name: str):
    def concat_module_table_string(string_so_far: str, module: Tuple[str, Any]) -> str:
        return "".join(
            gamla.concat_with(
                f"{module[0]}\n{len(module[0]) * '-'}\n\n.. currentmodule:: {package_name}.{module[0]}\n\n.. autosummary::\n{_get_function_table_entries(module[1])}\n",
                string_so_far,
            ),
        )

    return concat_module_table_string


def _concat_module_members_string(package_name: str):
    def concat_module_members_string(string_so_far: str, module: str) -> str:
        return "".join(
            gamla.concat_with(
                f".. automodule:: {package_name}.{module}\n   :members:\n\n",
                string_so_far,
            ),
        )

    return concat_module_members_string


def _create_api_string(package_name: str) -> Callable[[Iterable[str]], str]:
    return lambda modules: gamla.reduce(
        _concat_module_members_string(package_name),
        gamla.reduce(_concat_module_table_string(package_name), "API\n===\n\n", modules)
        + "Definitions\n-----------\n\n",
    )


def main():
    print(sys.argv[1])  # noqa
    print(sys.argv)  # noqa
    gamla.pipe(
        sys.argv[1],
        inspect.getmembers,
        gamla.filter(
            gamla.compose_left(
                gamla.second,
                _module_filter(importlib.import_module(sys.argv[1])),
            ),
        ),
        gamla.map(gamla.head),
        gamla.prepare_and_apply(_create_api_string(sys.argv[1])),
        open("./docs/source/api.rst", "w").write,
    )
    return 0


if __name__ == "__main__":
    exit(main())
