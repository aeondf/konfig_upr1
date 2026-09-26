"""Команда tail."""

from shell_emulator.commands.base import BaseCommand
from shell_emulator.commands.error import CommandError
from shell_emulator.core.constants import (
    DEFAULT_TAIL_LINES,
    MAX_TAIL_ARGS,
    TAIL_OPTION,
)
from shell_emulator.vfs import VfsError


class TailCommand(BaseCommand):
    """Показывает последние строки файла."""

    def __init__(self) -> None:
        """Создаёт команду tail."""
        super().__init__("tail")

    def run(self, shell, args: list[str]) -> str:
        """Выводит последние строки файла, по умолчанию десять."""
        count, path = self._parse_args(args)
        try:
            node = shell.vfs.resolve(path)
        except VfsError as error:
            raise CommandError(f"tail: {error}") from None
        if node.is_dir:
            raise CommandError(f"tail: {path}: is a directory")
        lines = node.content.splitlines()
        return "\n".join(lines[-count:]) if count else ""

    def _parse_args(self, args: list[str]) -> tuple[int, str]:
        if not args or len(args) > MAX_TAIL_ARGS:
            raise CommandError("tail: usage: tail [-n lines] file")
        if args[0] != TAIL_OPTION:
            return DEFAULT_TAIL_LINES, args[0]
        if len(args) != MAX_TAIL_ARGS:
            raise CommandError("tail: usage: tail [-n lines] file")
        if not args[1].isdigit():
            raise CommandError(f"tail: {args[1]}: invalid number of lines")
        return int(args[1]), args[2]
