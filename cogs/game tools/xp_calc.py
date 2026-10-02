import math
import discord
from discord import app_commands
from discord.ext import commands

class XpCalc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="xp_calc", description="Calculate remaining actions needed to reach a target level.")
    async def xp_calc(self, interaction: discord.Interaction, current_xp: int, target_level: int, xp_per_action: int):
        XP_TABLE = [
            0, 83, 174, 276, 388, 512, 650, 801, 969, 1154, 1358, 1584, 1833, 2107, 2411, 2746, 3116, 3523, 3972, 4467,
            5013, 5614, 6276, 7006, 7808, 8689, 9654, 10708, 11858, 13109, 14468, 15941, 17537, 19263, 21129, 23142,
            25312, 27649, 30161, 32858, 35752, 38854, 42175, 45728, 49527, 53586, 57920, 62545, 67477, 72731, 78326,
            84280, 90612, 97342, 104493, 112086, 120143, 128688, 137742, 147329, 157471, 168192, 179516, 191468,
            204073, 217358, 231351, 246081, 261578, 277872, 294996, 312982, 331862, 351669, 372437, 394200, 417000,
            440878, 465878, 492042, 519414, 548040, 577966, 609240, 641911, 676030, 711647, 748814, 787585, 828014,
            870158, 914075, 959825, 1007468, 1057068, 1108685, 1162380, 1218218, 1276267, 1336588, 1399245, 1464308,
            1531848, 1601938, 1674653, 1750068, 1828259, 1909303, 1993278, 2080263, 2170338, 2263584, 2360083, 2459918,
            2563174, 2669938, 2780299, 2894348, 3012177, 3133880, 3259553, 3389295, 3523204, 3661381, 3803928, 3950947,
            4102542, 4258818, 4419881, 4585838, 4756801, 4932882, 5114194, 5300851, 5492968, 5690662, 5894050, 6103251,
            6318385, 6539575, 6766945, 7000621, 7240728, 7487392, 7740739, 8000898, 8268000, 8542178, 8823565, 9112297,
            9408510, 9712342, 10023932, 10343420, 10670949, 11006663, 11350708, 11703230, 12064375, 12434293, 12813133,
            13034431
        ]

        if target_level < 1 or target_level > 99:
            await interaction.response.send_message("❌ Target level must be between 1 and 99.", ephemeral=True)
            return

        target_xp = XP_TABLE[target_level - 1]
        remaining_xp = target_xp - current_xp

        if remaining_xp <= 0:
            await interaction.response.send_message("🎉 You have already reached or surpassed this target level!")
            return

        actions_needed = math.ceil(remaining_xp / xp_per_action)
        embed = discord.Embed(title="📈 OSRS XP Calculator", color=discord.Color.teal())
        embed.add_field(name="Target Level", value=f"`Level {target_level}`", inline=True)
        embed.add_field(name="XP Remaining", value=f"`{remaining_xp:,} XP`", inline=True)
        embed.add_field(name="Actions Required", value=f"`{actions_needed:,}` actions", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(XpCalc(bot))