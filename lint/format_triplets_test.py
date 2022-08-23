import pytest

from lint import format_triplets


@pytest.mark.parametrize(
    "rows",
    (
        [["a", "rel", "b"]],
        [["a", "rel", "b,d"], ["c", "rel", "e,f"]],
    ),
)
def test_good(rows):
    assert not format_triplets.get_duplicated_objects(["rel"])(rows)


@pytest.mark.parametrize(
    "rows",
    (
        [["a", "rel", "b"], ["c", "rel", "b"]],
        [["a", "rel", "b,d"], ["c", "rel", "b,e"]],
    ),
)
def test_bad(rows):
    assert format_triplets.get_duplicated_objects(["rel"])(rows)
