import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db

# Tiers: (Name, Win Probability, Multiplier)
TIERS = {
    "safe": ("Safe Sacrifice", 0.70, 1.35),      # 70% chance to win 1.35x
    "risky": ("Risky Sacrifice", 0.45, 2.00),     # 45% chance to win 2.0x
    "death": ("Death's Gamble", 0.15, 5.00)       # 15% chance to win 5.0x
}


class DeathsCoffer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coffer", description="Sacrifice GP to Death's Coffer for a chance at multiplied rewards.")
    @app_commands.choices(risk=[
        app_commands.Choice(name="Safe Sacrifice (70% win rate | 1.35x payout)", value="safe"),
        app_commands.Choice(name="Risky Sacrifice (45% win rate | 2.0x payout)", value="risky"),
        app_commands.Choice(name="Death's Gamble (15% win rate | 5.0x payout)", value="death")
    ])
    async def coffer(self, interaction: discord.Interaction, risk: str, wager: int):
        if wager <= 0:
            await interaction.response.send_message("❌ Wager must be greater than 0 GP.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        user_id = interaction.user.id

        if not db.remove_gp(guild_id, user_id, wager):
            await interaction.response.send_message("❌ Insufficient GP balance in your wallet.", ephemeral=True)
            return

        tier_name, win_rate, multiplier = TIERS[risk]
        roll = random.random()

        if roll <= win_rate:
            payout = int(wager * multiplier)
            profit = payout - wager
            db.add_gp(guild_id, user_id, payout)

            embed = discord.Embed(
                title="💀 Death Accepts Your Sacrifice!",
                description=f"You offered **{wager:,} GP** on **{tier_name}**.\n\n"
                            f"✨ Death smiles upon you and grants **{payout:,} GP** (+{profit:,} GP profit)!",
                color=discord.Color.dark_purple()
            )
        else:
            embed = discord.Embed(
                title="💀 Death Reclaims Your Soul...",
                description=f"You offered **{wager:,} GP** on **{tier_name}**.\n\n"
                            f"🪦 Death consumed your sacrifice. You lost **{wager:,} GP**.",
                color=discord.Color.dark_red()
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(DeathsCoffer(bot))