"""Тесты выполнения стартового скрипта."""

from pathlib import Path

import pytest

from shell_emulator.shell import Shell

EXIT_CODE = 7


def write_script(tmp_path: Path, text: str) -> str:
    """Сохраняет текст скрипта во временный файл и возвращает путь."""
    path = tmp_path / "start.txt"
    path.write_text(text)
    return str(path)


def test_input_and_output_are_shown(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Каждая команда печатается с приглашением, потом её результат."""
    path = write_script(tmp_path, 'ls -la\ncd "a b"\n')
    Shell("myfs").run_script(path)
    assert capsys.readouterr().out == (
        "myfs$ ls -la\nls: ['-la']\nmyfs$ cd \"a b\"\ncd: ['a b']\n"
    )


def test_comments_and_blank_lines_skipped(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Строки с # и пустые строки не выполняются и не печатаются."""
    path = write_script(tmp_path, "# comment\n\n   \nls\n# another\n")
    Shell().run_script(path)
    assert capsys.readouterr().out == "vfs$ ls\nls: []\n"


def test_errors_do_not_stop_script(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Ошибка печатается, следующие команды выполняются."""
    path = write_script(tmp_path, "foo\nls\n")
    Shell().run_script(path)
    out = capsys.readouterr().out
    assert "foo: command not found" in out
    assert "ls: []" in out


def test_exit_stops_script(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """После exit оставшиеся строки не выполняются."""
    path = write_script(tmp_path, f"exit {EXIT_CODE}\nls\n")
    shell = Shell()
    shell.run_script(path)
    assert shell.running is False
    assert shell.exit_code == EXIT_CODE
    assert "ls:" not in capsys.readouterr().out


def test_missing_file(tmp_path: Path) -> None:
    """Несуществующий файл — FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        Shell().run_script(str(tmp_path / "nope.txt"))
