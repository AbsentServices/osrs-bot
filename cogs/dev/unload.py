from discord.ext import commands


class Unload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unload", description="Unload a specific cog extension.")
    @commands.is_owner()
    async def unload_cog(self, ctx: commands.Context, extension: str):
        """Example usage: !unload cogs.games.flip"""
        try:
            await self.bot.unload_extension(extension)
            await ctx.send(f"⏹️ Successfully unloaded extension: `{extension}`")
        except Exception as e:
            await ctx.send(f"❌ Error unloading `{extension}`: `{e}`")


async def setup(bot):
    await bot.add_cog(Unload(bot))