import random
import discord
from discord import app_commands
from discord.ext import commands

CLUE_LOOT_TABLES = {
    "easy": {
        "name": "Easy Clue Casket",
        "avg_gp": (5_000, 25_000),
        "uniques": [
            {"name": "Team Cape Zero", "chance": 128, "value": 150_000},
            {"name": "Black Trimmed Armor Piece", "chance": 64, "value": 40_000},
            {"name": "Cape of Skull", "chance": 256, "value": 300_000},
        ],
    },
    "medium": {
        "name": "Medium Clue Casket",
        "avg_gp": (15_000, 60_000),
        "uniques": [
            {"name": "Ranger Boots", "chance": 283, "value": 38_000_000},
            {"name": "Holy Sandals", "chance": 283, "value": 1_200_000},
            {"name": "Wizard Boots", "chance": 283, "value": 450_000},
            {"name": "Spiked Manacles", "chance": 283, "value": 1_100_000},
        ],
    },
    "hard": {
        "name": "Hard Clue Casket",
        "avg_gp": (40_000, 150_000),
        "uniques": [
            {"name": "3rd Age Platebody", "chance": 211_250, "value": 2_000_000_000},
            {"name": "3rd Age Longsword", "chance": 211_250, "value": 2_000_000_000},
            {"name": "Robin Hood Hat", "chance": 300, "value": 1_500_000},
            {"name": "Rune Trimmed Armor Piece", "chance": 100, "value": 80_000},
        ],
    },
    "elite": {
        "name": "Elite Clue Casket",
        "avg_gp": (80_000, 300_000),
        "uniques": [
            {"name": "3rd Age Druidic Robe Top", "chance": 487_500, "value": 2_000_000_000},
            {"name": "Ranger Gloves", "chance": 1250, "value": 1_100_000},
            {"name": "Royal Gown", "chance": 625, "value": 350_000},
        ],
    },
    "master": {
        "name": "Master Clue Casket",
        "avg_gp": (150_000, 600_000),
        "uniques": [
            {"name": "Bloodhound Pet", "chance": 1000, "value": 0},
            {"name": "3rd Age Pickaxe", "chance": 313_168, "value": 2_000_000_000},
            {"name": "3rd Age Druidic Staff", "chance": 313_168, "value": 1_800_000_000},
            {"name": "Ale of the Gods", "chance": 851, "value": 14_000_000},
            {"name": "Ankou Mask", "chance": 851, "value": 4_000_000},
        ],
    },
}


class ClueScrolls(commands.Cog):
    """Clue Scroll Simulation Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="clue",
        description="Solve a simulated clue scroll step and open the casket for loot.",
    )
    @app_commands.describe(tier="Select the clue scroll difficulty tier")
    @app_commands.choices(
        tier=[
            app_commands.Choice(name="Easy", value="easy"),
            app_commands.Choice(name="Medium", value="medium"),
            app_commands.Choice(name="Hard", value="hard"),
            app_commands.Choice(name="Elite", value="elite"),
            app_commands.Choice(name="Master", value="master"),
        ]
    )
    async def clue(
        self,
        interaction: discord.Interaction,
        tier: app_commands.Choice[str],
    ):
        casket_data = CLUE_LOOT_TABLES[tier.value]
        min_gp, max_gp = casket_data["avg_gp"]
        total_value = random.randint(min_gp, max_gp)

        rolls = random.randint(3, 5)
        uniques_obtained = []

        for _ in range(rolls):
            for item in casket_data["uniques"]:
                if random.randint(1, item["chance"]) == 1:
                    uniques_obtained.append(item)
                    total_value += item["value"]

        embed = discord.Embed(
            title=f"📜 {casket_data['name']} Opened!",
            color=discord.Color.gold(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(
            name="💰 Casket Value",
            value=f"**{total_value:,} GP**",
            inline=False,
        )

        if uniques_obtained:
            unique_text = "\n".join(
                [f"✨ **{item['name']}** ({item['value']:,} GP)" for item in uniques_obtained]
            )
            embed.add_field(name="🎁 Rare Unique Loot", value=unique_text, inline=False)
        else:
            embed.add_field(
                name="📦 Standard Loot",
                value="*Runes, teleports, and coins.*",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ClueScrolls(bot))