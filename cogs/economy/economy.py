import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    @app_commands.command(name="balance", description="Check current GP balance.")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        gp = db.get_gp(interaction.guild.id, target.id)
        embed = discord.Embed(
            title=f"💰 {target.display_name}'s Wallet",
            description=f"Current Balance: **{gp:,} GP**",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pay", description="Transfer server GP to another member.")
    async def pay(self, interaction: discord.Interaction, recipient: discord.Member, amount: int):
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive.", ephemeral=True)
            return

        if recipient.id == interaction.user.id or recipient.bot:
            await interaction.response.send_message("❌ Invalid recipient.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        if db.remove_gp(guild_id, interaction.user.id, amount):
            db.add_gp(guild_id, recipient.id, amount)
            await interaction.response.send_message(
                f"💸 {interaction.user.mention} transferred **{amount:,} GP** to {recipient.mention}!"
            )
        else:
            await interaction.response.send_message("❌ You do not have enough GP.", ephemeral=True)

    @app_commands.command(name="daily", description="Claim daily server GP reward.")
    async def daily(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        now = discord.utils.utcnow()

        if user_id in self.cooldowns and (now - self.cooldowns[user_id]).total_seconds() < 86400:
            remaining = 86400 - (now - self.cooldowns[user_id]).total_seconds()
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            await interaction.response.send_message(
                f"⌛ Daily reward already claimed. Come back in **{hours}h {minutes}m**.",
                ephemeral=True
            )
            return

        reward = 500
        db.add_gp(interaction.guild.id, user_id, reward)
        self.cooldowns[user_id] = now
        await interaction.response.send_message(f"🎁 You claimed your daily reward of **{reward:,} GP**!")

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
    await bot.add_cog(Economy(bot))