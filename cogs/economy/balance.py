import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Check current GP balance.")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        gp = db.get_gp(interaction.guild.id, target.id)
        embed = discord.Embed(
            title=f"💰 {target.display_name}'s Wallet",
            description=f"Current Balance: **{gp:,} GP**",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Balance(bot))