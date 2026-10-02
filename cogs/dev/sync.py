import os
import discord
from discord.ext import commands


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync", description="Sync slash commands manually.")
    @commands.is_owner()
    async def sync_commands(self, ctx: commands.Context):
        """Prefix command (!sync) to manually force-sync application slash commands."""
        guild_id = os.getenv("GUILD_ID")
        try:
            if guild_id:
                guild = discord.Object(id=int(guild_id))
                self.bot.tree.copy_global_to(guild=guild)
                synced = await self.bot.tree.sync(guild=guild)
                await ctx.send(f"✅ Synced **{len(synced)}** commands to guild `{guild_id}`.")
            else:
                synced = await self.bot.tree.sync()
                await ctx.send(f"✅ Synced **{len(synced)}** global commands.")
        except Exception as e:
            await ctx.send(f"❌ Failed to sync commands: `{e}`")


async def setup(bot):
    await bot.add_cog(Sync(bot))