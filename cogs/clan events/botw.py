import discord
from discord import app_commands
from discord.ext import commands

class BossOfTheWeek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="botw", description="Displays Boss of the Week leaderboard.")
    async def botw(self, interaction: discord.Interaction, boss: str):
        embed = discord.Embed(
            title=f"⚔️ Boss of the Week: {boss.capitalize()}",
            description="Live leaderboard tracking boss kill counts.",
            color=discord.Color.purple()
        )
        embed.add_field(name="1. PlayerOne", value="340 KC", inline=False)
        embed.add_field(name="2. PlayerTwo", value="210 KC", inline=False)
        embed.add_field(name="3. PlayerThree", value="115 KC", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(BossOfTheWeek(bot))