# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import logging
import time

import matplotlib.pyplot as plt
import pandas as pd

from apis import flickr_api, twitter_api
from apis.flickr_api import FlickrQuery, QueryType
from apis.twitter_api import TwitterSearchQuery, TwitterStreamingQuery
import geo
import store
from store import StoreType
from config import START_YEAR, END_YEAR
import config
from geo import Map


RADIUS = 30
logger = logging.getLogger('main')


def print_random_links(query):
    params = flickr_api._get_params(query)
    photos = flickr_api._get_photos_from_params(params)

    for _ in range(5):
        url = photos.get_random_link()
        print(url)


def plot(queries, use_cache=False, normalize=False):
    if not use_cache:
        for query in queries:
            store.save(query)
        store.save(flickr_api.FlickrQuery.switzerland)

    normalizer = store.read(flickr_api.FlickrQuery.switzerland)

    for query in queries:
        data = store.read(query)
        if normalize:
            data = data.divide(normalizer)
        plt.plot(data, label=query.name)

    plt.title('Tocotronic')
    plt.ylabel('Number of Flickr Photo Uploads')
    plt.xlabel('Year')
    plt.legend()
    plt.show()


def plot_statistics():
    series = pd.Series.from_csv('data/switzerland_flooding_money.csv', ';')
    series.plot()
    plt.show()


def save_map(queries, use_cache=False, n_bins=60, color_maps=config.COLOR_MAPS, mix_points=False, formats=['png']):
    if not use_cache:
        for query in queries:
            store.save(query, StoreType.POINTS)

    box = config.EUROPE_RESTRICTED
    map = Map(bounding_box=box)

    if mix_points:
        all_points = []
        for query in queries:
            points = store.read(query, StoreType.POINTS)
            all_points.append(points)
        map.draw_densities(all_points, n_bins)

    else:
        i = 0
        for query in queries:
            points = store.read(query, StoreType.POINTS)
            color_map = color_maps[i]
            i += 1
            map.draw_densities(points, n_bins=n_bins, color_map=color_map)

    for format in formats:
        path = 'plots/map%s.%s' % (time.time(), format)
        map.save(path, format=format)


def save_europa_map():
    languages = ['de', 'fr', 'it']
    queries = [FlickrQuery(language=language, query_type=QueryType.TAGS, only_geotagged=True) for language in languages]
    save_map(queries, use_cache=True, n_bins=40, formats=['png', 'svg'])

if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())





