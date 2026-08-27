import gamla

from lint import check_deployment_env_vars

_CHARTS = {
    "service-a": frozenset({"COMMON_VAR", "SERVICE_A_ONLY"}),
    "service-b": frozenset({"COMMON_VAR", "SERVICE_B_ONLY"}),
    "service-c": frozenset({"COMMON_VAR"}),
}

_NO_EXCEPTIONS = {}


def test_no_error_when_var_present_in_all_charts():
    gamla.pipe(
        check_deployment_env_vars.detect(
            {"service-a": frozenset({"COMMON_VAR"})},
            _CHARTS,
            _NO_EXCEPTIONS,
        ),
        gamla.assert_that(gamla.empty),
    )


def test_error_when_var_missing_from_other_chart():
    gamla.pipe(
        check_deployment_env_vars.detect(
            {"service-a": frozenset({"NEW_VAR"})},
            _CHARTS,
            _NO_EXCEPTIONS,
        ),
        gamla.assert_that(gamla.nonempty),
    )


def test_no_error_when_missing_chart_is_excepted():
    gamla.pipe(
        check_deployment_env_vars.detect(
            {"service-a": frozenset({"NEW_VAR"})},
            _CHARTS,
            {"NEW_VAR": {"service-b": "not needed", "service-c": "not needed"}},
        ),
        gamla.assert_that(gamla.empty),
    )


def test_error_when_only_some_missing_charts_are_excepted():
    gamla.pipe(
        check_deployment_env_vars.detect(
            {"service-a": frozenset({"NEW_VAR"})},
            _CHARTS,
            {"NEW_VAR": {"service-b": "not needed"}},
        ),
        gamla.assert_that(gamla.nonempty),
    )


def test_no_error_when_no_new_vars():
    gamla.pipe(
        check_deployment_env_vars.detect(
            {"service-a": frozenset()},
            _CHARTS,
            _NO_EXCEPTIONS,
        ),
        gamla.assert_that(gamla.empty),
    )


def test_stale_exception_warning_when_var_added_to_excepted_chart():
    gamla.pipe(
        check_deployment_env_vars._stale_exceptions(
            {"service-a": frozenset({"SOME_VAR"})},
            {"SOME_VAR": {"service-a": "not needed"}},
        ),
        gamla.assert_that(gamla.nonempty),
    )


def test_no_stale_exception_when_chart_not_excepted():
    gamla.pipe(
        check_deployment_env_vars._stale_exceptions(
            {"service-a": frozenset({"SOME_VAR"})},
            {"SOME_VAR": {"service-b": "not needed"}},
        ),
        gamla.assert_that(gamla.empty),
    )


def test_vars_from_added_diff_lines_detects_new_var():
    gamla.pipe(
        """\
--- a/deploy/assistant/templates/deployment.yaml
+++ b/deploy/assistant/templates/deployment.yaml
@@ -10,0 +11,2 @@
+            - name: TRITON_RUNTIME_SERVICE
+              value: {{ .Values.tritonRuntimeService }}
""",
        check_deployment_env_vars._vars_from_added_diff_lines,
        gamla.assert_that(gamla.inside("TRITON_RUNTIME_SERVICE")),
    )


def test_vars_from_added_diff_lines_ignores_removed_lines():
    gamla.pipe(
        "-            - name: OLD_VAR\n+            - name: NEW_VAR\n",
        check_deployment_env_vars._vars_from_added_diff_lines,
        gamla.assert_that(gamla.complement(gamla.inside("OLD_VAR"))),
    )