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
            await channel.send("안녕하세요 저는 ARiSA입니다. 오늘부터 여러분을 모시겠습니다.")

        if searchDB("guilds","id",f"id={guild.id}") == None:
            insertDB("guilds", "name, id",(guild.name, guild.id))
            print(f"신규 서버 {guild.name}가 등록되었습니다.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'{member.mention}님, {member.guild.name}에 오신 것을 환영합니다. `아리사` `help`로 도움말을 호출할 수 있습니다.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'{member}가 서버에서 나갔습니다. 안녕히 가십시오.')

async def setup(bot):
    await bot.add_cog(이벤트(bot))