# -*- coding: utf-8 -*-
import logging

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np

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
            cache.save(query)
        cache.save(flickr_api.Query.switzerland)

    normalizer = cache.read(flickr_api.Query.switzerland)

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


def draw_map(query, use_cache=False, bins=10):
    if not use_cache:
        cache.save(query, cache.CacheType.points)

    # # europe
    # north_east_lat = 81.008797
    # north_east_lon = 39.869301
    # south_west_lat = 27.636311
    # south_west_lon = -31.266001

    # custom
    north_east_lat =  72 # 62
    north_east_lon = 30 #20
    south_west_lat = 35
    south_west_lon = -12

    map = Basemap(resolution='i', urcrnrlat=north_east_lat, urcrnrlon=north_east_lon,
                  llcrnrlat=south_west_lat, llcrnrlon=south_west_lon)
    map.drawcountries(linewidth=0.5)
    map.drawcoastlines(linewidth=0.5)
    # map.shadedrelief()
    # map.fillcontinents(color='peru', zorder=0)
    # map.drawrivers(color='blue')


    points = cache.read(query, cache.CacheType.points)
    logger.debug('%s points read from cache.', len(points))
    lons = np.array([p.lon for p in points], dtype=float)
    lats = np.array([p.lat for p in points], dtype=float)


    edges = ((south_west_lon, north_east_lon), (south_west_lat, north_east_lat))
    density, bin_edges_x, bin_edges_y = np.histogram2d(lons, lats, bins=bins, range=edges )

    density = np.log10(density)
    density[density < 0] = 0

    xs, ys = np.meshgrid(bin_edges_x, bin_edges_y)
    mapped_bin_lons, mapped_bin_lats = map(xs, ys)

    # for i in range(len(xs)-1):
    #     map.plot(xs[i], ys[i], 'ro', 20)
    # plt.show()


    for point in points:
        try:
            x, y = map(point.lon, point.lat)
            map.plot(x, y, 'ro', 15, alpha=0.5)
        except:
            logging.warning('problem with point:')


    # logger.debug('transposed density: %s', density.transpose())
    plt.pcolormesh(mapped_bin_lons, mapped_bin_lats, density.transpose(), cmap='Blues')

    plt.colorbar()

    plt.show()


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    draw_map(Query.geotagged_flooding_tags, use_cache=True, bins=50)
