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


def copy_node(node: Node) -> Node:
    """Создаёт независимую копию узла со всем содержимым."""
    clone = Node(node.name, node.is_dir, content=node.content)
    for child in node.children.values():
        child_clone = copy_node(child)
        child_clone.parent = clone
        clone.children[child.name] = child_clone
    return clone


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

    def resolve_parent(self, path: str) -> tuple[Node, str]:
        """Возвращает папку-родителя и имя последнего элемента пути."""
        clean = path.rstrip("/")
        head, _, name = clean.rpartition("/")
        if not name:
            raise VfsError(f"{path}: invalid path")
        parent = self.resolve(head) if "/" in clean else self.cwd
        if not parent.is_dir:
            raise VfsError(f"{path}: not a directory")
        return parent, name

    def target(self, path: str, name: str) -> tuple[Node, str]:
        """Определяет папку и имя, под которым появится узел."""
        try:
            node = self.resolve(path)
        except VfsError:
            return self.resolve_parent(path)
        if node.is_dir:
            return node, name
        return node.parent, node.name

    def attach(self, node: Node, parent: Node, name: str) -> None:
        """Помещает узел в папку под указанным именем."""
        node.name = name
        node.parent = parent
        parent.children[name] = node

    def detach(self, node: Node) -> None:
        """Убирает узел из его папки."""
        if node.parent is not None:
            del node.parent.children[node.name]

    def is_inside(self, node: Node, other: Node) -> bool:
        """Проверяет, лежит ли узел внутри другого узла."""
        current: Node | None = node
        while current is not None:
            if current is other:
                return True
            current = current.parent
        return False

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
