import random
import discord
from discord import app_commands
from discord.ext import commands

BARS = {
    "bronze": {"name": "Bronze Bar", "level_req": 1, "bar_value": 80, "xp": 12.5},
    "iron": {"name": "Iron Bar", "level_req": 15, "bar_value": 180, "xp": 25.0},
    "steel": {"name": "Steel Bar", "level_req": 30, "bar_value": 450, "xp": 37.5},
    "mithril": {"name": "Mithril Bar", "level_req": 50, "bar_value": 1200, "xp": 50.0},
    "adamant": {"name": "Adamantite Bar", "level_req": 70, "bar_value": 2800, "xp": 62.5},
    "runite": {"name": "Rune Bar", "level_req": 85, "bar_value": 12500, "xp": 75.0},
}


class Smithing(commands.Cog):
    """Smithing skilling commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="smith", description="Smelt ores or hammer metal bars into gear for GP and XP.")
    @app_commands.describe(
        bar="Select the metal bar type to smith",
        quantity="Number of bars to smith (1-50)"
    )
    @app_commands.choices(
        bar=[
            app_commands.Choice(name="Bronze Bar (Lvl 1)", value="bronze"),
            app_commands.Choice(name="Iron Bar (Lvl 15)", value="iron"),
            app_commands.Choice(name="Steel Bar (Lvl 30)", value="steel"),
            app_commands.Choice(name="Mithril Bar (Lvl 50)", value="mithril"),
            app_commands.Choice(name="Adamantite Bar (Lvl 70)", value="adamant"),
            app_commands.Choice(name="Rune Bar (Lvl 85)", value="runite"),
        ]
    )
    async def smith(
        self,
        interaction: discord.Interaction,
        bar: app_commands.Choice[str],
        quantity: app_commands.Range[int, 1, 50] = 10,
    ):
        bar_data = BARS[bar.value]
        
        # Iron bar smelting chance emulation (80% success rate without Ring of Forging)
        if bar.value == "iron":
            succeeded = sum(1 for _ in range(quantity) if random.random() > 0.20)
        else:
            succeeded = quantity

        total_gp = succeeded * bar_data["bar_value"]
        total_xp = succeeded * bar_data["xp"]

        embed = discord.Embed(
            title=f"🔨 Smithing: {bar_data['name']}",
            color=discord.Color.dark_grey(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(name="Bars Smelted", value=f"**{succeeded} / {quantity}**", inline=True)
        embed.add_field(name="GP Earned", value=f"**{total_gp:,} GP**", inline=True)
        embed.add_field(name="XP Gained", value=f"**{total_xp:,.1f} XP**", inline=True)

        if bar.value == "iron" and succeeded < quantity:
            embed.set_footer(text=f"Failed to smelt {quantity - succeeded} iron ores into usable bars.")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Smithing(bot))