import discord
from discord.ext import commands
from utils import db


class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
                    # Dynamically read server config rate
                    config = db.get_guild_config(guild.id)
                    gp_reward = config.get("gp_per_invite", 100)

                    db.add_gp(guild.id, inviter.id, gp_reward)
                    print(f"[{guild.name}] Awarded {gp_reward} GP to {inviter.name} for inviting {member.name}")
                break


async def setup(bot):
    await bot.add_cog(InviteTracker(bot))