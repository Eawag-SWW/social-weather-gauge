# -*- coding: utf-8 -*-
from __future__ import division
import logging
import time

import matplotlib.pyplot as plt
from os.path import join
import pandas as pd

from apis import flickr_api
from apis.flickr_api import FlickrQuery
import store
from store import StoreType
import config
from geo import Map


RADIUS = 30
TEST_TAGS = ('flooding', 'Bob Dylan', 'house', 'music', 'grass', 'baby')
PLOT_START_YEAR = 2005
PLOT_END_YEAR = 2014
logger = logging.getLogger('main')


def compute_geotag_usage():

    year = 2014

    for tag in TEST_TAGS:

        tags = [tag]

        query = FlickrQuery(tags=tags, year=year )
        geotagged_query = FlickrQuery(tags=tags, year=year, only_geotagged=True)

        total = flickr_api.count_photos(query)
        geotagged = flickr_api.count_photos(geotagged_query)
        print '%s: %.2f (%d total) (%d)' % (tags, geotagged / total, total, geotagged)


def plot_photos_per_year(woe_id=None, use_cache=False):

    if not use_cache:
        for year in range(PLOT_START_YEAR, PLOT_END_YEAR):
            query = flickr_api.FlickrQuery(woe_id=woe_id, year=year)
            store.save(query, store.N_PHOTOS)

    series = pd.Series()
    for year in range(PLOT_START_YEAR, PLOT_END_YEAR):
        query = flickr_api.FlickrQuery(woe_id=woe_id, year=year)
        n_photos = store.read(query, store.N_PHOTOS)
        series.set_value(year, n_photos)

    series.plot(kind='bar', use_index=True)

    plt.title('Tocotronic')
    plt.ylabel('Number of Flickr Photo Uploads')
    plt.xlabel('Year')
    # plt.legend()
    path = join('plots', 'flickr', '%s.png' % time.time())
    plt.savefig(path)


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


# def save_europa_map():
#     languages = ['de', 'fr', 'it']
#     queries = [FlickrQuery(language=language, query_type=FlickrQueryType.TAGS, only_geotagged=True) for language in languages]
#     save_map(queries, use_cache=True, n_bins=40, formats=['png', 'svg'])


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    compute_geotag_usage()





