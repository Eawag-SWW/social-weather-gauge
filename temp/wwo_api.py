from datetime import date

import requests

from apis import twitter_api
from main import secrets

__author__ = 'dominic'


KEY = secrets.WORLDWEATHERONLINE_API_KEY

def get_precips(place, day, nMeasurements):

    if nMeasurements not in [1, 3, 6, 12, 24]:
        raise Exception()

    q = '%f,%f' % (place.centroid_lat, place.centroid_lon)
    params = {
        'key': KEY,
        'format': 'json',
        'date': day.strftime('%Y-%m-%d'),     #yyyy-MM-dd
        'q': q,
        'tp': nMeasurements
         # 'enddate':
    }

    url = 'https://api.worldweatheronline.com/free/v2/past-weather.ashx'
    response = requests.get(url, params=params)
    weather = response.json()['data']['weather']

    if len(weather) > 1:
        raise Exception('more than one weather element')

    precips = []
    for data_point in weather[0]['hourly']:
        precip = float(data_point['precipMM'])
        precips.append(precip)
    return precips



if __name__ == '__main__':
    place = twitter_api.construct_place(twitter_api.PLACE_ID_LONDON_CITY)
    day = date(2015, 9, 1)
    get_precipitation(place=place, day=day)