import discord
from discord import app_commands
from discord.ext import commands
from src.bot.plugins.base_plugin import BasePlugin
import time


class PingPlugin(BasePlugin):
    """
    Ping Plugin - Check bot latency and response time
    Provides both slash and prefix commands
    """

    PLUGIN_NAME = "Ping"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Check bot latency and response time"
    PLUGIN_AUTHOR = "ItsJhonAlex"

    async def setup(self):
        """Setup ping commands (slash and prefix)"""
        
        # Slash Command: /ping
        @app_commands.command(name="ping", description="Check bot latency")
        async def ping_slash(interaction: discord.Interaction):
            """
            Slash command to check bot latency
            Shows WebSocket latency and API response time
            """
            # Measure API response time
            start_time = time.time()
            
            # Send initial response
            await interaction.response.send_message("🏓 Pinging...")
            
            # Calculate response time
            end_time = time.time()
            api_latency = round((end_time - start_time) * 1000)
            
            # Get WebSocket latency
            ws_latency = round(self.bot.latency * 1000)
            
            # Create embed with latency information
            embed = discord.Embed(
                title="🏓 Pong!",
                color=self._get_latency_color(ws_latency),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(
                name="⚡ WebSocket Latency",
                value=f"`{ws_latency}ms`",
                inline=True
            )
            
            embed.add_field(
                name="📡 API Latency",
                value=f"`{api_latency}ms`",
                inline=True
            )
            
            embed.set_footer(text=f"Requested by {interaction.user.name}")
            
            # Edit the initial response with the embed
            await interaction.edit_original_response(content=None, embed=embed)
            
            self.logger.info(f"Ping command used by {interaction.user} (WS: {ws_latency}ms, API: {api_latency}ms)")
        
        # Prefix Command: !ping
        @commands.command(name="ping", help="Check bot latency")
        async def ping_prefix(ctx: commands.Context):
            """
            Prefix command to check bot latency
            Shows WebSocket latency and API response time
            """
            # Measure API response time
            start_time = time.time()
            
            # Send initial message
            message = await ctx.send("🏓 Pinging...")
            
            # Calculate response time
            end_time = time.time()
            api_latency = round((end_time - start_time) * 1000)
            
            # Get WebSocket latency
            ws_latency = round(self.bot.latency * 1000)
            
            # Create embed with latency information
            embed = discord.Embed(
                title="🏓 Pong!",
                color=self._get_latency_color(ws_latency),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(
                name="⚡ WebSocket Latency",
                value=f"`{ws_latency}ms`",
                inline=True
            )
            
            embed.add_field(
                name="📡 API Latency",
                value=f"`{api_latency}ms`",
                inline=True
            )
            
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            
            # Edit the initial message with the embed
            await message.edit(content=None, embed=embed)
            
            self.logger.info(f"Ping command used by {ctx.author} (WS: {ws_latency}ms, API: {api_latency}ms)")
        
        # Register both commands
        self.register_slash_command(ping_slash)
        self.register_prefix_command(ping_prefix)
        
        self.logger.info("Ping plugin loaded successfully")
    
    def _get_latency_color(self, latency: int) -> int:
        """
        Get color based on latency
        
        Args:
            latency: Latency in milliseconds
            
        Returns:
            Color as integer (Discord color)
        """
        if latency < 100:
            return 0x2ecc71  # Green - Excellent
        elif latency < 200:
            return 0xf39c12  # Orange - Good
        elif latency < 300:
            return 0xe67e22  # Dark Orange - Fair
        else:
            return 0xe74c3c  # Red - Poor

