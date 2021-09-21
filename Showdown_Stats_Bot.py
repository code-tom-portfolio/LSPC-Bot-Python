# Creating a bot for Managing a pokémon draft league using Discord and Google Sheets

import os
import discord
import asyncio
import urllib
from discord.ext import commands
import wobb_discord_token
import random
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
from pick import makePicks
from orderList import orderList
from latePick import latePick
from check import checkPick
from doPick import doPick
scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

TOKEN = wobb_discord_token.token
intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True


credentials = ServiceAccountCredentials.from_json_keyfile_name("token.json", scopes) #access the json key you downloaded earlier 
gc = gspread.service_account('token.json')

sh = gc.open("LSPC Season 8")
wk = sh.sheet1

print(sh.get_worksheet(6).get('A2'))

lateList = []
draftQueue = []

bot = commands.Bot("$",intents=intents)

# Client instance created to register responses to events

# a command in discord.py is <command-prefix><command-name>
# this creates a command that can be triggered by `$hello`, ie. "hello" is the command name
@bot.command(pass_context=True)
async def hello(ctx):  # note: discord commands must be coroutines, so define the function with `async def`
    # the ctx argument is passed as the first positional argument when pass_context=True
    # this is required if you need to access the "context" of this command's origin

    # you can access the author (type discord.Member) and channel (type discord.Channel) of the command as followed:
    message_author = ctx.message.author  # both .author and .channel can only be accessed from the message instance
    message_channel = ctx.message.channel

    # prints "<username> said hello" to the console
    print("{} said hello".format(message_author))

    # bot.send_message(...) is a coroutine, so it must be awaited
    # this sends a message "Hello, <username>!" to the message channel
    await ctx.send("Hello, {}!".format(ctx.author.mention))
    # bot.send_message takes the destination and content as the first and second positional arguments
    # more info on string formatting: https://pyformat.info

@bot.command(pass_context=True)
async def available(ctx, mon):
    if checkPick(sh, mon):
        await ctx.send("{} is available to be drafted!".format(mon))
    else:
        await ctx.send("{} is not available, are you sure this is a valid Pokémon?".format(mon))



@bot.command(pass_context=True)
async def test(ctx):
     await ctx.send("Here we go")
     #message_author = ctx.message.author
     #def check(m):
     #   return m.content == "Wobb" and m.channel == "test-wobb-bot"
     #for mem in lateList:
         #if mem.coach == ctx.message.author:
             #print('Welcome Back')
     #msg = await bot.wait_for("message", check=check)
     #await ctx.send(f"Hello {msg.author}!")
     #print(ctx.message.author)
     #myName = str(ctx.message.author)
     #makePicks(myName, wk, 1, mon)

@bot.command(pass_context=True)
async def adminDraft(ctx, name, mon, num):
    if str(ctx.message.author) == 'Dasboot867#0258':
        await ctx.send("Okay boss, I will draft {} for {}".format(mon, name))
        makePicks(name, wk, num, mon)

@bot.command(pass_context=True)
async def adminOrder(ctx, role: discord.Role):
    if str(ctx.message.author) == 'Dasboot867#0258':
        await ctx.send("Okay boss, I will make a draft order")
        coaches = role.members
        random.shuffle(coaches)
        await ctx.send('Time for a new Draft Order!')
        for mem in coaches:
        #displaying?
            await ctx.send('-{}'.format(mem.name))

@bot.command(pass_context=True)
async def getuser(ctx, role: discord.Role):
    
    #await ctx.send("\n".join(str(mem) for mem in role.members))
    print("\n".join(str(mem) for mem in role.members))

@bot.command(pass_context=True)
async def start(ctx, role: discord.Role, rounds: int):
    #print('Beginning draft with coaches: {}\n {} rounds \n Randomizing every {} round(s)'.format(role.members, rounds, random))
    #await ctx.send('Command works properly')
    if str(ctx.message.author) != 'Dasboot867#0258':
        await ctx.send("You do not have permission to start the draft!")
        return
    coaches = role.members
    roundOne = open("round one.txt").readlines()
    
    #await ctx.send('Beginning Round 1!')
    #for mem in roundOne:
    #    await ctx.send('The current pick is: {} \n Use "draft name"'.format(mem))
    #    try:
    #        message = await bot.wait_for("message", check=lambda m: m.author == mem and m.channel == ctx.channel, timeout=30.0)
    #
    #    except asyncio.TimeoutError:
    #        await ctx.send("You have timed out, your pick is being skipped")
    #    
    #    else:
    #        if message.content.lower() == "$draft":
    #            await ctx.send("This is when I will make a pick for you :)")
    #        else:
    #            await ctx.send("You gotta say draft, silly!")
    #
    #
    coaches = orderList(roundOne, coaches)
    for mem in coaches:
        print (mem.name)
    for x in range(8, rounds):
       

        await ctx.send('Beginning Round {}!'.format(x))
        #loop for each round in the draft
        if x > 2:
            if(x%2 == 0):
                #randomize
                print('Randomized Order for round {}'.format(x))
                random.shuffle(coaches)
                await ctx.send('Time for a new Draft Order!')
                for mem in coaches:
                    #displaying?
                    await ctx.send('-{}'.format(mem.name))
        myCopy = coaches
        myIndex = 0
        for mem in coaches:
            #loop for each member in the draft
            await ctx.send('The current pick is: {} \n Say "draft "'.format(mem.mention))
            if myIndex!=26:
                await ctx.send('{}, you are on deck. Please have your pick ready.'.format(myCopy[myIndex+1].mention))
            
            #doPick(coach, pickNum)
            await doPick(bot,mem,(x), sh, ctx)
            myIndex += 1
        coaches.reverse()
        if(x == 2):
            coaches = orderList(roundOne, coaches)
    await ctx.send('The draft is over!')
# This is how you define a discord.py event
@bot.event
async def on_ready():  # the event `on_ready` is triggered when the bot is ready to function
    print("The bot is READY!")
    print("Logged in as: {}".format(bot.user.name))

#@bot.event
#async def on_message(message):
    #ignoring messages by the bot to avoid infinite looping
#    if message.author.id == bot.user.id:
#        return
#
#    if message.content.startswith('$draft'):
#        await message.channel.send('{} said Draft!'.format(message.author.mention))
@bot.event
async def on_error(event, *args, **kwargs):
    #"""
    #Catches any exception that occurs during the bot's loop.
    #If any exception is raised in ``on_error``, it will `not` be handled.
    #The exception itself can be accessed from :class:`sys.exc_info`.
    #Args:
        #event:
        #    The name of the event that raised the exception.
        #*args:
        #    The positional arguments for the event that raised the exception
        #**kwargs:
        #     The keyword arguments for the event that raised the exception.
    #"""
    print("OH NO!, AN ERROR ")
    print("Error from:", event)
    print("Error context:", args, kwargs)

    from sys import exc_info

    exc_type, value, traceback = exc_info()
    print("Exception type:", exc_type)
    print("Exception value:", value)
    print("Exception traceback object:", traceback)

bot.run(TOKEN)