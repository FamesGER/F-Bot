import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import io
from PIL import Image
import requests
from io import BytesIO
from io import StringIO
import urllib

Client = discord.Client()
bot= commands.Bot(command_prefix = "") #use this prefix for commands

@bot.event
async def on_ready():
	print("Bot is ready")

	for server in Client.servers: 
        # Spin through every server
		for channel in server.channels: 
			# Channels on the server
			await bot.send_message(channel, "...")
				# So that we don't send to every channel:
			break

@bot.event
async def on_message(message):
	if message.author.id == "459090830330691594": #go out of function if the bot wrote the command
		return

	if message.content.upper().startswith("!PING"):
		await bot.send_message(message.channel, "Pong!")

	if message.content.upper().startswith("!LOSS"):
		await bot.add_reaction(message,emoji="👆")	#pointing up
		await bot.add_reaction(message,emoji="👐")	#open hands
		await bot.add_reaction(message,emoji="✌")	#peace sign
		await bot.add_reaction(message,emoji="💪")	#flex

	if message.content.upper().startswith("!SAY"):
		try:
			args = message.content.split(" ") #get message after command
		#args[0] = !SAY
		#args[1] = Hi
		#args[2] = there
			
			await bot.send_message(message.channel, " ".join(args[1:]))
		except:
			print ("No say input")
			return
	
	if message.content.upper().startswith("!INFO"):
		try:
			server = message.server #get the server that the message got typed in
			userIDdirty= message.author.mention #get the user that typed it
			userID = ("".join(e for e in userIDdirty if e.isalnum()))
			user = server.get_member(userID)
			bot.send_message(message.channel, str(user))
			if user.game == None: #check if the user is playing anything
				user.game = ("Nothing")
			await bot.send_message(message.channel,"The username is: {}".format(user.name))
			await bot.send_message(message.channel,"The user's ID is: " + user.id)
			await bot.send_message(message.channel,"The user is playing: " + str(user.game))
			await bot.send_message(message.channel,"The user is " + str(user.status))
		except:
			await bot.send_message(message.channel, "No Info")
			return
	if message.content.upper().startswith("!TESTIMG"):
		try:
			image = message.attachments
			await bot.send_message(message.channel, image[0]['url']) #returns image url
		except:
			await bot.send_message(message.channel,"No Image")

	if message.content.upper().startswith("!SADCAT") or message.content.startswith("<:GWfroggySadCat:400751069619159050>"):
		embed = discord.Embed()
		embed.set_image(url="https://raw.githubusercontent.com/FamesGER/F-Bot/master/sadCat.png")
		await bot.send_message(message.channel,embed=embed)





	#if message.content.startswith("<:GWfroggySadCat:400751069619159050>"): #if someone starts with the ol' classic sadCat emoji
	#	await bot.add_reaction(message,emoji="😢")


bot.run(os.environ.get('token'))
