import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import datetime
import io

import twitterstatus

c_key = os.environ.get('c_key') 
c_secret = os.environ.get('c_secret')
a_token = os.environ.get('a_token')
a_secret = os.environ.get('a_secret')

Client = discord.Client()
bot= commands.Bot(command_prefix = "") #use this prefix for commands
async def dailyDuck():	
	await bot.wait_until_ready()
	animalChannel = discord.Object(id='435149265673912351') #py-buns animal kingdom
	while not bot.is_closed:
		timeNow = datetime.datetime.now()
		if timeNow.hour == 10 and timeNow.minute == 1: #UTC 10:01, 12:01 GMT+1 
			newDuck = twitterstatus.getTweet(c_key,c_secret,a_token,a_secret).tweetStatus() #get tweet and media from DucksDaily, plus insert the tokens
			await bot.send_message(animalChannel, newDuck)
		await asyncio.sleep(10) # task runs every 10 seconds

@bot.event
async def on_ready():
	print("Bot is ready")
	await bot.change_presence(game=discord.Game(name='with other bots '))

@bot.event
async def on_reaction_add(reaction,user):
	if str(reaction.emoji) == "<:GWfroggySadCat:400751069619159050>":
		await bot.add_reaction(reaction.message,emoji = reaction.emoji)
	else:
		return

@bot.event
async def on_message(message):
	if message.author.id == "459090830330691594": #go out of function if the bot did it
		return

	if message.content.upper().startswith("!KILLFBOT"):
		if message.author.id == "143132657692311561": #me
			await bot.add_reaction(message,emoji="💪")
			asyncio.sleep(10)
			await bot.logout()
			await bot.close()
		else:
			await bot.send_message(message.channel, "Only the bot owner can shut me down!")

	if message.content.upper().startswith("!PING"):
		await bot.send_message(message.channel, ":ping_pong: ")

	if message.content.upper().startswith("!LOSS"):
		try:
			await bot.add_reaction(message,emoji="🕛")	#12
			await bot.add_reaction(message,emoji="🕐")	#1
			await bot.add_reaction(message,emoji="🕚")	#11
			await bot.add_reaction(message,emoji="🕒")	#3
		except:
			await bot.send_message(message.channel,"I don't have permissions to add reactions.")

	if message.content.upper().startswith("!SAY"):
		try:
			args = message.content.split(" ") #get message after command
		#args[0] = !SAY
		#args[1] = Hi
		#args[2] = there
			await bot.send_message(message.channel, " ".join(args[1:]))
		except:
			return

	if message.content.upper().startswith("!INFO"):
		try:
			try: #get mentioned user
				user = message.mentions[0]
			except: #if no user is mentioned, use the message author
				server = message.server #get the server that the message got typed in
				userIDdirty= message.author.mention #get the user that typed it
				userID = ("".join(e for e in userIDdirty if e.isalnum()))
				user = server.get_member(userID) #get the user in the server

			if user.game == None: #check if the user is playing anything
				user.game = ("Nothing")

			if user.bot == True: #check if the pinged user is a bot
				botCheck = " is a bot"
			else:
				botCheck= " is not a bot"
			userEmbed = discord.Embed( #create the embed
				title = user.name,
				description= 	"ID: " +user.id + "\n"
								"Is playing: "+str(user.game) + "\n"
								"Status: "+str(user.status) + "\n"
								"" + str(user.name) + botCheck + "\n"
			)
			userEmbed.set_image(url=user.avatar_url) #set the pinged user's avatar as the image
			userEmbed.set_author(name = "Requested from: " + message.author.name )
			await bot.send_message(message.channel,embed=userEmbed)
		except:
			await bot.send_message(message.channel,"E")

	if message.content.upper().startswith("!SADCAT") or message.content.startswith("<:GWfroggySadCat:400751069619159050>"):
		embed = discord.Embed()
		embed.set_image(url="https://raw.githubusercontent.com/FamesGER/F-Bot/master/sadCat.png") #sadcat image from github
		await bot.send_message(message.channel,embed=embed)

	if ("PAY" in  message.content.upper() and "RESPECT" in message.content.upper()) or ("PRESS" in message.content.upper() and "F" in message.content.upper()) or message.content.upper().startswith("F") :
		if message.content.upper().startswith("F") and len(message.content) > 1:
			if ("PAY" in  message.content.upper() and "RESPECT" in message.content.upper()) or ("PRESS" in message.content.upper() and "F" in message.content.upper()):
				await bot.add_reaction(message, emoji = "🇫")
			return
		await bot.add_reaction(message, emoji = "🇫")

	if message.content.upper().startswith("!TSOURCE") and message.author.id == "143132657692311561" : #like !say, but for me only and in TeamSource's meme crafting channel
		message.server = 	bot.get_server	("259795299034202113")	#teamsource
		message.channel = 	bot.get_channel	("308444015341076492") 	#memecrafting
		try:
			args = message.content.split(" ") #get message after command
			messageNEW = " ".join(args[1:])
		except:
			return

		if messageNEW == "sadcat":
			embed = discord.Embed()
			embed.set_image(url="https://raw.githubusercontent.com/FamesGER/F-Bot/master/sadCat.png") #sadcat image from github
			await bot.send_message(message.channel,embed=embed)
		else:
			await bot.send_message(message.channel, messageNEW)

	if message.content.upper().startswith("!DUCK"):
		newDuck = twitterstatus.getTweet(c_key,c_secret,a_token,a_secret).tweetStatus() #get tweet and media from DucksDaily
		await bot.send_message(message.channel, newDuck)

	if message.content.upper().startswith("!HELP"):
		import bothelp #import the bothelp file (to save space here)
		await bot.send_message(message.channel,bothelp.commandHelp())
		
	if message.content.upper().startswith("!RANDOMDUCK"):
		try:
			randomDuck = twitterstatus.getTweet(c_key,c_secret,a_token,a_secret).tweetRandom() #get random tweet
			await bot.send_message(message.channel, randomDuck)
		except:
			await bot.send_message(message.channel, "I couldn't get a random tweet!")
		

bot.loop.create_task(dailyDuck()) #daily duck, 10:00am UTC

bot.run(os.environ.get('token'))
