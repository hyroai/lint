from lint import format_triplets


def test_good():
    assert not format_triplets.get_duplicated_objects(["rel"])(
        [["a", "rel", "b"]],
    )


def test_bad():
    assert format_triplets.get_duplicated_objects(["rel"])(
        [["a", "rel", "b"], ["c", "rel", "b"]],
    )
