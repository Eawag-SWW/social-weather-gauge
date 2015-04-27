# -*- coding: utf-8 -*-
import logging

from time import time

from tweepy import Cursor
import numpy as np
from matplotlib import pyplot as plotter
from pattern.web import Twitter
import pandas as pd

from apis.flickr_api import flickr, Query
from apis import instagram_api, flickr_api, twitter_api
import utils


pd.options.display.mpl_style = 'default'


def tags_for_place(woe_id):
    response = flickr.places.tagsForPlace(woe_id=woe_id)
    print(response)


def find_place(query):
    response = flickr.places.find(query=query)
    print(response)


def count():
    year = 2012
    print flickr_api.count_photos(Query.geotagged_flooding_tags, year=year)
    print flickr_api.count_photos(Query.switzerland_flooding_tags, year=year)


def walking():
    query = flickr_api.Query.switzerland_flooding_tags
    for photo in flickr_api.get_photos(query, with_geotags=True)._iterator:
        print photo.get('latitude')






    # for photo in flickr.walk(**params):
    #     print photo.get('title')


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

def histogram():
    # np.histogram2d()
    n = 1000
    # x = np.random.normal(10,2,n)
    # y = np.random.normal(15,5,n)
    x = [1, 1, 1, 2, 2, 2]
    y = [1, 1, 1, 2, 2, 3]

    H, xedges, yedges = np.histogram2d(x,y, bins=3)
    print H
    print xedges
    print yedges

    # plotter.imshow(H, interpolation='nearest', origin='low',
    #             extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])

    X, Y = np.meshgrid(xedges, yedges)
    plotter.pcolormesh(X, Y, H)
    # figure.set_aspect('equal')

    plotter.savefig('testplot.jpg')


if __name__ == '__main__':
    histogram()

