import ast

import gamla
import toolz
from toolz import curried
from toolz.curried import operator


detect = gamla.compose_left(
    ast.walk,
    gamla.bifurcate(
        gamla.compose_left(
            curried.filter(gamla.is_instance(ast.FunctionDef)),
            curried.map(lambda function: function.name),
        ),
        gamla.compose_left(
            curried.filter(gamla.is_instance(ast.Name)),
            curried.map(lambda name: name.id),
        ),
    ),
    toolz.concat,
    curried.filter(lambda name: name.startswith("_")),
    curried.countby(toolz.identity),
    curried.valfilter(operator.eq(1)),
    dict.keys,
    curried.map(lambda name: f"`{name}` is defined but unused."),
)
