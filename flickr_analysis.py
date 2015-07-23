# -*- coding: utf-8 -*-
import logging
import time

import matplotlib.pyplot as plt
import pandas as pd

from apis import flickr_api
from apis.flickr_api import FlickrQuery, FlickrQueryType
import store
from store import StoreType
import config
from geo import Map


RADIUS = 30
logger = logging.getLogger('main')


def plot(queries, normalizer_query=None, use_cache=False):
    if not use_cache:
        for query in queries:
            store.save(query ... )
        store.save(normalizer_query, ...)

    for query in queries:
        data = store.read(query)
        if normalizer_query:
            normalizer = store.read(normalizer_query, ...)
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
    queries = [FlickrQuery(language=language, query_type=FlickrQueryType.TAGS, only_geotagged=True) for language in languages]
    save_map(queries, use_cache=True, n_bins=40, formats=['png', 'svg'])


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())





