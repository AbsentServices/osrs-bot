import discord
from discord import app_commands
from discord.ext import commands
from cogs.ge.ge_data import get_item_mapping, fetch_latest_price


class GEPrice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ge_price", description="Fetch real-time Grand Exchange prices via the OSRS Wiki API.")
    @app_commands.describe(item_name="The name of the item to look up (e.g. Abyssal whip)")
    async def ge_price(self, interaction: discord.Interaction, item_name: str):
        await interaction.response.defer()

        mapping = await get_item_mapping()
        item_info = mapping.get(item_name.lower())

        if not item_info:
            await interaction.followup.send(f"❌ Item **{item_name}** not found on the Grand Exchange.")
            return

        price_data = await fetch_latest_price(item_info["id"])
        if not price_data:
            await interaction.followup.send(f"❌ Unable to retrieve price data for **{item_info['name']}**.")
            return

        high_price = price_data.get("high")
        low_price = price_data.get("low")
        high_time = price_data.get("highTime")
        low_time = price_data.get("lowTime")

        high_str = f"{high_price:,} GP" if high_price else "N/A"
        low_str = f"{low_price:,} GP" if low_price else "N/A"

        embed = discord.Embed(
            title=f"📈 GE Price: {item_info['name']}",
            url=f"https://prices.runescape.wiki/osrs/item/{item_info['id']}",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=f"https://a.runescape.wiki/images/a/a2/{item_info['name'].replace(' ', '_')}.png")
        embed.add_field(name="🔴 Instant Sell (Low)", value=low_str, inline=True)
        embed.add_field(name="🟢 Instant Buy (High)", value=high_str, inline=True)
        embed.add_field(name="📦 Buy Limit", value=f"{item_info['limit']:,}" if isinstance(item_info['limit'], int) else "N/A", inline=False)
        embed.add_field(name="🪄 High Alch Value", value=f"{item_info['highalch']:,} GP", inline=True)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GEPrice(bot))