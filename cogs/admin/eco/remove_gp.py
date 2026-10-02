import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class RemoveGP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config_group = app_commands.Group(
        name="config",
        description="Admin configuration and server economy management commands."
    )

    @config_group.command(name="remove_gp", description="[Admin] Deduct server GP from a user.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def remove_gp(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be greater than 0.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        if db.remove_gp(guild_id, user.id, amount):
            new_balance = db.get_gp(guild_id, user.id)
            await interaction.response.send_message(
                f"✅ Deducted **{amount:,} GP** from {user.mention}. New balance: **{new_balance:,} GP**."
            )
        else:
            await interaction.response.send_message("❌ User does not have enough GP to deduct.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(RemoveGP(bot))