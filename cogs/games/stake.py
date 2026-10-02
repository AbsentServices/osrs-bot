import random
import discord
from discord import app_commands
from discord.ext import commands
from utils import db


class Stake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stake", description="Stake your GP in an OSRS Whip Duel against the Bot!")
    async def stake(self, interaction: discord.Interaction, wager: int):
        if wager <= 0:
            await interaction.response.send_message("❌ Wager must be greater than 0 GP.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        user_id = interaction.user.id

        if not db.remove_gp(guild_id, user_id, wager):
            await interaction.response.send_message("❌ Insufficient GP balance to stake.", ephemeral=True)
            return

        player_hp = 99
        bot_hp = 99

        # Simulate whip attacks
        turns = 0
        while player_hp > 0 and bot_hp > 0 and turns < 20:
            turns += 1
            p_hit = random.randint(0, 25)
            b_hit = random.randint(0, 25)

            bot_hp = max(0, bot_hp - p_hit)
            player_hp = max(0, player_hp - b_hit)

        if player_hp > bot_hp:
            winnings = wager * 2
            db.add_gp(guild_id, user_id, winnings)
            embed = discord.Embed(
                title="⚔️ Duel Victory!",
                description=f"You defeated the bot in the arena!\n\n"
                            f"❤️ Your HP: **{player_hp}/99**\n🤖 Bot HP: **{bot_hp}/99**\n\n"
                            f"🏆 You won **{winnings:,} GP**!",
                color=discord.Color.gold()
            )
        elif bot_hp > player_hp:
            embed = discord.Embed(
                title="⚔️ Defeated in the Arena!",
                description=f"The bot hit a fat specs and defeated you!\n\n"
                            f"❤️ Your HP: **{player_hp}/99**\n🤖 Bot HP: **{bot_hp}/99**\n\n"
                            f"💀 You lost **{wager:,} GP**.",
                color=discord.Color.red()
            )
        else:
            # Tie scenario -> Refund
            db.add_gp(guild_id, user_id, wager)
            embed = discord.Embed(
                title="⚔️ Double KO!",
                description="Both you and the bot knocked each other out at the same time!\n\n"
                            "🤝 Wager refunded.",
                color=discord.Color.light_grey()
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Stake(bot))