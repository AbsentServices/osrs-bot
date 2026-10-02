from discord.ext import commands


class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load", description="Load a specific cog extension.")
    @commands.is_owner()
    async def load_cog(self, ctx: commands.Context, extension: str):
        """Example usage: !load cogs.games.flip"""
        try:
            await self.bot.load_extension(extension)
            await ctx.send(f"✅ Successfully loaded extension: `{extension}`")
        except Exception as e:
            await ctx.send(f"❌ Error loading `{extension}`: `{e}`")


async def setup(bot):
    await bot.add_cog(Load(bot))