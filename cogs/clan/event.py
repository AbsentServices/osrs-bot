import discord
from discord import app_commands
from discord.ext import commands


class EventRSVP(discord.ui.View):
    def __init__(self, event_name: str, host: discord.User):
        super().__init__(timeout=None)
        self.event_name = event_name
        self.host = host
        self.attending = set()
        self.declined = set()

    @discord.ui.button(label="✅ Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        self.declined.discard(user.display_name)
        self.attending.add(user.display_name)
        await self.update_embed(interaction)

    @discord.ui.button(label="❌ Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        self.attending.discard(user.display_name)
        self.declined.add(user.display_name)
        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        
        attending_str = "\n".join([f"• {u}" for u in self.attending]) if self.attending else "None"
        declined_str = "\n".join([f"• {u}" for u in self.declined]) if self.declined else "None"

        embed.set_field_at(2, name=f"✅ Attending ({len(self.attending)})", value=attending_str, inline=True)
        embed.set_field_at(3, name=f"❌ Declined ({len(self.declined)})", value=declined_str, inline=True)

        await interaction.response.edit_message(embed=embed, view=self)


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="event", description="Create and schedule a clan event with RSVP reaction buttons.")
    @app_commands.describe(
        name="Name of the clan event (e.g. CoX Raid Night, Skill-of-the-Week)",
        time="Scheduled date/time (e.g. Friday @ 8 PM EST)"
    )
    async def event(self, interaction: discord.Interaction, name: str, time: str):
        embed = discord.Embed(
            title=f"🛡️ Clan Event: {name}",
            description="Click the buttons below to RSVP for this event!",
            color=discord.Color.blue()
        )
        embed.add_field(name="👑 Host", value=interaction.user.mention, inline=True)
        embed.add_field(name="⏰ Time", value=time, inline=True)
        embed.add_field(name="✅ Attending (0)", value="None", inline=True)
        embed.add_field(name="❌ Declined (0)", value="None", inline=True)

        view = EventRSVP(event_name=name, host=interaction.user)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Event(bot))