"""Команда cp."""

from shell_emulator.commands.base import BaseCommand
from shell_emulator.commands.error import CommandError
from shell_emulator.core.constants import (
    MAX_COPY_ARGS,
    MOVE_ARGS,
    RECURSIVE_OPTION,
)
from shell_emulator.vfs import Node, VfsError, copy_node


class CpCommand(BaseCommand):
    """Копирует файл или папку внутри VFS."""

    def __init__(self) -> None:
        """Создаёт команду cp."""
        super().__init__("cp")

    def run(self, shell, args: list[str]) -> str:
        """Копирует источник в приёмник; папки — только с -r."""
        recursive, source_path, target_path = self._parse_args(args)
        vfs = shell.vfs
        try:
            source = vfs.resolve(source_path)
            parent, name = vfs.target(target_path, source.name)
        except VfsError as error:
            raise CommandError(f"cp: {error}") from None
        self._check(vfs, source, parent, name, recursive, source_path)
        vfs.attach(copy_node(source), parent, name)
        return ""

    def _check(
        self,
        vfs,
        source: Node,
        parent: Node,
        name: str,
        recursive: bool,
        path: str,
    ) -> None:
        if source.is_dir and not recursive:
            raise CommandError(f"cp: {path}: is a directory")
        if parent.children.get(name) is source:
            raise CommandError(f"cp: {path}: source and target are the same")
        if source.is_dir and vfs.is_inside(parent, source):
            raise CommandError(f"cp: cannot copy {path} into itself")

    def _parse_args(self, args: list[str]) -> tuple[bool, str, str]:
        recursive = args[0] == RECURSIVE_OPTION if args else False
        rest = args[1:] if recursive else args
        if len(args) > MAX_COPY_ARGS or len(rest) != MOVE_ARGS:
            raise CommandError("cp: usage: cp [-r] source target")
        return recursive, rest[0], rest[1]
