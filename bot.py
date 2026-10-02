import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.invites = True


class OSRSBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        cogs_dir = "./cogs"

        # Recursively scan and load all cogs and subfolder cogs (e.g., cogs/game_tools/)
        for root, _, files in os.walk(cogs_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    rel_path = os.path.relpath(os.path.join(root, file), start=".")
                    # Convert file path to module path (e.g. cogs/game_tools/slayer_task.py -> cogs.game_tools.slayer_task)
                    module_path = rel_path[:-3].replace(os.sep, ".")
                    
                    try:
                        await self.load_extension(module_path)
                        print(f"Loaded extension: {module_path}")
                    except Exception as e:
                        print(f"Failed to load extension {module_path}: {e}")

        # Sync slash commands across global or guild scopes
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"Synced commands to guild {GUILD_ID}")
        else:
            await self.tree.sync()
            print("Synced global commands.")

    async def on_ready(self):
        print(f"Bot online as {self.user} (ID: {self.user.id})")


bot = OSRSBot()

if __name__ == "__main__":
    bot.run(TOKEN)