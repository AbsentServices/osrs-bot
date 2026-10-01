import math
import discord
from discord import app_commands
from discord.ext import commands

class CombatCalculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="combat", description="Calculate OSRS Combat Level.")
    async def combat(self, interaction: discord.Interaction, 
                     attack: int, strength: int, defence: int, hitpoints: int, 
                     prayer: int, ranged: int = 1, magic: int = 1):
        
        base = 0.25 * (defence + hitpoints + math.floor(prayer / 2))
        melee = 0.325 * (attack + strength)
        range_lvl = 0.325 * math.floor(3 * ranged / 2)
        mage_lvl = 0.325 * math.floor(3 * magic / 2)

        combat_lvl = base + max(melee, range_lvl, mage_lvl)
        
        embed = discord.Embed(title="⚔️ Combat Level Calculation", color=discord.Color.dark_red())
        embed.add_field(name="Combat Level", value=f"**{round(combat_lvl, 2)}**", inline=False)
        embed.add_field(name="Base", value=str(base))
        embed.add_field(name="Melee/Range/Mage Max", value=str(max(melee, range_lvl, mage_lvl)))

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(CombatCalculator(bot))