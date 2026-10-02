import discord
from discord import app_commands
from discord.ext import commands


class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load", description="Load a specific cog extension.")
    @commands.is_owner()
    async def load_prefix(self, ctx: commands.Context, extension: str):
        """Example usage: !load cogs.games.flip"""
        try:
            await self.bot.load_extension(extension)
            await ctx.send(f"✅ Successfully loaded extension: `{extension}`")
        except Exception as e:
            await ctx.send(f"❌ Error loading `{extension}`: `{e}`")

    @app_commands.command(name="load", description="Load a specific cog extension.")
    @app_commands.describe(extension="The module path of the extension (e.g. cogs.games.flip)")
    async def load_slash(self, interaction: discord.Interaction, extension: str):
        """Slash command version of load."""
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("❌ Only the bot owner can use this command.", ephemeral=True)
            return

        try:
            await self.bot.load_extension(extension)
            await interaction.response.send_message(f"✅ Successfully loaded extension: `{extension}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error loading `{extension}`: `{e}`", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Load(bot))