import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class RemoveShopItem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config_group = app_commands.Group(
        name="config",
        description="[Admin] Server settings and shop management commands."
    )

    @config_group.command(name="remove_shop_item", description="Remove an item from the reward shop.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def remove_shop_item(self, interaction: discord.Interaction, item_name: str):
        guild_data = db.get_guild_data(interaction.guild.id)
        shop = guild_data.get("shop", {})

        matched_item = next((i for i in shop if i.lower() == item_name.lower()), None)
        if not matched_item:
            await interaction.response.send_message(f"❌ Item `{item_name}` not found in shop.", ephemeral=True)
            return

        del guild_data["shop"][matched_item]
        db.save_guild_data(interaction.guild.id, guild_data)

        await interaction.response.send_message(f"🗑️ Removed **{matched_item}** from the reward shop.")


async def setup(bot):
    await bot.add_cog(RemoveShopItem(bot))