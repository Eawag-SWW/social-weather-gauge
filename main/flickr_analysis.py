# -*- coding: utf-8 -*-

import logging
import os
from os import path
import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn

from apis import flickr_api
from apis.flickr_api import FlickrQuery
from main import store
from main.local_config import ROOT_DIR
from main.config import DOCS_IMG_DIR, MISC_PLOTS_DIR, PLOTS_DIR

FLICKR_PLOT_DIR = path.join(PLOTS_DIR, 'flickr')
if not path.exists(FLICKR_PLOT_DIR):
    os.makedirs(FLICKR_PLOT_DIR)


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


def plot_photos_per_year(woe_id=None, save2docs=False):
    """
    Saves the plot in the flickr plots directory.
    Attention: Results are incorrect if there are to many photo
    uploads per year for this place/country.

    :param woe_id: id of the place/country the data is based on
    :param save2docs: this flags saves the plot directly in the documentation

    """

    series = pd.Series()

    for year in range(PLOT_START_YEAR, PLOT_END_YEAR):
        query = FlickrQuery(woe_id=woe_id, year=year)
        n_photos = store.read(store.N_PHOTOS, query)
        series.set_value(year, n_photos)

    series.plot(kind='bar', use_index=True)

    place_name = flickr_api.get_place_name(woe_id=woe_id)
    plt.title(place_name)
    plt.ylabel('Number of flickr photo uploads')
    plt.xlabel('Year')

    file_name = '%s.png' % time.time()
    target_path = path.join(FLICKR_PLOT_DIR, file_name)
    plt.savefig(target_path)

    if save2docs:
        place_name_formatted = place_name.lower().replace(' ', '-')
        file_name = 'flickr_%s' % place_name_formatted
        target_path = path.join(DOCS_IMG_DIR, file_name)
        plt.savefig(target_path)


def plot_normalized_tag_usage_per_year(tags, woe_id, save2docs=False):

    series = pd.Series()

    for year in range(PLOT_START_YEAR, PLOT_END_YEAR):
        tag_query = FlickrQuery(tags=tags, woe_id=woe_id, year=year)
        n_photos_tags = store.read(store.N_PHOTOS, tag_query)
        total_query = FlickrQuery(woe_id=woe_id, year=year)
        n_photos_total = store.read(store.N_PHOTOS, total_query)
        series.set_value(year, n_photos_tags / n_photos_total)

    series.plot(kind='bar', use_index=True)

    place_name = flickr_api.get_place_name(woe_id=woe_id)
    title = '{}: {}'.format(place_name, tags)
    plt.title(title)
    plt.ylabel('Normalized tag usage')
    plt.xlabel('Year')

    file_name = '%s.png' % time.time()
    target_path = path.join(FLICKR_PLOT_DIR, file_name)
    plt.savefig(target_path)

    if save2docs:
        place_name_formatted = place_name.lower().replace(' ', '-')
        file_name = 'flickr_flooding_%s' % place_name_formatted
        target_path = path.join(DOCS_IMG_DIR, file_name)
        plt.savefig(target_path)


def compute_geotag_usage():
    """
    Prints the relative amount of geotted photos for different tags. 
    """
    year = 2014

    for tag in TEST_TAGS:

        tags = [tag]
        query = FlickrQuery(tags=tags, year=year)
        geotagged_query = FlickrQuery(tags=tags, year=year, only_geotagged=True)

        total = flickr_api.count_photos(query)
        geotagged = flickr_api.count_photos(geotagged_query)
        print('%s: %.2f (%d total) (%d)' % (tags, geotagged / total, total, geotagged))


def plot_wsl_flooding_data(save2docs=False):

    data_path = path.join(ROOT_DIR, 'data', 'switzerland_flooding_money.csv')
    series = pd.Series.from_csv(data_path, ';')
    series.index = series.index.map(lambda t: t.strftime('%Y'))
    series[str(PLOT_START_YEAR):str(PLOT_END_YEAR)].plot(kind='bar')

    plt.title('WSL Flooding Data')
    if save2docs:
        plot_path = path.join(DOCS_IMG_DIR, 'wsl')
    else:
        plot_path = path.join(MISC_PLOTS_DIR, 'wsl-%.0f.png' % time.time())
    plt.savefig(plot_path)

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

    plot_wsl_flooding_data(save2docs=False)
