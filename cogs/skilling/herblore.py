import random
import discord
from discord import app_commands
from discord.ext import commands

POTIONS = {
    "attack": {"name": "Attack Potion", "level_req": 3, "value": 300, "xp": 25.0},
    "prayer": {"name": "Prayer Potion", "level_req": 38, "value": 8500, "xp": 87.5},
    "super_stat": {"name": "Super Strength Potion", "level_req": 55, "value": 4200, "xp": 125.0},
    "super_restore": {"name": "Super Restore Potion", "level_req": 63, "value": 11500, "xp": 142.5},
    "saradomin_brew": {"name": "Saradomin Brew", "level_req": 81, "value": 9800, "xp": 180.0},
    "super_combat": {"name": "Super Combat Potion", "level_req": 90, "value": 18500, "xp": 150.0},
}


class Herblore(commands.Cog):
    """Herblore skilling commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mix", description="Mix herbs and secondary ingredients into valuable potions.")
    @app_commands.describe(
        potion="Select the potion recipe to brew",
        quantity="Number of potions to brew (1-50)"
    )
    @app_commands.choices(
        potion=[
            app_commands.Choice(name="Attack Potion (Lvl 3)", value="attack"),
            app_commands.Choice(name="Prayer Potion (Lvl 38)", value="prayer"),
            app_commands.Choice(name="Super Strength (Lvl 55)", value="super_stat"),
            app_commands.Choice(name="Super Restore (Lvl 63)", value="super_restore"),
            app_commands.Choice(name="Saradomin Brew (Lvl 81)", value="saradomin_brew"),
            app_commands.Choice(name="Super Combat (Lvl 90)", value="super_combat"),
        ]
    )
    async def mix(
        self,
        interaction: discord.Interaction,
        potion: app_commands.Choice[str],
        quantity: app_commands.Range[int, 1, 50] = 10,
    ):
        potion_data = POTIONS[potion.value]
        
        total_gp = quantity * potion_data["value"]
        total_xp = quantity * potion_data["xp"]

        embed = discord.Embed(
            title=f"🧪 Herblore: {potion_data['name']}",
            color=discord.Color.purple(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(name="Potions Brewed", value=f"**{quantity}**", inline=True)
        embed.add_field(name="GP Earned", value=f"**{total_gp:,} GP**", inline=True)
        embed.add_field(name="XP Gained", value=f"**{total_xp:,.1f} XP**", inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Herblore(bot))