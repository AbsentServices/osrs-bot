import time
import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class WorkClaim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, "active_work_tasks"):
            bot.active_work_tasks = {}

    @app_commands.command(name="work_claim", description="Claim your GP reward after finishing an OSRS task.")
    async def work_claim(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        now = int(time.time())

        # Verify user has an active task
        if user_id not in self.bot.active_work_tasks:
            await interaction.response.send_message(
                "❌ You do not have an active OSRS task! Start one using `/work`.",
                ephemeral=True
            )
            return

        task_info = self.bot.active_work_tasks[user_id]
        finish_time = task_info["finish_time"]

        # Check if the task duration has completed
        if now < finish_time:
            remaining = finish_time - now
            minutes = remaining // 60
            seconds = remaining % 60
            await interaction.response.send_message(
                f"⌛ Your task is not complete yet!\n"
                f"You are still **{task_info['task']}**.\n"
                f"Come back in **{minutes}m {seconds}s**.",
                ephemeral=True
            )
            return

        # Task completed -> Award GP and remove task
        reward = task_info["reward"]
        task_desc = task_info["task"]
        guild_id = interaction.guild.id

        db.add_gp(guild_id, user_id, reward)
        del self.bot.active_work_tasks[user_id]

        embed = discord.Embed(
            title="🎁 OSRS Task Completed & Claimed!",
            description=f"You finished **{task_desc}** and earned **{reward:,} GP**!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(WorkClaim(bot))