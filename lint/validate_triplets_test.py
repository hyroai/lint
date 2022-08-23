import pytest

from lint import validate_triplets


@pytest.mark.parametrize(
    "rows",
    (
        [["a", "rel", "b"]],
        [["a", "rel", "b,d"], ["c", "rel", "e,f"]],
    ),
)
def test_good_duplicated_references(rows):
    assert not validate_triplets.get_duplicated_references(["rel"])(rows)


@pytest.mark.parametrize(
    "rows",
    (
        [["a", "rel", "b"], ["c", "rel", "b"]],
        [["a", "rel", "b,d"], ["c", "rel", "b,e"]],
    ),
)
def test_bad_duplicated_references(rows):
    assert validate_triplets.get_duplicated_references(["rel"])(rows)


@pytest.mark.parametrize(
    "rows",
    (
        [["a", "rel", "b"], ["b", "rel1", "c"]],
        [["a", "rel", "b,d"], ["b", "rel1", "e"], ["d", "rel1", "f"]],
    ),
)
def test_good_detached_references(rows):
    assert not validate_triplets.get_detached_references(["rel"])(rows)


@pytest.mark.parametrize(
    "rows",
    (
        [["a", "rel", "b"]],
        [["a", "rel", "b,d"], ["c", "rel", "b,e"]],
    ),
)
def test_bad_detached_references(rows):
    assert validate_triplets.get_detached_references(["rel"])(rows)
