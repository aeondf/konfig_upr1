"""Тесты команд ls, cd, uname, uptime и tail."""

from pathlib import Path

import pytest

from shell_emulator.commands import CommandError
from shell_emulator.shell import Shell
from shell_emulator.vfs import VFS

DEEP = Path("vfs/deep")
TAIL_LINES = 3
LAST_LINE = "12"


@pytest.fixture
def shell() -> Shell:
    """Оболочка с загруженной VFS vfs/deep."""
    vfs = VFS()
    vfs.load(DEEP)
    return Shell(vfs)


def test_ls_root(shell: Shell) -> None:
    """Команда ls без аргументов показывает содержимое текущей папки."""
    assert shell.execute("ls") == "docs\nreadme.md\nsrc"


def test_ls_path(shell: Shell) -> None:
    """Команда ls с путём показывает содержимое указанной папки."""
    assert shell.execute("ls /src/shell") == "shell.py"


def test_ls_file(shell: Shell) -> None:
    """Команда ls на файле показывает его имя."""
    assert shell.execute("ls readme.md") == "readme.md"


def test_ls_missing(shell: Shell) -> None:
    """Команда ls на несуществующем пути — ошибка."""
    with pytest.raises(CommandError, match="no such file"):
        shell.execute("ls nope")


def test_cd_and_prompt(shell: Shell) -> None:
    """Команда cd меняет текущую папку, она видна в приглашении."""
    shell.execute("cd docs/guides")
    assert shell.prompt == "deep:/docs/guides$ "


def test_cd_up(shell: Shell) -> None:
    """Команда cd .. поднимает на уровень выше."""
    shell.execute("cd docs/guides")
    shell.execute("cd ..")
    assert shell.prompt == "deep:/docs$ "


def test_cd_root(shell: Shell) -> None:
    """Команда cd без аргументов возвращает в корень."""
    shell.execute("cd docs")
    shell.execute("cd")
    assert shell.prompt == "deep:/$ "


def test_cd_above_root(shell: Shell) -> None:
    """Из корня выше подняться нельзя."""
    shell.execute("cd ../../..")
    assert shell.prompt == "deep:/$ "


def test_cd_to_file(shell: Shell) -> None:
    """Команда cd на файл — ошибка."""
    with pytest.raises(CommandError, match="not a directory"):
        shell.execute("cd readme.md")


def test_cd_missing(shell: Shell) -> None:
    """Команда cd на несуществующий путь — ошибка."""
    with pytest.raises(CommandError, match="no such file"):
        shell.execute("cd nope")


def test_uname(shell: Shell) -> None:
    """Команда uname выводит имя системы."""
    assert shell.execute("uname") == "ShellEmulator"


def test_uname_all(shell: Shell) -> None:
    """Команда uname -a добавляет имя VFS и версию."""
    output = shell.execute("uname -a")
    assert output.startswith("ShellEmulator deep 0.1.0")


def test_uptime(shell: Shell) -> None:
    """Команда uptime показывает время работы."""
    assert " up " in shell.execute("uptime")


def test_tail_default(shell: Shell) -> None:
    """Команда tail без опций выводит последние десять строк."""
    output = shell.execute("tail /docs/guides/linux/commands.txt")
    assert output.splitlines()[-1] == LAST_LINE
    assert output.startswith("3")


def test_tail_with_count(shell: Shell) -> None:
    """Команда tail -n N выводит N последних строк."""
    output = shell.execute(
        f"tail -n {TAIL_LINES} /docs/guides/linux/commands.txt"
    )
    assert len(output.splitlines()) == TAIL_LINES


def test_tail_short_file(shell: Shell) -> None:
    """Если строк меньше запрошенного, выводится весь файл."""
    assert shell.execute("tail /readme.md") == "Deep VFS root"


def test_tail_directory(shell: Shell) -> None:
    """Команда tail на папке — ошибка."""
    with pytest.raises(CommandError, match="is a directory"):
        shell.execute("tail /docs")


def test_tail_missing_file(shell: Shell) -> None:
    """Команда tail на несуществующем файле — ошибка."""
    with pytest.raises(CommandError, match="no such file"):
        shell.execute("tail nope")


def test_tail_without_args(shell: Shell) -> None:
    """Команда tail без аргументов — подсказка по использованию."""
    with pytest.raises(CommandError, match="usage"):
        shell.execute("tail")


def test_tail_bad_count(shell: Shell) -> None:
    """Нечисловое значение -n — ошибка."""
    with pytest.raises(CommandError, match="invalid number"):
        shell.execute("tail -n abc /readme.md")


def test_cp_file(shell: Shell) -> None:
    """Команда cp копирует файл под новым именем."""
    shell.execute("cp readme.md copy.md")
    assert shell.execute("tail copy.md") == "Deep VFS root"
    assert shell.execute("tail readme.md") == "Deep VFS root"


def test_cp_into_directory(shell: Shell) -> None:
    """Команда cp кладёт файл в папку, сохраняя имя."""
    shell.execute("cp readme.md docs")
    assert "readme.md" in shell.execute("ls docs")


def test_cp_copy_is_independent(shell: Shell) -> None:
    """Изменение копии не затрагивает оригинал."""
    shell.execute("cp -r docs docs2")
    shell.execute("mv docs2/intro.txt docs2/renamed.txt")
    assert "intro.txt" in shell.execute("ls docs")
    assert "renamed.txt" in shell.execute("ls docs2")


def test_cp_directory_needs_option(shell: Shell) -> None:
    """Папку без -r копировать нельзя."""
    with pytest.raises(CommandError, match="is a directory"):
        shell.execute("cp docs docs2")


def test_cp_into_itself(shell: Shell) -> None:
    """Папку нельзя копировать внутрь самой себя."""
    with pytest.raises(CommandError, match="into itself"):
        shell.execute("cp -r docs docs/guides")


def test_cp_same_target(shell: Shell) -> None:
    """Копирование файла в себя — ошибка."""
    with pytest.raises(CommandError, match="same"):
        shell.execute("cp readme.md readme.md")


def test_cp_bad_args(shell: Shell) -> None:
    """Неверное число аргументов cp — подсказка."""
    with pytest.raises(CommandError, match="usage"):
        shell.execute("cp readme.md")


def test_mv_rename(shell: Shell) -> None:
    """Команда mv переименовывает файл."""
    shell.execute("mv readme.md renamed.md")
    listing = shell.execute("ls")
    assert "renamed.md" in listing
    assert "readme.md" not in listing


def test_mv_into_directory(shell: Shell) -> None:
    """Команда mv переносит файл в другую папку."""
    shell.execute("mv readme.md docs")
    assert "readme.md" in shell.execute("ls docs")
    assert "readme.md" not in shell.execute("ls")


def test_mv_directory(shell: Shell) -> None:
    """Команда mv переносит папку со всем содержимым."""
    shell.execute("mv docs src")
    assert "docs" in shell.execute("ls src")
    assert "guide.txt" in shell.execute("ls /src/docs/guides")


def test_mv_into_itself(shell: Shell) -> None:
    """Папку нельзя перенести внутрь самой себя."""
    with pytest.raises(CommandError, match="into itself"):
        shell.execute("mv docs docs/guides")


def test_mv_root(shell: Shell) -> None:
    """Корень перенести нельзя."""
    with pytest.raises(CommandError, match="root"):
        shell.execute("mv / docs")


def test_mv_missing_source(shell: Shell) -> None:
    """Перенос несуществующего узла — ошибка."""
    with pytest.raises(CommandError, match="no such file"):
        shell.execute("mv nope docs")


def test_mv_bad_args(shell: Shell) -> None:
    """Неверное число аргументов mv — подсказка."""
    with pytest.raises(CommandError, match="usage"):
        shell.execute("mv readme.md")


def test_disk_is_not_modified_by_commands(shell: Shell) -> None:
    """Команды меняют только память, папка на диске остаётся прежней."""
    before = sorted(str(path) for path in DEEP.rglob("*"))
    shell.execute("cp -r docs docs2")
    shell.execute("mv readme.md docs2")
    shell.execute("mv docs2 src")
    assert sorted(str(path) for path in DEEP.rglob("*")) == before
