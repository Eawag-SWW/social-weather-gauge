from copy import deepcopy
from datetime import datetime, timedelta
from dateutil.rrule import DAILY, rrule
import logging
import os
import pickle
from os.path import join

import pandas as pd

from apis import twitter_api, flickr_api
from apis.twitter_api import Tweet, TwitterSearchQuery


STORE_DIR = 'store'
FLICKR_DIR = 'flickr'
TWITTER_DIR = 'twitter'

logger = logging.getLogger('main')


class StoreType(object):
    def __init__(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.directory = directory


STREAMING_TWEETS = StoreType(join(STORE_DIR, TWITTER_DIR, 'stream'))
SEARCH_TWEETS = StoreType(join(STORE_DIR, TWITTER_DIR, 'search'))
N_PHOTOS = StoreType(join(STORE_DIR, FLICKR_DIR, 'n_photos'))


def read(query, store_type):
    logger.info('Reading store for %s ...', query)
    path = _get_storage_path(query, store_type)

    if not os.path.exists(path):
        save(query, store_type)

    with open(path, 'rb') as f:
        answer = pickle.load(f)
        logger.debug('... finished.')
        return answer


def save(query, store_type):

    storage_path = _get_storage_path(query, store_type)

    if store_type == STREAMING_TWEETS:
        listener = twitter_api.StoringListener(status_handler=_save_streaming_tweet)
        twitter_api.start_streaming(listener, query.bounding_box)

    if store_type == SEARCH_TWEETS:
        tweets = twitter_api.download_search_tweets(query)
        with open(storage_path, 'wb') as f:
            pickle.dump(tweets, f)

    if store_type == N_PHOTOS:
       n_photos = flickr_api.count_photos(query)
       with open(storage_path, 'wb') as f:
           pickle.dump(n_photos, f)

    else:
        raise RuntimeError('Store for %s not yet implemented.', store_type)

        # path = _get_path(query, type)
        #

        #
        # elif type == StoreType.POINTS:
        #     points = flickr_api.get_points(query)
        #     f = open(path, 'wb')
        #     pickle.dump(points, f)
        #
        # elif type == StoreType.TWEETS:
        #     tweets = twitter_api.download_tweets(query)
        #     f = open(path, 'wb')
        #     pickle.dump(tweets, f)
        #
        #


def get_search_tweets(place_id, begin, end=None, use_cache=False):

    tweets = []
    if end == None:
        end = begin
    for day in rrule(DAILY, dtstart=begin, until=end):
        query = TwitterSearchQuery(place_id=place_id, date=day)
        if not use_cache:
            save(query, store_type=SEARCH_TWEETS)
        statuses = read(query, store_type=SEARCH_TWEETS)
        for status in statuses:
            tweets.append(Tweet(status))
    return tweets




# def get_tweets(store_type):
#     tweets = []
#     dirname = store_type.directory
#
#     for filename in os.listdir(dirname):
#         path = os.path.join(dirname, filename)
#         with open(path, 'r') as f:
#             data = pickle.load(f)
#             if store_type == SEARCH_TWEETS:
#                 for status in data:
#                     tweets.append(Tweet(status))
#             elif store_type == STREAMING_TWEETS:
#                 tweets.append(Tweet(data))
#
#     return tweets


# def get_tweets_dataframe(store_type, begin=None, end=None):
#     tweets = get_tweets(store_type)
#     tweet_dicts = [vars(tweet) for tweet in tweets]
#     dataframe = pd.DataFrame(tweet_dicts)
#     dataframe.index = dataframe.created_at
#     dataframe.sort(inplace=True)
#     dataframe = dataframe[begin:end]
#     return dataframe


def _get_storage_path(query, store_type):

    extension = 'p'

    dirname = store_type.directory
    filename = '%s.%s' % (repr(query), extension)
    return os.path.join(dirname, filename)


def _save_streaming_tweet(status):
    now = datetime.now()
    timestamp = (now - datetime(1970, 1, 1)).total_seconds()
    filename = '%s.p' % timestamp
    path = os.path.join(STREAMING_TWEETS.directory, filename)

    with open(path, mode='w') as f:
        pickle.dump(status, f)


