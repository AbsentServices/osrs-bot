import discord
from discord import app_commands
from discord.ext import commands


class QuestReqs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quest_reqs", description="Check player stat requirements for major quests.")
    async def quest_reqs(self, interaction: discord.Interaction, quest_name: str):
        embed = discord.Embed(
            title=f"📜 Quest Requirements: {quest_name.title()}",
            description="Comparison against required skill levels:",
            color=discord.Color.gold()
        )
        embed.add_field(name="🟢 Agility", value="70 / 70", inline=True)
        embed.add_field(name="🟢 Construction", value="70 / 70", inline=True)
        embed.add_field(name="🔴 Mining", value="62 / 72 (Missing 10 levels)", inline=True)
        embed.add_field(name="🟢 Hunter", value="70 / 70", inline=True)
        embed.add_field(name="🔴 Smithing", value="65 / 70 (Missing 5 levels)", inline=True)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(QuestReqs(bot))