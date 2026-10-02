import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class ViewSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config_group = app_commands.Group(
        name="config",
        description="[Admin] Server settings and shop management commands."
    )

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
    await bot.add_cog(ViewSettings(bot))