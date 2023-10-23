import json
import pathlib

from lint import format_assistant_configuration

PARENT_LIB_PATH = pathlib.Path(__file__).parent.resolve().__str__()
UNSORTED_ASSISTANT_FILE_PATH = (
    PARENT_LIB_PATH + "/test_mock_data/unsorted_assistant_configuration.json"
)
SORTED_ASSISTANT_FILE_PATH = (
    PARENT_LIB_PATH + "/test_mock_data/sorted_assistant_configuration.json"
)


def test_assistant_json_formatter():
    content_after_format = format_assistant_configuration.sort_assistant_configurations(
        open(UNSORTED_ASSISTANT_FILE_PATH, "r").read(),
    )
    sorted_content = open(SORTED_ASSISTANT_FILE_PATH, "r").read()
    assert json.loads(content_after_format) == json.loads(sorted_content)
