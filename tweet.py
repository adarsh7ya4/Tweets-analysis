import tweepy
import re
from tweepy import OAuthHandler
from textblob import TextBlob

#Generic Twitter Class for sentiment analysis
class TwitterClient(object):
	def __init__(self):
		# keys and tokens from the Twitter Dev Console 		
		consumer_key = 'NvJ6e2BykFHT4VktMOhAdwNoW'
		consumer_secret = 'smngxDDVSwyW27jYG57rnjPO0wdgQBX6Obs3Y3wYwH89WbN9UI'
		access_token = '708010108085612544-EzRPUH6v4r8iIRxxMPkQNSn6JXDnLmO'
		access_token_secret = 'uWxPdryQ5fGGSfjsf5CvXwpubFvur3IgS5G3mF5BU0tCf'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed!")
	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",tweet).split())

	def get_tweet_sentiment(self, tweet):
		# create Textblob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 10):
		tweets = []
		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = query, count = count)
			
			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error :" + str(e))

def main():
	# creating object of TwitterClient Class
	api = TwitterClient()
	#calling function to get tweets
	tweets = api.get_tweets(query = 'Article 370', count = 2000)
	
	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets
	print("Positive tweets percentage: ",100*len(ptweets)/len(tweets))

	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
	print("Negative tweets percentage: ",100*len(ntweets)/len(tweets))

	# percentage of neutral tweets
	print("Neutral tweets percentage: ",100*(len(tweets) - len(ptweets) - len(ntweets))/len(tweets))

	# printing first 5 positive tweets
	print("\n\nPositive tweets:")
	for tweet in ptweets[:10]:
		print(tweet['text'])

	# printing first 5 negative tweets
	print("\n\nNegative tweets:")
	for tweet in ntweets[:10]:
		print(tweet['text'])

if __name__ =="__main__":
	# calling main function
	main()
