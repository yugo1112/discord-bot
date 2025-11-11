import os
import asyncio
import shlex
import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv
from aiohttp import web

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  # ギルドID（任意）
OWNER_IDS = {int(x) for x in os.getenv("OWNER_IDS", "").split(",") if x}

SAFE_COMMANDS = {
    "uptime": "uptime",
    "date": "date",
    "disk": "df -h",
    "python": "python --version",
}

# Render が渡すポート番号（Web Serviceは絶対必要）
PORT = int(os.getenv("PORT", "10000"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# --- 権限チェック ---
def is_owner(interaction: discord.Interaction) -> bool:
    return not OWNER_IDS or (interaction.user.id in OWNER_IDS)


# --- シェルコマンド実行 ---
async def run_shell(command: str):
    proc = await asyncio.subprocess.create_subprocess_exec(
        *shlex.split(command),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    outs, errs = await proc.communicate()
    return proc.returncode, outs.decode(), errs.decode()


# --- Bot 起動時 ---
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    if GUILD_ID:
        guild = discord.Object(id=int(GUILD_ID))
        await tree.sync(guild=guild)
    else:
        await tree.sync()

    heartbeat.start()


# --- 心拍ログ ---
@tasks.loop(minutes=10)
async def heartbeat():
    print("Heartbeat OK")


# --- Slash Commands ---
@tree.command(name="hello", description="動作確認")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("こんにちは！")


@tree.command(name="ping", description="PING応答")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {client.latency*1000:.1f}ms")


@tree.command(name="exec", description="許可されたコマンドを実行")
@app_commands.describe(name="コマンド名")
@app_commands.choices(name=[app_commands.Choice(name=k, value=k) for k in SAFE_COMMANDS])
async def exec_cmd(interaction: discord.Interaction, name: app_commands.Choice[str]):
    if not is_owner(interaction):
        await interaction.response.send_message("権限がありません。", ephemeral=True)
        return

    cmd = SAFE_COMMANDS[name.value]
    await interaction.response.defer()

    code, out, err = await run_shell(cmd)
    msg = f"**$ {cmd}**\nexit: `{code}`\n"

    if out:
        msg += f"```\n{out}\n```"
    if err:
        msg += f"```\n{err}\n```"

    await interaction.followup.send(msg, ephemeral=True)


# --- Render で必要なミニWebサーバー ---
async def handle_root(request):
    return web.Response(text="discord-bot running")

async def handle_health(request):
    return web.Response(text="healthy")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/healthz", handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    print(f"HTTP server listening on :{PORT}")
    await site.start()

    # 永久稼働
    while True:
        await asyncio.sleep(3600)


# --- メイン ---
if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("環境変数 DISCORD_TOKEN を設定してください")

    async def main():
        bot_task = asyncio.create_task(client.start(TOKEN))
        web_task = asyncio.create_task(start_web())
        await asyncio.gather(bot_task, web_task)

    asyncio.run(main())
