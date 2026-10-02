import discord
from discord import app_commands
from discord.ext import commands


class Unload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unload", description="Unload a specific cog extension.")
    @commands.is_owner()
    async def unload_prefix(self, ctx: commands.Context, extension: str):
        """Example usage: !unload cogs.games.flip"""
        try:
            await self.bot.unload_extension(extension)
            await ctx.send(f"⏹️️ Successfully unloaded extension: `{extension}`")
        except Exception as e:
            await ctx.send(f"❌ Error unloading `{extension}`: `{e}`")

    @app_commands.command(name="unload", description="Unload a specific cog extension.")
    @app_commands.describe(extension="The module path of the extension (e.g. cogs.games.flip)")
    async def unload_slash(self, interaction: discord.Interaction, extension: str):
        """Slash command version of unload."""
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("❌ Only the bot owner can use this command.", ephemeral=True)
            return

        try:
            await self.bot.unload_extension(extension)
            await interaction.response.send_message(f"⏹️️ Successfully unloaded extension: `{extension}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error unloading `{extension}`: `{e}`", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Unload(bot))