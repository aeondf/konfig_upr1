"""Базовый класс команд."""


class BaseCommand:
    """Общий интерфейс всех команд оболочки."""

    def __init__(self, name: str) -> None:
        """Запоминает имя команды."""
        self.name = name

    def run(self, shell, args: list[str]) -> str:
        """Выполняет команду и возвращает текст для вывода."""
        raise NotImplementedError
