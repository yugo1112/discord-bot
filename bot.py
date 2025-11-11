import os
import asyncio
from aiohttp import web
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)  # hybrid_command用にOK

INITIAL_EXTENSIONS = [
    "cogs.janken",
    "cogs.admin",
    "cogs.achan",
    "cogs.omikuji",
]

# ------------ Render用: ダミーWebサーバーを"同じイベントループ"で起動 ------------
async def handle_root(request):
    return web.Response(text="Bot is running")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle_root)

    port = int(os.environ.get("PORT", 3000))
    runner = web.AppRunner(app)              # run_appは使わない（シグナル問題回避）
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"✅ HTTP server listening on :{port}")

    # ループを生かし続ける
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await runner.cleanup()
# -----------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash Commands Synced: {len(synced)}")
    except Exception as e:
        print(f"❌ Sync error: {e}")

async def main():
    # 1) まずWebサーバーを起動（Renderのポート検出を通す）
    web_task = asyncio.create_task(start_web())

    # 2) Cogを読み込み
    for ext in INITIAL_EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

    # 3) Botを起動（ブロッキングするので別タスクに）
    bot_task = asyncio.create_task(bot.start(TOKEN))

    # Botが終わったらWebも終了
    try:
        await bot_task
    finally:
        web_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await web_task

if __name__ == "__main__":
    import contextlib
    asyncio.run(main())
