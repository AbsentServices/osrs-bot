import discord
from discord import app_commands
from discord.ext import commands
from utils import db
from cogs.skilling.slayer.slayer_data import active_tasks


class SlayerKill(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slayer_kill", description="Slay monsters toward your current Slayer task!")
    async def slayer_kill(self, interaction: discord.Interaction, kills: int = 1):
        user_id = interaction.user.id
        guild_id = interaction.guild.id

        if user_id not in active_tasks or active_tasks[user_id]["remaining"] <= 0:
            await interaction.response.send_message("❌ You don't have an active Slayer task. Use `/slayer_task` to get one!", ephemeral=True)
            return

        if kills <= 0:
            await interaction.response.send_message("❌ You must kill at least 1 monster.", ephemeral=True)
            return

        task = active_tasks[user_id]
        actual_kills = min(kills, task["remaining"])
        task["remaining"] -= actual_kills
        earned_gp = actual_kills * task["reward_per_kill"]

        db.add_gp(guild_id, user_id, earned_gp)

        if task["remaining"] == 0:
            del active_tasks[user_id]
            embed = discord.Embed(
                title="⚔️ Slayer Task Completed!",
                description=f"You slew the final **{actual_kills}x {task['task']}**!\n\n"
                            f"🎉 Task Completed! You earned **{earned_gp:,} GP**.",
                color=discord.Color.gold()
            )
        else:
            embed = discord.Embed(
                title="⚔️ Slayer Progress",
                description=f"You slain **{actual_kills}x {task['task']}** and earned **{earned_gp:,} GP**!\n\n"
                            f"Remaining: **{task['remaining']}x {task['task']}**",
                color=discord.Color.blue()
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SlayerKill(bot))