# -*- coding: utf-8 -*-


import os

import matplotlib.pyplot as plotter
import numpy

import api
from api import Query

tags_list = [['hochwasser'], ['überschwemmung'], ['überflutung'], ['flut']]
RADIUS = 30


def print_random_links(query):
    params = api.get_params(query)
    photos = api.get_photos(params)

    for _ in range(5):
        url = photos.get_random_link()
        print(url)


def summary(query):
    print 'total:', api.count_photos(query)
    plot(query)


def plot(query, use_cache=False):

    path = 'data/%s.csv' % query.name
    start_year = 2004
    end_year = 2015

    if use_cache:
        data = numpy.loadtxt(path)

    else:
        x = []
        y = []
        for year in range(start_year, end_year):
            n_photos = api.count_photos(query, year)
            x.append(year)
            y.append(n_photos)
            print year, n_photos
        data = numpy.array([x, y])
        numpy.savetxt(path, data, fmt='%g', delimiter=',')

    plotter.plot(data[0], data[1])
    plotter.show()


def plot_normalized():
    path = 'data/%s.csv' % 'flooding_normalized'
    start_year = 2004
    end_year = 2015

    if os.path.isfile(path):
        data = numpy.loadtxt(path)

    else:
        x = []
        y = []
        for year in range(start_year, end_year):
            n_flooding = api.count_photos(Query.switzerland_flooding, year)
            n_switzerland = api.count_photos(Query.switzerland, year)
            quotient = n_flooding / float(n_switzerland)
            x.append(year)
            y.append(quotient)
            print year, n_flooding, n_switzerland, quotient
        data = numpy.array([x, y])
        numpy.savetxt(path, data, fmt='%g', delimiter=',')

    plotter.plot(data[0], data[1])
    plotter.show()


if __name__ == '__main__': 
    plot_normalized()