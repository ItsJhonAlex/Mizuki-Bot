#!/usr/bin/env python3
import os
import argparse

PLUGIN_TEMPLATE = '''import discord
from discord import app_commands
from discord.ext import commands
from bot.plugins.base_plugin import BasePlugin

class {class_name}(BasePlugin):
    """{description}"""

    PLUGIN_NAME = "{name}"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "{description}"
    PLUGIN_AUTHOR = "{author}"

    async def setup(self):
        self.logger.info(" {name}...")

        @commands.command(name="example")
        async def example(ctx: commands.Context):
            await ctx.send("¡Hola desde {name}!")

        self.register_prefix_command(example_prefix)

        @app_commands.command(name="example", description="Comando de example")
        async def example_slash(interaction: discord.Interaction):
            embed = discord.Embed(
                title="Example",
                description="¡Hello {name}!",
                color=0x00ff00
            )
            await interaction.response.send_message(embed=embed)

        self.register_slash_command(example_slash)

        self.logger.info("✅ Plugin {name} loaded")
'''


def create_plugin(plugin_name: str, author: str = "Mizuki Team", description: str = ""):

    plugin_dir = f"src/bot/plugins/{plugin_name}"
    os.makedirs(plugin_dir, exist_ok=True)

    with open(f"{plugin_dir}/__init__.py", 'w', encoding='utf-8') as f:
        f.write(f'"""{description or plugin_name} plugin"""\\n')

    class_name = ''.join(word.capitalize() for word in plugin_name.split('_'))
    if not description:
        description = f"Plugin {plugin_name} para Mizuki Bot"

    with open(f"{plugin_dir}/plugin.py", 'w', encoding='utf-8') as f:
        f.write(PLUGIN_TEMPLATE.format(
            class_name=class_name,
            name=plugin_name.title(),
            description=description,
            author=author
        ))

    print(f"✅ Plugin '{plugin_name}' create in {plugin_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crear un nuevo plugin")
    parser.add_argument("name", help="Nombre del plugin")
    parser.add_argument("--author", default="Mizuki Team", help="Autor del plugin")
    parser.add_argument("--description", default="", help="Descripción del plugin")

    args = parser.parse_args()
    create_plugin(args.name, args.author, args.description)