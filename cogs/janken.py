import discord
from discord.ext import commands
import asyncio
import random

class Janken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rounds = {}  # チャンネルごとのラウンド状態

    def get_key(self, ctx):
        return (ctx.guild.id, ctx.channel.id)

    def get_state(self, ctx):
        key = self.get_key(ctx)
        if key not in self.rounds:
            self.rounds[key] = {"players": set(), "task": None}
        return self.rounds[key]

    @commands.hybrid_command(name="janken", description="じゃんけんに参加する（1分後に自動締切）")
    async def janken(self, ctx):
        state = self.get_state(ctx)
        state["players"].add(ctx.author.id)

        # タスクがまだなら起動
        if state["task"] is None:
            state["task"] = asyncio.create_task(self.auto_end(ctx))

        await ctx.reply("✅ 参加登録完了！ 1分後に自動で結果を出します。")

    async def auto_end(self, ctx):
        await asyncio.sleep(60)
        await self.pon(ctx, auto=True)
        state = self.get_state(ctx)
        state["task"] = None

    @commands.hybrid_command(name="pon", description="今すぐ結果を出す")
    async def pon(self, ctx, auto=False):
        state = self.get_state(ctx)

        if not state["players"]:
            await ctx.reply("まだ誰も参加していません。")
            return

        # 自動締切タスクが生きてたら止める
        if state["task"]:
            state["task"].cancel()
            state["task"] = None

        # 手をランダムに決める
        hands = {uid: random.choice(["グー", "チョキ", "パー"]) for uid in state["players"]}
        state["players"].clear()

        # 結果出力
        lines = ["⏰ 自動ぽん！" if auto else "✋ じゃんけん…ぽん！"]
        for uid, hand in hands.items():
            lines.append(f"<@{uid}>：{hand}")

        await ctx.reply("\n".join(lines))

async def setup(bot):
    await bot.add_cog(Janken(bot))
