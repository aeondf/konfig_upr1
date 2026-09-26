"""Тесты выполнения стартового скрипта."""

from pathlib import Path

import pytest

from shell_emulator.shell import Shell
from shell_emulator.vfs import VFS

DEEP = Path("vfs/deep")
EXIT_CODE = 7


def write_script(tmp_path: Path, text: str) -> str:
    """Сохраняет текст скрипта во временный файл и возвращает путь."""
    path = tmp_path / "start.txt"
    path.write_text(text)
    return str(path)


def make_shell() -> Shell:
    """Оболочка с загруженной VFS vfs/deep."""
    vfs = VFS()
    vfs.load(DEEP)
    return Shell(vfs)


def test_input_and_output_are_shown(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Каждая команда печатается с приглашением, потом её результат."""
    path = write_script(tmp_path, "ls\ncd docs\n")
    make_shell().run_script(path)
    assert capsys.readouterr().out == (
        "deep:/$ ls\ndocs\nreadme.md\nsrc\ndeep:/$ cd docs\n"
    )


def test_comments_and_blank_lines_skipped(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Строки с # и пустые строки не выполняются и не печатаются."""
    path = write_script(tmp_path, "# comment\n\n   \nuname\n# another\n")
    make_shell().run_script(path)
    assert capsys.readouterr().out == "deep:/$ uname\nShellEmulator\n"


def test_errors_do_not_stop_script(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Ошибка печатается, следующие команды выполняются."""
    path = write_script(tmp_path, "foo\nuname\n")
    make_shell().run_script(path)
    out = capsys.readouterr().out
    assert "foo: command not found" in out
    assert "ShellEmulator" in out


def test_exit_stops_script(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """После exit оставшиеся строки не выполняются."""
    path = write_script(tmp_path, f"exit {EXIT_CODE}\nuname\n")
    shell = make_shell()
    shell.run_script(path)
    assert shell.running is False
    assert shell.exit_code == EXIT_CODE
    assert "ShellEmulator" not in capsys.readouterr().out


def test_missing_file(tmp_path: Path) -> None:
    """Несуществующий файл — FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        make_shell().run_script(str(tmp_path / "nope.txt"))
