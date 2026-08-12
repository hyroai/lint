import ast

import gamla


def _is_call_to_duplicate_function(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, (ast.Name, ast.Attribute))
        and (node.func.id if isinstance(node.func, ast.Name) else node.func.attr)
        == "duplicate_function"
    )


def _is_wrapper_called_immediately(node: ast.AST) -> bool:
    return isinstance(node, ast.Call) and _is_call_to_duplicate_function(node.func)


def _wraps_fresh_object(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and _is_call_to_duplicate_function(node)
        and bool(node.args)
        and isinstance(node.args[0], (ast.Call, ast.Lambda))
    )


detect = gamla.compose_left(
    ast.walk,
    gamla.bifurcate(
        gamla.compose_left(
            gamla.filter(_is_wrapper_called_immediately),
            gamla.map(
                lambda node: f"inert duplicate_function in line {node.lineno}: the wrapper is called immediately and discarded, so it never becomes a graph node.",
            ),
        ),
        gamla.compose_left(
            gamla.filter(_wraps_fresh_object),
            gamla.map(
                lambda node: f"inert duplicate_function in line {node.lineno}: the wrapped call/lambda creates a fresh object that cannot collide with another composition site.",
            ),
        ),
    ),
    gamla.concat,
)
