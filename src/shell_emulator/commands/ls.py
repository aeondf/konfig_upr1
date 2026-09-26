"""Команда ls."""

from shell_emulator.commands.base import BaseCommand
from shell_emulator.commands.error import CommandError
from shell_emulator.vfs import VfsError


class LsCommand(BaseCommand):
    """Показывает содержимое папки VFS."""

    def __init__(self) -> None:
        """Создаёт команду ls."""
        super().__init__("ls")

    def run(self, shell, args: list[str]) -> str:
        """Возвращает имена файлов и папок по указанному пути."""
        path = args[0] if args else "."
        try:
            node = shell.vfs.resolve(path)
        except VfsError as error:
            raise CommandError(f"ls: {error}") from None
        if not node.is_dir:
            return node.name
        return "\n".join(sorted(node.children))
