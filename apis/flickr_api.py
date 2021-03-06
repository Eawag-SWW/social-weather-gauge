# -*- coding: utf-8 -*-
""" Classes and functions which abstract over the flickr api. """

import logging

import flickrapi
from apis import Query

from main.geo import Point
from main import secrets

FORMAT = 'etree'  # 'parsed-json'
API_KEY = secrets.FLICKR_API_KEY
API_SECRET = secrets.FLICKR_API_SECRET
PER_PAGE_DEFAULT = 200

WOE_ID_SWITZERLAND = 23424957
WOE_ID_USA = 23424977
WOE_ID_GERMANY = 23424829
# PLACE_ID_SWITZERLAND = 'HfSZnNxTUb7.Mo5Vpg'

logger = logging.getLogger('main')

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format=FORMAT)


class FlickrQuery(Query):
    def __init__(self, tags=None, woe_id: str = None,
                 year: int = None, only_geotagged=False):

        self.tags = tags
        self.woe_id = woe_id
        self.only_geotagged = only_geotagged
        if year:
            self.min_upload_date = '%s-01-01' % year
            self.max_upload_date = '%s-12-31' % year
        else:
            self.min_upload_date = None
            self.max_upload_date = None

        params = dict()
        params['extras'] = 'geo'
        params['tags'] = tags
        params['woe_id'] = woe_id
        if only_geotagged:
            params['has_geo'] = 1
        if self.min_upload_date:
            params['min_upload_date'] = self.min_upload_date
        if self.max_upload_date:
            params['max_upload_date'] = self.max_upload_date

        self.params = params

    def __repr__(self):
        string = '%s_%s_%s_%s_%s' % (self.tags, self.woe_id, self.only_geotagged,
                                     self.min_upload_date, self.max_upload_date)
        return string.lower()


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

    def count_photos(self):
        count = 0
        for photo in self._iterator:
            count += 1
        return count

    def get_random_link(self):
        pass
        # todo: this just takes a photo of the the first n
        photo = random.choice(self._data)
        return 'https://www.flickr.com/photos/%s/%s' % (photo['owner'], photo['id'])


def get_photo_collection(query, per_page=PER_PAGE_DEFAULT):
    params = query.params
    params['per_page'] = per_page
    iterator = flickr.walk(**params)
    collection = PhotoCollection(iterator)
    return collection


def count_photos(query):
    params = query.params
    response = flickr.photos.search(**params)
    photos = response[0]
    total = int(photos.attrib['total'])
    logger.info('counted %d photos for query %s', total, query)
    return total


def get_place_name(woe_id):
    response = flickr.places.getInfo(woe_id=woe_id)
    name = response.find('place').attrib['name']
    return name


def find_woe_ids(search_string: str):
    response = flickr.places.find(query=search_string)
    for place in response[0]:
        template = '{name}({type}): woe_id {woe_id}'
        name = place.attrib['woe_name']
        type = place.attrib['place_type']
        woe_id = place.attrib['woeid']
        print(template.format(name=name, type=type, woe_id=woe_id))




def get_points(query, per_page=PER_PAGE_DEFAULT):
    logger.info('Querying points from Flickr ...')
    photo_collection = get_photo_collection(query, per_page=per_page)
    points = photo_collection.to_points()
    logger.info('... finished.')
    return points
