#!/usr/bin/env python3
import os
import argparse

PLUGIN_TEMPLATE = '''import discord
from discord import app_commands
from discord.ext import commands
from src.bot.plugins.base_plugin import BasePlugin

class {class_name}(BasePlugin):
    """{description}"""

    PLUGIN_NAME = "{name}"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "{description}"
    PLUGIN_AUTHOR = "{author}"

    async def setup(self):
        self.logger.info("Loading {name}...")

        @commands.command(name="example")
        async def example(ctx: commands.Context):
            await ctx.send("Hello from {name}!")

        self.register_prefix_command(example)

        @app_commands.command(name="example", description="Example command")
        async def example_slash(interaction: discord.Interaction):
            embed = discord.Embed(
                title="Example",
                description="Hello from {name}!",
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
        f.write(f'"""{description or plugin_name} plugin"""\n')

    class_name = ''.join(word.capitalize() for word in plugin_name.split('_'))
    if not description:
        description = f"Plugin {plugin_name} for Mizuki Bot"

    with open(f"{plugin_dir}/plugin.py", 'w', encoding='utf-8') as f:
        f.write(PLUGIN_TEMPLATE.format(
            class_name=class_name,
            name=plugin_name.title(),
            description=description,
            author=author
        ))

    print(f"✅ Plugin '{plugin_name}' created in {plugin_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new plugin")
    parser.add_argument("name", help="Plugin name")
    parser.add_argument("--author", default="Mizuki Team", help="Plugin author")
    parser.add_argument("--description", default="", help="Plugin description")

    args = parser.parse_args()
    create_plugin(args.name, args.author, args.description)