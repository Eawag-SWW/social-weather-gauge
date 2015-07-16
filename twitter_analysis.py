from datetime import datetime, timedelta
import logging
import nltk

import pandas as pd
import matplotlib.pyplot as plt
import seaborn

from apis.twitter_api import TwitterSearchQuery, TwitterStreamingQuery
import geo
import store

logger = logging.getLogger('main')


class Topic(object):
    pass

RAIN = Topic()



def plot_rain_data():

    df = pd.read_csv('data/rain-zurich-2015.dat', skiprows=8, header=1, delim_whitespace=True)
    df.rename(columns={'267': 'rain'}, inplace=True)
    datetime_labels = ['JAHR', 'MO', 'TG', 'HH', 'MM']
    transform = lambda s: datetime(*s)
    df['datetime'] = df[datetime_labels].apply(transform, axis=1)
    df.index = df.datetime
    to_drop = ['datetime', 'STA'] + datetime_labels
    df.drop(to_drop, axis=1, inplace=True)
    df = df.resample('D', how='sum')

    april_data = df['2015-04']
    april_data.plot()
    plt.show()


def print_search_tweet_counts(place_id=None, begin_date=None, end_date=None, use_cache=False):

    n_days = int((end_date - begin_date).days)

    for day in  [begin_date + timedelta(days=i) for i in range(n_days)]:
        tweets = store.get_search_tweets(place_id, day, day + timedelta(days=1), use_cache=use_cache)
        date_string = day.strftime('%d/%m')
        print '%s: %d' % (date_string, len(tweets))


def contains_topic(tweet, topic):
    tokens = tokenize(tweet)


# def plot_streaming_tweets():
#     begin = datetime(2015, 7, 8, 0)
#     end = datetime(2015, 7, 15, 0)
#     dataframe = store.get_tweets_dataframe(store.STREAMING_TWEETS, begin, end)
#     dataframe['count'] = 1
#     hourly = dataframe.resample('D', how='sum')
#     hourly['count'].plot()
#     # plt.ylim((0,100))
#     plt.show()


# def print_tweets(store_type, begin, end):
#     dataframe = store.get_tweets_dataframe(store_type, begin, end)
#     pd.set_option('display.max_colwidth', -1)
#     print dataframe.to_string(columns=['text', 'hashtags'])
