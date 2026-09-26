"""Тесты оболочки."""

import pytest

from shell_emulator.commands import CommandError
from shell_emulator.shell import Shell
from shell_emulator.vfs import VFS

EXIT_CODE = 3


def test_prompt() -> None:
    """Приглашение содержит имя VFS."""
    assert Shell(VFS("rootfs")).prompt == "rootfs:/$ "


def test_empty_vfs_has_no_files() -> None:
    """Без загрузки VFS корень пуст."""
    assert Shell().execute("ls") == ""


def test_empty_line() -> None:
    """Пустая строка ничего не делает."""
    assert Shell().execute("  ") == ""


def test_unknown_command() -> None:
    """Неизвестная команда — ошибка."""
    with pytest.raises(CommandError):
        Shell().execute("foo bar")


def test_exit() -> None:
    """Команда exit останавливает оболочку с заданным кодом."""
    shell = Shell()
    shell.execute(f"exit {EXIT_CODE}")
    assert shell.running is False
    assert shell.exit_code == EXIT_CODE


def test_exit_default_code() -> None:
    """Команда exit без аргумента возвращает код 0."""
    shell = Shell()
    shell.execute("exit")
    assert shell.exit_code == 0


def test_exit_bad_arg() -> None:
    """Нечисловой аргумент exit — ошибка, оболочка продолжает работу."""
    shell = Shell()
    with pytest.raises(CommandError):
        shell.execute("exit abc")
    assert shell.running is True


def test_exit_too_many_args() -> None:
    """Лишние аргументы exit — ошибка."""
    with pytest.raises(CommandError):
        Shell().execute("exit 1 2")
