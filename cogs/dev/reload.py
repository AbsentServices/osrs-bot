import discord
from discord import app_commands
from discord.ext import commands


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload", description="Reload a specific cog extension.")
    @commands.is_owner()
    async def reload_prefix(self, ctx: commands.Context, extension: str):
        """Example usage: !reload cogs.games.stake or !reload cogs.economy.work"""
        try:
            await self.bot.reload_extension(extension)
            await ctx.send(f"🔄 Successfully reloaded extension: `{extension}`")
        except Exception as e:
            await ctx.send(f"❌ Error reloading `{extension}`: `{e}`")

    @app_commands.command(name="reload", description="Reload a specific cog extension.")
    @app_commands.describe(extension="The module path of the extension (e.g. cogs.games.stake)")
    async def reload_slash(self, interaction: discord.Interaction, extension: str):
        """Slash command version of reload."""
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("❌ Only the bot owner can use this command.", ephemeral=True)
            return

        try:
            await self.bot.reload_extension(extension)
            await interaction.response.send_message(f"🔄 Successfully reloaded extension: `{extension}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error reloading `{extension}`: `{e}`", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Reload(bot))