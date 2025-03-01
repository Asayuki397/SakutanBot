from discord.ext import commands
from embed import create_embed
from discord import app_commands
from proto import llm_chat

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
        data = dict(상태 = status, 문제번호 = number)
        embed = create_embed("백준", data)
        await ctx.send(embed=embed)

        response = await llm_chat(self.bot, f"나는 이 알고리즘 문제에 대해 이야기하고 있어. 이 문제는 현재 {status} 상태야. 수정 전 코드를 반드시 먼저 적은 다음 코멘트를 달아줘. 수정할 부분이 있다면 수정 후 코드를 수정 전 코드 아래에 추가로 작성해도 좋아 \n{code}")
        if len(response) >= 1900: 
            responses = response.split("\n")
            for response in responses:
                if not response:
                    continue()
                await ctx.send(response)
        else: await ctx.send(response)

async def setup(bot):
    await bot.add_cog(백준(bot))
