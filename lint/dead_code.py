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
        gamla.compose_left(
            gamla.filter(gamla.is_instance(ast.alias)),
            gamla.map(
                gamla.compose_left(
                    gamla.juxt(*map(gamla.attrgetter, ("asname", "name"))),
                    gamla.filter(bool),
                    gamla.head,
                ),
            ),
        ),
    ),
    gamla.concat,
    gamla.filter(lambda name: name.startswith("_")),
    gamla.remove(lambda name: name.startswith("__")),
    gamla.remove(gamla.equals("_")),
    gamla.count_by(gamla.identity),
    gamla.valfilter(gamla.equals(1)),
    dict.keys,
    gamla.map(gamla.wrap_str("`{}` is defined but unused.")),
)
