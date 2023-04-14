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

CACHE_SIZE = 15
prompt_cache = []

prompt_cache_korean = []

@bot.event
async def on_ready():
    print("ARiSA logged in.")
    game = discord.Game("ARiSA 채팅방")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(msg):

    

    if msg.author.bot:
        return

    if msg.channel.id == 1096237172429947012:

        global prompt_cache

        res = llm(msg.content, cached = prompt_cache)

        new_cache = "\nMaster: " + msg.content + "\nARiSA: " + res
        prompt_cache.append(new_cache)

        if len(prompt_cache) > CACHE_SIZE:
            prompt_cache.pop(0)

        await msg.reply(res)

    elif msg.channel.id == 1096408494229430282:

        global prompt_cache_korean

        res = llm(msg.content, cached = prompt_cache_korean)

        new_cache = "\n주인님: " + msg.content + "\n아리사: " +res
        prompt_cache_korean.append(new_cache)

        if len(prompt_cache_korean) > CACHE_SIZE:
            prompt_cache_korean.pop(0)

        await msg.reply(res)
    else: 
        return


bot.run(f"{BOT_TOKEN}")