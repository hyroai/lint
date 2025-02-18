import gamla
from lint import validate_multiple_languages


def test_valid_cases():
    for valid_case in [
        """THANKS_CONFIGURABLE_ACTION = configurable_cg.action(
            key="...",
            default_action=gamla.frozendict(
                {
                    configuration.Language.EN: bot_action.Action("You're welcome!"),
                    configuration.Language.ES: bot_action.Action("Con gusto!"),
                }
            ),
        )""",
        """_SENDING_SMS_FAILED_ACTION_CONFIGURABLE = configurable_cg.action_with_legacy_key(
            "...",
            gamla.frozendict(
                {
                    configuration.Language.EN: bot_action.Action("I wasn't able to verify your code."),
                    configuration.Language.ES: bot_action.Action("No pude verificar su código."),
                }
            ),
        )"""
    ]:
        gamla.pipe(
            valid_case,
            validate_multiple_languages.detect,
            gamla.check(gamla.complement(gamla.count), AssertionError))


def test_invalid_cases():
    for invalid_case in [
        """THANKS_CONFIGURABLE_ACTION = configurable_cg.action(
            key="...",
            default_action=gamla.frozendict(
                {
                    configuration.Language.EN: bot_action.Action("You're welcome!")
                }
            ),
        )""",
        """_SENDING_SMS_FAILED_ACTION_CONFIGURABLE = configurable_cg.action_with_legacy_key(
            "...",
            gamla.frozendict(
                {
                    configuration.Language.EN: bot_action.Action("I wasn't able to verify your code.")
                }
            ),
        )"""
    ]:
        gamla.pipe(
            invalid_case,
            validate_multiple_languages.detect,
            gamla.check(gamla.count, AssertionError))
