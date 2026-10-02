import discord
from discord import app_commands
from discord.ext import commands

class EventRSVPView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.rsvps = {"DPS": [], "Tank": [], "Healer": [], "Learner": []}

    def _update_embed(self, embed: discord.Embed) -> discord.Embed:
        embed.clear_fields()
        for role, users in self.rsvps.items():
            value = "\n".join([u.mention for u in users]) if users else "None"
            embed.add_field(name=f"{role} ({len(users)})", value=value, inline=True)
        return embed

    async def _handle_rsvp(self, interaction: discord.Interaction, role: str):
        user = interaction.user
        for r_name, users in self.rsvps.items():
            if user in users and r_name != role:
                users.remove(user)
        
        if user in self.rsvps[role]:
            self.rsvps[role].remove(user)
        else:
            self.rsvps[role].append(user)

        embed = self._update_embed(interaction.message.embeds[0])
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="DPS", style=discord.ButtonStyle.primary, custom_id="rsvp_dps")
    async def rsvp_dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._handle_rsvp(interaction, "DPS")

    @discord.ui.button(label="Tank", style=discord.ButtonStyle.success, custom_id="rsvp_tank")
    async def rsvp_tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._handle_rsvp(interaction, "Tank")

    @discord.ui.button(label="Healer", style=discord.ButtonStyle.secondary, custom_id="rsvp_healer")
    async def rsvp_healer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._handle_rsvp(interaction, "Healer")

    @discord.ui.button(label="Learner", style=discord.ButtonStyle.danger, custom_id="rsvp_learner")
    async def rsvp_learner(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._handle_rsvp(interaction, "Learner")


class EventCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, "events_db"):
            bot.events_db = {}

    @app_commands.command(name="event_create", description="Schedule a clan event with role RSVPs.")
    async def event_create(self, interaction: discord.Interaction, title: str, description: str, time: str):
        embed = discord.Embed(
            title=f"📅 Clan Event: {title}",
            description=f"{description}\n\n🕒 **Time:** {time}",
            color=discord.Color.gold()
        )
        embed.add_field(name="DPS (0)", value="None", inline=True)
        embed.add_field(name="Tank (0)", value="None", inline=True)
        embed.add_field(name="Healer (0)", value="None", inline=True)
        embed.add_field(name="Learner (0)", value="None", inline=True)

        view = EventRSVPView()
        await interaction.response.send_message(embed=embed, view=view)
        msg = await interaction.original_response()
        
        self.bot.events_db[msg.id] = {"title": title, "time": time}


async def setup(bot):
    await bot.add_cog(EventCreate(bot))