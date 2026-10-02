import discord
from discord import app_commands
from discord.ext import commands

class Dryness(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dryness", description="Calculate dryness/luck probability based on drop rate and KC.")
    async def dryness(self, interaction: discord.Interaction, kc: int, drop_rate: int):
        if kc <= 0 or drop_rate <= 0:
            await interaction.response.send_message("❌ KC and drop rate must be positive integers.", ephemeral=True)
            return

        p = 1 / drop_rate
        p_no_drop = (1 - p) ** kc
        p_at_least_one = (1 - p_no_drop) * 100
        unluckiness = p_no_drop * 100

        embed = discord.Embed(title="📊 Drop Rate / Dryness Calculator", color=discord.Color.blue())
        embed.add_field(name="Kill Count", value=f"`{kc:,}`", inline=True)
        embed.add_field(name="Drop Rate", value=f"`1/{drop_rate:,}`", inline=True)
        embed.add_field(name="Chance of ≥1 Drop", value=f"`{p_at_least_one:.2f}%`", inline=False)
        embed.add_field(
            name="Unluckiness Verdict",
            value=f"You are in the top **{unluckiness:.2f}%** unluckiest players for not getting the item yet.",
            inline=False
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Dryness(bot))