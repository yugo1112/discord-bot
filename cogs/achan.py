import discord
from discord.ext import commands
import random

class Achan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # 画像＋コメントのセット
        self.ACHAN_DATA = [
            {
                "file": "achan/kuruma.jpg",
                "comment": "車高短プリウスのリアバンパー流されちゃった..."
            },
            
        ]

    @commands.hybrid_command(name="あちゃん", description="ランダムであちゃん画像を送ります")
    async def achan(self, ctx):
        # ランダム選択
        data = random.choice(self.ACHAN_DATA)

        comment = data["comment"]
        file_path = data["file"]

        # 画像読み込み
        file = discord.File(file_path, filename="achan.jpg")
        embed = discord.Embed(description=comment)
        embed.set_image(url="attachment://achan.jpg")

        await ctx.reply(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Achan(bot))
