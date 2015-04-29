# -*- coding: utf-8 -*-

from enum import Enum
import random
import logging

import flickrapi

import secrets


FORMAT = 'etree' # 'parsed-json'
API_KEY = secrets.API_KEY
API_SECRET = secrets.API_SECRET
PER_PAGE_DEFAULT = 200

WOE_ID_SWITZERLAND = 23424957
PLACE_ID_SWITZERLAND = 'HfSZnNxTUb7.Mo5Vpg'

FLOODING_TAGS_DE = 'hochwasser, überschwemmung, überflutung, flut'

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format=FORMAT)
logger = logging.getLogger('main')

class Query(Enum):
    switzerland = 1
    switzerland_flooding_text = 2
    switzerland_flooding_tags = 3
    geotagged_flooding_tags = 4


class Point(object):
    pass


class PhotoCollection:

    def __init__(self, iterator):
        self._iterator = iterator

    def to_points(self):
        points = []
        count = 0
        for photo in self._iterator:
            point = Point()
            point.lat = photo.get('latitude')
            point.lon = photo.get('longitude')
            points.append(point)
            count += 1
            if count % 10000 == 0:
                logger.debug(count)
        return points


    def get_random_link(self):
        pass
        # todo: this just takes a photo of the the first n
        photo = random.choice(self._data)
        return 'https://www.flickr.com/photos/%s/%s' % (photo['owner'], photo['id'])


def get_photos(query, with_geotags=False, per_page=PER_PAGE_DEFAULT):
    params = _get_params(query, with_geotags=with_geotags)
    photos = _get_photos_from_params(params, per_page=per_page)
    return photos

def _get_params(query, with_geotags=False):
    """

    :rtype : dict
    """
    params = dict()

    if with_geotags:
        params['extras'] = 'geo'

    if query == Query.switzerland:
        params['woe_id'] = WOE_ID_SWITZERLAND

    elif query == Query.switzerland_flooding_text:
        params['woe_id'] = WOE_ID_SWITZERLAND
        params['text'] = 'hochwasser'

    elif query == Query.switzerland_flooding_tags:
        params['woe_id'] = WOE_ID_SWITZERLAND
        params['tags'] = FLOODING_TAGS_DE

    elif query == Query.geotagged_flooding_tags:
        params['has_geo'] = 1
        params['tags'] = FLOODING_TAGS_DE

    else:
        raise Exception('invalid params name')
        # thun_params = dict()
        # thun_params['tags'] = tags
        # thun_params['lat'] = 47.566667 # 46.76
        # thun_params['lon'] =  7.6 # 7.624
        # thun_params['radius'] = RADIUS
        # params_list.append(thun_params)
    return params

def _get_photos_from_params(params, per_page=PER_PAGE_DEFAULT):
    params['per_page'] = per_page
    iterator = flickr.walk(**params)
    collection = PhotoCollection(iterator)
    return collection

def count_photos(query, year=None):
    params = _get_params(query)
    if year:
        params['min_upload_date'] = '%s-01-01' % year
        params['max_upload_date'] = '%s-12-31' % year
    response = flickr.photos.search(**params)
    photos = response[0]
    total = photos.attrib['total']
    return total

def get_points(query, per_page=PER_PAGE_DEFAULT):
    logger.debug('Querying points from flickr...')
    photo_collection = get_photos(query, with_geotags=True, per_page=per_page)
    points = photo_collection.to_points()
    logger.debug('finished')
    return points