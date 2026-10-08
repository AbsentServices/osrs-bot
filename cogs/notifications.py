import json
import os
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks

DATA_FILE = "data/notifications.json"


def load_config() -> dict:
    """Load notification channel configurations from JSON file."""
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_config(config: dict) -> None:
    """Save notification channel configurations to JSON file."""
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(DATA_FILE, "w") as f:
        json.dump(config, f, indent=4)


class Notifications(commands.Cog):
    """Cog for automated background feeds and webhook alerts."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = load_config()
        self.last_news_title = None
        
        # Start background polling tasks
        self.check_osrs_news.start()
        self.check_server_status.start()

    def cog_unload(self):
        """Cancel background tasks when the cog unloads."""
        self.check_osrs_news.cancel()
        self.check_server_status.cancel()

    # -------------------------------------------------------------------------
    # Slash Commands
    # -------------------------------------------------------------------------

    feed_group = app_commands.Group(
        name="feed", 
        description="Configure automated feeds and webhook alert channels"
    )

    @feed_group.command(
        name="set_channel", 
        description="Configure dedicated announcement channels for automated OSRS feeds"
    )
    @app_commands.describe(
        feed_type="The type of alert feed to configure",
        channel="The channel where updates will be posted"
    )
    @app_commands.choices(feed_type=[
        app_commands.Choice(name="JMod Tweets & News", value="news"),
        app_commands.Choice(name="OSRS Live Updates / Maintenance", value="status"),
        app_commands.Choice(name="Clan Drop Logs (RuneLite Webhook)", value="drops")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def set_channel(
        self, 
        interaction: discord.Interaction, 
        feed_type: app_commands.Choice[str], 
        channel: discord.TextChannel
    ):
        guild_id = str(interaction.guild_id)

        if guild_id not in self.config:
            self.config[guild_id] = {}

        self.config[guild_id][feed_type.value] = channel.id
        save_config(self.config)

        embed = discord.Embed(
            title="🔔 Notification Channel Updated",
            description=f"Successfully set **{feed_type.name}** alerts to post in {channel.mention}.",
            color=discord.Color.green()
        )

        if feed_type.value == "drops":
            webhook_url = f"https://your-bot-domain.com/api/drops/{guild_id}"
            embed.add_field(
                name="📦 RuneLite Integration Setup",
                value=(
                    f"To connect your clan drops, add this HTTP Endpoint in your "
                    f"RuneLite **Loot Logger / Discord Webhooks** plugin:\n"
                    f"`{webhook_url}`"
                ),
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @set_channel.error
    async def set_channel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ You need **Administrator** permissions to configure notification channels.",
                ephemeral=True
            )

    # -------------------------------------------------------------------------
    # Background Tasks & Webhook Dispatchers
    # -------------------------------------------------------------------------

    @tasks.loop(minutes=15)
    async def check_osrs_news(self):
        """Poll the official OSRS News API/RSS for new blog posts."""
        url = "https://secure.runescape.com/m=news/latest_news.json?osrs=true"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if not data:
                            return
                        
                        latest_article = data[0]
                        title = latest_article.get("title")
                        link = latest_article.get("url")
                        summary = latest_article.get("summary")

                        # Prevent duplicate postings
                        if title == self.last_news_title:
                            return
                        
                        self.last_news_title = title

                        # Build embed
                        embed = discord.Embed(
                            title=f"📰 {title}",
                            url=link,
                            description=summary,
                            color=discord.Color.gold()
                        )
                        embed.set_author(name="Old School RuneScape News", icon_url="https://oldschool.runescape.wiki/images/f/f0/Coins_10000.png")

                        # Dispatch to all configured channels
                        for guild_id, channels in self.config.items():
                            if "news" in channels:
                                target_channel = self.bot.get_channel(channels["news"])
                                if target_channel:
                                    await target_channel.send(content="🚨 **New OSRS Game Update / Blog Post!**", embed=embed)
            except Exception as e:
                print(f"[Notifications Cog] Error checking OSRS news: {e}")

    @tasks.loop(minutes=5)
    async def check_server_status(self):
        """Simulate polling server status/maintenance endpoints."""
        # Custom logic or OSRS status API endpoint can be added here
        pass

    @check_osrs_news.before_loop
    @check_server_status.before_loop
    async def before_tasks(self):
        await self.bot.wait_until_ready()

    # -------------------------------------------------------------------------
    # Helper Method for External Drop Webhooks (RuneLite Plugin Listener)
    # -------------------------------------------------------------------------

    async def dispatch_clan_drop(self, guild_id: int, player_name: str, item_name: str, item_value: int, image_url: str = None):
        """Method to trigger a loot drop notification from an API endpoint or HTTP server."""
        guild_str = str(guild_id)
        if guild_str not in self.config or "drops" not in self.config[guild_str]:
            return

        channel_id = self.config[guild_str]["drops"]
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return

        embed = discord.Embed(
            title="🎉 Rare Clan Drop Obtains!",
            description=f"**{player_name}** received a drop: **{item_name}**!",
            color=discord.Color.purple()
        )
        embed.add_field(name="Estimated Value", value=f"{item_value:,} GP", inline=True)
        if image_url:
            embed.set_thumbnail(url=image_url)

        await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Notifications(bot))