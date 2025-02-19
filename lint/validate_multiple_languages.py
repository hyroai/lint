import ast
import gamla


def _is_configurable_action_call(node: ast.Call) -> bool:
    return (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "configurable_cg"
            and node.func.attr in ["action", "action_with_legacy_key"]
    )


def _is_gamla_frozendict(node: ast.Call) -> bool:
    return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "gamla"
            and node.func.attr == "frozendict"
            and node.args
            and isinstance(node.args[0], ast.Dict)
    )


def _is_configuration_language_key(key: ast.AST) -> bool:
    return (
            isinstance(key, ast.Attribute)
            and isinstance(key.value, ast.Attribute)
            and isinstance(key.value.value, ast.Name)
            and key.value.value.id == "configuration"
            and key.value.attr == "Language"
            and key.attr in ["EN", "ES"]
    )


def _get_language_keys(dict_node: ast.Dict) -> set:
    return {
        key.attr
        for key in dict_node.keys
        if _is_configuration_language_key(key)
    }


def _validate_frozendict_missing_languages(frozendict_node: ast.Call) -> bool:
    if not frozendict_node.args:
        return False

    dict_arg = frozendict_node.args[0]
    if not isinstance(dict_arg, ast.Dict):
        return False

    language_keys = _get_language_keys(dict_arg)
    return "EN" not in language_keys or "ES" not in language_keys


_gen_configurable_actions = gamla.compose_left(
    ast.walk,
    gamla.filter(gamla.is_instance(ast.Call)),
    gamla.filter(_is_configurable_action_call),
)


def _find_invalid_frozendict(node: ast.Call):
    invalid_frozendict = []

    # Check all positional arguments
    for arg in node.args:
        if _is_gamla_frozendict(arg) and _validate_frozendict_missing_languages(arg):
            invalid_frozendict.append((arg, node.lineno))

    # Check all keyword arguments
    for keyword in node.keywords:
        if _is_gamla_frozendict(keyword.value) and _validate_frozendict_missing_languages(keyword.value):
            invalid_frozendict.append((keyword.value, node.lineno))

    return invalid_frozendict


detect = gamla.compose_left(
    _gen_configurable_actions,
    gamla.mapcat(_find_invalid_frozendict),
    gamla.map(
        lambda
            l: f"gamla.frozendict at line {l[1]} must include both configuration.Language.EN and configuration.Language.ES",
    ),
)