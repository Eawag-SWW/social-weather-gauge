from datetime import date
from unittest import TestCase
import os

import pandas.util.testing as pdt

from apis import wunderground_api, flickr_api
from apis.flickr_api import FlickrQuery
from main import store


class WundergroundTestCase(TestCase):

    def test_london_data_storage(self):

        begin = date(2015, 9, 10)
        end = date(2015, 9, 20)
        place_id='EGLL'
        query = wunderground_api.WundergroundQuery(place_id=place_id, begin=begin, end=end)

        goal = wunderground_api.get_rain(query)

        store.remove(query, store.WUNDERGROUND_RAIN)
        fresh_data = store.read(query, store.WUNDERGROUND_RAIN)
        cached_data = store.read(query, store.WUNDERGROUND_RAIN)

        pdt.assert_series_equal(fresh_data, goal)
        pdt.assert_series_equal(cached_data, goal)


class RemoveTestCase(TestCase):

    def test_remove_flickr_query(self):

        query = FlickrQuery(woe_id=flickr_api.WOE_ID_SWITZERLAND, year=2012)
        store_type = store.N_PHOTOS

        path = store._get_storage_path(query, store_type)
        if os.path.exists(path):
            os.remove(path)
        store.read(query, store.N_PHOTOS)

        self.assertTrue(os.path.exists(path))

        store.remove(query, store_type)
        self.assertFalse(os.path.exists(path))
