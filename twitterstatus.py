
class getTweet(consumer_key,consumer_secret,acces_token_access_secret):
	import tweepy
	from tweepy import OAuthHandler


	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	 
	twitterAPI = tweepy.API(auth)

	tweet = twitterAPI.user_timeline(screen_name = '@Ducks_Daily', count = 1, include_rts = False, include_entities =True) #get 1 tweet from Ducks Daily 
	def tweetMedia():
		for media in getTweet.tweet:
			return (media.entities['media'][0]['media_url_https'])
	def tweetStatus():
		for status in getTweet.tweet:
			return (status.entities['media'][0]['expanded_url'])
		
