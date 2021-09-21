#doPick.py
import asyncio
from pick import makePicks
from check import checkPick
async def doPick(bot,coach, pickNum, sh, ctx):
    wk = sh.sheet1
    try:
        message = await bot.wait_for("message", check=lambda m: m.author == coach or str(m.author) == 'Dasboot867#0258', timeout= 3600.0)
    except asyncio.TimeoutError:
        await ctx.send("You have timed out. Sorry.")
    else:
        if message.content.lower().startswith("draft"):
            if checkPick(sh,message.content[6:]):
                myName = str(coach)
                makePicks(myName, wk, pickNum, message.content[6:])
            else:
                await ctx.send("I do not believe that mon can be drafted. Please try again.")
                await doPick(bot,coach, pickNum, sh, ctx)
        elif message.content == 'skip':
            print(str(message.author))
            if str(message.author) == 'Dasboot867#0258':
                await ctx.send("Okay, I will skip this for now. Someone will need to handle this manually.")
            else:
                await ctx.send("Okay, I will skip this for now. Someone will need to handle this manually.")
        else:
            await ctx.send("Please make your pick {}".format(coach.name))
            await doPick(bot,coach, pickNum, sh, ctx)
