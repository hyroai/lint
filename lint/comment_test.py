import gamla

from lint import comment


def test_good():
    for good_comment in [
        "# TODO(uri): I am a good comment.",
        "# I am good too.",
        "a = 3  # I am good.",
    ]:
        gamla.pipe(
            good_comment,
            comment.detect,
            gamla.check(gamla.complement(gamla.count), AssertionError),
        )


def test_bad():
    for bad_comment in [
        "# todo(uri): I am a bad comment.",
        "#todo: do something",
        "# TODO ROM: uncomment when vaccine faq fixed",
        "# TODO (rachel): Remove if not relevant after rescraping novant's vaccine faq.",
        "#no leading space",
        "# not capitalized",
        "# No dot at end",
    ]:
        gamla.pipe(
            bad_comment,
            comment.detect,
            gamla.check(gamla.count, AssertionError),
        )
