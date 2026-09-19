"""Запуск эмулятора."""

import argparse
from pathlib import Path

from shell_emulator.shell import Shell


def parse_arguments() -> argparse.Namespace:
    """Читает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор командной оболочки")
    parser.add_argument("--vfs", help="путь к папке VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args()


def main() -> int:
    """Запускает эмулятор с параметрами из командной строки."""
    args = parse_arguments()
    print(f"[debug] vfs={args.vfs} script={args.script}")
    vfs_name = Path(args.vfs).name if args.vfs else "vfs"

    shell = Shell(vfs_name)

    if args.script:
        try:
            shell.run_script(args.script)
        except FileNotFoundError:
            print(f"script not found: {args.script}")
            return 1
        if not shell.running:
            return shell.exit_code

    return shell.run()


if __name__ == "__main__":
    raise SystemExit(main())
