# -*- coding: utf-8 -*-

import random
import logging

from enum import Enum
import flickrapi

from geo import Point
import secrets



FLOODING_TAGS = dict()
FLOODING_TAGS['de'] = 'hochwasser, überschwemmung, überflutung, flut'
FLOODING_TAGS['fr'] = 'crue, inondation'
FLOODING_TAGS['en'] = 'flood, high-water'
FLOODING_TAGS['it'] = 'inondazione, alluvione'


FORMAT = 'etree'  # 'parsed-json'
API_KEY = secrets.API_KEY
API_SECRET = secrets.API_SECRET
PER_PAGE_DEFAULT = 200

WOE_ID_SWITZERLAND = 23424957
PLACE_ID_SWITZERLAND = 'HfSZnNxTUb7.Mo5Vpg'

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format=FORMAT)
logger = logging.getLogger('main')


class QueryType(Enum):
    TAGS = 1


class FlickrQuery(object):
    def __init__(self, language, query_type, only_geotagged):

        self.language = language
        self.query_type = query_type
        self.only_geotagged = only_geotagged

        params = dict()
        params['extras'] = 'geo'
        if only_geotagged:
            params['has_geo'] = 1
        if query_type == QueryType.TAGS:
            params['tags'] = FLOODING_TAGS[language]
        self.params = params

    def __repr__(self):
        string = '%s_%s_%s' % (self.query_type, self.language, self.only_geotagged)
        string = string.lower()
        return string



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
        return points


    def get_random_link(self):
        pass
        # todo: this just takes a photo of the the first n
        photo = random.choice(self._data)
        return 'https://www.flickr.com/photos/%s/%s' % (photo['owner'], photo['id'])


def get_photos(query, per_page=PER_PAGE_DEFAULT):
    params = query.params
    params['per_page'] = per_page
    iterator = flickr.walk(**params)
    collection = PhotoCollection(iterator)
    return collection


def count_photos(query, year=None):
    params = query.params
    if year:
        params['min_upload_date'] = '%s-01-01' % year
        params['max_upload_date'] = '%s-12-31' % year
    response = flickr.photos.search(**params)
    photos = response[0]
    total = photos.attrib['total']
    return int(total)


def get_points(query, per_page=PER_PAGE_DEFAULT):
    logger.info('Querying points from Flickr ...')
    photo_collection = get_photos(query, per_page=per_page)
    points = photo_collection.to_points()
    logger.info('... finished.')
    return points