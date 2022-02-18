import ast

import gamla

_functions_and_lambdas = gamla.compose_left(
    ast.walk,
    gamla.filter(
        gamla.anyjuxt(
            *map(
                gamla.is_instance,
                [ast.AsyncFunctionDef, ast.FunctionDef, ast.Lambda],
            ),
        ),
    ),
)


_has_default_argument = gamla.compose_left(
    gamla.attrgetter("args"),
    gamla.attrgetter("defaults"),
    gamla.nonempty,
)


detect = gamla.compose_left(
    _functions_and_lambdas,
    gamla.filter(_has_default_argument),
    gamla.map(lambda l: f"default arguments in line {l.lineno}!"),
)
