import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class TicketPurchaseModal(discord.ui.Modal, title="Purchase Raffle Tickets"):
    """Modal popup allowing users to specify ticket quantity."""

    amount_input = discord.ui.TextInput(
        label="Number of Tickets",
        placeholder="Enter quantity (e.g., 1, 5, 10)...",
        default="1",
        min_length=1,
        max_length=5,
        required=True
    )

    def __init__(self, raffle_id: str, ticket_price: int, parent_view: "RaffleView"):
        super().__init__()
        self.raffle_id = raffle_id
        self.ticket_price = ticket_price
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            amount = int(self.amount_input.value.strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            await interaction.response.send_message(
                "❌ Please enter a valid positive whole number.",
                ephemeral=True
            )
            return

        total_cost = self.ticket_price * amount
        if db.remove_gp(interaction.user.id, total_cost):
            data = db.load_db()
            raffle = data["raffles"].get(self.raffle_id)

            if not raffle:
                await interaction.response.send_message("❌ This raffle no longer exists.", ephemeral=True)
                return

            raffle["tickets"].extend([interaction.user.id] * amount)
            db.save_db(data)

            new_balance = db.get_gp(interaction.user.id)
            total_tickets = len(raffle["tickets"])

            # Update the original raffle embed counter
            if interaction.message:
                embed = interaction.message.embeds[0]
                embed.set_field_at(
                    index=2,
                    name="Total Tickets Sold",
                    value=f"`{total_tickets:,}`",
                    inline=True
                )
                await interaction.message.edit(embed=embed)

            await interaction.response.send_message(
                f"🎟️ Successfully purchased **{amount:,} ticket(s)** for Raffle **#{self.raffle_id}**!\n"
                f"💰 Spent: **{total_cost:,} GP** | Remaining Balance: **{new_balance:,} GP**",
                ephemeral=True
            )
        else:
            current_gp = db.get_gp(interaction.user.id)
            await interaction.response.send_message(
                f"❌ Insufficient GP. Buying **{amount} ticket(s)** costs **{total_cost:,} GP**, "
                f"but you only have **{current_gp:,} GP**.",
                ephemeral=True
            )


class RaffleView(discord.ui.View):
    """Persistent view with buttons attached to active raffle messages."""

    def __init__(self, raffle_id: str, ticket_price: int):
        super().__init__(timeout=None)
        self.raffle_id = raffle_id
        self.ticket_price = ticket_price

        # Assign custom ID to button for discord.py persistence across restarts
        self.buy_button.custom_id = f"raffle_buy:{raffle_id}"

    @discord.ui.button(label="Buy Ticket(s)", style=discord.ButtonStyle.primary, emoji="🎟️")
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = db.load_db()
        if self.raffle_id not in data.get("raffles", {}):
            await interaction.response.send_message("❌ This raffle has ended or was removed.", ephemeral=True)
            return

        modal = TicketPurchaseModal(
            raffle_id=self.raffle_id,
            ticket_price=self.ticket_price,
            parent_view=self
        )
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="My Tickets", style=discord.ButtonStyle.secondary, emoji="📊", custom_id="raffle_check_tickets")
    async def my_tickets(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = db.load_db()
        raffle = data.get("raffles", {}).get(self.raffle_id)

        if not raffle:
            await interaction.response.send_message("❌ This raffle is no longer active.", ephemeral=True)
            return

        user_tickets = raffle["tickets"].count(interaction.user.id)
        total_tickets = len(raffle["tickets"])
        chance = (user_tickets / total_tickets * 100) if total_tickets > 0 else 0.0

        await interaction.response.send_message(
            f"📊 **Raffle #{self.raffle_id} Entry Details:**\n"
            f"• Your Tickets: **{user_tickets:,}**\n"
            f"• Total Tickets: **{total_tickets:,}**\n"
            f"• Current Win Chance: **{chance:.2f}%**",
            ephemeral=True
        )


class RaffleSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create_raffle", description="[Admin] Start a new interactive raffle.")
    @app_commands.checks.has_permissions(administrator=True)
    async def create_raffle(self, interaction: discord.Interaction, prize: str, ticket_price: int):
        data = db.load_db()
        raffle_id = str(len(data["raffles"]) + 1)

        data["raffles"][raffle_id] = {
            "prize": prize,
            "ticket_price": ticket_price,
            "tickets": []
        }
        db.save_db(data)

        embed = discord.Embed(
            title=f"🎟️ OSRS Raffle #{raffle_id}",
            description=f"A new raffle has started! Click **Buy Ticket(s)** below to enter.",
            color=discord.Color.purple()
        )
        embed.add_field(name="Prize", value=f"🏆 **{prize}**", inline=False)
        embed.add_field(name="Ticket Price", value=f"`{ticket_price:,} GP`", inline=True)
        embed.add_field(name="Total Tickets Sold", value="`0`", inline=True)
        embed.set_footer(text="Earn GP by inviting friends or checking the reward shop!")

        view = RaffleView(raffle_id=raffle_id, ticket_price=ticket_price)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="draw_raffle", description="[Admin] Draw a winner and conclude a raffle.")
    @app_commands.checks.has_permissions(administrator=True)
    async def draw_raffle(self, interaction: discord.Interaction, raffle_id: str):
        data = db.load_db()
        raffle = data["raffles"].get(raffle_id)

        if not raffle:
            await interaction.response.send_message("❌ Raffle ID not found.", ephemeral=True)
            return

        if not raffle["tickets"]:
            del data["raffles"][raffle_id]
            db.save_db(data)
            await interaction.response.send_message(
                f"❌ Raffle **#{raffle_id}** ended with zero tickets sold. No winner drawn."
            )
            return

        winner_id = random.choice(raffle["tickets"])
        winner = self.bot.get_user(winner_id) or await self.bot.fetch_user(winner_id)

        del data["raffles"][raffle_id]
        db.save_db(data)

        embed = discord.Embed(
            title=f"🎉 Raffle #{raffle_id} Winner!",
            description=f"Congratulations {winner.mention}, you won **{raffle['prize']}**!",
            color=discord.Color.gold()
        )
        embed.add_field(name="Total Entries", value=f"`{len(raffle['tickets']):,}` tickets", inline=True)
        embed.add_field(name="Winner ID", value=f"`{winner.id}`", inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(RaffleSystem(bot))