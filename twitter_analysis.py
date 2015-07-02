from datetime import datetime, timedelta
import logging

import pandas as pd
import matplotlib.pyplot as plt
import seaborn

from apis.twitter_api import TwitterSearchQuery, TwitterStreamingQuery
import geo
import store

logger = logging.getLogger('main')


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

    for d in [begin_date + timedelta(days=i) for i in range(n_days)]:

        query = TwitterSearchQuery(place_id=place_id, date=d)

        if not use_cache:
            store.save(query, store_type=store.SEARCH_TWEETS)

        tweets = store.read(query, store_type=store.SEARCH_TWEETS)

        date_string = d.strftime('%d/%m')
        print '%s: %d' % (date_string, len(tweets))


def store_twitter_stream():
    query = TwitterStreamingQuery(bounding_box=geo.ZURICH_EXTENDED)
    store.save(query, store_type=store.STREAMING_TWEETS)


def plot_streaming_tweets():
    begin = datetime(2015, 7, 1, 14)
    end = datetime(2015, 7, 1, 18)
    dataframe = store.get_tweets_dataframe(store.STREAMING_TWEETS, begin, end)
    dataframe['count'] = 1
    hourly = dataframe.resample('H', how='sum')
    hourly['count'].plot()
    plt.ylim((0,100))
    plt.show()



if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    store_twitter_stream()