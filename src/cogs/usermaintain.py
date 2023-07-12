import discord
from discord.ext import commands
from users import *
from database import *
import random
from .stock import *
from .errorhandler import UserNotFoundError

class 유저관리(commands.Cog, description = "회원가입, 내정보 등 유저 관리"):

    def __init__(self,bot):
        self.bot = bot

    @commands.hybrid_command(name = "회원가입", description = "회원가입을 할 수 있습니다.")
    async def 회원가입(self,ctx):
        await ctx.defer()
        id = ctx.author.id
        guild_id = ctx.guild.id
        print("회원가입이 가능한지 확인합니다.")
        userExistance = checkUser(id, guild_id)
        if userExistance:
            print("DB에서 ", ctx.author.name, "을 찾았습니다.")
            await ctx.send("이미 가입하셨습니다.")
        else:
            print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
            signup(ctx.author.name, id, ctx.guild.id)
            print("회원가입이 완료되었습니다.")
            await ctx.send(f"{ctx.author.mention}, 회원가입이 완료되었습니다.")

    @commands.hybrid_command(name = "내정보", description = "내정보를 확인할 수 있습니다.")
    async def 내정보(self, ctx):
        await ctx.defer()
        id = ctx.author.id
        guild_id = ctx.guild.id
        userExistance = checkUser(id, guild_id)

        if not userExistance:
            raise UserNotFoundError
        else:
            
            level = getLvl(id)
            exp = getExp(id)
            money = getMoney(id)
            loss = getLoss(id)
            rank = getRank(id, guild_id)

            expToUP = level*level + 6*level
            boxes = int(exp/expToUP*15)
            embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x00DDEE)
            embed.add_field(name = "레벨", value = level)
            embed.add_field(name = "순위", value = str(rank))
            embed.add_field(name = "XP: " + str(exp) + "/" + str(expToUP), value = boxes * ":blue_square:" + (15-boxes) * ":white_large_square:", inline = False)
            
            wallet = discord.Embed(title="내 자산", color = 0x00DDEE)
            wallet.add_field(name = "보유 자산", value = money, inline = False)
            wallet.add_field(name = "도박으로 날린 돈", value = loss, inline = False)

            stockembed = discord.Embed(title = "내 주식", color = 0x00DDEE)
            stack = 0
            for item in mystocks:
                callsign = item.split("-")[0]
                value = searchDB("stocks",callsign,f"id={id}")
                if value != 0:
                    amount = getAmount(id, callsign)
                    stockValue, var = getStock(callsign)
                    curAvg = getAvg(id, callsign)
                    stockembed.add_field(name = item.split("-")[1], value = f"{value}주\n평가금액 : {stockValue*amount}\n평가손익 : {stockValue*amount - curAvg*amount:+d}({(stockValue*amount - curAvg*amount)/(curAvg*amount)*100:+.2f}%)")
                    stack += 1
            if stack == 0: stockembed = None

            embeds = [e for e in [embed, wallet, stockembed] if e is not None]
            await ctx.send(embeds = embeds)

    @commands.hybrid_command(name = "랭킹", description = "랭킹을 확인할 수 있습니다.")
    async def 랭킹(self, ctx):
        await ctx.defer()
        ranking = fetchAllRanks(ctx.guild.id)
        embed = discord.Embed(title = f"{ctx.guild.name} 랭킹", description = None, color = 0x00DDEE)

        for i in range(0, len(ranking)):
            person = ranking[i]
            name = person[0]
            level = person[1]
            rank = person[2]
            embed.add_field(name = str(rank)+"위 "+name, value ="레벨: "+str(level), inline=False)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name = "탈퇴", description = "가입되어 있는 경우 탈퇴를 진행할 수 있습니다")
    async def 탈퇴(self, ctx):
        await ctx.defer()
        print("탈퇴가 가능한지 확인합니다.")
        userExistance = checkUser(ctx.author.id)
        if userExistance:
            DeleteAccount(ctx.author.id)
            print("탈퇴가 완료되었습니다.")

            await ctx.send("탈퇴가 완료되었습니다.")
        else:
            raise UserNotFoundError
       
    @commands.hybrid_command(name = "출석체크", description = "하루에 한 번 출석체크로 돈을 받을 수 있습니다.")
    async def 출석체크(self, ctx):
        await ctx.defer()
        lvl = getLvl(ctx.author.id)
        check, date = checkDaily(ctx.author.id)
        if check:
            await ctx.send("이미 {date}에 출석체크를 하셨습니다".format(date=date))
        else:
            try:
                value = lvl*1000*random.randrange(5,8)
                updateDB("db","dailybonus",date,"id={_id}".format(_id=ctx.author.id))
                addMoney(ctx.author.id, value)
                await ctx.send("출석체크가 완료되었습니다. {_value}만큼 돈이 입금되었습니다. 마지막 출석일: {date}".format(_value=value,date=date))
            except Exception as e:
                await ctx.send(e)
            
            
async def setup(bot):
    await bot.add_cog(유저관리(bot))
