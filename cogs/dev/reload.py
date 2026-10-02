from discord.ext import commands


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload", description="Reload a specific cog extension.")
    @commands.is_owner()
    async def reload_cog(self, ctx: commands.Context, extension: str):
        """Example usage: !reload cogs.games.stake or !reload cogs.economy.work"""
        try:
            await self.bot.reload_extension(extension)
            await ctx.send(f"🔄 Successfully reloaded extension: `{extension}`")
        except Exception as e:
            await ctx.send(f"❌ Error reloading `{extension}`: `{e}`")


async def setup(bot):
    await bot.add_cog(Reload(bot))