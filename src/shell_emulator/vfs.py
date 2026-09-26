"""Виртуальная файловая система в памяти."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


class VfsError(Exception):
    """Ошибка работы с виртуальной файловой системой."""


@dataclass
class Node:
    """Папка или файл в памяти."""

    name: str
    is_dir: bool
    parent: Node | None = field(default=None, repr=False)
    children: dict[str, Node] = field(default_factory=dict)
    content: str = ""


class VFS:
    """Дерево папок и файлов, загруженное с диска."""

    def __init__(self, name: str = "vfs") -> None:
        """Создаёт пустую VFS с корнем."""
        self.name = name
        self.root = Node("/", is_dir=True)
        self.cwd = self.root

    def load(self, path: Path) -> None:
        """Читает папку с диска в память."""
        self.name = path.name
        self._load_dir(path, self.root)

    def _load_dir(self, disk_dir: Path, node: Node) -> None:
        for entry in sorted(disk_dir.iterdir()):
            child = Node(name=entry.name, is_dir=entry.is_dir(), parent=node)
            node.children[entry.name] = child
            if entry.is_dir():
                self._load_dir(entry, child)
            else:
                child.content = entry.read_text(errors="replace")

    def resolve(self, path: str) -> Node:
        """Находит узел по абсолютному или относительному пути."""
        node = self.root if path.startswith("/") else self.cwd
        for part in path.split("/"):
            node = self._step(node, part, path)
        return node

    def _step(self, node: Node, part: str, path: str) -> Node:
        if part in ("", "."):
            return node
        if part == "..":
            return node.parent if node.parent else node
        child = node.children.get(part) if node.is_dir else None
        if child is None:
            raise VfsError(f"{path}: no such file or directory")
        return child

    def path_of(self, node: Node) -> str:
        """Возвращает абсолютный путь узла."""
        parts = []
        while node.parent is not None:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))

    def paths(self) -> list[str]:
        """Возвращает список всех путей в дереве."""
        result: list[str] = []
        self._collect(self.root, "", result)
        return result

    def _collect(self, node: Node, prefix: str, result: list[str]) -> None:
        for child in node.children.values():
            path = f"{prefix}/{child.name}"
            result.append(path)
            self._collect(child, path, result)
