import json
import os
import asyncio
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import discord
from discord.ext import commands

CONFIG_FILE = "data/web_config.json"

def load_config() -> dict:
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_config(config: dict) -> None:
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


app = FastAPI(title="OSRS Bot Web Dashboard")
templates = Jinja2Templates(directory="templates")
bot_instance: commands.Bot = None


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    config = load_config()
    guilds_data = []

    if bot_instance and bot_instance.is_ready():
        for guild in bot_instance.guilds:
            guild_id = str(guild.id)
            guild_config = config.get(guild_id, {
                "disabled_commands": [],
                "channels": {"news": "", "status": "", "drops": ""}
            })

            text_channels = [
                {"id": str(c.id), "name": c.name} 
                for c in guild.text_channels
            ]
            
            registered_commands = [
                cmd.name for cmd in bot_instance.tree.get_commands()
            ]

            guilds_data.append({
                "id": guild_id,
                "name": guild.name,
                "icon": guild.icon.url if guild.icon else None,
                "channels": text_channels,
                "commands": registered_commands,
                "config": guild_config
            })

    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "guilds": guilds_data}
    )


@app.post("/save/{guild_id}")
async def save_settings(
    guild_id: str, 
    request: Request
):
    form_data = await request.form()
    config = load_config()

    disabled_commands = form_data.getlist("disabled_commands")
    news_channel = form_data.get("channel_news", "")
    status_channel = form_data.get("channel_status", "")
    drops_channel = form_data.get("channel_drops", "")

    config[guild_id] = {
        "disabled_commands": disabled_commands,
        "channels": {
            "news": news_channel,
            "status": status_channel,
            "drops": drops_channel
        }
    }
    save_config(config)

    return HTMLResponse(
        content="<script>alert('Settings updated successfully!'); window.location.href='/';</script>"
    )


class WebServerCog(commands.Cog):
    """Cog that manages the online FastAPI web interface."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        global bot_instance
        bot_instance = bot
        self.server_task = None

    async def cog_load(self):
        config_uvicorn = uvicorn.Config(
            app=app, 
            host="0.0.0.0", 
            port=8000, 
            log_level="warning"
        )
        server = uvicorn.Server(config_uvicorn)
        self.server_task = asyncio.create_task(server.serve())

    async def cog_unload(self):
        if self.server_task:
            self.server_task.cancel()


async def setup(bot: commands.Bot):
    await bot.add_cog(WebServerCog(bot))