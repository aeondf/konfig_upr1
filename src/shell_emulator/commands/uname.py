"""Команда uname."""

import platform

from shell_emulator.commands.base import BaseCommand

SYSTEM_NAME = "ShellEmulator"
RELEASE = "0.1.0"


class UnameCommand(BaseCommand):
    """Показывает сведения об эмуляторе."""

    def __init__(self) -> None:
        """Создаёт команду uname."""
        super().__init__("uname")

    def run(self, shell, args: list[str]) -> str:
        """Выводит имя системы; с -a — полную строку."""
        if "-a" in args:
            machine = platform.machine()
            return f"{SYSTEM_NAME} {shell.vfs.name} {RELEASE} {machine}"
        return SYSTEM_NAME
