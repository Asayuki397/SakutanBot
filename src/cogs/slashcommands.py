import discord
from discord import app_commands
from discord.ext import commands
from database import insertDB, searchDB

class 슬래시커맨드(commands.Cog, description = "슬래시 커맨드와 관련된 명령어입니다."):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "동기화", description = "[관리자 전용] global 함수를 해당 서버에 동기화합니다.")
    @commands.has_permissions(administrator=True)
    async def 동기화(self,ctx) -> None:
        await ctx.defer()
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild = ctx.guild)
        await ctx.send(f'{len(synced)}개의 커맨드를 동기화했습니다.')
        if searchDB("guilds","id",f"id={ctx.guild.id}") == None:
            insertDB("guilds", "name, id",(ctx.guild.name, ctx.guild.id))
            print(f"신규 서버 {ctx.guild.name}가 등록되었습니다.")

    @commands.hybrid_command(name = "클리어", description = "[관리자 전용] 슬래시 커맨드를 해당 서버에서 제거합니다.")
    @commands.has_permissions(administrator=True)
    async def 클리어(self,ctx) -> None:
        await ctx.defer()
        ctx.bot.tree.clear_commands(guild = ctx.guild)
        await ctx.bot.tree.sync(guild = ctx.guild)
        await ctx.send("완료")
    
async def setup(bot):
    await bot.add_cog(슬래시커맨드(bot))