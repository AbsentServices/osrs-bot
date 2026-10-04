import discord
from discord import app_commands
from discord.ext import commands


class Split(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="split", description="Calculate raid loot splits accounting for team size and coffer tax.")
    @app_commands.describe(
        total_loot="Total value of the loot drop in GP",
        team_size="Number of party members in the raid",
        coffer_tax_percent="Optional percentage tax reserved for the clan coffer (default 0%)"
    )
    async def split(self, interaction: discord.Interaction, total_loot: int, team_size: int, coffer_tax_percent: float = 0.0):
        if total_loot <= 0 or team_size <= 0:
            await interaction.response.send_message("❌ Total loot and team size must be greater than 0.", ephemeral=True)
            return

        if coffer_tax_percent < 0 or coffer_tax_percent > 50:
            await interaction.response.send_message("❌ Coffer tax percentage must be between 0% and 50%.", ephemeral=True)
            return

        coffer_amount = int(total_loot * (coffer_tax_percent / 100))
        distributable_loot = total_loot - coffer_amount
        share_per_player = distributable_loot // team_size
        remainder = distributable_loot % team_size

        embed = discord.Embed(
            title="⚔️ Raid Loot Split Calculator",
            color=discord.Color.gold()
        )
        embed.add_field(name="💰 Total Loot", value=f"{total_loot:,} GP", inline=True)
        embed.add_field(name="👥 Team Size", value=f"{team_size} players", inline=True)
        embed.add_field(name="🏛️ Clan Coffer Tax", value=f"{coffer_tax_percent}% ({coffer_amount:,} GP)", inline=False)
        embed.add_field(name="🎉 Share Per Player", value=f"**{share_per_player:,} GP**", inline=False)

        if remainder > 0:
            embed.set_footer(text=f"Note: {remainder:,} GP leftover from division rounding.")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Split(bot))