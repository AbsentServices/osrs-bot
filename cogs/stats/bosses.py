import aiohttp
import discord
from discord import app_commands
from discord.ext import commands


class Bosses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bosses", description="Display boss kill counts (KC) and raid completions.")
    @app_commands.describe(username="The OSRS player username to lookup")
    async def bosses(self, interaction: discord.Interaction, username: str):
        await interaction.response.defer()

        url = f"https://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player={username}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 404:
                    await interaction.followup.send(f"❌ Player **{username}** was not found.")
                    return
                elif resp.status != 200:
                    await interaction.followup.send("❌ Error contacting OSRS Highscores.")
                    return

                data = await resp.text()

        lines = data.strip().split("\n")
        
        # OSRS Highscores includes minigames & bosses after skills (24 skills)
        # Raids KC lines in official OSRS CSV response:
        # CoX = 60, ToB = 91, ToA = 94
        raid_indices = {
            "Chambers of Xeric": 60,
            "Theatre of Blood": 91,
            "Tombs of Amascut": 94
        }

        embed = discord.Embed(
            title=f"⚔️ Boss Kills & Raids: {username.capitalize()}",
            color=discord.Color.dark_red()
        )

        found_kc = False
        for raid_name, idx in raid_indices.items():
            if idx < len(lines):
                parts = lines[idx].split(",")
                if len(parts) >= 2 and int(parts[1]) > 0:
                    found_kc = True
                    embed.add_field(
                        name=f"🏰 {raid_name}",
                        value=f"**{int(parts[1]):,}** KC (Rank #{int(parts[0]):,})",
                        inline=False
                    )

        if not found_kc:
            embed.description = "No raid completions recorded on highscores for this player."

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Bosses(bot))