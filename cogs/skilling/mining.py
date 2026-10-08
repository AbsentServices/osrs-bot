import random
import discord
from discord import app_commands
from discord.ext import commands

ROCKS = {
    "iron": {"name": "Iron Ore", "level_req": 15, "value": 150, "xp": 35.0, "gem_chance": 50},
    "coal": {"name": "Coal Ore", "level_req": 30, "value": 200, "xp": 50.0, "gem_chance": 40},
    "mithril": {"name": "Mithril Ore", "level_req": 55, "value": 600, "xp": 80.0, "gem_chance": 30},
    "adamant": {"name": "Adamantite Ore", "level_req": 70, "value": 1100, "xp": 95.0, "gem_chance": 20},
    "runite": {"name": "Runite Ore", "level_req": 85, "value": 11200, "xp": 125.0, "gem_chance": 10},
}


class Mining(commands.Cog):
    """Mining skilling commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mine", description="Mine rock veins for ores and precious gems.")
    @app_commands.describe(
        rock="Select the rock vein to mine",
        quantity="Number of ores to mine (1-50)"
    )
    @app_commands.choices(
        rock=[
            app_commands.Choice(name="Iron Ore (Lvl 15)", value="iron"),
            app_commands.Choice(name="Coal Ore (Lvl 30)", value="coal"),
            app_commands.Choice(name="Mithril Ore (Lvl 55)", value="mithril"),
            app_commands.Choice(name="Adamantite Ore (Lvl 70)", value="adamant"),
            app_commands.Choice(name="Runite Ore (Lvl 85)", value="runite"),
        ]
    )
    async def mine(
        self,
        interaction: discord.Interaction,
        rock: app_commands.Choice[str],
        quantity: app_commands.Range[int, 1, 50] = 10,
    ):
        rock_data = ROCKS[rock.value]
        ores_mined = sum(1 for _ in range(quantity) if random.random() > 0.20)
        gems_found = sum(1 for _ in range(ores_mined) if random.randint(1, rock_data["gem_chance"]) == 1)

        total_gp = (ores_mined * rock_data["value"]) + (gems_found * 2500)
        total_xp = ores_mined * rock_data["xp"]

        embed = discord.Embed(
            title=f"⛏️ Mining: {rock_data['name']}",
            color=discord.Color.dark_gold(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(name="Ores Mined", value=f"**{ores_mined} / {quantity}**", inline=True)
        embed.add_field(name="GP Earned", value=f"**{total_gp:,} GP**", inline=True)
        embed.add_field(name="XP Gained", value=f"**{total_xp:,.1f} XP**", inline=True)

        if gems_found > 0:
            embed.add_field(
                name="💎 Uncut Gems Found!",
                value=f"You unearthed **{gems_found}x** uncut gems while mining!",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Mining(bot))