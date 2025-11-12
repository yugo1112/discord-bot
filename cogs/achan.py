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
                "comment": "リアバンパー流されちゃった..."
            },
            
        ]

    @commands.hybrid_command(name="あちゃん", description="ランダムであちゃん画像を送ります")
    async def achan(self, ctx):
        await ctx.defer()
        send = ctx.followup.send

        data = random.choice(self.ACHAN_DATA)
        file_path = data["file"]
        comment = data["comment"]

        file = discord.File(file_path, filename="achan.jpg")
        embed = discord.Embed(description=comment)
        embed.set_image(url="attachment://achan.jpg")

        await send(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(Achan(bot))
