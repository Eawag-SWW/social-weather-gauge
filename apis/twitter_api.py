from datetime import timedelta
import tweepy
from tweepy import Cursor
from apis import Query

import secrets

CONSUMER_KEY = secrets.TWITTER_CONSUMER_KEY
CONSUMER_SECRET = secrets.TWITTER_CONSUMER_SECRET

PLACE_ID_ZURICH = '3acb748d0f1e9265'
PLACE_ID_GERMANY = 'fdcd221ac44fa326'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)


class TwitterQuery(Query):
    def __init__(self, place_id=None, date=None):
        self.place_id = place_id
        self.date = date

    def __repr__(self):
        return '%s_%s' % (self.place_id, self.date.strftime('%m-%d'))


def download_tweets(query):
    tweets = []
    place_id = query.place_id
    date = query.date
    format = '%Y-%m-%d'
    since = date.strftime(format)
    until = (date + timedelta(days=1)).strftime(format)
    query = 'place:%s since:%s until:%s' % (place_id, since, until)
    cursor = Cursor(api.search, q=query, count=100)
    for tweet in cursor.items():
        tweets.append(tweet)
    return tweets

