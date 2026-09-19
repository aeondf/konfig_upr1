"""Команда exit."""

from shell_emulator.commands.base import BaseCommand
from shell_emulator.commands.error import CommandError
from shell_emulator.core.constants import MAX_EXIT_ARGS


class ExitCommand(BaseCommand):
    """Завершает работу оболочки с заданным кодом."""

    def __init__(self) -> None:
        """Создаёт команду exit."""
        super().__init__("exit")

    def run(self, shell, args: list[str]) -> str:
        """Останавливает оболочку; код возврата берётся из аргумента."""
        if len(args) > MAX_EXIT_ARGS:
            raise CommandError("exit: too many arguments")
        code = 0
        if args:
            if not args[0].isdigit():
                raise CommandError(
                    f"exit: {args[0]}: numeric argument required"
                )
            code = int(args[0])
        shell.stop(code)
        return ""
