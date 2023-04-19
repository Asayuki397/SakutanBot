import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import json
from proto import llm, llm_chat

BOT_TOKEN = os.environ['BOT_TOKEN']
application_id = os.environ['APPLICATION_ID']
prefix = [prefix for prefix in os.environ['BOT_PREFIX'].split('-')]
intents=discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, intents=intents, application_id = application_id)
bot.owner_id = os.environ['BOT_OWNER_ID']

CACHE_SIZE = 3
prompt_cache = []
prompt_cache_chat = []
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

    if msg.content.startswith(prefix):
        return

    if msg.content.startswith(".."):
        return

    if msg.channel.id == 1097414601588617216:

        global prompt_cache_chat

        res = llm_chat(msg.content, cached = prompt_cache_chat)

        await msg.reply(res)

        new_cache = [
            {"role" : "user", "content" : str(msg.content)},
            {"role" : "assistant", "content" : str(res)}
        ]

        for cache in new_cache:
            prompt_cache_chat.append(cache)

        while len(prompt_cache_chat) > CACHE_SIZE*2:
            prompt_cache_chat.pop(0)



    if msg.channel.id == 1096237172429947012:

        global prompt_cache

        res = llm(msg.content, cached = prompt_cache)

        new_cache = "\nMaster: " + msg.content + "\nARiSA: " + res
        prompt_cache.append(new_cache)

        if len(prompt_cache) > CACHE_SIZE:
            prompt_cache.pop(0)

        await msg.reply(res)
    else: 
        return

@bot.command()
async def clear(ctx):
    prompt_cache = []
    await ctx.send("complete")


bot.run(f"{BOT_TOKEN}")