import random
import discord
from discord import app_commands
from discord.ext import commands

RECIPES = {
    "shrimp": {"name": "Raw Shrimp", "level_req": 1, "value": 40, "xp": 30.0, "burn_chance": 0.25},
    "trout": {"name": "Raw Trout", "level_req": 15, "value": 70, "xp": 70.0, "burn_chance": 0.20},
    "lobster": {"name": "Raw Lobster", "level_req": 40, "value": 220, "xp": 120.0, "burn_chance": 0.15},
    "swordfish": {"name": "Raw Swordfish", "level_req": 50, "value": 380, "xp": 140.0, "burn_chance": 0.12},
    "shark": {"name": "Raw Shark", "level_req": 80, "value": 1100, "xp": 210.0, "burn_chance": 0.08},
    "angler": {"name": "Raw Anglerfish", "level_req": 84, "value": 1900, "xp": 230.0, "burn_chance": 0.05},
}


class Cooking(commands.Cog):
    """Cooking skilling commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cook", description="Cook raw food on a range or fire.")
    @app_commands.describe(
        food="Select the raw food to cook",
        quantity="Number of raw food items to cook (1-50)"
    )
    @app_commands.choices(
        food=[
            app_commands.Choice(name="Shrimp (Lvl 1)", value="shrimp"),
            app_commands.Choice(name="Trout (Lvl 15)", value="trout"),
            app_commands.Choice(name="Lobster (Lvl 40)", value="lobster"),
            app_commands.Choice(name="Swordfish (Lvl 50)", value="swordfish"),
            app_commands.Choice(name="Shark (Lvl 80)", value="shark"),
            app_commands.Choice(name="Anglerfish (Lvl 84)", value="angler"),
        ]
    )
    async def cook(
        self,
        interaction: discord.Interaction,
        food: app_commands.Choice[str],
        quantity: app_commands.Range[int, 1, 50] = 10,
    ):
        food_data = RECIPES[food.value]
        
        cooked_successfully = 0
        burned_food = 0

        for _ in range(quantity):
            if random.random() < food_data["burn_chance"]:
                burned_food += 1
            else:
                cooked_successfully += 1

        total_gp = cooked_successfully * food_data["value"]
        total_xp = cooked_successfully * food_data["xp"]

        embed = discord.Embed(
            title=f"🍳 Cooking: {food_data['name']}",
            color=discord.Color.red(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(name="Successfully Cooked", value=f"**{cooked_successfully}**", inline=True)
        embed.add_field(name="Burned", value=f"**{burned_food}**", inline=True)
        embed.add_field(name="GP Value", value=f"**{total_gp:,} GP**", inline=True)
        embed.add_field(name="XP Gained", value=f"**{total_xp:,.1f} XP**", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Cooking(bot))