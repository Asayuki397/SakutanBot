import discord
import traceback
import sys
from discord.ext import commands

async def raiseError(ctx , type, message):
    errEmbed = discord.Embed(title = "에러", description = None, color = 0xDDA0DD)
    errEmbed.add_field(name = "종류", value = type,inline = False)
    errEmbed.add_field(name = "도움말", value = message, inline = False)
    await ctx.send(embed = errEmbed)

class UserNotFoundError(Exception):
    pass

class NoMarginError(Exception):
    pass

class MarketNotOpenError(Exception):
    pass

class 에러관리(commands.Cog, description = "에러 핸들링 커맨드"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            await raiseError(ctx, "명령어 존재하지 않음","존재하지 않는 명령어야 ㅠㅠ `아틔시` `help`으로 모든 명령어를 볼 수 있어~!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await raiseError(ctx, "필수 매개변수 없음",f"필요한 매개변수가 없어ㅠㅠ `아틔시` `help` `{ctx.command}` 을(를) 확인해봐")
            return

        if isinstance(error, commands.DisabledCommand):
            await raiseError(ctx, "비활성화된 커맨드",f'`{ctx.command}`은(는) 비활성화된 커맨드야')
            return

        if isinstance(error, UserNotFoundError):
            await raiseError(ctx, "유저 존재하지 않음","`아틔시 회원가입`으로 회원가입을 먼저 해줘")

        if isinstance(error, NoMarginError):
            await raiseError(ctx, "증거금 부족", "증거금이 모자라ㅠㅠ 주식의 현 가격 x 레버리지의 10%가 증거금으로 필요해")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await raiseError(ctx,"DM 사용 불가",f'`{ctx.command}`은(는) DM에서 쓸 수 없어')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            await raiseError(ctx,"매개변수 오류" ,f"유효하지 않은 매개변수야~! `아틔시` `help` `{ctx.command}`로 확인해봐")

        elif isinstance(error, ValueError):
            await raiseError(ctx, "유효하지 않은 입력값", f"유효하지 않은 입력값이야ㅠㅠ `아틔시` `help` `{ctx.command}`을(를) 확인해봐")

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

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