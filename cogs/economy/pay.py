import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pay", description="Transfer server GP to another member.")
    async def pay(self, interaction: discord.Interaction, recipient: discord.Member, amount: int):
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive.", ephemeral=True)
            return

        if recipient.id == interaction.user.id or recipient.bot:
            await interaction.response.send_message("❌ Invalid recipient.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        if db.remove_gp(guild_id, interaction.user.id, amount):
            db.add_gp(guild_id, recipient.id, amount)
            await interaction.response.send_message(
                f"💸 {interaction.user.mention} transferred **{amount:,} GP** to {recipient.mention}!"
            )
        else:
            await interaction.response.send_message("❌ You do not have enough GP.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Pay(bot))