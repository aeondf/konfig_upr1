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
    code = run_main(monkeypatch, "--vfs", "/tmp/myfs", "--script", str(script))
    out = capsys.readouterr().out
    assert code == EXIT_CODE
    assert f"[debug] vfs=/tmp/myfs script={script}" in out
    assert f"myfs$ exit {EXIT_CODE}" in out


def test_missing_script(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Несуществующий скрипт — сообщение и код 1."""
    code = run_main(monkeypatch, "--script", str(tmp_path / "nope.txt"))
    assert code == ERROR_CODE
    assert "script not found" in capsys.readouterr().out
