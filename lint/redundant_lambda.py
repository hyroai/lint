import ast
from typing import Iterable

import gamla

_gen_lambdas = gamla.compose_left(
    ast.walk,
    gamla.filter(gamla.is_instance(ast.Lambda)),
)


def _gen_lambda_arg_names(l: ast.Lambda) -> Iterable[str]:
    return gamla.pipe(l, lambda l: l.args.args, gamla.map(gamla.attrgetter("arg")))


_is_unary_def = gamla.compose_left(_gen_lambda_arg_names, gamla.count, gamla.equals(1))


def _is_lambda_internal_invocation(l: ast.Lambda) -> bool:
    return gamla.pipe(l.body, gamla.is_instance(ast.Call))


def _get_call_arg_names(call: ast.Call) -> Iterable[str]:
    return gamla.pipe(
        gamla.concat([call.args, call.keywords]),
        gamla.map(
            gamla.ternary(
                # Generator expressions can also be given as arguments.
                gamla.is_instance(ast.Name),
                gamla.attrgetter("id"),
                gamla.just(None),
            ),
        ),
    )


_is_lambda_redundant = gamla.alljuxt(
    _is_lambda_internal_invocation,
    _is_unary_def,
    gamla.compose_left(
        gamla.juxt(
            gamla.compose_left(_gen_lambda_arg_names, gamla.head),
            gamla.compose_left(lambda l: l.body, _get_call_arg_names, tuple),
        ),
        gamla.star(
            lambda lambda_arg, internal_call_args: gamla.len_equals(
                1,
                internal_call_args,
            )
            and gamla.head(internal_call_args) == lambda_arg,
        ),
    ),
)


detect = gamla.compose_left(
    _gen_lambdas,
    gamla.filter(_is_lambda_redundant),
    gamla.map(lambda l: f"redundant lambda in line {l.lineno}!"),
)
