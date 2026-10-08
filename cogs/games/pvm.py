import random
import discord
from discord import app_commands
from discord.ext import commands

# Standard OSRS Drop Tables & Data Definitions
BOSS_LOOT_TABLES = {
    "vorkath": {
        "name": "Vorkath",
        "avg_kill_value": 130_000,
        "pet_chance": 3000,
        "pet_name": "Vorki",
        "uniques": [
            {"name": "Draconic Visage", "chance": 5000, "value": 3_200_000},
            {"name": "Skeletal Visage", "chance": 5000, "value": 18_000_000},
            {"name": "Vorkath's Head", "chance": 50, "value": 0},
            {"name": "Dragonbone Necklace", "chance": 1000, "value": 600_000},
        ],
    },
    "zulrah": {
        "name": "Zulrah",
        "avg_kill_value": 110_000,
        "pet_chance": 4000,
        "pet_name": "Pet Snakeling",
        "uniques": [
            {"name": "Tanzanite Fang", "chance": 1024, "value": 2_500_000},
            {"name": "Magic Fang", "chance": 1024, "value": 1_200_000},
            {"name": "Uncut Onyx", "chance": 1024, "value": 2_100_000},
            {"name": "Serpentine Visage", "chance": 1024, "value": 2_800_000},
        ],
    },
}

RAID_UNIQUES = {
    "cox": [
        {"name": "Dexterous Prayer Scroll", "weight": 20, "value": 14_000_000},
        {"name": "Arcane Prayer Scroll", "weight": 20, "value": 1_000_000},
        {"name": "Twisted Bow", "weight": 2, "value": 1_650_000_000},
        {"name": "Ancestral Robe Top", "weight": 3, "value": 170_000_000},
        {"name": "Ancestral Robe Bottom", "weight": 3, "value": 150_000_000},
        {"name": "Ancestral Hat", "weight": 3, "value": 75_000_000},
        {"name": "Dragon Hunter Crossbow", "weight": 4, "value": 60_000_000},
    ],
    "tob": [
        {"name": "Scythe of Vitur", "weight": 2, "value": 1_400_000_000},
        {"name": "Ghrazi Rapier", "weight": 7, "value": 55_000_000},
        {"name": "Sanguinesti Staff", "weight": 7, "value": 85_000_000},
        {"name": "Avernic Defender Hilt", "weight": 8, "value": 80_000_000},
        {"name": "Justiciar Faceguard", "weight": 5, "value": 18_000_000},
    ],
    "toa": [
        {"name": "Tumeken's Shadow", "weight": 2, "value": 1_350_000_000},
        {"name": "Elidinis' Ward", "weight": 8, "value": 7_000_000},
        {"name": "Masori Mask", "weight": 4, "value": 25_000_000},
        {"name": "Masori Body", "weight": 4, "value": 110_000_000},
        {"name": "Masori Chaps", "weight": 4, "value": 90_000_000},
        {"name": "Osmumten's Fang", "weight": 14, "value": 15_000_000},
        {"name": "Lightbearer", "weight": 14, "value": 3_000_000},
    ],
}


class PvMSimulator(commands.Cog):
    """Monster and Boss Loot Simulation Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # -------------------------------------------------------------------------
    # /kill Command
    # -------------------------------------------------------------------------

    @app_commands.command(
        name="kill",
        description="Simulate killing a boss and output the loot collected, profit, and rare drops.",
    )
    @app_commands.describe(
        monster="Select the boss to simulate killing",
        quantity="Number of kills to simulate (1-1000)",
    )
    @app_commands.choices(
        monster=[
            app_commands.Choice(name="Vorkath", value="vorkath"),
            app_commands.Choice(name="Zulrah", value="zulrah"),
        ]
    )
    async def kill(
        self,
        interaction: discord.Interaction,
        monster: app_commands.Choice[str],
        quantity: app_commands.Range[int, 1, 1000] = 1,
    ):
        boss_data = BOSS_LOOT_TABLES[monster.value]
        
        total_regular_gp = sum(
            int(random.gauss(boss_data["avg_kill_value"], boss_data["avg_kill_value"] * 0.2))
            for _ in range(quantity)
        )

        uniques_obtained = {}
        pets_obtained = 0

        for _ in range(quantity):
            # Check pet drop
            if random.randint(1, boss_data["pet_chance"]) == 1:
                pets_obtained += 1

            # Check unique drops
            for item in boss_data["uniques"]:
                if random.randint(1, item["chance"]) == 1:
                    name = item["name"]
                    uniques_obtained[name] = uniques_obtained.get(name, 0) + 1
                    total_regular_gp += item["value"]

        # Build output embed
        embed = discord.Embed(
            title=f"⚔️ {quantity}x {boss_data['name']} Loot Simulation",
            color=discord.Color.gold(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(
            name="💰 Estimated Total Revenue",
            value=f"**{total_regular_gp:,} GP**",
            inline=False,
        )

        if uniques_obtained:
            unique_text = "\n".join(
                [f"• **{item}**: {count}x" for item, count in uniques_obtained.items()]
            )
            embed.add_field(name="✨ Rare Drops", value=unique_text, inline=False)
        else:
            embed.add_field(
                name="✨ Rare Drops",
                value="*No rare unique drops received.*",
                inline=False,
            )

        if pets_obtained > 0:
            embed.add_field(
                name="🐾 Pet Drop!",
                value=f"🎉 You unlocked the **{boss_data['pet_name']}**! ({pets_obtained}x)",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)

    # -------------------------------------------------------------------------
    # /chest Command
    # -------------------------------------------------------------------------

    @app_commands.command(
        name="chest",
        description="Simulate opening a raid completion reward chest (CoX, ToB, ToA).",
    )
    @app_commands.describe(
        raid="The raid chest to open",
        invocation_or_points="Invocation level for ToA OR total points for CoX (ignored for ToB)",
    )
    @app_commands.choices(
        raid=[
            app_commands.Choice(name="Chambers of Xeric (CoX)", value="cox"),
            app_commands.Choice(name="Theatre of Blood (ToB)", value="tob"),
            app_commands.Choice(name="Tombs of Amascut (ToA)", value="toa"),
        ]
    )
    async def chest(
        self,
        interaction: discord.Interaction,
        raid: app_commands.Choice[str],
        invocation_or_points: int = 300,
    ):
        raid_type = raid.value
        purple_chance = 0.0

        if raid_type == "cox":
            # CoX: 1% unique chance per 8,675 points (capped at 57.14%)
            purple_chance = min((invocation_or_points / 8675), 57.14)
        elif raid_type == "tob":
            # ToB: ~11% flat base purple chance for deathless raid
            purple_chance = 11.0
        elif raid_type == "toa":
            # ToA: Approximate percentage base formula on invocation
            purple_chance = min(max((invocation_or_points / 50) ** 1.8 * 0.4, 0.5), 15.0)

        roll = random.uniform(0, 100)
        got_purple = roll <= purple_chance

        embed = discord.Embed(
            title=f"📦 {raid.name} Reward Chest",
            color=discord.Color.purple() if got_purple else discord.Color.dark_grey(),
        )

        if got_purple:
            items = RAID_UNIQUES[raid_type]
            weights = [i["weight"] for i in items]
            selected_item = random.choices(items, weights=weights, k=1)[0]

            embed.description = "🟣 **SPECIAL RAID REWARD!**"
            embed.add_field(name="Item Obtained", value=f"**{selected_item['name']}**", inline=True)
            embed.add_field(name="Estimated Value", value=f"{selected_item['value']:,} GP", inline=True)
        else:
            base_loot_value = random.randint(150_000, 600_000)
            embed.description = "⚪ **Standard Raid Reward**"
            embed.add_field(name="Loot Value", value=f"{base_loot_value:,} GP", inline=True)

        embed.set_footer(text=f"Unique chance for this chest: {purple_chance:.2f}%")
        await interaction.response.send_message(embed=embed)

    # -------------------------------------------------------------------------
    # /cox_calc Command
    # -------------------------------------------------------------------------

    @app_commands.command(
        name="cox_calc",
        description="Calculate exact unique (purple) drop probabilities for a Chambers of Xeric raid.",
    )
    @app_commands.describe(
        party_size="Number of players in the raid party",
        total_points="Combined total team points accumulated",
    )
    async def cox_calc(
        self,
        interaction: discord.Interaction,
        party_size: app_commands.Range[int, 1, 100],
        total_points: app_commands.Range[int, 1, 5_000_000],
    ):
        # OSRS CoX calculation: 1% purple chance per 8,675 points
        total_purple_chance = min((total_points / 8675), 100.0)
        points_per_player = total_points / party_size
        individual_purple_chance = min((points_per_player / 8675), 57.14)

        embed = discord.Embed(
            title="📊 CoX Unique Drop Probability Calculator",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Party Size", value=f"{party_size} player(s)", inline=True)
        embed.add_field(name="Total Team Points", value=f"{total_points:,}", inline=True)
        embed.add_field(name="Avg Points / Player", value=f"{int(points_per_player):,}", inline=True)

        embed.add_field(
            name="🟣 Team Purple Chance",
            value=f"**{total_purple_chance:.2f}%**",
            inline=False,
        )
        embed.add_field(
            name="👤 Individual Purple Chance",
            value=f"**{individual_purple_chance:.2f}%**",
            inline=False,
        )

        embed.add_field(
            name="🏹 Twisted Bow Chance (Team)",
            value=f"**{(total_purple_chance * (2/69)):.3f}%** (1 in {int(100 / (total_purple_chance * (2/69))):,} raids)",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(PvMSimulator(bot))