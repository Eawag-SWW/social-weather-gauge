# -*- coding: utf-8 -*-

import logging
from pprint import pprint
from datetime import datetime, date

import numpy as np
from matplotlib import pyplot as plt
import nltk
from tweepy import Cursor
from nltk import Text

from apis import flickr_api, twitter_api
from apis.flickr_api import flickr, FlickrQuery
from apis.twitter_api import PrintingListener
from main import twitter_analysis, flickr_analysis, store, geo
from main.twitter_analysis import RAIN

logger = logging.getLogger('main')


def tags_for_place(woe_id):
    response = flickr.places.tagsForPlace(woe_id=woe_id)
    print(response)


def find_place(query):
    response = flickr.places.find(query=query)
    print(response)


def array():
    x = [1, 2, 3]
    y = [1, 4, 9]
    data = np.array([x, y])
    np.savetxt('test.csv', data, fmt='%g')
    loaded = np.loadtxt('test.csv')
    x = loaded[0]
    y = loaded[1]
    plt.plot(x, y)
    plt.show()
    print(data)


def instagram():
    popular_media = instagram_api.api.media_popular(count=20)
    for media in popular_media:
        print(media.images['standard_resolution'].url)


def twitter_geo():
    result = twitter_api.api.geo_search(query='Germany')
    print(len(result))
    for place in result:
        print(place.id)
        print(place.name)
        print(place.full_name)
        print(place.place_type)


def twitter_cursor():
    results = []
    q = 'place:%s since:2015-06-09 until:2015-06-10' % twitter_api.PLACE_ID_GERMANY
    cursor = Cursor(twitter_api.api.search, q=q, count=100)
    for tweet in list(cursor.items()):
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
    print(H)
    print(xedges)
    print(yedges)

    # plt.imshow(H, interpolation='nearest', origin='low',
    # extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])

    X, Y = np.meshgrid(xedges, yedges)
    plt.pcolormesh(X, Y, H)
    # figure.set_aspect('equal')

    plt.savefig('testplot.jpg')


def dictionary():
    dictionary = PyDictionary()
    print(dictionary.translate('flood', 'de'))
    print(dictionary.translate('flooding', 'de'))
    print(dictionary.synonym('flood'))
    print(dictionary.synonym('flooding'))
    print(dictionary.synonym('deluge'))

    flood = PyDictionary('flood', 'flooding', 'deluge')
    print(flood.printSynonyms())


def place_infos():
    twitter_api.construct_place(twitter_api.PLACE_ID_GERMANY)
    twitter_api.construct_place(twitter_api.PLACE_ID_ZURICH)


def twitter_streaming_response():
    twitter_api.start_streaming(PrintingListener(), bounding_box=geo.ZURICH_EXTENDED)


def print_tweets():
    for tweet in store.get_tweets(store_type=store.STREAMING_TWEETS)[:5]:
        print((list(vars(tweet).keys())))


def analyse_tweets():
    begin = datetime(2015, 6, 8, 0)
    end = datetime(2015, 6, 9, 0)
    twitter_analysis.print_tweets(store.SEARCH_TWEETS, begin, end)


def print_berlin_tweet_counts():
    begin = datetime(2015, 7, 7)
    end = datetime(2015, 7, 13)
    twitter_analysis.print_search_tweet_counts(twitter_api.PLACE_ID_BERLIN_CITY, begin, end, use_cache=True)


def get_twitter_text():
    begin = datetime(2015, 7, 8)
    end = datetime(2015, 7, 9)
    tweets = store.get_search_tweets(twitter_api.PLACE_ID_LONDON_ADMIN, begin, end, use_cache=True)
    raw_text = ''
    for tweet in tweets:
        raw_text += tweet.text
    tokens = nltk.word_tokenize(raw_text)
    return Text(tokens)


def print_number_of_dublin_tweets():
    begin = datetime(2015, 7, 15)
    end = datetime(2015, 7, 22)
    twitter_analysis.print_search_tweet_counts(twitter_api.PLACE_ID_DUBLIN, begin, end, use_cache=False)


def number_of_london_tweets():
    begin = datetime(2015, 7, 7)
    end = datetime(2015, 7, 15)
    twitter_analysis.print_search_tweet_counts(twitter_api.PLACE_ID_LONDON_ADMIN, begin, end, use_cache=False)


def flickr_data():
    # woe_id = flickr_api.WOE_ID_SWITZERLAND

    tags = ['flooding']

    query = FlickrQuery(tags=tags)
    geotagged_query = FlickrQuery(tags=tags, only_geotagged=True)

    total = flickr_api.count_photos(query)
    geotagged = flickr_api.count_photos(geotagged_query)
    print('%s: %.2f' % (tags, geotagged / total))


def flickr_plot():
    tags = flickr_analysis.FLOODING_TAGS['de']
    flickr_analysis.plot_normalized_tag_usage_per_year(tags, flickr_api.WOE_ID_SWITZERLAND, True)


def places():
    query = 'Deutschland'
    flickr_api.get_places(query)


def rain_tweets(place):
    topic = RAIN
    begin = datetime(2015, 8, 25)
    end = datetime(2015, 9, 1)
    twitter_analysis.plot_topic_distribution(topic, place, begin, end)

#
# def compare_rain_measurements():
#
#     begin = date(2015, 8, 25)
#     end = date(2015, 9, 2)
#     place = geo.LONDON_CITY
#     wunderground_rain = wunderground_api.get_rain()
#
#     plt.subplot(2, 1, 1)
#     twitter_rain = twitter_analysis.get_twitter_rain(place, begin, end)
#     wunderground_rain.plot(label='Wunderground')
#     twitter_rain.plot(secondary_y=True, label='Twitter', legend=True)
#
#     plt.subplot(2, 1, 2)
#     plt.scatter(twitter_rain, wunderground_rain)
#
#     frame = pd.DataFrame({'twitter': twitter_rain, 'wunderground': wunderground_rain})
#     print('correlation:')
#     print(frame.corr())
#
#     plt.show()
#
#     #
#     # plt.show()
#
#     # for day in rrule(DAILY, dtstart=begin, until=end):
#     #     print day
#     #     print 'wunderground: %f' % wunderground_precip[day]
#     #     for nMeasurements in (1, 3, 6, 12, 24):
#     #         wwo_precips = wwo_api.get_precips(place, day, nMeasurements)
#     #         print '%d: %s' % (nMeasurements, wwo_precips)


def coordinate():
    response = twitter_api.api.geo_id(twitter_api.PLACE_ID_LONDON_CITY)
    for point in response.bounding_box.coordinates[0]:
        print(point)


def twitter_place_id():
    twitter_place = store.get_twitter_place(twitter_api.PLACE_ID_LONDON_CITY)
    pprint(vars(twitter_place))


def tweets():
    place_id = twitter_api.PLACE_ID_SEATTLE
    twitter_place = store.get_twitter_place(place_id)
    place = geo.Place(twitter_place, 'KBFI')
    begin = date(2015, 10, 20)
    end = date(2015, 10, 27)
    twitter_analysis.save_place_overview(place, begin, end)


def plot():
    plt.subplot(211)
    plt.plot([2,4,7,33,4])
    plt.subplot(212)
    plt.text(0, 1, 'blablajas;kdjfjkljsdfaskdfjksjafsdkjfk;sadjksadjkfsadj')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    plot()
