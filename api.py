import flickrapi

import secrets
import constants

FORMAT = 'parsed-json'
API_KEY = secrets.API_KEY
API_SECRET = secrets.API_SECRET

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format=FORMAT)


class Photo:
    def __init__(self, data):
        self._data = data

    def get_date(self):
        pass


class Photos:

    def __init__(self, data):
        self._data = data
        self._limit = len(data)
        self._current = 0

    def __iter__(self):
        return self

    def next(self):
        if self._current > self._limit:
            raise StopIteration
        else:
            self._current += 1
            return self._data[self._current - 1]

    def get_size(self):
        return len(self._data)


def get_params(params_name):
    if params_name == 'switzerland':
        switzerland_params = dict()
        switzerland_params['woe_id'] = constants.WOE_ID_SWITZERLAND
        return switzerland_params
    else:
        raise Exception('invalid params name')
        # thun_params = dict()
        # thun_params['tags'] = tags
        # thun_params['lat'] = 47.566667 # 46.76
        # thun_params['lon'] =  7.6 # 7.624
        # thun_params['radius'] = RADIUS
        # params_list.append(thun_params)


def get_photos(params):
    response = flickr.photos.search(**params)
    photos = Photos(response['photos']['photo'])
    photos.total = int(response['photos']['total'])
    return photos

