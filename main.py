# -*- coding: utf-8 -*-
import logging

import os
import pickle
from enum import Enum

import matplotlib.pyplot as plotter
from mpl_toolkits.basemap import Basemap
import pandas as pd
import matplotlib
import time

from apis import flickr_api
from apis.flickr_api import Query
import cache
from config import START_YEAR, END_YEAR

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


def plot_statistics():
    series = pd.Series.from_csv('data/switzerland_flooding_money.csv', ';')
    series.plot()
    plotter.show()


def draw_map(query, use_cache=False):

    if not use_cache:
        cache.save_cache(query, cache.CacheType.points)

    north_east_lat = 81.008797
    north_east_lon = 39.869301
    south_west_lat = 27.636311
    south_west_lon = -31.266001

    map = Basemap(resolution='i', urcrnrlat=north_east_lat, urcrnrlon=north_east_lon, llcrnrlat=south_west_lat, llcrnrlon=south_west_lon)
    map.drawcountries()
    map.drawcoastlines(linewidth=0.5)
    map.drawrivers()

    logger.debug('reading cache ...')
    points = cache.read_cache(query, cache.CacheType.points)
    logger.debug('finished')

    for point in points:
        try:
            x,y = map(point.lon, point.lat)
            map.plot(x, y, 'ro', 15)
        except:
            logging.warning('problem with point:')

    plotter.show()


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    draw_map(Query.geotagged_flooding_tags, use_cache=True)
