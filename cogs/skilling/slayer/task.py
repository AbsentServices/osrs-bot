import random
import discord
from discord import app_commands
from discord.ext import commands
from cogs.skilling.slayer.slayer_data import SLAYER_MASTERS, active_tasks


class SlayerTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slayer_task", description="Get assigned a new Slayer task from a Slayer Master!")
    @app_commands.choices(master=[
        app_commands.Choice(name="Turael (Low Level)", value="turael"),
        app_commands.Choice(name="Vannaka (Mid Level)", value="vannaaka"),
        app_commands.Choice(name="Duradel (High Level)", value="duradel")
    ])
    async def slayer_task(self, interaction: discord.Interaction, master: str):
        user_id = interaction.user.id

        if user_id in active_tasks and active_tasks[user_id]["remaining"] > 0:
            current = active_tasks[user_id]
            await interaction.response.send_message(
                f"❌ You already have an active Slayer task! Kill **{current['remaining']}x {current['task']}** first using `/slayer_kill`.",
                ephemeral=True
            )
            return

        master_info = SLAYER_MASTERS[master]
        task_name, min_k, max_k, gp_per_kill = random.choice(master_info["tasks"])
        count = random.randint(min_k, max_k)

        active_tasks[user_id] = {
            "task": task_name,
            "remaining": count,
            "reward_per_kill": gp_per_kill
        }

        embed = discord.Embed(
            title="📜 Slayer Task Assigned!",
            description=f"**{master_info['name']}** has assigned you to kill:\n\n"
                        f"🎯 **{count}x {task_name}**\n"
                        f"💰 **Estimated Value:** {count * gp_per_kill:,} GP",
            color=discord.Color.dark_green()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SlayerTask(bot))