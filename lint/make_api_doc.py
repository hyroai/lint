"""Script for updating api.rst in accordance with changes in the repository"""
import inspect
import sys
from importlib import util as importlib_util
from typing import Callable

import gamla


def _load_module_from_path(path: str):
    spec = importlib_util.spec_from_file_location("gamla", path)
    module = importlib_util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _process_function_name_and_doc(name: str, doc: str) -> str:
    return f"## {name}\n\n{doc}\n\n"


_process_module: Callable[[str], str] = gamla.compose_left(
    _load_module_from_path,
    inspect.getmembers,
    gamla.filter(lambda member: inspect.isfunction(member[1]) and member[0][0] != "_"),
    gamla.map(gamla.packstack(gamla.identity, inspect.getdoc)),
    gamla.remove(gamla.compose(gamla.equals(None), gamla.second)),
    gamla.map(gamla.star(_process_function_name_and_doc)),
    "\n".join,
)


def main():
    gamla.pipe(
        sys.argv[1:],
        gamla.remove(gamla.anyjuxt(gamla.equals("setup.py"), gamla.inside("_test.py"))),
        gamla.map(_process_module),
        "\n".join,
        open("./docs.md", "w").write,
    )
    return 0


if __name__ == "__main__":
    exit(main())
