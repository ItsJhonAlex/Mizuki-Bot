import discord
from discord.ext import commands
import logging
import os
from typing import Optional
from src.bot.core.plugin_manager import PluginManager

class Bot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(
            command_prefix= os.getenv("DISCORD_PREFIX"),
            intents=intents,
            case_insensitive=True
        )

        self.logger = logging.getLogger("mizuki")
        # Primary plugin manager instance (kept as `plugins` for internal use)
        self.plugins = PluginManager(self)
        # Backwards-compatible alias: some plugins expect `bot.plugin_manager`
        # so provide the same instance under that name.
        self.plugin_manager = self.plugins

    async def setup_hook(self):
        self.logger.info(f"Setup hook called")
        await self.plugins.load_plugins()
        self.logger.info("Successfully loaded plugins")

    async def load_slash_commands(self):
        try:
            self.logger.info("Loading slash commands")
            await self.load_extension('bot.cogs.slash_commands')
            self.logger.info("Successfully loaded slash commands")
        except Exception as e:
            self.logger.error(f"Failed to load slash commands: {e}")

    async def start(self):
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            self.logger.error("Environment variable DISCORD_TOKEN not set")
            return
        self.logger.info("Starting bot")
        await super().start(token)

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} in {len(self.guilds)} guilds")

        try:
            synced = await self.tree.sync()
            self.logger.info(f"Successfully synced {len(synced)} slash commands")
        except Exception as e:
            self.logger.error(f"Failed to sync commands: {e}")

        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name= os.getenv("DISCORD_ACTIVITY")
        )
        await self.change_presence(activity=activity)


    async def close(self):
        self.logger.info("Closing bot")
        await super().close()
