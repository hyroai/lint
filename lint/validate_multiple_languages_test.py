import ast

import gamla
from lint import validate_multiple_languages


def test_valid_cases():
    """Test cases where both EN and ES languages are properly defined."""
    valid_cases = [
        # Basic configurable action with both languages
        """
THANKS_CONFIGURABLE_ACTION = configurable_cg.action(
            key="...",
            default_action=gamla.frozendict(
                {
                    configuration.Language.EN: bot_action.Action("You're welcome!"),
                    configuration.Language.ES: bot_action.Action("Con gusto!"),
                }
            ),
        )
""",

        # Legacy key action with both languages
        """
_SENDING_SMS_FAILED_ACTION_CONFIGURABLE = configurable_cg.action_with_legacy_key(
            "...",
            gamla.frozendict(
                {
                    configuration.Language.EN: bot_action.Action("I wasn't able to verify your code."),
                    configuration.Language.ES: bot_action.Action("No pude verificar su código."),
                }
            ),
        )
""",

        # Action with positional arguments and both languages
        """
CONFIRM_ACTION = configurable_cg.action(
            "confirm-action",
            "Confirm Action",
            gamla.frozendict(
                {
                    configuration.Language.EN: bot_action.Action("Do you confirm?"),
                    configuration.Language.ES: bot_action.Action("¿Confirmas?"),
                }
            ),
            "Confirmation prompt",
            False,
        )
"""

    ]

    for valid_case in valid_cases:
        gamla.pipe(
            valid_case,
            ast.parse,
            validate_multiple_languages.detect,
            gamla.check(gamla.complement(gamla.count), AssertionError),
        )


def test_invalid_cases():
    """Test cases where language support is incomplete or incorrect."""
    invalid_cases = [
        # Missing ES language
        """
THANKS_CONFIGURABLE_ACTION = configurable_cg.action(
            key="...",
            default_action=gamla.frozendict(
                {
                    configuration.Language.EN: bot_action.Action("You're welcome!")
                }
            ),
        )
""",

        # Missing EN language
        """
THANKS_CONFIGURABLE_ACTION = configurable_cg.action(
            key="...",
            default_action=gamla.frozendict(
                {
                    configuration.Language.ES: bot_action.Action("¡Con gusto!")
                }
            ),
        )
""",

        # Legacy key action missing ES
        """
_SENDING_SMS_FAILED_ACTION_CONFIGURABLE = configurable_cg.action_with_legacy_key(
            "...",
            gamla.frozendict(
                {
                    configuration.Language.EN: bot_action.Action("I wasn't able to verify your code.")
                }
            ),
        )
""",

        # Incorrect language key names
        """
CONFIRM_ACTION = configurable_cg.action(
            key="confirm",
            default_action=gamla.frozendict(
                {
                    configuration.Language.ENGLISH: bot_action.Action("Confirm?"),
                    configuration.Language.SPANISH: bot_action.Action("¿Confirmar?"),
                }
            ),
        )
"""
    ]

    for invalid_case in invalid_cases:
        gamla.pipe(
            invalid_case,
            ast.parse,
            validate_multiple_languages.detect,
            gamla.check(gamla.count, AssertionError),
        )


def test_non_configurable_actions():
    """Test that non-configurable actions are ignored."""
    non_configurable_cases = [
        # Regular dictionary with language keys
        """
regular_dict = {
            configuration.Language.EN: "English",
            configuration.Language.ES: "Spanish",
        }
""",

        # gamla.frozendict outside of configurable action
        """
other_dict = gamla.frozendict({
            configuration.Language.EN: "English",
        })
""",

        # Regular function call
        """
some_function(
            gamla.frozendict({
                configuration.Language.EN: "English"
            })
        )
"""
    ]

    for case in non_configurable_cases:
        gamla.pipe(
            case,
            ast.parse,
            validate_multiple_languages.detect,
            gamla.check(gamla.complement(gamla.count), AssertionError),
        )


def test_complex_cases():
    complex_cases = [
        # Multiple configurable actions in one file
        """
ACTION1 = configurable_cg.action(
            key="action1",
            default_action=gamla.frozendict({
                configuration.Language.EN: bot_action.Action("First action"),
                configuration.Language.ES: bot_action.Action("Primera acción"),
            })
        )

ACTION2 = configurable_cg.action(
            key="action2",
            default_action=gamla.frozendict({
                configuration.Language.EN: bot_action.Action("Second action"),
                configuration.Language.ES: bot_action.Action("Segunda acción"),
            })
        )
""",

        # Configurable action with string interpolation
        """
INTERPOLATED_ACTION = configurable_cg.action(
            key="interpolated",
            default_action=gamla.frozendict({
                configuration.Language.EN: bot_action.Action("Hello, {name}!"),
                configuration.Language.ES: bot_action.Action("¡Hola, {name}!"),
            })
        )
"""
    ]

    for case in complex_cases:
        gamla.pipe(
            case,
            ast.parse,
            validate_multiple_languages.detect,
            gamla.check(gamla.complement(gamla.count), AssertionError),
        )