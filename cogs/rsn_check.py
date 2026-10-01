import re
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

HISCORES_URL = "https://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player="
RUNEMETRICS_URL = "https://apps.runescape.com/runemetrics/profile/profile?user="

RSN_REGEX = re.compile(r"^[a-zA-Z0-9_\- ]{1,12}$")


class RSNCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="check_rsn", 
        description="Check if an OSRS RuneScape Name (RSN) is active, banned/blocked, or available."
    )
    async def check_rsn(self, interaction: discord.Interaction, rsn: str):
        cleaned_rsn = rsn.strip()

        # 1. Validate username format
        if not RSN_REGEX.match(cleaned_rsn):
            embed = discord.Embed(
                title="❌ Invalid RSN Format",
                description=f"`{cleaned_rsn}` is not a valid RuneScape name.\nRSNs must be 1–12 characters long and contain only letters, numbers, spaces, or hyphens.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.defer()

        headers = {"User-Agent": "OSRS_Discord_Bot/1.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            # 2. Query OSRS Hiscores
            formatted_name = cleaned_rsn.replace(" ", "_")
            async with session.get(f"{HISCORES_URL}{formatted_name}") as resp:
                if resp.status == 200:
                    embed = discord.Embed(
                        title=f"✅ Active RSN: {cleaned_rsn}",
                        description="This account is **active** and appears on the OSRS Hiscores.",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Status", value="🟢 Active / Unbanned", inline=True)
                    embed.set_thumbnail(url="https://oldschool.runescape.wiki/images/Stats_icon.png")
                    await interaction.followup.send(embed=embed)
                    return

            # 3. Fallback check via RuneMetrics API
            async with session.get(f"{RUNEMETRICS_URL}{formatted_name}") as rm_resp:
                if rm_resp.status == 200:
                    data = await rm_resp.json()
                    error = data.get("error")

                    if error == "NO_PROFILE":
                        embed = discord.Embed(
                            title=f"⚠️ Unranked / Available Name: {cleaned_rsn}",
                            description="This name is not listed on the hiscores. It may belong to a fresh account with low stats or be available for registration.",
                            color=discord.Color.gold()
                        )
                        embed.add_field(name="Status", value="🟡 No Active Profile Found", inline=True)
                    elif error == "NOT_A_MEMBER":
                        embed = discord.Embed(
                            title=f"🔒 Blocked or Restricted RSN: {cleaned_rsn}",
                            description="This account or name is currently restricted, banned, or blocked from public metrics.",
                            color=discord.Color.orange()
                        )
                        embed.add_field(name="Status", value="🟠 Restricted / Non-Member", inline=True)
                    else:
                        embed = discord.Embed(
                            title=f"🚫 Banned or Unavailable RSN: {cleaned_rsn}",
                            description=f"This RSN returned an error (`{error}`) and is likely **banned, blocked, or unavailable**.",
                            color=discord.Color.red()
                        )
                        embed.add_field(name="Status", value="🔴 Banned / Blocked", inline=True)
                else:
                    embed = discord.Embed(
                        title=f"🚫 Unavailable RSN: {cleaned_rsn}",
                        description="This username could not be retrieved from official servers and is likely **banned, blocked, or locked**.",
                        color=discord.Color.red()
                    )
                    embed.add_field(name="Status", value="🔴 Banned / Unavailable", inline=True)

                await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RSNCheck(bot))