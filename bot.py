import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio

import time
token = process.env.token
Client = discord.Client()
bot= commands.Bot(command_prefix = "!") #use this prefix for commands


@bot.event
async def on_ready():
	print("Bot is ready")

@bot.command(pass_context=True)
async def ping(ctx): #ping is the actual command name
	await bot.say(":ping_pong: ping!")
	print("Ping command")
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
	if user.game == None: #check if the user is playing anything
		user.game = "Nothing"
	await bot.say("The username is: {}".format(user.name))
	await bot.say("The user is playing: " + str(user.game))
	await bot.say(user.name + " is " + str(user.status))
@info.error #if !info errors
async def test_on_error(ctx,error):
	bot.say("No user input")





bot.run(os.environ.get('token'))
