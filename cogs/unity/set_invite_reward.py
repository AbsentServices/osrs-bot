import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class SetInviteReward(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config_group = app_commands.Group(
        name="config",
        description="[Admin] Server settings and shop management commands."
    )

    @config_group.command(name="set_invite_reward", description="Set GP awarded per successful member invite.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def set_invite_reward(self, interaction: discord.Interaction, amount: int):
        if amount < 0:
            await interaction.response.send_message("❌ Amount must be 0 or greater.", ephemeral=True)
            return

        db.update_guild_config(interaction.guild.id, "gp_per_invite", amount)
        await interaction.response.send_message(
            f"✅ Updated invite reward: Users will now receive **{amount:,} GP** per invite in this server."
        )


async def setup(bot):
    await bot.add_cog(SetInviteReward(bot))