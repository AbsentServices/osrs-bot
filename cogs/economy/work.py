import random
import time
import discord
from discord import app_commands
from discord.ext import commands

# List of OSRS tasks with (description, min_gp, max_gp, duration_seconds)
OSRS_TASKS = [
    ("mining an inventory of **Runite Ore** at the Heroes' Guild", 250, 600, 1800),      # 30 mins
    ("slaying **Gargoyles** in the Slayer Tower", 300, 750, 3600),                       # 60 mins
    ("chopping down **Magic Trees** in the Woodcutting Guild", 200, 500, 1800),         # 30 mins
    ("fishing a haul of **Raw Sharks** at the Fishing Platform", 180, 450, 1200),        # 20 mins
    ("completing laps of the **Rellekka Rooftop Course**", 150, 400, 900),              # 15 mins
    ("pickpocketing an **Ardougne Knight**", 100, 350, 600),                            # 10 mins
    ("high-alching **Green D'hide Bodies** at the Grand Exchange", 200, 500, 1800),    # 30 mins
    ("crafting a batch of **Wrath Runes** at the True Blood Altar", 350, 800, 3600),    # 60 mins
    ("looting the Barrows chest for **Ahrim's Robe Top**", 500, 1000, 3600),            # 60 mins
    ("killing **Vorkath** for a quick boss trip", 400, 900, 2700),                      # 45 mins
]


class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, "active_work_tasks"):
            bot.active_work_tasks = {}

    @app_commands.command(name="work", description="Start an OSRS task to earn server GP.")
    async def work(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        now = int(time.time())

        # Check if user is already doing a task
        if user_id in self.bot.active_work_tasks:
            task_info = self.bot.active_work_tasks[user_id]
            finish_time = task_info["finish_time"]

            if now < finish_time:
                remaining = finish_time - now
                minutes = remaining // 60
                seconds = remaining % 60
                await interaction.response.send_message(
                    f"⚔️ You are currently busy **{task_info['task']}**!\n"
                    f"Time remaining: **{minutes}m {seconds}s**. Use `/work_claim` when finished.",
                    ephemeral=True
                )
                return
            else:
                await interaction.response.send_message(
                    "✅ Your previous task is already finished! Use `/work_claim` to collect your GP reward.",
                    ephemeral=True
                )
                return

        # Assign a new random OSRS task
        task_desc, min_reward, max_reward, duration = random.choice(OSRS_TASKS)
        reward = random.randint(min_reward, max_reward)
        finish_time = now + duration

        self.bot.active_work_tasks[user_id] = {
            "task": task_desc,
            "reward": reward,
            "finish_time": finish_time
        }

        minutes_total = duration // 60
        embed = discord.Embed(
            title="⚔️ OSRS Task Started!",
            description=f"You have started **{task_desc}**.\n\n"
                        f"⏱️ **Duration:** {minutes_total} minutes\n"
                        f"💰 **Expected Reward:** {reward:,} GP",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Return and use /work_claim when your task is complete!")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Work(bot))