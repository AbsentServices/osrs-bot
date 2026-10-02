import os
import discord
from discord import app_commands
from discord.ext import commands


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _sync_logic(self):
        guild_id = os.getenv("GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.bot.tree.copy_global_to(guild=guild)
            synced = await self.bot.tree.sync(guild=guild)
            return f"✅ Synced **{len(synced)}** commands to guild `{guild_id}`."
        else:
            synced = await self.bot.tree.sync()
            return f"✅ Synced **{len(synced)}** global commands."

    @commands.command(name="sync", description="Sync slash commands manually.")
    @commands.is_owner()
    async def sync_prefix(self, ctx: commands.Context):
        """Prefix command (!sync) to manually force-sync application slash commands."""
        try:
            msg = await self._sync_logic()
            await ctx.send(msg)
        except Exception as e:
            await ctx.send(f"❌ Failed to sync commands: `{e}`")

    @app_commands.command(name="sync", description="Sync slash commands manually.")
    async def sync_slash(self, interaction: discord.Interaction):
        """Slash command (/sync) to manually force-sync application slash commands."""
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("❌ Only the bot owner can use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        try:
            msg = await self._sync_logic()
            await interaction.followup.send(msg, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to sync commands: `{e}`", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Sync(bot))