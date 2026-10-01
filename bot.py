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
        # Dynamically load all cogs inside cogs/ directory
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                extension = f"cogs.{filename[:-3]}"
                await self.load_extension(extension)
                print(f"Loaded extension: {extension}")

        # Sync slash commands
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