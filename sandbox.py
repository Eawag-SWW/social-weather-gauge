# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plotter
from pprint import pprint
from datetime import date, datetime

from tweepy import Cursor
from pattern.web import Twitter
import pandas as pd
from PyDictionary import PyDictionary

from apis import instagram_api, flickr_api, twitter_api
from apis.flickr_api import flickr, FlickrQuery
from apis.twitter_api import PrintingListener
import config
import geo
import main
import store
import twitter_analysis
import utils


def tags_for_place(woe_id):
    response = flickr.places.tagsForPlace(woe_id=woe_id)
    print(response)


def find_place(query):
    response = flickr.places.find(query=query)
    print(response)


def count():
    year = 2012
    print flickr_api.count_photos(FlickrQuery.geotagged_flooding_tags, year=year)
    print flickr_api.count_photos(FlickrQuery.switzerland_flooding_tags, year=year)


def walking():
    query = flickr_api.FlickrQuery.switzerland_flooding_tags
    for photo in flickr_api.get_photos(query, with_geotags=True)._iterator:
        print photo.get('latitude')






        # for photo in flickr.walk(**params):
        # print photo.get('title')


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


def twitter_cursor():
    results = []
    q = 'place:%s since:2015-06-09 until:2015-06-10' % twitter_api.PLACE_ID_GERMANY
    cursor = Cursor(twitter_api.api.search, q=q, count=100)
    for tweet in cursor.items():
        results.append(tweet)
        pprint(vars(tweet))
        break
        # print len(results)


def twitter_response():
    q = 'place:%s since:2015-06-09 until:2015-06-10' % twitter_api.PLACE_ID_GERMANY
    response = twitter_api.api.search(q)
    pprint(vars(response))


def histogram():
    # np.histogram2d()
    n = 1000
    # x = np.random.normal(10,2,n)
    # y = np.random.normal(15,5,n)
    x = [1, 1, 1, 2, 2, 2]
    y = [1, 1, 1, 2, 2, 3]

    H, xedges, yedges = np.histogram2d(x, y, bins=3)
    print H
    print xedges
    print yedges

    # plotter.imshow(H, interpolation='nearest', origin='low',
    # extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])

    X, Y = np.meshgrid(xedges, yedges)
    plotter.pcolormesh(X, Y, H)
    # figure.set_aspect('equal')

    plotter.savefig('testplot.jpg')


def dictionary():
    dictionary = PyDictionary()
    print dictionary.translate('flood', 'de')
    print dictionary.translate('flooding', 'de')
    print dictionary.synonym('flood')
    print dictionary.synonym('flooding')
    print dictionary.synonym('deluge')

    flood = PyDictionary('flood', 'flooding', 'deluge')
    print flood.printSynonyms()


def totals():
    queries = [config.FLOODING_GERMAN_TAGS_QUERY, config.FLOODING_FRENCH_TAGS_QUERY, config.FLOODING_ENGLISH_TAGS_QUERY]
    utils.print_totals(queries)


def print_tweet_counts_last_days():
    place_id = twitter_api.PLACE_ID_ZURICH
    begin = date(2015, 6, 1)
    end = date(2015, 6, 12)

    main.print_tweet_counts(place_id, begin, end, use_cache=False)


def place_infos():
    twitter_api.print_place_info(twitter_api.PLACE_ID_GERMANY)
    twitter_api.print_place_info(twitter_api.PLACE_ID_ZURICH)


def twitter_streaming_response():
    twitter_api.start_streaming(PrintingListener(), bounding_box=geo.ZURICH_EXTENDED)


def print_tweets():
    for tweet in store.get_tweets(store_type=store.STREAMING_TWEETS)[:5]:
        print(vars(tweet).keys())


def analyse_tweets():
    begin = datetime(2015, 6, 8, 0)
    end = datetime(2015, 6, 9, 0)
    twitter_analysis.print_tweets(store.SEARCH_TWEETS, begin, end)


def berlin_tweets():
    begin = datetime(2015, 7, 1)
    end = datetime(2015, 7, 14)
    twitter_analysis.print_search_tweet_counts(twitter_api.PLACE_ID_BERLIN_CITY, begin, end )

if __name__ == '__main__':
    berlin_tweets()
