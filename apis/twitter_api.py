import tweepy

import secrets

CONSUMER_KEY = secrets.TWITTER_CONSUMER_KEY
CONSUMER_SECRET = secrets.TWITTER_CONSUMER_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

api = tweepy.API(auth)


result = api.search('regen')
print dir(result)
