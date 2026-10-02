import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class Flip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="flip", description="Wager server GP on a 50/50 coin flip.")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Heads", value="heads"),
        app_commands.Choice(name="Tails", value="tails")
    ])
    async def flip(self, interaction: discord.Interaction, choice: str, wager: int):
        if wager <= 0:
            await interaction.response.send_message("❌ Wager must be greater than 0.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        if not db.remove_gp(guild_id, interaction.user.id, wager):
            await interaction.response.send_message("❌ Insufficient GP balance.", ephemeral=True)
            return

        outcome = random.choice(["heads", "tails"])
        if choice.lower() == outcome:
            winnings = wager * 2
            db.add_gp(guild_id, interaction.user.id, winnings)
            await interaction.response.send_message(
                f"🪙 Coin landed on **{outcome}**! You won **{winnings:,} GP**!"
            )
        else:
            await interaction.response.send_message(
                f"🪙 Coin landed on **{outcome}**. You lost **{wager:,} GP**."
            )


async def setup(bot):
    await bot.add_cog(Flip(bot))