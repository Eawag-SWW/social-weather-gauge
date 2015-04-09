# -*- coding: utf-8 -*-


from tweepy import Cursor
import numpy as np
from matplotlib import pyplot as plotter
from pattern.web import Twitter
import pandas as pd

from apis.flickr_api import flickr
from apis import instagram_api, flickr_api, twitter_api


pd.options.display.mpl_style = 'default'


def tags_for_place(woe_id):
    response = flickr.places.tagsForPlace(woe_id=woe_id)
    print(response)


def find_place(query):
    response = flickr.places.find(query=query)
    print(response)


def sandbox():
    params = flickr_api.get_params('switzerland')
    photos = flickr_api.get_photos(params)
    print photos.get_size()


def walking():
    params = flickr_api.get_params('switzerland')
    params['min_upload_date'] = '2015-01-01'
    # params['per_page'] = 1000
    photos = flickr_api.get_photos(params)
    print photos.total


def array():
    x = [1, 2, 3]
    y = [1, 4, 9]
    data = np.array([x, y])
    np.savetxt('test.csv', data, fmt='%g')
    loaded = np.loadtxt('test.csv')
    x = loaded[0]
    y = loaded[1]
    plotter.plot(x, y)
    plotter.show()
    print data


def facebook():
    api = Twitter()

    results = api.search('Hochwasser')
    print len(results)
    for result in results:
        print dir(result)
        break


def pandas():
    index = range(2004, 2015)
    data = np.random.randn(len(index))
    series = pd.Series(data, index=index)
    series.plot()
    plotter.show()


def pandas_plotting():
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    ts.plot()
    plotter.show()


def instagram():
    popular_media = instagram_api.api.media_popular(count=20)
    for media in popular_media:
        print media.images['standard_resolution'].url


def twitter_geo():
    result = twitter_api.api.geo_search(query='Germany')
    print len(result)
    for place in result:
        print place.id
        print place.name
        print place.full_name
        print place.place_type

def twitter_by_place():
    q = 'place:%s since:2015-04-01' % twitter_api.PLACE_ID_ZURICH
    cursor = Cursor(twitter_api.api.search, q=q)
    for tweet in cursor.items(5):
        print tweet.text
        print ' '
    print count


if __name__ == '__main__':
    twitter_by_place()

