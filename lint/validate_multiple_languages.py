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


def _is_empty_string(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value == ""


def _is_empty_action(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "Action"
        and node.args
        and _is_empty_string(node.args[0])
    )


def _validate_frozendict_node(frozendict_node: ast.Call, lineno: int) -> list:
    if not frozendict_node.args:
        return []

    dict_arg = frozendict_node.args[0]
    if not isinstance(dict_arg, ast.Dict):
        return []

    errors = []
    lang_map = _get_language_keys(dict_arg)

    if "EN" not in lang_map or "ES" not in lang_map:
        errors.append((frozendict_node, lineno, "missing_langs"))

    for key, value in zip(dict_arg.keys, dict_arg.values):
        if _is_configuration_language_key(key) and (_is_empty_string(value) or _is_empty_action(value)):
            errors.append((frozendict_node, lineno, f"empty_{key.attr}"))

    return errors


_gen_configurable_actions = gamla.compose_left(
    ast.walk,
    gamla.filter(gamla.is_instance(ast.Call)),
    gamla.filter(_is_configurable_action_call),
)


def _find_invalid_frozendict(node: ast.Call):
    invalid_frozendict = []

    for arg in node.args:
        if _is_gamla_frozendict(arg):
            invalid_frozendict.extend(_validate_frozendict_node(arg, node.lineno))

    for keyword in node.keywords:
        if keyword.arg == "default_action" and not _is_gamla_frozendict(keyword.value):
            invalid_frozendict.append((keyword.value, node.lineno, "invalid_default_action"))
        elif _is_gamla_frozendict(keyword.value):
            invalid_frozendict.extend(_validate_frozendict_node(keyword.value, node.lineno))

    return invalid_frozendict


def _format_error_message(error_tuple):
    node, lineno, error_type = error_tuple

    if error_type == "missing_langs":
        return f"gamla.frozendict at line {lineno} must include both configuration.Language.EN and configuration.Language.ES"
    elif error_type.startswith("empty_"):
        lang = error_type.split("_")[1]
        return f"gamla.frozendict at line {lineno} has empty string for configuration.Language.{lang}"
    elif error_type == "invalid_default_action":
        return f"default_action at line {lineno} must be a gamla.frozendict"

    return f"Invalid frozendict configuration at line {lineno}"


detect = gamla.compose_left(
    _gen_configurable_actions,
    gamla.mapcat(_find_invalid_frozendict),
    gamla.map(_format_error_message),
    tuple,
)