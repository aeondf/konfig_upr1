"""Команда mv."""

from shell_emulator.commands.base import BaseCommand
from shell_emulator.commands.error import CommandError
from shell_emulator.core.constants import MOVE_ARGS
from shell_emulator.vfs import VfsError


class MvCommand(BaseCommand):
    """Переносит или переименовывает узел VFS."""

    def __init__(self) -> None:
        """Создаёт команду mv."""
        super().__init__("mv")

    def run(self, shell, args: list[str]) -> str:
        """Переносит источник в приёмник, меняя только память."""
        if len(args) != MOVE_ARGS:
            raise CommandError("mv: usage: mv source target")
        vfs = shell.vfs
        try:
            source = vfs.resolve(args[0])
            parent, name = vfs.target(args[1], source.name)
        except VfsError as error:
            raise CommandError(f"mv: {error}") from None
        if source.parent is None:
            raise CommandError("mv: cannot move the root directory")
        if source.is_dir and vfs.is_inside(parent, source):
            raise CommandError(f"mv: cannot move {args[0]} into itself")
        vfs.detach(source)
        vfs.attach(source, parent, name)
        return ""
