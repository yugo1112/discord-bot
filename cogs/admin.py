import discord
from discord.ext import commands
import os

# OWNER_IDS を .env から読み取る
OWNER_IDS = {int(x) for x in os.getenv("OWNER_IDS", "").split(",") if x}

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 権限チェック
    async def cog_check(self, ctx):
        return ctx.author.id in OWNER_IDS

    @commands.hybrid_command(name="say", description="Bot に喋らせる（管理者専用）")
    async def say(self, ctx, *, message: str):
        await ctx.reply("✅ 発言しました！", ephemeral=True)
        await ctx.channel.send(message)

    @commands.hybrid_command(name="reload", description="Cog を再読み込み（管理者専用）")
    async def reload(self, ctx, cog: str = "cogs.janken"):
        try:
            await self.bot.reload_extension(cog)
            await ctx.reply(f"✅ {cog} を再読み込みしました！")
        except Exception as e:
            await ctx.reply(f"❌ エラー: {e}")

    @commands.hybrid_command(name="shutdown", description="Bot を停止（管理者専用）")
    async def shutdown(self, ctx):
        await ctx.reply("🛑 Bot を停止します…")
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Admin(bot))
