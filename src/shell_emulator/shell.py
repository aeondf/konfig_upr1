"""Оболочка: цикл чтения и выполнения команд."""

from shell_emulator.commands import COMMANDS, CommandError
from shell_emulator.parser import ParseError, Parser


class Shell:
    """Состояние оболочки и диспетчер команд."""

    def __init__(self, vfs_name: str = "vfs") -> None:
        """Создаёт оболочку с именем VFS для приглашения."""
        self.vfs_name = vfs_name
        self.running = True
        self.exit_code = 0
        self.parser = Parser()

    @property
    def prompt(self) -> str:
        """Приглашение к вводу с именем VFS."""
        return f"{self.vfs_name}$ "

    def stop(self, code: int) -> None:
        """Останавливает цикл с заданным кодом возврата."""
        self.running = False
        self.exit_code = code

    def execute(self, line: str) -> str:
        """Выполняет одну строку и возвращает текст результата."""
        tokens = self.parser.parse(line)
        if not tokens:
            return ""
        name, args = tokens[0], tokens[1:]
        command = COMMANDS.get(name)
        if command is None:
            raise CommandError(f"{name}: command not found")
        return command.run(self, args)

    def run_line(self, line: str) -> None:
        """Выполняет строку, печатая результат или сообщение об ошибке."""
        try:
            output = self.execute(line)
        except (ParseError, CommandError) as error:
            print(error)
            return
        if output:
            print(output)

    def run(self) -> int:
        """Запускает цикл до команды exit или конца ввода."""
        while self.running:
            try:
                line = input(self.prompt)
            except EOFError:
                print("exit")
                break
            except KeyboardInterrupt:
                print()
                continue
            self.run_line(line)
        return self.exit_code
