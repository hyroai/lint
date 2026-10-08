import subprocess
import textwrap

from lint.broad_except import find_broad_handlers, main


def _findings(source: str) -> list[tuple[int, str]]:
    source = textwrap.dedent(source)
    return find_broad_handlers(source, set(range(1, len(source.splitlines()) + 1)))


def _find_all(source: str) -> list[int]:
    return [lineno for lineno, _ in _findings(source)]


def test_except_exception_flagged():
    assert _find_all("""
        try:
            fetch()
        except Exception:
            pass
    """) == [4]


def test_except_exception_as_flagged():
    assert _find_all("""
        try:
            fetch()
        except Exception as e:
            log(e)
    """) == [4]


def test_bare_except_flagged():
    assert _find_all("""
        try:
            fetch()
        except:
            pass
    """) == [4]


def test_base_exception_flagged():
    assert _find_all("""
        try:
            fetch()
        except BaseException:
            pass
    """) == [4]


def test_broad_in_tuple_flagged():
    assert _find_all("""
        try:
            fetch()
        except (ValueError, Exception):
            pass
    """) == [4]


def test_builtins_exception_flagged():
    assert _find_all("""
        try:
            fetch()
        except builtins.Exception:
            pass
    """) == [4]


def test_except_star_flagged():
    assert _find_all("""
        try:
            fetch()
        except* Exception:
            pass
    """) == [4]


def test_specific_exception_allowed():
    assert _find_all("""
        try:
            fetch()
        except TimeoutError:
            return None
        except (KeyError, ValueError) as e:
            log(e)
    """) == []


def test_bare_reraise_allowed():
    assert _find_all("""
        try:
            fetch()
        except Exception:
            metrics.inc("fetch_failed")
            raise
    """) == []


def test_reraise_caught_name_allowed():
    assert _find_all("""
        try:
            fetch()
        except Exception as e:
            cleanup()
            raise e
    """) == []


def test_raise_from_caught_allowed():
    assert _find_all("""
        try:
            fetch()
        except Exception as e:
            raise FetchError("fetch failed") from e
    """) == []


def test_raise_unrelated_exception_flagged():
    assert _find_all("""
        try:
            fetch()
        except Exception:
            raise FetchError("fetch failed")
    """) == [4]


def test_raise_inside_nested_function_flagged():
    assert _find_all("""
        try:
            fetch()
        except Exception:
            def later():
                raise
    """) == [4]


def test_noqa_with_reason_allowed():
    assert _find_all("""
        try:
            fetch()
        except Exception:  # noqa: BLE001 - request boundary, must return 500
            pass
    """) == []


def test_noqa_with_reason_among_other_codes_allowed():
    assert _find_all("""
        try:
            fetch()
        except Exception:  # noqa: T201, BLE001 API boundary
            pass
    """) == []


def test_noqa_without_reason_flagged():
    findings = _findings("""
        try:
            fetch()
        except Exception:  # noqa: BLE001
            pass
    """)
    assert [lineno for lineno, _ in findings] == [4]
    assert "needs a reason" in findings[0][1]


def test_noqa_with_only_punctuation_flagged():
    assert _find_all("""
        try:
            fetch()
        except Exception:  # noqa: BLE001 -
            pass
    """) == [4]


def test_noqa_for_other_code_flagged():
    assert _find_all("""
        try:
            fetch()
        except Exception:  # noqa: E722 - legacy
            pass
    """) == [4]


def test_only_added_lines_checked():
    source = textwrap.dedent("""
        try:
            fetch()
        except Exception:
            pass
        try:
            fetch()
        except Exception:
            pass
    """)
    assert [lineno for lineno, _ in find_broad_handlers(source, {8, 9})] == [8]


def test_syntax_error_ignored():
    assert _find_all("except Exception:\n") == []


def _git(*args):
    subprocess.run(["git", *args], check=True, capture_output=True)


def _repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _git("init", "-q")
    _git("config", "user.email", "test@example.com")
    _git("config", "user.name", "test")
    (tmp_path / "old.py").write_text("try:\n    f()\nexcept Exception:\n    pass\n")
    _git("add", ".")
    _git("commit", "-qm", "init")


def test_main_grandfathers_existing_handlers(tmp_path, monkeypatch):
    _repo(tmp_path, monkeypatch)
    (tmp_path / "old.py").write_text(
        "x = 1\ntry:\n    f()\nexcept Exception:\n    pass\n",
    )
    _git("add", ".")
    assert main(["old.py"]) == 0


def test_main_fails_on_added_handler(tmp_path, monkeypatch, capsys):
    _repo(tmp_path, monkeypatch)
    (tmp_path / "new.py").write_text("try:\n    f()\nexcept:\n    pass\n")
    _git("add", ".")
    assert main(["new.py"]) == 1
    assert "new.py:3: broad exception handler" in capsys.readouterr().out


def test_main_skips_test_files(tmp_path, monkeypatch):
    _repo(tmp_path, monkeypatch)
    (tmp_path / "new_test.py").write_text(
        "try:\n    f()\nexcept Exception:\n    pass\n",
    )
    _git("add", ".")
    assert main(["new_test.py"]) == 0
