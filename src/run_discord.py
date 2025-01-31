import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import json
from proto import llm_chat

BOT_TOKEN = os.environ['BOT_TOKEN']
application_id = os.environ['APPLICATION_ID']
prefix = [prefix for prefix in os.environ['BOT_PREFIX'].split('-')]
print("명령어 접두사 : ", prefix)
intents=discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, intents=intents, application_id = application_id,
                   activity = discord.Game("gpt-o1-mini 장착"))
bot.owner_id = os.environ['BOT_OWNER_ID']

CACHE_SIZE = 5
prompt_cache = []
prompt_cache_chat = []

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands.")
    print("SakutanBot 로그인 완료")

@bot.event
async def on_message(msg):

    execution = True

    await bot.process_commands(msg)

    if bot.user.mentioned_in(msg):

        user_name = msg.author.name
        user_id = msg.author.id

        global prompt_cache_chat

        if len(prompt_cache_chat) == 0:
            prompt_cache_chat.append(
                    {"role" : "system", "content" : f"당신의 대화 상대 이름 : {user_name}, UID : {user_id}"},
                    )
        elif not prompt_cache_chat[0]["content"].endswith(str(user_id)):
            prompt_cache_chat[0] = {"role" : "system", "content" : f"당신의 대화 상대 이름 : {user_name}, UID : {user_id}"}

        res = await llm_chat(bot, msg.content, cached = prompt_cache_chat)

        await msg.reply(res)

        new_cache = [
            {"role" : "user", "content" : str(msg.content)},
            {"role" : "assistant", "content" : str(res)}
        ]

        for cache in new_cache:
            prompt_cache_chat.append(cache)

        while len(prompt_cache_chat) > CACHE_SIZE*2 + 1:
            prompt_cache_chat.pop(0)

        return

@bot.command()
async def clear(ctx):
    global prompt_cache
    global prompt_cache_chat
    prompt_cache = []
    prompt_cache_chat = []
    ebd = discord.Embed(title = "Execution Success", description = None, color = 0x00EEDD)
    ebd.add_field(name = "실행 완료", value = "프롬프트 캐시가 제거되었습니다.", inline = False)
    await ctx.send(embed = ebd)



current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"cogs")
print("현재 경로", current_path)
async def load_cogs():
    for ext in os.listdir(current_path):
        if ext.endswith(".py"):
            await bot.load_extension(f"cogs.{ext.split('.')[0]}")
            print(f"확장 -- {ext} 로드 완료")

asyncio.run(load_cogs())
bot.run(f"{BOT_TOKEN}")
