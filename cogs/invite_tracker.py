import discord
from discord.ext import commands
from utils import db

GP_PER_INVITE = 100

class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Mapping: {guild_id: [discord.Invite]}
        self.invites = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        try:
            self.invites[guild.id] = await guild.invites()
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        old_invites = self.invites.get(guild.id, [])
        
        try:
            new_invites = await guild.invites()
            self.invites[guild.id] = new_invites
        except discord.Forbidden:
            return

        for invite in old_invites:
            new_inv = discord.utils.get(new_invites, code=invite.code)
            if new_inv and new_inv.uses > invite.uses:
                inviter = invite.inviter
                if inviter and not inviter.bot:
                    db.add_gp(guild.id, inviter.id, GP_PER_INVITE)
                    print(f"[{guild.name}] Awarded {GP_PER_INVITE} GP to {inviter.name} for inviting {member.name}")
                break

async def setup(bot):
    await bot.add_cog(InviteTracker(bot))