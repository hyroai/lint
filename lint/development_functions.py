import ast

import gamla


def _get_functions_and_references(node):
    return gamla.pipe(
        node,
        gamla.case_dict(
            {
                gamla.is_instance(ast.Call): gamla.compose_left(
                    gamla.attrgetter("func"),
                    _get_functions_and_references,
                ),
                gamla.is_instance(
                    ast.Attribute,
                ): lambda n: f"{_get_functions_and_references(n.value)}.{n.attr}",
                gamla.is_instance(ast.Name): gamla.attrgetter("id"),
                gamla.just(True): gamla.identity,
            },
        ),
    )


_get_function_and_reference_ids = gamla.compose_left(
    ast.walk,
    gamla.filter(lambda node: isinstance(node, (ast.Call, ast.Attribute, ast.Name))),
    gamla.map(_get_functions_and_references),
    gamla.unique,
    gamla.filter(gamla.is_instance(str)),
)


def _is_development_call(util: str):
    return gamla.pipe(
        [
            "versions_updater.cache_kg_force",
            "versions_updater.cache_main_kg_force",
            "versions_updater.cache_faq_kg_force",
            "breakpoint",
            "ipdb",
            "gamla.debug",
            "debug.debug",
            "slot_filling.debug_log"
        ],
        gamla.anymap(gamla.contains(util)),
    )


detect = gamla.compose_left(
    _get_function_and_reference_ids,
    gamla.filter(_is_development_call),
    gamla.unique,
    gamla.map(lambda l: f"Usage of {l}!"),
)
