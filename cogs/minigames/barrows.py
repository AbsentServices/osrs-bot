import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db
from cogs.minigames.minigames_data import BARROWS_EQUIPMENT


class Barrows(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="barrows", description="Loot the Barrows chest for armor, weapons, or runes!")
    async def barrows(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        user_id = interaction.user.id

        hit_piece = random.randint(1, 14) == 1

        if hit_piece:
            item_name, item_value = random.choice(BARROWS_EQUIPMENT)
            db.add_gp(guild_id, user_id, item_value)

            embed = discord.Embed(
                title="🪦 Barrows Chest Opened!",
                description=f"🎉 **Loot Drop!** You found a piece of Barrows equipment:\n\n"
                            f"🛡️ **{item_name}**\n"
                            f"💰 Value: **{item_value:,} GP** (Added to balance)",
                color=discord.Color.gold()
            )
        else:
            rune_gp = random.randint(15000, 80000)
            db.add_gp(guild_id, user_id, rune_gp)

            embed = discord.Embed(
                title="🪦 Barrows Chest Opened!",
                description=f"You searched the chest and found standard chest supplies:\n\n"
                            f"🔮 **Runes & Bolt Racks**\n"
                            f"💰 Value: **{rune_gp:,} GP**",
                color=discord.Color.dark_grey()
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Barrows(bot))