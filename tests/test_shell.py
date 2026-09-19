"""Тесты оболочки."""

import pytest

from shell_emulator.commands import CommandError
from shell_emulator.shell import Shell

EXIT_CODE = 3


def test_prompt() -> None:
    """Приглашение содержит имя VFS."""
    assert Shell("rootfs").prompt == "rootfs$ "


def test_stub_returns_name_and_args() -> None:
    """Заглушка выводит имя команды и аргументы."""
    assert Shell().execute('ls -la "a b"') == "ls: ['-la', 'a b']"
    assert Shell().execute("cd") == "cd: []"


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
