import aiohttp
import discord
from discord import app_commands
from discord.ext import commands


class Gainz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gainz", description="Track player XP gains using the Wise Old Man API.")
    @app_commands.choices(timeframe=[
        app_commands.Choice(name="Day", value="day"),
        app_commands.Choice(name="Week", value="week"),
        app_commands.Choice(name="Month", value="month")
    ])
    async def gainz(self, interaction: discord.Interaction, username: str, timeframe: str = "week"):
        await interaction.response.defer()

        url = f"https://api.wiseoldman.net/v2/players/{username}/gained?period={timeframe}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 404:
                    await interaction.followup.send(f"❌ Player **{username}** is not tracked on Wise Old Man.")
                    return
                elif resp.status != 200:
                    await interaction.followup.send("❌ Error connecting to Wise Old Man API.")
                    return

                data = await resp.json()

        overall_gains = data.get("data", {}).get("skills", {}).get("overall", {})
        gained_xp = overall_gains.get("experience", {}).get("gained", 0)
        gained_levels = overall_gains.get("level", {}).get("gained", 0)

        embed = discord.Embed(
            title=f"📈 XP Gains ({timeframe.capitalize()}): {username.capitalize()}",
            color=discord.Color.green()
        )
        embed.add_field(name="✨ Total XP Gained", value=f"**+{gained_xp:,}** XP", inline=True)
        embed.add_field(name="⬆️ Levels Gained", value=f"**+{gained_levels}** Levels", inline=True)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Gainz(bot))