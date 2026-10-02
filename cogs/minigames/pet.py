import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db
from cogs.minigames.minigames_data import PET_BOSSES


class Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pet", description="Roll for a rare boss pet drop!")
    @app_commands.choices(boss=[
        app_commands.Choice(name="Vorkath (1 in 3,000)", value="vorkath"),
        app_commands.Choice(name="Zulrah (1 in 4,000)", value="zulrah"),
        app_commands.Choice(name="TzTok-Jad (1 in 100)", value="jad"),
        app_commands.Choice(name="Corporeal Beast (1 in 5,000)", value="corp"),
        app_commands.Choice(name="Chambers of Xeric (1 in 53)", value="cox")
    ])
    async def pet(self, interaction: discord.Interaction, boss: str):
        guild_id = interaction.guild.id
        user_id = interaction.user.id

        boss_name, pet_name, rate, bonus_gp = PET_BOSSES[boss]
        roll = random.randint(1, rate)

        if roll == 1:
            db.add_gp(guild_id, user_id, bonus_gp)

            embed = discord.Embed(
                title="🐾 VERY LUCKY DROP!",
                description=f"You have a funny feeling like you're being followed...\n\n"
                            f"🎯 Boss: **{boss_name}**\n"
                            f"🐾 Pet: **{pet_name}** (1 in {rate:,})\n"
                            f"💰 Bonus Bounty: **{bonus_gp:,} GP**!",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title=f"⚔️ {boss_name} Defeated",
                description=f"You defeated {boss_name}, but received no pet drop.\n"
                            f"🎲 Roll: **{roll:,}** / **{rate:,}**",
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Pet(bot))