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
print("명령어 접두사 : ", prefix)
intents=discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, intents=intents, application_id = application_id)
bot.owner_id = os.environ['BOT_OWNER_ID']

CACHE_SIZE = 3
prompt_cache = []
prompt_cache_chat = []

@bot.event
async def on_ready():
    print("ARiSA logged in.")
    game = discord.Game("ARiSA 채팅방")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(msg):

    execution = True

    if msg.author.bot:
        return

    if msg.content.startswith(".."):
        return

    if msg.channel.id == 1097414601588617216 and execution:

        user_name = msg.author.name

        global prompt_cache_chat

        if len(prompt_cache_chat) == 0:
            prompt_cache_chat.append(
                    {"role" : "system", "content" : f"당신의 대화 상대 이름 : {user_name}"},
                    )
        elif not prompt_cache_chat[0]["content"].endswith(user_name):
            prompt_cache_chat[0] = {"role" : "system", "content" : f"당신의 대화 상대 이름 : {user_name}"}

        res = llm_chat(msg.content, cached = prompt_cache_chat)

        await msg.reply(res)

        new_cache = [
            {"role" : "user", "content" : str(msg.content)},
            {"role" : "assistant", "content" : str(res)}
        ]

        for cache in new_cache:
            prompt_cache_chat.append(cache)

        while len(prompt_cache_chat) > CACHE_SIZE*2 + 1:
            prompt_cache_chat.pop(0)



    if msg.channel.id == 1096237172429947012 and execution:

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
    print("command execution : clear")
    global prompt_cache
    global prompt_cache_chat
    prompt_cache = []
    prompt_cache_chat = []
    ebd = discord.Embed(title = "Execution Success", description = "execution : cache clear", color = 0x00EEDD)
    ebd.add_field(name = "실행 완료", value = "프롬프트 캐시가 제거되었습니다.", inline = False)
    await ctx.send(embed = ebd)
    print("command execution complete")

bot.run(f"{BOT_TOKEN}")