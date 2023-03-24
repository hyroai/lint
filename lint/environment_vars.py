import ast

import gamla

_gen_getenv = gamla.compose_left(
    ast.walk,
    gamla.filter(gamla.is_instance(ast.Call)),
    gamla.filter(
        lambda node: node.func.attr == "getenv",
    ),
)

detect = gamla.compose_left(
    _gen_getenv,
    gamla.map(
        lambda l: f"Using os.getenv in line {l.lineno} is not allowed! Use get_environment instead.",
    ),
)
