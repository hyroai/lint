import re

import gamla

detect = gamla.compose_left(
    lambda s: s.split("\n"),
    gamla.filter(gamla.compose_left(str.lower, lambda s: re.match(r"\s*#.*", s))),
    gamla.bifurcate(
        gamla.compose_left(
            gamla.filter(
                gamla.alljuxt(
                    gamla.compose_left(str.lower, lambda s: re.search(r"\btodo\b", s)),
                    lambda s: not re.search(r"#\sTODO\([a-zA-Z]+\):\s.*", s),
                ),
            ),
            gamla.map(
                lambda s: f"Malformatted `TODO` syntax (should be `# TODO(name): ...`): [{s}]",
            ),
        ),
        gamla.compose_left(
            gamla.filter(lambda s: not re.search(r"#.*[.?]", s)),
            gamla.map(lambda s: f"Comment should end with a punctuation: [{s}]"),
        ),
        gamla.compose_left(
            gamla.filter(lambda s: re.search(r"#[^\s]", s)),
            gamla.map(lambda s: f"Comment should start with a space: [{s}]"),
        ),
        gamla.compose_left(
            gamla.filter(lambda s: re.search(r"#\s[a-z]", s)),
            gamla.map(lambda s: f"Comment should be capitalized: [{s}]"),
        ),
    ),
    gamla.concat,
)
