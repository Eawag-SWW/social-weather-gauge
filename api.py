import flickrapi

import secrets

FORMAT = 'parsed-json'
API_KEY = secrets.API_KEY
API_SECRET = secrets.API_SECRET

api = flickrapi.FlickrAPI(API_KEY, API_SECRET, format=FORMAT)

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


def get_photos(params):

    response = api.photos.search(**params)
    photos = Photos(response['photos']['photo'])
    photos.total = int(response['photos']['total'])
    return photos

