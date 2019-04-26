class getTweet():
	def __init__(self, consumer_key, consumer_secret, access_token, access_secret, twitterUser = "@LocalMallard", amount = 1):
		self.c_key = consumer_key
		self.c_secret = consumer_secret
		self.a_token = access_token
		self.a_secret = access_secret
		self.tUser = twitterUser
		self.tAmount= amount	
		
	def tweetAPI(self): #get twitter API
		import tweepy
		from tweepy import OAuthHandler
		auth = OAuthHandler(self.c_key, self.c_secret)
		auth.set_access_token(self.a_token, self.a_secret)

		twitterAPI = tweepy.API(auth,wait_on_rate_limit=True)
		return twitterAPI

	def tweet(self, customAmount = 1): #get a tweet
		tweet = self.tweetAPI().user_timeline(screen_name = self.tUser, count = customAmount	, include_rts = False, include_entities =True) #get n tweet from Ducks Daily 
		return tweet
	
	def tweetStatus(self):
			for status in self.tweet():
				try:
					return (status.entities['media'][0]['expanded_url'])
				except: #if it wasnt a tweet with media
					returnText = status.text
					return returnText

	def tweetRandom(self):
		import random
		randomAmount = 100
		tweet = self.tweet(customAmount= randomAmount)
		statusList = [];
		for status in tweet:
			try:
				statusList.append(status.entities['media'][0]['expanded_url']);
			except:
				continue
			#return (status.entities['media'][0]['expanded_url'])

		return random.choice(statusList)
