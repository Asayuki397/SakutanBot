from pykrx import stock
import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import Context
from discord.ui import Button, View
from discord import app_commands
from datetime import datetime, timedelta, timezone
import pandas as pd
from database import *
from users import *
from .errorhandler import *

timezone_offset = +9.0
tzinfo = timezone(timedelta(hours=timezone_offset))

global mystocks
mystocks = ["AKKN-AKUKIN 건설-삼성전자-005930","SHRN-SHIRANUI 건설-NAVER-035420","STND-STARTEND Co.-기아-000270","UMSI-UMISEA Ltd.-LG-003550"]



class Option():
    def __init__(self, callsign, userID, guild_id):
        
        self.id = userID
        self.guild_id = guild_id

        if checkUser(self.id, self.guild_id) == False:
            raise UserNotFoundError

        if stockdate(check_stock_is_open = True) == False:
            raise MarketNotOpenError

        self.callsign = callsign
        self.pos = None
        self.leverage = 1
        self.open_value = None
        self.close_value = None
        self.variance = None

    def open_position(self):
        stock = self.callsign
        self.open_value = getStockPrice(stock)
        if getMoney(self.id) < self.leverage * self.open_value * 0.1:
            raise ValueError
        addMoney(self.id, self.open_value*-1)

    def close_position(self):
        stock = self.callsign
        self.close_value = getStockPrice(stock)
        self.variance = self.close_value - self.open_value

        if self.pos == "long":
            self.leverage *= -1

        self.result = self.variance*self.leverage

        exp = 0
        if self.result > 0:
            self.result = int(self.result * 0.99997)
            exp = self.result // 100
            modifyExp(id, exp)

        addMoney(self.id, self.open_value + self.result)

        res_embed = discord.Embed(title="포지션 종료", description=None, color=0x00DDEE)
        res_embed.add_field(name="레버리지", value=f"{self.leverage}x")
        res_embed.add_field(name="수익", value=f"{self.result:+d}")
        res_embed.add_field(name="획득 경험치", value =f"{self.exp}")
        res_embed.set_footer(text = "수수료 : 0.003%")

        return res_embed


def getStockValue(name):
    return name.iloc[0,3], f"{name.iloc[0,6]:+.2f}"

def stockdate(check_stock_is_open = False):
    t = datetime.now(tzinfo)
    stock_is_open = False
    if t.weekday() == 5 or t.weekday() == 6: # 주말이면 금요일로
        t = t - timedelta(days = t.weekday()-4)
    elif t.weekday() == 0 and t.hour < 10: #월요일 10시 전이면 금요일로
        t = t - timedelta(days = 3)
    elif t.hour < 10: #10시 전이면 전날 23시로 고정하기
        t = t - timedelta(days = 1)
    else:
        stock_is_open = True
    today = t.strftime("%Y%m%d")

    if check_stock_is_open:
        return stock_is_open

    return today
    
def addStock(_id,column,amount):
    addDB("stocks",f"{column}",f"{amount}",f"id={_id}")

def updateStock(_id,column,amount):
    updateDB("stocks",f"{column}",f"{amount}",f"id={_id}")

def getTicker(callsign):
    for item in mystocks:
        if item.split("-")[0] == callsign:
            return item.split("-")[3]

def getAmount(id, callsign):
    curamount = searchDB("stocks",f"{callsign}",f"id={id}")
    return curamount

def getAvg(id, callsign):
    curavg = searchDB("stocks",f"{callsign}avg",f"id={id}")
    return curavg

def getStock(callsign, today = stockdate()):
    ticker = getTicker(callsign)
    fetchStock = stock.get_market_ohlcv_by_date(fromdate = today, todate = today, ticker = ticker)
    val,var =  getStockValue(fetchStock) #two return values -- current value and variance
    return val, var

def getStockPrice(callsign) -> int: return getStock(callsign)[0]


class 주식(commands.Cog, description = "한국 증시와 연동된 투자 시뮬레이션"):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(name = "주식", description = "주식의 시세와 콜사인을 확인할 수 있습니다.")
    async def 주식(self,ctx):
        await ctx.defer()
        today = stockdate()
        embed = discord.Embed(title = "주식", description=today[:4]+"-"+today[4:6]+"-"+today[6:8] + " 기준", color = 0x00DDEE)
        for item in mystocks:
            callsign = item.split("-")[0]
            curVal, variance = getStock(callsign, today)
            stockName = item.split("-")[1]
            connectedStock = item.split("-")[2]
            embed.add_field(name = f"[{callsign}] {stockName} ({connectedStock})",value = str(curVal) + " / " + str(variance),inline = False)
        
        await ctx.send(embed=embed)
  
    @commands.hybrid_command(name = "매수", description = "주식을 매수할 수 있습니다.")
    @app_commands.describe(callsign = "주식의 콜사인을 입력하세요. `주식`으로 콜사인을 확인할 수 있습니다.")
    @app_commands.describe(amount = "매수할 수량을 입력하세요.")
    async def 매수(self, ctx, callsign : str, amount : int):
        await ctx.defer()
        if amount <= 0:
            await ctx.send("수량은 자연수로 부탁드립니다.")
            return
        id = ctx.author.id
        stockValue, var = getStock(callsign)
        curavg = searchDB("stocks",f"{callsign}avg",f"id={id}") #returns current average value
        curamount = searchDB("stocks",f"{callsign}",f"id={id}") #returns current amount
        price = stockValue * amount
        if getMoney(id) < price:
            await ctx.send("소지금을 초과하는 주문은 할 수 없습니다.")
            return
        else:
            addStock(id, callsign, amount)
            addMoney(id,price * -1)
            currentValue = curamount * curavg
            newavg = (currentValue + price) / (curamount + amount)
            updateStock(id, f"{callsign}avg",newavg)
            embed = discord.Embed(title = "체결 성공", description = None, color=0x00DDEE)
            embed.add_field(name = "체결가", value = price)
            embed.add_field(name = "현재 보유 수량", value = curamount + amount)
            embed.add_field(name = "평균 구매가", value = newavg)
            await ctx.send(embed = embed)

    @commands.hybrid_command(name = "매도", description = "주식을 매도할 수 있습니다.")
    @app_commands.describe(callsign = "주식의 콜사인을 입력하세요. `주식`으로 콜사인을 확인할 수 있습니다.")
    @app_commands.describe(amount = "매도할 수량을 입력하세요.")
    async def 매도(self, ctx, callsign : str, amount : int):
        await ctx.defer()
        if amount <= 0:
            await ctx.send("수량은 자연수로 부탁드립니다.")
            return
        id = ctx.author.id
        stockValue, var = getStock(callsign)
        curavg = getAvg(id, callsign)
        curamount = getAmount(id,callsign) #returns current amount
        price = stockValue * amount
        if curamount < amount:
            await ctx.send("소지개수를 초과하는 주문은 할 수 없습니다.")
            return
        else:
            earning = price - (curavg * amount)
            addStock(id, callsign, amount * -1)
            addMoney(id,price)
            embed = discord.Embed(title = "체결 성공", description = None, color=0x00DDEE)
            embed.add_field(name = "체결가", value = price)
            embed.add_field(name = "현재 보유 수량", value = curamount - amount)
            embed.add_field(name = "평균 구매가", value = curavg)
            embed.add_field(name = "손익", value = f"{earning:+d}")
            embed.add_field(name = "수익률", value = f"{earning/amount/curavg:+.2f}")
            if earning > 0:
                modifyExp(id, earning // 10)
                embed.add_field(name = "획득 경험치", value = earning // 10)
            else:
                embed.add_field(name = "획득 경험치", value = earning // 0)
            await ctx.send(embed= embed)

    @commands.hybrid_command(name="옵션", description="옵션 거래를 할 수 있습니다.")
    @app_commands.describe(callsign="주식의 콜사인을 입력하세요. `주식`으로 콜사인을 확인할 수 있습니다.")
    @app_commands.describe(leverage="주식의 레버리지를 입력하세요. 높은 숫자를 입력할수록 투자위험도와 수익이 증가합니다.")
    async def 옵션(self, ctx, callsign: str, leverage: int):
        await ctx.defer()
        id = ctx.author.id
        stock = callsign
        op = Option(callsign, id)
        op.leverage = leverage

        long_button = Button(
            label="LONG", style=discord.ButtonStyle.danger, custom_id="long"
        )
        short_button = Button(
            label="SHORT", style=discord.ButtonStyle.green, custom_id="short"
        )

        async def long_callback(interaction):
            op.pos = "long"
            await interaction.response.edit_message(content="롱포지션에 진입했습니다.")
            await buttons.delete()

        async def short_callback(interaction):
            op.pos = "short"
            await interaction.response.edit_message(content="숏포지션에 진입했습니다.")
            await buttons.delete()

        long_button.callback = long_callback
        short_button.callback = short_callback
        view = View()
        view.add_item(long_button)
        view.add_item(short_button)
        buttons = await ctx.send(view=view)

        op.open_position()
        await asyncio.sleep(60)
        res_embed = op.close_position()

        await ctx.send(embed=res_embed)


async def setup(bot):
    await bot.add_cog(주식(bot))
