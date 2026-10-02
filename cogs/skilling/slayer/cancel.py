import discord
from discord import app_commands
from discord.ext import commands
from cogs.skilling.slayer.slayer_data import active_tasks


class SlayerCancel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slayer_cancel", description="Cancel your current Slayer task.")
    async def slayer_cancel(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        if user_id not in active_tasks or active_tasks[user_id]["remaining"] <= 0:
            await interaction.response.send_message("❌ You don't have an active Slayer task to cancel.", ephemeral=True)
            return

        task_name = active_tasks[user_id]["task"]
        del active_tasks[user_id]
        await interaction.response.send_message(f"🗑️ Cancelled your task to kill **{task_name}**.")


async def setup(bot):
    await bot.add_cog(SlayerCancel(bot))