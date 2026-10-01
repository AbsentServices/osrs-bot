import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class TicketPurchaseModal(discord.ui.Modal, title="Purchase Raffle Tickets"):
    amount_input = discord.ui.TextInput(
        label="Number of Tickets",
        default="1",
        min_length=1,
        max_length=5,
        required=True
    )

    def __init__(self, raffle_id: str, ticket_price: int):
        super().__init__()
        self.raffle_id = raffle_id
        self.ticket_price = ticket_price

    async def on_submit(self, interaction: discord.Interaction):
        try:
            amount = int(self.amount_input.value.strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid number.", ephemeral=True)
            return

        total_cost = self.ticket_price * amount
        guild_id = interaction.guild.id

        if db.remove_gp(guild_id, interaction.user.id, total_cost):
            guild_data = db.get_guild_data(guild_id)
            raffle = guild_data.get("raffles", {}).get(self.raffle_id)

            if not raffle:
                await interaction.response.send_message("❌ This raffle no longer exists.", ephemeral=True)
                return

            raffle["tickets"].extend([interaction.user.id] * amount)
            db.save_guild_data(guild_id, guild_data)

            new_balance = db.get_gp(guild_id, interaction.user.id)
            await interaction.response.send_message(
                f"🎟️ Purchased **{amount:,} ticket(s)** for Raffle **#{self.raffle_id}**!\n"
                f"💰 Remaining GP in server: **{new_balance:,} GP**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("❌ You do not have enough GP in this server.", ephemeral=True)


class RaffleView(discord.ui.View):
    def __init__(self, raffle_id: str, ticket_price: int):
        super().__init__(timeout=None)
        self.raffle_id = raffle_id
        self.ticket_price = ticket_price

    @discord.ui.button(label="Buy Ticket(s)", style=discord.ButtonStyle.primary, emoji="🎟️")
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_data = db.get_guild_data(interaction.guild.id)
        if self.raffle_id not in guild_data.get("raffles", {}):
            await interaction.response.send_message("❌ This raffle has ended.", ephemeral=True)
            return

        modal = TicketPurchaseModal(raffle_id=self.raffle_id, ticket_price=self.ticket_price)
        await interaction.response.send_modal(modal)


class RaffleSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create_raffle", description="[Admin] Start a new raffle.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def create_raffle(self, interaction: discord.Interaction, prize: str, ticket_price: int):
        guild_data = db.get_guild_data(interaction.guild.id)
        raffle_id = str(len(guild_data["raffles"]) + 1)

        guild_data["raffles"][raffle_id] = {
            "prize": prize,
            "ticket_price": ticket_price,
            "tickets": []
        }
        db.save_guild_data(interaction.guild.id, guild_data)

        embed = discord.Embed(
            title=f"🎟️ Raffle #{raffle_id}",
            description=f"Prize: **{prize}**\nPrice per ticket: **{ticket_price:,} GP**",
            color=discord.Color.purple()
        )
        view = RaffleView(raffle_id=raffle_id, ticket_price=ticket_price)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="draw_raffle", description="[Admin] Draw a raffle winner.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def draw_raffle(self, interaction: discord.Interaction, raffle_id: str):
        guild_data = db.get_guild_data(interaction.guild.id)
        raffle = guild_data["raffles"].get(raffle_id)

        if not raffle or not raffle["tickets"]:
            await interaction.response.send_message("❌ Raffle not found or no tickets were bought.", ephemeral=True)
            return

        winner_id = random.choice(raffle["tickets"])
        winner = self.bot.get_user(winner_id) or await self.bot.fetch_user(winner_id)

        del guild_data["raffles"][raffle_id]
        db.save_guild_data(interaction.guild.id, guild_data)

        await interaction.response.send_message(
            f"🎉 **Raffle #{raffle_id} Winner!**\nCongratulations {winner.mention}, you won **{raffle['prize']}**!"
        )


async def setup(bot):
    await bot.add_cog(RaffleSystem(bot))