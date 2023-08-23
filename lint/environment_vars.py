import ast

import gamla

_gen_getenv = gamla.compose_left(
    ast.walk,
    gamla.filter(gamla.is_instance(ast.Attribute)),
    gamla.filter(
        lambda node: node.attr == "getenv",
    ),
)

detect = gamla.compose_left(
    _gen_getenv,
    gamla.map(
        lambda l: f"Using os.getenv in line {l.lineno} is not allowed! Use nlu.config.get_env_var instead.",
    ),
)
