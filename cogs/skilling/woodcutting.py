import random
import discord
from discord import app_commands
from discord.ext import commands

TREES = {
    "oak": {"name": "Oak Tree", "level_req": 15, "log_value": 40, "xp": 37.5, "pet_chance": 5000},
    "willow": {"name": "Willow Tree", "level_req": 30, "log_value": 20, "xp": 67.5, "pet_chance": 4000},
    "maple": {"name": "Maple Tree", "level_req": 45, "log_value": 80, "xp": 100.0, "pet_chance": 3000},
    "yew": {"name": "Yew Tree", "level_req": 60, "log_value": 280, "xp": 175.0, "pet_chance": 2000},
    "magic": {"name": "Magic Tree", "level_req": 75, "log_value": 1100, "xp": 250.0, "pet_chance": 1000},
}


class Woodcutting(commands.Cog):
    """Woodcutting skilling commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chop", description="Chop trees to gather logs and earn server GP.")
    @app_commands.describe(
        tree="Select the type of tree to chop",
        quantity="Number of logs to chop (1-50)"
    )
    @app_commands.choices(
        tree=[
            app_commands.Choice(name="Oak Tree (Lvl 15)", value="oak"),
            app_commands.Choice(name="Willow Tree (Lvl 30)", value="willow"),
            app_commands.Choice(name="Maple Tree (Lvl 45)", value="maple"),
            app_commands.Choice(name="Yew Tree (Lvl 60)", value="yew"),
            app_commands.Choice(name="Magic Tree (Lvl 75)", value="magic"),
        ]
    )
    async def chop(
        self,
        interaction: discord.Interaction,
        tree: app_commands.Choice[str],
        quantity: app_commands.Range[int, 1, 50] = 10,
    ):
        tree_data = TREES[tree.value]
        logs_chopped = sum(1 for _ in range(quantity) if random.random() > 0.15)
        total_gp = logs_chopped * tree_data["log_value"]
        total_xp = logs_chopped * tree_data["xp"]

        pet_obtained = False
        for _ in range(logs_chopped):
            if random.randint(1, tree_data["pet_chance"]) == 1:
                pet_obtained = True
                break

        embed = discord.Embed(
            title=f"🪓 Woodcutting: {tree_data['name']}",
            color=discord.Color.dark_green(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        embed.add_field(name="Logs Chopped", value=f"**{logs_chopped} / {quantity}**", inline=True)
        embed.add_field(name="GP Earned", value=f"**{total_gp:,} GP**", inline=True)
        embed.add_field(name="XP Gained", value=f"**{total_xp:,.1f} XP**", inline=True)

        if pet_obtained:
            embed.add_field(
                name="🐾 Pet Drop!",
                value="🎉 You have a feeling like you're being followed... **Beaver Pet** unlocked!",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Woodcutting(bot))