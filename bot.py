import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import datetime
import io
import requests

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
	if str(reaction.emoji) == "<:GWfroggySadCat:400751069619159050>" or str(reaction.emoji) == "🇫":
		await bot.add_reaction(reaction.message, emoji = reaction.emoji)
@bot.event
async def on_reaction_remove(reaction,user):
	if str(reaction.emoji) == "<:GWfroggySadCat:400751069619159050>" or str(reaction.emoji) == "🇫" and reaction.count == 1 : #if last emoji is unreacted, unreact too
		await bot.remove_reaction(reaction.message, emoji = reaction.emoji, member= reaction.message.server.me)

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
			await bot.send_message(message.channel,"".join(args[1:]))
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
								"*Total online*: " + str((numOnline + numIdle + numDND)) + "\n"
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
			serverEmbed.set_footer(text= "Requested by: " + message.author.name)

			await bot.send_message(message.channel,embed=serverEmbed)
		elif "".join(args[1:]).isdigit() == True: #if userID is put in instead
			try:
				user = bot.get_user_info(str(args[1:]))
				print (user().name)
			except:
				return
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

	if message.content.upper().startswith("!SADCAT"):
		response = requests.get("https://raw.githubusercontent.com/FamesGER/F-Bot/master/sadCat.png", stream=True)
		await bot.send_file(message.channel, io.BytesIO(response.raw.read()), filename='sadCat.png')

	if message.content.startswith("<:GWfroggySadCat:400751069619159050>"):
		try:
			for x in bot.get_all_emojis():
				if x.id == '479740476992258078':
					await bot.add_reaction(message, x)
		except:
			print("sadcat didn't work")
		
	if message.content.upper().startswith("!CRYCAT"):
		response = requests.get("https://raw.githubusercontent.com/FamesGER/F-Bot/master/screamcat.png", stream=True)
		await bot.send_file(message.channel, io.BytesIO(response.raw.read()), filename='cryCat.png')
	
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

		if messageNEW == "sadcat": #if message has sadcat in the beginning,
			response = requests.get("https://raw.githubusercontent.com/FamesGER/F-Bot/master/sadCat.png", stream=True)
			await bot.send_file(message.channel, io.BytesIO(response.raw.read()), filename='sadCat.png')
		else: #if not, send the normal message
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
		
	if message.content.upper().startswith('!GAME'):

		serverMembers = message.server.members
		args = message.content.split(" ") #get message after command
		if "".join(args[1:]) == 'players': #lists members with Game role
			newText=[]
			#newText.append('```')#beginn
			for member in serverMembers:
				if "473379902708514817" in [y.id for y in member.roles]:
					newText.append(str(member.name))
			#newText.append('```')#end
			gameEmbed = discord.Embed( #create the embed
					title = "Gamers",
					description = str(newText)
				)	
			gameEmbed.set_footer(text= "Requested by: " + message.author.name)
			await bot.send_message(message.channel, embed=gameEmbed)

		if "".join(args[1]) == 'list':
			gamesListRaw = botgspread.botgspread(sheetNumber= 1).row_val() #get the current row
			print(str(gamesListRaw))
			gamesListFormat1 = str(gamesListRaw).replace("', '","\n")
			gamesListFormat2 = str(gamesListFormat1.replace("['","")).replace("']","")

			gamesList= gamesListFormat2
			listEmbed = discord.Embed(
				title= "Games",
				description=gamesList
				)
			#for x in gamesList:
			#	listEmbed.add_field(name="_ _",value=x,inline=False) #inline is false to it creates a new line for each game
			await bot.send_message(message.channel, embed=listEmbed)

		#if arg 1(second) is add, add everything arg 2 to the sheet
		if "".join(args[1]) == 'add':
			addedGame= str("".join(args[2]))
			currentGames = botgspread.botgspread(sheetNumber= 1).row_val(1)
			currentGames.append(addedGame)
			newGames = currentGames
			botgspread.botgspread(sheetNumber= 1).delete_row() #delete old games row
			botgspread.botgspread(sheetNumber= 1).row_ins(val=newGames) #insert updated one
			
	if message.content.upper().startswith('THIS IS SO SAD'):
		try:
			for x in bot.get_all_emojis(): #get all the emojis
				if x.id == '479740476992258078': #find sadcat emoji
					await bot.add_reaction(message, x)
		except:
			print("sadcat didn't work")
			
	if message.content.upper().startswith('YEE HAW') or message.content.upper().startswith('YEEHAW') or message.content.upper().startswith('YEEYEE') or message.content.upper().startswith('YEE YEE'):
		try:
			await bot.add_reaction(message,emoji="🤠")
		except:
			print("sad")

bot.loop.create_task(dailyDuck()) #daily duck, 10:00am UTC
bot.run(os.environ.get('token'))
