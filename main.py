# -*- coding: utf-8 -*-


import os

import matplotlib.pyplot as plotter
import numpy
import pandas as pd
import matplotlib

from apis import flickr_api
from apis.flickr_api import Query
START_YEAR = 2000
END_YEAR = 2015
tags_list = [['hochwasser'], ['überschwemmung'], ['überflutung'], ['flut']]
RADIUS = 30

matplotlib.style.use('ggplot')

def print_random_links(query):
    params = flickr_api.get_params(query)
    photos = flickr_api.get_photos(params)

    for _ in range(5):
        url = photos.get_random_link()
        print(url)


def summary(query):
    print query.name
    total = 0
    for year in range(START_YEAR, END_YEAR):
        total += flickr_api.count_photos(query, year)
    print 'total:', total
    plot(query)


def plot(queries, use_cache=False, normalize=False):

    if type(queries) != list:
        queries = [queries]

    if not use_cache:
        for query in queries:
            save_cache(query)
        save_cache(flickr_api.Query.switzerland)
    
    normalizer = read_cache(flickr_api.Query.switzerland)

    for query in queries:
        data = read_cache(query)
        if normalize:
            data = data.divide(normalizer)
        plotter.plot(data, label=query.name)

    plotter.title('Tocotronic')
    plotter.ylabel('Number of Flickr Photo Uploads')
    plotter.xlabel('Year')
    plotter.legend()
    plotter.show()


def read_cache(query):
    series = pd.Series.from_csv(query.data_path())
    # series = pd.read_csv(query.data_path(), index_col=0)
    return series


def save_cache(query):
    data = dict()
    for year in range(START_YEAR, END_YEAR):
        n_photos = flickr_api.count_photos(query, year)
        data[year] = n_photos
    series = pd.Series(data)
    path = query.data_path()
    series.to_csv(path)


def plot_statistics():
    series = pd.Series.from_csv('data/switzerland_flooding_money.csv', ';')
    series.plot()
    plotter.show()


def sandbox():
    queries = [flickr_api.Query.switzerland_flooding_tags, flickr_api.Query.switzerland_flooding_text]
    plot(queries, use_cache=True, normalize=True)
    plot(queries, use_cache=True, normalize=False)


if __name__ == '__main__':
    sandbox()
