from datetime import timedelta, datetime
import logging
from pprint import pprint

import tweepy
from tweepy import Cursor, StreamListener, Stream

from apis import Query
import secrets
from utils import Stopwatch


logger = logging.getLogger('main')

CONSUMER_KEY = secrets.TWITTER_CONSUMER_KEY
CONSUMER_SECRET = secrets.TWITTER_CONSUMER_SECRET

PLACE_ID_ZURICH = '3acb748d0f1e9265'
PLACE_ID_GERMANY = 'fdcd221ac44fa326'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token('56120535-CkZqukNLJXx66Buxv8DTVdirmbJP6IuBSJvRdQApT',
                      'jqp67goMi7zSHFjAHk5ARM8SEiCXhdUH70AAQKeAso9JQ')
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


class TwitterStreamListener(StreamListener):

    def __init__(self):
        super(TwitterStreamListener, self).__init__()

    def on_error(self, status_code):
        print 'ERROR. Code: %s.' % status_code


class OngoingStreamListener(TwitterStreamListener):
    def __init__(self):
        super(OngoingStreamListener, self).__init__()
        self.stopwatch = Stopwatch()

    def on_connect(self):
        logger.info('Connected to Twitter Stream.')
        logger.info('Start time: ' + datetime.now().strftime('%c'))
        self.stopwatch.start()

    def on_status(self, status):
        if hasattr(status, 'place') and status.place.place_type == 'country':
            with open('../temp/excluded_places.txt', 'a') as f:
                f.write(status.place.full_name + '\n')
        else:
            with open('../temp/tweets.txt', 'a') as f:
                f.write(status.place.full_name)
                f.write(status.coordinates)
                f.write(status.text)
                f.write('---')


class FirstTweetListener(TwitterStreamListener):
    def on_status(self, status):
        print 'status'

    def on_data(self, raw_data):
        print 'tocotronic'
        pprint(raw_data)


def print_place_info(place_id):
    response = api.geo_id(place_id)
    pprint(vars(response))


def stream(streamListener=OngoingStreamListener, bounding_box=None):
    listener = streamListener()
    stream = Stream(auth=api.auth, listener=listener)
    parameters = dict()
    if bounding_box:
        locations = [bounding_box.south_west_lon, bounding_box.south_west_lat,
                     bounding_box.north_east_lon, bounding_box.north_east_lat]
        parameters['locations'] = locations
        # track = []
    stream.filter(**parameters)


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    stream(streamListener=FirstTweetListener)
