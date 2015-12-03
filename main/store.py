from datetime import datetime, date
from dateutil.rrule import DAILY, rrule
import logging
import os
from os import path
import pickle

from apis import twitter_api, flickr_api, Query, wunderground_api
from apis.twitter_api import Tweet, TwitterSearchQuery
from main.local_config import ROOT_DIR


STORE_DIR = path.join(ROOT_DIR, 'store_room')
FLICKR_DIR = 'flickr'
TWITTER_DIR = 'twitter'
WUNDERGROUND_DIR = 'wunderground'

logger = logging.getLogger('main')


class StoreType(object):
    def __init__(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.directory = directory


STREAMING_TWEETS = StoreType(path.join(STORE_DIR, TWITTER_DIR, 'stream'))
SEARCH_TWEETS = StoreType(path.join(STORE_DIR, TWITTER_DIR, 'search'))
TWITTER_PLACE = StoreType(path.join(STORE_DIR, TWITTER_DIR, 'place'))
N_PHOTOS = StoreType(path.join(STORE_DIR, FLICKR_DIR, 'n_photos'))
WUNDERGROUND_RAIN = StoreType(path.join(STORE_DIR, WUNDERGROUND_DIR, 'rain'))

store_types = [STREAMING_TWEETS, SEARCH_TWEETS, TWITTER_PLACE, N_PHOTOS, WUNDERGROUND_RAIN]
for store_type in store_types:
    directory = store_type.directory
    if not path.exists(directory):
        os.mkdir(directory)


def read(store_type: StoreType, query: Query):
    logger.info('Reading store for %s.', query)
    storage_path = _get_storage_path(store_type, query)

    if not path.exists(storage_path):
        logger.info('No data found in store. Will retrieve new data.')
        save(store_type, query)
        logger.info('Data retrieved and saved in store.')

    with open(storage_path, 'rb') as f:
        answer = pickle.load(f)
        return answer


def save(store_type: StoreType, query):
    """Downloads and saves data on disc according to query and store_type."""

    storage_path = _get_storage_path(store_type, query)
    if os.path.exists(storage_path):
        raise Exception('Data for query %s already in store.', query)

    if store_type == STREAMING_TWEETS:
        listener = twitter_api.StoringListener(status_handler=_save_streaming_tweet)
        twitter_api.start_streaming(listener, query.bounding_box)

    elif store_type == SEARCH_TWEETS:
        tweets = twitter_api.download_search_tweets(query)
        with open(storage_path, 'wb') as f:
            pickle.dump(tweets, f)

    elif store_type == N_PHOTOS:
        n_photos = flickr_api.count_photos(query)
        with open(storage_path, 'wb') as f:
            pickle.dump(n_photos, f)

    elif store_type == WUNDERGROUND_RAIN:
        rain_series = wunderground_api.get_rain(query)
        with open(storage_path, 'wb') as f:
            pickle.dump(rain_series, f)

    else:
        raise RuntimeError('Store for %s not yet implemented.', store_type)

# TODO outdated?
# def get_search_tweets(place_id: str, begin: date, end: date = None):
#
#     tweets = []
#     if end is None:
#         end = begin
#     for day in rrule(DAILY, dtstart=begin, until=end):
#         query = TwitterSearchQuery(place_id=place_id, date=day)
#         statuses = read(store_type=SEARCH_TWEETS, query=query)
#         for status in statuses:
#             tweets.append(Tweet(status))
#     return tweets


def remove(store_type: StoreType, query: Query):
    storage_path = _get_storage_path(store_type, query)
    if not os.path.exists(storage_path):
        logger.warning('Trying to remove store item which does not exist.')
    else:
        os.remove(storage_path)


def _get_storage_path(store_type: StoreType, query: Query):

    extension = 'p'
    dir_name = store_type.directory
    filename = '%s.%s' % (repr(query), extension)

    return os.path.join(dir_name, filename)


def _save_streaming_tweet(status):
    now = datetime.now()
    timestamp = (now - datetime(1970, 1, 1)).total_seconds()
    filename = '%s.p' % timestamp
    path = os.path.join(STREAMING_TWEETS.directory, filename)

    with open(path, mode='w') as f:
        pickle.dump(status, f)


def _pickle_to_file(object_to_pickle, storage_path):
    with open(storage_path, 'wb') as f:
        pickle.dump(object_to_pickle, f)


def _depickle_from_file(storage_path):
    with open(storage_path, 'rb') as f:
        return pickle.load(f)


def get_twitter_place(twitter_place_id: str):

    file_name = '%s.p' % twitter_place_id
    storage_path = join(TWITTER_PLACE.directory, file_name)
    if not path.exists(storage_path):
        try:
            twitter_place = twitter_api.api.geo_id(twitter_place_id)
        except:
            twitter_api.print_limit_status()
            raise RuntimeError('No data from twitter api. Probably rate limit problem.')
        _pickle_to_file(twitter_place, storage_path)

    twitter_place = _depickle_from_file(storage_path)
    return twitter_place


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