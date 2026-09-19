"""Команда cd."""

from shell_emulator.commands.base import BaseCommand


class CdCommand(BaseCommand):
    """Заглушка: выводит имя команды и аргументы."""

    def __init__(self) -> None:
        """Создаёт команду cd."""
        super().__init__("cd")

    def run(self, shell, args: list[str]) -> str:
        """Возвращает имя команды и список аргументов."""
        return f"{self.name}: {args}"
