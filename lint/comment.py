import re

import gamla

detect = gamla.compose_left(
    lambda s: s.split("\n"),
    gamla.filter(
        gamla.alljuxt(
            gamla.compose_left(str.lower, lambda s: re.search(r"\btodo\b", s)),
            lambda s: not re.search(r"#\sTODO\([a-zA-Z]+\):\s.*", s),
        ),
    ),
)
