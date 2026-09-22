"""Тесты виртуальной файловой системы."""

from pathlib import Path

from shell_emulator.vfs import VFS

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
