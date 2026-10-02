import discord
from discord import app_commands
from discord.ext import commands
from utils import db

class ShopSelect(discord.ui.Select):
    def __init__(self, shop_items: dict):
        options = [
            discord.SelectOption(
                label=item_name,
                description=f"Cost: {price:,} GP",
                value=item_name,
                emoji="🪙"
            )
            for item_name, price in shop_items.items()
        ]
        super().__init__(
            placeholder="Choose an item from the shop...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="shop_item_select"
        )

    async def callback(self, interaction: discord.Interaction):
        selected_item = self.values[0]
        guild_data = db.get_guild_data(interaction.guild.id)
        price = guild_data.get("shop", {}).get(selected_item)

        if price is None:
            await interaction.response.send_message(
                "❌ Selected item is no longer available in this server's shop.",
                ephemeral=True
            )
            return

        user_gp = db.get_gp(interaction.guild.id, interaction.user.id)
        confirm_view = PurchaseConfirmView(item_name=selected_item, price=price)

        embed = discord.Embed(
            title="🛒 Confirm Purchase",
            description=f"Are you sure you want to buy **{selected_item}**?",
            color=discord.Color.gold()
        )
        embed.add_field(name="Price", value=f"`{price:,} GP`", inline=True)
        embed.add_field(name="Your Balance", value=f"`{user_gp:,} GP`", inline=True)

        await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=True)


class PurchaseConfirmView(discord.ui.View):
    def __init__(self, item_name: str, price: int):
        super().__init__(timeout=60)
        self.item_name = item_name
        self.price = price

    @discord.ui.button(label="Confirm Purchase", style=discord.ButtonStyle.success, emoji="✅")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if db.remove_gp(interaction.guild.id, interaction.user.id, self.price):
            new_balance = db.get_gp(interaction.guild.id, interaction.user.id)
            embed = discord.Embed(
                title="🎉 Purchase Successful!",
                description=f"You purchased **{self.item_name}** for **{self.price:,} GP**.",
                color=discord.Color.green()
            )
            embed.add_field(name="Remaining Balance", value=f"`{new_balance:,} GP`", inline=False)
            self.stop()
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.edit_message(
                content="❌ Transaction failed: Insufficient GP in this server.",
                embed=None,
                view=None
            )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary, emoji="✖️")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.response.edit_message(content="🚫 Purchase canceled.", embed=None, view=None)


class ShopView(discord.ui.View):
    def __init__(self, shop_items: dict):
        super().__init__(timeout=None)
        self.add_item(ShopSelect(shop_items))

    @discord.ui.button(label="Check Balance", style=discord.ButtonStyle.primary, emoji="💰", row=1)
    async def check_balance(self, interaction: discord.Interaction, button: discord.ui.Button):
        gp = db.get_gp(interaction.guild.id, interaction.user.id)
        await interaction.response.send_message(f"💰 You have **{gp:,} GP** in this server.", ephemeral=True)


class RewardShop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shop", description="Open this server's OSRS reward shop.")
    @app_commands.guild_only()
    async def shop(self, interaction: discord.Interaction):
        guild_data = db.get_guild_data(interaction.guild.id)
        items = guild_data.get("shop", {})

        if not items:
            await interaction.response.send_message("❌ The reward shop is empty.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"⚔️ {interaction.guild.name} Reward Shop",
            description="Select an item from the menu below to purchase with your GP.",
            color=discord.Color.gold()
        )
        for item, price in items.items():
            embed.add_field(name=item, value=f"`{price:,} GP`", inline=False)

        await interaction.response.send_message(embed=embed, view=ShopView(items))


async def setup(bot):
    await bot.add_cog(RewardShop(bot))