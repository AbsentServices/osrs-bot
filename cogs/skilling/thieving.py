import random
import discord
from discord import app_commands
from discord.ext import commands

TARGETS = {
    "man": {"name": "Man / Woman", "level_req": 1, "value": 50, "xp": 8.0, "fail_chance": 0.20, "pet_chance": 5000},
    "farmer": {"name": "Master Farmer", "level_req": 38, "value": 650, "xp": 43.0, "fail_chance": 0.35, "pet_chance": 3000},
    "knight": {"name": "Ardougne Knight", "level_req": 55, "value": 1200, "xp": 84.3, "fail_chance": 0.30, "pet_chance": 2000},
    "vyre": {"name": "Vyre Noble", "level_req": 82, "value": 4500, "xp": 300.0, "fail_chance": 0.45, "pet_chance": 1000},
    "elf": {"name": "Prifddinas Elf", "level_req": 85, "value": 6000, "xp": 353.0, "fail_chance": 0.50, "pet_chance": 800},
}


class Thieving(commands.Cog):
    """Thieving skilling commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="pickpocket", description="Pickpocket NPCs across Gielinor for loot and Rocky pet rolls.")
    @app_commands.describe(
        target="Select the NPC target to pickpocket",
        attempts="Number of pickpocket attempts (1-50)"
    )
    @app_commands.choices(
        target=[
            app_commands.Choice(name="Man / Woman (Lvl 1)", value="man"),
            app_commands.Choice(name="Master Farmer (Lvl 38)", value="farmer"),
            app_commands.Choice(name="Ardougne Knight (Lvl 55)", value="knight"),
            app_commands.Choice(name="Vyre Noble (Lvl 82)", value="vyre"),
            app_commands.Choice(name="Prifddinas Elf (Lvl 85)", value="elf"),
        ]
    )
    async def pickpocket(
        self,
        interaction: discord.Interaction,
        target: app_commands.Choice[str],
        attempts: app_commands.Range[int, 1, 50] = 10,
    ):
        target_data = TARGETS[target.value]
        
        successful = 0
        caught = 0

        for _ in range(attempts):
            if random.random() < target_data["fail_chance"]:
                caught += 1
            else:
                successful += 1

        total_gp = successful * target_data["value"]
        total_xp = successful * target_data["xp"]

        pet_obtained = False
        for _ in range(successful):
            if random.randint(1, target_data["pet_chance"]) == 1:
                pet_obtained = True
                break

        embed = discord.Embed(
            title=f"🗝️ Thieving: {target_data['name']}",
            color=discord.Color.dark_purple(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(name="Successful Pickpockets", value=f"**{successful} / {attempts}**", inline=True)
        embed.add_field(name="Caught / Stunned", value=f"**{caught}**", inline=True)
        embed.add_field(name="GP Stolen", value=f"**{total_gp:,} GP**", inline=True)
        embed.add_field(name="XP Gained", value=f"**{total_xp:,.1f} XP**", inline=False)

        if pet_obtained:
            embed.add_field(
                name="🐾 Pet Drop!",
                value="🎉 You have a feeling like you're being followed... **Rocky Pet** unlocked!",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Thieving(bot))