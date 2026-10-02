import discord
from discord import app_commands
from discord.ext import commands

class SkillOfTheWeek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sotw", description="Displays Skill of the Week leaderboard.")
    async def sotw(self, interaction: discord.Interaction, skill: str):
        embed = discord.Embed(
            title=f"🏆 Skill of the Week: {skill.capitalize()}",
            description="Live leaderboard tracking XP gains via Hiscores.",
            color=discord.Color.green()
        )
        embed.add_field(name="1. PlayerOne", value="+2,450,000 XP", inline=False)
        embed.add_field(name="2. PlayerTwo", value="+1,800,000 XP", inline=False)
        embed.add_field(name="3. PlayerThree", value="+950,000 XP", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SkillOfTheWeek(bot))