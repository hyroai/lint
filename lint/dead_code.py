import ast

import gamla

detect = gamla.compose_left(
    ast.walk,
    gamla.bifurcate(
        gamla.compose_left(
            gamla.filter(
                gamla.anyjuxt(
                    gamla.is_instance(ast.AsyncFunctionDef),
                    gamla.is_instance(ast.FunctionDef),
                    gamla.is_instance(ast.ClassDef),
                ),
            ),
            gamla.map(gamla.attrgetter("name")),
        ),
        gamla.compose_left(
            gamla.filter(gamla.is_instance(ast.Name)),
            gamla.map(gamla.attrgetter("id")),
        ),
        gamla.compose_left(
            gamla.filter(gamla.is_instance(ast.Attribute)),
            gamla.map(gamla.attrgetter("attr")),
        ),
    ),
    gamla.concat,
    gamla.filter(lambda name: name.startswith("_")),
    gamla.remove(
        gamla.contains(
            {
                "__code__",
                "__contains__",
                "__file__",
                "__getattribute__",
                "__getitem__",
                "__gt__",
                "__hash__",
                "__len__",
                "__name__",
                "__post_init__",
                "__repr__",
                "__traceback__",
            },
        ),
    ),
    gamla.count_by(gamla.identity),
    gamla.valfilter(gamla.equals(1)),
    dict.keys,
    gamla.map(gamla.wrap_str("`{}` is defined but unused.")),
)
