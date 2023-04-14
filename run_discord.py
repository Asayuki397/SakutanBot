import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import json
from proto import llm

BOT_TOKEN = os.environ['BOT_TOKEN']
application_id = os.environ['APPLICATION_ID']
prefix = [prefix for prefix in os.environ['BOT_PREFIX'].split('-')]
intents=discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, intents=intents, application_id = application_id)
bot.owner_id = os.environ['BOT_OWNER_ID']

@bot.event
async def on_ready():
    print("ARiSA logged in.")
    game = discord.Game("ARiSA 채팅방")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(msg):
    if msg.channel.id == 1096237172429947012:
        res = llm(msg.content)
        await msg.reply(res)


bot.run(f"{BOT_TOKEN}")