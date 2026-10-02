import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from cogs.stats.hiscores_data import SKILLS


class Hiscores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hiscores", description="Fetch total OSRS skill stats for a player.")
    @app_commands.describe(username="The OSRS player username to lookup")
    async def hiscores(self, interaction: discord.Interaction, username: str):
        await interaction.response.defer()

        url = f"https://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player={username}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 404:
                    await interaction.followup.send(f"❌ Player **{username}** not found on OSRS Highscores.")
                    return
                elif resp.status != 200:
                    await interaction.followup.send("❌ Unable to reach OSRS Highscores API right now.")
                    return

                data = await resp.text()

        lines = data.strip().split("\n")
        embed = discord.Embed(
            title=f"🛡️ OSRS Highscores: {username.capitalize()}",
            color=discord.Color.gold()
        )

        overall_rank, overall_lvl, overall_xp = lines[0].split(",")
        embed.add_field(
            name="🏆 Overall",
            value=f"**Level:** {int(overall_lvl):,}\n**XP:** {int(overall_xp):,}\n**Rank:** #{int(overall_rank):,}",
            inline=False
        )

        # Highlight keycombat/popular skills
        key_skills = ["Attack", "Strength", "Defence", "Ranged", "Prayer", "Magic", "Hitpoints", "Slayer"]
        for idx, skill in enumerate(SKILLS[1:], start=1):
            if skill in key_skills and idx < len(lines):
                rank, level, xp = lines[idx].split(",")
                if int(level) > 1:
                    embed.add_field(
                        name=skill,
                        value=f"Lvl {level} ({int(xp):,} XP)",
                        inline=True
                    )

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Hiscores(bot))