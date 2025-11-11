import os
import asyncio
import threading
from aiohttp import web
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

INITIAL_EXTENSIONS = [
    "cogs.janken",
    "cogs.admin",
    "cogs.achan",
    "cogs.omikuji"
]

# ========= Web サーバー (Render用) =========
async def handle(request):
    return web.Response(text="Bot is running")

def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)

    port = int(os.environ.get("PORT", 3000))
    print(f"✅ Web server running on port {port}")

    web.run_app(app, port=port)

# ← Bot 起動より前に必ずスレッドで Web Server を実行
threading.Thread(target=start_web_server, daemon=True).start()
# ==============================================


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


async def start_bot():
    for ext in INITIAL_EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"Loaded {ext}")
        except Exception as e:
            print(f"Failed to load {ext}: {e}")

    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(start_bot())
