from datetime import datetime
from dateutil.rrule import DAILY, rrule

from apis import twitter_api
from apis.twitter_api import PLACE_ID_LONDON_CITY
from main import secrets

__author__ = 'dominic'

from forecastio import load_forecast

KEY = secrets.FORECAST_API_KEY

def print_forecast(twitter_place_id, begin, end):
    place = twitter_api.Place(twitter_place_id)
    for day in rrule(DAILY, dtstart=begin, until=end):
        forecast = load_forecast(KEY, lat=place.centroid_lat, lng=place.centroid_lon, time=day)
        datablock = forecast.daily()
        for data in datablock.data:
            print data.time
            print data.summary
            if hasattr(data, 'precipAccumulation'):
                print data.precipAccumulation

if __name__ == '__main__':
    begin = datetime(2015, 8, 25)
    end = datetime(2015, 9, 2)
    print_forecast(PLACE_ID_LONDON_CITY, begin, end)
