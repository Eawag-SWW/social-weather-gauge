# -*- coding: utf-8 -*-
import logging

import matplotlib.pyplot as plt
import pandas as pd

from apis import flickr_api
from apis.flickr_api import FlickrQuery, QueryType
import cache
from cache import CacheType
from config import START_YEAR, END_YEAR
import config
from geo import Map


tags_list = [['hochwasser'], ['überschwemmung'], ['überflutung'], ['flut']]
RADIUS = 30
logger = logging.getLogger('main')
# matplotlib.style.use('ggplot')


def print_random_links(query):
    params = flickr_api._get_params(query)
    photos = flickr_api._get_photos_from_params(params)

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
    if not use_cache:
        for query in queries:
            cache.save(query)
        cache.save(flickr_api.FlickrQuery.switzerland)

    normalizer = cache.read(flickr_api.FlickrQuery.switzerland)

    for query in queries:
        data = cache.read(query)
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


def draw_map(queries, use_cache=False, n_bins=60, color_maps=['Blues', config.D_REDS], mix_points=False):
    if not use_cache:
        for query in queries:
            cache.save(query, CacheType.POINTS)

    box = config.EUROPE_RESTRICTED
    map = Map(bounding_box=box)

    if mix_points:
        all_points = []
        for query in queries:
            points = cache.read(query, CacheType.POINTS)
            all_points.append(points)
        map.draw_densities(all_points, n_bins)

    else:
        i = 0
        for query in queries:
            points = cache.read(query, CacheType.POINTS)
            color_map = color_maps[i]
            i += 1
            map.draw_densities(points, n_bins=n_bins, color_map=color_map)

    map.show()


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    queries = [config.FLOODING_GERMAN_TAGS_QUERY, config.FLOODING_FRENCH_TAGS_QUERY]
    draw_map(queries, use_cache=True, n_bins=50)

