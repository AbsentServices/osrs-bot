import discord
from discord import app_commands
from discord.ext import commands
from cogs.ge.ge_data import get_item_mapping, fetch_latest_price


class GEMargin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ge_margin", description="View flipping margins and profit potential per item.")
    @app_commands.describe(item_name="The item name to calculate margins for")
    async def ge_margin(self, interaction: discord.Interaction, item_name: str):
        await interaction.response.defer()

        mapping = await get_item_mapping()
        item_info = mapping.get(item_name.lower())

        if not item_info:
            await interaction.followup.send(f"❌ Item **{item_name}** not found.")
            return

        price_data = await fetch_latest_price(item_info["id"])
        if not price_data or not price_data.get("high") or not price_data.get("low"):
            await interaction.followup.send(f"❌ Incomplete price data available for **{item_info['name']}**.")
            return

        high_price = price_data["high"]
        low_price = price_data["low"]

        # OSRS GE Tax calculation (2% tax capped at 5M per item)
        tax = min(int(high_price * 0.02), 5_000_000)
        margin = high_price - low_price
        profit_per_item = margin - tax

        limit = item_info["limit"]
        max_profit_str = f"{profit_per_item * limit:,} GP" if isinstance(limit, int) else "N/A"

        embed = discord.Embed(
            title=f"📊 Flipping Margin: {item_info['name']}",
            url=f"https://prices.runescape.wiki/osrs/item/{item_info['id']}",
            color=discord.Color.green() if profit_per_item > 0 else discord.Color.red()
        )
        embed.add_field(name="📥 Buy Price (Low)", value=f"{low_price:,} GP", inline=True)
        embed.add_field(name="📤 Sell Price (High)", value=f"{high_price:,} GP", inline=True)
        embed.add_field(name="🏛️ GE Tax (2%)", value=f"-{tax:,} GP", inline=False)
        embed.add_field(name="💰 Net Profit / Item", value=f"**{profit_per_item:,} GP**", inline=True)
        embed.add_field(name="📦 Limit Profit (1 Buy Limit)", value=max_profit_str, inline=True)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GEMargin(bot))