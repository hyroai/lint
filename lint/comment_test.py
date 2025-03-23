import gamla

from lint import comment


def test_good():
    for good_comment in [
        "## I am a markdown numbered list bullet",
        "# TODO(uri): I am a good comment.",
        "# I am good too.",
        "a = 3  # I am good.",
        "from nlu.config import logging_config  # noqa: F401",
        "    for element in filter(  # type: ignore",
        '            url=render.add_utm_param("https://example.example.org/#screening"),',
        "        # https://example.com/example/index.html#/example/",
        "#: Bla bla.",
        "// Bla bla.",
        "// TODO(David): I am a good comment.",
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
        "// todo(david): I am a bad comment.",
        "//no leading space",
    ]:
        gamla.pipe(
            bad_comment,
            comment.detect,
            gamla.check(gamla.count, AssertionError),
        )
