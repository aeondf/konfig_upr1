"""Тесты параметров командной строки."""

from pathlib import Path

import pytest

from shell_emulator.main import main

EXIT_CODE = 5
ERROR_CODE = 1


def run_main(monkeypatch: pytest.MonkeyPatch, *argv: str) -> int:
    """Запускает main() с заданными параметрами."""
    monkeypatch.setattr("sys.argv", ["main.py", *argv])
    return main()


def test_debug_output_and_vfs_name(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Параметры печатаются, имя VFS берётся из последней части пути."""
    script = tmp_path / "s.txt"
    script.write_text(f"exit {EXIT_CODE}\n")
    code = run_main(monkeypatch, "--vfs", "vfs/deep", "--script", str(script))
    out = capsys.readouterr().out
    assert code == EXIT_CODE
    assert f"[debug] vfs=vfs/deep script={script}" in out
    assert f"deep:/$ exit {EXIT_CODE}" in out


def test_vfs_tree_is_printed(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """При загрузке VFS печатается дерево путей."""
    script = tmp_path / "s.txt"
    script.write_text("exit\n")
    run_main(monkeypatch, "--vfs", "vfs/deep", "--script", str(script))
    out = capsys.readouterr().out
    assert "[debug] vfs tree:" in out
    assert "/docs/guides/linux/commands.txt" in out


def test_missing_vfs(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Несуществующая папка VFS — сообщение и код 1."""
    code = run_main(monkeypatch, "--vfs", "vfs/nope")
    assert code == ERROR_CODE
    assert "vfs:" in capsys.readouterr().out


def test_vfs_is_not_a_directory(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Файл вместо папки VFS — сообщение и код 1."""
    code = run_main(monkeypatch, "--vfs", "vfs/minimal/readme.txt")
    assert code == ERROR_CODE
    assert "directory" in capsys.readouterr().out


def test_missing_script(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Несуществующий скрипт — сообщение и код 1."""
    code = run_main(monkeypatch, "--script", str(tmp_path / "nope.txt"))
    assert code == ERROR_CODE
    assert "script:" in capsys.readouterr().out
