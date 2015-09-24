from datetime import datetime, date
import logging

from dateutil.rrule import DAILY, rrule
import nltk
import pandas as pd
import matplotlib.pyplot as plt

from apis import wunderground_api
from apis.wunderground_api import WundergroundQuery
from main import store
from main.geo import Place

logger = logging.getLogger('main')


class Topic(object):
    def __init__(self, terms):
        self.terms = terms


RAIN_TERMS = dict({'en': ['rain']})
RAIN = Topic(RAIN_TERMS)


def plot_swiss_rain_data():
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


def contains_topic(tweet, topic):
    lang = 'en'
    stemmer = nltk.PorterStemmer()
    raw = tweet.text.lower()
    tokens = nltk.word_tokenize(raw)
    stemmed_tokens = list(map(stemmer.stem, tokens))
    query = stemmer.stem(topic.terms[lang][0])
    if query in stemmed_tokens:
        logger.debug(tweet)
        logger.debug(stemmed_tokens)
        logger.debug('')
        return True
    else:
        return False


def get_topic_distribution(topic: Topic, place: Place, begin: date, end: date):

    rows = []

    for day in rrule(DAILY, dtstart=begin, until=end):
        n_tweets = 0
        n_positive = 0
        place_id = place.twitter_place_id
        tweets = store.get_search_tweets(place_id, day)
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

    frame = pd.DataFrame.from_items(rows, columns=['n_tweets', 'n_positive', 'percent'], orient='index')

    logger.info(frame)

    return frame['percent']


def plot_rain_comparison(place: Place, begin: date, end: date):

    if hasattr(place, 'wunderground_place_id'):
        wunderground_place_id = place.wunderground_place_id
    else:
        raise Exception('Place has no wunderground id.')

    wunderground_query = WundergroundQuery(wunderground_place_id, begin, end)
    wunderground_rain = wunderground_api.get_rain(wunderground_query)

    twitter_rain = get_topic_distribution(topic=RAIN, place=place, begin=begin, end=end)

    title = '%s\n%s-%s' % (place, begin, end)

    plt.subplot(2, 1, 1)
    wunderground_rain.plot(label='Wunderground', legend=True)
    twitter_rain.plot(secondary_y=True, label='Twitter', legend=True)

    plt.subplot(2, 1, 2)
    plt.scatter(twitter_rain, wunderground_rain)

    frame = pd.DataFrame({'twitter': twitter_rain, 'wunderground': wunderground_rain})
    print('correlation:')
    print(frame.corr())

    plt.show()


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

if __name__ == '__main__':
    begin = date(2015, 8, 25)
    end = date(2015, 9, 2)

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

