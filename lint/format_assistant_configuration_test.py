import json
import pathlib

import pytest

from lint import format_assistant_configuration

_UNSORTED_ASSISTANT_FILE_PATH = (
    pathlib.Path(__file__).parent.resolve().__str__()
    + "/test_mock_data/unsorted_assistant_configuration.json"
)

_UNSORTED_ASSISTANT_V2_FILE_PATH = (
    pathlib.Path(__file__).parent.resolve().__str__()
    + "/test_mock_data/unsorted_assistant_configuration_v2.json"
)

_SORTED_ASSISTANT = {
    "name": "tch_password_reset",
    "channel": "VOICE",
    "skills": (
        {
            "skill_id": "password_reset",
            "skill_instance_name": "password_reset",
            "configuration": [
                {
                    "key": "04578122-6912-4aa7-ad6e-0b5457e04965",
                    "type": "PHONE",
                    "configuration": {"type": "FROM_CONSTANT", "value": "+15416928738"},
                },
                {
                    "key": "183ef8e7-1bb2-4bb8-b37c-69b9e456d690",
                    "type": "TEXT",
                    "configuration": {
                        "type": "FROM_CONSTANT",
                        "value": "password_reset",
                    },
                },
                {
                    "key": "25d28a8b-89ec-441a-8f4d-04de34ccbeba",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": "I will send a text to {data}. Is this number correct?",
                            "suggestions": [],
                        },
                    },
                },
                {
                    "key": "30428dc3-1a09-4374-906d-cc9a4b9ee958",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": '"This is The Christ Hospital Virtual Assistant. Here is a link to the MyChart Username recovery page: https://www.thechristhospitalmychart.com/MyChart/recoverlogin.asp \nHere is a link to the MyChart password reset page: https://www.thechristhospitalmychart.com/MyChart/passwordreset.asp"',
                            "suggestions": [],
                        },
                    },
                },
                {
                    "key": "436ea384-69c7-4123-9cf2-cee3f676cf52",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": "Please say either yes, or no. May I text you the link you need in order to reset your password?",
                            "suggestions": [],
                        },
                    },
                },
                {
                    "key": "6367fee1-a2ad-4bc5-ba34-3714af068574",
                    "type": "INTEGRATION",
                    "configuration": {
                        "type": "FROM_CONSTANT",
                        "value": "67326bab-5503-41bb-bcec-9b3130661907",
                    },
                },
                {
                    "key": "70ce7b62-2271-4d23-9f2b-a27d7b53089b",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": "I just sent the link to reset your password or username.",
                            "suggestions": [],
                        },
                    },
                },
                {
                    "key": "744943be-7e92-4e5d-995a-91a880e2ba6a",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": "Sorry, I didn’t get that.",
                            "suggestions": [],
                        },
                    },
                },
                {
                    "key": "86005140-b35f-4d53-a8fa-1ab8e3a1984a",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": "Is this the number I should send the text message?",
                            "suggestions": [],
                        },
                    },
                },
                {
                    "key": "a056983e-a884-4ace-9c14-6186f89aaec8",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": "May I text you the link you need to reset your username or password?",
                            "suggestions": [],
                        },
                    },
                },
                {
                    "key": "a7210316-6089-4bd0-82f7-07cdf11b3ba5",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": "Can you please slowly repeat your phone number?",
                            "suggestions": [],
                        },
                    },
                },
                {
                    "key": "ade9cae4-999e-4027-ba48-f711bc92a2f4",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": "Please say the mobile phone number we should text. Please say the full number including the area code.",
                            "suggestions": [],
                        },
                    },
                },
                {
                    "key": "feb5aca8-f32f-4ada-821c-be8e8afc8155",
                    "type": "SINGLE_OPTION",
                    "configuration": [
                        {
                            "selected_option": "transfer_to_agent",
                            "selected_option_configuration": [
                                {
                                    "key": "13ae35af-0e5b-4f84-9e97-9d981274afbf",
                                    "type": "PHONE",
                                    "configuration": {
                                        "type": "FROM_CONSTANT",
                                        "value": "+15134934886",
                                    },
                                },
                                {
                                    "key": "df4c7da9-d22e-41ad-8a87-9167454795a1",
                                    "type": "ACTION",
                                    "configuration": {
                                        "ENGLISH": {
                                            "text": "Alright, I am transferring you to a live agent for further assistance.",
                                            "suggestions": [],
                                        },
                                    },
                                },
                                {
                                    "key": "e6eeb0e4-69be-4d11-a9a1-b055a8dccdbd",
                                    "type": "TEXT",
                                    "configuration": {
                                        "type": "FROM_CONSTANT",
                                        "value": "agent",
                                    },
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    "base_skill": {
        "skill_id": "voice_essentials",
        "skill_instance_name": "voice_essentials_skill",
        "configuration": [
            {
                "key": "1a74c64a-6a92-4cf6-84ca-6f0e5a026c05",
                "type": "SINGLE_OPTION",
                "configuration": [
                    {
                        "selected_option": "hang_up",
                        "selected_option_configuration": [
                            {
                                "key": "aa366772-5433-4d22-afd0-f183c6e46b09",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {
                                        "text": "Thank you for calling The Christ Hospital, and have a nice day.",
                                        "suggestions": [],
                                    },
                                },
                            },
                        ],
                    },
                ],
            },
            {
                "key": "3a1c93ee-9753-41eb-a46d-d5b22c0858c4",
                "type": "SINGLE_OPTION",
                "configuration": [
                    {
                        "selected_option": "transfer",
                        "selected_option_configuration": [
                            {
                                "key": "4a65eb65-7e64-472a-bcdc-ba023220a008",
                                "type": "PHONE",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "+15134934886",
                                },
                            },
                            {
                                "key": "23d6c324-902a-45b1-a6b6-b350c3f6da1d",
                                "type": "TEXT",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "agent",
                                },
                            },
                            {
                                "key": "e3bbd1e3-9a0a-4ad2-b8a9-100e51547147",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {
                                        "text": "Alright, I am transferring you to a live agent for further assistance.",
                                        "suggestions": [],
                                    },
                                },
                            },
                        ],
                    },
                ],
            },
            {
                "key": "5372ea25-2f94-44a3-a345-3b3308c01c0e",
                "type": "SINGLE_OPTION",
                "configuration": [
                    {
                        "selected_option": "do_nothing",
                        "selected_option_configuration": [],
                    },
                ],
            },
            {
                "key": "850b8ec3-0fc4-45ce-8a5c-ebf3a493bd1a",
                "type": "ACTION",
                "configuration": {
                    "ENGLISH": {
                        "text": "I didn't quite hear you, can you say it again?",
                        "suggestions": [],
                    },
                },
            },
            {
                "key": "8da75cac-30e7-4396-bad1-2fc5eca2588a",
                "type": "ACTION",
                "configuration": {
                    "ENGLISH": {
                        "text": "Let's pick up where we left off.",
                        "suggestions": [],
                    },
                },
            },
            {
                "key": "bcacf2ce-7773-45bd-bd00-6eaadadf811a",
                "type": "ACTION",
                "configuration": {
                    "ENGLISH": {
                        "text": "Hello, I am The Christ Hospital’s virtual assistant. I can help you with resetting your password or username.",
                        "suggestions": [],
                    },
                },
            },
            {
                "key": "fa3fd2ca-b40b-4ca4-bf47-e64b061b18d6",
                "type": "SINGLE_OPTION",
                "configuration": [
                    {
                        "selected_option": "transfer",
                        "selected_option_configuration": [
                            {
                                "key": "0d9ca9e4-ef22-4e42-a37b-0cc6295e8ced",
                                "type": "TEXT",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "agent",
                                },
                            },
                            {
                                "key": "39331999-6113-4fd7-a961-4907dd277e0e",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {
                                        "text": "Sorry, I have difficulties hearing you. Let me transfer you to a representative.",
                                        "suggestions": [],
                                    },
                                },
                            },
                            {
                                "key": "d79ddc7d-a362-4b89-9909-e28858caf36c",
                                "type": "PHONE",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "+15134934886",
                                },
                            },
                        ],
                    },
                ],
            },
        ],
    },
    "selected_languages": ["ENGLISH"],
}

_SORTED_ASSISTANT_V2 = {
    "name": "demo_codeless_assistant",
    "channel": "VOICE",
    "skills": (
        {
            "skill_id": "password_reset",
            "skill_instance_name": "skill_password_reset",
            "configuration": {
                "key": "8a3526f9-129b-484f-8f2e-0c10965474ac",
                "type": "OBJECT",
                "configuration": [
                    {
                        "key": "04578122-6912-4aa7-ad6e-0b5457e04965",
                        "type": "PHONE",
                        "configuration": {
                            "type": "FROM_CONSTANT",
                            "value": "+15416928738",
                        },
                    },
                    {
                        "key": "183ef8e7-1bb2-4bb8-b37c-69b9e456d690",
                        "type": "TEXT",
                        "configuration": {
                            "type": "FROM_CONSTANT",
                            "value": "password_reset",
                        },
                    },
                    {
                        "key": "25d28a8b-89ec-441a-8f4d-04de34ccbeba",
                        "type": "ACTION",
                        "configuration": {
                            "ENGLISH": {
                                "text": "The phone number I’ve heard is {data}, is that correct?",
                            },
                        },
                    },
                    {
                        "key": "30428dc3-1a09-4374-906d-cc9a4b9ee958",
                        "type": "ACTION",
                        "configuration": {
                            "ENGLISH": {
                                "text": "Thank you for calling Hyro Health, here is the link.",
                            },
                        },
                    },
                    {
                        "key": "436ea384-69c7-4123-9cf2-cee3f676cf52",
                        "type": "ACTION",
                        "configuration": {
                            "ENGLISH": {"text": "Please say either yes or no."},
                        },
                    },
                    {
                        "key": "6367fee1-a2ad-4bc5-ba34-3714af068574",
                        "type": "INTEGRATION",
                        "configuration": {
                            "type": "FROM_CONSTANT",
                            "value": "67326bab-5503-41bb-bcec-9b3130661907",
                        },
                    },
                    {
                        "key": "70ce7b62-2271-4d23-9f2b-a27d7b53089b",
                        "type": "ACTION",
                        "configuration": {
                            "ENGLISH": {
                                "text": "Got it, I've just sent you the link that contains everything you need.",
                            },
                        },
                    },
                    {
                        "key": "744943be-7e92-4e5d-995a-91a880e2ba6a",
                        "type": "ACTION",
                        "configuration": {
                            "ENGLISH": {"text": "I didn’t quite catch that."},
                        },
                    },
                    {
                        "key": "86005140-b35f-4d53-a8fa-1ab8e3a1984a",
                        "type": "ACTION",
                        "configuration": {
                            "ENGLISH": {
                                "text": "Should I send the message to the number you are currently calling from?",
                            },
                        },
                    },
                    {
                        "key": "a056983e-a884-4ace-9c14-6186f89aaec8",
                        "type": "ACTION",
                        "configuration": {
                            "ENGLISH": {
                                "text": "I can help you to reset your username and password. May I text you the link you need?",
                            },
                        },
                    },
                    {
                        "key": "a7210316-6089-4bd0-82f7-07cdf11b3ba5",
                        "type": "ACTION",
                        "configuration": {
                            "ENGLISH": {
                                "text": "Could you please slowly repeat your phone number?",
                            },
                        },
                    },
                    {
                        "key": "ade9cae4-999e-4027-ba48-f711bc92a2f4",
                        "type": "ACTION",
                        "configuration": {
                            "ENGLISH": {
                                "text": "Please say the phone number we should reach you at. Please provide your full phone number, including area code.",
                            },
                        },
                    },
                    {
                        "key": "feb5aca8-f32f-4ada-821c-be8e8afc8155",
                        "type": "CHOOSE_ONE",
                        "configuration": {
                            "key": "1fc02f66-3c28-4696-bec8-d5f61c31be07",
                            "type": "ACTION",
                            "configuration": {"ENGLISH": {"text": ""}},
                        },
                    },
                ],
            },
        },
    ),
    "base_skill": {
        "skill_id": "voice_essentials",
        "skill_instance_name": "voice_essentials_skill",
        "configuration": {
            "key": "f538ddd3-e2dd-461e-bb36-b3a4e0ed3475",
            "type": "OBJECT",
            "configuration": [
                {
                    "key": "1a74c64a-6a92-4cf6-84ca-6f0e5a026c05",
                    "type": "CHOOSE_ONE",
                    "configuration": {
                        "key": "4019a832-f897-4016-a845-132835862c1c",
                        "type": "OBJECT",
                        "configuration": [
                            {
                                "key": "58ee518b-a976-4770-b6b4-1387926a5d4d",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {
                                        "text": "Alright, what else do you need help with?",
                                    },
                                },
                            },
                            {
                                "key": "61b1b897-7715-4c8e-8b69-b9ad1c736c98",
                                "type": "TEXT",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "agent",
                                },
                            },
                            {
                                "key": "744943be-7e92-4e5d-995a-91a880e2ba6a",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {"text": "I didn’t quite catch that."},
                                },
                            },
                            {
                                "key": "7e6d02c3-6d60-470e-aef2-da4bdd0cb435",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {
                                        "text": "Ok, I'm transferring you to a live agent.",
                                    },
                                },
                            },
                            {
                                "key": "80565967-3f0e-495b-8267-67cb927bc9f0",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {"text": "Ok, have a nice day."},
                                },
                            },
                            {
                                "key": "ac0fd38d-d477-4974-a010-3c61bda03d8c",
                                "type": "PHONE",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "+1234567891",
                                },
                            },
                            {
                                "key": "c5e5a54e-5d55-44b4-8f94-bccf4b844a74",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {
                                        "text": "Is there anything else you need help with?",
                                    },
                                },
                            },
                        ],
                    },
                },
                {
                    "key": "3a1c93ee-9753-41eb-a46d-d5b22c0858c4",
                    "type": "CHOOSE_ONE",
                    "configuration": {
                        "key": "1c1d6358-0b3f-4b8e-ad76-78cc308c8ea4",
                        "type": "OBJECT",
                        "configuration": [
                            {
                                "key": "23d6c324-902a-45b1-a6b6-b350c3f6da1d",
                                "type": "TEXT",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "agent",
                                },
                            },
                            {
                                "key": "4a65eb65-7e64-472a-bcdc-ba023220a008",
                                "type": "PHONE",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "+1234567891",
                                },
                            },
                            {
                                "key": "e3bbd1e3-9a0a-4ad2-b8a9-100e51547147",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {
                                        "text": "Ok, I'm transferring you to a live agent.",
                                    },
                                },
                            },
                        ],
                    },
                },
                {
                    "key": "5372ea25-2f94-44a3-a345-3b3308c01c0e",
                    "type": "CHOOSE_ONE",
                    "configuration": {
                        "key": "9e219c73-1971-454f-8898-5f912ae91726",
                        "type": "OBJECT",
                        "configuration": [],
                    },
                },
                {
                    "key": "850b8ec3-0fc4-45ce-8a5c-ebf3a493bd1a",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {
                            "text": "I didn't quite hear you, can you say it again?",
                        },
                    },
                },
                {
                    "key": "8da75cac-30e7-4396-bad1-2fc5eca2588a",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {"text": "Let's pick up where we left off."},
                    },
                },
                {
                    "key": "bcacf2ce-7773-45bd-bd00-6eaadadf811a",
                    "type": "ACTION",
                    "configuration": {
                        "ENGLISH": {"text": "Hello, I’m an AI assistant."},
                    },
                },
                {
                    "key": "fa3fd2ca-b40b-4ca4-bf47-e64b061b18d6",
                    "type": "CHOOSE_ONE",
                    "configuration": {
                        "key": "844d17b9-7d23-4194-b5bd-647df8884eb5",
                        "type": "OBJECT",
                        "configuration": [
                            {
                                "key": "0d9ca9e4-ef22-4e42-a37b-0cc6295e8ced",
                                "type": "TEXT",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "agent",
                                },
                            },
                            {
                                "key": "39331999-6113-4fd7-a961-4907dd277e0e",
                                "type": "ACTION",
                                "configuration": {
                                    "ENGLISH": {
                                        "text": "Ok, I'm transferring you to a live agent.",
                                    },
                                },
                            },
                            {
                                "key": "d79ddc7d-a362-4b89-9909-e28858caf36c",
                                "type": "PHONE",
                                "configuration": {
                                    "type": "FROM_CONSTANT",
                                    "value": "+1234567891",
                                },
                            },
                        ],
                    },
                },
            ],
        },
    },
    "languages": [{"language": "ENGLISH", "isDefault": True}],
    "version": "V2",
}


@pytest.mark.parametrize(
    ("version", "assistant_path", "sorted_assistant"),
    [
        pytest.param("V1", _UNSORTED_ASSISTANT_FILE_PATH, _SORTED_ASSISTANT, id="v1"),
        pytest.param(
            "V2",
            _UNSORTED_ASSISTANT_V2_FILE_PATH,
            _SORTED_ASSISTANT_V2,
            id="v2",
        ),
    ],
)
def test_assistant_json_formatter(
    version: str,
    assistant_path: str,
    sorted_assistant: dict,
):
    assistant_dict = json.load(open(assistant_path, "r"))
    if version == "V1":
        content_after_format = (
            format_assistant_configuration.sort_assistant_configurations_v1(
                assistant_dict,
            )
        )
    else:
        content_after_format = (
            format_assistant_configuration.sort_assistant_configurations_v2(
                assistant_dict,
            )
        )

    assert sorted_assistant == content_after_format
