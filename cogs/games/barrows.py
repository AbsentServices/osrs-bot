import random
import discord
from discord import app_commands
from discord.ext import commands

BARROWS_ITEMS = [
    # Ahrim
    {"name": "Ahrim's Hood", "value": 150_000},
    {"name": "Ahrim's Robetop", "value": 2_800_000},
    {"name": "Ahrim's Robeskirt", "value": 2_200_000},
    {"name": "Ahrim's Staff", "value": 80_000},
    # Dharok
    {"name": "Dharok's Helm", "value": 400_000},
    {"name": "Dharok's Platebody", "value": 1_200_000},
    {"name": "Dharok's Platelegs", "value": 1_800_000},
    {"name": "Dharok's Greataxe", "value": 600_000},
    # Guthan
    {"name": "Guthan's Helm", "value": 250_000},
    {"name": "Guthan's Platebody", "value": 500_000},
    {"name": "Guthan's Chainskirt", "value": 450_000},
    {"name": "Guthan's Warspear", "value": 650_000},
    # Karil
    {"name": "Karil's Coif", "value": 80_000},
    {"name": "Karil's Leathertop", "value": 1_600_000},
    {"name": "Karil's Leatherskirt", "value": 750_000},
    {"name": "Karil's Crossbow", "value": 120_000},
    # Torag
    {"name": "Torag's Helm", "value": 180_000},
    {"name": "Torag's Platebody", "value": 350_000},
    {"name": "Torag's Platelegs", "value": 400_000},
    {"name": "Torag's Hammers", "value": 70_000},
    # Verac
    {"name": "Verac's Helm", "value": 220_000},
    {"name": "Verac's Brassard", "value": 450_000},
    {"name": "Verac's Plateskirt", "value": 380_000},
    {"name": "Verac's Flail", "value": 200_000},
]


class BarrowsMinigame(commands.Cog):
    """Barrows Chest Simulator Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="barrows",
        description="Open a Barrows chest simulator after defeating all 6 brothers.",
    )
    async def barrows(self, interaction: discord.Interaction):
        items_obtained = []

        # 6 rolls total (1/15 chance per roll when 6 brothers slain)
        for _ in range(6):
            if random.randint(1, 15) == 1:
                piece = random.choice(BARROWS_ITEMS)
                items_obtained.append(piece)

        rune_value = random.randint(15_000, 60_000)
        total_value = rune_value + sum(item["value"] for item in items_obtained)

        embed = discord.Embed(
            title="⚰️ Barrows Chest Opened!",
            color=discord.Color.dark_purple(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(name="Brothers Slain", value="6 / 6", inline=True)
        embed.add_field(name="Potential Value", value=f"**{total_value:,} GP**", inline=True)

        if items_obtained:
            item_text = "\n".join(
                [f"🟣 **{item['name']}** ({item['value']:,} GP)" for item in items_obtained]
            )
            embed.add_field(name="🛡️ Barrows Equipment", value=item_text, inline=False)
        else:
            embed.add_field(
                name="🔮 Runes & Bolt Racks",
                value=f"• Blood, Death, & Mind Runes ({rune_value:,} GP)",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(BarrowsMinigame(bot))