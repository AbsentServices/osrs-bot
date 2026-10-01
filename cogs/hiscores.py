import re
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

# Official OSRS Hiscores API Endpoint
HISCORES_URL = "https://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player="

# Valid RSN pattern: 1-12 characters, letters/numbers/spaces/hyphens
RSN_REGEX = re.compile(r"^[a-zA-Z0-9_\- ]{1,12}$")

# Index mapping for skills returned by the Hiscores CSV
SKILLS = [
    "Overall", "Attack", "Defence", "Strength", "Hitpoints", "Ranged",
    "Prayer", "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing",
    "Firemaking", "Crafting", "Smithing", "Mining", "Herblore", "Agility",
    "Thieving", "Slayer", "Farming", "Runecraft", "Hunter", "Construction"
]

# Common Boss indices in the Hiscores Lite CSV
BOSSES = {
    37: "Abyssal Sire", 38: "Alchemical Hydra", 39: "Artio", 40: "Barrows Chests",
    41: "Bryophyta", 42: "Callisto", 43: "Calvar'ion", 44: "Cerberus",
    45: "Chambers of Xeric", 46: "CoX: Challenge Mode", 47: "Chaos Fanatic",
    48: "Commander Zilyana", 49: "Corporeal Beast", 50: "Crazy Archaeologist",
    51: "Dagannoth Prime", 52: "Dagannoth Rex", 53: "Dagannoth Supreme",
    54: "Deranged Archaeologist", 55: "General Graardor", 56: "Giant Mole",
    57: "Grotesque Guardians", 58: "Hespori", 59: "Kalphite Queen",
    60: "King Black Dragon", 61: "Kraken", 62: "Kree'Arra",
    63: "K'ril Tsutsaroth", 64: "Mimic", 65: "Nex", 66: "Nightmare",
    67: "Phosani's Nightmare", 68: "Obor", 69: "Phantom Muspah",
    70: "Sarachnis", 71: "Scorpia", 72: "Skotizo", 73: "Spindel",
    74: "Tempoross", 75: "The Gauntlet", 76: "The Corrupted Gauntlet",
    77: "The Leviathan", 78: "The Whisperer", 79: "Theatre of Blood",
    80: "ToB: Hard Mode", 81: "Thermonuclear Smoke Devil", 82: "Tombs of Amascut",
    83: "ToA: Expert Mode", 84: "TzKal-Zuk", 85: "TzTok-Jad", 86: "Vardorvis",
    87: "Venenatis", 88: "Vet'ion", 89: "Vorkath", 90: "Wintertodt",
    91: "Zalcano", 92: "Zulrah"
}


class Hiscores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="hiscores",
        description="Look up player stats and boss KC on the OSRS Hiscores."
    )
    async def hiscores(self, interaction: discord.Interaction, rsn: str):
        cleaned_rsn = rsn.strip()

        # Validate RSN format
        if not RSN_REGEX.match(cleaned_rsn):
            embed = discord.Embed(
                title="❌ Invalid RSN",
                description=f"`{cleaned_rsn}` is not a valid RuneScape name.\nNames must be 1–12 characters long.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.defer()

        formatted_name = cleaned_rsn.replace(" ", "_")
        headers = {"User-Agent": "OSRS_Discord_Bot/1.0"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{HISCORES_URL}{formatted_name}") as resp:
                if resp.status != 200:
                    embed = discord.Embed(
                        title="❌ Player Not Found",
                        description=f"Player **{cleaned_rsn}** was not found on the OSRS Hiscores.\nThey may be unranked, banned, or the username is incorrect.",
                        color=discord.Color.red()
                    )
                    await interaction.followup.send(embed=embed)
                    return

                raw_data = await resp.text()

        lines = [line.strip() for line in raw_data.split("\n") if line.strip()]

        # 1. Parse Skills
        parsed_skills = {}
        for i, skill_name in enumerate(SKILLS):
            if i < len(lines):
                parts = lines[i].split(",")
                if len(parts) >= 3:
                    rank, level, xp = parts[0], int(parts[1]), int(parts[2])
                    parsed_skills[skill_name] = {"level": level, "xp": xp, "rank": rank}

        overall = parsed_skills.get("Overall", {"level": 0, "xp": 0, "rank": "Unranked"})

        # 2. Parse Bosses
        boss_kills = {}
        for line_idx, boss_name in BOSSES.items():
            if line_idx < len(lines):
                parts = lines[line_idx].split(",")
                if len(parts) >= 2:
                    kc = int(parts[1])
                    if kc > 0:
                        boss_kills[boss_name] = kc

        # Format Skill Levels in Columns
        skill_lines = []
        for skill_name in SKILLS[1:]:  # Skip Overall
            sdata = parsed_skills.get(skill_name, {"level": 1})
            skill_lines.append(f"**{skill_name}:** `{sdata['level']}`")

        mid = len(skill_lines) // 2
        col1 = "\n".join(skill_lines[:mid])
        col2 = "\n".join(skill_lines[mid:])

        # Build Embed
        embed = discord.Embed(
            title=f"⚔️ OSRS Hiscores — {cleaned_rsn}",
            url=f"https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal.ws?user1={formatted_name}",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url="https://oldschool.runescape.wiki/images/Stats_icon.png")

        embed.add_field(
            name="📊 Summary",
            value=f"**Total Level:** `{overall['level']:,}`\n**Total XP:** `{overall['xp']:,}`\n**Overall Rank:** `#{int(overall['rank']):,}`" if overall['rank'] != '-1' else f"**Total Level:** `{overall['level']:,}`\n**Total XP:** `{overall['xp']:,}`",
            inline=False
        )

        embed.add_field(name="Skills (1/2)", value=col1, inline=True)
        embed.add_field(name="Skills (2/2)", value=col2, inline=True)

        # Top 5 Boss Kills
        if boss_kills:
            sorted_bosses = sorted(boss_kills.items(), key=lambda item: item[1], reverse=True)[:5]
            boss_text = "\n".join([f"• **{bname}:** `{kc:,} KC`" for bname, kc in sorted_bosses])
            embed.add_field(name="🏆 Top Boss Kill Counts", value=boss_text, inline=False)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Hiscores(bot))