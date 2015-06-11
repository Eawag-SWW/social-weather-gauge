import logging
import pickle

from enum import Enum
import pandas as pd

from apis import flickr_api
from apis import twitter_api
from config import START_YEAR, END_YEAR

logger = logging.getLogger('main')


class CacheType(Enum):
    FLICKR_PLOT = 1
    POINTS = 2
    TWEETS = 3


def read(query, type):
    logger.debug('Reading cache for %s ...', query)
    path = _get_path(query, type)

    if type == CacheType.FLICKR_PLOT:
        answer = pd.Series.from_csv(path)
    elif type == CacheType.POINTS or type == CacheType.TWEETS:
        f = open(path, 'rb')
        answer = pickle.load(f)
        logger.debug('... finished. %n items read.', len(answer))
    else:
        raise RuntimeError('Undefined CacheType: %s', type)
    return answer


def save(query, type):
    path = _get_path(query, type)

    if type == CacheType.FLICKR_PLOT:
        data = dict()
        for year in range(START_YEAR, END_YEAR):
            n_photos = flickr_api.count_photos(query, year)
            data[year] = n_photos
        series = pd.Series(data)
        series.to_csv(path)

    elif type == CacheType.POINTS:
        points = flickr_api.get_points(query)
        f = open(path, 'wb')
        pickle.dump(points, f)

    elif type == CacheType.TWEETS:
        tweets = twitter_api.download_tweets(query)
        f = open(path, 'wb')
        pickle.dump(tweets, f)

    else:
        raise RuntimeError('Undefined CacheType: %s', type)


def _get_path(query, type):

    if type == CacheType.FLICKR_PLOT:
        extension = 'csv'
    else:
        extension = 'p'

    dir = type.name.lower()
    filename = repr(query)
    path = 'cache/%s/%s.%s' % (dir, filename, extension)
    return path