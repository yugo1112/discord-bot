import discord
from discord.ext import commands
import random

class Omikuji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # おみくじ結果のリスト（好きに追加できる）
        self.RESULTS = [
            ("大吉", "やったね！最高の1日になるよ！🌟"),
            ("中吉", "なかなか良い運勢だよ！😄"),
            ("小吉", "ちょっといいことがあるかも？✨"),
            ("吉", "平和で穏やかな日になりそう😊"),
            ("末吉", "焦らず行動すると良いことあるよ〜"),
            ("凶", "今日は慎重に…！でも大丈夫、君なら乗り切れる💪"),
            ("大凶", "逆にレア！ここから運気急上昇の予兆かも笑🔥")
        ]

    @commands.hybrid_command(name="おみくじ", description="おみくじを引きます！")
    async def omikuji(self, ctx):
        omikuji, comment = random.choice(self.RESULTS)

        embed = discord.Embed(
            title=f"🎉 おみくじ結果：**{omikuじ}** 🎉",
            description=comment,
            color=discord.Color.gold()
        )

        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Omikuji(bot))
