import time
import discord
from discord import app_commands
from discord.ext import commands

SEEDS = {
    "potato": {"name": "Potato Seed", "level_req": 1, "growth_seconds": 300, "base_yield": 8, "crop_value": 40, "xp": 14.0},
    "sweetcorn": {"name": "Sweetcorn Seed", "level_req": 20, "growth_seconds": 1200, "base_yield": 10, "crop_value": 150, "xp": 38.5},
    "ranarr": {"name": "Ranarr Seed", "level_req": 32, "growth_seconds": 2400, "base_yield": 7, "crop_value": 7500, "xp": 80.5},
    "watermelon": {"name": "Watermelon Seed", "level_req": 47, "growth_seconds": 3600, "base_yield": 12, "crop_value": 800, "xp": 120.0},
    "snapdragon": {"name": "Snapdragon Seed", "level_req": 62, "growth_seconds": 4800, "base_yield": 8, "crop_value": 12000, "xp": 142.0},
    "torstol": {"name": "Torstol Seed", "level_req": 85, "growth_seconds": 7200, "base_yield": 9, "crop_value": 18000, "xp": 224.5},
}

# In-memory storage for user farming plots (In production, replace or back by db.py)
USER_PLOTS = {}


class Farming(commands.Cog):
    """Farming skilling commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    farm_group = app_commands.Group(name="farm", description="Plant and harvest crops for Farming XP and GP.")

    @farm_group.command(name="plant", description="Plant a seed in your farming patch.")
    @app_commands.describe(seed="Select the seed type to plant")
    @app_commands.choices(
        seed=[
            app_commands.Choice(name="Potato Seed (Lvl 1 - 5 mins)", value="potato"),
            app_commands.Choice(name="Sweetcorn Seed (Lvl 20 - 20 mins)", value="sweetcorn"),
            app_commands.Choice(name="Ranarr Seed (Lvl 32 - 40 mins)", value="ranarr"),
            app_commands.Choice(name="Watermelon Seed (Lvl 47 - 60 mins)", value="watermelon"),
            app_commands.Choice(name="Snapdragon Seed (Lvl 62 - 80 mins)", value="snapdragon"),
            app_commands.Choice(name="Torstol Seed (Lvl 85 - 120 mins)", value="torstol"),
        ]
    )
    async def plant(self, interaction: discord.Interaction, seed: app_commands.Choice[str]):
        user_id = interaction.user.id
        now = int(time.time())

        # Check if plot is already occupied
        if user_id in USER_PLOTS:
            plot = USER_PLOTS[user_id]
            growth_time = SEEDS[plot["seed"]]["growth_seconds"]
            ready_timestamp = plot["planted_at"] + growth_time

            if now < ready_timestamp:
                embed = discord.Embed(
                    title="🌱 Patch Occupied",
                    description=f"You already have **{SEEDS[plot['seed']]['name']}** growing!\nHarvest ready: <t:{ready_timestamp}:R>.",
                    color=discord.Color.orange(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        # Plant new seed
        USER_PLOTS[user_id] = {
            "seed": seed.value,
            "planted_at": now,
        }

        seed_data = SEEDS[seed.value]
        ready_timestamp = now + seed_data["growth_seconds"]

        embed = discord.Embed(
            title="🌱 Seed Planted!",
            description=f"You planted **{seed_data['name']}** in your farming patch.",
            color=discord.Color.green(),
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="Harvest Ready", value=f"<t:{ready_timestamp}:F> (<t:{ready_timestamp}:R>)", inline=False)

        await interaction.response.send_message(embed=embed)

    @farm_group.command(name="harvest", description="Harvest mature crops from your farming patch.")
    async def harvest(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        now = int(time.time())

        if user_id not in USER_PLOTS:
            embed = discord.Embed(
                title="🌾 Empty Patch",
                description="You don't have any crops planted right now. Use `/farm plant` to plant a seed!",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        plot = USER_PLOTS[user_id]
        seed_data = SEEDS[plot["seed"]]
        ready_timestamp = plot["planted_at"] + seed_data["growth_seconds"]

        if now < ready_timestamp:
            embed = discord.Embed(
                title="⏳ Crops Still Growing",
                description=f"Your **{seed_data['name']}** isn't fully grown yet!\nReady: <t:{ready_timestamp}:R>.",
                color=discord.Color.gold(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Calculate rewards and clear plot
        yield_count = seed_data["base_yield"]
        total_gp = yield_count * seed_data["crop_value"]
        total_xp = yield_count * seed_data["xp"]

        del USER_PLOTS[user_id]

        embed = discord.Embed(
            title="🧑‍🌾 Crop Harvested!",
            description=f"You harvested your patch of **{seed_data['name']}**!",
            color=discord.Color.dark_green(),
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="Yield", value=f"**{yield_count}x Crops**", inline=True)
        embed.add_field(name="GP Earned", value=f"**{total_gp:,} GP**", inline=True)
        embed.add_field(name="XP Gained", value=f"**{total_xp:,.1f} XP**", inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Farming(bot))