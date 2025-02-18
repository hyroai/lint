import re
import gamla

LANGUAGE_PATTERN = re.compile(r"configuration\.Language\.([A-Z]+)")


def detect_missing_languages(code: str) -> list:
    languages = set(LANGUAGE_PATTERN.findall(code))

    if languages < {"EN", "ES"}:  # Check if both EN and ES exist
        return ["Missing required language translations (EN and ES)."]

    return []


detect = gamla.compose_left(
    lambda s: s.split("\n\n"),
    gamla.map(detect_missing_languages),
    gamla.concat,
)
