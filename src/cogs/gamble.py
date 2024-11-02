import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
from users import *
from proto import arisa_reaction
import psycopg2
import random
from .errorhandler import UserNotFoundError


class game():

    def __init__(self,ctx, id : int, betting : int, winRate = 1.95):
        self.id = id
        self.betting = betting

        if self.betting < 0:
            raise ValueError

        self.winRate = winRate

        if checkUser(self.id) == False:
            raise UserNotFoundError

        if getMoney(id) < self.betting:
            raise ValueError
    
    def showRes(self, res : str):
        resEmbed = discord.Embed(title = "게임 결과", description = None)
        if res == "playerW":
            resEmbed.add_field(name = "결과", value = "승리")
            earning = int(self.betting*self.winRate)
        elif res == "draw":
            resEmbed.add_field(name = "결과", value = "무승부")
            earning = self.betting
        else:
            resEmbed.add_field(name = "결과", value = "패배")
            earning = 0

def coin():
    coin_face = random.randrange(0,2)
    if coin_face == 0:
        return "앞면" 
    elif coin_face == 1:
        return "뒷면"

def dice(betting):
    dice_face = random.randrange(1,7)
    if dice_face == 6:
        earning = int(betting*2.98)
    elif dice_face == 5:
        earning = int(betting*1.99)
    elif dice_face == 4:
        earning = betting*1
    else:
        earning = 0
    
    return dice_face, earning

class blackjack:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.card = []
            cls.mark = ["♤", "♢", "♧", "♡"]
            for m in cls.mark:
                for i in range(2,11):
                    cls.card.append(m+" "+str(i))
                cls.card.append(m+" J")
                cls.card.append(m+" Q")
                cls.card.append(m+" K")
                cls.card.append(m+" A")
            cls.deck = cls.card.copy()
            random.shuffle(cls.deck)
            cls.instance = super(blackjack, cls).__new__(cls)
        return cls.instance     

    def draw_card(self, amount):
        sels = []
        for i in range(amount):
            if len(self.deck) < 2:
                self.deck += self.card.copy()
                random.shuffle(self.deck)
            sels.append(self.deck.pop(1))
        return sels

    def getCardValue(self, _card):
        value = _card.split(" ")[1]
        return value

    def handtotal(self, hand):
        total = 0
        for card in hand:
            cardValue = self.getCardValue(card)
            if cardValue == "J" or cardValue == "Q" or cardValue == "K":
                total += 10
            elif cardValue != "A": total += int(cardValue)
        for card in hand:
            cardValue = self.getCardValue(card)
            if cardValue == "A":
                if total >= 11: total += 1
                else: total += 11
        return total
    
    def checkblackjack(self):
        player = self.draw_card(2)
        dealer = self.draw_card(2)
        if self.handtotal(player) == 21 and self.handtotal(dealer) == 21:
            return "bothBJ" , dealer, player
        elif self.handtotal(player) == 21:
            return "playerBJ", dealer, player
        elif self.handtotal(dealer) == 21:
            return "dealerBJ", dealer, player
        else:
            return "noBJ" , dealer, player

    def hit(self, hand):
        hand.append(self.draw_card(1)[0])
        return hand

    def showdown(self, p,d):
        while self.handtotal(d) < 17:
            d = self.hit(d)
        if self.handtotal(d) > 21:
            return "dealerBU"
        elif self.handtotal(d) > self.handtotal(p):
            return "dealerW"
        elif self.handtotal(d) == self.handtotal(p):
            return "draw"
        else:
            return "playerW"

class rps:

    def __init__(self, id, player : str, betting : int):

        self.rpsList = ["바위","보","가위"]
        self.rpsIcon = ["✊", "✋","✌️"]
        self.player = player
        self.dealer = random.choice(self.rpsList)
        self.betting = betting
        self.id = id

    async def battle(self):

        player = self.player
        dealer = self.dealer
        betting = self.betting
        id = self.id

        if betting <= 0:
            raise ValueError
        if player not in self.rpsList:
            raise ValueError

        if player == dealer:
            res = "draw"
        elif dealer == "바위":
            if player == "보":
                res = "playerW"
            else:
                res = "dealerW"
        elif dealer == "보":
            if player == "가위":
                res = "playerW"
            else:
                res = "dealerW"
        elif dealer == "가위":
            if player == "바위":
                res = "playerW"
            else:
                res = "dealerW"
        

        resEmbed = discord.Embed(title = "게임 결과", description = None, color = 0x00DDEE)
        resEmbed.add_field(name = "나", value = player + self.rpsIcon[self.rpsList.index(player)])
        resEmbed.add_field(name = "사쿠땅", value = dealer + self.rpsIcon[self.rpsList.index(dealer)])

        if res == "draw":
            resEmbed.add_field(name = "결과", value = "무승부")
            earning = betting
        elif res == "playerW":
            resEmbed.add_field(name = "결과", value = "승리")
            earning = int(betting*1.95)
        elif res == "dealerW":
            resEmbed.add_field(name = "결과", value = "패배")
            earning = 0
            addLoss(id,betting)

        addMoney(id, earning)
        
        modifyExp(id,earning // 100)
        resEmbed.add_field(name = "획득 금액", value = earning)
        resEmbed.add_field(name = "손익", value = f"{earning - betting:+d}")
        resEmbed.add_field(name = "획득 경험치",value = earning // 100)

        return resEmbed

class quiz(game):
    def __init__(self, ctx, id, betting, winRate, topic):
        super().__init__(ctx, id, betting, winRate)
        self.topic = topic

    def newQuestion(self):
        if self.topic == None:
            raise ValueError
        elif self.topic == "math":
            self.side1 = random.randrange(50)
            self.side2 = random.randrange(50)
            self.question = f"{self.side1}*{self.side2} = ?"
            self.answer = self.side1*self.side2

            return self.question, self.answer

    def checkAns(self, player):
        self.player = player
        if self.player == self.answer:
            self.result == "playerW"

        else:
            self.result == "dealerW"

        self.showRes(self.result)
     

"""
디스코드 명령어
"""

class 도박(commands.Cog, description = "과도한 도박은 정신건강에 해롭습니다."):
    def __init__(self,bot):
        self.bot = bot

    @commands.hybrid_command(name = "주사위", description = "간단한 주사위 도박입니다")
    @app_commands.describe(betting = "베팅할 금액을 입력하세요")
    async def 주사위(self, ctx,betting : int):
        await ctx.defer()
        if betting <= 0:
            raise ValueError
        id = int(ctx.author.id)
        try :
            if betting > getMoney(id):
                raise ValueError
            else:
                result, amount = dice(betting)
                addMoney(id, betting*-1)
                embed = discord.Embed(title = "게임 결과", description = None, color = 0x00DDEE)
                embed.add_field(name = "결과", value = result)
                embed.add_field(name = "획득 금액", value = amount)
                embed.add_field(name = "손익", value = f"{amount-betting:+d}")
                embed.add_field(name = "획득 경험치", value = amount // 100)
                await ctx.send(embed=embed)
                addMoney(id, amount)
                modifyExp(id, amount // 100)
                if amount < betting:
                    addLoss(id, betting-amount)
        except Exception as e:
            await ctx.send(e)

    @commands.hybrid_command(name = "블랙잭", description = "블랙잭 도박입니다.")
    @app_commands.describe(betting = "베팅할 금액을 입력하세요")
    async def 블랙잭(self, ctx, betting:int):
        if betting <= 0:
            raise ValueError
        if betting > getMoney(ctx.author.id):
            raise ValueError
        else:
            try:
                addMoney(ctx.author.id,betting*-1)
                bj = blackjack()
                result, dealer, player = bj.checkblackjack()
                embed = discord.Embed(title="블랙잭", description = None, color = 0x00DDEE)
                embed.add_field(name = "딜러", value = dealer[0])
                embed.add_field(name = "플레이어", value = player)
                msg = await ctx.send(embed=embed)
                resembed = discord.Embed(title="결과", description= None, color = 0x00DDEE)
                if result != "noBJ":
                    if result == "bothBJ":
                        amount = betting
                        resembed.add_field(name = "결과", value = "무승부(양방 블랙잭)")
                        resembed.add_field(name = "딜러", value = dealer)
                        resembed.add_field(name = "플레이어", value = player)
                        resembed.add_field(name = "획득 금액", value = amount)
                        resembed.add_field(name = "손익", value = f"{amount-betting:+d}")
                        resembed.add_field(name = "획득 경험치", value = amount // 100)
                        activity = "블랙잭에서 서로 블랙잭을 해서 무승부"
                    elif result == "playerBJ":
                        amount = int(betting*2.5)
                        resembed.add_field(name = "결과", value = "승리(블랙잭)")
                        resembed.add_field(name = "딜러", value = dealer)
                        resembed.add_field(name = "플레이어", value = player)
                        resembed.add_field(name = "획득 금액", value = amount)
                        resembed.add_field(name = "손익", value = f"{amount-betting:+d}")
                        resembed.add_field(name = "획득 경험치", value = amount // 100)
                        activity = "블랙잭에서 블랙잭으로 승리"
                    elif result == "dealerBJ":
                        amount = 0
                        resembed.add_field(name = "결과", value = "패배(딜러 블랙잭)")
                        resembed.add_field(name = "딜러", value = dealer)
                        resembed.add_field(name = "플레이어", value = player)
                        resembed.add_field(name = "획득 금액", value = amount)
                        resembed.add_field(name = "손익", value = f"{amount-betting:+d}")
                        resembed.add_field(name = "획득 경험치", value = amount // 100)
                        activity = "블랙잭에서 딜러 블랙잭으로 패배"
                        addLoss(ctx.author.id, betting-amount)
                    addMoney(ctx.author.id, amount)
                    modifyExp(ctx.author.id, amount //100)
                    await ctx.send(embed=resembed)
                    await ctx.send(arisa_reaction(activity))
                    return

                hitbutton = Button(label="HIT", style=discord.ButtonStyle.danger,custom_id="hit")
                standbutton = Button(label="STAND", style=discord.ButtonStyle.green,custom_id="stand")
                async def hit_callback(interaction, player = player):
                    player = bj.hit(player)
                    newembed = discord.Embed(title="블랙잭", description = None, color = 0x00DDEE)
                    newembed.add_field(name = "딜러", value = dealer[0])
                    newembed.add_field(name = "플레이어", value = player)
                    await msg.edit(embed=newembed)
                    await interaction.response.defer()
                    if bj.handtotal(player) > 21:
                        amount = 0
                        resembed.add_field(name = "결과", value = "패배(플레이어 버스트)")
                        resembed.add_field(name = "딜러", value = dealer)
                        resembed.add_field(name = "플레이어", value = player)
                        resembed.add_field(name = "획득 금액", value = amount)
                        resembed.add_field(name = "손익", value = f"{amount-betting:+d}")
                        resembed.add_field(name = "획득 경험치", value = amount // 100)
                        addLoss(ctx.author.id, betting-amount)
                        await ctx.send(embed=resembed)
                        await msg.delete()
                        await buttons.delete()
                        activity = "블랙잭에서 플레이어 버스트로 패배"
                        await ctx.send(arisa_reaction(activity))
                        return
                async def stand_callback(interaction, player = player,dealer = dealer):
                    result = bj.showdown(player,dealer)
                    await msg.delete()
                    await interaction.response.edit_message(content="쇼다운!")
                    if result == "dealerBU":
                        amount = betting*2
                        resembed.add_field(name = "결과", value = "승리(딜러 버스트)")
                        resembed.add_field(name = "딜러", value = dealer)
                        resembed.add_field(name = "플레이어", value = player)
                        resembed.add_field(name = "획득 금액", value = amount)
                        resembed.add_field(name = "손익", value = f"{amount-betting:+d}")
                        resembed.add_field(name = "획득 경험치", value = amount // 100)
                        activity = "블랙잭에서 딜러 버스트로 승리"
                    elif result == "playerW":
                        amount = betting*2
                        resembed.add_field(name = "결과", value = "승리")
                        resembed.add_field(name = "딜러", value = dealer)
                        resembed.add_field(name = "플레이어", value = player)
                        resembed.add_field(name = "획득 금액", value = amount)
                        resembed.add_field(name = "손익", value = f"{amount-betting:+d}")
                        resembed.add_field(name = "획득 경험치", value = amount // 100)
                        activity = "블랙잭에서 숫자가 커서 승리"
                    elif result == "dealerW":
                        amount = 0
                        resembed.add_field(name = "결과", value = "패배")
                        resembed.add_field(name = "딜러", value = dealer)
                        resembed.add_field(name = "플레이어", value = player)
                        resembed.add_field(name = "획득 금액", value = amount)
                        resembed.add_field(name = "손익", value = f"{amount-betting:+d}")
                        resembed.add_field(name = "획득 경험치", value = amount // 100)
                        addLoss(ctx.author.id, betting-amount)
                        activity = "블랙잭에서 숫자가 작아 패배"
                    else:
                        amount = betting
                        resembed.add_field(name = "결과", value = "무승부")
                        resembed.add_field(name = "딜러", value = dealer)
                        resembed.add_field(name = "플레이어", value = player)
                        resembed.add_field(name = "획득 금액", value = amount)
                        resembed.add_field(name = "손익", value = f"{amount-betting:+d}")
                        resembed.add_field(name = "획득 경험치", value = amount // 100)
                        activity = "블랙잭에서 숫자가 같아 무승부"
                    addMoney(ctx.author.id, amount)
                    modifyExp(ctx.author.id, amount //100)
                    player = None
                    dealer = None
                    await buttons.delete()
                    await ctx.send(embed=resembed)
                    await ctx.send(arisa_reaction(activity))
                hitbutton.callback = hit_callback
                standbutton.callback = stand_callback
                view = View()
                view.add_item(hitbutton)
                view.add_item(standbutton)
                buttons = await ctx.send(view=view)
            except Exception as e:
                await ctx.send(e)

    @commands.hybrid_command(name = "코인", description = "간단한 동전 던지기 도박입니다")
    @app_commands.describe(predict = "`앞면` 또는 `뒷면`으로 예측을 입력하세요")
    @app_commands.describe(betting = "베팅할 금액을 입력하세요")
    async def 코인(self,ctx,predict : str,betting : int):
        id = ctx.author.id
        if betting <= 0 or predict not in ["앞면","뒷면"] or betting > getMoney(id):
            raise ValueError
        addMoney(id,betting*-1)
        res = coin()
        resEmbed = discord.Embed(title = "게임 결과", description = None, color = 0x00DDEE)
        if predict == res:
            resEmbed.add_field(name = "결과", value = "승리")
            earning = int(betting*1.95)
            addMoney(id,earning)
            exp = earning // 100
        else:
            resEmbed.add_field(name = "결과", value = "패배")
            addLoss(id,betting)
            earning = 0
            exp = 0
        modifyExp(id,exp)
        resEmbed.add_field(name = "획득 금액", value = earning)
        resEmbed.add_field(name = "손익", value = f"{earning-betting:+d}")
        resEmbed.add_field(name = "획득 경험치", value = exp)
        await ctx.send(embed=resEmbed)

    @commands.hybrid_command(name = "가위바위보", description = "가위바위보 도박입니다")
    @app_commands.describe(betting = "베팅할 금액을 입력하세요")
    async def 가위바위보(self,ctx,betting:int):
        id = ctx.author.id
        addMoney(id,betting*-1)
        embed = discord.Embed(title = "가위바위보",description = None, color = 0x00DDEE)
        rock = Button(label="바위✊", style = discord.ButtonStyle.primary,custom_id = "rock")
        scissors = Button(label = "가위✌️", style = discord.ButtonStyle.primary,custom_id = "scissors")
        paper = Button(label = "보✋",style = discord.ButtonStyle.primary,custom_id = "paper")
        async def rock_callback(interaction):
            player = "바위"
            g = rps(id,player,betting)
            await interaction.response.defer()
            await buttons.delete()
            await ctx.send(embed = await g.battle())
        async def scissors_callback(interaction):
            player = "가위"
            g = rps(id,player,betting)
            await interaction.response.defer()
            await buttons.delete()
            await ctx.send(embed = await g.battle())
        async def paper_callback(interaction):
            player = "보"
            g = rps(id,player,betting)
            await interaction.response.defer()
            await buttons.delete()
            await ctx.send(embed = await g.battle())
        rock.callback = rock_callback
        scissors.callback = scissors_callback
        paper.callback = paper_callback
        view = View()
        view.add_item(rock)
        view.add_item(scissors)
        view.add_item(paper)
        buttons = await ctx.send(view=view)
"""
    @commands.hybrid_command(name = "퀴즈 ", description = "아리사가 퀴즈를 냅니다.")
    @app_commands.describe(betting = "베팅할 금액을 입력하세요")
    async def 퀴즈(self, ctx, betting : int):
        quiz = quiz(ctx = ctx, betting = betting)
        question, answer = quiz.newQuestion
        await ctx.send(question)
"""
async def setup(bot):
    await bot.add_cog(도박(bot))
