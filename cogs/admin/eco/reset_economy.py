import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class ResetEconomy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config_group = app_commands.Group(
        name="config",
        description="Admin configuration and server economy management commands."
    )

    @config_group.command(name="reset_economy", description="[Admin] Reset all user balances for this server.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def reset_economy(self, interaction: discord.Interaction):
        guild_data = db.get_guild_data(interaction.guild.id)
        guild_data["users"] = {}
        db.save_guild_data(interaction.guild.id, guild_data)

        await interaction.response.send_message("⚠️ All server GP balances have been successfully reset.")


async def setup(bot):
    await bot.add_cog(ResetEconomy(bot))