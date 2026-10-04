import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leaderboard", description="Display the server GP balance leaderboard.")
    async def leaderboard(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        
        # Retrieve all user balances for the current server guild
        all_balances = db.get_all_balances(guild_id) if hasattr(db, "get_all_balances") else {}

        if not all_balances:
            await interaction.response.send_message("ℹ️ No economy data found for this server yet.", ephemeral=True)
            return

        # Sort users by GP descending
        sorted_users = sorted(all_balances.items(), key=lambda x: x[1], reverse=True)[:10]

        embed = discord.Embed(
            title=f"🏆 Server GP Leaderboard: {interaction.guild.name}",
            color=discord.Color.gold()
        )

        leaderboard_text = ""
        medals = ["🥇", "🥈", "🥉"]

        for idx, (user_id, balance) in enumerate(sorted_users, start=1):
            rank = medals[idx - 1] if idx <= 3 else f"`#{idx}`"
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f"User ID {user_id}"
            leaderboard_text += f"{rank} **{name}**: {balance:,} GP\n"

        embed.description = leaderboard_text
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))