import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

OSRS_MAPPING_URL = "https://prices.runescape.wiki/api/v1/osrs/mapping"
OSRS_PRICES_URL = "https://prices.runescape.wiki/api/v1/osrs/latest"

class PriceCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ge", description="Check item prices on the OSRS Grand Exchange.")
    async def ge(self, interaction: discord.Interaction, item_name: str):
        await interaction.response.defer()
        
        headers = {"User-Agent": "OSRS_Discord_Bot_Template/1.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            # Get item ID mapping
            async with session.get(OSRS_MAPPING_URL) as resp:
                if resp.status != 200:
                    await interaction.followup.send("❌ Error fetching Wiki data.")
                    return
                mapping = await resp.json()

            target = next((item for item in mapping if item["name"].lower() == item_name.lower()), None)
            if not target:
                await interaction.followup.send(f"❌ Item `{item_name}` not found.")
                return

            item_id = target["id"]
            
            # Fetch latest price
            async with session.get(f"{OSRS_PRICES_URL}?id={item_id}") as resp:
                prices_data = await resp.json()
                item_price = prices_data.get("data", {}).get(str(item_id), {})

            high = item_price.get("high", "N/A")
            low = item_price.get("low", "N/A")

            embed = discord.Embed(title=target["name"], color=discord.Color.green())
            embed.set_thumbnail(url=f"https://oldschool.runescape.wiki/images/{target['name'].replace(' ', '_')}.png")
            embed.add_field(name="High Price (Insta-Buy)", value=f"{high:,} GP" if isinstance(high, int) else high)
            embed.add_field(name="Low Price (Insta-Sell)", value=f"{low:,} GP" if isinstance(low, int) else low)
            
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PriceCheck(bot))