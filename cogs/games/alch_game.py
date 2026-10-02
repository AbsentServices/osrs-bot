import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class AlchGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="alch", description="High Alch an item and guess if its value is High or Low!")
    @app_commands.choices(guess=[
        app_commands.Choice(name="High (Over 50,000 GP)", value="high"),
        app_commands.Choice(name="Low (Under 50,000 GP)", value="low")
    ])
    async def alch(self, interaction: discord.Interaction, guess: str, wager: int):
        if wager <= 0:
            await interaction.response.send_message("❌ Wager must be greater than 0 GP.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        user_id = interaction.user.id

        if not db.remove_gp(guild_id, user_id, wager):
            await interaction.response.send_message("❌ Insufficient GP balance.", ephemeral=True)
            return

        # Generate alch value from 1 to 100,000
        alch_value = random.randint(1, 100000)
        actual_result = "high" if alch_value > 50000 else "low"

        if guess.lower() == actual_result:
            payout = wager * 2
            db.add_gp(guild_id, user_id, payout)
            embed = discord.Embed(
                title="✨ High Magic Success!",
                description=f" You alched the mystery item for **{alch_value:,} GP**!\n"
                            f"Your guess (**{guess.upper()}**) was correct.\n\n"
                            f"🎉 You won **{payout:,} GP**!",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="💥 Magic Failed!",
                description=f" You alched the mystery item for **{alch_value:,} GP**.\n"
                            f"Your guess (**{guess.upper()}**) was incorrect.\n\n"
                            f"❌ You lost **{wager:,} GP**.",
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(AlchGame(bot))