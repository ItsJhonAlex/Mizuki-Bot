import discord
from discord import app_commands
from discord.ext import commands
import logging
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class BasePlugin(ABC):
    PLUGIN_NAME: str = "BasePlugin"
    PLUGIN_DESCRIPTION: str = "Base Plugin"
    PLUGIN_VERSION: str = "1.0"
    PLUGIN_AUTHOR: str = ""
    PLUGIN_EMAIL: str = ""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(f"plugins.{self.__class__.__name__}")

        self._prefix_commands: List[commands.Command] = []
        self._slash_commands: List[app_commands.Command] = []
        self._event_listeners: Dict[str, Any] = {}

    @abstractmethod
    async def setup(self) -> None:
        pass

    async def teardown(self) -> None:
        await self._cleanup_commands()
        self.logger.info(f"Plugin {self.PLUGIN_NAME} teardown")

    async def _cleanup_commands(self):
        for command in self._prefix_commands:
            self.bot.remove_command(command.name)

        for command in self._slash_commands:
            self.bot.tree.remove_command(command.name, type=command.type)

        for event_name, listener in self._event_listeners.items():
            self.bot.remove_listener(listener, event_name)

    def register_prefix_command(self, command: commands.Command):
        self.bot.add_command(command)
        self._prefix_commands.append(command)

    def register_slash_command(self, command: app_commands.Command):
        self.bot.tree.add_command(command)
        self._slash_commands.append(command)

    def register_event_listener(self, event: str, listener):
        self.bot.add_listener(listener, event)
        self._event_listeners[event] = listener

    def get_metadata(self) -> Dict[str, str]:
        return {
            "name": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "description": self.PLUGIN_DESCRIPTION,
            "author": self.PLUGIN_AUTHOR,
            "email": self.PLUGIN_EMAIL
        }

    def get_command_count(self) -> Dict[str, int]:
        return {
            "prefix_commands": len(self._prefix_commands),
            "slash_commands": len(self._slash_commands),
            "event_listeners": len(self._event_listeners)
        }
