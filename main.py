# -*- coding: utf-8 -*-


import random

import matplotlib.pyplot as plotter
import api
import constants

tags_list = [['hochwasser'], ['überschwemmung'], ['überflutung'], ['flut']]
RADIUS = 30


class DataSet:
    pass





        params['switzerland'] = switzerland_params
    return get_params


def print_random_links(response):
    photos = response['photos']['photo']
    for _ in range(5):
        photo = random.choice(photos)
        url = 'https://www.flickr.com/photos/%s/%s' % (photo['owner'], photo['id'])
        print(url)


def get_data_set():
    params = get_params('switzerland')
    photos = api.get_photos(params)
    counter = 0
    for photo in photos:
        print photo['title']
        counter += 1
        if counter > 20: break
    return DataSet()
    # for photo in photos:
    #     date = photo.get_date()


def plot_switzerland():
    data_set = get_data_set()

    # plotter.plot_date(data)
    # plotter.show()

if __name__ == '__main__':
    plot_switzerland()









def bak():
    params = get_params('switzerland')
    print('params: %s \n total: %s \n' % (params, total))