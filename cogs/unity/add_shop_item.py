import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class AddShopItem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config_group = app_commands.Group(
        name="config",
        description="[Admin] Server settings and shop management commands."
    )

    @config_group.command(name="add_shop_item", description="Add or update an item in the reward shop.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def add_shop_item(self, interaction: discord.Interaction, item_name: str, price: int):
        if price <= 0:
            await interaction.response.send_message("❌ Price must be greater than 0.", ephemeral=True)
            return

        guild_data = db.get_guild_data(interaction.guild.id)
        guild_data["shop"][item_name] = price
        db.save_guild_data(interaction.guild.id, guild_data)

        await interaction.response.send_message(
            f"✅ **{item_name}** has been added/updated in the shop for **{price:,} GP**."
        )


async def setup(bot):
    await bot.add_cog(AddShopItem(bot))