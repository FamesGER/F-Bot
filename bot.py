import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import datetime
import io

import twitterstatus, botgspread

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
		if timeNow.hour == 10 and timeNow.minute == 1: #UTC 10:01 
			newDuck = twitterstatus.getTweet(c_key,c_secret,a_token,a_secret).tweetStatus() #get tweet and media from DucksDaily, plus insert the tokens
			await bot.send_message(animalChannel, newDuck)
			botgspread.botgspread().row_ins(val="New duck" + str(timeNow.hour))
			await asyncio.sleep(60)
		else:
			await asyncio.sleep(10) # task runs every 10 seconds

@bot.event
async def on_ready():
	print("Bot is ready")
	await bot.change_presence(game=discord.Game(name='with other bots '))

@bot.event
async def on_reaction_add(reaction,user):
	if str(reaction.emoji) == "<:GWfroggySadCat:400751069619159050>":
		await bot.add_reaction(reaction.message, emoji = reaction.emoji)
	
	if str(reaction.emoji) == "🇫":
		await bot.add_reaction(reaction.message, emoji = reaction.emoji)


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
			timeNow = datetime.datetime.now()
			gspreadmessage = [message.author.name, message.content, str(timeNow.month) + "." +  str(timeNow.day) + " at " + str(timeNow.hour) + ":" + str(timeNow.minute) + " UTC"]
			botgspread.botgspread().row_ins(val=gspreadmessage)
		except:
			return

	if message.content.upper().startswith("!INFO"):
		args = message.content.split(" ") #get message after command

		if "".join(args[1:]) == 'server': #if !info server is called
			newServer = message.server
			numOffline = 0 #online
			numOnline = 0 #offline
			numIdle = 0 #away
			numDND = 0 #busy
			for currentMember in newServer.members:
				if str(currentMember.status) == "online":
					numOnline = numOnline +1
				elif str(currentMember.status) == "offline":
					numOffline = numOffline +1
				elif str(currentMember.status) == "idle":
					numIdle = numIdle +1
				else:
					numDND = numDND +1

			serverEmbed = discord.Embed(

				title= newServer.name,
				description= 	"**❯ General information** \n"
								"Server region: " + str(newServer.region)+ "\n"
								"Created at: " + str(newServer.created_at)+ "\n"
								"Members: " + str(newServer.member_count) + "\n"
								"**❯ Members** \n"
								"**Total online**: " + str((numOnline + numIdle + numDND)) + "\n"
								"Online: " + str(numOnline) + "\n"
								"Idle: " + str(numIdle) + "\n"
								"Busy: " + str(numDND) + "\n"
								"Offline: " + str(numOffline) + "\n"
								"**❯ Useless information** \n"
								"Owner: " + str(newServer.owner.name) + "\n"
								"Special features: " + str(newServer.features) +"\n"
								"Splash: " +str(newServer.splash_url) + "\n"
				)
			serverEmbed.set_image(url=newServer.icon_url)
			serverEmbed.set_footer(text= "Requested from: " + message.author.name)


			await bot.send_message(message.channel,embed=serverEmbed)


		else:
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
					botCheck = "is a bot🤖"
				else:
					botCheck= "is not a bot"

				try:
					nickCheck= str(user.nick)
				except:
					nickCheck = ""

				userEmbed = discord.Embed( #create the embed
					title = user.name + " (" + nickCheck + ")",
					description=
									"ID: " +user.id + "\n"
									"Is playing: "+str(user.game) + "\n"
									"Status: "+str(user.status) + "\n"
									"User " + botCheck + "\n"
									"Joined at: " + str(user.joined_at) + "\n"
				)
				userEmbed.set_image(url=user.avatar_url) #set the pinged user's avatar as the image
				userEmbed.set_footer(text= "Requested from: " + message.author.name)
				await bot.send_message(message.channel,embed=userEmbed)
			except:
				await bot.send_message(message.channel,"E")

	if message.content.upper().startswith("!SADCAT") or message.content.startswith("<:GWfroggySadCat:400751069619159050>"):
		embed = discord.Embed()
		embed.set_image(url="https://raw.githubusercontent.com/FamesGER/F-Bot/master/sadCat.png") #sadcat image from github
		await bot.send_message(message.channel,embed=embed)

	if ("PAY" in  message.content.upper() and ("RESPECT" in message.content.upper() or "RESPECC" in message.content.upper())) or ("PRESS" in message.content.upper() and "F" in message.content.upper()) or message.content.upper().startswith("F") :
		if message.content.upper().startswith("F") and len(message.content) > 1:
			if ("PAY" in  message.content.upper() and ("RESPECT" in message.content.upper() or "RESPECC" in message.content.upper())) or ("PRESS" in message.content.upper() and "F" in message.content.upper()):
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
			
	if message.content.upper().startswith('!CLEARGSPREAD') and message.author.id == "143132657692311561":
		botgspread.botgspread().delete_allrows()
		
#bot.loop.create_task(bphMessageSend())
bot.loop.create_task(dailyDuck()) #daily duck, 10:00am UTC

bot.run(os.environ.get('token'))
