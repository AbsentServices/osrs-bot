import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class AddGP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config_group = app_commands.Group(
        name="config",
        description="Admin configuration and server economy management commands."
    )

    @config_group.command(name="add_gp", description="[Admin] Manually award server GP to a user.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def add_gp(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be greater than 0.", ephemeral=True)
            return

        db.add_gp(interaction.guild.id, user.id, amount)
        new_balance = db.get_gp(interaction.guild.id, user.id)
        await interaction.response.send_message(
            f"✅ Awarded **{amount:,} GP** to {user.mention}. New balance: **{new_balance:,} GP**."
        )


async def setup(bot):
    await bot.add_cog(AddGP(bot))