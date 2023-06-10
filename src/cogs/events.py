import discord
from discord.ext import commands
from database import *

class 이벤트(commands.Cog, description = ""):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = guild.system_channel
        if channel is not None:
            await channel.send("안녕하세요 메이드 ARiSA입니다.")

        if searchDB("guilds","id",f"id={guild.id}") == None:
            insertDB("guilds", "name, id",(guild.name, guild.id))
            print(f"신규 서버 {guild.name}가 등록되었습니다.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'{member.mention}, {member.guild.name}에 온 걸 환영해!! 나는 이 서버의 메이드 아쿠땅BOT이야!!\n궁금한게 있으면 `아틔시 help`로 물어봐!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'{member}가 서버에서 나갔어ㅠㅠ 언젠가 다시 볼 수 있었으면 좋겠네')

async def setup(bot):
    await bot.add_cog(이벤트(bot))