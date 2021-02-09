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
            gamla.map(lambda function_or_class: function_or_class.name),
        ),
        gamla.compose_left(
            gamla.filter(gamla.is_instance(ast.Name)),
            gamla.map(lambda name: name.id),
        ),
        gamla.compose_left(
            gamla.filter(gamla.is_instance(ast.Attribute)),
            gamla.map(lambda attribute: attribute.attr),
        ),
    ),
    gamla.concat,
    gamla.filter(lambda name: name.startswith("_")),
    gamla.remove(lambda name: name.startswith("__")),
    gamla.remove(gamla.equals("_")),
    gamla.count_by(gamla.identity),
    gamla.valfilter(gamla.equals(1)),
    dict.keys,
    gamla.map(lambda name: f"`{name}` is defined but unused."),
)
