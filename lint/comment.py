import re

import gamla

detect = gamla.compose_left(
    lambda s: s.split("\n"),
    gamla.filter(gamla.compose_left(str.lower, lambda s: re.match(r"\s*(#|//).*", s))),
    gamla.remove(lambda s: re.search(r"# type: ignore", s)),
    gamla.remove(lambda s: re.search(r"noqa", s)),
    gamla.compose_left(
        gamla.filter(
            gamla.alljuxt(
                gamla.compose_left(str.lower, lambda s: re.search(r"\btodo\b", s)),
                lambda s: not re.search(r"(#|//)\sTODO\([a-zA-Z]+\):\s.*", s),
            ),
        ),
        gamla.map(
            lambda s: f"Malformatted `TODO` syntax (should be `TODO(name): ...`): [{s}]",
        ),
    ),
    tuple,
)
