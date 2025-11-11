import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import threading
from aiohttp import web
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# スラッシュコマンド対応
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# 読み込む Cog 一覧
INITIAL_EXTENSIONS = [
    "cogs.janken",
    "cogs.admin",
    "cogs.achan",
    "cogs.omikuji"
]

# ---------------- Webサーバー（Render用） ----------------
async def handle(request):
    return web.Response(text="Bot is running!")

def start_web_server():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    web.run_app(app, port=int(os.environ.get("PORT", 3000)))

threading.Thread(target=start_web_server).start()
# -----------------------------------------------------------


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"✅ Slash Commands Synced: {len(synced)} commands")
    except Exception as e:
        print(f"❌ Sync error: {e}")


async def main():
    # Cog読み込み
    for ext in INITIAL_EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

    # Bot起動
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
