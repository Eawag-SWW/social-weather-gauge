# -*- coding: utf-8 -*-


import random

import matplotlib.pyplot as plotter
import flickrapi

import api
import constants
tags_list = [['hochwasser'], ['überschwemmung'], ['überflutung'], ['flut']]

RADIUS = 30

class DataSet:
    pass



def get_params(params_name):
    if params_name == 'switzerland':
        switzerland_params = dict()
        switzerland_params['woe_id'] = constants.WOE_ID_SWITZERLAND
        return switzerland_params
    else:
        raise Exception('invalid params name')
        # thun_params = dict()
        # thun_params['tags'] = tags
        # thun_params['lat'] = 47.566667 # 46.76
        # thun_params['lon'] =  7.6 # 7.624
        # thun_params['radius'] = RADIUS
        # params_list.append(thun_params)


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