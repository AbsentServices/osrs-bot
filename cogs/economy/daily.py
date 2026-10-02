import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

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


async def setup(bot):
    await bot.add_cog(Daily(bot))