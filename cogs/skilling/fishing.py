import random
import discord
from discord import app_commands
from discord.ext import commands

FISH_SPOTS = {
    "trout": {"name": "Trout", "level_req": 20, "value": 60, "xp": 50.0, "pet_chance": 5000},
    "lobster": {"name": "Lobster", "level_req": 40, "value": 180, "xp": 90.0, "pet_chance": 4000},
    "swordfish": {"name": "Swordfish", "level_req": 50, "value": 320, "xp": 100.0, "pet_chance": 3000},
    "monkfish": {"name": "Monkfish", "level_req": 62, "value": 420, "xp": 120.0, "pet_chance": 2500},
    "shark": {"name": "Shark", "level_req": 76, "value": 850, "xp": 110.0, "pet_chance": 1500},
    "angler": {"name": "Anglerfish", "level_req": 82, "value": 1600, "xp": 120.0, "pet_chance": 1000},
}


class Fishing(commands.Cog):
    """Fishing skilling commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="fish", description="Cast your line at fishing spots across Gielinor.")
    @app_commands.describe(
        fish="Select the target fish to catch",
        quantity="Number of fish to attempt catching (1-50)"
    )
    @app_commands.choices(
        fish=[
            app_commands.Choice(name="Trout (Lvl 20)", value="trout"),
            app_commands.Choice(name="Lobster (Lvl 40)", value="lobster"),
            app_commands.Choice(name="Swordfish (Lvl 50)", value="swordfish"),
            app_commands.Choice(name="Monkfish (Lvl 62)", value="monkfish"),
            app_commands.Choice(name="Shark (Lvl 76)", value="shark"),
            app_commands.Choice(name="Anglerfish (Lvl 82)", value="angler"),
        ]
    )
    async def fish(
        self,
        interaction: discord.Interaction,
        fish: app_commands.Choice[str],
        quantity: app_commands.Range[int, 1, 50] = 10,
    ):
        fish_data = FISH_SPOTS[fish.value]
        fish_caught = sum(1 for _ in range(quantity) if random.random() > 0.18)
        total_gp = fish_caught * fish_data["value"]
        total_xp = fish_caught * fish_data["xp"]

        pet_obtained = False
        for _ in range(fish_caught):
            if random.randint(1, fish_data["pet_chance"]) == 1:
                pet_obtained = True
                break

        embed = discord.Embed(
            title=f"🎣 Fishing: {fish_data['name']}",
            color=discord.Color.blue(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(name="Fish Caught", value=f"**{fish_caught} / {quantity}**", inline=True)
        embed.add_field(name="GP Earned", value=f"**{total_gp:,} GP**", inline=True)
        embed.add_field(name="XP Gained", value=f"**{total_xp:,.1f} XP**", inline=True)

        if pet_obtained:
            embed.add_field(
                name="🐾 Pet Drop!",
                value="🎉 You have a feeling like you're being followed... **Herbi / Heron Pet** unlocked!",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fishing(bot))