import discord
from discord import app_commands
from discord.ext import commands

class SlayerTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slayer_task", description="Look up recommended gear and info for a Slayer task.")
    async def slayer_task(self, interaction: discord.Interaction, task_name: str):
        embed = discord.Embed(
            title=f"🗡️ Slayer Task Info: {task_name.title()}",
            color=discord.Color.dark_green()
        )
        embed.add_field(name="Weakness", value="Slash / Fire Spells", inline=True)
        embed.add_field(name="Superior Variant", value="Yes", inline=True)
        embed.add_field(name="Recommendation", value="Skip / Block depending on points", inline=True)
        embed.add_field(
            name="Recommended Gear", 
            value="Melee Gear (Proselyte / Bandos), Slayer Helmet, Ardougne Cloak", 
            inline=False
        )
        embed.add_field(
            name="Locations", 
            value="Catacombs of Kourend, Stronghold Slayer Cave", 
            inline=False
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SlayerTask(bot))