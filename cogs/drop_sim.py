import random
import discord
from discord import app_commands
from discord.ext import commands

BOSS_TABLES = {
    "zulrah": [
        ("Tanzanite fang", 1/512),
        ("Magic fang", 1/512),
        ("Serpentine visage", 1/512),
        ("Uncut onyx", 1/1024),
        ("Zulrah's scales", 1/1)
    ],
    "vorkath": [
        ("Vorkath's head", 1/50),
        ("Draconic visage", 1/5000),
        ("Skeletal visage", 1/5000),
        ("Dragon bone / hides", 1/1)
    ]
}

class DropSim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="simulate_kills", description="Simulate OSRS boss kills and drops.")
    @app_commands.choices(boss=[
        app_commands.Choice(name="Zulrah", value="zulrah"),
        app_commands.Choice(name="Vorkath", value="vorkath")
    ])
    async def simulate_kills(self, interaction: discord.Interaction, boss: str, kills: int):
        if kills > 1000:
            await interaction.response.send_message("❌ Max simulation limit is 1,000 kills.", ephemeral=True)
            return

        table = BOSS_TABLES.get(boss)
        results = {}

        for _ in range(kills):
            for item, chance in table:
                if random.random() < chance:
                    results[item] = results.get(item, 0) + 1

        embed = discord.Embed(title=f"🎲 Drop Simulation: {kills}x {boss.capitalize()}", color=discord.Color.purple())
        if not results:
            embed.description = "No rare drops obtained! Bad luck!"
        else:
            for item, count in results.items():
                embed.add_field(name=item, value=f"`x{count}`", inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DropSim(bot))