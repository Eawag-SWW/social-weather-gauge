# -*- coding: utf-8 -*-

from enum import Enum
import random

import flickrapi

import secrets


FORMAT = 'parsed-json'
API_KEY = secrets.API_KEY
API_SECRET = secrets.API_SECRET

WOE_ID_SWITZERLAND = 23424957
PLACE_ID_SWITZERLAND = 'HfSZnNxTUb7.Mo5Vpg'

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format=FORMAT)

class Query(Enum):
    switzerland = 1
    switzerland_flooding_text = 2
    switzerland_flooding_tags = 3

    def data_path(self):
        return 'data/%s.csv' % self.name


class Photo:
    def __init__(self, data):
        self._data = data

    def get_date(self):
        pass

class Photos:

    def __iter__(self):
        return self

    def next(self):
        if self._current > self._limit:
            raise StopIteration
        else:
            self._current += 1
            return self._data[self._current - 1]

    def get_random_link(self):
        # todo: this just takes a photo of the the first n
        photo = random.choice(self._data)
        return 'https://www.flickr.com/photos/%s/%s' % (photo['owner'], photo['id'])

def get_params(query):
    params = dict()
    if query == Query.switzerland:
        switzerland_params = dict()
        switzerland_params['woe_id'] = WOE_ID_SWITZERLAND
        return switzerland_params
    elif query == Query.switzerland_flooding_text:
        params['woe_id'] = WOE_ID_SWITZERLAND
        params['text'] = 'hochwasser'
    elif query == Query.switzerland_flooding_tags:
        params['woe_id'] = WOE_ID_SWITZERLAND
        params['tags'] = 'hochwasser, überschwemmung, überflutung, flut'
    else:
        raise Exception('invalid params name')
        # thun_params = dict()
        # thun_params['tags'] = tags
        # thun_params['lat'] = 47.566667 # 46.76
        # thun_params['lon'] =  7.6 # 7.624
        # thun_params['radius'] = RADIUS
        # params_list.append(thun_params)
    return params

def get_photos(params):
    response = flickr.photos.search(**params)
    photos = Photos()
    photos._data = response['photos']['photo']
    photos.total = int(response['photos']['total'])
    return photos

def count_photos(query, year=None):
    params = get_params(query)
    if year:
        params['min_upload_date'] = '%s-01-01' % year
        params['max_upload_date'] = '%s-12-31' % year
    photos = get_photos(params)
    return photos.total
