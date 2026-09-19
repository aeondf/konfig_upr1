"""Запуск эмулятора."""

from shell_emulator.shell import Shell


def main() -> int:
    """Создаёт оболочку и возвращает её код завершения."""
    return Shell().run()


if __name__ == "__main__":
    raise SystemExit(main())
