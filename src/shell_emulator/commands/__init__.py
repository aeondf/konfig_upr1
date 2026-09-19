"""Реестр команд оболочки."""

from shell_emulator.commands.base import BaseCommand
from shell_emulator.commands.cd import CdCommand
from shell_emulator.commands.error import CommandError
from shell_emulator.commands.exit import ExitCommand
from shell_emulator.commands.ls import LsCommand

COMMANDS: dict[str, BaseCommand] = {
    command.name: command
    for command in (LsCommand(), CdCommand(), ExitCommand())
}

__all__ = ["COMMANDS", "BaseCommand", "CommandError"]
