from datetime import date
from unittest import TestCase
import os

import pandas.util.testing as pdt

from apis import wunderground_api, flickr_api
from apis.flickr_api import FlickrQuery
from main import store


class RemoveTestCase(TestCase):

    def test_remove_flickr_query(self):

        query = FlickrQuery(woe_id=flickr_api.WOE_ID_SWITZERLAND, year=2012)

        store_type = store.N_PHOTOS
        storage_path = store._get_storage_path(store_type, query)
        print(storage_path)
        if os.path.exists(storage_path):
            os.remove(storage_path)
        store.read(store.N_PHOTOS, query)

        self.assertTrue(os.path.exists(storage_path))

        store.remove(store_type, query)
        self.assertFalse(os.path.exists(storage_path))


class WundergroundTestCase(TestCase):

    def test_london_data_storage(self):

        begin = date(2015, 9, 10)
        end = date(2015, 9, 20)
        place_id='EGLL'
        query = wunderground_api.WundergroundQuery(place_id=place_id, begin=begin, end=end)

        goal = wunderground_api.get_rain(query)

        store.remove(store.WUNDERGROUND_RAIN, query)
        fresh_data = store.read(store.WUNDERGROUND_RAIN, query)
        cached_data = store.read(store.WUNDERGROUND_RAIN, query)

        pdt.assert_series_equal(fresh_data, goal)
        pdt.assert_series_equal(cached_data, goal)
