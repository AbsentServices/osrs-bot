import random
import discord
from discord import app_commands
from discord.ext import commands

BOSS_PETS = {
    "zulrah": {"name": "Pet Snakeling", "boss_name": "Zulrah", "chance": 4000, "icon": "🐍"},
    "vorkath": {"name": "Vorki", "boss_name": "Vorkath", "chance": 3000, "icon": "🐉"},
    "jad": {"name": "TzRek-Jad", "boss_name": "TzTok-Jad", "chance": 200, "icon": "🔥"},
    "corp": {"name": "Pet Dark Core", "boss_name": "Corporal Beast", "chance": 5000, "icon": "👻"},
    "kraken": {"name": "Pet Kraken", "boss_name": "Kraken", "chance": 3000, "icon": "🐙"},
    "gwd": {"name": "Pet General Graardor", "boss_name": "General Graardor", "chance": 5000, "icon": "🛡️"},
}


class PetRolls(commands.Cog):
    """Boss Pet Roll Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="pet",
        description="Roll on pet drop chances from iconic OSRS bosses.",
    )
    @app_commands.describe(boss="Select the boss to attempt a pet drop roll")
    @app_commands.choices(
        boss=[
            app_commands.Choice(name="Zulrah (1/4,000)", value="zulrah"),
            app_commands.Choice(name="Vorkath (1/3,000)", value="vorkath"),
            app_commands.Choice(name="TzTok-Jad (1/200)", value="jad"),
            app_commands.Choice(name="Corporal Beast (1/5,000)", value="corp"),
            app_commands.Choice(name="Kraken (1/3,000)", value="kraken"),
            app_commands.Choice(name="General Graardor (1/5,000)", value="gwd"),
        ]
    )
    async def pet(
        self,
        interaction: discord.Interaction,
        boss: app_commands.Choice[str],
    ):
        pet_info = BOSS_PETS[boss.value]
        roll = random.randint(1, pet_info["chance"])
        won_pet = roll == 1

        embed = discord.Embed(
            title=f"{pet_info['icon']} {pet_info['boss_name']} Pet Roll",
            color=discord.Color.green() if won_pet else discord.Color.red(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(name="Drop Rate", value=f"1 / {pet_info['chance']:,}", inline=True)
        embed.add_field(name="Your Roll", value=f"#{roll:,}", inline=True)

        if won_pet:
            embed.description = (
                f"🎉 **YOU HAVE A FEELING LIKE YOU'RE BEING FOLLOWED!**\n\n"
                f"You unlocked the **{pet_info['name']}** pet badge!"
            )
        else:
            embed.description = f"❌ You did not receive the **{pet_info['name']}** pet. Better luck next time!"

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(PetRolls(bot))