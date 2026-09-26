"""Команда uptime."""

import time

from shell_emulator.commands.base import BaseCommand
from shell_emulator.core.constants import MINUTES_IN_HOUR, SECONDS_IN_MINUTE


class UptimeCommand(BaseCommand):
    """Показывает время работы эмулятора."""

    def __init__(self) -> None:
        """Создаёт команду uptime и запоминает момент запуска."""
        super().__init__("uptime")
        self.started = time.monotonic()

    def run(self, shell, args: list[str]) -> str:
        """Выводит текущее время и время с момента запуска."""
        total = int(time.monotonic() - self.started)
        minutes = total // SECONDS_IN_MINUTE
        hours = minutes // MINUTES_IN_HOUR
        now = time.strftime("%H:%M:%S")
        return (
            f"{now} up {hours:02d}:{minutes % MINUTES_IN_HOUR:02d}:"
            f"{total % SECONDS_IN_MINUTE:02d}"
        )
