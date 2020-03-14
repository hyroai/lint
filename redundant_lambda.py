import ast
from typing import Iterable

import gamla
import toolz
from toolz import curried
from toolz.curried import operator

_gen_lambdas = toolz.compose_left(
    ast.walk, curried.filter(lambda x: isinstance(x, ast.Lambda))
)


def _gen_lambda_arg_names(l: ast.Lambda) -> Iterable[str]:
    return toolz.pipe(l, lambda l: l.args.args, curried.map(lambda a: a.arg))


_is_unary_def = toolz.compose_left(_gen_lambda_arg_names, toolz.count, operator.eq(1))


def _is_lambda_internal_invocation(l: ast.Lambda) -> bool:
    return toolz.pipe(l.body, lambda b: isinstance(b, ast.Call))


def _get_call_arg_names(call: ast.Call) -> Iterable[str]:
    return toolz.pipe(
        toolz.concat([call.args, call.keywords]),
        curried.map(
            gamla.curried_ternary(
                # Generator expressions can also be given as arguments.
                lambda arg: isinstance(arg, ast.Name),
                lambda arg: arg.id,
                gamla.just(None),
            )
        ),
    )


_is_lambda_redundant = gamla.alljuxt(
    _is_lambda_internal_invocation,
    _is_unary_def,
    toolz.compose_left(
        toolz.juxt(
            toolz.compose_left(_gen_lambda_arg_names, toolz.first),
            toolz.compose_left(lambda l: l.body, _get_call_arg_names, tuple),
        ),
        gamla.star(
            lambda lambda_arg, internal_call_args: gamla.len_equals(
                1, internal_call_args
            )
            and toolz.first(internal_call_args) == lambda_arg
        ),
    ),
)


detect = toolz.compose_left(
    _gen_lambdas,
    curried.filter(_is_lambda_redundant),
    curried.map(lambda l: f"redundant lambda in line {l.lineno}!"),
)
