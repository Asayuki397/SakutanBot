import discord
import traceback
import sys
from discord.ext import commands

async def raiseError(ctx , type, message):
    errEmbed = discord.Embed(title = "에러", description = None, color = 0xFF0000)
    errEmbed.add_field(name = "종류", value = type,inline = False)
    errEmbed.add_field(name = "도움말", value = message, inline = False)
    await ctx.send(embed = errEmbed)

class UserNotFoundError(Exception):
    pass

class NoMarginError(Exception):
    pass

class MarketNotOpenError(Exception):
    pass

class NotEnoughMoneyError(Exception):
    pass

class 에러관리(commands.Cog, description = "에러 핸들링 커맨드"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        print("error detected!!!!!")
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        if hasattr(ctx.command, 'on_error'):
            return
        

        ignored = (commands.CommandNotFound, )

        print("getattr 전", error)

        error = getattr(error, 'original', error)
        print("getattr 후 :", error)

        if isinstance(error, ignored):
            await raiseError(ctx, "명령어 존재하지 않음",f"존재하지 않는 명령어입니다. `{ctx.prefix}` `help`으로 모든 명령어를 볼 수 있습니다.")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await raiseError(ctx, "필수 매개변수 없음",f"필요한 매개변수가 없습니다. `{ctx.prefix}` `help` `{ctx.command}` 을(를) 확인해 보십시오.")
            return

        if isinstance(error, commands.DisabledCommand):
            await raiseError(ctx, "비활성화된 커맨드",f'`{ctx.command}`은(는) 비활성화된 커맨드입니다.')
            return

        if isinstance(error, UserNotFoundError):
            await raiseError(ctx, "유저 존재하지 않음",f"`{ctx.prefix}` `회원가입`을 먼저 진행하십시오")
            return

        if isinstance(error, NoMarginError):
            await raiseError(ctx, "증거금 부족", "증거금이 부족합니다. 주식의 현 가격 x 레버리지의 10%가 증거금으로 필요합니다.")
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await raiseError(ctx,"DM 사용 불가",f'`{ctx.command}`은(는) DM에서 사용할 수 없습니다.')
                return
            except discord.HTTPException:
                return

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            await raiseError(ctx,"매개변수 오류" ,f"유효하지 않은 매개변수입니다. `{ctx.prefix}` `help` `{ctx.command}`로 확인하십시오")
            return

        elif isinstance(error, ValueError):
            await raiseError(ctx, "유효하지 않은 입력값", f"유효하지 않은 입력값입니다. `{ctx.prefix}` `help` `{ctx.command}`을(를) 확인하십시오.")
            return

        elif isinstance(error, NotEnoughMoneyError):
            await raiseError(ctx,"잔액 부족", f"잔액이 부족합니다. `{ctx.prefix}` `내정보`로 잔액을 확인할 수 있습니다.")
            return

        else:
            print(error)
 

    """Below is an example of a Local Error Handler for our command do_repeat"""

    @commands.command(name='repeat', aliases=['mimic', 'copy'])
    async def do_repeat(self, ctx, *, inp: str):
        """A simple command which repeats your input!
        Parameters
        ------------
        inp: str
            The input you wish to repeat.
        """
        await ctx.send(inp)

    @do_repeat.error
    async def do_repeat_handler(self, ctx, error):
        """A local Error Handler for our command do_repeat.
        This will only listen for errors in do_repeat.
        The global on_command_error will still be invoked after.
        """

        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'inp':
                await ctx.send("You forgot to give me input to repeat!")


async def setup(bot):
    await bot.add_cog(에러관리(bot))
