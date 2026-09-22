"""Запуск эмулятора."""

import argparse

from pydantic import ValidationError

from shell_emulator.config import Config
from shell_emulator.shell import Shell
from shell_emulator.vfs import VFS


def parse_arguments() -> argparse.Namespace:
    """Читает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор командной оболочки")
    parser.add_argument("--vfs", help="путь к папке VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args()


def main() -> int:
    """Запускает эмулятор с параметрами из командной строки."""
    args = parse_arguments()
    try:
        config = Config(vfs=args.vfs, script=args.script)
    except ValidationError as error:
        for item in error.errors():
            print(f"{item['loc'][0]}: {item['msg']}")
        return 1
    print(f"[debug] vfs={config.vfs} script={config.script}")

    vfs = VFS()
    if config.vfs:
        vfs.load(config.vfs)
        print("[debug] vfs tree:", *vfs.paths(), sep="\n  ")

    shell = Shell(vfs)
    if config.script:
        shell.run_script(config.script)
        if not shell.running:
            return shell.exit_code

    return shell.run()


if __name__ == "__main__":
    raise SystemExit(main())
