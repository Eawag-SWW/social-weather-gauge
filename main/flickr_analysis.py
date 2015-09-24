# -*- coding: utf-8 -*-

import logging
import time
from os.path import join

import matplotlib.pyplot as plt
import pandas as pd

from apis import flickr_api
from apis.flickr_api import FlickrQuery
from main import store

# todo: correct path
... DOCS_IMG_PATH = path.join('docs', 'source', 'img')

RADIUS = 30
TEST_TAGS = ('flooding', 'Bob Dylan', 'house', 'music', 'grass', 'baby')
PLOT_START_YEAR = 2004
PLOT_END_YEAR = 2014
FLOODING_TAGS = dict()
FLOODING_TAGS['de'] = 'hochwasser, überschwemmung, überflutung, flut'
FLOODING_TAGS['fr'] = 'crue, inondation'
FLOODING_TAGS['en'] = 'flood, high-water'
FLOODING_TAGS['it'] = 'inondazione, alluvione'

logger = logging.getLogger('main')


def compute_geotag_usage():

    year = 2014

    for tag in TEST_TAGS:

        tags = [tag]

        query = FlickrQuery(tags=tags, year=year)
        geotagged_query = FlickrQuery(tags=tags, year=year, only_geotagged=True)

        total = flickr_api.count_photos(query)
        geotagged = flickr_api.count_photos(geotagged_query)
        print('%s: %.2f (%d total) (%d)' % (tags, geotagged / total, total, geotagged))


def plot_photos_per_year(woe_id=None, use_cache=False, save2docs=False):

    if not use_cache:
        for year in range(PLOT_START_YEAR, PLOT_END_YEAR):
            query = flickr_api.FlickrQuery(woe_id=woe_id, year=year)
            store.save(store.N_PHOTOS, query)

    series = pd.Series()
    for year in range(PLOT_START_YEAR, PLOT_END_YEAR):
        query = flickr_api.FlickrQuery(woe_id=woe_id, year=year)
        n_photos = store.read(store.N_PHOTOS, query)
        series.set_value(year, n_photos)

    series.plot(kind='bar', use_index=True)

    place_name = flickr_api.retrieve_place_name(woe_id=woe_id)
    plt.title(place_name)
    plt.ylabel('number of flickr photo uploads')
    plt.xlabel('year')

    path = join('plots', 'flickr', '%s.png' % time.time())
    plt.savefig(path)

    if save2docs:
        place_name_formatted = place_name.lower().replace(' ', '-')
        file_name = 'flickr_%s' % place_name_formatted
        path = join(DOCS_IMG_PATH, file_name)
        plt.savefig(path)


def plot_normalized_tag_usage(tags=None, woe_id=None, save2docs=False):

    series = pd.Series()

    for year in range(PLOT_START_YEAR, PLOT_END_YEAR):
        tag_query = FlickrQuery(tags=tags, woe_id=woe_id, year=year)
        n_photos_tags = store.read(store.N_PHOTOS, tag_query)
        total_query = FlickrQuery(woe_id=woe_id, year=year)
        n_photos_total = store.read(store.N_PHOTOS, total_query)
        series.set_value(year, n_photos_tags / n_photos_total)

    series.plot(kind='bar', use_index=True)

    place_name = flickr_api.retrieve_place_name(woe_id=woe_id)
    title = '{}: {}'.format(place_name, tags).decode('utf-8')
    plt.title(title)
    plt.ylabel('normalized tag usage')
    plt.xlabel('year')

    path = join('plots', 'flickr', '%s.png' % time.time())
    plt.savefig(path)

    if save2docs:
        place_name_formatted = place_name.lower().replace(' ', '-')
        file_name = 'flickr_flooding_%s' % place_name_formatted
        path = join(DOCS_IMG_PATH, file_name)
        plt.savefig(path)


def plot_wsl_flooding_data():
    series = pd.Series.from_csv('data/switzerland_flooding_money.csv', ';')
    series.index = series.index.map(lambda t: t.strftime('%Y'))
    series[str(PLOT_START_YEAR):str(PLOT_END_YEAR)].plot(kind='bar')

    plt.title('WSL flooding data')

    path = join(DOCS_IMG_PATH, 'wsl')
    plt.savefig(path)

# TODO adapt method save_map to new store refactoring

#
# def save_map(queries, use_cache=False, n_bins=60, color_maps=config.COLOR_MAPS, mix_points=False, formats=['png']):
#     if not use_cache:
#         for query in queries:
#             store.save(query, StoreType.POINTS)
#
#     box = config.EUROPE_RESTRICTED
#     map = Map(bounding_box=box)
#
#     if mix_points:
#         all_points = []
#         for query in queries:
#             points = store.read(query, StoreType.POINTS)
#             all_points.append(points)
#         map.draw_densities(all_points, n_bins)
#
#     else:
#         i = 0
#         for query in queries:
#             points = store.read(query, StoreType.POINTS)
#             color_map = color_maps[i]
#             i += 1
#             map.draw_densities(points, n_bins=n_bins, color_map=color_map)
#
#     for format in formats:
#         path = 'plots/map%s.%s' % (time.t
# ime(), format)
#         map.save(path, format=format)


# def save_europa_map():
#     languages = ['de', 'fr', 'it']
#     queries = [FlickrQuery(language=language, query_type=FlickrQueryType. \
#       TAGS, only_geotagged=True) for language in languages]
#     save_map(queries, use_cache=True, n_bins=40, formats=['png', 'svg'])


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    plot_wsl_flooding_data()





