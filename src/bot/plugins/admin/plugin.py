import discord
from discord import app_commands
from discord.ext import commands
from src.bot.plugins.base_plugin import BasePlugin


class AdminPlugin(BasePlugin):

    PLUGIN_NAME = "Admin"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Administration tools for the bot"
    PLUGIN_AUTHOR = "Mizuki Team"

    async def setup(self):
        @app_commands.command(name="plugins", description="List all loaded plugins")
        @app_commands.default_permissions(administrator=True)
        async def plugins_list(interaction: discord.Interaction):
            plugins_info = self.bot.plugin_manager.list_plugins()

            if not plugins_info:
                await interaction.response.send_message("❌ No plugins loaded")
                return

            embed = discord.Embed(title="🔌 Loaded Plugins", color=0x7289DA)

            for plugin_info in plugins_info:
                if plugin_info:
                    value = (f"**Version:** {plugin_info['version']}\n"
                             f"**Description:** {plugin_info['description']}\n"
                             f"**Author:** {plugin_info['author']}\n"
                             f"**Commands:** {plugin_info['commands']['prefix_commands']} prefix, "
                             f"{plugin_info['commands']['slash_commands']} slash")

                    embed.add_field(
                        name=f"📦 {plugin_info['name']}",
                        value=value,
                        inline=False
                    )

            await interaction.response.send_message(embed=embed)

        self.register_slash_command(plugins_list)
