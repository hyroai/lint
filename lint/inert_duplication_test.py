import ast

import pytest

from lint import inert_duplication


@pytest.mark.parametrize(
    "source,expected_findings",
    [
        ("duplication.duplicate_function(_make_slot)(config)", 1),
        ('duplicate_function(gamla.itemgetter("x"))', 1),
        ("duplication.duplicate_function(lambda x: x)", 1),
        ("compose_left(duplication.duplicate_function(_module_level_fn), other)", 0),
    ],
)
def test_detect_inert_duplication(source, expected_findings):
    assert len(tuple(inert_duplication.detect(ast.parse(source)))) == expected_findings
