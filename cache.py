import logging
import pickle

from enum import Enum
import pandas as pd

from apis import flickr_api
from config import START_YEAR, END_YEAR

logger = logging.getLogger('main')


class CacheType(Enum):
    plot = 1
    points = 2


def read(query, type):
    path = _get_path(query, type)

    if type == CacheType.plot:
        answer = pd.Series.from_csv(path)
    elif type == CacheType.points:
        f = open(path, 'rb')
        answer = pickle.load(f)
    else:
        raise RuntimeError('Undefined CacheType: %s', type)

    return answer


def save(query, type):
    path = _get_path(query, type)

    if type == CacheType.plot:
        data = dict()
        for year in range(START_YEAR, END_YEAR):
            n_photos = flickr_api.count_photos(query, year)
            data[year] = n_photos
        series = pd.Series(data)
        series.to_csv(path)

    elif type == CacheType.points:
        points = flickr_api.get_points(query)
        path = _get_path(query, type)
        f = open(path, 'wb')
        pickle.dump(points, f)

    else:
        raise RuntimeError('Undefined CacheType: %s', type)


def _get_path(query, type):

    if type == CacheType.plot:
        extension = 'csv'
    elif type == CacheType.points:
        extension = 'p'
    else:
        raise RuntimeError('Undefined CacheType')

    dir = type.name
    filename = query.name
    path = 'cache/%s/%s.%s' % (dir, filename, extension)
    return path