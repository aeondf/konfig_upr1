"""Тесты виртуальной файловой системы."""

from pathlib import Path

import pytest

from shell_emulator.vfs import VFS, VfsError

MINIMAL = Path("vfs/minimal")
FILES = Path("vfs/files")
DEEP = Path("vfs/deep")

FILES_COUNT = 4
DEEP_PATHS_COUNT = 11


def test_empty_vfs() -> None:
    """Без загрузки есть только корень."""
    vfs = VFS()
    assert vfs.name == "vfs"
    assert vfs.root.is_dir is True
    assert vfs.root.children == {}
    assert vfs.cwd is vfs.root


def test_name_from_directory() -> None:
    """Имя VFS берётся из имени папки."""
    vfs = VFS()
    vfs.load(MINIMAL)
    assert vfs.name == "minimal"


def test_minimal_vfs() -> None:
    """Минимальная VFS: один файл с содержимым."""
    vfs = VFS()
    vfs.load(MINIMAL)
    assert vfs.paths() == ["/readme.txt"]
    assert vfs.root.children["readme.txt"].content == "hello\n"


def test_several_files() -> None:
    """VFS из нескольких файлов в корне."""
    vfs = VFS()
    vfs.load(FILES)
    assert len(vfs.paths()) == FILES_COUNT
    assert vfs.root.children["a.txt"].is_dir is False


def test_deep_vfs() -> None:
    """VFS с вложенностью больше трёх уровней."""
    vfs = VFS()
    vfs.load(DEEP)
    paths = vfs.paths()
    assert len(paths) == DEEP_PATHS_COUNT
    assert "/docs/guides/linux/commands.txt" in paths


def test_parent_links() -> None:
    """У каждого узла есть ссылка на родителя."""
    vfs = VFS()
    vfs.load(DEEP)
    docs = vfs.root.children["docs"]
    guides = docs.children["guides"]
    assert docs.parent is vfs.root
    assert guides.parent is docs


def test_disk_is_not_modified() -> None:
    """Загрузка не меняет папку на диске."""
    before = sorted(str(path) for path in DEEP.rglob("*"))
    VFS().load(DEEP)
    assert sorted(str(path) for path in DEEP.rglob("*")) == before


def test_resolve_absolute_and_relative() -> None:
    """Метод resolve понимает абсолютные и относительные пути."""
    vfs = VFS()
    vfs.load(DEEP)
    assert vfs.resolve("/docs/guides").name == "guides"
    assert vfs.resolve("docs").name == "docs"


def test_resolve_dots() -> None:
    """Метод resolve понимает . и .."""
    vfs = VFS()
    vfs.load(DEEP)
    vfs.cwd = vfs.resolve("docs/guides")
    assert vfs.resolve("..").name == "docs"
    assert vfs.resolve("./linux").name == "linux"
    assert vfs.resolve("../..") is vfs.root


def test_resolve_missing() -> None:
    """Несуществующий путь — VfsError."""
    vfs = VFS()
    vfs.load(DEEP)
    with pytest.raises(VfsError):
        vfs.resolve("nope")


def test_path_of() -> None:
    """Метод path_of строит абсолютный путь узла."""
    vfs = VFS()
    vfs.load(DEEP)
    node = vfs.resolve("/docs/guides/linux/commands.txt")
    assert vfs.path_of(node) == "/docs/guides/linux/commands.txt"
    assert vfs.path_of(vfs.root) == "/"
