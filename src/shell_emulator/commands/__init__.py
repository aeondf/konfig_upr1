"""Реестр команд оболочки."""

from shell_emulator.commands.base import BaseCommand
from shell_emulator.commands.cd import CdCommand
from shell_emulator.commands.cp import CpCommand
from shell_emulator.commands.error import CommandError
from shell_emulator.commands.exit import ExitCommand
from shell_emulator.commands.ls import LsCommand
from shell_emulator.commands.mv import MvCommand
from shell_emulator.commands.tail import TailCommand
from shell_emulator.commands.uname import UnameCommand
from shell_emulator.commands.uptime import UptimeCommand

COMMANDS: dict[str, BaseCommand] = {
    command.name: command
    for command in (
        LsCommand(),
        CdCommand(),
        UptimeCommand(),
        UnameCommand(),
        TailCommand(),
        CpCommand(),
        MvCommand(),
        ExitCommand(),
    )
}

__all__ = ["COMMANDS", "BaseCommand", "CommandError"]
