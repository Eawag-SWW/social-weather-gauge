from datetime import date
from apis import wunderground_api

__author__ = 'dominic'

import unittest
import pandas.util.testing as pdt


class GetRainTest(unittest.TestCase):

    def test_london_(self):

        url = '''http://www.wunderground.com/history/airport/EGLL/ \
            2015/8/25/CustomHistory.html?dayend=2&monthend=9&yearend=2015 \
            &req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic= \
            &reqdb.wmo=&MR=1&format=1'''

        goal = wunderground_api._get_rain_from_url(url)

        begin = date(2015, 8, 25)
        end = date(2015, 9, 2)
        actual = wunderground_api.get_rain('EGLL', begin, end)

        pdt.assert_series_equal(actual, goal)

