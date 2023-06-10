import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import asyncio
import random
from discord.ext.commands import Context
from discord import app_commands

timezone_offset = +9.0
tzinfo = timezone(timedelta(hours=timezone_offset))

class 메시지(commands.Cog, description = "질문과 잡담"):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "핑", description= "봇의 핑을 확인합니다.")
    async def 핑(self, ctx) -> None:
        ping1 = f"{str(round(self.bot.latency * 1000))} ms"
        embed = discord.Embed(title = "퐁🏓", description = "**" + ping1 + "**", color = 0x00DDEE)
        await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(메시지(bot))
