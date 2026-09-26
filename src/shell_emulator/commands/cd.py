"""Команда cd."""

from shell_emulator.commands.base import BaseCommand
from shell_emulator.commands.error import CommandError
from shell_emulator.vfs import VfsError


class CdCommand(BaseCommand):
    """Меняет текущую папку VFS."""

    def __init__(self) -> None:
        """Создаёт команду cd."""
        super().__init__("cd")

    def run(self, shell, args: list[str]) -> str:
        """Переходит в указанную папку; без аргументов — в корень."""
        path = args[0] if args else "/"
        try:
            node = shell.vfs.resolve(path)
        except VfsError as error:
            raise CommandError(f"cd: {error}") from None
        if not node.is_dir:
            raise CommandError(f"cd: {path}: not a directory")
        shell.vfs.cwd = node
        return ""
