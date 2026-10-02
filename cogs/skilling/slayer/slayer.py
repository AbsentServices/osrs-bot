import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db

# Slayer Task Pool: Task Name, Min Kills, Max Kills, Reward GP per kill
SLAYER_MASTERS = {
    "turael": {
        "name": "Turael (Beginner)",
        "min_level": 1,
        "tasks": [
            ("Goblins", 15, 30, 200),
            ("Monkeys", 20, 35, 250),
            ("Skeletons", 15, 25, 300)
        ]
    },
    "vannaaka": {
        "name": "Vannaka (Intermediate)",
        "min_level": 1,
        "tasks": [
            ("Hill Giants", 30, 60, 800),
            ("Hellhounds", 40, 70, 1200),
            ("Ankou", 35, 65, 1000)
        ]
    },
    "duradel": {
        "name": "Duradel (Master)",
        "min_level": 1,
        "tasks": [
            ("Abyssal Demons", 50, 100, 3500),
            ("Dark Beasts", 40, 80, 4500),
            ("Rune Dragons", 20, 40, 8000)
        ]
    }
}

# In-memory storage for active tasks: {user_id: {"task": str, "remaining": int, "reward_per_kill": int}}
active_tasks = {}


class Slayer(commands.Cog):
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
    await bot.add_cog(Slayer(bot))