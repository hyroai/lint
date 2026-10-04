import subprocess
import textwrap

from lint.broad_except import find_broad_handlers, main


def _find_all(source: str) -> list[int]:
    source = textwrap.dedent(source)
    return find_broad_handlers(source, set(range(1, len(source.splitlines()) + 1)))


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


def test_noqa_does_not_exempt():
    assert _find_all("""
        try:
            fetch()
        except Exception:  # noqa: BLE001
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
    assert find_broad_handlers(source, {8, 9}) == [8]


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
    assert "new.py:3" in capsys.readouterr().out


def test_main_skips_test_files(tmp_path, monkeypatch):
    _repo(tmp_path, monkeypatch)
    (tmp_path / "new_test.py").write_text(
        "try:\n    f()\nexcept Exception:\n    pass\n",
    )
    _git("add", ".")
    assert main(["new_test.py"]) == 0
