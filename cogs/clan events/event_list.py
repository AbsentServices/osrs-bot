import discord
from discord import app_commands
from discord.ext import commands

class EventList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="event_list", description="List all scheduled active clan events.")
    async def event_list(self, interaction: discord.Interaction):
        events = getattr(self.bot, "events_db", {})
        if not events:
            await interaction.response.send_message("No upcoming events scheduled.", ephemeral=True)
            return

        embed = discord.Embed(title="📜 Scheduled Clan Events", color=discord.Color.blue())
        for msg_id, info in events.items():
            embed.add_field(name=info["title"], value=f"🕒 {info['time']}", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(EventList(bot))