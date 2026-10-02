import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db
from cogs.minigames.minigames_data import CLUE_TIERS


class Clue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clue", description="Open a simulated OSRS Clue Scroll reward casket!")
    @app_commands.choices(tier=[
        app_commands.Choice(name="Easy", value="easy"),
        app_commands.Choice(name="Medium", value="medium"),
        app_commands.Choice(name="Hard", value="hard"),
        app_commands.Choice(name="Master", value="master")
    ])
    async def clue(self, interaction: discord.Interaction, tier: str):
        guild_id = interaction.guild.id
        user_id = interaction.user.id

        clue_data = CLUE_TIERS[tier]
        reward_item, item_value = random.choice(clue_data["rewards"])

        db.add_gp(guild_id, user_id, item_value)

        embed = discord.Embed(
            title=f"📦 {clue_data['name']} Casket Opened!",
            description=f"You opened the casket and found:\n\n"
                        f"✨ **{reward_item}**\n"
                        f"💰 Value: **{item_value:,} GP** (Added to balance)",
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Clue(bot))