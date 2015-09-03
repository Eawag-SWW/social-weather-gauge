from datetime import date
from pprint import pprint
import requests
from apis import twitter_api
import secrets

__author__ = 'dominic'


KEY = secrets.WORLDWEATHERONLINE_API_KEY

def retrieve_precipitation(place, day):

    q = '%f,%f' %  (place.centroid_lat, place.centroid_lon)
    params = {
        'key': KEY,
        'format': 'json',
        'date': day.strftime('%Y-%m-%d'),     #yyyy-MM-dd
        'q': q,
        'tp': 24
         # 'enddate':
    }

    url = 'https://api.worldweatheronline.com/free/v2/past-weather.ashx'
    response = requests.get(url, params=params)
    weather = response.json()['data']['weather']
    data_point = weather[0]['hourly'][0]
    return float(data_point['precipMM'])


if __name__ == '__main__':
    place = twitter_api.construct_place(twitter_api.PLACE_ID_LONDON_CITY)
    day = date(2015, 9, 1)
    retrieve_precipitation(place=place, day=day)