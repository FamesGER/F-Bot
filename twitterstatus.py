
class getTweet():
	def __init__(self, consumer_key,consumer_secret,acces_token_access_secret):
		self.c_key = consumer_key
		self.c_secret = consumer_secret
		self.a_token = access_token
		self.a_secret = access_secret
	
	import tweepy
	from tweepy import OAuthHandler

	auth = OAuthHandler(self.c_key, self.c_secret)
	auth.set_access_token(self.a_token, self.a_secret)
	 
	twitterAPI = tweepy.API(auth)

	tweet = twitterAPI.user_timeline(screen_name = '@Ducks_Daily', count = 1, include_rts = False, include_entities =True) #get 1 tweet from Ducks Daily 
	
	def tweetMedia():
		for media in getTweet.tweet:
			return (media.entities['media'][0]['media_url_https'])
	def tweetStatus():
		for status in getTweet.tweet:
			return (status.entities['media'][0]['expanded_url'])
