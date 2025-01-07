from discord.ext import commands
from embed import create_embed
from discord import app_commands

class 백준(commands.Cog, description = ""):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "백준", description = "백준 문제 풀이를 올릴 수 있습니다.")
    @app_commands.describe(status = "현재 문제 풀이 상태 (예 : 질문, 해결, 실패)")
    @app_commands.describe(number = "문제 번호")
    @app_commands.describe(code = "코드 복붙")
    async def 백준(self, ctx, status, number, code):
        if status == "질문": status = "❓질문"
        elif status == "해결": status = "✅해결"
        elif status == "실패" : status = "❌실패"
        data = dict(status=status, number=number, code="`"+code+"`")
        embed = create_embed(ctx, data)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(백준(bot))
