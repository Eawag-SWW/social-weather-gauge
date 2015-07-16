from datetime import timedelta, datetime
import logging
from pprint import pprint

import tweepy
from tweepy import Cursor, StreamListener, Stream

from apis import Query
import secrets


logger = logging.getLogger('main')

CONSUMER_KEY = secrets.TWITTER_CONSUMER_KEY
CONSUMER_SECRET = secrets.TWITTER_CONSUMER_SECRET

PLACE_ID_ZURICH = '3acb748d0f1e9265'
PLACE_ID_GERMANY = 'fdcd221ac44fa326'
PLACE_ID_BERLIN_CITY = '3078869807f9dd36'
PLACE_ID_LONDON_CITY = '457b4814b4240d87'
PLACE_ID_LONDON_ADMIN = '5d838f7a011f4a2d'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token('56120535-CkZqukNLJXx66Buxv8DTVdirmbJP6IuBSJvRdQApT',
                      'jqp67goMi7zSHFjAHk5ARM8SEiCXhdUH70AAQKeAso9JQ')
api = tweepy.API(auth)


class Tweet(object):
    def __init__(self, status=None):
        if status:
            self.created_at = status.created_at
            self.text = status.text
            self.coordinates = status.coordinates
            if status.place:
                self.place = status.place.full_name

            self.hashtags = []
            for hashtag in status.entities['hashtags']:
                self.hashtags.append(hashtag['text'])

    def __str__(self):
        if hasattr(self, 'place'):
            place_string = self.place.encode('UTF-8')
        else:
            place_string = 'No Place.'
        return '''
        ---
        %s
        %s
        %s

        %s
        ---
        ''' % (self.created_at, self.coordinates, place_string, self.text.encode('UTF-8'))


class TwitterSearchQuery(Query):
    def __init__(self, place_id=None, date=None):
        self.place_id = place_id
        self.date = date

    def __repr__(self):
        return '%s_%s' % (self.place_id, self.date.strftime('%m-%d'))


class TwitterStreamingQuery(Query):
    def __init__(self, bounding_box):
        self.bounding_box = bounding_box


class TwitterStreamListener(StreamListener):
    def __init__(self):
        super(TwitterStreamListener, self).__init__()

    def on_error(self, status_code):
        print 'ERROR. Code: %s.' % status_code


class StoringListener(TwitterStreamListener):
    def __init__(self, status_handler):
        super(StoringListener, self).__init__()
        self.status_handler = status_handler

    def on_connect(self):
        logger.info('Connected to Twitter Stream.')
        logger.info('Start time: ' + datetime.now().strftime('%c'))

    def on_status(self, status):
        if hasattr(status, 'place') and status.place.place_type == 'country':
            logger.info('Excluded tweet with place: %s.', status.place.full_name)
        else:
            self.status_handler(status)
            logger.info('Good tweet.')


class PrintingListener(TwitterStreamListener):
    def on_status(self, status):
        print 'Status:'
        pprint(vars(status))


def download_search_tweets(query):
    logger.info('Downloading Tweets for query %s ...', query)
    tweets = []
    place_id = query.place_id
    date = query.date
    fmt = '%Y-%m-%d'
    since = date.strftime(fmt)
    until = (date + timedelta(days=1)).strftime(fmt)
    query = 'place:%s since:%s until:%s' % (place_id, since, until)
    cursor = Cursor(api.search, q=query, count=100)
    for tweet in cursor.items():
        tweets.append(tweet)
    logger.info('... finished.')
    return tweets


def start_streaming(stream_listener, bounding_box=None):
    stream = Stream(auth=api.auth, listener=stream_listener)
    parameters = dict()
    if bounding_box:
        locations = [bounding_box.south_west_lon, bounding_box.south_west_lat,
                     bounding_box.north_east_lon, bounding_box.north_east_lat]
        parameters['locations'] = locations
        # track = []
    try:
        stream.filter(**parameters)
    except:
        logger.error('Streaming error. Will try egain.')
        start_streaming(stream_listener, bounding_box)


def date_string_to_datetime(date):
    pass


def print_place_info(place_id):
    response = api.geo_id(place_id)
    pprint(vars(response))


def print_places(query_string):
    result = api.geo_search(query=query_string)
    print 'Places for query "%s" (%d results)' % (query_string, len(result))
    print '---'
    for place in result:
        print ' - %s (id: %s, type: %s)' % (place.full_name, place.id, place.place_type)
