import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# 読み込む Cog をリストにする
INITIAL_EXTENSIONS = ["cogs.janken","cogs.admin"]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

async def main():
    for ext in INITIAL_EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"Loaded {ext}")
        except Exception as e:
            print(f"Failed to load {ext}: {e}")

    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

# ---- Render 対策：ダミーWebサーバー ----
from aiohttp import web

async def handle(request):
    return web.Response(text="OK")

def run_dummy_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, port=port)

# 非同期で bot と同時に動かす
async def main():
    # bot
    bot_task = asyncio.create_task(client.start(TOKEN))

    # dummy server
    server_task = asyncio.to_thread(run_dummy_web_server)

    await asyncio.gather(bot_task, server_task)

if __name__ == "__main__":
    asyncio.run(main())
