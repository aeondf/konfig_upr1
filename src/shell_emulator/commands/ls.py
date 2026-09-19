"""Команда ls."""

from shell_emulator.commands.base import BaseCommand


class LsCommand(BaseCommand):
    """Заглушка: выводит имя команды и аргументы."""

    def __init__(self) -> None:
        """Создаёт команду ls."""
        super().__init__("ls")

    def run(self, shell, args: list[str]) -> str:
        """Возвращает имя команды и список аргументов."""
        return f"{self.name}: {args}"
