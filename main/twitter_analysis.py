from datetime import datetime, date
import logging
from os import path
import os

from dateutil.rrule import DAILY, rrule
import nltk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

from apis import twitter_api
from apis.twitter_api import TwitterSearchQuery
from apis.wunderground_api import WundergroundQuery
from main import store, utils
from main.config import PLOTS_DIR, DATA_DIR
from main.geo import Place
from main.local_config import ROOT_DIR
from main.store import SEARCH_TWEETS

TWITTER_PLOTS_DIR = path.join(PLOTS_DIR, 'twitter')
os.makedirs(TWITTER_PLOTS_DIR, exist_ok=True)

logger = logging.getLogger('main')


class Language(object):
    def __init__(self, code: str):
        self.code = code


class Topic(object):
    def __init__(self, terms):
        self.terms = terms


class TopicSummary(object):
    pass


class Terms(object):
    def __init__(self):
        self.data = dict()

    def set(self, language, words):
        self.data[language.code] = words

    def get(self, language):
        return self.data[language.code]


ENGLISH = Language('en')
RAIN_TERMS = Terms()
RAIN_TERMS.set(ENGLISH, ['rain'])
RAIN = Topic(RAIN_TERMS)


def plot_swiss_rain_data(filename: str):

    filepath = path.join(DATA_DIR, filename)

    df = pd.read_csv(filepath, skiprows=7, header=1, delim_whitespace=True)
    df.rename(columns={'237': 'rain'}, inplace=True)

    date_labels = ['JAHR', 'MO', 'TG']
    transform = lambda s: date(*s)
    df['date'] = df[date_labels].apply(transform, axis=1)
    df.index = df.date
    to_drop = ['date', 'STA', 'MM', 'HH', '236'] + date_labels
    df.drop(to_drop, axis=1, inplace=True)
    # df = df.resample('D', how='sum')

    df = df[1:]

    df.plot()
    plt.show()


def contains_topic(tweet, topic):
    # todo: make language dynamic
    language = ENGLISH

    stemmer = nltk.PorterStemmer()

    raw = tweet.text.lower()
    tokens = nltk.word_tokenize(raw)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    query = topic.terms.get(language)[0]
    stemmed_query = stemmer.stem(query)

    if stemmed_query in stemmed_tokens:
        return True
    else:
        return False


def get_topic_summary(topic: Topic, place: Place, begin: date, end: date) -> TopicSummary:

    rows = []

    for day in rrule(DAILY, dtstart=begin, until=end):
        n_tweets = 0
        n_positive = 0
        place_id = place.twitter_place_id
        query = TwitterSearchQuery(place_id, day)
        tweets = store.read(SEARCH_TWEETS, query)
        for tweet in tweets:
            n_tweets += 1
            if contains_topic(tweet, topic):
                n_positive += 1
        if n_tweets == 0:
            continue
        else:
            percent = 100 * n_positive / n_tweets
            row = (day, [n_tweets, n_positive, percent])
            rows.append(row)

    table = pd.DataFrame.from_items(rows, columns=['n_tweets', 'n_positive', 'percent'], orient='index')

    topic_summary = TopicSummary()
    topic_summary.frequency_series = table['percent']
    topic_summary.table = table
    return topic_summary


def save_place_overview(place: Place, begin: date, end: date):

    if not hasattr(place, 'wunderground_id'):
        raise Exception('Place has no wunderground id.')

    wunderground_query = WundergroundQuery(place.wunderground_id, begin, end)
    wunderground_rain = store.read(store.WUNDERGROUND_RAIN, wunderground_query)

    print(wunderground_rain)

    topic_summary = get_topic_summary(topic=RAIN, place=place, begin=begin, end=end)
    twitter_rain = topic_summary.frequency_series

    title = '%s\n%s-%s' % (place, begin, end)
    plt.title(title)

    plt.subplot(2, 1, 1)
    wunderground_rain.plot(label='Wunderground', legend=True)
    twitter_rain.plot(secondary_y=True, label='Twitter', legend=True)
    plt.text(topic_summary.table)

    plt.subplot(2, 1, 2)
    plt.scatter(twitter_rain, wunderground_rain)

    frame = pd.DataFrame({'twitter': twitter_rain, 'wunderground': wunderground_rain})
    print('correlation:')
    print(frame.corr())

    plot_id = '%s_%s_%s_%s' % ('rain', place, begin, end)
    utils.save_plot(plot_id=plot_id, directory=TWITTER_PLOTS_DIR)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    begin = date(2015, 12, 1)
    end = date(2015, 12, 12)
    twitter_place_id = twitter_api.PLACE_ID_ZURICH_ADMIN
    twitter_place = store.get_twitter_place(twitter_place_id)
    place = Place(twitter_place, 'LSMD')
    save_place_overview(place, begin, end)

#
# def plot_wolrdwheateronline_precipitation(place, begin, end):
#     series = pd.Series()
#     for day in rrule(DAILY, dtstart=begin, until=end):
#         precipitation = wwo_api.get_precipitation(place, day)
#         series.set_value(day, precipitation)
#     series.index = series.index.map(lambda t: t.strftime('%m/%d'))
#     series.plot('bar')
#     dir = join('plots', 'twitter')
#     if not os.path.exists(dir):
#         os.makedirs(dir)
#     path = join(dir, 'wwo_%s.png' % time.time())
#     plt.savefig(path)

# plot_wolrdwheateronline_precipitation(place=place, begin=begin, end=end)
# plot_topic_distribution(topic=RAIN, place_id=twitter_place_id, begin=begin, end=end)

# def plot_streaming_tweets():
# begin = datetime(2015, 7, 8, 0)
# end = datetime(2015, 7, 15, 0)
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