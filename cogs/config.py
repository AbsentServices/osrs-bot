import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config_group = app_commands.Group(
        name="config",
        description="[Admin] Server settings and shop management commands."
    )

    @config_group.command(name="set_invite_reward", description="Set GP awarded per successful member invite.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def set_invite_reward(self, interaction: discord.Interaction, amount: int):
        if amount < 0:
            await interaction.response.send_message("❌ Amount must be 0 or greater.", ephemeral=True)
            return

        db.update_guild_config(interaction.guild.id, "gp_per_invite", amount)
        await interaction.response.send_message(
            f"✅ Updated invite reward: Users will now receive **{amount:,} GP** per invite in this server."
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

    @config_group.command(name="remove_shop_item", description="Remove an item from the reward shop.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def remove_shop_item(self, interaction: discord.Interaction, item_name: str):
        guild_data = db.get_guild_data(interaction.guild.id)
        shop = guild_data.get("shop", {})

        # Case-insensitive item lookup
        matched_item = next((i for i in shop if i.lower() == item_name.lower()), None)
        if not matched_item:
            await interaction.response.send_message(f"❌ Item `{item_name}` not found in shop.", ephemeral=True)
            return

        del guild_data["shop"][matched_item]
        db.save_guild_data(interaction.guild.id, guild_data)

        await interaction.response.send_message(f"🗑️ Removed **{matched_item}** from the reward shop.")

    @config_group.command(name="view_settings", description="View current server configuration and shop items.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def view_settings(self, interaction: discord.Interaction):
        guild_data = db.get_guild_data(interaction.guild.id)
        config = guild_data.get("config", {})
        shop = guild_data.get("shop", {})

        embed = discord.Embed(
            title=f"⚙️ {interaction.guild.name} Configuration",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Invite Reward Rate",
            value=f"`{config.get('gp_per_invite', 100):,} GP` per invite",
            inline=False
        )

        shop_list = "\n".join([f"• **{item}**: `{price:,} GP`" for item, price in shop.items()]) if shop else "No items in shop."
        embed.add_field(name="Current Shop Items", value=shop_list, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(ConfigCog(bot))