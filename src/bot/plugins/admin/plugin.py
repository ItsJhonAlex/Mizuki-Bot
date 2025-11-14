import discord
from discord import app_commands
from discord.ext import commands
from src.bot.plugins.base_plugin import BasePlugin


class AdminPlugin(BasePlugin):

    PLUGIN_NAME = "Admin"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Herramientas de administración del bot"
    PLUGIN_AUTHOR = "Mizuki Team"

    async def setup(self):

        @app_commands.command(name="plugins", description="Lista todos los plugins cargados")
        @app_commands.default_permissions(administrator=True)
        async def plugins_list(interaction: discord.Interaction):
            plugins_info = self.bot.plugin_manager.list_plugins()

            if not plugins_info:
                await interaction.response.send_message("❌ No hay plugins cargados")
                return

            embed = discord.Embed(title="🔌 Plugins Cargados", color=0x7289DA)

            for plugin_info in plugins_info:
                if plugin_info:
                    value = (f"**Versión:** {plugin_info['version']}\n"
                             f"**Descripción:** {plugin_info['description']}\n"
                             f"**Autor:** {plugin_info['author']}\n"
                             f"**Comandos:** {plugin_info['commands']['prefix_commands']} prefijo, "
                             f"{plugin_info['commands']['slash_commands']} slash")

                    embed.add_field(
                        name=f"📦 {plugin_info['name']}",
                        value=value,
                        inline=False
                    )

            await interaction.response.send_message(embed=embed)

        self.register_slash_command(plugins_list)
