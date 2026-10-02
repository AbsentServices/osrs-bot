import discord
from discord import app_commands
from discord.ext import commands

class Bingo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bingo", description="Clan bingo board tracker and tile submission.")
    async def bingo(self, interaction: discord.Interaction, tile: str = None, proof: discord.Attachment = None):
        if proof and tile:
            await interaction.response.send_message(
                f"✅ Proof submitted for tile **{tile}**! An admin will review your screenshot: {proof.url}"
            )
        else:
            embed = discord.Embed(title="🧩 Clan Bingo Board Status", color=discord.Color.gold())
            embed.add_field(name="Tile 1: Get a drop > 1M", value="Status: Completed", inline=True)
            embed.add_field(name="Tile 2: 50 Zulrah KC", value="Status: In Progress", inline=True)
            embed.add_field(name="Tile 3: Obtain a Fire Cape", value="Status: Unclaimed", inline=True)
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Bingo(bot))